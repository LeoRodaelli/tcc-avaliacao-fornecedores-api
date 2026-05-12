# Guia de Conexão: API FastAPI → Power BI

## 📊 Objetivo
Conectar a API de Scorecard de Fornecedores ao Power BI para criar dashboards em tempo real.

---

## 🔧 Pré-requisitos

1. **Power BI Desktop** instalado (versão 2023 ou superior)
2. **API rodando** em um servidor acessível (ex: `http://seu-servidor.com:8000`)
3. **Endpoint disponível:** `/dashboard` da API

---

## 📝 Passo 1: Obter os Dados da API

### 1.1 Testar a API
Antes de conectar ao Power BI, teste se a API está funcionando:

```bash
# Abra o navegador e acesse:
http://seu-servidor.com:8000/dashboard
```

Você deve receber um JSON assim:

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
    ...
  ]
}
```

---

## 🔌 Passo 2: Conectar Power BI à API

### 2.1 Abrir Power BI Desktop

1. Clique em **"Obter Dados"** (Get Data)
2. Procure por **"Web"** e clique nela
3. Clique em **"Conectar"**

### 2.2 Inserir a URL da API

Na janela que abrir, insira a URL do endpoint:

```
http://seu-servidor.com:8000/dashboard
```

**Ou, se estiver testando localmente:**

```
http://localhost:8000/dashboard
```

Clique em **"OK"**

### 2.3 Autenticação (se necessário)

Se a API não exigir autenticação, selecione **"Anônimo"** e clique em **"Conectar"**.

Se exigir, configure as credenciais apropriadas.

---

## 📥 Passo 3: Transformar os Dados

### 3.1 Abrir o Power Query

Após conectar, o Power BI vai mostrar os dados em formato JSON. Clique em **"Transformar Dados"** para abrir o Power Query.

### 3.2 Expandir a Tabela "fornecedores"

1. Na coluna **"fornecedores"**, você verá um ícone de **"Expandir"** (duas setas)
2. Clique nele para expandir a lista de fornecedores
3. Selecione as colunas que deseja (recomendado: todas)
4. Clique em **"OK"**

### 3.3 Expandir "fornecedor" e "scorecard"

Repita o processo para as colunas aninhadas:
- Expanda **"fornecedor"** para obter: `id`, `codigo_material`, `nome`, `pais`, `comprador`, `gestor_qualidade`
- Expanda **"scorecard"** para obter: `fornecedor_id`, `score_qualidade`, `score_comercial`, `score_entrega`, `score_final`, `status`

### 3.4 Remover Colunas Desnecessárias

Remova as colunas que não precisa (como `criado_em`, `atualizado_em`, etc.).

### 3.5 Carregar os Dados

Clique em **"Fechar e Aplicar"** para carregar os dados no Power BI.

---

## 📊 Passo 4: Criar Visualizações

### 4.1 Criar um Cartão de Resumo

1. Na aba **"Visualizações"**, clique em **"Cartão"**
2. Arraste o campo **"score_medio"** para a área de visualização
3. Configure o rótulo como "Score Médio"

### 4.2 Criar um Gráfico de Barras (Fornecedores por Status)

1. Clique em **"Gráfico de Barras Agrupadas"**
2. Arraste **"status"** para o eixo X
3. Arraste **"fornecedor_id"** para o eixo Y (será contado automaticamente)
4. Isso mostrará quantos fornecedores há em cada status (verde, amarelo, vermelho)

### 4.3 Criar uma Tabela de Detalhes

1. Clique em **"Tabela"**
2. Arraste os seguintes campos:
   - `codigo_material`
   - `nome`
   - `score_qualidade`
   - `score_comercial`
   - `score_entrega`
   - `score_final`
   - `status`

### 4.4 Adicionar Cores por Status

1. Selecione a visualização de tabela
2. Na aba **"Formatação"**, procure por **"Formatação Condicional"**
3. Selecione a coluna **"status"**
4. Configure as cores:
   - Verde = #22B14C
   - Amarelo = #FFC000
   - Vermelho = #C00000

---

## 🔄 Passo 5: Atualizar os Dados Automaticamente

### 5.1 Configurar Atualização Agendada

1. No Power BI Desktop, clique em **"Arquivo"** → **"Opções e Configurações"** → **"Opções"**
2. Procure por **"Atualização de Dados"**
3. Configure a frequência de atualização (ex: a cada 1 hora)

### 5.2 Publicar no Power BI Service (Nuvem)

Para que a atualização automática funcione na nuvem:

1. Clique em **"Publicar"** (no Power BI Desktop)
2. Selecione o workspace onde deseja publicar
3. No Power BI Service, acesse o dataset
4. Clique em **"Configurações"** → **"Atualização Agendada"**
5. Configure a frequência e horário de atualização

---

## 📌 Endpoints Disponíveis na API

Se quiser criar múltiplas conexões ou dashboards diferentes, aqui estão os endpoints:

| Endpoint | Descrição | Retorna |
|----------|-----------|---------|
| `/dashboard` | Dados agregados de todos os fornecedores | JSON com resumo e lista completa |
| `/fornecedores` | Lista todos os fornecedores | Array de fornecedores |
| `/fornecedores/{id}` | Detalhes de um fornecedor | Dados de um fornecedor específico |
| `/scorecard/{id}` | Scorecard de um fornecedor | Score calculado com status |

---

## 🔐 Segurança (Opcional)

Se quiser adicionar autenticação à API:

### Adicionar Token de Autenticação

No Power BI, ao conectar à API:

1. Selecione **"Autenticação Básica"** ou **"Autenticação de Chave"**
2. Insira o token/chave fornecido
3. Clique em **"Conectar"**

---

## 🐛 Troubleshooting

### Problema: "Não consigo conectar à API"

**Solução:**
- Verifique se a API está rodando: `http://seu-servidor.com:8000/health`
- Verifique o firewall e permissões de rede
- Confirme que a URL está correta

### Problema: "Erro de JSON inválido"

**Solução:**
- Teste a API no navegador primeiro
- Verifique se o banco de dados está conectado corretamente
- Veja os logs da API para mais detalhes

### Problema: "A atualização não funciona"

**Solução:**
- Se estiver no Power BI Service, configure o gateway de dados
- Verifique se a API está sempre acessível
- Aumente o timeout da conexão

---

## 📈 Exemplo de Dashboard Completo

Um dashboard completo deve incluir:

1. **KPIs (Cartões):**
   - Total de Fornecedores
   - Score Médio
   - Fornecedores Verde
   - Fornecedores Amarelo
   - Fornecedores Vermelho

2. **Gráficos:**
   - Distribuição por Status (Pizza ou Barras)
   - Score por Fornecedor (Barras Horizontais)
   - Tendência de Scores (Linha)

3. **Tabelas:**
   - Detalhes de cada fornecedor
   - Breakdown de critérios (Qualidade, Comercial, Entrega)

4. **Filtros:**
   - Por Status (Verde, Amarelo, Vermelho)
   - Por Comprador
   - Por Gestor de Qualidade

---

## 📞 Suporte

Se tiver dúvidas:

1. Consulte a documentação da API: `http://seu-servidor.com:8000/docs`
2. Verifique os logs da API
3. Teste os endpoints diretamente no navegador ou Postman

---

## ✅ Checklist Final

- [ ] API está rodando e acessível
- [ ] Endpoint `/dashboard` retorna dados válidos
- [ ] Power BI Desktop está instalado
- [ ] Conexão com a API foi estabelecida
- [ ] Dados foram transformados corretamente
- [ ] Visualizações foram criadas
- [ ] Atualização automática foi configurada
- [ ] Dashboard foi publicado (opcional)

Pronto! Seu dashboard está conectado à API e recebendo dados em tempo real! 🎉
