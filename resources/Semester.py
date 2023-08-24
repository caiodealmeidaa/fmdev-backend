import traceback
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required


# Usada para obter informações sobre os semestres de cursos ou disciplinas em um sistema
class Semester(Resource):


# Ele obtém os dados da solicitação POST usando request.get_json().
# Gera uma cláusula SQL WHERE com base nos filtros de cursos e disciplinas fornecidos.
# Monta uma consulta SQL para recuperar os semestres relacionados aos cursos e disciplinas filtrados.
# Usa a função utils.execute_query(query) para executar a consulta no banco de dados.
# Retorna os resultados da consulta, que são os semestres encontrados.
    @jwt_required
    def post(self):
        try:
            where = ''
            payload = request.get_json()

            if 'courses' in payload and len(payload['courses']) > 0:
                courses = utils.list_to_sql_string(payload['courses'])
                where = f"WHERE curso IN ({courses})"

            if 'subjects' in payload and len(payload['subjects']) > 0:
                subjects = utils.list_to_sql_string(payload['subjects'])

                if where != '':
                    where += f" AND nome_da_disciplina IN ({subjects})"
                else:
                    where = f"WHERE nome_da_disciplina IN ({subjects})"

            query = f"""SELECT 
                            semestre as label, 
                            semestre as value 
                        FROM moodle
                        {where}
                        GROUP BY semestre
                        ORDER BY semestre"""

            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Semester"}, 500
        

# Se houver algum erro durante o processo, o bloco except capturará a exceção, imprimirá o rastreamento de pilha
# e retornará uma mensagem de erro junto com um código de status HTTP 500 (Internal Server Error).

# req(DISCIPLINAS)
# res(SEMESTER)