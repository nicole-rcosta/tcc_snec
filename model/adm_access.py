from database.conexao import conectar
import bcrypt

def buscar_adm(id_usuario, senha):
    """
        Busca usuários com o cargo de administrador.
    """
    
    conexao, cursor = conectar()

    try:
        # busca usuário cadastrado pelo id
        sql = """
            SELECT id_usuario, cargo, senha
            FROM db_snec.tb_usuarios
            WHERE id_usuario = %s;
        """
        cursor.execute(sql, (id_usuario, ))
        adm = cursor.fetchone()

        # verifica se o usuário foi puxado 
        if not adm:
            return {"sucesso": False, "mensagem": "Acesso negado!."}

        # verifica se o cargo do usuário é 'adm'
        cargo = adm['cargo']
        if cargo != "adm":
            return {"sucesso": False, "mensagem": "Acesso negado!."}

        # verifica senha do usuário
        senha_hash_banco = adm['senha']
        senha_bytes = senha.encode('utf-8')
        hash_banco_bytes = senha_hash_banco.encode('utf-8')

        if bcrypt.checkpw(senha_bytes, hash_banco_bytes):
            return {"sucesso": True, "mensagem": "Acesso liberado!."}
        else:
            return {"sucesso": False, "mensagem": "Senha incorreta!"}
            
    # Trata erros 
    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def buscar_usuario_pendente():
    """
            Busca usuários com a aprovação pendente.
    """

    conexao, cursor = conectar()

    # Busca usuários com aprovação pendente
    try:
        sql = """
            SELECT id_usuario, nome_usuario, cargo
            FROM db_snec.tb_usuarios
            WHERE status = "pendente";
        """

        cursor.execute(sql)
        usuarios_pendentes = cursor.fetchall()

        # Verifica se o comando SQL conseguiu puxar
        if not usuarios_pendentes:
            return {"sucesso": False, "mensagem": "Nenhum usuário pendente!"}
        else:
            return {"sucesso": True, "mensagem": usuarios_pendentes}

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def aprovar_usuario(id):
    """
            Atualiza usuários pendentes para aprovados.
    """
    conexao, cursor = conectar()

    try:
        # Atualiza status do usuário para 'aprovado' pelo id
        sql = """
            UPDATE db_snec.tb_usuarios
            SET status = 'aprovado'
            WHERE id_usuario = %s;
        """

        aprovar = cursor.execute(sql, (id, ))
        if aprovar:
            return {"sucesso": True, "mensagem": "Usuário Aprovado!"}
        else:
            return {"sucesso": False, "mensagem": "Erro. Tente Novamente!"}

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.commit()
            conexao.close()

def rejeitar_usuario(id):
    """
                Atualiza usuários pendentes para desaprovados.
    """
    conexao, cursor = conectar()
    # Atualiza status do usuário para 'desaprovado' pelo id
    try:
        sql = """
            UPDATE db_snec.tb_usuarios
            SET status = 'desaprovado'
            WHERE id_usuario = %s;
        """

        aprovar = cursor.execute(sql, (id, ))
        if aprovar:
            return {"sucesso": True, "mensagem": "Acesso negado ao usuário!"}
        else:
            return {"sucesso": False, "mensagem": "Erro. Tente Novamente!"}

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.commit()
            conexao.close()
    