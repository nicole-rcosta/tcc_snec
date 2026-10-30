from database.conexao import conectar
from datetime import date

datas = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}

def buscar_turmas():
    conexao, cursor = conectar()
    
    try:
        cursor.execute("SELECT id_turma, turma FROM tb_turmas")
        turmas = cursor.fetchall()
        print(turmas)

        if turmas:
            return {"sucesso": True, "turmas": turmas}
        else:
            return {"sucesso": False, "mensagem": "Nenhuma turma cadastrada."}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()    

def buscar_qntd_alunos(id_turma):

    conexao, cursor = conectar()

    try:
        cursor.execute("SELECT quantidade_alunos FROM tb_turmas WHERE id_turma = %s", (id_turma, ))
        qntd_alunos = cursor.fetchone()

        return qntd_alunos

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def buscar_alunos(id_turma):

    conexao, cursor = conectar()

    try:
    
        hoje_num = date.today().weekday()
        dia_semana = datas.get(hoje_num, 'SEG')

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

        if alunos:
            return {"sucesso": True, "alunos": alunos}
        else:
            return {"sucesso": False, "mensagem": "Nenhum aluno cadastrado."}
    
    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
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


def salvar_his_lanche(id_turma, quantidade_alunos, id_usuario):
    conexao, cursor = conectar()

    try:

        query_lanche = """
                        INSERT INTO tb_his_lanche (id_turma, data, id_usuario, quantidade_alunos)
                        VALUES (%s, CURRENT_DATE(), %s, %s);
                    """
        cursor.execute(query_lanche, (id_turma, id_usuario, quantidade_alunos))

        conexao.commit()
        return True

    except Exception as error:
        conexao.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        conexao.close()

def salvar_his_almoco(id_usuario, rms_contraturnos):

    print(rms_contraturnos)

    conexao, cursor = conectar()

    try:
        
        query_almoco = """
                        INSERT INTO tb_his_almoco (rm_aluno, id_usuario, atendido)
                        VALUES(%s, %s, %s);
                    """
        # Itera diretamente pelos RMs selecionados e define atendido como False
        for rm in rms_contraturnos:
            cursor.execute(query_almoco, (rm, id_usuario, False))

        conexao.commit()
        return True

    except Exception as error:
        conexao.rollback()
        print(error)
        return False

    finally:
        cursor.close()
        conexao.close()

def buscar_his_lanche(id_turma):
    conexao, cursor = conectar()

    try:

        sql = """
            SELECT * FROM tb_his_lanche
            WHERE id_turma = %s
            AND data = CURRENT_DATE();
        """

        cursor.execute(sql, (id_turma, ))
        his = cursor.fetchone()

        if his:
            return {"sucesso": True, "mensagem": "O histórico dessa sala já foi salvo."}
        else:
            return {"sucesso": False, "mensagem": "O histórico do dia da turma já foi salvo."}

    except Exception as error:
        conexao.rollback()
        print(error)
        return {"sucesso": False, "mensagem": "Erro interno no servidor"}

    finally:
        cursor.close()
        conexao.close()