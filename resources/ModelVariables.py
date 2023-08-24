import json
import traceback
import pandas as pd
from flask_restful import Resource
from flask import current_app
from flask_jwt_extended import jwt_required

# usada para obter as variáveis do modelo de um arquivo CSV contendo dados de teste
class ModelVariables(Resource):


# recebe um parâmetro key (chave), que parece ser o nome do arquivo CSV contendo os dados de teste do modelo.
# O método lê o arquivo CSV com base no nome da chave e no tipo de divisão 'TEST_FEATURES'.
# cria um DataFrame do Pandas usando os dados do arquivo CSV.
# constrói uma estrutura de dados JSON contendo as variáveis do modelo a partir do primeiro registro do DataFrame.
# O resultado é retornado como um dicionário JSON contendo a estrutura de dados com as variáveis do modelo.
    # @jwt_required
    def get(self, key):
        try:
            filename, split_type = key, 'TEST_FEATURES'

            filename = f"{current_app.config.get(split_type)}/{filename}.csv"
            df = pd.read_csv(filename)

            data = {
                'data': [df.iloc[0].to_dict()]
            }
            # json.dumps(data)

            return {'data': data}

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Model Variables"}, 500
