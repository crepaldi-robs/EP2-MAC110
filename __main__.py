import math
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


_const_G = 8.65 * 1e-13


class Nave:
    def __init__(self, x, y, vx, vy, r, i):
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.radius = r
        self.id = i

    def __repr__(self):
        return f'Nave[{self.id}](position={self.pos}, velocity={self.vel}, radius={self.radius})'

    def __str__(self):
        return self.__repr__()


class Astro:
    def __init__(self, x, y, m, r, i):
        self.pos = [x, y]
        self.mass = m
        self.radius = r
        self.id = i

    def __repr__(self):
        return f'Astro[{self.id}](position={self.pos}, mass={self.mass}, radius={self.radius})'

    def __str__(self):
        return self.__repr__()


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
    acceleration = (_const_G * astro.mass) / (distancia(p, astro.pos) ** 2)
    d_x = abs(p[0] - astro.pos[0])
    d_y = abs(p[1] - astro.pos[1])
    r = distancia(astro.pos, p)
    return [acceleration * d_x / r, acceleration * d_y / r]


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
        acceleration += aceleracaoGravitacional(astro, p)
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
        if distancia(nave.pos, astro.pos) < nave.radius:
            return False
    return True


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
    acceleration = aceleracaoResultante(astros, nave.pos)

    nave.pos[0] = nave.pos[0] + nave.vel[0] * delta_t + acceleration[0] * (delta_t ** 2 / 2)
    nave.pos[1] = nave.pos[1] + nave.vel[1] * delta_t + acceleration[1] * (delta_t ** 2 / 2)

    nave.vel[0] = nave.vel[0] + acceleration[0] * delta_t
    nave.vel[1] = nave.vel[1] + acceleration[1] * delta_t

    return Nave(nave.pos[0], nave.pos[0], nave.vel[0], nave.vel[1], nave.radius, nave.id)


def distanciaAstroMaisProximo(nave, astros):
    """
Calcula a distância da nave $Nave$ em relação ao astro mais próximo
dentre os astros presentes na lista $Astros$. A distância deve ser medida em relação à
superfície do astro e da nave. Em caso de nave colidida, a disntância deve ser zero.

    :param nave: Nave
    :param astros: [Astro]
    :return: float
    """
    mn_dist = distancia(nave.pos, astros[0].pos)
    for astro in astros:
        if distancia(nave.pos, astro.pos) < mn_dist:
            mn_dist = distancia(nave.pos, astro.pos)
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
    T = [[]]
    D = [[]]

    for i in range(len(naves)):
        auxT, auxD = [], []
        for j in range(niter):
            auxT.append(naves[i].pos)
            auxD.append(distanciaAstroMaisProximo(naves[i], astros))
        T.append(auxT)
        D.append(auxD)

    '''
    for nave in naves:
        T[nave.id].append(nave.pos)
        D[nave.id].append(distanciaAstroMaisProximo(nave, astros))

    eprint('0-T:', T)
    eprint('0-D:', D)
    '''

    for i in range(niter):
        print('********* iteração {} *********'.format(i + 1))
        auxT, auxD = [], []
        for nave in naves:
            if deteccaoColisao(nave, astros):
                nave = atualizaNave(nave, astros, delta_t)

            p = nave.pos
            mn_d = distanciaAstroMaisProximo(nave, astros)
            auxT.append(p)
            auxD.append(mn_d)

            print('*** Nave {} ***'.format(nave.id + 1))
            print('Posição: ({},{})'.format(p[0], p[1]))
            print('Distância ao astro mais próximo: {}'.format(mn_d))

            eprint('{}-T:'.format(i + 1), T)
            eprint('{}-D:'.format(i + 1), D)
        T.append(auxT)
        D.append(auxD)

    eprint("n-T:", T)
    eprint("n-D:", D)

    return T, D


# main
def main():
    niter = int(input('Número máximo de iterações:'))
    delta_t = float(input('Delta t:'))

    naves = []
    astros = []

    sz_naves = int(input('Número de naves:'))
    for i in range(sz_naves):
        print('*** Nave', i + 1, '***')
        x = float(input('Digite a posição (x,y):'))
        y = float(input())
        vx = float(input('Digite a velocidade inicial (vx,vy):'))
        vy = float(input())
        r = float(input('Digite o raio:'))

        naves.append(Nave(x, y, vx, vy, r, i))

    sz_astros = int(input('Número de astros:'))
    for i in range(sz_astros):
        x = float(input('Digite a posição (x,y):'))
        y = float(input())
        m = float(input('Digite a massa:'))
        r = float(input('Digite o raio:'))

        astros.append(Astro(x, y, m, r, i))

    '''
    print(Naves)
    for i in range(sz_naves):
       print(Naves[i].pos, Naves[i].vel, Naves[i].radius, Naves[i].id)
    print(Astros)
    for i in range(sz_astros):
        print(Astros[i].pos, Astros[i].mass, Astros[i].radius, Astros[i].id)
    '''
    '''
    print("type of naves:", type(Naves))
    for nave in naves:
        print(type(nave), end=' ')
    print(end='\n')
    print("type of astros:", type(Astros))
    for astro in astros:
        print(type(astro), end=' ')
    print(end='\n')
    '''
    eprint(naves)
    eprint(astros)

    simulacao(naves, astros, niter, delta_t)


if __name__ == '__main__':
    main()
