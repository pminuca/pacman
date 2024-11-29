from pacman import *
import time

def obtem_direcao(ponto1, ponto2):
    theta = math.atan2(ponto1[1] - ponto2[1], ponto1[0] - ponto2[0])
    dir_x = math.cos(theta) * 5
    dir_y = math.sin(theta) * 5
    return dir_x, dir_y

def pacman_cima(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (0,5)

def pacman_baixo(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (0,-5)

def pacman_direita(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (5,0)

def pacman_esquerda(estado_jogo):
    estado_jogo['pacman']['direcao_atual'] = (-5,0)

def perseguicao(fantasma_posicao, ponto_posicao):
    direcao = obtem_direcao(ponto_posicao, fantasma_posicao)
    dir_x = direcao[0]
    dir_y = direcao[1]

    if abs(dir_x) > abs(dir_y):
        if dir_x > 0:
            proxima_direcao = (5,0)
        else:
            proxima_direcao = (-5,0)
    else:
        if dir_y > 0:
            proxima_direcao = (0,5)
        else:
            proxima_direcao = (0,-5)

    testar_direcao = fantasma_posicao + proxima_direcao
    if movimento_valido(testar_direcao, estado_jogo):
        return proxima_direcao
    else:
        # procurar a direcao mais proxima
        distancia_minima = 100000
        direcao_distancia_minima = None
        for i in range(0,4):
            testar_direcao_x= fantasma_posicao[0] + DIRECOES_POSSIVEIS[i][0]
            testar_direcao_y= fantasma_posicao[1] + DIRECOES_POSSIVEIS[i][1]
            if movimento_valido((testar_direcao_x,testar_direcao_y), estado_jogo):
                distancia = calculate_distance((testar_direcao_x,testar_direcao_y),ponto_posicao)
                if distancia_minima>distancia:
                    distancia_minima=distancia
                    direcao_distancia_minima=(DIRECOES_POSSIVEIS[i])

        return direcao_distancia_minima

def movimenta_pinky(estado_jogo):
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    pinky_pos = estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].pos()
    return perseguicao(pinky_pos, pacman_pos)

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3*TAMANHO_CELULA
    scatter_corner_pos = calcula_x_y_from_index(0)
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    clyde_pos = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()
    distancia = calculate_distance(pacman_pos, clyde_pos)

    if distancia > scatter_distance_threshold:
        return perseguicao(clyde_pos, pacman_pos)
    else:
        return perseguicao(clyde_pos, scatter_corner_pos)
    
def movimenta_inky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)   

def movimenta_blinky(estado_jogo):
    return random.choice(DIRECOES_POSSIVEIS)

def perdeu_jogo(estado_jogo):
    for i in range (3,7):
        if ha_colisao(t1=estado_jogo['pacman']['objeto'], t2=estado_jogo['fantasmas'][i]['objeto'], collision_distance=20):
            terminar_jogo(estado_jogo)   

def ganhou_jogo(estado_jogo):
    if estado_jogo['score'] == 155:
        print ("Parabéns, ganhaste o jogo")
        estado_jogo['janela'].bye()
    
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
    try:
        #dicionario com as funcoes de movimento dos jogadores
        funcoes_jogador = {'pacman_cima': pacman_cima, 'pacman_baixo': pacman_baixo, 'pacman_esquerda': pacman_esquerda, 'pacman_direita': pacman_direita, 'guarda_jogo' : guarda_jogo, 'carrega_jogo' : carrega_jogo}    
        funcoes_fantasmas = {BLINKY_OBJECT : movimenta_blinky, PINKY_OBJECT : movimenta_pinky, INKY_OBJECT : movimenta_inky, CLYDE_OBJECT : movimenta_clyde}

        nome_ficheiro = input('Qual dos dois mapas pretende carregar: \n   - ENTER para carregar o mapa default \n   - s para carregar o mapa guardado\n')
        if nome_ficheiro == '':
            nome_ficheiro = 'mapa_inicial.txt'
        else:
            if nome_ficheiro == 's':
                nome_ficheiro='save.txt'
            
        #funções de inicio do jogo
        estado_jogo = init_state()
        carrega_jogo(estado_jogo, nome_ficheiro)
        setup(estado_jogo, True, funcoes_jogador,funcoes_fantasmas)
        update_board(estado_jogo)
        estado_jogo['marcador'].up()
        

        #inicia_jogo(estado_jogo)
        while not perdeu_jogo(estado_jogo):
            if estado_jogo['mapa'] is not None:
                estado_jogo['janela'].update() #actualiza a janela
                movimenta_objectos(estado_jogo)
                atualiza_pontos(estado_jogo)
                time.sleep(0.05)
            ganhou_jogo(estado_jogo)

    except TclError:
        pass





        