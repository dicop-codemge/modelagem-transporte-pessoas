"""
🎯 Cliente de Chat - Sistema Ollama + FastAPI
Para usar: docker exec -it fastapi-proxy python chat_client.py
"""

import requests
import json
import time


class ChatClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def verificar_status(self):
        """Verifica status do sistema"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except Exception as e:
            return {"status": "erro", "erro": str(e)}
    
    def listar_modelos(self):
        """Lista modelos disponíveis"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            return []
    
    def conversar(self, prompt, modelo="tinyllama", temperature=0.7):
        """Conversa com o modelo"""
        try:
            payload = {
                "model": modelo,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                elapsed = time.time() - start_time
                
                return {
                    "sucesso": True,
                    "resposta": result.get("response", ""),
                    "tempo": round(elapsed, 2),
                    "tokens": result.get("eval_count", 0)
                }
            else:
                return {
                    "sucesso": False,
                    "erro": f"Status {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"sucesso": False, "erro": str(e)}
    
    def conversar_simples(self, prompt, modelo="tinyllama"):
        """Conversa simples - retorna apenas o texto"""
        resultado = self.conversar(prompt, modelo)
        if resultado["sucesso"]:
            return resultado["resposta"]
        else:
            return f"Erro: {resultado['erro']}"


def demonstracao():
    """Demonstração do sistema"""
    print("💬 DEMONSTRAÇÃO - Sistema Ollama + FastAPI")
    print("=" * 60)
    
    client = ChatClient()
    
    # Verificar status
    print("📊 Verificando status...")
    status = client.verificar_status()
    print(f"Status: {status}")
    
    if status.get("status") != "saudavel":
        print("❌ Sistema não está saudável. Verifique os containers.")
        return
    
    # Listar modelos
    print("\n📋 Modelos disponíveis:")
    modelos = client.listar_modelos()
    if not modelos:
        print("❌ Nenhum modelo encontrado.")
        print("💡 Execute: docker exec ollama-server ollama pull tinyllama")
        return
    
    for modelo in modelos:
        print(f"  • {modelo}")
    
    modelo_escolhido = modelos[0]
    print(f"\n💬 Testando conversa com: {modelo_escolhido}")
    
    # Testes
    testes = [
        {
            "nome": "Teste Simples",
            "prompt": "Oi! Em uma frase, me diga o que você faz.",
            "temperatura": 0.3
        },
        {
            "nome": "Análise Técnica",
            "prompt": """Analise este projeto ferroviário:
            
Projeto: Linha Metro Express
- Extensão: 45 km
- Estações: 12
- Velocidade: 80 km/h
- Investimento: R$ 2,1 bilhões
- Capacidade: 60.000 passageiros/dia
- Tarifa: R$ 6,50

Retorne uma análise técnica em 3 pontos principais.""",
            "temperatura": 0.2
        }
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n🧪 TESTE {i}: {teste['nome']}")
        print(f"📝 Prompt: {teste['prompt'][:50]}...")
        
        resultado = client.conversar(
            prompt=teste["prompt"],
            modelo=modelo_escolhido,
            temperature=teste["temperatura"]
        )
        
        if resultado["sucesso"]:
            print(f"✅ Resposta ({resultado['tempo']}s):")
            print(f"📝 {resultado['resposta'][:200]}...")
            if resultado["tokens"] > 0:
                print(f"🔢 Tokens: {resultado['tokens']}")
        else:
            print(f"❌ Erro: {resultado['erro']}")
    
    print(f"\n🎨 EXEMPLO: Prompt Personalizado")
    print("=" * 40)
    
    # Exemplo de prompt personalizado para transporte
    prompt_personalizado = """
Você é um consultor especialista em transporte público.

CENÁRIO:
Uma cidade de 500.000 habitantes quer implementar um sistema de VLT (Veículo Leve sobre Trilhos).

DADOS:
- Orçamento disponível: R$ 800 milhões
- Demanda estimada: 35.000 passageiros/dia
- Extensão proposta: 25 km
- Número de estações: 18

TAREFA:
Avalie a viabilidade deste projeto em exatamente 4 pontos:
1. Viabilidade Financeira
2. Viabilidade Técnica  
3. Impacto Social
4. Recomendação Final

Seja direto e técnico.
"""
    
    print("🤖 Executando análise especializada...")
    resultado = client.conversar(
        prompt=prompt_personalizado,
        modelo=modelo_escolhido,
        temperature=0.1  # Baixa criatividade para análise técnica
    )
    
    if resultado["sucesso"]:
        print("✅ Análise de Viabilidade:")
        print(resultado["resposta"])
        print(f"\n⏱️ Tempo: {resultado['tempo']}s")
    else:
        print(f"❌ Erro: {resultado['erro']}")


if __name__ == "__main__":
    demonstracao()
