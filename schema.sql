-- =====================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS
-- Sistema de Avaliação de Fornecedores - TCC
-- PostgreSQL
-- =====================================================

-- Criar tabela de Fornecedores
CREATE TABLE fornecedores (
    id SERIAL PRIMARY KEY,
    codigo_material VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    pais VARCHAR(100),
    comprador VARCHAR(100),
    gestor_qualidade VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de Qualidade (valor independente 0-150)
CREATE TABLE criterios_qualidade (
    id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
    score_qualidade INTEGER DEFAULT 0,                -- valor independente 0-150
    data_avaliacao DATE DEFAULT CURRENT_DATE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de Critérios de Comercial (C1-C5, soma = 0-90)
CREATE TABLE criterios_comercial (
    id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
    c1_status_contratual INTEGER DEFAULT 0,           -- critério comercial 1
    c2_negotiation_target INTEGER DEFAULT 0,          -- critério comercial 2
    c3_competitiveness INTEGER DEFAULT 0,             -- critério comercial 3
    c4_payment_terms INTEGER DEFAULT 0,               -- critério comercial 4
    c5_communication INTEGER DEFAULT 0,               -- critério comercial 5
    data_avaliacao DATE DEFAULT CURRENT_DATE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de Critérios de Entrega (D1-D5, soma = 0-60)
CREATE TABLE criterios_entrega (
    id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
    d1_adherence_schedule INTEGER DEFAULT 0,          -- critério entrega 1
    d2_conformity_seg INTEGER DEFAULT 0,              -- critério entrega 2
    d3_special_freights INTEGER DEFAULT 0,            -- critério entrega 3
    d4_packaging_labelling INTEGER DEFAULT 0,         -- critério entrega 4
    d5_communication INTEGER DEFAULT 0,               -- critério entrega 5
    data_avaliacao DATE DEFAULT CURRENT_DATE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de Scorecard (agregada)
CREATE TABLE scorecard (
    id SERIAL PRIMARY KEY,
    fornecedor_id INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
    score_qualidade INTEGER DEFAULT 0,                -- valor independente 0-150
    score_comercial INTEGER DEFAULT 0,                -- soma C1-C5, 0-90
    score_entrega INTEGER DEFAULT 0,                  -- soma D1-D5, 0-60
    score_final DECIMAL(10,2) DEFAULT 0,              -- Qualidade + Comercial + Entrega (0-300)
    status VARCHAR(20) DEFAULT 'amarelo',             -- verde, amarelo, vermelho
    data_calculo DATE DEFAULT CURRENT_DATE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para melhor performance
CREATE INDEX idx_fornecedor_codigo ON fornecedores(codigo_material);
CREATE INDEX idx_qualidade_fornecedor ON criterios_qualidade(fornecedor_id);
CREATE INDEX idx_comercial_fornecedor ON criterios_comercial(fornecedor_id);
CREATE INDEX idx_entrega_fornecedor ON criterios_entrega(fornecedor_id);
CREATE INDEX idx_scorecard_fornecedor ON scorecard(fornecedor_id);
CREATE INDEX idx_scorecard_status ON scorecard(status);

-- =====================================================
-- INSERÇÃO DE DADOS DE EXEMPLO (3 FORNECEDORES - SCORECARD v2)
-- =====================================================

-- Fornecedor 1: ITM-001 (Score Final: 265 - VERDE)
-- Qualidade: 135, Comercial: 80 (C1-C5), Entrega: 50 (D1-D5) → Total: 265
INSERT INTO fornecedores (codigo_material, nome, pais, comprador, gestor_qualidade)
VALUES ('ITM-001', 'Fornecedor 1', 'Brasil', 'Enzo', 'Felipe');

INSERT INTO criterios_qualidade (fornecedor_id, score_qualidade)
VALUES (1, 135);

INSERT INTO criterios_comercial (fornecedor_id, c1_status_contratual, c2_negotiation_target, c3_competitiveness, c4_payment_terms, c5_communication)
VALUES (1, 25, 10, 10, 15, 20);

INSERT INTO criterios_entrega (fornecedor_id, d1_adherence_schedule, d2_conformity_seg, d3_special_freights, d4_packaging_labelling, d5_communication)
VALUES (1, 15, 10, 10, 5, 10);

-- Fornecedor 2: ITM-002 (Score Final: 210 - AMARELO)
-- Qualidade: 115, Comercial: 60 (C1-C5), Entrega: 35 (D1-D5) → Total: 210
INSERT INTO fornecedores (codigo_material, nome, pais, comprador, gestor_qualidade)
VALUES ('ITM-002', 'Fornecedor 2', 'Brasil', 'Enzo', 'Felipe');

INSERT INTO criterios_qualidade (fornecedor_id, score_qualidade)
VALUES (2, 115);

INSERT INTO criterios_comercial (fornecedor_id, c1_status_contratual, c2_negotiation_target, c3_competitiveness, c4_payment_terms, c5_communication)
VALUES (2, 15, 10, 10, 10, 15);

INSERT INTO criterios_entrega (fornecedor_id, d1_adherence_schedule, d2_conformity_seg, d3_special_freights, d4_packaging_labelling, d5_communication)
VALUES (2, 10, 5, 5, 5, 10);

-- Fornecedor 3: ITM-003 (Score Final: 130 - VERMELHO)
-- Qualidade: 70, Comercial: 35 (C1-C5), Entrega: 25 (D1-D5) → Total: 130
INSERT INTO fornecedores (codigo_material, nome, pais, comprador, gestor_qualidade)
VALUES ('ITM-003', 'Fornecedor 3', 'Brasil', 'Enzo', 'Felipe');

INSERT INTO criterios_qualidade (fornecedor_id, score_qualidade)
VALUES (3, 70);

INSERT INTO criterios_comercial (fornecedor_id, c1_status_contratual, c2_negotiation_target, c3_competitiveness, c4_payment_terms, c5_communication)
VALUES (3, 10, 5, 5, 5, 10);

INSERT INTO criterios_entrega (fornecedor_id, d1_adherence_schedule, d2_conformity_seg, d3_special_freights, d4_packaging_labelling, d5_communication)
VALUES (3, 5, 5, 5, 5, 5);

-- =====================================================
-- FUNÇÃO PARA CALCULAR SCORECARD AUTOMATICAMENTE
-- =====================================================

CREATE OR REPLACE FUNCTION calcular_scorecard(p_fornecedor_id INTEGER)
RETURNS TABLE (
    fornecedor_id INTEGER,
    score_qualidade INTEGER,
    score_comercial INTEGER,
    score_entrega INTEGER,
    score_final DECIMAL,
    status VARCHAR
) AS $$
DECLARE
    v_score_qualidade INTEGER;
    v_score_comercial INTEGER;
    v_score_entrega INTEGER;
    v_score_final DECIMAL;
    v_status VARCHAR;
BEGIN
    -- Obter Qualidade (valor independente 0-150)
    SELECT COALESCE(criterios_qualidade.score_qualidade, 0)
    INTO v_score_qualidade
    FROM criterios_qualidade
    WHERE criterios_qualidade.fornecedor_id = p_fornecedor_id
    ORDER BY criterios_qualidade.data_avaliacao DESC
    LIMIT 1;

    -- Obter Comercial (soma de C1-C5, 0-90)
    SELECT COALESCE(criterios_comercial.c1_status_contratual, 0) + 
           COALESCE(criterios_comercial.c2_negotiation_target, 0) + 
           COALESCE(criterios_comercial.c3_competitiveness, 0) + 
           COALESCE(criterios_comercial.c4_payment_terms, 0) + 
           COALESCE(criterios_comercial.c5_communication, 0)
    INTO v_score_comercial
    FROM criterios_comercial
    WHERE criterios_comercial.fornecedor_id = p_fornecedor_id
    ORDER BY criterios_comercial.data_avaliacao DESC
    LIMIT 1;

    -- Obter Entrega (soma de D1-D5, 0-60)
    SELECT COALESCE(criterios_entrega.d1_adherence_schedule, 0) + 
           COALESCE(criterios_entrega.d2_conformity_seg, 0) + 
           COALESCE(criterios_entrega.d3_special_freights, 0) + 
           COALESCE(criterios_entrega.d4_packaging_labelling, 0) + 
           COALESCE(criterios_entrega.d5_communication, 0)
    INTO v_score_entrega
    FROM criterios_entrega
    WHERE criterios_entrega.fornecedor_id = p_fornecedor_id
    ORDER BY criterios_entrega.data_avaliacao DESC
    LIMIT 1;

    -- Calcular Score Final (SOMA: Qualidade + Comercial + Entrega)
    -- Escala 0-300 (Qualidade 0-150 + Comercial 0-90 + Entrega 0-60)
    v_score_final := v_score_qualidade + v_score_comercial + v_score_entrega;

    -- Definir Status baseado no Score Final (Novos Thresholds - Braga v2)
    -- Verde: >= 240 (Excelência - >=80%)
    -- Amarelo: 180-239 (Aceitável/Monitoramento - >=60%)
    -- Vermelho: < 180 (Crítico - <60%)
    IF v_score_final >= 240 THEN
        v_status := 'verde';
    ELSIF v_score_final >= 180 THEN
        v_status := 'amarelo';
    ELSE
        v_status := 'vermelho';
    END IF;

    -- Deletar scorecard antigo se existir
    DELETE FROM scorecard WHERE scorecard.fornecedor_id = p_fornecedor_id;

    -- Inserir novo scorecard
    INSERT INTO scorecard (fornecedor_id, score_qualidade, score_comercial, score_entrega, score_final, status)
    VALUES (p_fornecedor_id, v_score_qualidade, v_score_comercial, v_score_entrega, v_score_final, v_status);

    RETURN QUERY SELECT p_fornecedor_id, v_score_qualidade, v_score_comercial, v_score_entrega, v_score_final, v_status;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- EXECUTAR CÁLCULOS PARA OS 3 FORNECEDORES
-- =====================================================

SELECT calcular_scorecard(1);
SELECT calcular_scorecard(2);
SELECT calcular_scorecard(3);

-- =====================================================
-- VERIFICAR DADOS INSERIDOS
-- =====================================================

SELECT * FROM fornecedores;
SELECT * FROM scorecard;