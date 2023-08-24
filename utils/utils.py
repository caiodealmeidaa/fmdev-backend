import os
import jwt
import json
import math
import shutil
import traceback
import pandas as pd
from Model import db
from flask import current_app

# Esta função executa uma consulta SQL e retorna os resultados em formato JSON ou DataFrame Pandas.
# Ela aceita dois argumentos: query, que é a consulta SQL a ser executada, e mode, que indica se os resultados
# devem ser retornados como JSON ('sql') ou como um DataFrame Pandas ('pandas').
def execute_query(query, mode='sql'):

    data = []

    res = db.engine.execute(query)

    for item in res:
        data.append(item)

    df = pd.DataFrame(data, columns=res.keys())

    if mode == 'pandas':
        return df

    data = df.to_json(orient='records', force_ascii=False)
    data = json.loads(data)

    return data

#  converte uma lista de strings em uma string formatada para ser usada em cláusulas SQL IN.
#  aceita uma lista de strings chamada data e retorna uma string no formato "'item1', 'item2', ...".
def list_to_sql_string(data):
    string = ''

    string = "', '".join(data)
    string = f"'{string}'"

    return string

# tenta converter um valor para um float com duas casas decimais. Ela lida com casos em que o valor é None ou NaN.
# Aceita um valor chamado value e retorna o valor como um float com duas casas decimais.
def to_float(value):
    if value is None or math.isnan(value) == True:
        return None

    new_value = "%.2f" % value
    new_value = float(new_value)

    return new_value

#  exclui um arquivo do sistema de arquivos se ele existir. Aceita um caminho de arquivo chamado path
#  e verifica se o arquivo existe antes de excluí-lo.
def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"The file {path} does not exist")

# extrai o ID do usuário do token JWT fornecido no cabeçalho da solicitação. Aceita um objeto request
# do Flask contendo o cabeçalho da solicitação e retorna o ID do usuário, se estiver presente no token.
def get_user_id(request):
    user_id = None
    encoded_jwt = request.headers['Authorization']
    encoded_jwt = encoded_jwt.replace('Bearer ', '')

    decoded_jwt = jwt.decode(encoded_jwt, verify=False)

    if 'identity' in decoded_jwt:
        if 'id' in decoded_jwt['identity']:
            user_id = decoded_jwt['identity']['id']

    return user_id

# obtém o nome de arquivo a partir do caminho fornecido no corpo da solicitação e substitui a extensão pelo valor fornecido.
# Aceita um objeto request do Flask contendo o corpo da solicitação e a extensão desejada.
def get_filename_from_path(request, extension):
    payload = request.get_json()
    path = payload['path']
    filename = os.path.basename(path).replace('.csv', extension)

    return filename

#  exclui vários arquivos e pastas associados a um modelo treinado. Aceita um nome de arquivo filename e exclui os arquivos de saída, modelo,
#  características de treinamento, destino de treinamento, características de teste e destino de teste, bem como o arquivo de pipeline associado.
def delete_model_files(filename):
    shutil.rmtree(
        f"{current_app.config.get('TRAIN_TPOT_OUTPUT')}/{filename}", ignore_errors=True)
    delete_file(
        f"{current_app.config.get('TRAIN_MODELS')}/{filename}.sav")
    delete_file(
        f"{current_app.config.get('TRAIN_FEATURES')}/{filename}.csv")
    delete_file(
        f"{current_app.config.get('TRAIN_TARGET')}/{filename}.csv")
    delete_file(
        f"{current_app.config.get('TEST_FEATURES')}/{filename}.csv")
    delete_file(
        f"{current_app.config.get('TEST_TARGET')}/{filename}.csv")
    delete_file(
        f"{current_app.config.get('TRAIN_PIPELINES')}/{filename}.py")

# extrai a extensão de um nome de arquivo. Aceita um nome de arquivo chamado filename e retorna a extensão do arquivo.
def get_extension_from_path(filename):
    filename, file_extension = os.path.splitext(filename)

    return file_extension

# Essas funções fornecem uma variedade de utilidades para manipular dados, arquivos e autenticação em um aplicativo Flask.
# Elas são usadas em diferentes partes do código para melhorar a legibilidade, modularidade e reutilização do código.