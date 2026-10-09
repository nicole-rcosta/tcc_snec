from database.conexao import conectar
import bcrypt

def cadastrar(nome:str, email:str, cargo:str, senha:str, cpf:str) -> bool:
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

# 

# model/usuarios.py
import bcrypt
from database.conexao import conectar

def atualizar_senha(email: str, nova_senha: str) -> bool:
    conexao = None
    cursor = None
    try:
        
        senha_bytes = nova_senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

        conexao, cursor = conectar()

        sql = """
            UPDATE tb_usuarios 
            SET senha = %s 
            WHERE email = %s;
        """
        cursor.execute(sql, (senha_hash, email))
        conexao.commit()
        return True

    except Exception as erro:
        print(f"Erro ao redefinir senha do usuário: {erro}")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()