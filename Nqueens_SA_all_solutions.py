import random
import math
import time

# =============================================
# Funções Principais do Algoritmo
# =============================================

def simulated_annealing_n_queens(N, temperatura_inicial, taxa_resfriamento, temp_minima, visitados=None):
    """
    Versão modificada do Simulated Annealing para o problema das N-Rainhas.
    Inclui verificação de estados já visitados para evitar soluções repetidas.
    """
    # Inicialização aleatória do estado (permutação de colunas)
    estado_atual = list(range(N))
    random.shuffle(estado_atual)
    energia_atual = calcular_energia(estado_atual)
    
    # Controle do processo de resfriamento
    temperatura = temperatura_inicial
    
    # Loop principal: executa até resfriar ou encontrar solução perfeita
    while temperatura > temp_minima and energia_atual > 0:
        # Gera um vizinho trocando duas colunas aleatórias
        vizinho = estado_atual.copy()
        i, j = random.sample(range(N), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
        
        # Calcula energia do vizinho, com verificação de repetição
        if visitados is not None and tuple(vizinho) in visitados:
            energia_vizinho = float('inf')
        else:
            energia_vizinho = calcular_energia(vizinho)
        
        # Decisão de aceitação
        delta_energia = energia_vizinho - energia_atual
        if delta_energia < 0 or (random.random() < math.exp(-delta_energia / temperatura)):
            estado_atual = vizinho
            energia_atual = energia_vizinho
        
        # Resfria o sistema
        temperatura *= taxa_resfriamento

    return estado_atual, energia_atual

# =============================================
# Funções Auxiliares
# =============================================

def calcular_energia(estado):
    """
    Calcula o número de conflitos diagonais (energia) para um estado do tabuleiro.
    """
    conflitos = 0
    N = len(estado)
    for i in range(N):
        for j in range(i + 1, N):
            if abs(i - j) == abs(estado[i] - estado[j]):
                conflitos += 1
    return conflitos

# =============================================
# Encontrar Todas as Soluções Únicas
# =============================================

def encontrar_solucoes_unicas(N, max_tentativas, temperatura_inicial, taxa_resfriamento, temp_minima):
    solucoes = set()
    visitados = set()
    
    for tentativa in range(1, max_tentativas + 1):
        solucao, energia = simulated_annealing_n_queens(
            N, temperatura_inicial, taxa_resfriamento, temp_minima, visitados
        )
        if energia == 0:
            solucao_t = tuple(solucao)
            if solucao_t not in solucoes:
                solucoes.add(solucao_t)
                visitados.add(solucao_t)
    return [list(s) for s in solucoes]

# =============================================
# Execução com Tentativas Dinâmicas
# =============================================

# Dicionário com número exato de soluções para N até, digamos, 10
solucoes_conhecidas = {
    1:      1,
    2:      0,
    3:      0,
    4:      2,
    5:     10,
    6:      4,
    7:     40,
    8:     92,
    9:    352,
    10:   724,
    11:  2680,
    12: 14200,
    13: 73712,
    14:365596,
    15:2279184,
}

temperatura_inicial = 1000.0
taxa_resfriamento = 0.999
temp_minima = 0.01

caminho = r'C:\Users\ivana\Documents\Estudo\Quantum Annealing\BK\tempos_sa_avancado.txt'
with open(caminho, 'w') as f:
    f.write("N,max_tentativas,tempo,solucoes\n")

for N in range(4, 14):
    alvo = solucoes_conhecidas.get(N, None)
    max_tent = 50        # chute inicial
    teto = 100000         # limite para não ficar preso
    best_time = None
    best_sols = 0

    while True:
        inicio = time.time()
        solucoes = encontrar_solucoes_unicas(
            N, max_tent,
            temperatura_inicial, taxa_resfriamento, temp_minima
        )
        dur = time.time() - inicio
        qtd = len(solucoes)

        # guarda “melhor” resultado (mais soluções por menos tempo)
        if best_time is None or (qtd > best_sols and dur < best_time):
            best_time = dur
            best_sols = qtd

        # critério de parada: achou todas as soluções (se souber) OU atingiu teto
        if (alvo is not None and qtd >= alvo) or max_tent >= teto:
            print(f"N={N} → tentativas={max_tent}, "
                  f"soluções={qtd}, tempo={dur:.2f}s")
            with open(caminho, 'a') as f:
                f.write(f"{N},{max_tent},{dur:.4f},{qtd}\n")
            break

        # caso contrário, aumenta as tentativas e repete
        max_tent *= 2  # você pode mudar para incremento fixo: max_tent += 50