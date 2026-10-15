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
    cursor.execute("""SELECT LPAD(tb_alunos.rm_aluno,4,"0") as rm_aluno, tb_alunos.nome_aluno, tb_turmas.turma FROM db_snec.tb_alunos
                        INNER JOIN tb_turmas 
                        ON tb_alunos.id_turma = tb_turmas.id_turma
                        ORDER BY
                        tb_alunos.nome_aluno;""")


    alunos=cursor.fetchall()


    conexao.close()



    return alunos



def deletar_aluno(rm:str) -> bool:


    conexao,cursor = conectar()
     
    cursor.execute("""delete from tb_alunos where rm_aluno = (%s);""",(rm,) )

    conexao.commit()
    conexao.close()

