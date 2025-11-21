import json
import os

# -----------------------------------------------------------------------------
# FONTE DE DADOS: IBGE
#
# Referência oficial: https://paises.ibge.gov.br/
# -----------------------------------------------------------------------------

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados(filepath="dados_paises.json"):
    dados_globais = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            lista_paises = json.load(file)
            for dados_pais_lista in lista_paises:
                nome_pais = dados_pais_lista.pop('Pais', None)
                if nome_pais:
                    dados_globais[nome_pais] = dados_pais_lista
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None
    return dados_globais

def apresenta_pais(dados_globais, nome_pais):
    return dados_globais.get(nome_pais, "País não encontrado.")

def apresenta_dado(dados_globais, nome_dado):
    resultado = {}
    for pais, dados in dados_globais.items():
        resultado[pais] = dados.get(nome_dado)
    return resultado

def _obter_lista_de_dados_validos(dados_globais, nome_dado):
    valores = []
    for dados in dados_globais.values():
        valor = dados.get(nome_dado)
        if isinstance(valor, (int, float)): 
            valores.append(valor)
    return valores

# --- Funções static ---

def calcula_media(valores_validos):
    if not valores_validos: return 0.0
    return sum(valores_validos) / len(valores_validos)

def calcula_variancia(valores_validos):
    n = len(valores_validos)
    if n < 2: return 0.0
    media = calcula_media(valores_validos)
    return sum((x - media) ** 2 for x in valores_validos) / (n - 1)

def calcula_mediana(valores_validos):
    if not valores_validos: return 0.0
    valores = sorted(valores_validos)
    n = len(valores)
    meio = n // 2
    return valores[meio] if n % 2 == 1 else (valores[meio - 1] + valores[meio]) / 2.0

def calcula_media_ponderada_de_dado(dados_globais, nome_dado, nome_peso):
    soma_pond = 0.0
    soma_pesos = 0.0
    for dados in dados_globais.values():
        val = dados.get(nome_dado)
        peso = dados.get(nome_peso)
        if isinstance(val, (int, float)) and isinstance(peso, (int, float)) and peso > 0:
            soma_pond += val * peso
            soma_pesos += peso
    return 0.0 if soma_pesos == 0 else soma_pond / soma_pesos

# --- menu numerado ---

def selecionar_opcao(lista_opcoes, titulo):
    print(f"\n--- Selecione {titulo} ---")
    colunas = 3
    for i, item in enumerate(lista_opcoes, 1):
        print(f"{i:2d}. {item:<25}", end="")
        if i % colunas == 0:
            print()
    print("\n")

    while True:
        entrada = input(f"Digite o NÚMERO ou o NOME de '{titulo}': ").strip()
        if entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(lista_opcoes):
                return lista_opcoes[idx]
        
        entrada_lower = entrada.lower()
        for item in lista_opcoes:
            if item.lower() == entrada_lower:
                return item
        
        print("Opção inválida. Tente o número da lista.")

# --- Main ---

if __name__ == "__main__":
    ARQUIVO_JSON = "dados_paises.json"
    print(f"Carregando: {ARQUIVO_JSON}...")
    dados = carregar_dados(ARQUIVO_JSON)
    
    if not dados:
        print("Falha ao carregar dados.")
    else:
        print(f"Base carregada: {len(dados)} países.\n")
        
        lista_paises = sorted(list(dados.keys()))
        
        chaves = set()
        for d in dados.values(): chaves.update(d.keys())
        lista_dados = sorted(list(chaves))

        while True:
            limpar_terminal()
            print("--- Estatística Interativa ---")
            print("1. Ver País")
            print("2. Ranking")
            print("3. Média")
            print("4. Variância")
            print("5. Média Ponderada")
            print("6. Mediana")
            print("7. Sair")
            print("-" * 30)
            
            escolha = input("Opção: ").strip()
            
            if escolha == '7':
                break

            
            if escolha == '1':
                nome = selecionar_opcao(lista_paises, "o País")
                res = apresenta_pais(dados, nome)
                
                print(f"\n--- {nome} ---")
                if isinstance(res, dict):
                    for k, v in res.items():
                        print(f" - {k}: {v:,.2f}" if isinstance(v, (int, float)) else f" - {k}: {v}")
                else:
                    print(res)
                input("\nEnter para voltar...")

            elif escolha == '2':
                dado = selecionar_opcao(lista_dados, "o Dado para Ranking")
                res = apresenta_dado(dados, dado)
                validos = {p: v for p, v in res.items() if isinstance(v, (int, float))}
                
                print(f"\nRanking '{dado}':")
                for i, (p, v) in enumerate(sorted(validos.items(), key=lambda x: x[1], reverse=True), 1):
                    print(f" {i:02d}. {p}: {v:,.2f}")
                input("\nEnter para voltar...")

            elif escolha == '3':
                dado = selecionar_opcao(lista_dados, "o Dado para Média")
                vals = _obter_lista_de_dados_validos(dados, dado)
                print(f"\n > Média de {dado}: {calcula_media(vals):,.2f}")
                input("\nEnter para voltar...")

            elif escolha == '4':
                dado = selecionar_opcao(lista_dados, "o Dado para Variância")
                vals = _obter_lista_de_dados_validos(dados, dado)
                print(f"\n > Variância de {dado}: {calcula_variancia(vals):,.2f}")
                input("\nEnter para voltar...")

            elif escolha == '5':
                dado = selecionar_opcao(lista_dados, "o Valor (ex: PIB)")
                peso = selecionar_opcao(lista_dados, "o Peso (ex: Populacao)")
                res = calcula_media_ponderada_de_dado(dados, dado, peso)
                print(f"\n > Média Pond. de {dado} (por {peso}): {res:,.2f}")
                input("\nEnter para voltar...")

            elif escolha == '6':
                dado = selecionar_opcao(lista_dados, "o Dado para Mediana")
                vals = _obter_lista_de_dados_validos(dados, dado)
                print(f"\n > Mediana de {dado}: {calcula_mediana(vals):,.2f}")
                input("\nEnter para voltar...")
            
            else:
                input("Opção inválida.")