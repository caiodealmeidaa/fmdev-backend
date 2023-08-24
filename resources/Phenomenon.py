import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# usada para obter informações sobre fenômenos ou modelos, possivelmente a partir de uma fonte de dados 
# como um banco de dados, e retornar essas informações em formato JSON
class Phenomenon(Resource):


# lida com solicitações GET para a rota associada ao recurso Phenomenon
# constrói uma consulta SQL que seleciona os campos model_id e name da tabela train_models, ordenando os resultados pelo campo name.
    @jwt_required
    def get(self):
        try:
            query = f"""SELECT 
                            model_id as value, 
                            name as label
                        FROM 
                            train_models
                        ORDER BY 
                            name"""

# retorna o resultado da consulta SQL usando a função utils.execute_query(query).
            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Phenomenon"}, 500

# res(Arquivo salvo do modelo treinado)