#!/usr/bin/env python3
"""
FastAPI App para Extração de Dados com Ollama

Este app fornece endpoints para extrair dados estruturados de textos
usando modelos LLM através do Ollama.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import requests
import json
import logging
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da aplicação
app = FastAPI(
    title="Extração de Dados com Ollama",
    description="API para extração máxima de dados estruturados de textos",
    version="1.0.0"
)

# Configuração do Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3")

# Modelos de entrada
class ExtractionRequest(BaseModel):
    texto: str
    contexto: Optional[str] = "ferroviario"
    modelo: Optional[str] = DEFAULT_MODEL

class ExtractionResponse(BaseModel):
    sucesso: bool
    dados_extraidos: Optional[Dict[str, Any]] = None
    erro: Optional[str] = None
    modelo_usado: str
    tokens_usados: Optional[int] = None

@app.get("/")
async def root():
    """Endpoint de status da API"""
    return {
        "status": "ativo",
        "servico": "Extração de Dados com Ollama",
        "versao": "1.0.0",
        "ollama_url": OLLAMA_BASE_URL,
        "modelo_padrao": DEFAULT_MODEL
    }

@app.get("/health")
async def health_check():
    """Verifica se o serviço Ollama está disponível"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "saudavel", "ollama": "disponivel"}
        else:
            return {"status": "erro", "ollama": "indisponivel"}
    except Exception as e:
        return {"status": "erro", "ollama": "indisponivel", "erro": str(e)}

@app.post("/extrair", response_model=ExtractionResponse)
async def extrair_dados(request: ExtractionRequest):
    """
    Extrai dados estruturados de um texto usando LLM
    
    Args:
        request: Dados da requisição com texto e contexto
        
    Returns:
        Dados extraídos em formato estruturado
    """
    try:
        # Importar a classe de prompt
        from prompt_extracao_maxima import PromptExtracao
        
        # Criar instância do extrator
        extrator = PromptExtracao()
        
        # Gerar prompt contextualizado
        prompt = extrator.gerar_prompt_contextualizado(
            request.texto, 
            request.contexto
        )
        
        # Preparar requisição para Ollama
        ollama_request = {
            "model": request.modelo,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_k": 10,
                "top_p": 0.9
            }
        }
        
        # Enviar para Ollama
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=ollama_request,
            timeout=120
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Erro do Ollama: {response.status_code}"
            )
        
        # Processar resposta
        ollama_response = response.json()
        resultado_texto = ollama_response.get("response", "")
        
        # Tentar extrair JSON da resposta
        try:
            # Procurar por JSON na resposta
            json_start = resultado_texto.find('{')
            json_end = resultado_texto.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = resultado_texto[json_start:json_end]
                dados_extraidos = json.loads(json_str)
            else:
                # Se não encontrar JSON, retornar texto bruto
                dados_extraidos = {
                    "resposta_bruta": resultado_texto,
                    "formato": "texto_nao_estruturado"
                }
        except json.JSONDecodeError:
            # Se falhar no parse JSON, retornar texto bruto
            dados_extraidos = {
                "resposta_bruta": resultado_texto,
                "formato": "json_invalido"
            }
        
        # Validar resultado
        dados_validados = extrator.validar_resultado(dados_extraidos)
        
        return ExtractionResponse(
            sucesso=True,
            dados_extraidos=dados_validados,
            modelo_usado=request.modelo,
            tokens_usados=ollama_response.get("eval_count", 0)
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão com Ollama: {e}")
        raise HTTPException(
            status_code=503,
            detail="Serviço Ollama indisponível"
        )
    except Exception as e:
        logger.error(f"Erro na extração: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@app.get("/modelos")
async def listar_modelos():
    """Lista modelos disponíveis no Ollama"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao listar modelos"
            )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erro de conexão: {str(e)}"
        )

@app.post("/modelo/baixar")
async def baixar_modelo(modelo: str):
    """Baixa um modelo no Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/pull",
            json={"name": modelo},
            timeout=600  # 10 minutos para download
        )
        if response.status_code == 200:
            return {"status": "sucesso", "modelo": modelo}
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao baixar modelo"
            )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erro de conexão: {str(e)}"
        )

@app.get("/contextos")
async def listar_contextos():
    """Lista contextos disponíveis para extração"""
    return {
        "contextos_disponiveis": [
            "ferroviario",
            "financeiro", 
            "geografico"
        ],
        "contexto_padrao": "ferroviario"
    }

# Middleware para CORS se necessário
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
