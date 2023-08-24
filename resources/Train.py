
import os
import joblib
import traceback
import numpy as np
import pandas as pd
from utils import utils
from tpot import TPOTClassifier
from flask_restful import Resource
from dask.distributed import Client
from flask import request, current_app
from flask_jwt_extended import jwt_required
from sklearn.metrics import make_scorer, SCORERS
from sklearn.model_selection import train_test_split


# destinado a treinar modelos de aprendizado de máquina usando o algoritmo TPOT.
class Train(Resource):


# Retorna a lista de pipelines usados a partir do resultado da execução do TPOT.
    def get_used_pipeline(self, tpot):
        pipelines = []

        for item in tpot.pareto_front_fitted_pipelines_:
            algorithm = item.split('(', 1)[0]
            params = item.split('(', 1)[1]
            params = params.replace(f"{algorithm}__", '')
            params_splitted = params.split(', ')
            pipelines.append({
                'algorithm': algorithm,
                'hyperparameters': params_splitted
            })

        return pipelines

# Realiza o treinamento do modelo TPOT com os dados de treinamento fornecidos.
    def train(self, x_train, y_train, generations, kfold):
        client = Client(processes=False)
        output_folder = f"{current_app.config.get('TRAIN_TPOT_OUTPUT')}/{self.get_filename_from_path('')}"

        tpot = TPOTClassifier(generations=generations,
                              population_size=20, cv=kfold,
                              random_state=42, verbosity=3,
                              use_dask=True,
                              periodic_checkpoint_folder=output_folder)

        with joblib.parallel_backend("dask"):
            tpot.fit(x_train, y_train)

        return tpot

# Obtém um DataFrame a partir dos dados CSV fornecidos na solicitação.
    def get_dataframe_from_csv(self):
        payload = request.get_json()

        path = payload['path']
        df = pd.read_csv(path)

        return df

#  Obtém um DataFrame sem codificação one-hot para as colunas categóricas.
    def get_df_without_one_hot_encoding(self, target):
        df = self.get_dataframe_from_csv()
        df_categoric = df.copy()
        df_categoric = df_categoric.select_dtypes(include=['object'])
        df = df.drop(df_categoric.columns, axis=1)
        df_x = df.copy()

        del df_x[target]

        return df, df_x

#  Obtém um DataFrame sem codificação one-hot para as colunas categóricas.
    def get_filename_from_path(self, extension):
        payload = request.get_json()
        path = payload['path']
        filename = os.path.basename(path).replace('.csv', extension)

        return filename


# Salva o modelo treinado em um arquivo com extensão .sav.
    def save(self, tpot):
        filename = self.get_filename_from_path('.sav')
        filename = f"{current_app.config.get('TRAIN_MODELS')}/{filename}"
        joblib.dump(tpot.fitted_pipeline_, open(filename, 'wb'))

 # Exporta o melhor pipeline treinado para um arquivo com extensão .py.
    def export(self, tpot):
        filename = self.get_filename_from_path('.py')
        filename = f"{current_app.config.get('TRAIN_PIPELINES')}/{filename}"
        tpot.export(filename)

# Salva conjuntos de dados (treinamento/teste) em arquivos CSV.
    def save_split(self, df, split_type):
        filename = self.get_filename_from_path('.csv')
        filename = f"{current_app.config.get(split_type)}/{filename}"

        df.to_csv(filename, index=False)

# Um método que lida com solicitações POST para a rota associada ao recurso Train. 
# Realiza o treinamento do modelo TPOT com base nos dados fornecidos e retorna informações sobre o treinamento.
    @jwt_required
    def post(self):
        try:
            payload = request.get_json()
            mandatory_fields = ['train', 'test', 'generations', 'path', 'target']

            for field in mandatory_fields:
                if field not in payload:
                    return {'msg': f'{field} not found'}, 500

            train = payload['train'] / 100
            test = payload['test'] / 100
            target = payload['target']
            generations = payload['generations']
            kfold = payload['kfold']

            df, df_x = self.get_df_without_one_hot_encoding(target)

            x_train, x_test, y_train, y_test = train_test_split(
                df_x, df[target], train_size=train, test_size=test)

            tpot = self.train(x_train, y_train, generations, kfold)

            self.save(tpot)
            self.export(tpot)
            self.save_split(x_train, 'TRAIN_FEATURES')
            self.save_split(y_train, 'TRAIN_TARGET')
            self.save_split(x_test, 'TEST_FEATURES')
            self.save_split(y_test, 'TEST_TARGET')

            return {
                "score": tpot.score(x_test, y_test),
                "qtd_evaluated_pipelines": len(tpot.evaluated_individuals_),
                "fitted_pipelines": self.get_used_pipeline(tpot)
            }

        except:
            traceback.print_exc()
            return {"msg": "Error on POST Train"}, 500

# método que lida com solicitações DELETE para a rota associada ao recurso Train. 
# Exclui os arquivos relacionados ao modelo treinado.
    @jwt_required
    def delete(self):
        try:
            filename = self.get_filename_from_path('')
            utils.delete_model_files(filename)

            return {'msg': 'Deleted with successful'}

        except:
            traceback.print_exc()
            return {"msg": "Error on DELETE Train"}, 500


# req(generations, kfold, path, target, test, train)
# res(score, qtd_evaluated_pipelines, fitted_pipelines)