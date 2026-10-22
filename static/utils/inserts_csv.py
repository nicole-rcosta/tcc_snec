import pandas
import mysql.connector as sql

def conectar():
    conexao = sql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="db_snec"
    )

    #Criando o cursor
    cursor = conexao.cursor(dictionary=True)
    return conexao, cursor

# Lê o arquivo Excel
dados = pandas.read_excel('static/utils/alunos.xls')

alunos = dados.to_dict('records')


conexao,cursor = conectar()

cursor = conexao.cursor()

sql = "INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma) VALUES "

for aluno in alunos:
    sql = sql  + f"""(
                        '{aluno['rm']}',
                        '{aluno['nome']}',
                        (SELECT id_turma FROM tb_turmas WHERE turma = '{aluno['turma']}')
                    ),"""

sql = sql.rstrip(',') + ';'

# Executa os inserts
cursor.execute(sql)

# Salva as alterações
conexao.commit()

cursor.close()
conexao.close()





