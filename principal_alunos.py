from pacman import *
import time

def obtem_direecao(ponto1, ponto2):
    theta = math.atan2(ponto1[1] - ponto2[1], ponto1[0] - ponto2[0])
    dir_x = math.cos(theta)
    dir_y = math.sin(theta)
    return dir_x, dir_y

def mover_pacman(estado_jogo, pos, angulo):
    t.up()
    t.goto((estado_jogo['pacman']['objeto'].pos()))
    t.setheading(angulo)
    t.up()
    t.fd(TAMANHO_CELULA)
    t.hideturtle()
    estado_jogo['pacman']['direcao_atual'] = pos

def pacman_cima(estado_jogo):
    mover_pacman(estado_jogo, (0,5), 90)

def pacman_baixo(estado_jogo):
    mover_pacman(estado_jogo, (0,-5), 270)

def pacman_direita(estado_jogo):
    mover_pacman(estado_jogo, (5,0), 0)

def pacman_esquerda(estado_jogo):
    mover_pacman(estado_jogo, (-5,0), 180)
    
def movimenta_pinky(estado_jogo):
    distancia_minima=100000
    direcao_distancia_minima=None
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    for i in range(0,4):
        testar_direcao_x= estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].xcor() + DIRECOES_POSSIVEIS[i][0]
        testar_direcao_y= estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].ycor() + DIRECOES_POSSIVEIS[i][1]
        if movimento_valido((testar_direcao_x,testar_direcao_y), estado_jogo):
            distancia = calculate_distance((testar_direcao_x,testar_direcao_y),pacman_pos)
            if distancia_minima>distancia:
                distancia_minima=distancia
                direcao_distancia_minima=(DIRECOES_POSSIVEIS[i])

    return direcao_distancia_minima

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_clyde(estado_jogo):
    pass
#     scatter_distance_threshold = 3
#     scatter_corner_index = 0
#     pacman_pos = estado_jogo['pacman']['objeto'].pos()
#     ghost_pos = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()
#     distancia = calculate_distance(pacman_pos, ghost_pos)
#     while not movimento_valido((estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()), estado_jogo):
#         if distancia > scatter_distance_threshold:
#             obtem_direecao(estado_jogo['pacman']['objeto'].pos(), estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos())
#             estado_jogo['fantasmas'][CLYDE_OBJECT]['direcao_atual'] = obtem_direecao(estado_jogo['pacman']['objeto'].pos(), estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos())

#         #else:
#             #break
    
#     return  obtem_direecao(estado_jogo['pacman']['objeto'].pos(), estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos())

def movimenta_inky(estado_jogo):
    direcao_escolhida = random.choice(DIRECOES_POSSIVEIS)
    while not movimento_valido((direcao_escolhida[0], direcao_escolhida[1]), estado_jogo):
        direcao_escolhida=random.choice(DIRECOES_POSSIVEIS)
        
    return direcao_escolhida

def movimenta_blinky(estado_jogo):
    direcao_escolhida = random.choice(DIRECOES_POSSIVEIS)
    while not movimento_valido((direcao_escolhida[0], direcao_escolhida[1]), estado_jogo):
        direcao_escolhida=random.choice(DIRECOES_POSSIVEIS)
        
    return direcao_escolhida

def perdeu_jogo(estado_jogo):
    for i in range (3,7):
        if ha_colisao(t1=estado_jogo['pacman']['objeto'], t2=estado_jogo['fantasmas'][i]['objeto'], collision_distance=20):
            terminar_jogo(estado_jogo)   
    
def atualiza_pontos(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() 
    y = estado_jogo['pacman']['objeto'].ycor()
    index = offset((x,y))
    if estado_jogo['mapa'][index] == 1:
        estado_jogo['score'] += 1
        estado_jogo['mapa'][index] = 7
        x, y = calcula_x_y_from_index(index)
        estado_jogo['marcador'].goto(x + 10,y + 10)
        estado_jogo['marcador'].dot(2,'blue')
        update_board(estado_jogo)

def atualiza_mapa(estado_jogo, x, y, elemento):
    index = offset((x,y))
    while estado_jogo['mapa'][index] in [BLINKY_OBJECT, PINKY_OBJECT, INKY_OBJECT, CLYDE_OBJECT]:
        index += 1
    estado_jogo['mapa'][index] = elemento

def actualiza_posicao_pacman_fantasma(estado_jogo):
    x = estado_jogo['pacman']['objeto'].xcor() 
    y = estado_jogo['pacman']['objeto'].ycor()
    atualiza_mapa(estado_jogo, x, y, PACMAN_OBJECT)
    for ghost_id, ghost in estado_jogo['fantasmas'].items():
        x = ghost['objeto'].xcor()
        y = ghost['objeto'].ycor()
        atualiza_mapa(estado_jogo, x, y, ghost_id)

def guarda_jogo(estado_jogo):
    actualiza_posicao_pacman_fantasma(estado_jogo)
    mapa = estado_jogo['mapa']

    nome_ficheiro = 'save.txt'

    with open(nome_ficheiro, 'w') as ficheiro: 
        for i in range(0, len(mapa), MAP_WIDTH):
            linha = ','.join(map(str, mapa[i:i+MAP_WIDTH]))  
            ficheiro.write(linha + '\n')

def carrega_jogo(estado_jogo, nome_ficheiro):
    mapa_jogo = [] 

    with open(nome_ficheiro, 'r') as ficheiro: 
        for linha_ficheiro in ficheiro: 
            linha = [int(num) for num in linha_ficheiro.strip().split(',') if num]
            mapa_jogo.extend(linha) 

    estado_jogo['mapa'] = mapa_jogo
    pontos = mapa_jogo.count(7)
    estado_jogo['score'] = pontos

if __name__ == '__main__':
    #dicionario com as funcoes de movimento dos jogadores
    funcoes_jogador = {'pacman_cima': pacman_cima, 'pacman_baixo': pacman_baixo, 'pacman_esquerda': pacman_esquerda, 'pacman_direita': pacman_direita, 'guarda_jogo' : guarda_jogo, 'carrega_jogo' : carrega_jogo}    
    funcoes_fantasmas = {BLINKY_OBJECT : movimenta_blinky, PINKY_OBJECT : movimenta_pinky, INKY_OBJECT : movimenta_inky, CLYDE_OBJECT : movimenta_clyde}

    nome_ficheiro = input('Pretende carregar um mapa (Enter para carregar o mapa default): ')
    if nome_ficheiro == '':
        nome_ficheiro = 'mapa_inicial.txt'
    
    #funções de inicio do jogo
    estado_jogo = init_state()
    carrega_jogo(estado_jogo, nome_ficheiro)
    setup(estado_jogo, True, funcoes_jogador,funcoes_fantasmas)
    update_board(estado_jogo)

    #inicia_jogo(estado_jogo)
    while not perdeu_jogo(estado_jogo):
        if estado_jogo['mapa'] is not None:
            estado_jogo['janela'].update() #actualiza a janela
            movimenta_objectos(estado_jogo)
            atualiza_pontos(estado_jogo)
            time.sleep(0.05)