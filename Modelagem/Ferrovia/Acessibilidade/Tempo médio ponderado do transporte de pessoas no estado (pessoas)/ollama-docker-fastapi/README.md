# Ollama + FastAPI - Sistema Simplificado

Sistema completo para rodar modelos LLM localmente com Ollama e FastAPI como proxy transparente.

## 🎯 Funcionalidades

- **Ollama**: Servidor LLM rodando em container
- **FastAPI Proxy**: API que atua como proxy transparente para o Ollama
- **Prompts Externos**: Controle total dos prompts fora da aplicação
- **Conversa Direta**: Comunicação direta com os modelos via API

## 🚀 Início Rápido

### Pré-requisitos
- Docker e Docker Compose
- Python 3.8+ (para o cliente)

### Uma única linha para subir tudo:
```bash
docker compose up -d
```

### Com script automático:
```powershell
# Windows PowerShell
.\start.ps1
```

## 📁 Estrutura Simplificada

```
ollama-docker-fastapi/
├── Dockerfile              # Container da API
├── compose.yml             # Orquestração dos serviços
├── app.py                  # FastAPI Proxy (transparente)
├── requirements.txt        # Dependências Python
├── chat_client.py          # Cliente Python para teste
├── exemplo_prompts_externos.py  # Exemplos de uso
├── start.ps1              # Script de inicialização
└── README.md              # Este arquivo
```

## 🌐 Endpoints

### FastAPI Proxy (Porta 8000)
- `GET /health` - Status do sistema
- `GET /api/tags` - Listar modelos disponíveis
- `POST /api/generate` - Gerar texto
- `POST /api/chat` - Conversa com contexto
- `POST /api/pull` - Baixar novos modelos
- `GET /docs` - Documentação automática

### Ollama Direto (Porta 11434)
- Acesso direto ao Ollama (opcional)

## 💻 Uso via Cliente Python

```python
from chat_client import ChatClient

# Inicializar cliente
client = ChatClient()

# Verificar status
status = client.verificar_status()
print(status)

# Listar modelos
modelos = client.listar_modelos()
print(modelos)

# Conversar
resposta = client.conversar_simples(
    "Explique o que é transporte ferroviário",
    modelo="tinyllama"
)
print(resposta)
```

## 🎨 Prompts Externos - Filosofia

O sistema foi projetado para **não ter lógica de prompts internos**. Toda a inteligência de prompt fica **fora** da aplicação:

```python
# Seus prompts personalizados
prompt_extracao = f"""
Você é um especialista em análise de dados de transporte.
Extraia TODOS os dados do texto: {texto}
Retorne em formato JSON estruturado.
"""

# Envio via proxy (sem modificação)
resultado = client.conversar(
    prompt=prompt_extracao,
    modelo="tinyllama",
    temperature=0.1
)
```

### Vantagens:
- ✅ **Controle total** sobre prompts
- ✅ **Flexibilidade máxima** para diferentes casos de uso
- ✅ **FastAPI só transita** dados sem modificar
- ✅ **Facilidade de manutenção** e teste
- ✅ **Reutilização** de prompts em diferentes contextos

## 🔧 Instalação de Modelos

```bash
# Via container direto (recomendado)
docker exec ollama-server ollama pull tinyllama

# Verificar modelos instalados
curl http://localhost:8000/api/tags
```

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Seu Cliente   │───▶│  FastAPI Proxy  │───▶│     Ollama      │
│  (Prompts)      │    │  (Transparente) │    │   (Modelos)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      ▲                           │                       │
      │                           │                       │
      └───────────────────────────┴───────────────────────┘
                    Resposta sem modificação
```

### Fluxo de Dados:
1. **Cliente** envia prompt personalizado
2. **FastAPI Proxy** repassa exatamente como recebido
3. **Ollama** processa com o modelo escolhido
4. **Resposta** retorna sem modificações
5. **Cliente** recebe resposta pura do modelo

## ❓ Resolução de Problemas

### Container não inicia
```bash
docker compose logs
docker compose down && docker compose up -d
```

### Modelo não responde
```bash
# Verificar se modelo existe
curl http://localhost:8000/api/tags

# Baixar modelo se necessário
docker exec ollama-server ollama pull tinyllama
```

### Para parar tudo
```bash
docker compose down
```

## 🎯 Casos de Uso

### 1. Extração de Dados
```python
prompt = f"Extraia dados técnicos do texto: {texto_ferroviario}"
dados = client.conversar(prompt, "tinyllama", temperature=0.1)
```

### 2. Análise de Viabilidade
```python
prompt = f"Analise viabilidade financeira: {dados_projeto}"
analise = client.conversar(prompt, "tinyllama", temperature=0.3)
```

### 3. Geração de Relatórios
```python
prompt = f"Gere relatório executivo: {dados_completos}"
relatorio = client.conversar(prompt, "tinyllama", temperature=0.2)
```
