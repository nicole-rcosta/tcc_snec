from database.conexao import conectar
from static.utils.cpf_validation import validar_cpf
import bcrypt

def cadastrar(nome:str, email:str, cargo:str, senha:str, cpf:str, status:str) -> bool:
    conexao = None
    cursor = None
    
    try:
        conexao, cursor = conectar()

        sql = """
                SELECT * FROM tb_usuarios
                WHERE cpf = %s;
            """
        cursor.execute(sql, (cpf, ))
        user = cursor.fetchone()

        if user:
            print("Usuário já cadastrado")
            return {"sucesso": False, "mensagem": "Usuário já cadastrado."}
        else:
            senha_bytes = senha.encode('utf-8')
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

            if not validar_cpf(cpf):
                print("cpf invalido")
                return {"sucesso": False, "mensagem": "CPF inválido."}
            
            sql = """
                INSERT INTO tb_usuarios (nome_usuario, email, cargo, senha, cpf, status) 
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            cursor.execute(sql, (nome, email, cargo, senha_hash, cpf, status))
            conexao.commit()
            return True

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        if conexao:
            conexao.rollback()
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}

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
            WHERE cpf = %s;
        """

        cursor.execute(sql, (cpf,))
        usuario = cursor.fetchone()

        if not usuario:
            print("Usuário não encontrado.")
            return {"sucesso": False, "mensagem": "Usuário não encontrado. Cadastre-se!"}

        id_usuario = usuario['id_usuario']
        nome_usuario = usuario['nome_usuario']
        cargo = usuario['cargo']
        senha_hash_banco = usuario['senha']
        status_result = usuario['status']

        if status_result != "aprovado":
            print("Cadastro ainda pendente de aprovação pelo Administrador.")
            return {
                "sucesso": False, 
                "mensagem": "Aguarde a aprovação do administrador para efetivar o seu cadastro."
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

# 
def verificar_email(email: str) -> bool:
    conexao = None
    cursor = None
    # procura o email digitado na tabela pra ver se eele existe
    try:
        conexao, cursor = conectar()

        sql = """
            SELECT email
            FROM tb_usuarios
            WHERE email = %s;
        """

        cursor.execute(sql, (email,))

        usuario = cursor.fetchone()
        # se ele exitir a função retorna true
        if usuario:
            return True

        return False
    # trata o erro
    except Exception as erro:
        print(f"Erro ao verificar e-mail: {erro}")
        return False
    # fecha o cursor
    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

def atualizar_senha(email: str, nova_senha: str) -> bool:
    conexao = None
    cursor = None

    try:
       senha_bytes = nova_senha.encode('utf-8')
       salt = bcrypt.gensalt()
       senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')
       
       conexao, cursor = conectar()

       # Atualiza a senha do usuário
       sql = """
           UPDATE tb_usuarios
           SET senha = %s
           WHERE email = %s;
       """

       cursor.execute(
           sql,
           (senha_hash, email)
       )

       conexao.commit()

       return True

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