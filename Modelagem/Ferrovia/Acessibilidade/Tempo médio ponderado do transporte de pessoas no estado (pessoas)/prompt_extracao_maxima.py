"""
🚀 PROMPT PARA EXTRAÇÃO MÁXIMA DE DADOS TABULARES

Este módulo contém prompts especializados para extração máxima de informações
de textos e conversão em dados tabulares estruturados.

Uso:
    from prompt_extracao_maxima import PromptExtracao
    
    extrator = PromptExtracao()
    prompt = extrator.gerar_prompt_principal(texto)
    # Enviar prompt para LLM
    resultado = llm.completar(prompt)
"""

import json
from typing import Dict, List, Any, Optional

class PromptExtracao:
    """
    Classe para gerar prompts especializados em extração máxima de dados
    """
    
    def __init__(self):
        self.prompt_base = self._definir_prompt_base()
        self.contextos_especializados = self._definir_contextos()
        
    def _definir_prompt_base(self) -> str:
        """Define o prompt principal para extração máxima"""
        return """
Você é um especialista em extração de dados estruturados e tabulares. Sua missão é extrair TODAS as informações possíveis de uma string de texto e organizá-las em formato tabular/estruturado.

INSTRUÇÕES CRÍTICAS:
1. Extraia TUDO que parecer ser um dado, valor, métrica ou informação quantificável
2. Organize os dados em categorias lógicas 
3. Capture tanto dados explícitos quanto implícitos
4. Identifique padrões, relacionamentos e hierarquias
5. Preserve contexto e metadados
6. Seja extremamente detalhista e exaustivo

TEXTO PARA ANÁLISE:
{texto}

FORMATO DE SAÍDA ESPERADO:
Retorne um JSON estruturado com as seguintes seções:

{{
  "dados_identificados": {{
    "valores_numericos": [
      {{
        "valor": "123.45",
        "unidade": "R$",
        "contexto": "preço da passagem",
        "confianca": 0.95,
        "posicao_texto": "linha 15"
      }}
    ],
    "valores_textuais": [
      {{
        "campo": "nome_projeto",
        "valor": "Linha Férrea XYZ",
        "contexto": "identificação do empreendimento",
        "confianca": 0.90
      }}
    ],
    "datas_temporais": [
      {{
        "data": "2024-01-15",
        "formato_original": "15/01/2024",
        "contexto": "data de inauguração",
        "confianca": 0.85
      }}
    ],
    "coordenadas_geograficas": [
      {{
        "latitude": -19.5555,
        "longitude": -43.7777,
        "local": "Estação Central",
        "contexto": "localização da estação"
      }}
    ]
  }},
  "estruturas_detectadas": {{
    "tabelas": [
      {{
        "cabecalho": ["Coluna1", "Coluna2", "Coluna3"],
        "linhas": [
          ["valor1", "valor2", "valor3"],
          ["valor4", "valor5", "valor6"]
        ],
        "contexto": "tabela de tarifas",
        "confianca": 0.92
      }}
    ],
    "listas": [
      {{
        "tipo": "municipios_atendidos",
        "itens": ["Belo Horizonte", "Contagem", "Betim"],
        "contexto": "cidades servidas pela linha",
        "confianca": 0.88
      }}
    ],
    "hierarquias": [
      {{
        "nivel1": "Transporte Ferroviário",
        "nivel2": "Passageiros",
        "nivel3": "Linha Metropolitana",
        "contexto": "classificação do serviço"
      }}
    ]
  }},
  "padroes_identificados": {{
    "codigos": [
      {{
        "codigo": "FER-001",
        "tipo": "projeto",
        "contexto": "identificação do projeto ferroviário",
        "confianca": 0.90
      }}
    ],
    "formulas": [
      {{
        "formula": "Receita = Passageiros × Tarifa",
        "variaveis": ["Receita", "Passageiros", "Tarifa"],
        "contexto": "cálculo de receita",
        "confianca": 0.75
      }}
    ],
    "relacoes": [
      {{
        "origem": "demanda_passageiros",
        "destino": "receita_anual",
        "tipo": "correlacao_positiva",
        "contexto": "mais passageiros geram mais receita"
      }}
    ]
  }},
  "metadados_contextuais": {{
    "dominio": "transporte_ferroviario",
    "subdominios": ["passageiros", "tarifas", "operacao"],
    "palavras_chave": ["ferrovia", "passageiros", "estação", "tarifa"],
    "entidades_nomeadas": [
      {{
        "nome": "Estação Central",
        "tipo": "local",
        "contexto": "ponto de parada"
      }}
    ],
    "metricas_qualidade": {{
      "completude": 0.85,
      "precisao": 0.90,
      "consistencia": 0.88
    }}
  }},
  "dados_derivados": {{
    "calculos_possiveis": [
      {{
        "nome": "receita_por_km",
        "formula": "receita_total / extensao_km",
        "disponibilidade": "possivel",
        "valores_necessarios": ["receita_total", "extensao_km"]
      }}
    ],
    "tendencias": [
      {{
        "variavel": "demanda_passageiros",
        "tendencia": "crescente",
        "periodo": "2020-2024",
        "confianca": 0.70
      }}
    ],
    "anomalias": [
      {{
        "campo": "velocidade_operacional",
        "valor": "300 km/h",
        "motivo": "valor muito alto para ferrovia convencional",
        "sugestao": "verificar se é trem de alta velocidade"
      }}
    ]
  }},
  "recomendacoes_melhoria": {{
    "dados_faltantes": [
      "coordenadas_estacoes",
      "horarios_operacao",
      "capacidade_por_composicao"
    ],
    "validacoes_sugeridas": [
      "verificar consistência de unidades",
      "validar datas cronologicamente",
      "confirmar valores monetários"
    ],
    "expansoes_possiveis": [
      "buscar dados complementares em outras fontes",
      "calcular indicadores de performance",
      "criar series temporais"
    ]
  }}
}}

REGRAS DE EXTRAÇÃO:
1. Seja EXTREMAMENTE detalhista
2. Capture até informações aparentemente irrelevantes
3. Identifique padrões sutis no texto
4. Preserve SEMPRE o contexto original
5. Atribua níveis de confiança realistas
6. Sugira relacionamentos entre dados
7. Identifique possíveis erros ou inconsistências
8. Proponha dados derivados calculáveis
9. Mantenha rastreabilidade (posição no texto)
10. Classifique dados por domínio/categoria

ATENÇÃO ESPECIAL PARA:
- Números com unidades (R$, km, km/h, passageiros, etc.)
- Códigos alfanuméricos (FER-001, etc.)
- Nomes próprios (cidades, estações, projetos)
- Datas em qualquer formato
- Coordenadas geográficas
- Percentuais e proporções
- Intervalos e ranges (10-15 min)
- Dados técnicos (bitola, capacidade, etc.)
- Informações operacionais (horários, frequência)
- Dados financeiros (investimentos, receitas, custos)

SEJA IMPLACÁVEL NA EXTRAÇÃO - NADA DEVE PASSAR DESPERCEBIDO!
"""

    def _definir_contextos(self) -> Dict[str, str]:
        """Define contextos especializados para diferentes domínios"""
        return {
            "ferroviario": """
CONTEXTO: Dados de transporte ferroviário de passageiros
FOCO ESPECIAL EM: tarifas, demanda, estações, extensão, bitola, velocidade, capacidade, receitas, investimentos, municípios atendidos, tempos de viagem, frequência de serviço

CAMPOS PRIORITÁRIOS:
- Preços e tarifas (R$)
- Demanda de passageiros (passageiros/dia, mês, ano)
- Extensão da linha (km)
- Número de estações
- Tipo de bitola (métrica, larga, estreita)
- Velocidade operacional (km/h)
- Capacidade dos trens (passageiros)
- Receitas (anual, por km)
- Investimentos totais
- Municípios/cidades atendidas
- Tempos de viagem (ida e volta)
- Frequência de serviço (trens/dia)
- Códigos de projeto (FER-XXX)
""",
            "financeiro": """
CONTEXTO: Dados financeiros e econômicos
FOCO ESPECIAL EM: valores monetários, percentuais, indicadores, custos, receitas, investimentos, retorno, viabilidade

CAMPOS PRIORITÁRIOS:
- Valores em moeda (R$, USD, EUR)
- Percentuais e taxas (%, p.a.)
- Indicadores financeiros (ROI, VPL, TIR)
- Custos operacionais
- Receitas e faturamento
- Investimentos (CAPEX, OPEX)
- Fluxos de caixa
- Prazos e períodos
- Inflação e correção monetária
""",
            "geografico": """
CONTEXTO: Dados geográficos e territoriais
FOCO ESPECIAL EM: coordenadas, distâncias, áreas, municípios, regiões, rotas, altitudes

CAMPOS PRIORITÁRIOS:
- Coordenadas (latitude, longitude)
- Distâncias (km, metros)
- Áreas (km², hectares)
- Municípios e estados
- Regiões geográficas
- Rotas e trajetos
- Altitudes e elevações
- Limites territoriais
- Pontos de referência
"""
        }
    
    def gerar_prompt_principal(self, texto: str) -> str:
        """
        Gera o prompt principal para extração máxima
        
        Args:
            texto: Texto a ser analisado
            
        Returns:
            Prompt formatado pronto para uso
        """
        return self.prompt_base.format(texto=texto)
    
    def gerar_prompt_contextualizado(self, texto: str, contexto: str = "ferroviario") -> str:
        """
        Gera prompt com contexto específico
        
        Args:
            texto: Texto a ser analisado
            contexto: Tipo de contexto ('ferroviario', 'financeiro', 'geografico')
            
        Returns:
            Prompt contextualizado pronto para uso
        """
        prompt_base = self.gerar_prompt_principal(texto)
        
        if contexto in self.contextos_especializados:
            contexto_especifico = self.contextos_especializados[contexto]
            prompt_contextualizado = f"{contexto_especifico}\n\n{prompt_base}"
            return prompt_contextualizado
        
        return prompt_base
    
    def extrair_dados_maximos(self, texto: str, contexto: str = "ferroviario") -> Dict[str, Any]:
        """
        Método exemplo para integração com LLM
        
        Args:
            texto: Texto a ser analisado
            contexto: Contexto específico
            
        Returns:
            Dicionário com dados estruturados (simulado)
        """
        prompt = self.gerar_prompt_contextualizado(texto, contexto)
        
        # AQUI VOCÊ INTEGRARIA COM SEU LLM PREFERIDO
        # resultado = llm.completar(prompt)
        # return json.loads(resultado)
        
        # Exemplo de estrutura de retorno
        return {
            "prompt_usado": prompt,
            "status": "pronto_para_llm",
            "instrucoes": "Envie o prompt para seu LLM e processe o resultado JSON"
        }
    
    def validar_resultado(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e melhora o resultado da extração
        
        Args:
            resultado: Resultado da extração do LLM
            
        Returns:
            Resultado validado e melhorado
        """
        metricas = {
            "completude": 0.0,
            "precisao": 0.0,
            "consistencia": 0.0,
            "validacoes": []
        }
        
        # Validações básicas
        if "dados_identificados" in resultado:
            metricas["completude"] += 0.3
        if "estruturas_detectadas" in resultado:
            metricas["completude"] += 0.3
        if "padroes_identificados" in resultado:
            metricas["completude"] += 0.2
        if "metadados_contextuais" in resultado:
            metricas["completude"] += 0.2
        
        # Adicionar métricas ao resultado
        resultado["metricas_qualidade"] = metricas
        
        return resultado

# Exemplo de uso
def exemplo_uso():
    """Demonstra como usar o prompt de extração máxima"""
    
    extrator = PromptExtracao()
    
    # Texto exemplo
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
    
    # Gerar prompt
    prompt = extrator.gerar_prompt_contextualizado(texto_exemplo, "ferroviario")
    
    print("🚀 PROMPT GERADO:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    print("\n📋 INSTRUÇÕES:")
    print("1. Copie o prompt acima")
    print("2. Envie para seu LLM preferido (GPT, Claude, etc.)")
    print("3. Processe o resultado JSON")
    print("4. Use extrator.validar_resultado() para validar")
    
    return prompt

if __name__ == "__main__":
    exemplo_uso()
