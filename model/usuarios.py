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

def logar(cpf: str, senha: str) -> dict:
    conexao = None
    cursor = None

    try:
        conexao, cursor = conectar()

        sql = """
            SELECT id_usuario, nome_usuario, cargo, senha, status 
            FROM tb_usuarios 
            WHERE cpf = %s
            ;
        """

        cursor.execute(sql, (cpf,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Usuário não encontrado.")
            return {"sucesso": False, "mensagem": "CPF ou senha incorretos."}

        id_usuario = resultado['id_usuario']
        nome_usuario = resultado['nome_usuario']
        cargo = resultado['cargo']
        senha_hash_banco = resultado['senha']
        status_result = resultado['status']

        if status_result != "aprovado":
            print("Cadastro ainda pendente de aprovação pelo Administrador.")
            return {
                "sucesso": False, 
                "mensagem": "Seu cadastro está pendente de aprovação pelo Administrador."
            }

        senha_bytes = senha.encode('utf-8')
        hash_banco_bytes = senha_hash_banco.encode('utf-8')

        if bcrypt.checkpw(senha_bytes, hash_banco_bytes):
            print(f"Login aprovado para {nome_usuario} ({cargo})!")
            return {
                "sucesso": True,
                "mensagem": "Login realizado com sucesso!",
                "usuario": {
                    "id": id_usuario,
                    "nome": nome_usuario,
                    "cargo": cargo
                }
            }
        else:
            print("Senha incorreta!")
            return {"sucesso": False, "mensagem": "CPF ou senha incorretos."}

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()