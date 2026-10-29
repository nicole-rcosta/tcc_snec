import pandas
from database.conexao import conectar
import mysql.connector

def inserir_excel_bcd(arquivo):
    try:
        extensao =  arquivo.filename.rsplit('.', 1)[1].lower()

        if extensao == 'csv':
            arquivo.seek(0)
            dados = pandas.read_csv(arquivo, sep=';')
        else:
            dados = pandas.read_excel(arquivo)

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

        return True

    except mysql.connector.errors.IntegrityError:
        print('derg9u')
        return False

    





