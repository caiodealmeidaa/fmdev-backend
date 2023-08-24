import traceback
import pandas as pd
from utils import utils
from flask import request, current_app, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# Usada para lidar com o download de arquivos(relacionados a pipelines de treinamento ou arquivos CSV)
# em um aplicativo Flask que usa Flask-RESTful para criar uma API REST.
class Download(Resource):

    # Obtém o parâmetro de consulta action da solicitação HTTP e retorna a extensão de arquivo apropriada com base na ação.
    # Se a ação for igual a 'TRAIN_PIPELINES', retorna 'py', caso contrário, retorna 'csv'.
    def get_extension_by_file_action(self):
        file_action = request.args['action']

        if file_action == 'TRAIN_PIPELINES':
            return 'py'
        
        return 'csv'

    # Lida com solicitações GET para a rota associada ao recurso Download. Ele obtém o parâmetro de consulta action da solicitação HTTP
    # e a extensão de arquivo apropriada usando o método get_extension_by_file_action().
    # Em seguida, ele constrói o caminho completo do arquivo a ser baixado usando a configuração de current_app e o nome do arquivo e a extensão derivada.
    # Finalmente, ele usa a função send_file para enviar o arquivo como uma resposta de download anexado.

    @jwt_required
    def get(self, key):
        try:
            file_action = request.args['action']
            extension = self.get_extension_by_file_action()
            path = f"{current_app.config.get(file_action)}/{key}.{extension}"

            return send_file(path, as_attachment=True)
            
        except:
            traceback.print_exc()
            return {"msg": "Error on GET Download"}, 500

# Usada para lidar com o download de arquivos (possivelmente relacionados a pipelines de treinamento ou arquivos CSV) em um aplicativo Flask que usa Flask-RESTful para criar uma API REST.


# res(BAIXA O CSV)