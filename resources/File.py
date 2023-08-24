import os
import uuid
import traceback
from Model import db
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required
from Model import FileModel, FileModelSchema
from utils.utils import get_extension_from_path, delete_file


# Usada para manipulação de arquivos em um aplicativo Flask que usa Flask-RESTful para criar uma API REST.
class File(Resource):

# verifica se a extensão do arquivo é permitida com base na extensão do arquivo fornecido. 
# A lista de extensões permitidas é definida como ALLOWED_EXTENSIONS.
    ALLOWED_EXTENSIONS = {'csv'}

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

# obtém o tamanho do arquivo em bytes usando o módulo os.stat.
    def get_file_size(self, upload_folder, file_id):
        file_length = os.stat(f"{upload_folder}/{file_id}").st_size
        
        return file_length

# método que tenta inserir informações sobre o arquivo no banco de dados. Ele cria uma instância do modelo FileModel,
# adiciona-a à sessão do banco de dados, comita a sessão e retorna os dados inseridos.
    def insert_on_database(self, data):
        try:
            model = FileModel(
                file_id=data['id'],
                filename=data['filename'],
                extension=data['extension'],
                size=data['size']
            )

            db.session.add(model)
            db.session.commit()

            schema = FileModelSchema()
            data = schema.dump(model)

            return data
        except:
            traceback.print_exc()
            return None

# lida com solicitações POST para a rota associada ao recurso File. Ele verifica se há um arquivo na solicitação e, se for o caso,
# salva-o na pasta de upload do aplicativo. Em seguida, cria um dicionário de dados sobre o arquivo, incluindo seu ID, nome do arquivo,
# extensão, tamanho e URL, e insere esses dados no banco de dados usando insert_on_database. Retorna os dados inseridos.
    @jwt_required
    def post(self):
        try:
            if 'file' not in request.files:
                return {'msg': 'No file part'}, 500

            file = request.files['file']
            extension = get_extension_from_path(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
            file_id = f"{str(uuid.uuid4())}{extension}"

            if file and self.allowed_file(file.filename):
                file.save(os.path.join(upload_folder, file_id))
            else:
                return {'msg': 'Extension file invalid'}, 500
            
            data = {
                'id': file_id,
                'filename': file.filename,
                'extension': extension.replace('.', ''),
                'size': self.get_file_size(upload_folder, file_id),
                'url': f"{upload_folder}/{file_id}"
            }

            model = self.insert_on_database(data)

            return model
        except:
            traceback.print_exc()
            return {'msg': f"Error on save file"}, 500

# Lida com solicitações DELETE para a rota associada ao recurso File. Ele obtém o registro do arquivo do banco de dados,
# Obtém o caminho do arquivo a partir do registro, exclui o arquivo e o registro do banco de dados. 
# Retorna True se a operação for bem-sucedida.
    @jwt_required
    def delete(self, key):
        try:
            file = FileModel.query.filter_by(id=key).first()
            path = f"{current_app.config.get('UPLOAD_FOLDER')}/{file.file_id}"
            delete_file(path)
            
            db.session.delete(file)
            db.session.commit()

            return True
        except:
            traceback.print_exc()
            return {'msg': f"Error on delete file"}, 500

# classe parece ser usada para gerenciar o upload, armazenamento e exclusão de arquivos em um aplicativo
# Flask que usa Flask-RESTful para criar uma API REST, além de interagir com um banco de dados para armazenar informações sobre esses arquivos.
#  As operações são protegidas por autenticação JWT.

# req(file)
# res(updated_at, created_at, id, file_id, extension, size)