import secrets
import traceback
from Model import db
from utils import utils
from sqlalchemy import desc
from datetime import datetime
from resources.File import File
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required
from Model import FileModel, DatasourceModel, DatasourceModelSchema

# Essa classe será usada para definir o endpoint da API para interagir com fontes de dados (datasources)
# lida com solicitações GET, POST e DELETE relacionadas a fontes de dados (datasources)
class Datasource(Resource):

# lida com solicitações GET para a rota associada ao recurso Datasource. Ele tenta obter informações sobre as fontes de dados (datasources) do banco de dados. A consulta busca as colunas id, created_at, name e size da tabela DatasourceModel, bem como o tamanho do arquivo associado da tabela FileModel. 
# em seguida, a resposta é formatada como um esquema usando DatasourceModelSchema e retornada.
    @jwt_required
    def get(self):
        try:
            res = db.session.query(DatasourceModel.id, DatasourceModel.created_at,
                                   DatasourceModel.name, FileModel.size) \
                .join(FileModel, DatasourceModel.file_id == FileModel.id) \
                .order_by(desc(DatasourceModel.created_at)).all()

            schema = DatasourceModelSchema(many=True)
            data = schema.dump(res)

            return data

        except:
            traceback.print_exc()
            return {'msg': f"Error on list datasources"}, 500

# lida com solicitações POST para a rota associada ao recurso Datasource. Ele obtém os dados do JSON da solicitação e cria um novo objeto DatasourceModel com base nesses dados. O objeto é adicionado ao banco de dados e a sessão é confirmada.
# Em seguida, o método get() é chamado para retornar a lista atualizada de fontes de dados.
    @jwt_required
    def post(self):
        try:
            data = request.get_json()

            model = DatasourceModel(
                name=data['name'],
                file_id=data['file_id']
            )

            db.session.add(model)
            db.session.commit()

            return self.get()

        except:
            traceback.print_exc()
            return {'msg': f"Error on create datasource"}, 500
        
#  Lida com solicitações DELETE para a rota associada ao recurso Datasource. 
#  Ele recebe um parâmetro key que provavelmente se refere ao ID da fonte de dados a ser excluída.
#  O método tenta encontrar a fonte de dados e o arquivo associado no banco de dados.
#  Em seguida, ele exclui o arquivo físico, remove a fonte de dados e o arquivo do banco de dados e confirma a sessão.
#  Novamente, o método get() é chamado para retornar a lista atualizada de fontes de dados.
    @jwt_required
    def delete(self, key):
        try:
            datasource = DatasourceModel.query.filter_by(id=key).first()
            file = FileModel.query.filter_by(id=datasource.file_id).first()

            path = f"{current_app.config.get('UPLOAD_FOLDER')}/{file.file_id}"
            utils.delete_file(path)

            db.session.delete(datasource)
            db.session.commit()

            db.session.delete(file)
            db.session.commit()

            return self.get()

        except:
            traceback.print_exc()
            return {'msg': f"Error on delete datasource"}, 500

# classe parece ser usada para criar, listar e excluir fontes de dados (datasources) em um aplicativo Flask
# que usa Flask-RESTful para criar uma API REST. As operações são protegidas por autenticação JWT.

# req(file_id, name)
# res(name, id, created_at, size)