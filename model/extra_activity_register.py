from database.conexao import conectar

def recuperar_atividade():
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
    try:
        conexao, cursor = conectar()
        cursor.execute("INSERT INTO tb_atividades (atividade, periodo) VALUES (%s, %s);", atividade, periodo)
        conexao.commit()
        conexao.close()
        return True

    except Exception as erro:
        print(erro)
        return False


def excluir_atividade(id_atividade):
    try:
        conexao, cursor = conectar()
        cursor.execute("DELETE FROM tb_atividades WHERE id_atividade = %s;", id_atividade)
        conexao.commit()
        conexao.close()
        return True
    
    except Exception as erro:
        print(erro)
        return False
