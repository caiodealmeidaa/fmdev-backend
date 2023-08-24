import traceback
import pandas as pd
from utils import utils
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required
from Model import FileModel, DatasourceModel


# Classe responsável por fornecer uma lista de indicadores com base no contexto (LMS ou CSV)
class Indicator(Resource):

# obtém indicadores específicos de um LMS. Ele recebe o ID do LMS da solicitação JSON,
# cria uma consulta SQL para selecionar indicadores de um banco de dados com base no ID do LMS e retorna os resultados.
    def get_indicators_by_lms(self):
        lms_id = request.get_json()['id']

        query = f"""SELECT 
                        name as value,
                        description as label
                    FROM
                        indicators
                    WHERE 
                        lms='{lms_id}'
                    GROUP BY 
                        name, description, lms
                    ORDER BY
                        name
                    """
        
        return utils.execute_query(query)

# obtém indicadores de um arquivo CSV. Ele obtém o ID da fonte de dados da solicitação JSON, consulta o banco de dados
# para obter detalhes sobre o arquivo correspondente, lê o arquivo CSV usando pandas e cria uma lista de indicadores(?)
# a partir das colunas do DataFrame.   
    def get_indicators_by_csv(self):
        indicators = []
        id = request.get_json()['id']
        datasource = DatasourceModel.query.filter_by(id=id).first()
        file = FileModel.query.filter_by(id=datasource.file_id).first()

        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        path = f"{upload_folder}/{file.file_id}"

        df = pd.read_csv(path)

        for column in df.columns:
            indicators.append({
                'value': column,
                'label': column
            })

        return indicators

#  lida com solicitações POST para a rota associada ao recurso Indicator.
#  Ele verifica o contexto da solicitação JSON (LMS ou CSV) e chama o método correspondente para obter a lista de indicadores.
#  Retorna a lista de indicadores obtida ou uma lista vazia em caso de erro.
    @jwt_required
    def post(self):
        try:
            context = request.get_json()['context']

            if context == 'LMS':
                return self.get_indicators_by_lms()
            
            if context == 'CSV':
                return self.get_indicators_by_csv()
            
            return []
        except:
            traceback.print_exc()
            return {"msg": "Error on GET Indicator"}, 500
        
# usada para fornecer uma lista de indicadores com base no contexto (LMS ou CSV) por meio de uma API REST, onde as operações são protegidas por autenticação JWT.

#req(CONTEXT e ID) 
#res(colunas da tabela INDICADORES) -> return POST