CREATE DATABASE IF NOT EXISTS db_snec;
USE db_snec;

CREATE TABLE IF NOT EXISTS tb_atividades (
 id_atividade INT PRIMARY KEY AUTO_INCREMENT,
 atividade VARCHAR(50) NOT NULL,
 periodo VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS tb_turmas (
 id_turma INT PRIMARY KEY AUTO_INCREMENT,
 turma VARCHAR(10) NOT NULL UNIQUE,
 periodo VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS tb_usuarios (
  id_usuario INT PRIMARY KEY AUTO_INCREMENT,
  nome_usuario VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  cargo VARCHAR(50) NOT NULL,
  senha VARCHAR(255) NOT NULL,
  cpf VARCHAR(11) UNIQUE NOT NULL,
  status VARCHAR(20) DEFAULT 'pendente'
);

CREATE TABLE IF NOT EXISTS tb_alunos (
 rm_aluno INT PRIMARY KEY,
 nome_aluno VARCHAR(100) NOT NULL,
 id_turma INT,
 CONSTRAINT FK_ALUNO_TURMA
 FOREIGN KEY (id_turma) REFERENCES tb_turmas(id_turma)
);

CREATE TABLE IF NOT EXISTS tb_his_almoco (
 rm_aluno INT,
 data DATE DEFAULT (CURRENT_DATE),
 id_usuario INT,
 atendido BOOLEAN DEFAULT FALSE,
 CONSTRAINT FK_ALMOCO_ALUNO
 FOREIGN KEY (rm_aluno) REFERENCES tb_alunos(rm_aluno),
 CONSTRAINT FK_ALMOCO_USUARIO
 FOREIGN KEY (id_usuario) REFERENCES tb_usuarios(id_usuario),
 PRIMARY KEY(rm_aluno, data)
);

CREATE TABLE IF NOT EXISTS tb_his_lanche (
 id_turma INT,
 data DATE DEFAULT (CURRENT_DATE),
 id_usuario INT,
 quantidade_alunos INT NOT NULL,
 CONSTRAINT FK_LANCHE_TURMA
 FOREIGN KEY (id_turma) REFERENCES tb_turmas(id_turma),
 CONSTRAINT FK_LANCHE_USUARIO
 FOREIGN KEY (id_usuario) REFERENCES tb_usuarios(id_usuario),
 PRIMARY KEY (id_turma, data)
);

CREATE TABLE IF NOT EXISTS tb_aluno_atividade (
 rm_aluno INT,
 id_atividade INT,
 dia_semana ENUM('SEG', 'TER', 'QUA', 'QUI', 'SEX') NOT NULL,	-- DAYOFWEEK(data)
 CONSTRAINT FK_ALUNO_ATIVIDADE
 FOREIGN KEY (rm_aluno) REFERENCES tb_alunos(rm_aluno),
 CONSTRAINT FK_ATIVIDADE_ALUNO
 FOREIGN KEY (id_atividade) REFERENCES tb_atividades(id_atividade),
 PRIMARY KEY(rm_aluno, id_atividade, dia_semana)
);