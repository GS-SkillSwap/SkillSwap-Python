import json
import math # Deixado caso queira implementar o Desvio Padrão (sqrt da variância)
import os # Adicionado para limpar o terminal

def limpar_terminal():
    """Limpa o console, compatível com Windows ('nt') ou Linux/macOS ('posix')."""
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados(filepath="dados_paises.json"):
    """
    Carrega os dados do JSON.
    O JSON deve ser uma LISTA de dicionários.
    Transforma a lista em um DICIONÁRIO de dicionários, usando 'Pais' como chave.
    """
    dados_globais = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            lista_paises = json.load(file)
            
            for dados_pais_lista in lista_paises:
                # Usa .pop() para extrair o nome e deixar só o dict de dados
                nome_pais = dados_pais_lista.pop('Pais', None)
                if nome_pais:
                    dados_globais[nome_pais] = dados_pais_lista
                else:
                    print("Aviso: Encontrado um registro sem nome de 'Pais'.")
                    
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filepath}' não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{filepath}' não é um JSON válido.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None
        
    return dados_globais

def apresenta_pais(dados_globais, nome_pais):
    """Retorna o dicionário de dados para um país específico."""
    if not dados_globais:
        return "Erro: Os dados não foram carregados."
        
    return dados_globais.get(nome_pais, "País não encontrado.")

def apresenta_dado(dados_globais, nome_dado):
    """Retorna um dicionário {país: valor} para um dado específico."""
    if not dados_globais:
        return "Erro: Os dados não foram carregados."

    resultado = {}
    for pais, dados in dados_globais.items():
        valor = dados.get(nome_dado) 
        resultado[pais] = valor
        
    return resultado

def _obter_lista_de_dados_validos(dados_globais, nome_dado):
    """Função auxiliar para filtrar apenas valores numéricos válidos."""
    valores = []
    if not dados_globais:
        return valores
        
    for dados in dados_globais.values():
        valor = dados.get(nome_dado)
        
        # MELHORIA: Verifica se é um número (int ou float), não apenas se não é None.
        if isinstance(valor, (int, float)): 
            valores.append(valor)
    return valores

# --- Funções Estatísticas Refatoradas ---
# Agora são "puras": recebem a lista de valores já filtrada.

def calcula_media(valores_validos):
    """Calcula a média de uma lista de números."""
    if not valores_validos:
        return 0.0
        
    return sum(valores_validos) / len(valores_validos)

def calcula_variancia(valores_validos):
    """Calcula a variância amostral (n-1) de uma lista de números."""
    n = len(valores_validos)
    
    if n < 2:
        return 0.0 # Variância não pode ser calculada com menos de 2 pontos
        
    media = calcula_media(valores_validos)
    
    soma_quadrados = sum((x - media) ** 2 for x in valores_validos)
    
    return soma_quadrados / (n - 1) # Variância Amostral

def calcula_mediana(valores_validos):
    """Calcula a mediana de uma lista de números."""
    if not valores_validos:
        return 0.0
        
    valores_ordenados = sorted(valores_validos)
    n = len(valores_ordenados)
    meio = n // 2
    
    if n % 2 == 1:
        # Lista ímpar
        return valores_ordenados[meio]
    else:
        # Lista par
        return (valores_ordenados[meio - 1] + valores_ordenados[meio]) / 2.0

def calcula_media_ponderada_de_dado(dados_globais, nome_dado, nome_dado_peso):
    """
    Calcula a média ponderada.
    Esta função não foi refatorada pois precisa acessar dois dados simultaneamente.
    """
    if not dados_globais:
        return 0.0

    soma_ponderada = 0.0
    soma_pesos = 0.0
    
    for dados in dados_globais.values():
        valor = dados.get(nome_dado)
        peso = dados.get(nome_dado_peso)
        
        # MELHORIA: Verifica se ambos são numéricos
        if isinstance(valor, (int, float)) and isinstance(peso, (int, float)) and peso > 0:
            soma_ponderada += valor * peso
            soma_pesos += peso
            
    if soma_pesos == 0:
        return 0.0
        
    return soma_ponderada / soma_pesos


# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    
    ARQUIVO_JSON = "dados_paises.json"
    
    print(f"Carregando dados de '{ARQUIVO_JSON}'...")
    dados = carregar_dados(ARQUIVO_JSON)
    
    if not dados:
        print("Não foi possível carregar os dados. Encerrando o programa.")
    else:
        print(f"Dados de {len(dados)} países carregados com sucesso.\n")
        
        # --- Listas de Consulta ---
        lookup_paises = {nome.lower(): nome for nome in dados.keys()}
        
        # MELHORIA DE ROBUSTEZ:
        # Coleta chaves de TODOS os países, não só do primeiro
        chaves_disponiveis = set()
        for dados_pais in dados.values():
            chaves_disponiveis.update(dados_pais.keys())
            
        lista_dados_disponiveis = sorted(list(chaves_disponiveis))
        lookup_dados = {nome.lower(): nome for nome in lista_dados_disponiveis}

        # --- Funções Auxiliares do Menu ---
        def obter_nome_pais():
            """Pede ao usuário um nome de país e valida."""
            while True:
                nome_digitado = input("   Digite o nome do país (ou 'listar'): ").strip().lower()
                if nome_digitado == 'listar':
                    print("  Países disponíveis:", ", ".join(sorted(dados.keys())))
                    continue
                nome_correto = lookup_paises.get(nome_digitado)
                if nome_correto:
                    return nome_correto
                print("  País não encontrado. Tente novamente.")

        def obter_nome_dado(prompt_texto):
            """Pede ao usuário um nome de dado e valida."""
            while True:
                nome_digitado = input(f"  {prompt_texto} (ou 'listar'): ").strip().lower()
                if nome_digitado == 'listar':
                    print("  Dados disponíveis:", ", ".join(lista_dados_disponiveis))
                    continue
                nome_correto = lookup_dados.get(nome_digitado)
                if nome_correto:
                    return nome_correto
                print("  Nome do dado não encontrado. Tente novamente.")
        
        # --- Loop do Menu Principal ---
        
        while True:
            limpar_terminal() # MELHORIA: Limpa a tela antes de mostrar o menu
            
            # Título e contagem movidos para dentro do loop
            print("--- Painel de Análise Estatística Interativa ---")
            print(f" (Base de {len(dados)} países carregada)\n")
            
            print("Escolha uma análise:")
            print(" 1. Ver dados de um país")
            print(" 2. Ver um dado (Ranking de todos os países)")
            print(" 3. Calcular Média de um dado")
            print(" 4. Calcular Variância de um dado")
            print(" 5. Calcular Média Ponderada de um dado")
            print(" 6. Calcular Mediana de um dado")
            print(" 7. Sair")
            print("-" * 40)
            
            escolha = input("Digite o número da sua escolha: ").strip()
            
            if escolha == '1':
                # --- Apresenta País ---
                print("\n[Análise: Ver dados de um país]")
                nome_pais = obter_nome_pais()
                resultado = apresenta_pais(dados, nome_pais)
                if isinstance(resultado, dict):
                    print(f"\n--- Dados para: {nome_pais} ---")
                    for chave, valor in resultado.items():
                        # Formata o valor se for um número
                        if isinstance(valor, (int, float)):
                            print(f"  - {chave}: {valor:,.2f}")
                        else:
                            print(f"  - {chave}: {valor}")
                else:
                    print(resultado)
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '2':
                # --- Apresenta Dado ---
                print("\n[Análise: Ranking de um dado]")
                nome_dado = obter_nome_dado("Digite o nome do dado")
                resultado = apresenta_dado(dados, nome_dado)
                
                print(f"\n  Resultados para '{nome_dado}' (ordenado do maior para o menor):")
                
                # MELHORIA: Ordena a saída para criar um ranking
                resultados_validos = {p: v for p, v in resultado.items() if isinstance(v, (int, float))}
                resultados_invalidos = {p: v for p, v in resultado.items() if not isinstance(v, (int, float))}
                
                # 3. Ordena e imprime válidos
                for pais, valor in sorted(resultados_validos.items(), key=lambda item: item[1], reverse=True):
                    print(f"  - {pais}: {valor:,.2f}")
                
                # 4. Imprime inválidos (None, "N/A", etc.) no final
                if resultados_invalidos:
                    print("  --- (Dados não numéricos ou ausentes) ---")
                    for pais, valor in resultados_invalidos.items():
                        print(f"  - {pais}: {valor}")
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '3':
                # --- Média ---
                print("\n[Análise: Calcular Média]")
                nome_dado = obter_nome_dado("Digite o nome do dado")
                
                # O Menu agora busca os dados
                valores = _obter_lista_de_dados_validos(dados, nome_dado)
                # E passa a lista limpa para a função de cálculo
                media = calcula_media(valores)
                
                print("-" * 40)
                print(f"  > A média de '{nome_dado}' é: {media:,.2f}")
                # MELHORIA DE UX: Adiciona contexto
                print(f"  (Cálculo baseado em {len(valores)} de {len(dados)} países)")
                print("-" * 40)
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '4':
                # --- Variância ---
                print("\n[Análise: Calcular Variância]")
                nome_dado = obter_nome_dado("Digite o nome do dado")
                
                valores = _obter_lista_de_dados_validos(dados, nome_dado)
                variancia = calcula_variancia(valores)
                
                print("-" * 40)
                print(f"  > A variância de '{nome_dado}' é: {variancia:,.2f}")
                print(f"  (Cálculo baseado em {len(valores)} de {len(dados)} países)")
                print("-" * 40)
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '5':
                # --- Média Ponderada ---
                print("\n[Análise: Calcular Média Ponderada]")
                nome_dado = obter_nome_dado("Digite o nome do dado para a média")
                nome_peso = obter_nome_dado("Digite o nome do dado para o peso (ex: Populacao_Milhoes)")
                
                # Esta função não foi refatorada por ser mais complexa
                media_pond = calcula_media_ponderada_de_dado(dados, nome_dado, nome_peso)
                
                print("-" * 40)
                print(f"  > A média ponderada de '{nome_dado}' por '{nome_peso}' é: {media_pond:,.2f}")
                print("-" * 40)
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '6':
                # --- Mediana ---
                print("\n[Análise: Calcular Mediana]")
                nome_dado = obter_nome_dado("Digite o nome do dado")
                
                valores = _obter_lista_de_dados_validos(dados, nome_dado)
                mediana = calcula_mediana(valores)
                
                print("-" * 40)
                print(f"  > A mediana de '{nome_dado}' é: {mediana:,.2f}")
                print(f"  (Cálculo baseado em {len(valores)} de {len(dados)} países)")
                print("-" * 40)
                
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa

            elif escolha == '7':
                print("Encerrando...")
                break
                
            else:
                print("Opção inválida. Por favor, escolha um número de 1 a 7.")
                input("\n   Pressione Enter para voltar ao menu...") # MELHORIA: Pausa