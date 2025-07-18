"""
🎯 EXEMPLO PRÁTICO - Como usar o Prompt de Extração Máxima

Este arquivo demonstra como usar o prompt de extração máxima com diferentes LLMs
e como processar os resultados para obter dados tabulares estruturados.
"""

from prompt_extracao_maxima import PromptExtracao
import json

def exemplo_com_openai():
    """
    Exemplo de uso com OpenAI GPT
    """
    print("🔥 EXEMPLO COM OPENAI GPT")
    print("=" * 50)
    
    # Texto de exemplo real
    texto_ferroviario = """
    FER-002 - VLT Região Metropolitana de Belo Horizonte
    
    CARACTERÍSTICAS TÉCNICAS:
    - Extensão total: 28,1 km
    - Bitola: Métrica (1.000 mm)
    - Estações: 19 estações
    - Velocidade comercial: 25 km/h
    - Velocidade máxima: 70 km/h
    - Capacidade por trem: 408 passageiros
    - Frequência: 6 minutos no pico
    
    DADOS OPERACIONAIS:
    - Demanda projetada: 160.000 passageiros/dia útil
    - Tempo de viagem: 42 minutos (terminal a terminal)
    - Horário de funcionamento: 05h00 às 00h00
    - Frota: 20 trens
    
    DADOS FINANCEIROS:
    - Tarifa proposta: R$ 3,80
    - Investimento total: R$ 1,17 bilhão
    - Receita anual estimada: R$ 180 milhões
    - Custo operacional: R$ 120 milhões/ano
    
    MUNICÍPIOS ATENDIDOS:
    Belo Horizonte, Contagem, Betim
    
    COORDENADAS PRINCIPAIS:
    Estação Central BH: -19.9167, -43.9345
    Terminal Betim: -19.9700, -44.1900
    """
    
    # Criar extrator
    extrator = PromptExtracao()
    
    # Gerar prompt
    prompt = extrator.gerar_prompt_contextualizado(texto_ferroviario, "ferroviario")
    
    print("📝 PROMPT GERADO:")
    print(prompt[:500] + "...")
    
    print("\n🚀 CÓDIGO PARA USAR COM OPENAI:")
    print("""
    import openai
    
    # Configurar cliente OpenAI
    client = openai.OpenAI(api_key="sua_api_key")
    
    # Enviar prompt
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um especialista em extração de dados."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    
    # Processar resultado
    resultado_texto = response.choices[0].message.content
    dados_extraidos = json.loads(resultado_texto)
    
    # Validar resultado
    dados_validados = extrator.validar_resultado(dados_extraidos)
    """)

def exemplo_com_anthropic():
    """
    Exemplo de uso com Anthropic Claude
    """
    print("\n🔥 EXEMPLO COM ANTHROPIC CLAUDE")
    print("=" * 50)
    
    print("🚀 CÓDIGO PARA USAR COM CLAUDE:")
    print("""
    import anthropic
    
    # Configurar cliente Anthropic
    client = anthropic.Anthropic(api_key="sua_api_key")
    
    # Enviar prompt
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Processar resultado
    resultado_texto = response.content[0].text
    dados_extraidos = json.loads(resultado_texto)
    
    # Validar resultado
    dados_validados = extrator.validar_resultado(dados_extraidos)
    """)

def exemplo_com_ollama_local():
    """
    Exemplo de uso com Ollama local
    """
    print("\n🔥 EXEMPLO COM OLLAMA LOCAL")
    print("=" * 50)
    
    print("🚀 CÓDIGO PARA USAR COM OLLAMA:")
    print("""
    import requests
    
    # Preparar requisição
    ollama_request = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    # Enviar para Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=ollama_request
    )
    
    # Processar resultado
    ollama_response = response.json()
    resultado_texto = ollama_response["response"]
    
    # Extrair JSON da resposta
    json_start = resultado_texto.find('{')
    json_end = resultado_texto.rfind('}') + 1
    json_str = resultado_texto[json_start:json_end]
    dados_extraidos = json.loads(json_str)
    
    # Validar resultado
    dados_validados = extrator.validar_resultado(dados_extraidos)
    """)

def exemplo_resultado_esperado():
    """
    Mostra um exemplo do resultado esperado
    """
    print("\n🎯 EXEMPLO DE RESULTADO ESPERADO")
    print("=" * 50)
    
    resultado_exemplo = {
        "dados_identificados": {
            "valores_numericos": [
                {
                    "valor": "28.1",
                    "unidade": "km",
                    "contexto": "extensão total da linha",
                    "confianca": 0.95,
                    "posicao_texto": "linha 5"
                },
                {
                    "valor": "408",
                    "unidade": "passageiros",
                    "contexto": "capacidade por trem",
                    "confianca": 0.92,
                    "posicao_texto": "linha 9"
                },
                {
                    "valor": "3.80",
                    "unidade": "R$",
                    "contexto": "tarifa proposta",
                    "confianca": 0.94,
                    "posicao_texto": "linha 19"
                }
            ],
            "valores_textuais": [
                {
                    "campo": "codigo_projeto",
                    "valor": "FER-002",
                    "contexto": "identificação do projeto",
                    "confianca": 0.98
                },
                {
                    "campo": "nome_projeto",
                    "valor": "VLT Região Metropolitana de Belo Horizonte",
                    "contexto": "nome completo do empreendimento",
                    "confianca": 0.95
                }
            ]
        },
        "estruturas_detectadas": {
            "listas": [
                {
                    "tipo": "municipios_atendidos",
                    "itens": ["Belo Horizonte", "Contagem", "Betim"],
                    "contexto": "cidades servidas pela linha",
                    "confianca": 0.90
                }
            ]
        },
        "padroes_identificados": {
            "codigos": [
                {
                    "codigo": "FER-002",
                    "tipo": "projeto_ferroviario",
                    "contexto": "identificação oficial do projeto",
                    "confianca": 0.98
                }
            ]
        }
    }
    
    print("📊 RESULTADO EM JSON:")
    print(json.dumps(resultado_exemplo, indent=2, ensure_ascii=False))

def exemplo_conversao_para_excel():
    """
    Mostra como converter os dados extraídos para Excel
    """
    print("\n📈 CONVERTENDO PARA EXCEL")
    print("=" * 50)
    
    print("🚀 CÓDIGO PARA CONVERTER PARA EXCEL:")
    print("""
    import pandas as pd
    
    def converter_para_excel(dados_extraidos, arquivo_saida):
        # Extrair valores numéricos
        valores_num = dados_extraidos.get('dados_identificados', {}).get('valores_numericos', [])
        df_numerico = pd.DataFrame(valores_num)
        
        # Extrair valores textuais
        valores_txt = dados_extraidos.get('dados_identificados', {}).get('valores_textuais', [])
        df_textual = pd.DataFrame(valores_txt)
        
        # Salvar em Excel com múltiplas abas
        with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
            df_numerico.to_excel(writer, sheet_name='Dados_Numericos', index=False)
            df_textual.to_excel(writer, sheet_name='Dados_Textuais', index=False)
            
            # Adicionar aba de resumo
            resumo = {
                'Campo': ['Total_Valores_Numericos', 'Total_Valores_Textuais', 'Confianca_Media'],
                'Valor': [len(valores_num), len(valores_txt), 
                         sum(v.get('confianca', 0) for v in valores_num + valores_txt) / 
                         max(1, len(valores_num + valores_txt))]
            }
            pd.DataFrame(resumo).to_excel(writer, sheet_name='Resumo', index=False)
    
    # Usar a função
    converter_para_excel(dados_validados, 'dados_extraidos.xlsx')
    """)

def main():
    """
    Executa todos os exemplos
    """
    print("🚀 GUIA COMPLETO - PROMPT DE EXTRAÇÃO MÁXIMA")
    print("=" * 60)
    
    # Executar exemplos
    exemplo_com_openai()
    exemplo_com_anthropic()
    exemplo_com_ollama_local()
    exemplo_resultado_esperado()
    exemplo_conversao_para_excel()
    
    print("\n✅ PRÓXIMOS PASSOS:")
    print("1. Escolha seu LLM preferido (OpenAI, Anthropic, Ollama)")
    print("2. Configure as credenciais necessárias")
    print("3. Execute o código correspondente")
    print("4. Processe e valide os resultados")
    print("5. Converta para Excel ou formato desejado")
    
    print("\n🎯 DICAS IMPORTANTES:")
    print("- Teste com textos pequenos primeiro")
    print("- Ajuste a temperatura do modelo (0.1 para mais precisão)")
    print("- Valide sempre os resultados")
    print("- Use o contexto adequado para seu domínio")

if __name__ == "__main__":
    main()
