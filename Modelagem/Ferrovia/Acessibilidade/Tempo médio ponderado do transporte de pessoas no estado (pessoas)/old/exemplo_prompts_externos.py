"""
🎯 EXEMPLO PRÁTICO: Prompts Externos + Conversa Direta
Demonstra como definir prompts fora da aplicação e usar via FastAPI Proxy
Para usar: docker exec -it fastapi-proxy python exemplo_prompts_externos.py
"""

from chat_client import ChatClient


class MeusPrompts:
    """Classe com prompts personalizados definidos externamente"""
    
    @staticmethod
    def prompt_extracao_ferroviaria(texto: str) -> str:
        """Prompt para extrair dados ferroviários"""
        return f"""
Você é um especialista em análise de dados de transporte ferroviário.

TAREFA: Extrair TODOS os dados quantitativos do texto a seguir.

TEXTO:
{texto}

INSTRUÇÕES:
1. Identifique TODOS os números, valores, medidas
2. Organize por categorias (financeiro, técnico, operacional)
3. Retorne em formato JSON estruturado
4. Inclua unidades de medida
5. Se um dado não existir, use null

FORMATO DE SAÍDA (JSON):
{{
  "dados_tecnicos": {{
    "extensao_km": null,
    "num_estacoes": null,
    "velocidade_max_kmh": null,
    "bitola_metros": null,
    "capacidade_passageiros": null
  }},
  "dados_financeiros": {{
    "investimento_total": null,
    "tarifa_basica": null,
    "receita_anual": null,
    "custo_operacional": null
  }},
  "dados_operacionais": {{
    "demanda_diaria": null,
    "frequencia_servico": null,
    "tempo_viagem_min": null,
    "horario_funcionamento": null
  }},
  "localizacao": {{
    "municipios": [],
    "estados": [],
    "coordenadas": null
  }},
  "cronograma": {{
    "data_inauguracao": null,
    "prazo_construcao": null,
    "fase_projeto": null
  }}
}}

IMPORTANTE: Responda APENAS com o JSON, sem explicações adicionais.
"""

    @staticmethod
    def prompt_analise_viabilidade(dados_json: str) -> str:
        """Prompt para análise de viabilidade"""
        return f"""
Você é um consultor especialista em viabilidade de projetos ferroviários.

DADOS DO PROJETO (JSON):
{dados_json}

TAREFA: Realizar análise de viabilidade completa.

ANÁLISE SOLICITADA:
1. **Viabilidade Técnica**: Avalie aspectos técnicos (extensão, capacidade, velocidade)
2. **Viabilidade Financeira**: Calcule indicadores (payback, ROI estimado, receita/km)
3. **Viabilidade Operacional**: Analise demanda vs capacidade, frequência
4. **Riscos Identificados**: Liste principais riscos e mitigações
5. **Recomendações**: Próximos passos e melhorias sugeridas

FORMATO DE RESPOSTA:
Para cada categoria, dê uma nota de 1-10 e justificativa de 2-3 linhas.

CÁLCULOS SOLICITADOS:
- Se houver receita anual e investimento: calcule payback simples
- Se houver demanda e tarifa: estime receita potencial
- Se houver extensão e investimento: calcule custo por km

Seja objetivo e técnico nas análises.
"""

    @staticmethod
    def prompt_comparacao_projetos(projeto1: str, projeto2: str) -> str:
        """Prompt para comparar dois projetos"""
        return f"""
Você é um analista de projetos de transporte ferroviário.

PROJETO A:
{projeto1}

PROJETO B:
{projeto2}

TAREFA: Compare os dois projetos em uma tabela estruturada.

CRITÉRIOS DE COMPARAÇÃO:
1. Extensão (km)
2. Investimento total
3. Custo por km
4. Capacidade de passageiros
5. Receita anual estimada
6. Payback simples
7. Impacto social (municípios atendidos)
8. Complexidade técnica

FORMATO DE SAÍDA:
| Critério | Projeto A | Projeto B | Vencedor | Justificativa |
|----------|-----------|-----------|----------|---------------|
| ... | ... | ... | ... | ... |

Ao final, recomende qual projeto tem melhor custo-benefício e por quê.
"""

    @staticmethod
    def prompt_relatorio_executivo(dados: str) -> str:
        """Prompt para gerar relatório executivo"""
        return f"""
Você é um diretor de planejamento de transporte. Crie um relatório executivo conciso.

DADOS DO PROJETO:
{dados}

ESTRUTURA DO RELATÓRIO:

# SUMÁRIO EXECUTIVO
## Dados Principais
- [Liste os 5 dados mais importantes em bullets]

## Viabilidade Geral
- [Avaliação em uma frase]

## Investimento e Retorno
- [Valores principais e payback]

## Recomendação
- [APROVADO / APROVADO COM RESSALVAS / REJEITADO]
- [Justificativa em 2 linhas]

## Próximos Passos
- [3 ações prioritárias]

LIMITE: Máximo 200 palavras. Seja direto e executivo.
"""


def demonstracao_prompts_externos():
    """Demonstra uso de prompts definidos externamente"""
    print("🎯 DEMONSTRAÇÃO: Prompts Externos + Conversa Direta")
    print("=" * 60)
    
    # Inicializar cliente
    client = ChatClient()
    
    # Verificar status
    status = client.verificar_status()
    if status["status"] != "disponivel":
        print("❌ Sistema não disponível. Execute 'start_simple.ps1' primeiro.")
        return
    
    # Pegar modelo disponível
    modelos = client.listar_modelos()
    if not modelos:
        print("❌ Nenhum modelo disponível.")
        return
    
    modelo = modelos[0]
    print(f"🤖 Usando modelo: {modelo}")
    
    # Dados de exemplo
    texto_exemplo = """
    Projeto FER-025 - Linha Express São Paulo-Campinas
    
    DADOS TÉCNICOS:
    - Extensão total: 118,5 km
    - Bitola: Larga (1,60m)
    - Estações: 8 paradas principais
    - Velocidade máxima: 160 km/h
    - Velocidade comercial: 120 km/h
    - Capacidade: 2.400 passageiros por composição
    
    DADOS FINANCEIROS:
    - Investimento total: R$ 12,8 bilhões
    - Tarifa básica: R$ 15,90
    - Tarifa expressa: R$ 22,50
    - Receita anual estimada: R$ 892 milhões
    - Custo operacional anual: R$ 245 milhões
    
    OPERAÇÃO:
    - Demanda projetada: 95.000 passageiros/dia
    - Frequência: 15 minutos (pico), 30 minutos (normal)
    - Tempo de viagem: 42 minutos
    - Funcionamento: 5h às 24h
    
    LOCALIZAÇÃO:
    - Municípios: São Paulo, Osasco, Barueri, Jundiaí, Campinas
    - Estados: São Paulo
    - Data prevista de inauguração: Dezembro/2027
    """
    
    # Teste 1: Extração de dados
    print("\n📊 TESTE 1: Extração de dados estruturados")
    print("-" * 50)
    
    prompt_extracao = MeusPrompts.prompt_extracao_ferroviaria(texto_exemplo)
    
    resultado_extracao = client.conversar(
        prompt=prompt_extracao,
        modelo=modelo,
        temperature=0.1  # Baixa criatividade para extração precisa
    )
    
    if resultado_extracao["sucesso"]:
        print("✅ Dados extraídos com sucesso!")
        dados_json = resultado_extracao["resposta"]
        print(f"📋 JSON extraído:\n{dados_json}")
        
        # Teste 2: Análise de viabilidade
        print("\n📈 TESTE 2: Análise de viabilidade")
        print("-" * 50)
        
        prompt_viabilidade = MeusPrompts.prompt_analise_viabilidade(dados_json)
        
        resultado_viabilidade = client.conversar(
            prompt=prompt_viabilidade,
            modelo=modelo,
            temperature=0.3  # Moderada criatividade para análise
        )
        
        if resultado_viabilidade["sucesso"]:
            print("✅ Análise de viabilidade:")
            print(resultado_viabilidade["resposta"])
        
        # Teste 3: Relatório executivo
        print("\n📄 TESTE 3: Relatório executivo")
        print("-" * 50)
        
        prompt_relatorio = MeusPrompts.prompt_relatorio_executivo(texto_exemplo)
        
        resultado_relatorio = client.conversar(
            prompt=prompt_relatorio,
            modelo=modelo,
            temperature=0.2  # Baixa criatividade para relatório formal
        )
        
        if resultado_relatorio["sucesso"]:
            print("✅ Relatório executivo:")
            print(resultado_relatorio["resposta"])
    
    else:
        print(f"❌ Erro na extração: {resultado_extracao['erro']}")


def exemplo_conversa_interativa():
    """Exemplo de conversa interativa"""
    print("\n💬 EXEMPLO: Conversa Interativa")
    print("=" * 40)
    
    client = ChatClient()
    modelos = client.listar_modelos()
    
    if modelos:
        modelo = modelos[0]
        print(f"🤖 Conversando com: {modelo}")
        
        perguntas = [
            "Quais são os principais benefícios do transporte ferroviário?",
            "Como calcular a viabilidade financeira de um projeto ferroviário?",
            "Quais fatores influenciam a demanda de passageiros em trens urbanos?"
        ]
        
        for i, pergunta in enumerate(perguntas, 1):
            print(f"\n❓ Pergunta {i}: {pergunta}")
            
            resposta = client.conversar_simples(pergunta, modelo)
            print(f"🤖 Resposta: {resposta[:200]}...")


def exemplo_diferentes_temperaturas():
    """Exemplo mostrando diferentes configurações de temperatura"""
    print("\n🌡️ EXEMPLO: Diferentes Temperaturas")
    print("=" * 40)
    
    client = ChatClient()
    modelos = client.listar_modelos()
    
    if modelos:
        modelo = modelos[0]
        prompt_base = "Descreva em uma frase os benefícios do transporte ferroviário."
        
        temperaturas = [0.1, 0.5, 0.9]
        
        for temp in temperaturas:
            print(f"\n🌡️ Temperatura {temp}:")
            resultado = client.conversar(
                prompt=prompt_base,
                modelo=modelo,
                temperature=temp
            )
            
            if resultado["sucesso"]:
                print(f"📝 {resultado['resposta']}")


if __name__ == "__main__":
    print("🚀 SISTEMA DE PROMPTS EXTERNOS + CONVERSA DIRETA")
    print("=" * 70)
    print("💡 Ideia: Prompts definidos fora da aplicação, FastAPI só transita")
    print("🎯 Vantagem: Controle total sobre prompts + flexibilidade máxima")
    print("=" * 70)
    
    demonstracao_prompts_externos()
    exemplo_conversa_interativa()
    exemplo_diferentes_temperaturas()
    
    print("\n✨ DEMONSTRAÇÃO CONCLUÍDA!")
    print("💡 Agora você pode criar seus próprios prompts e usar via FastAPI proxy!")
