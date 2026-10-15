from database.conexao import conectar


def recuperar_dados_dashboard():
    # Desestrutura a conexão e o cursor retornados por conectar()
    conn, cursor = conectar()

    # Busca todas as turmas e verifica se há lançamento de lanche no dia atual
    query_turmas = """
        SELECT 
            t.id_turma,
            t.turma AS nome,
            COALESCE(l.quantidade_alunos, 0) AS total_lanche,
            CASE 
                WHEN l.id_turma IS NOT NULL THEN 'concluded'
                ELSE 'waiting'
            END AS status
        FROM tb_turmas t
        LEFT JOIN tb_his_lanche l 
            ON t.id_turma = l.id_turma 
            AND l.data = CURRENT_DATE()
        ORDER BY t.turma ASC;
    """
    cursor.execute(query_turmas)
    turmas = cursor.fetchall()

    # Total de lanches somando as turmas que já enviaram contagem hoje
    query_total_lanches = """
        SELECT COALESCE(SUM(quantidade_alunos), 0) AS total
        FROM tb_his_lanche
        WHERE data = CURRENT_DATE();
    """
    cursor.execute(query_total_lanches)
    resultado_lanche = cursor.fetchone()
    total_lanches = resultado_lanche['total'] if resultado_lanche else 0

    # Total de almoços (contagem dos alunos atendidos no dia)
    query_total_almocos = """
        SELECT COUNT(*) AS total
        FROM tb_his_almoco
        WHERE data = CURRENT_DATE() AND atendido = TRUE;
    """
    cursor.execute(query_total_almocos)
    resultado_almoco = cursor.fetchone()
    total_almocos = resultado_almoco['total'] if resultado_almoco else 0

    # Sempre feche o cursor e a conexão ao finalizar
    cursor.close()
    conn.close()

    # Define se todas as turmas cadastradas já tiveram a chamada concluída hoje
    todas_concluidas = all(t['status'] == 'concluded' for t in turmas) if turmas else False

    return {
        "turmas": turmas,
        "total_lanches": total_lanches,
        "total_almocos": total_almocos,
        "todas_concluidas": todas_concluidas
    }