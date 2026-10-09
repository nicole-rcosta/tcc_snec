from database.conexao import conectar
import datetime

def buscar_alunos_contraturno(id_turma):
    conexao, cursor = conectar
    
    # Descobre o dia da semana atual no formato do ENUM ('SEG', 'TER', 'QUA', 'QUI', 'SEX')
    dias_map = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX'}
    hoje_num = datetime.date.today().weekday()
    
    if hoje_num > 4: # Fim de semana
        return []
        
    dia_semana = dias_map[hoje_num]

    query = """
        SELECT 
            a.rm_aluno AS rm,
            a.nome_aluno AS aluno,
            t.turma AS ano,
            act.atividade,
            act.periodo AS turno,
            COALESCE(ha.atendido, FALSE) AS status
        FROM tb_alunos a
        JOIN tb_turmas t ON a.id_turma = t.id_turma
        JOIN tb_aluno_atividade aa ON a.rm_aluno = aa.rm_aluno
        JOIN tb_atividades act ON aa.id_atividade = act.id_atividade
        LEFT JOIN tb_his_almoco ha ON ha.rm_aluno = a.rm_aluno AND ha.data = CURRENT_DATE()
        WHERE a.id_turma = %s AND aa.dia_semana = %s
    """
    
    cursor.execute(query, (id_turma, dia_semana))
    alunos = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return alunos


def registrar_presenca_contraturno(id_turma, id_usuario, quantidade_alunos, alunos_contraturno):
    """
    alunos_contraturno deve ser uma lista de dicionários vinda do front-end:
    [
        {"rm_aluno": 7087, "atendido": False},
        {"rm_aluno": 7068, "atendido": True}
    ]
    """
    conexao, cursor = conectar()

    try:
        # 1. Registrar a quantidade total de alunos da turma no dia (tb_his_lanche)
        query_lanche = """
            INSERT INTO tb_his_lanche (id_turma, data, id_usuario, quantidade_alunos)
            VALUES (%s, CURRENT_DATE(), %s, %s)
            ON DUPLICATE KEY UPDATE 
                quantidade_alunos = VALUES(quantidade_alunos),
                id_usuario = VALUES(id_usuario);
        """
        cursor.execute(query_lanche, (id_turma, id_usuario, quantidade_alunos))

        # 2. Registrar a presença individual de cada aluno no contraturno/almoço (tb_his_almoco)
        query_almoco = """
            INSERT INTO tb_his_almoco (rm_aluno, data, id_usuario, atendido)
            VALUES (%s, CURRENT_DATE(), %s, %s)
            ON DUPLICATE KEY UPDATE 
                atendido = VALUES(atendido),
                id_usuario = VALUES(id_usuario);
        """

        for aluno in alunos_contraturno:
            cursor.execute(query_almoco, (
                aluno['rm_aluno'], 
                id_usuario, 
                aluno['atendido']
            ))

        # Confirma as alterações no banco de dados
        conexao.commit()
        return {"sucesso": True, "mensagem": "Registrado com sucesso!"}

    except Exception as err:
        conexao.rollback()
        print(f"Erro ao salvar: {err}")
        return {"sucesso": False, "mensagem": "Erro ao salvar no banco de dados."}

    finally:
        cursor.close()
        conexao.close()