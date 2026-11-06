import pandas
from database.conexao import conectar
import mysql.connector

def inserir_excel_bcd(arquivo):
    """Insere alunos por meio de uma planilha."""

    cursor, conexao = None
    conexao, cursor = conectar()

    try:
        extensao =  arquivo.filename.rsplit('.', 1)[1].lower()

        if extensao == 'csv':
            arquivo.seek(0)
            dados = pandas.read_csv(arquivo, sep=';')
        else:
            dados = pandas.read_excel(arquivo)

        dados = dados.dropna(how='all')  

        if dados.empty:
            print("Planinha em branco ou sem registros válidos")
            return False

        alunos = dados.to_dict('records')

        sql = "INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma) VALUES "

        for aluno in alunos:
            if pandas.isna(aluno.get('rm')) or pandas.isna(aluno.get('nome')) or pandas.isna(aluno.get('turma')):
                continue

            sql = sql  + f"""(
                                '{aluno['rm']}',
                                '{aluno['nome']}',
                                (SELECT id_turma FROM tb_turmas WHERE turma = '{aluno['turma']}')
                            ),"""

        if sql.endswith("VALUES "): 
            cursor.close()
            conexao.close()
            return False

        sql = sql.rstrip(',') + ';'

        # Executa os inserts
        cursor.execute(sql)
        # Salva as alterações
        conexao.commit()
    
        cursor.close()
        conexao.close()

        return True

    except (mysql.connector.errors.IntegrityError, mysql.connector.errors.ProgrammingError, pandas.errors.EmptyDataError) as e:
        print(f"Erro ao processar planilha/banco: {e}")
        return False
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False