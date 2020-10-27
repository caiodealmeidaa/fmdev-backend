import traceback
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class Semester(Resource):

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