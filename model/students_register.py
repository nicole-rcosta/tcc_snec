from database.conexao import conectar

def adicionar_aluno(rm:int, nome_aluno:str, id_turma:int) -> bool:
    """Adicona o aluno com as informações passadas através dos parâmetros."""

    cursor, conexao = None
    conexao,cursor = conectar()

    try:
        sql = """
            INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma)
            VALUES (%s,%s, %s);
        """
     
        cursor.execute(sql, (rm, nome_aluno, id_turma))
        conexao.commit()

    except Exception as erro:
        print(f"Erro ao atualizar senha: {erro}")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def recuperar_alunos():
    """Função que busca os alunos cadastrados."""

    cursor, conexao = None
    conexao,cursor = conectar()

    try:
        sql = """
            SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma FROM db_snec.tb_alunos
            INNER JOIN tb_turmas 
            ON tb_alunos.id_turma = tb_turmas.id_turma
            ORDER BY
            tb_alunos.nome_aluno;
        """

        cursor.execute(sql)
        alunos=cursor.fetchall()
        return alunos

    except Exception as erro:
        print(f"Erro ao atualizar senha: {erro}")
        if conexao:
            conexao.rollback()
        return False
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def deletar_aluno(rm:str) -> bool:
    """Deleta o aluno com as informações passadas através dos parâmetros."""

    cursor, conexao = None
    conexao, cursor = conectar()

    try:
        sql = """DELETE FROM tb_alunos WHERE rm_aluno = (%s);"""
        cursor.execute(sql, (rm,))
        conexao.commit()
        return {"sucesso": True, "mensagem": "Aluno deletado!"}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        
        if conexao:
            conexao.rollback()
        if "1451" in str(erro) or "foreign key constraint" in str(erro).lower():
            return {"sucesso": False, "mensagem": "Não é possível excluir: este aluno está cadastrado em uma atividade."}
            
        print(f"Erro ao deletar sala (ID: {rm}): {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()