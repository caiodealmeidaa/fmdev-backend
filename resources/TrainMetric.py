import joblib
import traceback
import pandas as pd
from utils import utils
from flask_restful import Resource
from sklearn.metrics import SCORERS
from flask import request, current_app
from flask_jwt_extended import jwt_required

CLASSIFICATION_METRICS = [
    {'type': 'accuracy', 'name': 'Acurácia'},
    {'type': 'balanced_accuracy', 'name': 'Balanced accuracy'},
    {'type': 'average_precision', 'name': 'Average precision'},
    {'type': 'neg_brier_score', 'name': 'Neg brier score'},
    {'type': 'f1', 'name': 'F1'},
    {'type': 'f1_micro', 'name': 'F1 micro'},
    {'type': 'f1_macro', 'name': 'F1 macro'},
    {'type': 'f1_weighted', 'name': 'F1 weighted'},
    {'type': 'f1_samples', 'name': 'F1 samples'},
    {'type': 'neg_log_loss', 'name': 'Neg log loss'},
    {'type': 'precision', 'name': 'Precision'},
    {'type': 'recall', 'name': 'Recall'},
    {'type': 'jaccard', 'name': 'Jaccard'},
    {'type': 'roc_auc', 'name': 'Roc auc'},
    {'type': 'roc_auc_ovr', 'name': 'Roc auc ovr'},
    {'type': 'roc_auc_ovo', 'name': 'Roc auc ovo'},
    {'type': 'roc_auc_ovr_weighted', 'name': 'Roc auc ovr weighted'},
    {'type': 'roc_auc_ovo_weighted', 'name': 'Roc auc ovo weighted'}
]

# CLUSTERING_METRICS = [
#     {'type': 'accuracy', 'name': 'Acurácia'},
#     {'type': 'balanced_accuracy', 'name': 'Balanced accuracy'},
#     {'type': 'average_precision', 'name': 'Average precision'},
#     {'type': 'neg_brier_score', 'name': 'Neg brier score'},
#     {'type': 'f1', 'name': 'F1'},
#     {'type': 'f1_micro', 'name': 'F1 micro'},
#     {'type': 'f1_macro', 'name': 'F1 macro'},
# ]

# recurso da API REST usado para calcular várias métricas de avaliação para um modelo treinado usando o algoritmo TPOT. 
class TrainMetric(Resource):

# Obtém os dados de teste (features ou target) a partir dos arquivos CSV correspondentes.
    def get_test_data(self, split_type):
        filename = utils.get_filename_from_path(request, '.csv')
        filename = f"{current_app.config.get(split_type)}/{filename}"
        data = pd.read_csv(filename)

        return data

#  Calcula as métricas de avaliação para um modelo treinado usando os dados de teste fornecidos.
    def get_metrics(self, tpot, x_test, y_test):
        metrics = []

        for item in CLASSIFICATION_METRICS:
            try:
                metrics.append({'name': item['name'],
                                'value': SCORERS[item['type']](tpot, x_test, y_test)
                                })
            except:
                pass

        return metrics

# Carrega o modelo treinado a partir do arquivo .sav correspondente.
    def load_model(self):
        filename = utils.get_filename_from_path(request, '')
        path = f"{current_app.config.get('TRAIN_MODELS')}/{filename}.sav"
        loaded_model = joblib.load(open(path, 'rb'))

        return loaded_model

# Calcula as métricas de avaliação para um modelo treinado usando os dados de teste
# e retorna uma lista de dicionários contendo as métricas calculadas.
    @jwt_required
    def post(self):
        try:
            data = []
            tpot = self.load_model()
            x_test = self.get_test_data('TEST_FEATURES')
            y_test = self.get_test_data('TEST_TARGET')
            metrics = self.get_metrics(tpot, x_test, y_test)

            return metrics

        except:
            traceback.print_exc()
            return {"msg": "Error on POST Metric"}, 500

# req(PATH arquivo pre-processamento)
# res(METRICAS)