import pandas
from database.conexao import conectar

def inserir_excel_bcd(arquivo):

    extensao =  arquivo.filename.rsplit('.', 1)[1].lower()

    if extensao == 'csv':
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





