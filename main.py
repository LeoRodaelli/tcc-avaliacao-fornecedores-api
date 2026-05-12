"""
API de Avaliação de Fornecedores - TCC
Sistema de Scorecard com integração PostgreSQL
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
import os
from decimal import Decimal
import requests
import json
from dotenv import load_dotenv
import traceback

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# =====================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =====================================================

# Variáveis de ambiente (ajuste conforme necessário)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://usuario:senha@localhost:5432/tcc_fornecedores"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =====================================================
# MODELOS DO BANCO DE DADOS
# =====================================================

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_material = Column(String(50), unique=True, index=True)
    nome = Column(String(255))
    pais = Column(String(100))
    comprador = Column(String(100))
    gestor_qualidade = Column(String(100))
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CriteriosQualidade(Base):
    __tablename__ = "criterios_qualidade"
    
    id = Column(Integer, primary_key=True, index=True)
    fornecedor_id = Column(Integer, index=True)
    score_qualidade = Column(Integer, default=0)  # Valor independente 0-150
    data_avaliacao = Column(Date, default=date.today)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CriteriosEntrega(Base):
    __tablename__ = "criterios_entrega"
    
    id = Column(Integer, primary_key=True, index=True)
    fornecedor_id = Column(Integer, index=True)
    d1_adherence_schedule = Column(Integer, default=0)
    d2_conformity_seg = Column(Integer, default=0)
    d3_special_freights = Column(Integer, default=0)
    d4_packaging_labelling = Column(Integer, default=0)
    d5_communication = Column(Integer, default=0)
    data_avaliacao = Column(Date, default=date.today)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CriteriosComercial(Base):
    __tablename__ = "criterios_comercial"
    
    id = Column(Integer, primary_key=True, index=True)
    fornecedor_id = Column(Integer, index=True)
    c1_status_contratual = Column(Integer, default=0)
    c2_negotiation_target = Column(Integer, default=0)
    c3_competitiveness = Column(Integer, default=0)
    c4_payment_terms = Column(Integer, default=0)
    c5_communication = Column(Integer, default=0)
    data_avaliacao = Column(Date, default=date.today)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Scorecard(Base):
    __tablename__ = "scorecard"
    
    id = Column(Integer, primary_key=True, index=True)
    fornecedor_id = Column(Integer, index=True)
    score_qualidade = Column(Integer, default=0)
    peso_qualidade = Column(Numeric(5, 2), default=40.00)
    score_comercial = Column(Integer, default=0)
    peso_comercial = Column(Numeric(5, 2), default=20.00)
    score_entrega = Column(Integer, default=0)
    peso_entrega = Column(Numeric(5, 2), default=40.00)
    score_final = Column(Numeric(10, 2), default=0)
    status = Column(String(20), default="amarelo")
    data_calculo = Column(Date, default=date.today)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# =====================================================
# SCHEMAS PYDANTIC (Para requisições/respostas)
# =====================================================

class CriteriosQualidadeSchema(BaseModel):
    c1_status_contratual: int
    c2_negotiation_target: int
    c3_competitiveness: int
    c4_payment_terms: int
    c5_communication: int
    
    class Config:
        from_attributes = True

class CriteriosEntregaSchema(BaseModel):
    d1_adherence_schedule: int
    d2_conformity_seg: int
    d3_special_freights: int
    d4_packaging_labelling: int
    d5_communication: int
    
    class Config:
        from_attributes = True

class CriteriosComercialSchema(BaseModel):
    score_comercial: int
    
    class Config:
        from_attributes = True

class ScorecardSchema(BaseModel):
    fornecedor_id: int
    score_qualidade: int
    score_comercial: int
    score_entrega: int
    score_final: float
    status: str
    
    class Config:
        from_attributes = True

class FornecedorSchema(BaseModel):
    id: int
    codigo_material: str
    nome: str
    pais: str
    comprador: str
    gestor_qualidade: str
    
    class Config:
        from_attributes = True

class FornecedorComScorecardSchema(BaseModel):
    fornecedor: FornecedorSchema
    scorecard: ScorecardSchema
    
    class Config:
        from_attributes = True

class DashboardSchema(BaseModel):
    total_fornecedores: int
    fornecedores_verde: int
    fornecedores_amarelo: int
    fornecedores_vermelho: int
    score_medio: float
    fornecedores: List[FornecedorComScorecardSchema]

# =====================================================
# INICIALIZAR FASTAPI
# =====================================================

app = FastAPI(
    title="API de Avaliação de Fornecedores",
    description="Sistema de Scorecard para TCC - Engenharia de Produção",
    version="1.0.0"
)

# Adicionar CORS para permitir requisições do Power BI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DEPENDENCY: Obter sessão do banco
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# ENDPOINTS DA API
# =====================================================

@app.get("/", tags=["Info"])
def root():
    """Endpoint raiz - Informações da API"""
    return {
        "nome": "API de Avaliação de Fornecedores",
        "versao": "1.0.0",
        "descricao": "Sistema de Scorecard para TCC",
        "endpoints": {
            "fornecedores": "/fornecedores",
            "scorecard": "/scorecard/{fornecedor_id}",
            "dashboard": "/dashboard",
            "documentacao": "/docs"
        }
    }

@app.get("/fornecedores", response_model=List[FornecedorSchema], tags=["Fornecedores"])
def listar_fornecedores(db: Session = Depends(get_db)):
    """
    Listar todos os fornecedores
    """
    fornecedores = db.query(Fornecedor).all()
    if not fornecedores:
        raise HTTPException(status_code=404, detail="Nenhum fornecedor encontrado")
    return fornecedores

# IMPORTANTE: Esta rota DEVE vir ANTES de /fornecedores/{fornecedor_id}
# caso contrário, FastAPI tentará interpretar "codigo" como um fornecedor_id
@app.get("/fornecedores/codigo/{codigo_material}", response_model=FornecedorSchema, tags=["Fornecedores"])
def obter_fornecedor_por_codigo(codigo_material: str, db: Session = Depends(get_db)):
    """
    Obter detalhes de um fornecedor por código de material
    Exemplo: GET /fornecedores/codigo/ITM-001
    """
    print(f"[DEBUG] Buscando fornecedor com código: {codigo_material}")
    fornecedor = db.query(Fornecedor).filter(Fornecedor.codigo_material == codigo_material).first()
    if not fornecedor:
        print(f"[DEBUG] Fornecedor com código {codigo_material} não encontrado")
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    print(f"[DEBUG] Fornecedor encontrado: {fornecedor.nome}")
    return fornecedor

@app.get("/fornecedores/{fornecedor_id}", response_model=FornecedorSchema, tags=["Fornecedores"])
def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """
    Obter detalhes de um fornecedor específico por ID
    Exemplo: GET /fornecedores/1
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@app.get("/scorecard/{fornecedor_id}", response_model=ScorecardSchema, tags=["Scorecard"])
def obter_scorecard(fornecedor_id: int, db: Session = Depends(get_db)):
    """
    Obter scorecard de um fornecedor
    Calcula: Qualidade + Comercial + Entrega com pesos
    """
    # Verificar se fornecedor existe
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    # Obter critérios
    qualidade = db.query(CriteriosQualidade).filter(
        CriteriosQualidade.fornecedor_id == fornecedor_id
    ).order_by(CriteriosQualidade.data_avaliacao.desc()).first()
    
    comercial = db.query(CriteriosComercial).filter(
        CriteriosComercial.fornecedor_id == fornecedor_id
    ).order_by(CriteriosComercial.data_avaliacao.desc()).first()
    
    entrega = db.query(CriteriosEntrega).filter(
        CriteriosEntrega.fornecedor_id == fornecedor_id
    ).order_by(CriteriosEntrega.data_avaliacao.desc()).first()
    
    # Calcular scores
    # Qualidade: valor independente (0-150)
    score_qualidade = qualidade.score_qualidade if qualidade else 0
    
    # Comercial: soma de C1-C5 (0-90)
    score_comercial = 0
    if comercial:
        score_comercial = (
            (comercial.c1_status_contratual or 0) +
            (comercial.c2_negotiation_target or 0) +
            (comercial.c3_competitiveness or 0) +
            (comercial.c4_payment_terms or 0) +
            (comercial.c5_communication or 0)
        )
    
    # Entrega: soma de D1-D5 (0-60)
    score_entrega = 0
    if entrega:
        score_entrega = (
            (entrega.d1_adherence_schedule or 0) +
            (entrega.d2_conformity_seg or 0) +
            (entrega.d3_special_freights or 0) +
            (entrega.d4_packaging_labelling or 0) +
            (entrega.d5_communication or 0)
        )
    
    # Score final = Qualidade + Comercial + Entrega (0-300)
    score_final = score_qualidade + score_comercial + score_entrega
    
    # Determinar status baseado em thresholds
    if score_final >= 240:
        status = "verde"
    elif score_final >= 180:
        status = "amarelo"
    else:
        status = "vermelho"
    
    return {
        "fornecedor_id": fornecedor_id,
        "score_qualidade": score_qualidade,
        "score_comercial": score_comercial,
        "score_entrega": score_entrega,
        "score_final": float(score_final),
        "status": status
    }

@app.get("/dashboard", tags=["Dashboard"])
def obter_dashboard(db: Session = Depends(get_db)):
    """
    Obter dashboard com resumo de todos os fornecedores
    """
    fornecedores = db.query(Fornecedor).all()
    
    if not fornecedores:
        raise HTTPException(status_code=404, detail="Nenhum fornecedor encontrado")
    
    fornecedores_com_scorecard = []
    scores = []
    
    for fornecedor in fornecedores:
        scorecard = obter_scorecard(fornecedor.id, db)
        fornecedores_com_scorecard.append({
            "fornecedor": fornecedor,
            "scorecard": scorecard
        })
        scores.append(scorecard["score_final"])
    
    # Contar por status
    verde = sum(1 for f in fornecedores_com_scorecard if f["scorecard"]["status"] == "verde")
    amarelo = sum(1 for f in fornecedores_com_scorecard if f["scorecard"]["status"] == "amarelo")
    vermelho = sum(1 for f in fornecedores_com_scorecard if f["scorecard"]["status"] == "vermelho")
    
    score_medio = sum(scores) / len(scores) if scores else 0
    
    return {
        "total_fornecedores": len(fornecedores),
        "fornecedores_verde": verde,
        "fornecedores_amarelo": amarelo,
        "fornecedores_vermelho": vermelho,
        "score_medio": score_medio,
        "fornecedores": fornecedores_com_scorecard
    }

@app.get("/dashboard/codigo/{codigo_material}", tags=["Dashboard"])
def obter_dashboard_por_codigo(codigo_material: str, db: Session = Depends(get_db)):
    """
    Obter scorecard de um fornecedor específico por código de material
    Combina dados do fornecedor com seu scorecard
    """
    fornecedor = obter_fornecedor_por_codigo(codigo_material, db)
    scorecard = obter_scorecard(fornecedor.id, db)
    
    # Chamar o endpoint de obter_scorecard que já faz o cálculo
    return obter_scorecard(fornecedor.id, db)

# =====================================================
# POWER BI INTEGRATION
# =====================================================

POWER_BI_CONFIG = {
    "client_id": os.getenv("POWERBI_CLIENT_ID", ""),
    "client_secret": os.getenv("POWERBI_CLIENT_SECRET", ""),
    "tenant_id": os.getenv("POWERBI_TENANT_ID", ""),
    "report_id": os.getenv("POWERBI_REPORT_ID", ""),
    "workspace_id": os.getenv("POWERBI_WORKSPACE_ID", "me")
}

@app.get("/powerbi/token", tags=["Power BI"])
def get_powerbi_token():
    """
    Gerar token de acesso para Power BI Embedded
    """
    try:
        # Validar configurações
        if not POWER_BI_CONFIG["client_id"]:
            raise ValueError("POWERBI_CLIENT_ID nao configurado")
        if not POWER_BI_CONFIG["client_secret"]:
            raise ValueError("POWERBI_CLIENT_SECRET nao configurado")
        if not POWER_BI_CONFIG["tenant_id"]:
            raise ValueError("POWERBI_TENANT_ID nao configurado")
        
        token_url = f"https://login.microsoftonline.com/{POWER_BI_CONFIG['tenant_id']}/oauth2/v2.0/token"
        print(f"[DEBUG] Token URL: {token_url}")
        
        token_data = {
            "grant_type": "client_credentials",
            "client_id": POWER_BI_CONFIG["client_id"],
            "client_secret": POWER_BI_CONFIG["client_secret"],
            "scope": "https://analysis.windows.net/.default"
        }
        
        print(f"[DEBUG] Enviando requisicao para Azure AD...")
        response = requests.post(token_url, data=token_data, timeout=10)
        print(f"[DEBUG] Status Code: {response.status_code}")
        
        if response.status_code != 200:
            error_detail = response.text
            print(f"[DEBUG] Erro da resposta: {error_detail}")
            raise HTTPException(status_code=500, detail=f"Azure AD retornou erro: {error_detail}")
        
        token_response = response.json()
        
        if "access_token" not in token_response:
            print(f"[DEBUG] Resposta sem access_token: {token_response}")
            raise ValueError("Resposta do Azure AD nao contem access_token")
        
        print(f"[DEBUG] Token gerado com sucesso")
        return {
            "access_token": token_response.get("access_token"),
            "token_type": "Bearer",
            "expires_in": token_response.get("expires_in"),
            "report_id": POWER_BI_CONFIG["report_id"],
            "workspace_id": POWER_BI_CONFIG["workspace_id"]
        }
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[ERROR] Erro ao gerar token Power BI: {error_msg}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao gerar token: {error_msg}")

@app.get("/powerbi/config", tags=["Power BI"])
def get_powerbi_config():
    """
    Retornar configuracoes do Power BI (sem dados sensíveis)
    """
    return {
        "report_id": POWER_BI_CONFIG["report_id"],
        "workspace_id": POWER_BI_CONFIG["workspace_id"],
        "embed_url": f"https://app.powerbi.com/reportEmbed?reportId={POWER_BI_CONFIG['report_id']}&groupId={POWER_BI_CONFIG['workspace_id']}"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check da API
    """
    return {"status": "ok", "timestamp": datetime.utcnow()}

# =====================================================
# EXECUTAR A API
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
