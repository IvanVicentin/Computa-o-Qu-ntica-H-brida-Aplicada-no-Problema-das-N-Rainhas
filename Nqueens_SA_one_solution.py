import random
import math

# ======================
# Funções do Algoritmo
# ======================

def simulated_annealing_n_queens(N, temperatura_inicial, taxa_resfriamento, temp_minima):
    """
    Resolve o problema das N-Rainhas usando simulated annealing.
    
    Args:
        N (int): Número de rainhas e tamanho do tabuleiro (N x N)
        temperatura_inicial (float): Temperatura inicial para o processo
        taxa_resfriamento (float): Taxa de redução da temperatura (0 < taxa < 1)
        temp_minima (float): Temperatura mínima para parar o algoritmo
    
    Returns:
        tuple: (solução final, energia final)
    """
    
    # Inicializa o estado como uma permutação aleatória de colunas
    # Garante automaticamente exatamente uma rainha por linha e coluna
    # Exemplo para N=4: [1, 3, 0, 2] significa:
    # - Linha 0: Rainha na coluna 1
    # - Linha 1: Rainha na coluna 3
    # - Linha 2: Rainha na coluna 0
    # - Linha 3: Rainha na coluna 2
    estado_atual = list(range(N))
    random.shuffle(estado_atual) #Funçao p/ randomizar
    
    # Calcula energia inicial (número de conflitos nas diagonais)
    energia_atual = calcular_energia(estado_atual)
    
    # Inicializa temperatura e contador de iterações
    temperatura = temperatura_inicial
    iteracao = 0 #Contador de iterações
    
    # Loop principal de annealing - executa até resfriar (temp minima) ou encontrar solução (diferença da energia = 0)
    while temperatura > temp_minima and energia_atual > 0:
        # Gera estado vizinho trocando duas rainhas aleatórias
        # Mantém a propriedade de permutação (1 rainha por linha/coluna)
        vizinho = estado_atual.copy() # Cria um novo estado copiando o antigo
        i, j = random.sample(range(N), 2)  # Seleciona dois índices distintos
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]  # Troca as colunas
           
        # Calcula diferença de energia entre estado atual e vizinho
        nova_energia = calcular_energia(vizinho)
        delta_energia = nova_energia - energia_atual
        
        # Critério de aceitação de
        if delta_energia < 0:
            # Aceita imediatamente soluções melhores
            estado_atual = vizinho
            energia_atual = nova_energia
        else:
            # Aceita soluções piores com probabilidade baseada na temperatura
            # Probabilidade diminui conforme a temperatura baixa
            probabilidade_aceitacao = math.exp(-delta_energia / temperatura)
            if random.random() < probabilidade_aceitacao:
                estado_atual = vizinho
                energia_atual = nova_energia
        
        # Resfria o sistema de acordo com a taxa
        temperatura *= taxa_resfriamento
        iteracao += 1

    return estado_atual, energia_atual

def calcular_energia(estado):
    """
    Calcula a energia (número de rainhas atacando-se) para um estado do tabuleiro.
    Energia mais baixa é melhor (0 = solução válida).
    
    Args:
        estado (list): Array representando posições das rainhas (índice = linha, valor = coluna)
    
    Retorna:
        int: Número de conflitos diagonais (rainhas se atacando)
    """
    conflitos = 0
    N = len(estado)
    
    # Verifica todos os pares de rainhas
    for i in range(N):
        for j in range(i + 1, N):
            # Duas rainhas estão na mesma diagonal se:
            # Distância horizontal == distância vertical
            if abs(i - j) == abs(estado[i] - estado[j]): #[1, 3, 0, 2]
                conflitos += 1
                
    return conflitos # Que serão a "energia"

def imprimir_tabuleiro(solucao):
    """
    Visualiza a solução do N-Rainhas como um tabuleiro de xadrez.
    
    Args:
        solucao (list): Array de posições das rainhas
    """
    N = len(solucao)
    for linha in range(N):
        # Cria representação visual da linha
        linha_tabuleiro = []
        for coluna in range(N):
            # Adiciona 'Q' se tem rainha, '.' se vazio
            linha_tabuleiro.append('Q' if coluna == solucao[linha] else '.')
        print(' '.join(linha_tabuleiro))

# ======================
# Configuração do Algoritmo
# ======================
N = 300                 # Tamanho do tabuleiro e número de rainhas
temperatura_inicial = 1000.0   # Alta temperatura inicial promove exploração
taxa_resfriamento = 0.999     # Redução de 0,1% na temperatura por iteração
temp_minima = 0.01          # Temperatura mínima para parar a busca

# ======================
# Execução e Resultados
# ======================
solucao, energia = simulated_annealing_n_queens(N, temperatura_inicial, taxa_resfriamento, temp_minima)

if energia == 0:
    print(f"Solução válida encontrada para {N}-Rainhas!")
    imprimir_tabuleiro(solucao)
else: # Caso o código nao esteja encontrando soluções corretas, variar os parâmetros
    print(f"Solução perfeita não encontrada (conflitos restantes: {energia}). Tente:")
    print("- Aumentar a temperatura inicial")
    print("- Reduzir a taxa de resfriamento ")
    print("- Diminuir a temperatura mínima")
    imprimir_tabuleiro(solucao)  # Mostra a melhor tentativa
