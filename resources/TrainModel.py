import secrets
import traceback
from Model import db
from utils import utils
from datetime import datetime
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required
from Model import TrainModel, TrainModelSchema



# usado para lidar com operações relacionadas a modelos de treinamento.
class TrainModelResource(Resource):

# Obtém um objeto TrainModel pelo ID.
    def get_by_id(key):
        try:
            return TrainModel.query.filter_by(model_id=key).first()
        except:
            traceback.print_exc()
            return {}

# Atualiza as informações do modelo após uma previsão ser feita, como a última vez 
# que a previsão foi feita e a quantidade total de previsões feitas.
    def update_predict(key):
        try:
            model = TrainModel.query.filter_by(model_id=key).first()

            model.last_predict_at = datetime.utcnow()

            if model.qtd_predict is None:
                model.qtd_predict = 0
            else:
                model.qtd_predict += 1

            db.session.add(model)
            db.session.commit()

            return True
        except:
            traceback.print_exc()
            return False

# método que lida com solicitações GET para a rota associada ao recurso TrainModelResource.
# Retorna uma lista de modelos de treinamento associados ao usuário autenticado.
    @jwt_required
    def get(self):
        try:
            user_id = utils.get_user_id(request)
            res = TrainModel.query.filter_by(user_id=user_id).all()

            schema = TrainModelSchema(exclude=['api_key'], many=True)
            data = schema.dump(res)

            return data

        except:
            traceback.print_exc()
            return None, 500

# método que lida com solicitações POST para a rota associada ao recurso TrainModelResource.
# Cria um novo modelo de treinamento associado ao usuário autenticado.
    @jwt_required
    def post(self):
        try:
            user_id = utils.get_user_id(request)
            model_id = utils.get_filename_from_path(request, '')

            data = request.get_json()

            train_model = TrainModel(
                name=data['name'],
                description=data['description'],
                model_id=model_id,
                score=data['score'],
                user_id=user_id,
                api_key=secrets.token_hex()
            )

            db.session.add(train_model)
            db.session.commit()

            return self.get()

        except:
            traceback.print_exc()
            return [], 500
    
# Um método que lida com solicitações PUT para a rota associada ao recurso TrainModelResource.
# Atualiza informações sobre um modelo de treinamento específico.
    @jwt_required
    def put(self, key):
        try:
            payload = request.get_json()
          
            model = TrainModel.query.filter_by(model_id=key).first()

            if 'action' in payload and payload['action'] == 'GENERATE_KEY':
                 model.api_key = secrets.token_hex()

            db.session.add(model)
            db.session.commit()

            return self.get()
        
        except:
            traceback.print_exc()
            return [], 500

# lida com solicitações DELETE para a rota associada ao recurso TrainModelResource.
# Deleta um modelo de treinamento específico e seus arquivos associados.
    @jwt_required
    def delete(self, key):
        try:
            model = TrainModel.query.filter_by(model_id=key).first()

            utils.delete_model_files(key)
            utils.delete_file(f"{current_app.config.get('PRE_PROCESSING_RAW')}/{key}.csv")
            db.session.delete(model)
            db.session.commit()

            return self.get()

        except:
            traceback.print_exc()
            return {'msg': f"Error to delete train model"}, 500

# req(description, name, path, score)
# res(updated_at, user_id, name, created_at, qtd_predict, description, last_predict_at, model_id, id, score)