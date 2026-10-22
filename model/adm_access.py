from database.conexao import conectar
import bcrypt

def buscar_adm(id_usuario, senha):
    conexao, cursor = conectar()

    try:
        sql = """
            SELECT id_usuario, cargo, senha
            FROM db_snec.tb_usuarios
            WHERE id_usuario = %s;
        """
        cursor.execute(sql, (id_usuario, ))
        adm = cursor.fetchone()

        if not adm:
            return {"sucesso": False, "mensagem": "Acesso negado!."}

        cargo = adm['cargo']
        if cargo != "adm":
            return {"sucesso": False, "mensagem": "Acesso negado!."}

        senha_hash_banco = adm['senha']
        senha_bytes = senha.encode('utf-8')
        hash_banco_bytes = senha_hash_banco.encode('utf-8')

        if bcrypt.checkpw(senha_bytes, hash_banco_bytes):
            return {"sucesso": True, "mensagem": "Acesso liberado!."}
        else:
            return {"sucesso": False, "mensagem": "Senha incorreta!"}
            

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def buscar_usuario_pendente():
    conexao, cursor = conectar()

    try:
        sql = """
            SELECT nome_usuario, cargo
            FROM db_snec.tb_usuarios
            WHERE status = "pendente";
        """

        cursor.execute(sql)
        usuarios_pendentes = cursor.fetchall()

        if not usuarios_pendentes:
            return {"sucesso": False, "mensagem": "Nenhum usuário pendente!."}
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
    