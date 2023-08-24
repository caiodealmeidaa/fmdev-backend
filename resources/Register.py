import datetime
from Model import db
from run import bcrypt
from flask import request
from Model import User
from flask_restful import Resource



# usada para criar um novo usuário no sistema
class Register(Resource):

# Ele obtém os dados da solicitação POST usando request.get_json().
# Usa o módulo datetime para obter a data e hora atuais.
# Cria um objeto User com os dados fornecidos na solicitação e a senha hashed usando o bcrypt.
# Adiciona o objeto User ao banco de dados usando o objeto db e, em seguida, realiza o commit da sessão.
# Retorna informações sobre o usuário recém-criado, incluindo nome de usuário, email e timestamps de criação e atualização.
    def post(self):
        data = request.get_json()
        now = datetime.datetime.now()

        user = User(
            username=data['username'],
            password=bcrypt.generate_password_hash(
                data['password']).decode('utf-8'),
            email=data['email'],
            created_at=now,
            updated_at=now
        )

        db.session.add(user)
        db.session.commit()

        return {"data": {
            "username": user.username,
            "email": user.email,
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": now.strftime("%Y-%m-%d %H:%M:%S")
        }}


# Esse código aparentemente faz parte de um sistema de autenticação e registro de usuários em uma aplicação Flask,
# onde os dados do usuário são armazenados em um banco de dados e as senhas são armazenadas com segurança usando o hash bcrypt.