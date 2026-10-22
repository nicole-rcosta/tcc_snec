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



def cadastrar_atividade(ativid: str, periodo: str) -> dict:
    conexao = None
    cursor = None

    try:
        # Verifica se algum campo está vazio
        if not ativid or not periodo:
            return {
                "sucesso": False,
                "erro_atividade_vazia": True
            }

        conexao, cursor = conectar()

        # Verifica se a atividade já existe
        # Mantenha aqui a mesma consulta que você já usa
        # para consultar as atividades cadastradas.

        sql_verificar = """
            SELECT id_atividade
            FROM tb_atividades
            WHERE atividade = %s;
        """

        cursor.execute(sql_verificar, (ativid,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "sucesso": False,
                "erro_atividade_existente": True
            }

        sql = """
            INSERT INTO tb_atividades (atividade, periodo)
            VALUES (%s, %s);
        """

        cursor.execute(sql, (ativid, periodo))

        conexao.commit()

        return {
            "sucesso": True
        }

    except Exception as erro:
        print(f"Erro ao cadastrar atividade: {erro}")

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



def excluir_atividade(id_atividade):
    try:
        conexao, cursor = conectar()
        cursor.execute("DELETE FROM tb_atividades WHERE id_atividade = %s;", (id_atividade, ))
        conexao.commit()
        conexao.close()
        return True
    
    except Exception as erro:
        print(erro)
        return False
