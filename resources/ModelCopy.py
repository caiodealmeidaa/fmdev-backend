import json
import joblib
import traceback
import pandas as pd
from utils import utils
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required
from resources.TrainModel import TrainModelResource


# usada para copiar um modelo de aprendizado de máquina treinado e fazer previsões usando esse modelo copiado. 
class ModelCopy(Resource):


# método que recebe um parâmetro key (chave) e um parâmetro data.
# constrói e retorna um template de comando cURL com base na chave e nos dados fornecidos.
# O template de cURL parece ser usado para enviar uma solicitação POST para a API de previsão do modelo.
    def get_curl_template(self, key, data):
        model = TrainModelResource.get_by_id(key)

        template = f"""curl --location --request POST '{current_app.config.get('BASE_URL')}/api/predict/{key}' \
                        --header 'Fmdev-Api-Key: {model.api_key}' \
                        --header 'Accept: application/json, text/plain, */*' \
                        --header 'Content-Type: application/json;charset=UTF-8' \
                        --header 'Content-Type: text/plain' \
                        --data-raw '{json.dumps(data)}'"""
        return template

# recebe um nome de arquivo e um tipo de divisão (split_type). 
# lê o arquivo CSV correspondente ao tipo de divisão e retorna um DataFrame do Pandas contendo os dados de teste.
    def get_df_test_data(self, filename, split_type):
        filename = f"{current_app.config.get(split_type)}/{filename}.csv"
        df = pd.read_csv(filename)

        return df

# obtém os dados de teste do DataFrame, cria uma estrutura de dados para esses dados e, em seguida, 
# gera um template de comando cURL usando a função get_curl_template(). 
# O resultado é retornado como um dicionário JSON contendo o template de cURL.
    @jwt_required
    def get(self, key):
        try:
            df = self.get_df_test_data(key, 'TEST_FEATURES')

            data = {
                'data': [df.iloc[0].to_dict()]
            }

            template = self.get_curl_template(key, data)

            return { 'template': template }

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Copy"}, 500


# usada para obter dados de teste de um modelo treinado, construir um template de comando cURL 
# para fazer previsões com o modelo e retornar esse template como uma resposta JSON.

# GET
# res(CURL do modelo)