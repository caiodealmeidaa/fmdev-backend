from flask import Blueprint
from flask_restful import Api
from resources.Lms import LmsResource
from resources.Login import Login
from resources.Subject import Subject
from resources.Course import Course
from resources.Chart import Chart
from resources.Register import Register
from resources.Semester import Semester
from resources.Indicator import Indicator
from resources.PreProcessing import PreProcessing
from resources.Train import Train
from resources.TrainStatus import TrainStatus
from resources.TrainModel import TrainModelResource
from resources.TrainMetric import TrainMetric
from resources.ModelCopy import ModelCopy
from resources.Predict import Predict
from resources.Download import Download
from resources.Datasource import Datasource
from resources.File import File
from resources.Phenomenon import Phenomenon
from resources.ModelVariables import ModelVariables
from resources.Student import Student
from resources.Period import Period
#from resources.Cluster import Cluster


# Criadas as rotas da API Flask
# Cada recurso da API (como login, registro, treinamento de modelo, etc.) é associado a uma rota específica.
# Isso facilita a organização e a manutenção do código, permitindo que cada recurso seja definido em seu próprio arquivo e,
# em seguida, importado aqui para construir as rotas.
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
# As linhas subsequentes adicionam cada recurso à API usando o método add_resource. 
# Cada recurso é mapeado para uma rota específica
api.add_resource(Login, '/auth/login')
api.add_resource(File, '/file', '/file/<string:key>')
api.add_resource(Register, '/auth/register')
api.add_resource(LmsResource, '/lms')
api.add_resource(Subject, '/subject')
api.add_resource(Course, '/course')
api.add_resource(Semester, '/semester')
api.add_resource(Indicator, '/indicator')
api.add_resource(PreProcessing, '/pre-processing')
api.add_resource(Chart, '/chart')
api.add_resource(Train, '/train')
api.add_resource(TrainStatus, '/train-status')
api.add_resource(TrainModelResource, '/train-model', '/train-model/<string:key>')
api.add_resource(TrainMetric, '/train-metric')
api.add_resource(ModelCopy, '/model-copy/<string:key>')
api.add_resource(Predict, '/predict/<string:key>')
api.add_resource(Download, '/download/<string:key>')
api.add_resource(Datasource, '/data-source', '/data-source/<string:key>')
api.add_resource(Phenomenon, '/phenomenon')
api.add_resource(ModelVariables, '/model-variables/<string:key>')
api.add_resource(Period, '/period')
api.add_resource(Student, '/student')
#api.add_resource(Cluster, '/cluster')

# Esse padrão de organização de código é muito útil para projetos maiores, pois ajuda a manter a estrutura limpa e escalável, facilitando a adição de novos recursos e a manutenção dos existentes. 
# Cada recurso é definido em seu próprio arquivo e pode ser gerenciado independentemente.
