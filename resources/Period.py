import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required


# lida com solicitações POST para filtrar e retornar dados de períodos acadêmicos.
# usada para obter os períodos de tempo a partir de uma fonte de dados, possivelmente um banco de dados, 
# e retornar esses períodos em formato JSON
class Period(Resource):

# O método começa analisando os dados JSON recebidos na solicitação.
# constrói uma cláusula WHERE vazia.
    @jwt_required
    def post(self):
        try:
            where = ''
            payload = request.get_json()
# Verifica se há uma lista de disciplinas (subjects) nos dados JSON e se essa lista não está vazia.
# Se sim, ele transforma essa lista em uma string de SQL usando a função utils.list_to_sql_string() e 
# adiciona uma cláusula WHERE à string where.
            if 'subjects' in payload and len(payload['subjects']) > 0:
                subjects = utils.list_to_sql_string(payload['subjects'])
                where = f"WHERE nome_da_disciplina IN ({subjects})"


# Verifica se há uma lista de semestres (semesters) nos dados JSON e se essa lista não está vazia.
# Se sim, ele transforma essa lista em uma string de SQL usando a função utils.list_to_sql_string(). 
# Se where já estiver preenchida, ele acrescenta uma cláusula AND à string where, caso contrário,
# cria uma nova cláusula WHERE com base nos semestres.
            if 'semesters' in payload and len(payload['semesters']) > 0:
                semesters = utils.list_to_sql_string(payload['semesters'])

                if where != '':
                    where += f" AND semestre IN ({semesters})"
                else:
                    where = f"WHERE semestre IN ({semesters})"

# Constrói uma consulta SQL com base nas cláusulas where e outras condições, selecionando os períodos (label e value) da tabela moodle.
# A consulta é ordenada por período.
            query = f"""SELECT 
                            período as label, 
                            período as value 
                        FROM moodle
                        {where}
                        GROUP BY período
                        ORDER BY período"""

# retorna o resultado da consulta SQL usando a função utils.execute_query(query).
            return utils.execute_query(query)


# Se ocorrer um erro durante a execução, ele imprime as informações de traceback e
# retorna uma mensagem de erro junto com um código de status 500.
        except:
            traceback.print_exc()
            return {"msg": "Error on GET Period"}, 500
