#!/usr/bin/env python3
"""
Teste da API de Extração de Dados
"""

import requests
import json
import time

# Configuração
API_BASE_URL = "http://localhost:8000"

def test_health():
    """Testa se a API está funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"Health Check: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro no health check: {e}")
        return False

def test_extraction():
    """Testa a extração de dados"""
    # Texto de exemplo
    texto_exemplo = """
    FER-001 - Linha Metropolitana BH-Contagem
    Extensão: 32,5 km
    Bitola: Métrica (1,00m)
    Estações: 15 paradas
    Velocidade: 80 km/h
    Capacidade: 1.200 passageiros por composição
    Tarifa: R$ 4,50 (econômica) / R$ 6,75 (executiva)
    Demanda: 45.000 passageiros/dia
    Receita anual: R$ 73.500.000
    Investimento: R$ 2.8 bilhões
    Municípios: Belo Horizonte, Contagem, Betim
    """
    
    # Dados da requisição
    payload = {
        "texto": texto_exemplo,
        "contexto": "ferroviario",
        "modelo": "llama3"
    }
    
    try:
        print("Enviando requisição para extração...")
        response = requests.post(
            f"{API_BASE_URL}/extrair",
            json=payload,
            timeout=120
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print("Extração realizada com sucesso!")
            print("=" * 50)
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        else:
            print(f"Erro: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def test_models():
    """Testa a listagem de modelos"""
    try:
        response = requests.get(f"{API_BASE_URL}/modelos", timeout=10)
        print(f"Modelos disponíveis: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Erro: {response.text}")
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")

def main():
    """Executa todos os testes"""
    print("🚀 Testando API de Extração de Dados")
    print("=" * 50)
    
    # Teste 1: Health Check
    print("\n1. Testando Health Check...")
    if not test_health():
        print("❌ API não está funcionando!")
        return
    
    # Teste 2: Listar modelos
    print("\n2. Testando listagem de modelos...")
    test_models()
    
    # Teste 3: Extração de dados
    print("\n3. Testando extração de dados...")
    test_extraction()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main()