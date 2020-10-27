import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class Student(Resource):

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

            if 'semesters' in payload and len(payload['semesters']) > 0:
                semesters = utils.list_to_sql_string(payload['semesters'])

                if where != '':
                    where += f" AND semestre IN ({semesters})"
                else:
                    where = f"WHERE semestre IN ({semesters})"

            if 'periods' in payload and len(payload['periods']) > 0:
                periods = utils.list_to_sql_string(payload['periods'])

                if where != '':
                    where += f" AND período IN ({periods})"
                else:
                    where = f"WHERE período IN ({periods})"

            query = f"""SELECT 
                            nome_do_aluno as label, 
                            nome_do_aluno as value 
                        FROM moodle
                        {where}
                        GROUP BY nome_do_aluno
                        ORDER BY nome_do_aluno"""

            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Student"}, 500
