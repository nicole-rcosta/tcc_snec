INSERT INTO tb_usuarios(nome_usuario, email, cargo, senha, cpf, status)
VALUES ('Manuely', 'm@gmail.com', 'prof', '$12$oosJifQ5pCi3iM4gz9FAg.Wykn9r4xp0aYH97Z4FM5Z7Jca0KXnui', '49221826830', 'pendente'),
	   ('Pablo', 'pablo@gmail.com', 'nutri', '$12$oosJifQ5pCi3iM4gz9FAg.Wykn9r4xp0aYH97Z4FM5Z7Jca0KXnui', '44488705880', 'pendente');



INSERT INTO tb_turmas (turma, periodo, quantidade_alunos) VALUES
('1ºA', 'Manhã', 32),
('1ºB', 'Manhã', 32),
('2ºA', 'Manhã', 32),
('2ºB', 'Manhã', 32),
('3ºA', 'Manhã', 32),
('3ºB', 'Manhã', 32);

INSERT INTO tb_alunos (rm_aluno, nome_aluno, id_turma) VALUES
('1001', 'João Pedro Silva', 1),
('1002', 'Maria Eduarda Santos', 1),
('1003', 'Lucas Gabriel Oliveira', 1),

('1004', 'Ana Clara Souza', 2),
('1005', 'Gabriel Henrique Costa', 2),
('1006', 'Beatriz Vitória Lima', 2),

('1007', 'Rafael Augusto Pereira', 3),
('1008', 'Larissa Fernanda Rocha', 3),
('1009', 'Matheus Vinicius Martins', 3),

('1010', 'Pedro Henrique Alves', 4),
('1011', 'Julia Beatriz Rodrigues', 4),
('1012', 'Gustavo Henrique Martins', 4),

('1013', 'Felipe Augusto Barbosa', 5),
('1014', 'Isabela Cristina Ferreira', 5),
('1015', 'Daniel Victor Almeida', 6);

INSERT INTO tb_atividades (atividade, periodo) VALUES
('Futebol', 'Tarde'),
('Vôlei', 'Tarde'),
('Basquete', 'Tarde'),
('Robótica', 'Manhã'),
('Teatro', 'Tarde'),
('Música', 'Manhã'),
('Xadrez', 'Tarde'),
('Dança', 'Tarde'),
('Artes', 'Manhã'),
('Informática', 'Tarde');

INSERT INTO tb_aluno_atividade (rm_aluno, id_atividade, dia_semana) VALUES
('1001', 1, 'SEG'),
('1001', 4, 'QUA'),

('1002', 2, 'TER'),
('1002', 7, 'QUI'),

('1003', 3, 'SEX'),
('1003', 5, 'TER'),

('1004', 1, 'QUA'),
('1004', 8, 'SEX'),

('1005', 4, 'SEG'),
('1005', 6, 'QUI'),

('1006', 2, 'TER'),
('1006', 9, 'SEX'),

('1007', 7, 'SEG'),
('1007', 10, 'QUA'),

('1008', 3, 'TER'),
('1008', 5, 'QUI'),

('1009', 1, 'SEX'),
('1009', 6, 'TER'),

('1010', 8, 'SEG'),
('1010', 10, 'QUI'),

('1011', 2, 'QUA'),
('1011', 7, 'SEX'),

('1012', 4, 'TER'),
('1012', 9, 'QUI'),

('1013', 5, 'SEG'),
('1013', 8, 'QUA'),

('1014', 3, 'SEX'),
('1014', 10, 'TER'),

('1015', 6, 'SEG'),
('1015', 9, 'SEX');
