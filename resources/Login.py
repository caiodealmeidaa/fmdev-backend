import datetime
from Model import db
from Model import User
from run import bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

# usada para lidar com o processo de autenticação de usuários por meio de uma API REST
class Login(Resource):

# Método que lida com solicitações POST para a rota associada ao recurso Login.
# obtém o email e a senha do JSON da solicitação. 
# Em seguida, consulta o banco de dados para recuperar os dados do usuário (ID, senha e nome de usuário)
# com base no email fornecido. Se o usuário não for encontrado, ele retorna um erro de "Usuário não encontrado". 
# Caso contrário, ele verifica se a senha fornecida coincide com a senha armazenada usando a função check_password_hash do objeto bcrypt.
# Se as senhas coincidirem, ele cria um token de acesso JWT para o usuário e retorna um JSON contendo o token, o tipo de token e,
# opcionalmente, um token de atualização. Se as senhas não coincidirem, ele retorna um erro de "Nome de usuário e senha inválidos".

    def post(self):
        email = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query \
            .with_entities(User.id, User.password, User.username) \
            .filter_by(email=email).first()
        
        if user is None:
            return {"error": "User not found"}, 401

        if bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(
                identity={'username': user.username, 'id': user.id}, expires_delta=False)
            result = {
                "refresh_token": None,
                "token": access_token,
                "type": "bearer"}
        else:
            result = {"error": "Invalid username and password"}, 401

        return result


# usada para autenticar os usuários por meio de uma API REST, gerando tokens de acesso JWT se a autenticação for bem-sucedida.

# req(email, password)
# res(refresh_token, token, type)