from database.conexao import conectar
from datetime import date

datas = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}

def buscar_turmas():
    """Recupera todas as turmas cadastradas."""

    conexao, cursor = conectar()
    
    try:
        sql = """
            SELECT id_turma, turma 
            FROM tb_turmas;
        """
        cursor.execute(sql)
        turmas = cursor.fetchall()

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

def buscar_qntd_alunos(id_turma:int) -> bool:
    """Recupera quantidade de alunos das turmas pelo ID."""
    
    conexao, cursor = conectar()

    try:
        sql = """
            SELECT quantidade_alunos 
            FROM tb_turmas 
            WHERE id_turma = %s;
        """
        cursor.execute(sql, (id_turma, ))
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

def buscar_alunos(id_turma:int) -> dict:
    """Recuperam alunos pelo ID das turmas."""

    conexao, cursor = conectar()

    try:
        hoje_num = date.today().weekday()
        dia_semana = datas.get(hoje_num, 'SEG')

        sql = """
            SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma, tb_atividades.atividade, tb_atividades.periodo, COALESCE (tb_his_almoco.atendido, TRUE) AS status
            FROM tb_alunos
            INNER JOIN tb_turmas ON tb_alunos.id_turma = tb_turmas.id_turma
            INNER JOIN tb_aluno_atividade ON tb_alunos.rm_aluno = tb_aluno_atividade.rm_aluno
            INNER JOIN tb_atividades ON tb_aluno_atividade.id_atividade = tb_atividades.id_atividade 
            LEFT JOIN tb_his_almoco 
            ON tb_alunos.rm_aluno = tb_his_almoco.rm_aluno 
            AND tb_his_almoco.data = CURRENT_DATE()
            WHERE tb_turmas.id_turma = %s
            AND tb_aluno_atividade.dia_semana = %s;
        """

        cursor.execute(sql, (id_turma, dia_semana, ))
        alunos = cursor.fetchall()

        if alunos:
            return {"sucesso": True, "alunos": alunos}
        else:
            return {"sucesso": False, "mensagem": "Nenhum aluno cadastrado em atividades hoje."}
    
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

def salvar_his_lanche(id_turma:int, quantidade_alunos:int, id_usuario:int) -> bool:
    """Envia os dados informados do lanche para o banco de dados."""

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
        if conexao:
            conexao.rollback()
        print(f"Erro ao cadastrar usuário: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def salvar_his_almoco(id_usuario:int, rms_contraturnos) -> bool:
    """Envia os dados informados do almoço para o banco de dados."""

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
        if conexao:
            conexao.rollback()
        print(f"Erro ao cadastrar usuário: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def existe_his_lanche(id_turma):
    """Retorna True se já existe registro de lanche da turma hoje, senão False."""

    conexao, cursor = conectar()

    try:
        sql = """
            SELECT 1 FROM tb_his_lanche
            WHERE id_turma = %s
            AND data = CURRENT_DATE()
            LIMIT 1;
        """
        cursor.execute(sql, (id_turma, ))
        return cursor.fetchone() is not None

    except Exception as error:
        if conexao:
            conexao.rollback()
        print(f"Erro ao cadastrar usuário: {error}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()