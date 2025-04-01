import random
import math
from collections.abc import Callable
from typing import Union


BitString = int
Aptidao = Union[int, float]
Cromossomo = tuple[BitString, Aptidao]
Populacao = list[Cromossomo]
FuncAptidao = Callable[[Cromossomo], Aptidao]


def aptidao(c: Cromossomo, bits: int) -> int:
    return bin(c[0]).count('1') / bits


def gerar_mascara_aleatoria_de_corte(bits: int) -> int:
    corte = random.randrange(1, bits-1)
    mascara = '0b' + '1'*corte + '0'*(bits-corte)
    return int(mascara, base=2)

    
def gerar_cromossomo(bits: int) -> Cromossomo:
    return random.getrandbits(bits), 0.0


def gerar_populacao(bits: int, tamanho: int) -> Populacao:
    return [gerar_cromossomo(bits) for _ in range(tamanho)]


def cortar_cromossomo(mascara: int, cromossomo: Cromossomo) -> int:
    bits = len(f'{mascara:b}')
    print('Realizando corte:')
    print(f'\tMascara (M):   \t{mascara:b}')
    print(f'\tCromossomo (C):\t{cromossomo[0]:0{bits}b}\n')
    
    resultado = (mascara | cromossomo[0]) ^ mascara
    print(f'\t(M OR C) XOR M\t{resultado:0{bits}b}\n')

    return resultado

def crossover(c1: Cromossomo, c2: Cromossomo, bits: int) -> tuple[Cromossomo, Cromossomo]:
    print('Realizando o crossover')
    mascara = gerar_mascara_aleatoria_de_corte(bits)

    c1_f = cortar_cromossomo(mascara, c1)
    c2_f = cortar_cromossomo(mascara, c2)
    
    f1 = (c1[0] & mascara) | c2_f
    f2 = (c2[0] & mascara) | c1_f
    print(f'Filho 1: {f1:0{bits}b}')
    print(f'Filho 2: {f2:0{bits}b}')

    return f1, f2


def realizar_mutacao(c: int, taxa: float, bits: int) -> int:
    binario = f'{c:0{bits}b}'
    mudado = ''
    pot = int(abs(math.log10(taxa)))
    max_valor = int((10**pot)/(taxa*10**pot))
    for i in binario:
        if random.randrange(1,max_valor) == 1:
            print('realizando mutacao')
            mudado += '1' if i == '0' else '0'
            continue
        mudado += str(i)

    return int(mudado, base=2)


def avaliar_populacao(p: Populacao, f: FuncAptidao, bits: int) -> Populacao:
    return [ (c[0], f(c, bits)) for c in p ]


def selecionar_pela_roleta(p: Populacao) -> Cromossomo:
    pass




if __name__ == '__main__':
    BITS, TAM = 30, 6    
    TOT_GERACOES = 10
    TAXA_MUT = 0.0001

    pop = gerar_populacao(BITS, TAM)
    print(f'População: {pop}')

    pop_av  = avaliar_populacao(pop, aptidao, BITS)
    print(f'População avaliada: {pop_av}')

    geracao = 1
    # while geracao < TOT_GERACOES:
    #     geracao += 1
    #     selecionar_
    for i in range(len(pop_av)-1):
        f1, f2 = crossover(pop_av[i], pop_av[i+1], BITS)
        m1 = realizar_mutacao(f1, TAXA_MUT, BITS)
        m2 = realizar_mutacao(f2, TAXA_MUT, BITS)
        if f1 != m1:
            print(f'Mutacao {i}: {f1:0{BITS}b}')
            print(f'Mutacao {i}: {m1:0{BITS}b}')
        if f2 != m2:
            print(f'Mutacao {i}: {f2:0{BITS}b}')
            print(f'Mutacao {i}: {m2:0{BITS}b}')
