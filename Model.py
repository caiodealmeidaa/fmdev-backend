from datetime import datetime
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


#  O codigo a seguir descreve a estrutura das classes de modelo da sua aplicação. Essas classes são definidas usando o SQLAlchemy, que é uma biblioteca ORM (Object-Relational Mapping) para Python, e o Marshmallow, que é uma biblioteca para serialização/desserialização de objetos Python para JSON.

# Cria uma instância do Marshmallow para serialização/desserialização de objetos.
ma = Marshmallow()
# Cria uma instância do SQLAlchemy para gerenciar a interação com o banco de dados.
db = SQLAlchemy()


# Uma classe mixin que define os campos created_at e updated_at para adicionar automaticamente a data e hora de criação e atualização aos registros do banco de dados.
class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# Classe de modelo que representa a tabela de usuários no banco de dados. Possui campos como id, username, email, password, created_at e updated_at.
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, username, email, password, created_at, updated_at):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

# Classe de esquema para a serialização/desserialização de objetos do tipo User.
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

# Classe de modelo que representa a tabela LMS (Learning Management System) no banco de dados. Ela possui campos como id, name, description, url, token, version, created_at e updated_at.
class Lms(db.Model, TimestampMixin):
    __tablename__ = 'lms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    url = db.Column(db.Text())
    token = db.Column(db.Text())
    version = db.Column(db.String())

    def __init__(self, name, url, version, token):
        self.name = name
        self.url = url
        self.version = version
        self.token = token

# Classe de esquema para a serialização/desserialização de objetos do tipo Lms.
class LmsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    url = fields.String()
    token = fields.String()
    version = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

#  Classe de modelo que representa a tabela de indicadores no banco de dados. Possui campos como id, name, description, lms, created_at e updated_at.
class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True)
    description = db.Column(db.String(), nullable=False)
    lms = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, name, description, lms, created_at, updated_at):
        self.name = name
        self.description = description
        self.lms = lms
        self.created_at = created_at
        self.updated_at = updated_at

# Classe de esquema para a serialização/desserialização de objetos do tipo Indicator.
class IndicatorSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    lms = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

# Classe de modelo que representa a tabela de modelos de treinamento no banco de dados. Possui campos como id, name, description, model_id, score, api_key, qtd_predict, last_predict_at e user_id.
class TrainModel(db.Model, TimestampMixin):
    __tablename__ = 'train_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    model_id = db.Column(db.String(), nullable=False, index=True)
    score = db.Column(db.Float())
    api_key = db.Column(db.String())
    qtd_predict = db.Column(db.Integer(), default=0)
    last_predict_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, description, model_id, score, api_key, user_id):
        self.name = name
        self.description = description
        self.model_id = model_id
        self.score = score
        self.api_key = api_key
        self.user_id = user_id

# Classe de esquema para a serialização/desserialização de objetos do tipo TrainModel.
class TrainModelSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    user_id = fields.Integer()
    model_id = fields.String()
    score = fields.Float()
    api_key = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    qtd_predict = fields.Integer()
    last_predict_at = fields.DateTime()

# Classe de modelo que representa a tabela de fontes de dados no banco de dados. Possui campos como id, name, file_id, created_at e updated_at.
class DatasourceModel(db.Model, TimestampMixin):
    __tablename__ = 'datasources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)

    def __init__(self, name, file_id):
        self.name = name
        self.file_id = file_id

# Classe de esquema para a serialização/desserialização de objetos do tipo DatasourceModel.
class DatasourceModelSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    file_id = fields.Integer()
    size = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

# Classe de modelo que representa a tabela de arquivos no banco de dados. Possui campos como id, file_id, filename, extension, size, created_at e updated_at.
class FileModel(db.Model, TimestampMixin):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(), nullable=False)
    filename = db.Column(db.String(), nullable=False)
    extension =  db.Column(db.String(), nullable=False)
    size =  db.Column(db.Float(), nullable=False)

    def __init__(self, file_id, filename, extension, size):
        self.file_id = file_id
        self.filename = filename
        self.extension = extension
        self.size = size

# Classe de esquema para a serialização/desserialização de objetos do tipo FileModel.
class FileModelSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    file_id = fields.String()
    filename = fields.String()
    extension = fields.String()
    size = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# Essas classes de modelo são a base para a definição das tabelas do banco de dados e sua interação com a aplicação. O Marshmallow é usado para definir como esses objetos devem ser serializados (convertidos em JSON) e desserializados (convertidos de JSON para objetos). Isso é útil para a comunicação com APIs, manipulação de dados e validação de entrada/saída.