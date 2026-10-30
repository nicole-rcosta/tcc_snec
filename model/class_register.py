from database.conexao import conectar

def adicionar_sala(turma:str,periodo:str,qnt_alunos:int) -> bool:
    """
    Adicona a sala com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()
     
    cursor.execute("""INSERT INTO tb_turmas (turma, periodo, quantidade_alunos)
                        VALUES (%s,%s,%s);""",(turma,periodo,qnt_alunos) )

    conexao.commit()
    conexao.close()



def recuperar_salas():
    conexao,cursor = conectar()
    cursor.execute("""SELECT id_turma, turma, periodo, quantidade_alunos FROM db_snec.tb_turmas ORDER BY turma;""")


    musicas=cursor.fetchall()


    conexao.close()

    return musicas


def deletar_sala(cod:int) -> bool:

    conexao,cursor = conectar()

    try:
        delete = cursor.execute("""delete from tb_turmas where id_turma = (%s);""",(cod,) )
        if delete:
            return {"sucesso": True, "mensagem": "Sala apagada."}
        else:
            return {"sucesso": False, "mensagem": "Existem alunos cadastrados nessa sala."}

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
