import traceback
from Model import db
from Model import Lms, LmsSchema
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# responsável por lidar com as operações relacionadas a um LMS por meio de uma API REST
class LmsResource(Resource):

# lida com solicitações POST para a rota associada ao recurso LmsResource.
# recebe dados JSON da solicitação, cria um novo objeto Lms com base nesses dados e o insere no banco de dados.
# retorna um objeto JSON contendo o nome e a data de criação do LMS recém-criado.
    @jwt_required
    def post(self):
        try:
            data = request.get_json()

            lms = Lms(
                name=data['name'],
                url=data['url'],
                token=data['token'],
                version=data['version']
            )

            db.session.add(lms)
            db.session.commit()

            schema = LmsSchema(only=("name", "created_at"))
            result = schema.dump(lms)

            return result

        except:
            traceback.print_exc()
            return None, 500
#  lida com solicitações GET para a rota associada ao recurso LmsResource.
#  recupera todos os registros do LMS do banco de dados
#  e retorna uma lista de objetos JSON representando esses registros.
    @jwt_required
    def get(self):
        try:
            res = Lms.query.order_by(Lms.id).with_entities(
                Lms.id, Lms.name, Lms.description, Lms.url, Lms.token, Lms.version).all()

            schema = LmsSchema(many=True)
            data = schema.dump(res)

            return data

        except:
            traceback.print_exc()
            return None, 500

# lida com solicitações PUT para a rota associada ao recurso LmsResource. 
# recebe dados JSON da solicitação, recupera um objeto Lms com base no ID fornecido e atualiza os campos url,
# token e version com os novos valores fornecidos nos dados JSON. 
# retorna uma lista atualizada de objetos JSON representando os registros do LMS.
    @jwt_required
    def put(self):
        try:
            payload = request.get_json()

            lms = Lms.query.filter_by(id=payload['id']).first()

            if 'url' in payload:
                lms.url = payload['url']

            if 'token' in payload:
                lms.token = payload['token']

            if 'version' in payload:
                lms.version = payload['version']

            db.session.add(lms)
            db.session.commit()

            return self.get()

        except:
            traceback.print_exc()
            return None, 500


# usada para fornecer uma API REST que permite a criação, leitura e atualização de registros de LMS, 
# com as operações protegidas por autenticação JWT.


# GET:
# res(INFOS DO LMS)
