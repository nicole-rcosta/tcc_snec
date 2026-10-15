from database.conexao import conectar

def adicionar_aluno(rm:int,nome_aluno:str,id_turma:int,id_atividade:int,dia_semana:str) -> bool:
    """
    Adicona o aluno com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()
     
    cursor.execute("""INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma)
                        VALUES (%s,%s, %s);

                        INSERT INTO tb_aluno_atividade (rm_aluno,id_atividade,dia_semana)
                        VALUES (%s, %s , %s );""",(rm,nome_aluno,id_turma,rm,id_atividade,dia_semana) )

    conexao.commit()
    conexao.close()



def recuperar_alunos():
    conexao,cursor = conectar()
    cursor.execute("""SELECT
                            tb_alunos.nome_aluno AS nome,
                            tb_alunos.rm_aluno AS rm,
                            tb_turmas.turma AS turma,
                            tb_atividades.atividade AS atividade,
                            tb_atividades.periodo AS periodo,
                            tb_aluno_atividade.dia_semana AS dia
                        FROM tb_alunos
                        INNER JOIN tb_aluno_atividade
                            ON tb_alunos.rm_aluno = tb_aluno_atividade.rm_aluno
                        INNER JOIN tb_turmas
                            ON tb_alunos.id_turma = tb_turmas.id_turma
                        INNER JOIN tb_atividades
                            ON tb_aluno_atividade.id_atividade = tb_atividades.id_atividade
                        ORDER BY
                            tb_alunos.nome_aluno;""")


    alunos=cursor.fetchall()


    conexao.close()

    return alunos


def deletar_aluno(cod:int) -> bool:


    conexao,cursor = conectar()
     
    cursor.execute("""delete from tb_turmas where id_turma = (%s);""",(cod,) )

    conexao.commit()
    conexao.close()
