import traceback
import pandas as pd
from utils import utils
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required



# usada para obter informações sobre alunos com base em filtros de cursos, disciplinas, semestres e períodos
class Student(Resource):

# where = '': Inicializa a cláusula WHERE da consulta SQL como uma string vazia.
# payload = request.get_json(): Obtém os dados JSON da solicitação POST.
    @jwt_required
    def post(self):
        try:
            where = ''
            payload = request.get_json()
# Em seguida, começa a construir uma cláusula WHERE para filtrar os resultados do banco de dados com base nas informações fornecidas na solicitação:
# Verifica se a chave 'courses' está presente nos dados JSON e se não está vazia.
            if 'courses' in payload and len(payload['courses']) > 0:
# Converte a lista de cursos em uma string no formato adequado para uso em uma cláusula SQL.
                courses = utils.list_to_sql_string(payload['courses'])
# Adiciona à cláusula WHERE a restrição de cursos.
                where = f"WHERE curso IN ({courses})"

# Repete a lógica acima para 'subjects', 'semesters' e 'periods' para adicionar as restrições correspondentes à cláusula WHERE.
            if 'subjects' in payload and len(payload['subjects']) > 0:
                subjects = utils.list_to_sql_string(payload['subjects'])

                if where != '':
                    where += f" AND nome_da_disciplina IN ({subjects})"
                else:
                    where = f"WHERE nome_da_disciplina IN ({subjects})"

            if 'semesters' in payload and len(payload['semesters']) > 0:
                semesters = utils.list_to_sql_string(payload['semesters'])

                if where != '':
                    where += f" AND semestre IN ({semesters})"
                else:
                    where = f"WHERE semestre IN ({semesters})"

            if 'periods' in payload and len(payload['periods']) > 0:
                periods = utils.list_to_sql_string(payload['periods'])

                if where != '':
                    where += f" AND período IN ({periods})"
                else:
                    where = f"WHERE período IN ({periods})"


# Após construir a cláusula WHERE com base nos filtros, o código monta uma consulta SQL:
# Gera uma consulta SQL que seleciona os nomes dos alunos da tabela 'moodle' aplicando as restrições da cláusula WHERE,
# agrupando pelo nome do aluno e ordenando por nome do aluno.
            query = f"""SELECT 
                            nome_do_aluno as label, 
                            nome_do_aluno as value 
                        FROM moodle
                        {where}
                        GROUP BY nome_do_aluno
                        ORDER BY nome_do_aluno"""
# Por fim, a consulta SQL é executada usando a função utils.execute_query(query), que é suposta retornar os resultados da consulta.
            return utils.execute_query(query)

        except:
            traceback.print_exc()
            return {"msg": "Error on GET Student"}, 500


# req(COURSES, SUBJECTS, SEMESTERS)
# res(ALUNOS)