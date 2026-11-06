import pandas
from database.conexao import conectar
import mysql.connector

def inserir_excel_bcd(arquivo):
    """
        Insere alunos por meio de uma planilha.
    """
    try:
        extensao =  arquivo.filename.rsplit('.', 1)[1].lower()

        if extensao == 'csv':
            arquivo.seek(0)
            try:
                # Tenta ler primeiro em UTF-8 auto-detectando o separador (, ; ou \t)
                dados = pandas.read_csv(arquivo, sep=None, engine='python', encoding='utf-8')
            except (UnicodeDecodeError, pandas.errors.ParserError):
                # Se falhar a decodificação UTF-8 (como no caso do símbolo °), tenta latin1
                arquivo.seek(0)
                dados = pandas.read_csv(arquivo, sep=None, engine='python', encoding='latin1')
        else:
            dados = pandas.read_excel(arquivo)


        dados = dados.dropna(how='all')  

        if dados.empty:
            print("Planinha em branco ou sem registros válidos")
            return False

        alunos = dados.to_dict('records')
        
        conexao, cursor = conectar()


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

    except mysql.connector.errors.IntegrityError as e :
        conexao, cursor = conectar()
        # Pega as salas que vieram na planilha
        salas_planilha = dados['turma'].dropna().unique().tolist()
        
        # Busca no banco quais salas existem de fato
        cursor.execute("SELECT turma FROM tb_turmas")
        salas_banco = [row['turma'] for row in cursor.fetchall()]
        
        # Filtra quais salas da planilha NÃO estão na lista do banco
        salas_invalidas = [sala for sala in salas_planilha if sala not in salas_banco]
        
        print(f"Erro: As seguintes salas não existem no banco: {salas_invalidas}")
        cursor.close()
        conexao.close()
        return salas_invalidas
        

    except (mysql.connector.errors.ProgrammingError, pandas.errors.EmptyDataError) as e:
        print(f"Erro ao processar planilha/banco: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False
