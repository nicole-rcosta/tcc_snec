from database.conexao import conectar
import datetime

def buscar_alunos():
    conexao, cursor = conectar

    datas = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}
    hoje_num = datetime.date.today().weekday()

    cursor.execute("""SELECT rm_aluno, nome_aluno, turma, atividade, periodo, atendido FROM tb_alunos
    INNER JOIN tb_turmas ON tb_alunos.id_turma = tb_turmas.id_turma
    INNER JOIN tb_aluno_atividade tb_aluno_atividade ON tb_alunos.rm_aluno = tb_aluno_atividade.rm_aluno
    INNER JOIN tb_atividades ON tb_aluno_atividade.id_atividade = tb_atividades.id_atividade; """)







    cursor.close()
    conexao.close()