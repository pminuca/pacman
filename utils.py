import turtle
from pacman import *

def carrega_mapa(nome_ficheiro): 
    mapa_jogo = [] 

    with open(nome_ficheiro, 'r') as ficheiro: 
        for linha_ficheiro in ficheiro: 
            linha = [int(num) for num in linha_ficheiro.strip().split(',') if num]
            mapa_jogo.extend(linha) 
        
    return mapa_jogo

def arranjar_posicao_pacman(estado_jogo):
    turtle.up()
    turtle.goto((estado_jogo['pacman']['objeto'].pos()))
    


def arranjar_posicao_inky(estado_jogo):
    turtle.up()
    turtle.goto(estado_jogo['fantasmas'][INKY_OBJECT]['objeto'].pos())


