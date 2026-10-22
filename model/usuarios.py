from database.conexao import conectar
from static.utils.cpf_validation import validar_cpf
import bcrypt

def cadastrar(nome: str, email: str, cargo: str, senha: str, cpf: str, status: str) -> dict:
    conexao = None
    cursor = None

    try:
        # Verifica se algum campo está vazio
        if not nome or not email or not cargo or not senha or not cpf:
            return {
                "sucesso": False,
                "erro_cadastro_vazio": True
            }

        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

        if not validar_cpf(cpf):
            print("cpf invalido")
            return {
                "sucesso": False,
                "erro_cpf": True
            }

        conexao, cursor = conectar()

        # Verifica se o email ou CPF já existem
        sql_verificar = """
            SELECT id_usuario
            FROM tb_usuarios
            WHERE email = %s OR cpf = %s;
        """

        cursor.execute(sql_verificar, (email, cpf))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "sucesso": False,
                "erro_cadastro_existente": True
            }

        sql = """
            INSERT INTO tb_usuarios (nome_usuario, email, cargo, senha, cpf, status) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(
            sql,
            (nome, email, cargo, senha_hash, cpf, status)
        )

        conexao.commit()

        return {
            "sucesso": True
        }

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")

        if conexao:
            conexao.rollback()

        return {
            "sucesso": False,
            "erro_servidor": True
        }

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
            return {
                "sucesso": False,
                "erro_login": True
            }

        id_usuario = resultado['id_usuario']
        nome_usuario = resultado['nome_usuario']
        cargo = resultado['cargo']
        senha_hash_banco = resultado['senha']
        status_result = resultado['status']

        senha_bytes = senha.encode('utf-8')
        hash_banco_bytes = senha_hash_banco.encode('utf-8')

        if not bcrypt.checkpw(senha_bytes, hash_banco_bytes):
            return {
                "sucesso": False,
                "erro_login": True
            }

        if status_result != "aprovado":
            return {
                "sucesso": False,
                "erro_aprovacao": True
            }

        return {
            "sucesso": True,
            "usuario": {
                "id": id_usuario,
                "nome": nome_usuario,
                "cargo": cargo
            }
        }

    except Exception as erro:
        print(f"Erro ao processar login: {erro}")

        return {
            "sucesso": False,
            "erro_servidor": True
        }

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