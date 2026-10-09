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

def logar(nome:str, cpf:str, senha:str) -> bool:
    senha_bytes = senha.encode('utf-8')
    senha_banco_bytes = nome['senha'].encode('utf-8')

    # Lógica comparação de senhas cripto
    if bcrypt.checkpw(senha_bytes, senha_banco_bytes):
        print("Login aprovado!")
    else:
        print("Senha incorreta!")
    
    # Busca pelo cpf no banco de dados
    try:
        conexao, cursor = conectar()
        cursor.execute("SELECT nome_usuario, cpf, senha, status from tb_usuarios WHERE cpf = %s;", (cpf, ))
        resultado = cursor.fetchone()
        conexao.close()
        return resultado
    
    # cpf cadastrado? -> status aprovado? -> senhas iguais? -> libera
    
    except Exception as erro:
        print(erro)
        return False