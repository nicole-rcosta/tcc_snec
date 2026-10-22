INSERT INTO tb_usuarios(nome_usuario, email, cargo, senha, cpf, status)
VALUE ('ADM SNEC', 'sneccode@gmail.com', 'adm', '$2b$12$WpdfRGaObonrj/OnjmTHM.BcB73YWHLsf2KXQuN0h.hxgK6EJjd8W', '00000000000', 'aprovado'),
	  ('Nicole', 'nicole@gmail.com', 'nutri', '$2b$12$0MauxWmCreNWVzsruq7PBuWwkkSFQGfMwnZN05HqldiATSFXR8wcK', '46044913805', 'aprovado');

SELECT * FROM tb_usuarios;


INSERT INTO tb_usuarios (id_usuario, nome_usuario, email, cargo, senha, cpf) 
VALUES (1, 'Professor Teste', 'prof@teste.com', 'Professor', '123456', '12345678900')
ON DUPLICATE KEY UPDATE nome_usuario='Professor Teste';


INSERT INTO tb_turmas (id_turma, turma, periodo, quantidade_alunos) VALUES 
(1, '9º ano A', 'Manhã', 30),
(2, '9º ano B', 'Manhã', 28),
(3, '1º ano A', 'Manhã', 32),
(4, '1º ano B', 'Tarde', 29),
(5, '2º ano A', 'Tarde', 31),
(6, '3º ano A', 'Manhã', 27)
ON DUPLICATE KEY UPDATE quantidade_alunos=VALUES(quantidade_alunos);


INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma) VALUES 
-- 9º ano A (id_turma = 1)
(1001, 'Aluno Teste 1', 1),
(1002, 'Maria Silva', 1),
(1003, 'João Souza', 1),


-- 9º ano B (id_turma = 2)
(1004, 'Ana Costa', 2),
(1005, 'Carlos Eduardo', 2),
(1006, 'Beatriz Lima', 2),


-- 1º ano A (id_turma = 3)
(1007, 'Gabriel Alves', 3),
(1008, 'Fernanda Rocha', 3),
(1009, 'Lucas Mendes', 3),


-- 1º ano B (id_turma = 4)
(1010, 'Mariana Oliveira', 4),
(1011, 'Rafael Santos', 4),


-- 2º ano A (id_turma = 5)
(1012, 'Camila Ribeiro', 5),
(1013, 'Pedro Henrique', 5),


-- 3º ano A (id_turma = 6)
(1014, 'Juliana Martins', 6),
(1015, 'Thiago Barbosa', 6)
ON DUPLICATE KEY UPDATE nome_aluno=VALUES(nome_aluno);


-- 4. Lança o LANCHE de HOJE para 3 das 6 turmas (as outras 3 ficam pendentes no dashboard)
INSERT INTO tb_his_lanche (id_turma, data, id_usuario, quantidade_alunos) VALUES 
(1, CURRENT_DATE(), 1, 28),
(3, CURRENT_DATE(), 1, 30),
(5, CURRENT_DATE(), 1, 29)
ON DUPLICATE KEY UPDATE quantidade_alunos=VALUES(quantidade_alunos);


-- 5. Lança o ALMOÇO de HOJE para 8 alunos que já foram atendidos
INSERT INTO tb_his_almoco (rm_aluno, data, id_usuario, atendido) VALUES 
(1001, CURRENT_DATE(), 1, TRUE),
(1002, CURRENT_DATE(), 1, TRUE),
(1004, CURRENT_DATE(), 1, TRUE),
(1007, CURRENT_DATE(), 1, TRUE),
(1008, CURRENT_DATE(), 1, TRUE),
(1009, CURRENT_DATE(), 1, TRUE),
(1012, CURRENT_DATE(), 1, TRUE),
(1014, CURRENT_DATE(), 1, TRUE)
ON DUPLICATE KEY UPDATE atendido = TRUE;

-- Insere as ativ. extracurriculares 
INSERT INTO tb_atividades (id_atividade, atividade, periodo) VALUES
(1, 'Reforço de Matemática', 'Tarde'),
(2, 'Treino de Futsal', 'Tarde'),
(3, 'Oficina de Robótica', 'Tarde')
ON DUPLICATE KEY UPDATE atividade=VALUES(atividade);

INSERT INTO tb_aluno_atividade (rm_aluno, id_atividade, dia_semana) VALUES
(1001, 1, 'QUI'), 
(1002, 2, 'QUI'), 
(1004, 1, 'QUI'), 
(1007, 2, 'QUI'), 
(1008, 3, 'QUI'), 
(1009, 1, 'QUI'), 
(1012, 2, 'QUI'), 
(1014, 3, 'QUI')  
ON DUPLICATE KEY UPDATE id_atividade = VALUES(id_atividade);