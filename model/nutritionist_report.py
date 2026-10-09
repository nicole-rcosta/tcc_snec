from database.conexao import conectar
import datetime

def buscar_alunos_almoco_hoje():
    """
    Busca TODOS os alunos que possuem atividade no contraturno no dia da semana atual,
    trazendo o status de presença (atendido = True/False) em tb_his_almoco.
    """
    conexao, cursor = conectar()

    # Mapeamento do dia da semana (0 = Segunda, 4 = Sexta)
    dias_map = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}
    hoje_num = datetime.date.today().weekday()

    # Se for fim de semana (Sábado = 5, Domingo = 6), retorna lista vazia
    if hoje_num > 4:
        cursor.close()
        conexao.close()
        return {"total_dia": 0, "data_hoje": datetime.date.today().strftime('%d/%m/%Y'), "alunos": []}

    dia_semana = dias_map[hoje_num]

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

    return {
        "total_dia": len(alunos),
        "data_hoje": datetime.date.today().strftime('%d/%m/%Y'),
        "alunos": alunos
    }


def registrar_almoco_aluno(rm_aluno, atendido, id_usuario=None):
    """
    Registra o almoço do aluno apenas se ele ainda não tiver sido marcado hoje.
    Utiliza INSERT IGNORE para impedir qualquer tentativa de reescrever/desmarcar.
    """
    # Bloqueio prévio no Python caso a requisição venha como False (tentativa de desmarcar)
    if not atendido:
        return {
            "sucesso": False, 
            "mensagem": "O almoço deste aluno já foi marcado e não pode ser desmarcado!"
        }

    conexao, cursor = conectar()

    try:
        # INSERT IGNORE insere o registro na 1ª vez. 
        # Se já existir um registro hoje (rm_aluno + CURRENT_DATE), o MySQL ignora silenciosamente.
        query = """
            INSERT IGNORE INTO tb_his_almoco (rm_aluno, data, id_usuario, atendido)
            VALUES (%s, CURRENT_DATE(), %s, TRUE);
        """
        
        cursor.execute(query, (rm_aluno, id_usuario))
        conexao.commit()

        # cursor.rowcount > 0 indica que uma nova linha foi realmente inserida
        if cursor.rowcount > 0:
            return {"sucesso": True, "mensagem": "Almoço registrado com sucesso!"}
        else:
            return {
                "sucesso": False, 
                "mensagem": "O almoço deste aluno já havia sido registrado hoje!"
            }

    except Exception as err:
        conexao.rollback()
        print(f"Erro ao registrar almoço: {err}")
        return {"sucesso": False, "mensagem": f"Erro no banco de dados: {err}"}

    finally:
        cursor.close()
        conexao.close()