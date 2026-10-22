from database.conexao import conectar

def adicionar_sala(turma: str, periodo: str, qnt_alunos: int) -> dict:

    conexao = None
    cursor = None

    try:
        
        if not turma or not periodo or not qnt_alunos:
            return {
                "sucesso": False,
                "erro_sala_vazia": True
            }

        conexao, cursor = conectar()

        # ve se a turma já existe
        sql_verificar = """
            SELECT id_turma
            FROM tb_turmas
            WHERE turma = %s;
        """

        cursor.execute(sql_verificar, (turma,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "sucesso": False,
                "erro_turma_existente": True
            }

        sql = """
            INSERT INTO tb_turmas (turma, periodo, quantidade_alunos)
            VALUES (%s, %s, %s);
        """

        cursor.execute(
            sql,
            (turma, periodo, qnt_alunos)
        )

        conexao.commit()

        return {
            "sucesso": True
        }

    except Exception as erro:
        print(f"Erro ao cadastrar sala: {erro}")

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




def recuperar_salas():
    conexao,cursor = conectar()
    cursor.execute("""SELECT id_turma, turma, periodo, quantidade_alunos FROM db_snec.tb_turmas ORDER BY turma;""")


    musicas=cursor.fetchall()


    conexao.close()

    return musicas


def deletar_sala(cod:int) -> bool:


    conexao,cursor = conectar()
     
    cursor.execute("""delete from tb_turmas where id_turma = (%s);""",(cod,) )

    conexao.commit()
    conexao.close()
