from database.conexao import conectar
from datetime import date

datas = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}

def buscar_alunos(id_turma):
    conexao, cursor = conectar()

    try:
    
        hoje_num = date.today().weekday()
        dia_semana = datas.get(hoje_num, 'SEG')

        cursor.execute("SELECT quantidade_alunos FROM tb_turmas WHERE id_turma = %s", (id_turma, ))
        info = cursor.fetchone()

        if info:
            formato = info['quantidade_alunos'] if isinstance(info, dict) else info[0]
        else: 
            formato = 0


        cursor.execute("""SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma, tb_atividades.atividade, tb_atividades.periodo, COALESCE (tb_his_almoco.atendido, TRUE) AS status
        FROM tb_alunos
        INNER JOIN tb_turmas ON tb_alunos.id_turma = tb_turmas.id_turma
        INNER JOIN tb_aluno_atividade ON tb_alunos.rm_aluno = tb_aluno_atividade.rm_aluno
        INNER JOIN tb_atividades ON tb_aluno_atividade.id_atividade = tb_atividades.id_atividade 
        LEFT JOIN tb_his_almoco 
        ON tb_alunos.rm_aluno = tb_his_almoco.rm_aluno 
        AND tb_his_almoco.data = CURRENT_DATE()
        WHERE tb_turmas.id_turma = %s
        AND tb_aluno_atividade.dia_semana = %s; """, (id_turma, dia_semana, ))
        
        alunos = cursor.fetchall()
        return formato, alunos


    finally:
        cursor.close()
        conexao.close()


def alunos_presentes(rms_atendidos):
    if not rms_atendidos:
        return[]

    conexao, cursor = conectar()

    try:
        placeholder = ', '.join(['%s'] * len(rms_atendidos))
        cursor.execute(f"SELECT rm_aluno, nome_aluno FROM tb_alunos WHERE rm_aluno IN ({placeholder})", tuple(rms_atendidos))
        alunos_presentes = cursor.fetchall()
        return alunos_presentes

    finally:    
        cursor.close()
        conexao.close()



def salvar_presenca(id_turma, quantidade_alunos, id_usuario, rms_atendidos, rms_contraturnos):
    conexao, cursor = conectar()

    try:
        query_lanche = """
                        INSERT INTO tb_his_lanche (id_turma, data, id_usuario, quantidade_alunos)
                        VALUES (%s, CURRENT_DATE(), %s, %s)
                        ON DUPLICATE KEY UPDATE
                        quantidade_alunos = VALUES(quantidade_alunos),
                        id_usuario = VALUES(id_usuario);  
                    """
        cursor.execute(query_lanche, (id_turma, id_usuario, quantidade_alunos))

        query_almoco = """
                        INSERT INTO tb_his_almoco (rm_aluno, data, id_usuario, atendido)
                        VALUES(%s, CURRENT_DATE(), %s, %s)
                        ON DUPLICATE KEY UPDATE
                        atendido = VALUES(atendido),
                        id_usuario = VALUES(id_usuario);
                    """
        for rm in rms_contraturnos:
            atendido = rm in rms_atendidos
            cursor.execute(query_almoco, (rm, id_usuario, atendido))
        

        conexao.commit()
        return True
    

    except Exception as error:
        conexao.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        conexao.close()






