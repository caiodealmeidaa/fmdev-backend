import traceback
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required


# usada para obter informações sobre DISCIPLINAS com base em filtros de CURSOS
class Subject(Resource):


# Ele obtém os dados da solicitação usando request.get_json()
# Gera uma cláusula SQL WHERE com base no filtro de CURSOS fornecido.
# Monta uma consulta SQL para recuperar os nomes das disciplinas que pertencem aos CURSOS especificados.
# Utiliza a função utils.execute_query para executar a consulta e retornar os resultados.
    @jwt_required
    def post(self):
        try:
            where = ''
            payload = request.get_json()

            if 'courses' in payload and len(payload['courses']) > 0:
                courses = utils.list_to_sql_string(payload['courses'])
                where = f"WHERE curso IN ({courses})"

            query = f"""SELECT 
                            nome_da_disciplina as label, 
                            nome_da_disciplina as value 
                        FROM moodle
                        {where}
                        GROUP BY nome_da_disciplina
                        ORDER BY nome_da_disciplina"""
            
            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on get Subject"}, 500
        

#req(COURSE)
#res(DISCIPLINAS)