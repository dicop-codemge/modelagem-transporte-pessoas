"""
🚀 IMPLEMENTAÇÃO PRÁTICA DO PROMPT DE EXTRAÇÃO MÁXIMA
Exemplo de como usar o prompt para extrair dados tabulares de strings
"""

import json
import re
from typing import Dict, List, Any, Optional


class ExtracaoMaximaProcessor:
    """
    Processador para extração máxima de dados tabulares usando prompts especializados
    """
    
    def __init__(self):
        self.prompt_base = self._carregar_prompt_base()
        self.padroes_regex = self._definir_padroes_regex()
        self.dominios_especificos = self._definir_dominios()
    
    def _carregar_prompt_base(self) -> str:
        """Carrega o prompt base para extração máxima"""
        return """
        Você é um especialista em extração de dados estruturados e tabulares. 
        Sua missão é extrair TODAS as informações possíveis de uma string de texto 
        e organizá-las em formato tabular/estruturado.

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
        Retorne um JSON estruturado com dados organizados por categorias.
        
        SEJA IMPLACÁVEL NA EXTRAÇÃO - NADA DEVE PASSAR DESPERCEBIDO!
        """
    
    def _definir_padroes_regex(self) -> Dict[str, str]:
        """Define padrões regex para diferentes tipos de dados"""
        return {
            # Valores monetários
            'valores_monetarios': r'R\$\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)',
            
            # Números com unidades
            'numeros_com_unidades': r'(\d+(?:[.,]\d+)?)\s*(km|kg|m|min|h|passageiros?|anos?|meses?|dias?)',
            
            # Códigos alfanuméricos
            'codigos': r'([A-Z]{2,5}[-_]?\d{2,5})',
            
            # Percentuais
            'percentuais': r'(\d+(?:[.,]\d+)?)\s*%',
            
            # Datas
            'datas': r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
            
            # Coordenadas
            'coordenadas': r'(-?\d+(?:[.,]\d+)?)\s*[°º]?\s*(-?\d+(?:[.,]\d+)?)\s*[°º]?',
            
            # Nomes próprios (cidades, projetos)
            'nomes_proprios': r'([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛ][a-záàâãéèêíìîóòôõúùû\s]+(?:-[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛ][a-záàâãéèêíìîóòôõúùû\s]*)?)',
            
            # Intervalos/ranges
            'intervalos': r'(\d+(?:[.,]\d+)?)\s*(?:a|até|-)?\s*(\d+(?:[.,]\d+)?)',
            
            # Horários
            'horarios': r'(\d{1,2}):(\d{2})\s*(?:h|hs|horas?)?',
            
            # Extensões/distâncias
            'extensoes': r'(\d+(?:[.,]\d+)?)\s*(?:km|quilômetros?|metros?|m)\b',
            
            # Capacidades
            'capacidades': r'(\d+(?:[.,]\d+)?)\s*(?:passageiros?|pessoas?|lugares?|assentos?)',
            
            # Frequências
            'frequencias': r'(\d+(?:[.,]\d+)?)\s*(?:por|\/)\s*(?:dia|hora|mês|ano)',
            
            # Velocidades
            'velocidades': r'(\d+(?:[.,]\d+)?)\s*(?:km\/h|kmh|km\s*por\s*hora)'
        }
    
    def _definir_dominios(self) -> Dict[str, List[str]]:
        """Define domínios específicos e suas palavras-chave"""
        return {
            'ferroviario': [
                'ferrovia', 'trem', 'estação', 'linha', 'bitola', 'trilho',
                'composição', 'vagão', 'locomotiva', 'passageiro', 'tarifa',
                'metro', 'metrô', 'VLT', 'monotrilho'
            ],
            'financeiro': [
                'receita', 'custo', 'investimento', 'orçamento', 'valor',
                'tarifa', 'preço', 'lucro', 'prejuízo', 'ROI', 'VPL', 'TIR'
            ],
            'geografico': [
                'município', 'cidade', 'estado', 'região', 'distrito',
                'bairro', 'local', 'endereço', 'coordenada', 'latitude', 'longitude'
            ],
            'operacional': [
                'horário', 'frequência', 'capacidade', 'velocidade', 'tempo',
                'duração', 'operação', 'funcionamento', 'manutenção', 'serviço'
            ],
            'tecnico': [
                'extensão', 'comprimento', 'largura', 'altura', 'peso',
                'potência', 'voltagem', 'corrente', 'material', 'especificação'
            ]
        }
    
    def extrair_dados_maximos(self, texto: str, dominio: str = 'geral') -> Dict[str, Any]:
        """
        Extrai dados máximos de uma string usando prompt especializado
        """
        # 1. Análise preliminar
        analise_preliminar = self._analisar_texto_preliminar(texto)
        
        # 2. Aplicar padrões regex
        dados_regex = self._aplicar_padroes_regex(texto)
        
        # 3. Identificar domínio específico
        dominio_detectado = self._detectar_dominio(texto)
        
        # 4. Extrair dados contextuais
        dados_contextuais = self._extrair_contexto(texto, dominio_detectado)
        
        # 5. Organizar dados estruturados
        dados_estruturados = self._organizar_dados_estruturados(
            texto, analise_preliminar, dados_regex, dados_contextuais
        )
        
        # 6. Calcular métricas de qualidade
        metricas = self._calcular_metricas_qualidade(dados_estruturados, texto)
        
        # 7. Sugerir melhorias
        sugestoes = self._sugerir_melhorias(dados_estruturados, texto)
        
        return {
            'analise_preliminar': analise_preliminar,
            'dados_extraidos': dados_estruturados,
            'metricas_qualidade': metricas,
            'sugestoes_melhoria': sugestoes,
            'dominio_detectado': dominio_detectado,
            'texto_original': texto[:500] + '...' if len(texto) > 500 else texto
        }
    
    def _analisar_texto_preliminar(self, texto: str) -> Dict[str, Any]:
        """Análise preliminar do texto"""
        linhas = texto.split('\n')
        palavras = texto.split()
        
        return {
            'total_caracteres': len(texto),
            'total_linhas': len(linhas),
            'total_palavras': len(palavras),
            'linhas_com_dois_pontos': len([l for l in linhas if ':' in l]),
            'linhas_com_numeros': len([l for l in linhas if re.search(r'\d', l)]),
            'densidade_numerica': len(re.findall(r'\d+', texto)) / len(palavras) if palavras else 0,
            'possui_estrutura_tabular': self._detectar_estrutura_tabular(texto),
            'idioma_detectado': 'português'  # Simplificado
        }
    
    def _aplicar_padroes_regex(self, texto: str) -> Dict[str, List[Dict[str, Any]]]:
        """Aplica todos os padrões regex definidos"""
        resultados = {}
        
        for nome_padrao, padrao in self.padroes_regex.items():
            matches = re.finditer(padrao, texto, re.IGNORECASE)
            dados_padrao = []
            
            for match in matches:
                dados_padrao.append({
                    'valor': match.group(0),
                    'grupos': match.groups(),
                    'posicao_inicio': match.start(),
                    'posicao_fim': match.end(),
                    'contexto': self._extrair_contexto_local(texto, match.start(), match.end()),
                    'confianca': self._calcular_confianca_regex(match, nome_padrao)
                })
            
            if dados_padrao:
                resultados[nome_padrao] = dados_padrao
        
        return resultados
    
    def _detectar_dominio(self, texto: str) -> str:
        """Detecta o domínio principal do texto"""
        texto_lower = texto.lower()
        pontuacoes_dominio = {}
        
        for dominio, palavras_chave in self.dominios_especificos.items():
            pontuacao = sum(1 for palavra in palavras_chave if palavra in texto_lower)
            pontuacoes_dominio[dominio] = pontuacao
        
        if pontuacoes_dominio:
            return max(pontuacoes_dominio, key=pontuacoes_dominio.get)
        
        return 'geral'
    
    def _extrair_contexto(self, texto: str, dominio: str) -> Dict[str, Any]:
        """Extrai contexto específico baseado no domínio"""
        contexto = {
            'palavras_chave_encontradas': [],
            'entidades_nomeadas': [],
            'relacoes_identificadas': [],
            'hierarquias_detectadas': []
        }
        
        # Identificar palavras-chave do domínio
        if dominio in self.dominios_especificos:
            palavras_dominio = self.dominios_especificos[dominio]
            for palavra in palavras_dominio:
                if palavra.lower() in texto.lower():
                    contexto['palavras_chave_encontradas'].append(palavra)
        
        # Identificar entidades nomeadas (simplificado)
        nomes_proprios = re.findall(r'[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛ][a-záàâãéèêíìîóòôõúùû\s]+', texto)
        contexto['entidades_nomeadas'] = list(set(nomes_proprios[:10]))  # Limitar a 10
        
        # Identificar relações simples (A -> B)
        relacoes = re.findall(r'(\w+)\s*(?:para|até|de|em)\s*(\w+)', texto, re.IGNORECASE)
        contexto['relacoes_identificadas'] = list(set(relacoes[:5]))  # Limitar a 5
        
        return contexto
    
    def _organizar_dados_estruturados(self, texto: str, analise: Dict, regex_dados: Dict, contexto: Dict) -> Dict[str, Any]:
        """Organiza todos os dados em estrutura final"""
        return {
            'valores_numericos': self._consolidar_valores_numericos(regex_dados),
            'valores_textuais': self._consolidar_valores_textuais(regex_dados, contexto),
            'datas_temporais': self._consolidar_datas(regex_dados),
            'dados_geograficos': self._consolidar_dados_geograficos(regex_dados),
            'dados_tecnicos': self._consolidar_dados_tecnicos(regex_dados),
            'dados_operacionais': self._consolidar_dados_operacionais(regex_dados),
            'estruturas_detectadas': self._detectar_estruturas(texto),
            'padroes_identificados': self._identificar_padroes(texto, regex_dados),
            'relacoes_dados': self._identificar_relacoes_dados(regex_dados)
        }
    
    def _consolidar_valores_numericos(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Consolida todos os valores numéricos encontrados"""
        valores = []
        
        # Valores monetários
        if 'valores_monetarios' in regex_dados:
            for item in regex_dados['valores_monetarios']:
                valores.append({
                    'valor': item['grupos'][0],
                    'tipo': 'monetario',
                    'unidade': 'R$',
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        # Números com unidades
        if 'numeros_com_unidades' in regex_dados:
            for item in regex_dados['numeros_com_unidades']:
                valores.append({
                    'valor': item['grupos'][0],
                    'tipo': 'numerico_com_unidade',
                    'unidade': item['grupos'][1],
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        # Percentuais
        if 'percentuais' in regex_dados:
            for item in regex_dados['percentuais']:
                valores.append({
                    'valor': item['grupos'][0],
                    'tipo': 'percentual',
                    'unidade': '%',
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        return valores
    
    def _consolidar_valores_textuais(self, regex_dados: Dict, contexto: Dict) -> List[Dict[str, Any]]:
        """Consolida valores textuais"""
        valores = []
        
        # Códigos
        if 'codigos' in regex_dados:
            for item in regex_dados['codigos']:
                valores.append({
                    'valor': item['grupos'][0],
                    'tipo': 'codigo',
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        # Entidades nomeadas
        for entidade in contexto.get('entidades_nomeadas', []):
            valores.append({
                'valor': entidade,
                'tipo': 'entidade_nomeada',
                'contexto': 'nome_proprio_detectado',
                'confianca': 0.7,
                'posicao': 0
            })
        
        return valores
    
    def _consolidar_datas(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Consolida datas encontradas"""
        datas = []
        
        if 'datas' in regex_dados:
            for item in regex_dados['datas']:
                datas.append({
                    'data_original': item['grupos'][0],
                    'formato_detectado': self._detectar_formato_data(item['grupos'][0]),
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        return datas
    
    def _consolidar_dados_geograficos(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Consolida dados geográficos"""
        geograficos = []
        
        if 'coordenadas' in regex_dados:
            for item in regex_dados['coordenadas']:
                geograficos.append({
                    'latitude': item['grupos'][0],
                    'longitude': item['grupos'][1],
                    'contexto': item['contexto'],
                    'confianca': item['confianca'],
                    'posicao': item['posicao_inicio']
                })
        
        return geograficos
    
    def _consolidar_dados_tecnicos(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Consolida dados técnicos"""
        tecnicos = []
        
        campos_tecnicos = ['extensoes', 'capacidades', 'velocidades']
        
        for campo in campos_tecnicos:
            if campo in regex_dados:
                for item in regex_dados[campo]:
                    tecnicos.append({
                        'tipo': campo,
                        'valor': item['grupos'][0],
                        'contexto': item['contexto'],
                        'confianca': item['confianca'],
                        'posicao': item['posicao_inicio']
                    })
        
        return tecnicos
    
    def _consolidar_dados_operacionais(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Consolida dados operacionais"""
        operacionais = []
        
        campos_operacionais = ['horarios', 'frequencias']
        
        for campo in campos_operacionais:
            if campo in regex_dados:
                for item in regex_dados[campo]:
                    operacionais.append({
                        'tipo': campo,
                        'valor': item['valor'],
                        'contexto': item['contexto'],
                        'confianca': item['confianca'],
                        'posicao': item['posicao_inicio']
                    })
        
        return operacionais
    
    def _detectar_estruturas(self, texto: str) -> Dict[str, Any]:
        """Detecta estruturas de dados (tabelas, listas, etc.)"""
        return {
            'tabelas_detectadas': self._detectar_tabelas(texto),
            'listas_detectadas': self._detectar_listas(texto),
            'hierarquias_detectadas': self._detectar_hierarquias(texto)
        }
    
    def _detectar_tabelas(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta estruturas tabulares"""
        tabelas = []
        
        # Padrão simples: linhas com separadores consistentes
        linhas = texto.split('\n')
        for i, linha in enumerate(linhas):
            if '|' in linha or '\t' in linha:
                # Possível linha de tabela
                separador = '|' if '|' in linha else '\t'
                colunas = [col.strip() for col in linha.split(separador)]
                
                if len(colunas) > 1:
                    tabelas.append({
                        'linha': i,
                        'colunas': colunas,
                        'separador': separador,
                        'confianca': 0.8
                    })
        
        return tabelas
    
    def _detectar_listas(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta listas"""
        listas = []
        
        # Padrão: linhas começando com -, *, números, etc.
        linhas = texto.split('\n')
        lista_atual = []
        
        for linha in linhas:
            linha = linha.strip()
            if re.match(r'^[-*•]\s+', linha) or re.match(r'^\d+[\.)]\s+', linha):
                lista_atual.append(linha)
            elif lista_atual:
                if len(lista_atual) > 1:
                    listas.append({
                        'itens': lista_atual,
                        'tipo': 'lista_marcadores',
                        'confianca': 0.9
                    })
                lista_atual = []
        
        # Adicionar última lista se existir
        if lista_atual and len(lista_atual) > 1:
            listas.append({
                'itens': lista_atual,
                'tipo': 'lista_marcadores',
                'confianca': 0.9
            })
        
        return listas
    
    def _detectar_hierarquias(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta hierarquias (títulos, subtítulos, etc.)"""
        hierarquias = []
        
        linhas = texto.split('\n')
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            
            # Detectar níveis de hierarquia
            if re.match(r'^[A-Z\s]+:?$', linha):  # TÍTULO EM MAIÚSCULAS
                hierarquias.append({
                    'nivel': 1,
                    'texto': linha,
                    'linha': i,
                    'tipo': 'titulo_principal'
                })
            elif re.match(r'^[A-Z][a-z\s]+:?$', linha):  # Título Capitalizado
                hierarquias.append({
                    'nivel': 2,
                    'texto': linha,
                    'linha': i,
                    'tipo': 'subtitulo'
                })
            elif linha.endswith(':'):  # Qualquer coisa com dois pontos
                hierarquias.append({
                    'nivel': 3,
                    'texto': linha,
                    'linha': i,
                    'tipo': 'item_com_detalhes'
                })
        
        return hierarquias
    
    def _identificar_padroes(self, texto: str, regex_dados: Dict) -> Dict[str, Any]:
        """Identifica padrões nos dados"""
        return {
            'codigos_encontrados': len(regex_dados.get('codigos', [])),
            'valores_monetarios_encontrados': len(regex_dados.get('valores_monetarios', [])),
            'datas_encontradas': len(regex_dados.get('datas', [])),
            'coordenadas_encontradas': len(regex_dados.get('coordenadas', [])),
            'padroes_repetitivos': self._detectar_padroes_repetitivos(texto),
            'sequencias_numericas': self._detectar_sequencias_numericas(texto)
        }
    
    def _identificar_relacoes_dados(self, regex_dados: Dict) -> List[Dict[str, Any]]:
        """Identifica relações entre dados"""
        relacoes = []
        
        # Exemplo: se tem valor monetário e número com unidade "passageiros", pode ser tarifa
        if 'valores_monetarios' in regex_dados and 'numeros_com_unidades' in regex_dados:
            for valor_monetario in regex_dados['valores_monetarios']:
                for numero_unidade in regex_dados['numeros_com_unidades']:
                    if 'passageiro' in numero_unidade['grupos'][1].lower():
                        relacoes.append({
                            'tipo': 'tarifa_por_passageiro',
                            'valor_monetario': valor_monetario['grupos'][0],
                            'quantidade_passageiros': numero_unidade['grupos'][0],
                            'confianca': 0.7
                        })
        
        return relacoes
    
    def _calcular_metricas_qualidade(self, dados: Dict, texto: str) -> Dict[str, float]:
        """Calcula métricas de qualidade da extração"""
        total_dados = sum(len(v) if isinstance(v, list) else 1 for v in dados.values())
        total_caracteres = len(texto)
        
        return {
            'completude_estimada': min(total_dados / (total_caracteres / 100), 1.0),
            'densidade_extração': total_dados / total_caracteres if total_caracteres > 0 else 0,
            'cobertura_numerica': len(dados.get('valores_numericos', [])) / total_dados if total_dados > 0 else 0,
            'cobertura_textual': len(dados.get('valores_textuais', [])) / total_dados if total_dados > 0 else 0,
            'estruturacao': len(dados.get('estruturas_detectadas', {}).get('tabelas_detectadas', [])) / 10,
            'confianca_media': self._calcular_confianca_media(dados)
        }
    
    def _sugerir_melhorias(self, dados: Dict, texto: str) -> Dict[str, List[str]]:
        """Sugere melhorias para maximizar a extração"""
        sugestoes = {
            'pre_processamento': [],
            'padroes_adicionais': [],
            'validacoes': [],
            'expansoes': []
        }
        
        # Sugestões baseadas na análise
        if len(dados.get('valores_numericos', [])) < 5:
            sugestoes['padroes_adicionais'].append('Adicionar padrões para números decimais')
        
        if not dados.get('datas_temporais'):
            sugestoes['padroes_adicionais'].append('Melhorar detecção de datas')
        
        if '\t' in texto:
            sugestoes['pre_processamento'].append('Texto contém tabs - pode ter estrutura tabular')
        
        sugestoes['validacoes'].append('Verificar consistência de unidades')
        sugestoes['expansoes'].append('Buscar dados relacionados em outras fontes')
        
        return sugestoes
    
    # Métodos auxiliares
    def _detectar_estrutura_tabular(self, texto: str) -> bool:
        """Detecta se o texto tem estrutura tabular"""
        separadores = ['\t', '|', ';']
        for sep in separadores:
            if texto.count(sep) > 2:
                return True
        return False
    
    def _extrair_contexto_local(self, texto: str, inicio: int, fim: int) -> str:
        """Extrai contexto local ao redor de uma posição"""
        contexto_inicio = max(0, inicio - 50)
        contexto_fim = min(len(texto), fim + 50)
        return texto[contexto_inicio:contexto_fim].strip()
    
    def _calcular_confianca_regex(self, match, nome_padrao: str) -> float:
        """Calcula confiança de um match regex"""
        base_confidence = {
            'valores_monetarios': 0.9,
            'numeros_com_unidades': 0.85,
            'codigos': 0.8,
            'datas': 0.75,
            'coordenadas': 0.7
        }
        return base_confidence.get(nome_padrao, 0.6)
    
    def _detectar_formato_data(self, data_str: str) -> str:
        """Detecta formato da data"""
        if '/' in data_str:
            return 'dd/mm/yyyy'
        elif '-' in data_str:
            return 'dd-mm-yyyy'
        elif '.' in data_str:
            return 'dd.mm.yyyy'
        return 'desconhecido'
    
    def _detectar_padroes_repetitivos(self, texto: str) -> List[str]:
        """Detecta padrões que se repetem"""
        padroes = []
        
        # Padrões simples
        if texto.count('FER-') > 1:
            padroes.append('Códigos FER- repetitivos')
        if texto.count('R$') > 3:
            padroes.append('Múltiplos valores monetários')
        if texto.count('km') > 3:
            padroes.append('Múltiplas medidas em km')
        
        return padroes
    
    def _detectar_sequencias_numericas(self, texto: str) -> List[str]:
        """Detecta sequências numéricas"""
        numeros = re.findall(r'\d+', texto)
        sequencias = []
        
        if len(numeros) > 2:
            sequencias.append(f'Encontrados {len(numeros)} números')
        
        return sequencias
    
    def _calcular_confianca_media(self, dados: Dict) -> float:
        """Calcula confiança média dos dados extraídos"""
        confianças = []
        
        for categoria, itens in dados.items():
            if isinstance(itens, list):
                for item in itens:
                    if isinstance(item, dict) and 'confianca' in item:
                        confianças.append(item['confianca'])
        
        return sum(confianças) / len(confianças) if confianças else 0.0


# Exemplo de uso
if __name__ == "__main__":
    # Criar processador
    processor = ExtracaoMaximaProcessor()
    
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
    Data de inauguração: 15/03/2025
    Coordenadas estação central: -19.9167, -43.9345
    """
    
    # Processar
    resultado = processor.extrair_dados_maximos(texto_exemplo)
    
    # Exibir resultado
    print("🚀 RESULTADO DA EXTRAÇÃO MÁXIMA:")
    print("=" * 50)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
