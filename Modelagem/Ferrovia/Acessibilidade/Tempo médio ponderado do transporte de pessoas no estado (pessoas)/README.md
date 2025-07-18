# 🚀 Sistema de Extração Máxima de Dados Ferroviários

Este projeto fornece um sistema completo para extração máxima de dados estruturados de documentos PDF ferroviários e conversão em formato tabular.

## 📁 Arquivos Principais

### 🔧 Módulos de Processamento
- **`pdf_processor.py`** - Processador principal para extração de PDFs
- **`ferroviario_processor.py`** - Processador especializado em dados ferroviários
- **`maximize_extraction.py`** - Script para extração máxima com regex avançados

### 🎯 Sistema de Prompts
- **`prompt_extracao_maxima.py`** - Classe principal com prompts especializados para LLMs
- **`exemplo_uso_completo.py`** - Exemplos práticos de uso com diferentes LLMs

### 🐳 Container Docker
- **`ollama-docker-fastapi/`** - Container completo com Ollama + FastAPI
  - API REST para extração de dados
  - Interface web para testes
  - Prompt integrado (removido do container, agora externo)

### 📊 Análise e Exemplos
- **`exemplo_extracao_maxima.py`** - Exemplo prático de extração
- **`code.ipynb`** - Notebook Jupyter para análise interativa

## 🎯 Como Usar

### 1. Prompt Especializado para LLMs

```python
from prompt_extracao_maxima import PromptExtracao

# Criar extrator
extrator = PromptExtracao()

# Gerar prompt contextualizado
prompt = extrator.gerar_prompt_contextualizado(texto, "ferroviario")

# Usar com seu LLM preferido (GPT, Claude, Ollama)
```

### 2. Processamento de PDFs

```python
from maximize_extraction import processar_pdf_maximo

# Extrair dados máximos de um PDF
dados = processar_pdf_maximo("documento.pdf")
```

### 3. API Docker (Ollama + FastAPI)

```bash
cd ollama-docker-fastapi
docker-compose up -d

# Testar API
python test_api.py
```

## 🎯 Campos Extraídos

O sistema extrai automaticamente:

- **📊 Dados Numéricos**: Preços, extensões, capacidades, velocidades
- **🏷️ Dados Textuais**: Nomes de projetos, códigos, municípios
- **📅 Datas e Períodos**: Cronogramas, inaugurações
- **🗺️ Dados Geográficos**: Coordenadas, regiões
- **💰 Dados Financeiros**: Investimentos, receitas, custos
- **🚊 Dados Técnicos**: Bitola, estações, composições

## 🔧 Configuração

### Requisitos
- Python 3.8+
- pandas, openpyxl, pdfplumber
- Docker (para API)

### Instalação
```bash
pip install pandas openpyxl pdfplumber tqdm
```

## 📈 Resultados

O sistema produz dados estruturados em formato JSON com:
- Valores extraídos com níveis de confiança
- Contexto e rastreabilidade
- Validação automática
- Conversão para Excel

## 🎯 Especialização em Prompts

O arquivo `prompt_extracao_maxima.py` contém prompts especializados para:
- **Ferroviário**: Tarifas, demanda, estações, bitola
- **Financeiro**: Investimentos, receitas, indicadores  
- **Geográfico**: Coordenadas, distâncias, regiões

Use com qualquer LLM (OpenAI, Anthropic, Ollama) para máxima extração!

---

**🚀 Resultado**: Sistema completo e limpo para extração máxima de dados tabulares de documentos ferroviários!
