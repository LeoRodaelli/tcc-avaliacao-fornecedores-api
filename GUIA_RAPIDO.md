# 🚀 Guia Rápido - Primeira Entrega

## O que você recebeu?

Uma **API completa e funcional** que calcula o scorecard de fornecedores e se conecta ao Power BI.

---

## 📂 Arquivos Entregues

```
projeto/
├── main.py                    # API FastAPI
├── schema.sql                 # Script SQL do banco de dados
├── requirements.txt           # Dependências Python
├── Dockerfile                 # Containerização
├── docker-compose.yml         # Orquestração de serviços
├── .env.example               # Configurações de exemplo
├── README.md                  # Documentação completa
├── POWERBI_CONEXAO.md        # Guia Power BI
└── GUIA_RAPIDO.md            # Este arquivo
```

---

## ⚡ Setup em 5 Minutos (Com Docker)

### 1. Instale Docker e Docker Compose
- Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt-get install docker.io docker-compose`

### 2. Coloque todos os arquivos em uma pasta

```bash
mkdir projeto-tcc
cd projeto-tcc
# Coloque todos os arquivos aqui
```

### 3. Inicie os serviços

```bash
docker-compose up -d
```

### 4. Verifique se está rodando

```bash
# Teste a API
curl http://localhost:8000/health

# Ou abra no navegador
http://localhost:8000/docs
```

### 5. Pronto! 🎉

A API está rodando em `http://localhost:8000`

---

## 🔌 Como Conectar ao Power BI

1. Abra **Power BI Desktop**
2. Clique em **"Obter Dados"** → **"Web"**
3. Insira a URL: `http://localhost:8000/dashboard`
4. Clique em **"Conectar"**
5. Clique em **"Transformar Dados"**
6. Expanda as colunas `fornecedores`, `fornecedor` e `scorecard`
7. Clique em **"Fechar e Aplicar"**
8. Crie visualizações!

**Mais detalhes:** Veja o arquivo `POWERBI_CONEXAO.md`

---

## 📊 Dados Disponíveis

A API retorna dados de **3 fornecedores** com scorecard calculado:

| Fornecedor | Qualidade | Comercial | Entrega | Total | Status |
|-----------|-----------|-----------|---------|-------|--------|
| ITM-001 | 80 | 85 | 95 | 260 | 🟢 Verde |
| ITM-002 | 50 | 90 | 75 | 215 | 🟡 Amarelo |
| ITM-003 | 45 | 85 | 75 | 205 | 🟡 Amarelo |

---

## 🔗 Endpoints Principais

```bash
# Listar fornecedores
curl http://localhost:8000/fornecedores

# Scorecard de um fornecedor
curl http://localhost:8000/scorecard/1

# Dashboard (para Power BI)
curl http://localhost:8000/dashboard

# Documentação interativa
http://localhost:8000/docs
```

---

## 🗄️ Banco de Dados

**Tipo:** PostgreSQL  
**Host:** localhost (se local) ou seu servidor Locaweb  
**Porta:** 5432  
**Usuário:** usuario  
**Senha:** senha123  
**Banco:** tcc_fornecedores  

### Para conectar ao seu servidor Locaweb:

1. Edite o arquivo `.env`:
```
DATABASE_URL=postgresql://seu_usuario:sua_senha@seu_servidor_locaweb.com:5432/tcc_fornecedores
```

2. Reinicie a API:
```bash
docker-compose restart api
```

---

## 📈 Fórmula do Scorecard

```
Score Final = (Qualidade × 40%) + (Comercial × 20%) + (Entrega × 40%)

Status:
  🟢 Verde: Score ≥ 200
  🟡 Amarelo: 120 ≤ Score < 200
  🔴 Vermelho: Score < 120
```

---

## 🆘 Problemas Comuns

### "Não consigo conectar à API"
```bash
# Verifique se está rodando
docker-compose ps

# Se não estiver, inicie
docker-compose up -d
```

### "Porta 8000 já está em uso"
```bash
# Mude a porta no docker-compose.yml
# Ou mate o processo
lsof -i :8000
kill -9 <PID>
```

### "Erro de conexão com PostgreSQL"
```bash
# Verifique os logs
docker-compose logs postgres

# Reinicie
docker-compose restart postgres
```

---

## 📝 Próximas Entregas

- **Fase 2:** Adicionar mais fornecedores (15 total)
- **Fase 3:** Integração com inspeção 100%
- **Fase 4:** Histórico de scores
- **Fase 5:** Integração com SAP

---

## 📞 Contato

Qualquer dúvida, entre em contato com o desenvolvedor!

---

## ✅ Checklist

- [ ] Docker instalado
- [ ] Arquivos copiados para uma pasta
- [ ] `docker-compose up -d` executado
- [ ] API respondendo em `http://localhost:8000/health`
- [ ] Power BI conectado ao endpoint `/dashboard`
- [ ] Dashboard criado no Power BI

**Pronto para apresentar ao professor!** 🎓
