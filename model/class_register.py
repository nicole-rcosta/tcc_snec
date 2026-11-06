from database.conexao import conectar
import mysql.connector

def adicionar_sala(turma:str,periodo:str,qnt_alunos:int) -> bool:
    """
    Adicona a sala com as informações passadas através dos parâmetros.
    """

    conexao,cursor = conectar()


    sql = """
        SELECT turma FROM tb_turmas
        WHERE turma = %s;
    """
    cursor.execute(sql, (turma, ))
    turma_result = cursor.fetchone()

    if turma_result:
        return {"sucesso": True, "erro": "Esta turma já está cadastrada."}
    else:
        cursor.execute("""INSERT INTO tb_turmas (turma, periodo, quantidade_alunos)
                            VALUES (%s,%s,%s);""",(turma, periodo, qnt_alunos) )
        conexao.commit()
        return {"sucesso": True, "mensagem": "Turma cadastrada com sucesso."}
        
    cursor.close()
    conexao.close()

def recuperar_salas():
    """
        Recupera salas já cadastradas 
    """
    conexao,cursor = conectar()
    cursor.execute("""SELECT id_turma, turma, periodo, quantidade_alunos FROM db_snec.tb_turmas ORDER BY turma;""")


    salas = cursor.fetchall()


    conexao.close()

    return salas

def deletar_sala(cod:int) -> bool:
    """
        Deleta salas já cadastradas
    """
    conexao,cursor = conectar()

    try:
        cursor.execute("""delete from tb_turmas where id_turma = (%s);""",(cod,) )
        conexao.commit()
        return {"sucesso": True, "mensagem": "Sala deletada!"}

    except Exception as erro:
        print(f"Erro ao cadastrar usuário: {erro}")
        
        if conexao:
            conexao.rollback()
        if "1451" in str(erro) or "foreign key constraint" in str(erro).lower():
            return {
                "sucesso": False, 
                "mensagem": "Não é possível excluir: existem alunos cadastrados nesta sala."
            }
            
        print(f"Erro ao deletar sala (ID: {cod}): {erro}")
        return {"sucesso": False, "mensagem": "Erro interno no servidor."}
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
