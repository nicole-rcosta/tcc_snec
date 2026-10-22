from database.conexao import conectar



def adicionar_aluno_atividade(rm:int,atividade:str,dia_semana:int) -> bool:
    """
    Adicona o aluno com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()
     
    cursor.execute("""INSERT INTO `db_snec`.`tb_aluno_atividade` (`rm_aluno`, `id_atividade`, `dia_semana`) VALUES (%s, %s, %s);""",(rm,atividade,dia_semana) )

    conexao.commit()
    conexao.close()


def excluir_aluno_atividade(rm:int,atividade:str,dia_semana:int) -> bool:
    """
    Adicona o aluno com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()
     
    cursor.execute("""DELETE FROM `db_snec`.`tb_aluno_atividade` WHERE (`rm_aluno` = %s) and (`id_atividade` = %s) and (`dia_semana` = %s);;""",(rm,atividade,dia_semana) )

    conexao.commit()
    conexao.close()


def recuperar_alunos_atividade():
    conexao,cursor = conectar()
    cursor.execute("""SELECT
                            tb_alunos.nome_aluno AS nome,
                            tb_alunos.rm_aluno AS rm,
                            tb_turmas.turma AS turma,
                            tb_atividades.atividade AS atividade,
                            tb_atividades.id_atividade AS id_atividade,
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

