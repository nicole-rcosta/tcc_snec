from database.conexao import conectar
from datetime import datetime

datas = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}

def buscar_alunos(dia_semana, id_turma):
    conexao, cursor = conectar

    
    hoje_num = datetime.date.today().weekday()
    dia_semana = datas.get(hoje_num, 'SEG')

    cursor.execute("""SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma, tb_atividades.atividade, tb_atividades.periodo, COALESCE (tb_his_almoco.atendido, FALSE) AS status
    FROM tb_alunos
    INNER JOIN tb_turmas ON tb_alunos.id_turma = tb_turmas.id_turma
    INNER JOIN tb_aluno_atividade ON tb_alunos.rm_aluno = tb_aluno_atividade.rm_aluno
    INNER JOIN tb_atividades ON tb_aluno_atividade.id_atividade = tb_atividades.id_atividade 
    LEFT JOIN tb_his_almoco 
    ON tb_alunos.rm_aluno = tb_his_almoco.rm_aluno 
    AND tb_his_almoco.data = CURRENT_DATE()
    WHERE tb_turmas.id_turma = %s
    AND tb_aluno_atividade.dia_semana = %s; """, (dia_semana, id_turma, ))
    
    alunos = cursor.fetchall()
    cursor.close()
    conexao.close()

    return alunos



