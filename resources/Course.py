import traceback
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# obter informações sobre cursos a partir de um banco de dados ou fonte de dados específica
class Course(Resource):

# obtém os dados do JSON da solicitação. Verifica se a chave 'datasource' está presente nos dados. 
# Se estiver presente, ele constrói uma consulta SQL que busca informações sobre cursos de uma fonte de dados especificada (payload['datasource']).
# A consulta seleciona os cursos únicos da fonte de dados, agrupa-os por curso e os ordena por curso. Em caso de sucesso, retorna os resultados da consulta
# como uma lista de cursos no formato de rótulos e valores. Se ocorrer um erro durante o processamento, ele captura exceções, imprime o rastreamento do erro
# e retorna uma mensagem de erro.
    @jwt_required
    def post(self):
        try:
            payload = request.get_json()

            if 'datasource' not in payload:
                return {'msg': 'Datasource not found'}, 500

            query = f"""SELECT 
                            curso as label, 
                            curso as value 
                        FROM {payload['datasource']}
                        GROUP BY curso
                        ORDER BY curso"""

            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on POST Course"}, 500


# Geralmente, essa classe é usada como parte de um serviço da web Flask que fornece uma API
# para obter informações sobre cursos de uma fonte de dados específica, como um banco de dados, 
# e retornar essas informações como uma lista de cursos para uso posterior.

# req(FONTE DE DADOS)
# res(CURSOS)