import datetime
from database.conexao import conectar

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
            a.rm_aluno AS rm,
            a.nome_aluno AS aluno,
            t.turma AS ano,
            act.atividade,
            COALESCE(ha.atendido, FALSE) AS status
        FROM tb_alunos a
        JOIN tb_turmas t ON a.id_turma = t.id_turma
        JOIN tb_aluno_atividade aa ON a.rm_aluno = aa.rm_aluno
        JOIN tb_atividades act ON aa.id_atividade = act.id_atividade
        LEFT JOIN tb_his_almoco ha ON ha.rm_aluno = a.rm_aluno AND ha.data = CURRENT_DATE()
        WHERE aa.dia_semana = %s
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