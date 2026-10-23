from database.conexao import conectar


def adicionar_aluno(rm: int, nome_aluno: str, id_turma: int) -> dict:
    """
    Adiciona o aluno com as informações passadas através dos parâmetros.
    """

    conexao = None
    cursor = None

    try:
        # Verifica se algum campo está vazio
        if not rm or not nome_aluno or not id_turma:
            return {
                "sucesso": False,
                "erro_aluno_vazio": True
            }

        conexao, cursor = conectar()

        # Verifica se o RM já existe
        sql_verificar = """
            SELECT rm_aluno
            FROM tb_alunos
            WHERE rm_aluno = %s;
        """

        cursor.execute(sql_verificar, (rm,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "sucesso": False,
                "erro_aluno_existente": True
            }

        sql = """
            INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma)
            VALUES (%s, %s, %s);
        """

        cursor.execute(
            sql,
            (rm, nome_aluno, id_turma)
        )

        conexao.commit()

        return {
            "sucesso": True
        }

    except Exception as erro:
        print(f"Erro ao cadastrar aluno: {erro}")

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



def recuperar_alunos():
    conexao, cursor = conectar()

    cursor.execute("""
        SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma 
        FROM db_snec.tb_alunos
        INNER JOIN tb_turmas 
        ON tb_alunos.id_turma = tb_turmas.id_turma
        ORDER BY tb_alunos.nome_aluno;
    """)

    alunos = cursor.fetchall()

    conexao.close()

    return alunos




def deletar_aluno(rm:str) -> bool:


    conexao,cursor = conectar()
     
    cursor.execute("""delete from tb_alunos where rm_aluno = (%s);""",(rm,) )

    conexao.commit()
    conexao.close()

