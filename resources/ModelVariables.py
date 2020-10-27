import json
import traceback
import pandas as pd
from flask_restful import Resource
from flask import current_app
from flask_jwt_extended import jwt_required

class ModelVariables(Resource):

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
