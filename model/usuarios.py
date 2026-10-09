from database.conexao import conectar
import bcrypt

def cadastrar(nome, email, cargo, senha, cpf):
    conexao = None
    cursor = None
    try:
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

        conexao, cursor = conectar()
        
        sql = """
            INSERT INTO tb_usuarios (nome_usuario, email, cargo, senha, cpf) 
            VALUES (%s, %s, %s, %s, %s);
        """
        
        cursor.execute(sql, (nome, email, cargo, senha_hash, cpf))
        conexao.commit()
        return True

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