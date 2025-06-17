-- ================================
-- APRIMORAMENTO DO BANCO DE DADOS
-- FASE 4 - FARMTECH SOLUTIONS
-- ================================

-- 1. Adiciona campo para rastrear origem da decisão (ML, CLIMA, MANUAL)
ALTER TABLE DECISAO_IRRIGACAO
  ADD COLUMN tipo_decisao VARCHAR(20) AFTER pode_irrigar;

-- 2. Relaciona cada decisão com a leitura que originou
ALTER TABLE DECISAO_IRRIGACAO
  ADD COLUMN cd_leitura BIGINT AFTER tipo_decisao;

-- 3. Cria índice para otimizar consultas por data/hora
CREATE INDEX idx_leitura_data ON LEITURA_SENSOR (data_hora);
CREATE INDEX idx_decisao_data ON DECISAO_IRRIGACAO (data_hora);

-- 4. Cria chave estrangeira entre decisão e leitura
ALTER TABLE DECISAO_IRRIGACAO
  ADD CONSTRAINT fk_decisao_leitura
  FOREIGN KEY (cd_leitura) REFERENCES LEITURA_SENSOR(cd_leitura);

-- 5. Cria tabela auxiliar para registrar previsões feitas pelo modelo ML
CREATE TABLE PREVISAO_IRRIGACAO (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  valor_umidade DOUBLE,
  valor_ph DOUBLE,
  valor_fosforo INT,
  valor_potassio INT,
  probabilidade_irrigar DOUBLE,
  decisao_final BOOLEAN
);
