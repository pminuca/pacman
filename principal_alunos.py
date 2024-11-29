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

def perseguicao(posicao_x_fantasma, posicao_y_fantasma,ponto_posicao):
    distancia_minima=100000
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

def movimenta_pinky(estado_jogo):
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    pinky_pos = estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].pos()
    pinky_x = estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].xcor()
    pinky_y = estado_jogo['fantasmas'][PINKY_OBJECT]['objeto'].ycor()
    perseguicao(pinky_x, pinky_y, pacman_pos)
    return perseguicao(pinky_x, pinky_y, pacman_pos)

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def movimenta_clyde(estado_jogo):
    scatter_distance_threshold = 3*TAMANHO_CELULA
    scatter_corner_index = calcula_x_y_from_index(0)
    pacman_pos = estado_jogo['pacman']['objeto'].pos()
    clyde_pos = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].pos()
    clyde_x = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].xcor()
    clyde_y = estado_jogo['fantasmas'][CLYDE_OBJECT]['objeto'].ycor()
    distancia = calculate_distance(pacman_pos, clyde_pos)

    if distancia > scatter_distance_threshold:
        return perseguicao(clyde_x, clyde_y, pacman_pos)
        
    else:
        return perseguicao(clyde_x, clyde_y, scatter_corner_index)
    
def movimenta_inky(estado_jogo):
    direcao_escolhida = random.choice(DIRECOES_POSSIVEIS)   
    return direcao_escolhida

def movimenta_blinky(estado_jogo):
    direcao_escolhida = random.choice(DIRECOES_POSSIVEIS)
    return direcao_escolhida

def perdeu_jogo(estado_jogo):
    for i in range (3,7):
        if ha_colisao(t1=estado_jogo['pacman']['objeto'], t2=estado_jogo['fantasmas'][i]['objeto'], collision_distance=20):
            terminar_jogo(estado_jogo)   

def ganhou_jogo(estado_jogo):
    mapa = estado_jogo['mapa']
    if mapa.count(7) == 155:
        print ("Parabéns, ganhaste o jogo")
    
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

    nome_ficheiro = input('Qual dos dois mapas pretende carregar (ENTER para carregar o mapa default), (s para carregar o mapa guardado): ')
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
    #except TclError





        