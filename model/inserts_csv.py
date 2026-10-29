import pandas
import mysql.connector
from database.conexao import conectar


def inserir_excel_bcd(arquivo):
    try:
        extensao = arquivo.filename.rsplit('.', 1)[1].lower()


        if extensao == 'csv':
            arquivo.seek(0)
            dados = pandas.read_csv(arquivo, sep=';')
        else:
            dados = pandas.read_excel(arquivo)


        # 1. REMOVE LINHAS COMPLETAMENTE VAZIAS DA PLANILHA
        dados = dados.dropna(how='all')


        # 2. BLOQUEIO DE PLANILHA EM BRANCO OU SÓ COM CABEÇALHO
        if dados.empty:
            print("Planilha em branco ou sem registros válidos.")
            return False


        alunos = dados.to_dict('records')
        
        conexao, cursor = conectar()


        sql = "INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma) VALUES "


        for aluno in alunos:
            if pandas.isna(aluno.get('rm')) or pandas.isna(aluno.get('nome')) or pandas.isna(aluno.get('turma')):
                continue


            sql += f"""(
                '{aluno['rm']}',
                '{aluno['nome']}',
                (SELECT id_turma FROM tb_turmas WHERE turma = '{aluno['turma']}')
            ),"""


        # Se nenhuma linha válida foi processada, encerra sem executar SQL inválida
        if sql.endswith("VALUES "):
            cursor.close()
            conexao.close()
            return False


        sql = sql.rstrip(',') + ';'


        
        cursor.execute(sql)
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