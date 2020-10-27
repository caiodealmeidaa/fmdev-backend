import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class Period(Resource):

    @jwt_required
    def post(self):
        try:
            where = ''
            payload = request.get_json()

            if 'subjects' in payload and len(payload['subjects']) > 0:
                subjects = utils.list_to_sql_string(payload['subjects'])
                where = f"WHERE nome_da_disciplina IN ({subjects})"

            if 'semesters' in payload and len(payload['semesters']) > 0:
                semesters = utils.list_to_sql_string(payload['semesters'])

                if where != '':
                    where += f" AND semestre IN ({semesters})"
                else:
                    where = f"WHERE semestre IN ({semesters})"

            query = f"""SELECT 
                            período as label, 
                            período as value 
                        FROM moodle
                        {where}
                        GROUP BY período
                        ORDER BY período"""

            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Period"}, 500
