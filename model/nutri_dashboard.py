from database.conexao import conectar
import datetime

def recuperar_dados_dashboard():
    """
            Recupera dados e exibe no dashboard da Nurticionista.
    """
    # Desestrutura a conexão e o cursor retornados por conectar()
    conexao, cursor = conectar()

    try:
    # Busca todas as turmas e verifica se há lançamento de lanche no dia atual
        query_turmas = """
            SELECT 
                tb_turmas.id_turma,
                tb_turmas.turma AS nome,
                COALESCE(tb_his_lanche.quantidade_alunos, 0) AS total_lanche,
                CASE 
                    WHEN tb_his_lanche.id_turma IS NOT NULL OR tb_his_almoco.rm_aluno IS NOT NULL THEN 'concluded'
                    ELSE 'waiting'
                END AS status
            FROM tb_turmas 
            LEFT JOIN tb_his_lanche 
                ON tb_turmas.id_turma = tb_his_lanche.id_turma 
                AND tb_his_lanche.data = CURRENT_DATE()
            LEFT JOIN tb_alunos 
                    ON tb_turmas.id_turma = tb_alunos.id_turma
            LEFT JOIN tb_his_almoco
                        ON tb_alunos.rm_aluno = tb_his_almoco.rm_aluno
                        AND tb_his_almoco.data = CURRENT_DATE()
            GROUP BY 
                tb_turmas.id_turma, 
                    tb_turmas.turma, 
                    tb_his_lanche.quantidade_alunos, 
                    tb_his_lanche.id_turma
            ORDER BY tb_turmas.turma ASC;
        """
        cursor.execute(query_turmas)
        turmas = cursor.fetchall()

        if not turmas:
            return {"sucesso": False, "mensagem": "Nenhuma turma cadastrada"}

        # Total de lanches somando as turmas que já enviaram contagem hoje
        query_total_lanches = """
            SELECT COALESCE(SUM(tb_his_lanche.quantidade_alunos), 0) AS total
            FROM tb_his_lanche
            WHERE tb_his_lanche.data = CURRENT_DATE();
        """
        cursor.execute(query_total_lanches)
        resultado_lanche = cursor.fetchone()
        total_lanches = resultado_lanche['total'] if resultado_lanche else 0

        # Total de almoços (contagem dos alunos atendidos no dia)
        query_total_almocos = """
            SELECT COUNT(DISTINCT tb_his_almoco.rm_aluno) AS total
            FROM tb_his_almoco
            WHERE tb_his_almoco.data = CURRENT_DATE();
        """
        cursor.execute(query_total_almocos)
        resultado_almoco = cursor.fetchone()
        total_almocos = resultado_almoco['total'] if resultado_almoco else 0


        # Define se todas as turmas cadastradas já tiveram a chamada concluída hoje
        todas_concluidas = all(t['status'] == 'concluded' for t in turmas) if turmas else False

        return {
            "sucesso": True,
            "turmas": turmas,
            "total_lanches": total_lanches,
            "total_almocos": total_almocos,
            "todas_concluidas": todas_concluidas
        }

    finally:
        cursor.close()
        conexao.close()




def buscar_alunos_almoco_hoje():
    """
    Busca SOMENTE os alunos previstos para o almoço no dia da semana atual 
    (com base nas atividades do contraturno cadastradas em tb_aluno_atividade).
    """
    conexao, cursor = conectar()

    dias_map = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}
    hoje_num = datetime.date.today().weekday()

    # Se for fim de semana (Sábado = 5, Domingo = 6), retorna lista vazia
    if hoje_num > 4:
        cursor.close()
        conexao.close()
        return {
            "total_dia": 0, 
            "data_hoje": datetime.date.today().strftime('%d/%m/%Y'), 
            "alunos": []
        }

    dia_semana = dias_map[hoje_num]

    # Filtra pelo dia da semana atual
    query = """
            SELECT 
            ha.rm_aluno AS rm,
            a.nome_aluno AS aluno,
            t.turma AS ano,
            act.atividade AS atividade,
            ha.atendido AS status
            FROM tb_his_almoco ha
            INNER JOIN tb_alunos a 
                ON ha.rm_aluno = a.rm_aluno
            INNER JOIN tb_turmas t 
                ON a.id_turma = t.id_turma
            INNER JOIN tb_aluno_atividade aa 
                ON ha.rm_aluno = aa.rm_aluno
            INNER JOIN tb_atividades act 
                ON aa.id_atividade = act.id_atividade
            WHERE ha.data = CURRENT_DATE()
            AND aa.dia_semana = %s
            ORDER BY a.nome_aluno ASC;
    """

    cursor.execute(query, (dia_semana,))
    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Converte a coluna 'status' (0 ou 1 do MySQL) para booleano nativo (True/False)
    for aluno in alunos:
        aluno['status'] = bool(aluno['status'])

    return {
        "total_dia": len(alunos),
        "data_hoje": datetime.date.today().strftime('%d/%m/%Y'),
        "alunos": alunos
    }


def atualizar_status_almoco_aluno(rm_aluno, atendido, id_usuario=None):
    """
    Registra ou altera o atendimento do almoço (True/False) na tabela tb_his_almoco.
    """
    conexao, cursor = conectar()

    try:
        query = """
            INSERT INTO tb_his_almoco (rm_aluno, data, id_usuario, atendido)
            VALUES (%s, CURRENT_DATE(), %s, %s)
            ON DUPLICATE KEY UPDATE
                atendido = VALUES(atendido),
                id_usuario = VALUES(id_usuario);
        """
        cursor.execute(query, (rm_aluno, id_usuario, atendido))
        conexao.commit()
        return {"sucesso": True, "mensagem": "Status do almoço atualizado com sucesso!"}

    except Exception as err:
        conexao.rollback()
        print(f"Erro ao atualizar status do almoço: {err}")
        return {"sucesso": False, "mensagem": f"Erro no banco de dados: {err}"}

    finally:
        cursor.close()
        conexao.close()