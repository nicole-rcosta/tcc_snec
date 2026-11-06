from database.conexao import conectar

def recuperar_atividade():
    """
                Recupera atividades já cadastradas.
    """
    try: 
        conexao, cursor = conectar()
        cursor.execute("SELECT id_atividade, atividade, periodo FROM tb_atividades")
        atividades = cursor.fetchall()
        conexao.close()
        return atividades
  
    except Exception as erro:
        print(erro)
        return False

def cadastrar_atividade(atividade, periodo):
    """
            Cadastra atividades.
    """
    
    try:
        conexao, cursor = conectar()
        cursor.execute("INSERT INTO tb_atividades (atividade, periodo) VALUES (%s, %s);", (atividade, periodo))
        conexao.commit()
        conexao.close()
        return True

    except Exception as erro:
        print(erro)
        return False

def excluir_atividade(id_atividade):
    """
        Exclui ativdades por ID
    """

    conexao, cursor = conectar()

    try:
        cursor.execute("""DELETE FROM tb_atividades WHERE id_atividade = %s;""", (id_atividade, ) )
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