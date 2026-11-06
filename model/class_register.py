from database.conexao import conectar

def adicionar_sala(turma:str, periodo:str, qnt_alunos:int) -> bool:
    """Adicona a sala com as informações passadas através dos parâmetros."""

    cursor, conexao = None
    conexao,cursor = conectar()

    try:
        sql = """
            SELECT turma FROM tb_turmas
            WHERE turma = %s;
        """
        cursor.execute(sql, (turma, ))
        turma_result = cursor.fetchone()

        if turma_result:
            return {"sucesso": True, "erro": "Esta turma já está cadastrada."}
        else:
            cursor.execute("""INSERT INTO tb_turmas (turma, periodo, quantidade_alunos)
                                VALUES (%s,%s,%s);""",(turma, periodo, qnt_alunos) )
            conexao.commit()
            return {"sucesso": True, "mensagem": "Turma cadastrada com sucesso."}
            
    
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

def recuperar_salas():
    """Recupera salas já cadastradas."""

    cursor, conexao = None
    conexao,cursor = conectar()

    try:
        sql = """SELECT id_turma, turma, periodo, quantidade_alunos FROM db_snec.tb_turmas ORDER BY turma;"""
        cursor.execute(sql)
        salas = cursor.fetchall()
        return salas

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

def deletar_sala(cod:int) -> bool:
    """Deleta salas já cadastradas."""

    cursor, conexao = None
    conexao,cursor = conectar()

    try:
        sql = """DELETE FROM tb_turmas WHERE id_turma = (%s);"""
        cursor.execute(sql, (cod, ))
        conexao.commit()
        return {"sucesso": True, "mensagem": "Sala deletada!"}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        
        if conexao:
            conexao.rollback()
        if "1451" in str(erro) or "foreign key constraint" in str(erro).lower():
            return {
                "sucesso": False, 
                "mensagem": "Não é possível excluir: existem alunos cadastrados nesta sala."
            }
            
        print(f"Erro ao deletar sala (ID: {cod}): {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()