from database.conexao import conectar

def cadastrar (nome_usuario, email, cargo, senha, cpf):
    try:
        conexao, cursor = conectar()
        cursor.execute("INSERT INTO tb_usuarios (nome_usuario, email, cargo, senha, cpf) VALUES (%s, %s, %s, %s, %s);", (nome_usuario, email, cargo, senha, cpf))
        conexao.commit()
        conexao.close()

    except Exception as erro:
        print(erro)
        return False