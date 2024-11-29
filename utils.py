from pacman import *
from principal_alunos import *

def perseguicao(ponto_fantasma, ponto_final): 
    ponto_fantasma = estado_jogo['fantasmas'][]['objeto'].pos()
    direcao=random.choice(DIRECOES_POSSIVEIS)
    if movimento_valido(direcao, estado_jogo):
        distancia = calculate_distance(ponto_fantasma,ponto_final)
        if 


def obtem_direcao(ponto1, ponto2):
    theta = math.atan2(ponto1[1] - ponto2[1], ponto1[0] - ponto2[0])
    dir_x = math.cos(theta) * 5
    dir_y = math.sin(theta) * 5
    return dir_x, dir_y

def perseguicao(posicao_x_fantasma, posicao_y_fantasma, fantasma_posicao, ponto_posicao):
    distancia_minima=601
    direcao_distancia_minima=None
    theta = math.atan2(fantasma_posicao[1] - ponto_posicao[1], fantasma_posicao[0] - ponto_posicao[0])
    dir_x = math.cos(theta) * 5
    dir_y = math.sin(theta) * 5

    if abs(dir_x) > abs(dir_y):
        if dir_x > 0:
            proxima_direcao = (5,0)
        else:
            proxima_direcao = (-5,0)

    else:
        if abs(dir_x) < abs(dir_y):
            if dir_y > 0:
                proxima_direcao = (0,5)
            else:
                proxima_direcao = (0,-5)

    testar_direcao = fantasma_posicao + proxima_direcao
    if movimento_valido(testar_direcao, estado_jogo):
        distancia = calculate_distance(testar_direcao,ponto_posicao)
        if distancia_minima>distancia:
            distancia_minima=distancia
            direcao_distancia_minima=proxima_direcao

    return direcao_distancia_minima



def perseguicao(posicao_x_fantasma, posicao_y_fantasma,ponto_posicao):
    distancia_minima=601
    direcao_distancia_minima=None
    for i in range(0,4):
        testar_direcao_x= posicao_x_fantasma + DIRECOES_POSSIVEIS[i][0]
        testar_direcao_y= posicao_y_fantasma + DIRECOES_POSSIVEIS[i][1]
        if movimento_valido((testar_direcao_x,testar_direcao_y), estado_jogo):
            distancia = calculate_distance((testar_direcao_x,testar_direcao_y),ponto_posicao)
            if distancia_minima>distancia:
                distancia_minima=distancia
                direcao_distancia_minima=(DIRECOES_POSSIVEIS[i])

    return direcao_distancia_minima


def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3
    scatter_corner_index = (0,0)
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    ghost_pos = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()
    pacman_x = pacman_pos[0]
    pacman_y = pacman_pos[1]
    clyde_x = ghost_pos[0]
    clyde_y = ghost_pos[1]
    distancia_clyde = calculate_distance(pacman_pos,ghost_pos)
    if distancia_clyde > scatter_distance_threshold:
        if abs(pacman_x - clyde_x) > abs(pacman_y - clyde_y):
            if pacman_x > clyde_x:
                direcao_clyde = (5,0)
            if pacman_x < clyde_x:
                direcao_clyde = (-5,0)
        else:
            if pacman_y > clyde_y:
                direcao_clyde = (0,5)
            if pacman_y < clyde_y:
                direcao_clyde = (0,-5)
        if movimento_valido((clyde_x + direcao_clyde[0], clyde_y + direcao_clyde[1]), estado_jogo):
            return direcao_clyde
        else:
            direcao_clyde = random.choice(DIRECOES_POSSIVEIS)
            return direcao_clyde
        
    




def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3  # Distância mínima para dispersar
    scatter_corner = (0,0)  # Coordenadas fixas do scatter corner
    
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    clyde = estado_jogo['fantasmas']['CLYDE_OBJECT']
    ghost_pos = clyde['objeto'].pos()
    
    # Calcular distância entre Clyde e Pac-Man
    distancia = calculate_distance(pacman_pos, ghost_pos)
    
    # Definir o alvo: ou Pac-Man, ou o scatter corner
    target_tile = pacman_pos if distancia > scatter_distance_threshold else scatter_corner
    
    # Determinar a melhor direção para se mover em direção ao target_tile
    melhor_direcao = None
    menor_distancia = 601
    
    for direcao in DIRECOES_POSSIVEIS:
        # Próxima posição considerando a direção
        next_x = ghost_pos[0] + direcao[0]
        next_y = ghost_pos[1] + direcao[1]
        next_tile = (next_x, next_y)
        
        # Verificar se o movimento é válido
        if movimento_valido(next_tile, estado_jogo):
            # Calcular a distância até o alvo (target_tile)
            distancia = calculate_distance(next_tile, target_tile)
            
            # Selecionar a direção que minimiza a distância
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_direcao = direcao
    
    # Atualizar posição de Clyde
    if melhor_direcao:
        next_x = ghost_pos[0] + melhor_direcao[0]
        next_y = ghost_pos[1] + melhor_direcao[1]
        clyde['objeto'].goto(next_x, next_y)
        clyde['direcao_atual'] = melhor_direcao
    else:
        # Caso não haja direção válida, Clyde permanece parado
        clyde['direcao_atual'] = None

    return melhor_direcao







DIRECOES_POSSIVEIS = [(0, 5), (0, -5), (5, 0), (-5, 0)]

def movimenta_fantasma_perseguidor(estado_jogo, ghost_id):
    """
    Move um fantasma em direção ao Pac-Man.
    """
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    ghost = estado_jogo['fantasmas'][ghost_id]
    ghost_pos = ghost['objeto'].pos()

    # Usar obtem_direecao para calcular direção desejada
    dir_x, dir_y = obtem_direecao(pacman_pos, ghost_pos)

    melhor_direcao = None
    menor_distancia = float('inf')

    for direcao in DIRECOES_POSSIVEIS:
        # Adicionar a direção proposta
        next_x = ghost_pos[0] + direcao[0]
        next_y = ghost_pos[1] + direcao[1]
        next_tile = (next_x, next_y)

        # Verificar se a direção é válida
        if movimento_valido(next_tile, estado_jogo):
            # Comparar ângulo para priorizar a direção que mais aproxima do Pac-Man
            direcao_desejada = (dir_x * 5, dir_y * 5)  # Ajustar escala para o grid
            distancia_desejada = calculate_distance((next_x, next_y), pacman_pos)

            # Escolher a menor distância como critério de perseguição
            if distancia_desejada < menor_distancia:
                melhor_direcao = direcao
                menor_distancia = distancia_desejada

    # Movimentar o fantasma
    if melhor_direcao:
        next_x = ghost_pos[0] + melhor_direcao[0]
        next_y = ghost_pos[1] + melhor_direcao[1]
        goto(next_x, next_y, ghost['objeto'])
        ghost['direcao_atual'] = melhor_direcao
    else:
        ghost['direcao_atual'] = None  # Fica parado se não houver direção válida





DIRECOES_POSSIVEIS = [(0, 5), (0, -5), (5, 0), (-5, 0)]

def movimenta_fantasma_fuga(estado_jogo, ghost_id, distancia_critica):
    """
    Move um fantasma para longe do Pac-Man, indo em direção ao canto (0, 0)
    se estiver muito próximo do Pac-Man.
    """
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    ghost = estado_jogo['fantasmas'][ghost_id]
    ghost_pos = ghost['objeto'].pos()

    # Verificar a distância atual entre o fantasma e Pac-Man
    distancia_para_pacman = calculate_distance(ghost_pos, pacman_pos)

    # Se estiver fora da distância crítica, não faz nada
    if distancia_para_pacman > distancia_critica:
        return

    # Caso contrário, fugir para o canto (0, 0)
    melhor_direcao = None
    menor_distancia_canto = float('inf')

    for direcao in DIRECOES_POSSIVEIS:
        # Calcular nova posição com base na direção
        next_x = ghost_pos[0] + direcao[0]
        next_y = ghost_pos[1] + direcao[1]
        next_tile = (next_x, next_y)

        # Verificar se o movimento é válido
        if movimento_valido(next_tile, estado_jogo):
            # Calcular distância do canto (0, 0)
            distancia_canto = calculate_distance(next_tile, (0, 0))

            # Escolher a direção que aproxima mais do canto
            if distancia_canto < menor_distancia_canto:
                melhor_direcao = direcao
                menor_distancia_canto = distancia_canto

    # Mover o fantasma na direção escolhida
    if melhor_direcao:
        next_x = ghost_pos[0] + melhor_direcao[0]
        next_y = ghost_pos[1] + melhor_direcao[1]
        goto(next_x, next_y, ghost['objeto'])
        ghost['direcao_atual'] = melhor_direcao
    else:
        ghost['direcao_atual'] = None  # Fica parado se não houver direção válida
