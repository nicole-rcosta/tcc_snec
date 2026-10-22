from database.conexao import conectar

def verificar_adm(id_usuario):
    conexao,cursor = conectar()

    sql = """
        SELECT id_usuario, cargo, senha
        FROM db_snec.tb_usuarios
        WHERE id_usuario = %s";
    """
    cursor.execute
    adm = cursor.fetchone(sql, id_usuario)
    conexao.close()
    return adm