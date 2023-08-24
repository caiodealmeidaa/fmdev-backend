import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

#  Lida com a geração de dados de gráficos a partir de um arquivo CSV. 
class Chart(Resource):

    # Função que recebe o caminho do arquivo CSV e o indicador que será usado
    def get_csv_data(self, path, indicator):
        res = {'status': 'success'}

        try:
            df = pd.read_csv(path)
            res['data'] = df[indicator]
        except:
            res['status'] = 'error'

        return res

    # obtém os dados do JSON da solicitação, verifica se o caminho do arquivo CSV e o 
    # indicador estão presentes nos dados. Se estiverem presentes, chama o método get_csv_data
    # para obter os dados do indicador a partir do arquivo CSV e retorna esses dados como uma lista.
    # Em caso de erro, ele captura exceções, imprime o rastreamento do erro e retorna uma mensagem de erro.
    @jwt_required
    def post(self):
        try:
            path = None
            payload = request.get_json()

            if 'path' not in payload or payload['path'] is None:
                return {"msg": "Invalid path"}, 500

            res = self.get_csv_data(payload['path'], payload['indicator'])

            if res['status'] == 'error':
                return {"msg": "Invalid path"}, 500

            return res['data'].tolist()
        except:
            traceback.print_exc()
            return {"msg": "Error on POST Chart"}, 500

# Geralmente, essa classe é usada como parte de um serviço da web Flask que fornece uma API 
# para obter dados de um arquivo CSV específico com base no indicador solicitado. 
# Esses dados podem ser usados para plotar gráficos ou gerar visualizações.
