# Sistema de Avaliação de Fornecedores - API

## 📋 Descrição

API FastAPI para cálculo de scorecard de fornecedores com integração PostgreSQL e Power BI. Desenvolvida para o projeto de TCC em Engenharia de Produção.

**Versão:** 1.0.0  
**Status:** Primeira Entrega (PoC com 3 fornecedores)

---

## 🎯 Funcionalidades

✅ Cálculo automático de scorecard com 3 pilares (Qualidade, Comercial, Entrega)  
✅ Sistema de Traffic Light (Verde, Amarelo, Vermelho)  
✅ Pesos configuráveis para cada pilar  
✅ Integração com PostgreSQL  
✅ Endpoints RESTful para consulta de dados  
✅ Dashboard agregado para Power BI  
✅ Documentação automática (Swagger)  
✅ CORS habilitado para Power BI  

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      Power BI Desktop                        │
│                    (Visualizações)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    HTTP GET /dashboard
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI (Python)                          │
│              (Cálculo de Scorecard)                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Endpoints:                                          │   │
│  │ • GET /fornecedores                                 │   │
│  │ • GET /scorecard/{id}                               │   │
│  │ • GET /dashboard                                    │   │
│  │ • GET /docs (Swagger)                               │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    SQLAlchemy ORM
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              PostgreSQL (Banco de Dados)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tabelas:                                            │   │
│  │ • fornecedores                                      │   │
│  │ • criterios_qualidade                               │   │
│  │ • criterios_entrega                                 │   │
│  │ • criterios_comercial                               │   │
│  │ • scorecard                                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Pré-requisitos

### Opção 1: Docker (Recomendado)
- Docker Desktop instalado
- Docker Compose instalado

### Opção 2: Local
- Python 3.11+
- PostgreSQL 15+
- pip (gerenciador de pacotes Python)

---

## 🚀 Instalação e Execução

### Opção 1: Com Docker Compose (Mais Fácil)

#### 1. Clone ou baixe os arquivos

```bash
# Certifique-se de ter os seguintes arquivos no mesmo diretório:
# - docker-compose.yml
# - Dockerfile
# - main.py
# - requirements.txt
# - schema.sql
# - .env.example
```

#### 2. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env se necessário (opcional, valores padrão já estão configurados)
```

#### 3. Inicie os serviços

```bash
# Inicie PostgreSQL e API
docker-compose up -d

# Verifique se está rodando
docker-compose ps
```

#### 4. Verifique se está funcionando

```bash
# Teste a API
curl http://localhost:8000/health

# Acesse a documentação Swagger
# Abra no navegador: http://localhost:8000/docs
```

---

### Opção 2: Instalação Local

#### 1. Instale as dependências Python

```bash
pip install -r requirements.txt
```

#### 2. Configure o PostgreSQL

```bash
# Crie um banco de dados
createdb tcc_fornecedores

# Execute o script SQL
psql -U seu_usuario -d tcc_fornecedores -f schema.sql
```

#### 3. Configure a variável de ambiente

```bash
# Crie um arquivo .env
cp .env.example .env

# Edite o .env com suas credenciais do PostgreSQL
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/tcc_fornecedores
```

#### 4. Execute a API

```bash
# Opção A: Com uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opção B: Com Python direto
python main.py
```

#### 5. Acesse a API

```
http://localhost:8000
http://localhost:8000/docs (Swagger UI)
```

---

## 📊 Estrutura de Dados

### Tabelas Principais

#### `fornecedores`
```sql
id (PK)
codigo_material (UNIQUE)
nome
pais
comprador
gestor_qualidade
criado_em
atualizado_em
```

#### `criterios_qualidade`
```sql
id (PK)
fornecedor_id (FK)
c1_status_contratual (max 25)
c2_negotiation_target (max 25)
c3_competitiveness (max 5)
c4_payment_terms (max 20)
c5_communication (max 10)
data_avaliacao
```

#### `criterios_entrega`
```sql
id (PK)
fornecedor_id (FK)
d1_adherence_schedule (max 25)
d2_conformity_seg (max 30)
d3_special_freights (max 20)
d4_packaging_labelling (max 10)
d5_communication (max 15)
data_avaliacao
```

#### `criterios_comercial`
```sql
id (PK)
fornecedor_id (FK)
score_comercial (0-100)
data_avaliacao
```

#### `scorecard`
```sql
id (PK)
fornecedor_id (FK)
score_qualidade
score_comercial
score_entrega
score_final
status (verde/amarelo/vermelho)
data_calculo
```

---

## 🔌 Endpoints da API

### Informações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Health check |
| GET | `/docs` | Documentação Swagger |

### Fornecedores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/fornecedores` | Listar todos os fornecedores |
| GET | `/fornecedores/{id}` | Obter detalhes de um fornecedor |

### Scorecard

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/scorecard/{id}` | Obter scorecard de um fornecedor |
| POST | `/scorecard/calcular/{id}` | Forçar recálculo do scorecard |

### Dashboard

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/dashboard` | Dados agregados para Power BI |

---

## 📈 Fórmula de Cálculo do Scorecard

```
Score Qualidade = C1 + C2 + C3 + C4 + C5
Score Comercial = Valor direto (0-100)
Score Entrega = D1 + D2 + D3 + D4 + D5

Score Final = (Qualidade × 0.40) + (Comercial × 0.20) + (Entrega × 0.40)

Status:
  - Verde: Score Final ≥ 200
  - Amarelo: 120 ≤ Score Final < 200
  - Vermelho: Score Final < 120
```

---

## 🔗 Integração com Power BI

Para conectar ao Power BI, consulte o arquivo **POWERBI_CONEXAO.md** que contém:

1. Passo a passo de conexão
2. Transformação de dados
3. Criação de visualizações
4. Configuração de atualização automática

**Resumo rápido:**
1. Power BI → Obter Dados → Web
2. Insira a URL: `http://seu-servidor:8000/dashboard`
3. Transforme os dados no Power Query
4. Crie visualizações

---

## 🔐 Segurança

### Recomendações para Produção

1. **Autenticação:** Adicione JWT ou OAuth2
2. **HTTPS:** Use certificados SSL/TLS
3. **Rate Limiting:** Implemente limite de requisições
4. **Validação:** Valide todas as entradas
5. **Logs:** Configure logging centralizado
6. **Variáveis de Ambiente:** Nunca commite credenciais

### Exemplo de Autenticação (Futuro)

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/dashboard", security=Depends(security))
def obter_dashboard(credentials: HTTPAuthCredentials = Depends(security)):
    # Validar token
    pass
```

---

## 🐛 Troubleshooting

### Problema: Erro de conexão com PostgreSQL

**Solução:**
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps

# Verifique as credenciais no .env
cat .env

# Reinicie os serviços
docker-compose restart postgres
```

### Problema: Porta 8000 já está em uso

**Solução:**
```bash
# Mude a porta no docker-compose.yml
# Ou mate o processo que está usando a porta
lsof -i :8000
kill -9 <PID>
```

### Problema: Dados não aparecem no Power BI

**Solução:**
1. Verifique se a API está respondendo: `curl http://localhost:8000/dashboard`
2. Verifique se há dados no banco: `docker-compose exec postgres psql -U usuario -d tcc_fornecedores -c "SELECT * FROM fornecedores;"`
3. Atualize a conexão no Power BI

---

## 📝 Exemplo de Requisição/Resposta

### GET /dashboard

**Requisição:**
```bash
curl http://localhost:8000/dashboard
```

**Resposta:**
```json
{
  "total_fornecedores": 3,
  "fornecedores_verde": 1,
  "fornecedores_amarelo": 1,
  "fornecedores_vermelho": 1,
  "score_medio": 180.5,
  "fornecedores": [
    {
      "fornecedor": {
        "id": 1,
        "codigo_material": "ITM-001",
        "nome": "Fornecedor 1",
        "pais": "Brasil",
        "comprador": "Enzo",
        "gestor_qualidade": "Felipe"
      },
      "scorecard": {
        "fornecedor_id": 1,
        "score_qualidade": 80,
        "score_comercial": 85,
        "score_entrega": 95,
        "score_final": 86.5,
        "status": "verde"
      }
    }
  ]
}
```

---

## 📚 Próximos Passos

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar inspeção 100% com fotos
- [ ] Adicionar histórico de scores
- [ ] Criar alertas automáticos
- [ ] Integrar com SAP (OData/RFC)
- [ ] Adicionar visão computacional para inspeção
- [ ] Deploy em produção

---

## 👥 Equipe

- **Desenvolvedor:** Você (Freelancer)
- **Cliente/Estagiário:** Braga (SEG Automotive)
- **Orientador:** Professor de TCC (PUC-Campinas)

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Consulte a documentação Swagger: `http://localhost:8000/docs`
2. Verifique os logs: `docker-compose logs -f api`
3. Teste os endpoints com Postman ou curl

---

## 📄 Licença

Este projeto é parte do TCC em Engenharia de Produção - PUC-Campinas.

---

## ✅ Checklist de Entrega

- [x] Banco de dados PostgreSQL estruturado
- [x] API FastAPI com endpoints funcionais
- [x] Cálculo de scorecard com pesos
- [x] Sistema de Traffic Light
- [x] Integração com Power BI
- [x] Docker e Docker Compose
- [x] Documentação completa
- [ ] Deploy em produção (próxima fase)
- [ ] Testes automatizados (próxima fase)
- [ ] Autenticação (próxima fase)

---

**Última atualização:** 31/03/2026  
**Versão:** 1.0.0 (PoC)
