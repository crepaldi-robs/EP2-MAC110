"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP,
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : Roberto Crepaldi Neto
  NUSP : 15487099

  Referências: Com exceção das rotinas fornecidas no enunciado
  e em sala de aula, caso você tenha utilizado alguma refência,
  liste-as abaixo para que o seu programa não seja considerado
  plágio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em
  http://wiki.python.org.br/QuickSort
"""

import math
# import sys

'''
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
'''


_const_G = 8.65 * (10 ** -13)


def initNave(x, y, v_x, v_y, r, id):
    return [[x, y], [v_x, v_y], r, id]


def initAstro(x, y, m, r, id):
    return [[x, y], m, r, id]


def distancia(p1, p2):
    """
Calcula a distância entre dois pontos fornecidos $P1 = [x_1, x_2]$ e $P2 = [x_2, y_2]$.

    :param p1: [float, float]
    :param p2: [float, float]
    :return: float
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def aceleracaoGravitacional(astro, p):
    """
Calcula e devolve a aceleração da atração gravitacional $[a_x, a_y]$
exercida sobre a nave no ponto $P = [x, y]$ pelo astro $Astro$.

    :param astro: Astro
    :param p: [float, float]
    :return: [float, float]
    """
    acceleration = (_const_G * astro[1]) / (distancia(p, astro[0]) ** 2)
    d_x = p[0] - astro[0][0]
    d_y = p[1] - astro[0][1]
    r = distancia(astro[0], p)
    return [-acceleration * d_x / r, -acceleration * d_y / r]


def aceleracaoResultante(astros, p):
    """
Calcula e devolve a aceleração resultante $[a_x, a_y]$
da soma das contribuições exercidas por cada um dos astros presentes
na lista $Astros$ sobre a nave no ponto $P = [x, y]$.

    :param astros: [Astro]
    :param p: [float, float]
    :return: [float, float]
    """
    acceleration = [0, 0]
    for astro in astros:
        acceleration[0] += aceleracaoGravitacional(astro, p)[0]
        acceleration[1] += aceleracaoGravitacional(astro, p)[1]
    return acceleration


def deteccaoColisao(nave, astros):
    """
Verifica se ocorre sobreposição entre a nave fornecida com algum dos astros
presentes na lista $Astros$. Devolve \textbf{True} se a nave colidiu com algum astro,
caso contrário a função retorna \textbf{False}.

    :param nave: Nave
    :param astros: [Astro]
    :return: bool
    """
    for astro in astros:
        if distancia(nave[0], astro[0]) <= nave[2] + astro[2]:
            return True
    return False


def atualizaNave(nave, astros, delta_t):
    """
Atualiza a posição e velocidade da nave em $Nave$
sujeita às forças de atração gravitacional dos astros presentes na lista $Astros$,
após um intervalo de tempo $delta_t$ (Δt).

    :param nave: Nave
    :param astros: [Astro]
    :param delta_t: float
    :return: Nave
    """
    acceleration = aceleracaoResultante(astros, nave[0])

    # eprint(f'pre-Nave({nave.id}): {nave.pos}, {nave.vel} | a = {acceleration}', end='\n')

    nave[0][0] += nave[1][0] * delta_t + acceleration[0] * (delta_t ** 2 / 2)
    nave[0][1] += nave[1][1] * delta_t + acceleration[1] * (delta_t ** 2 / 2)

    nave[1][0] += acceleration[0] * delta_t
    nave[1][1] += acceleration[1] * delta_t

    # eprint(f'pos-Nave({nave.id}): {nave.pos}, {nave.vel} | a = {acceleration}', end='\n')

    return initNave(nave[0][0], nave[0][1], nave[1][0], nave[1][1], nave[2], nave[3])


def distanciaAstroMaisProximo(nave, astros):
    """
Calcula a distância da nave $Nave$ em relação ao astro mais próximo
dentre os astros presentes na lista $Astros$. A distância deve ser medida em relação à
superfície do astro e da nave. Em caso de nave colidida, a disntância deve ser zero.

    :param nave: Nave
    :param astros: [Astro]
    :return: float
    """
    mn_dist = distancia(nave[0], astros[0][0])
    aux = []
    for astro in astros:
        dist = distancia(nave[0], astro[0]) - (nave[2] + astro[2])
        # print(f'dist = distancia({nave[0]}, {astro[0]}) - ({nave[2]} + {astro[2]}) = {distancia(nave[0], astro[0])} - {nave[2] + astro[2]} = {dist}')
        if deteccaoColisao(nave, astros):
            dist = 0
        aux.append(dist)
        if dist < mn_dist:
            mn_dist = dist
    # print(aux)
    return mn_dist


def simulacao(naves, astros, niter, delta_t):
    """
Recebe uma lista de naves em $Naves$, uma lista de astros em $Astros$,
o número de iterações $niter$ da simulação e o intervalo de tempo $delta_t$.
A função deve calcular as trajetórias das naves em $Naves$ sob o efeito da
força gravitacional exercida pelos astros em $Astros$.

A função deve devolver:
  ∙Uma lista $[T_1, T_2, …, T_N]$ das trajetórias de cada nave, sendo $N$
  o número total de naves. Cada trajetória $T_i$ é por sua vez uma lista das posições
  da i-ésima nave ao longo da simulação.
  ⋅Uma lista $[D_1, D_2, …, D_N]$, em que $N$ é o número total de naves e
  $D_i$ representa uma lista com as distâncias da i-ésima nave em relação
  ao seu astro mais próximo a cada iteração.
O instante inicial da simulação é zero e a cada passo da simulação o tempo de simulação
é acrescido de $delta_t$. As posições das naves serão atualizadas em cada passo da
simulação. Uma nave será desativada assim que colodir com algum astro. Neste caso
a nave conserva a posição em que ocorreu a colisão ao longo das próximas iterações.
Não serão consideradas colisões entre naves. A simulação termina quando o número de
iterações executadas atingir $niter$.
Esta função DEVE usar as funções "atualizaNave", "deteccaoColisao" e "distanciaAstroMaisProximo".

    :param naves: [Nave]
    :param astros: [Astro]
    :param niter: int
    :param delta_t: float
    :return: [[float]], [[float]]
    """
    aux_id = 0
    for nave in naves:
        nave.append(aux_id)
        aux_id += 1
    aux_id = 0
    for astro in astros:
        astro.append(aux_id)
        aux_id += 1

    T = [[-1] * niter] * len(naves)
    D = [[-1] * niter] * len(naves)

    for i in range(niter):
        print('********* iteração {} *********'.format(i + 1))
        for nave in naves:
            if not deteccaoColisao(nave, astros):
                nave = atualizaNave(nave, astros, delta_t)

            p = nave[0]
            mn_d = distanciaAstroMaisProximo(nave, astros)
            T[nave[3]][i] = p
            D[nave[3]][i] = mn_d

            print('*** Nave {} ***'.format(nave[3] + 1))
            print('Posição: ({:.3f},{:.3f})'.format(p[0], p[1]))
            print('Distância ao astro mais próximo: {:.3f}'.format(mn_d))

    # eprint(f'T: {T}', end='\n')
    # eprint(f'D: {D}', end='\n')

    return T, D


# main
#Não altere o código abaixo:
def main():
    niter = int(input("Número máximo de iterações: "))
    delta_t = float(input("Delta t: "))
    nnaves = int(input("Número de naves: "))
    Naves = []
    for i in range(nnaves):
        print("*** Nave %d ***"%(i+1))
        x,y = input("Digite a posição (x,y): ").split()
        x,y = float(x),float(y)
        vx,vy = input("Digite a velocidade inicial (vx,vy): ").split()
        vx,vy = float(vx),float(vy)
        r = float(input("Digite o raio: "))
        Naves.append([[x,y], [vx,vy], r])

    nastros = int(input("Número de astros: "))
    Astros = []
    for i in range(nastros):
        print("*** Astro %d ***"%(i+1))
        x,y = input("Digite a posição (x,y): ").split()
        x,y = float(x),float(y)
        massa = float(input("Digite a massa: "))
        R = float(input("Digite o raio: "))
        Astros.append([[x,y], massa, R])

    T, D = simulacao(Naves, Astros, niter, delta_t)
    for i in range(niter):
        print("********* iteração %d *********"%(i+1))
        for j in range(nnaves):
            print("*** Nave %d ***"%(j+1))
            print("Posição: ",end="")
            P = T[j][i]
            print("(%.3f,%.3f)"%(P[0],P[1]))
            print("Distância ao astro mais próximo: ",end="")
            print("%.3f"%(D[j][i]))


if __name__ == '__main__':
    main()
