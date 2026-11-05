from database.conexao import conectar

def adicionar_aluno(rm:int,nome_aluno:str,id_turma:int) -> bool:
    """
    Adicona o aluno com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()
     
    cursor.execute("""INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma)
                        VALUES (%s,%s, %s);""",(rm,nome_aluno,id_turma) )

    conexao.commit()
    conexao.close()

def recuperar_alunos():
    conexao,cursor = conectar()
    cursor.execute("""SELECT tb_alunos.rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma FROM db_snec.tb_alunos
                        INNER JOIN tb_turmas 
                        ON tb_alunos.id_turma = tb_turmas.id_turma
                        ORDER BY
                        tb_alunos.nome_aluno;""")


    alunos=cursor.fetchall()


    conexao.close()



    return alunos



def deletar_aluno(rm:str) -> bool:
    """
        Deleta o aluno com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()

    try:
        cursor.execute("""delete from tb_alunos where rm_aluno = (%s);""",(rm,) )
        conexao.commit()
        return {"sucesso": True, "mensagem": "Aluno deletado!"}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        
        if conexao:
            conexao.rollback()
        if "1451" in str(erro) or "foreign key constraint" in str(erro).lower():
            return {
                "sucesso": False, 
                "mensagem": "Não é possível excluir: este aluno está cadastrado em uma atividade."
            }
            
        print(f"Erro ao deletar sala (ID: {rm}): {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
