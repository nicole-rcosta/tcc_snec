from database.conexao import conectar

def recuperar_atividade():
    """Recupera atividades já cadastradas."""

    conexao, cursor = conectar()

    try: 
        sql = """SELECT id_atividade, atividade, periodo FROM tb_atividades;"""
        cursor.execute(sql)
        atividades = cursor.fetchall()
        return atividades
  
    except Exception as erro:
        print(erro)
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def cadastrar_atividade(atividade, periodo):
    """Cadastra atividades."""

    conexao, cursor = conectar()
    
    try:
        sql = """INSERT INTO tb_atividades (atividade, periodo) VALUES (%s, %s);"""
        cursor.execute(sql, (atividade, periodo))
        conexao.commit()
        return True

    except Exception as erro:
        print(erro)
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    
def excluir_atividade(id_atividade):
    """Exclui ativdades por ID."""

    conexao, cursor = conectar()

    try:
        sql = """DELETE FROM tb_atividades WHERE id_atividade = %s;"""
        cursor.execute(sql, (id_atividade, ) )
        conexao.commit()
        return {"sucesso": True, "mensagem": "Atividade deletada!"}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        
        if conexao:
            conexao.rollback()
        if "1451" in str(erro) or "foreign key constraint" in str(erro).lower():
            return {
                "sucesso": False, 
                "mensagem": "Não é possível excluir: esta atividade está vinculada a um aluno."
            }
            
        print(f"Erro ao deletar sala (ID: {id_atividade}): {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()