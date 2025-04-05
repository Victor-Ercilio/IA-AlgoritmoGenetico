from random import randrange, random
from enum import Enum
import string, itertools, math


class Via(Enum):
    UNICA = 1
    DUPLA = 2


class Custo(Enum):
    MAXIMIZAR = 1
    MINIMIZAR = 2


VIA = Via.UNICA
TOTAL_CIDADES = 5
CIDADES = string.ascii_uppercase[:TOTAL_CIDADES]
ORIGEM = CIDADES[0]


class Rotas:

    def __init__(self, rota:str, custo:float=0.0, custo_proporcional:float=0.0, nota:float=0.0, nota_proporcional:float=0.0):
        self.rota = rota
        self.custo = custo
        self.custo_prop = custo_proporcional
        self.nota = nota
        self.nota_prop = nota_proporcional

    
    def __str__(self):
        return self.rota
    

    def __repr__(self):
        return f'Rota({self.rota}, {self.custo}, {self.custo_prop})'
    

    def aplicar_mutacao(self, taxa: float):
        cidades = self.rota[1:len(self.rota)-1]

        if len(cidades) > 1:
            for i in range(len(cidades)):
                if random() < taxa:
                    atual = cidades[i]
                    outras = cidades.replace(cidades[i], '') 
                    index_outra = randrange(len(outras))
                    outra = outras[index_outra]

                    cidades = cidades.replace(atual, '.')
                    cidades = cidades.replace(outra, ',')
                    
                    cidades = cidades.replace('.', outra)
                    cidades = cidades.replace(',', atual)
        
        self.rota = self.rota[0] + cidades + self.rota[-1]


def calcular_custo_entre_cidades(rota: str) -> int:
    if TOTAL_CIDADES == 3 and VIA == Via.DUPLA:
        match rota:
            case "AB": return 1
            case "AC": return 4
            case "BA": return 5 
            case "BC": return 2 
            case "CA": return 3 
            case "CB": return 1
            case _: ValueError(f'rota entre cidades ({rota}) desconhecida')
    
    if TOTAL_CIDADES == 4:
        raise NotImplementedError('funcão custo para 4 cidades não implementado')

    if TOTAL_CIDADES == 5 and VIA == Via.UNICA:
        match rota:
            case "AB" | "BA": return 2
            case "AC" | "CA": return 7
            case "AD" | "DA": return 8
            case "AE" | "EA": return 4
            case "BC" | "CB": return 6
            case "BD" | "DB": return 8
            case "BE" | "EB": return 4
            case "CD" | "DC": return 5
            case "CE" | "EC": return 6
            case "DE" | "ED": return 7
            case _: ValueError(f'rota entre cidades ({rota}) desconhecida')
        
    if TOTAL_CIDADES == 5 and VIA == Via.DUPLA:
        match rota:
            case "AB": return 4
            case "BA": return 3
            case "AC": return 8 
            case "CA": return 6
            case "AD": return 2
            case "DA": return 7
            case "AE": return 6 
            case "EA": return 5
            case "BC": return 6 
            case "CB": return 1
            case "BD": return 9 
            case "DB": return 4
            case "BE": return 9 
            case "EB": return 7
            case "CD": return 5 
            case "DC": return 1
            case "CE": return 4 
            case "EC": return 8
            case "DE": return 3 
            case "ED": return 2
            case _: ValueError(f'rota entre cidades ({rota}) desconhecida')
    
    


def calcular_custo_caminho(caminho: str) -> int:
    if len(caminho) == 0:
        return 0
    if len(caminho) == 2:
        return calcular_custo_entre_cidades(caminho)
    return calcular_custo_entre_cidades(caminho[:2]) + calcular_custo_caminho(caminho[1:])


def gerar_caminho():
    cidades = [c for c in CIDADES.replace(ORIGEM, '') ]
    caminho = ''

    while len(cidades) > 0:
        caminho += cidades.pop(randrange(len(cidades)))
    
    return ORIGEM + caminho + ORIGEM


def avaliar_rotas(rotas: list[Rotas]):
    """
    Calcula o custo individual de cada rota e guarda a de maior custo.
    A de maior custo servirá para inverter a pontuação, ou seja, até o momento,
    as rotas mais custosas tem maior pontuação, após a inverção a de maior custo
    terá custo 1 enquanto a de menor terá um custo alto. Entenda o custo como
    uma nota, a melhor rota tem menor custo e por isso uma nota mais alta.
    """
    total: int = 0
    maior_custo: int = 0

    for r in rotas:
        r.custo = calcular_custo_caminho(r.rota)
        if r.custo > maior_custo:
            maior_custo = r.custo
    
    maior_custo += 1
    for r in rotas:
        r.custo = maior_custo - r.custo
        total += r.custo

    # pot = math.floor(math.log10(total)) - 1
    for r in rotas:
        r.custo_prop = r.custo / total
        # r.custo_prop = total / (r.custo * 10**pot)
    
    rotas.sort(key=lambda rota: rota.custo)


def selecionar_rota(rotas: list[Rotas]) -> Rotas:
    aleatorio = random()
    total = 0

    for r in rotas:
        total += r.custo_prop
        if total >= aleatorio:
            return r


def crossover(rota_1: Rotas, rota_2: Rotas, corte: int=None) -> tuple[Rotas, Rotas]:
    if not corte:
        corte = randrange(len(rota_1.rota))
    ini1 = rota_1.rota[:corte]
    ini2 = rota_2.rota[:corte]
    fim1 = rota_1.rota[corte:]
    fim2 = rota_2.rota[corte:]

    if set(fim1) ^ set(fim2):
        dif = set(fim1) ^ set(fim2)
        set_i2f1, set_i1f2 = set(ini2) & set(fim1) & dif, set(ini1) & set(fim2) & dif
        set_dif_i2f1, set_dif_i1f2 = set_i2f1 ^ dif, set_i1f2 ^ dif

        while len(set_i2f1) > 0:
            ini2 = ini2.replace(set_i2f1.pop(), set_dif_i2f1.pop()) 
        while len(set_i1f2) > 0:
            ini1 = ini1.replace(set_i1f2.pop(), set_dif_i1f2.pop())
        
    return Rotas(ini1+fim2), Rotas(ini2+fim1)


def criar_prox_geracao(rotas: list[Rotas], taxa_mut: float, taxa_cros: float) -> list[Rotas]:
    rotas.sort(key=lambda rota: rota.custo, reverse=True)
    tamanho: int = len(rotas)
    prox_gercao:list[Rotas] = []

    # Elitismo - o melhor é copiado direto para próxima geração
    prox_gercao.append(rotas[0])

    while len(prox_gercao) < tamanho:
        r1, r2 = selecionar_rota(rotas), selecionar_rota(rotas)
        if random() <= taxa_cros:
            r1, r2 = crossover(r1, r2)
        r1.aplicar_mutacao(taxa_mutacao)
        r2.aplicar_mutacao(taxa_mutacao)
        prox_gercao.append(r1)
        prox_gercao.append(r2)
    
    return prox_gercao


def exibir_geracao(geracao: list[Rotas]) -> None:
    print(f'\t{"Rotas":^12}  {"Custo":^12}  {"Proporcao":^12}')
    for r in geracao:
        print(f'\t{r.rota:^12}  {r.custo:^12.2f}  {r.custo_prop:^12.2%}')


def exibir_custos_todas_rotas_possiveis(rotas: list[Rotas]) -> None:
    # Todas as rotas possíveis
    rotas = [ORIGEM + ''.join(r) + ORIGEM for r in itertools.permutations(CIDADES.replace(ORIGEM, ''))]
    rotas_custos = [ (r, calcular_custo_caminho(r)) for r in rotas ]
    rotas_custos.sort(key=lambda r: r[1])

    for i in rotas_custos:
        print(f'\t{i[0]}\t{i[1]}')


if __name__ == '__main__':
    try:
        print('-'*20, 'INICIO DO PROGRAMA', '-'*20)
        qtd_rotas: int = 8
        rotas: list[Rotas] = [ Rotas(gerar_caminho()) for _ in range(qtd_rotas) ]
        avaliar_rotas(rotas)
        geracoes: int = 4
        geracao = 0
        taxa_mutacao = 0.001
        taxa_crossover = 0.7

        print('\nPopulação Inicial')
        exibir_geracao(rotas)
        while geracao < geracoes:
            geracao += 1
            
            rotas = criar_prox_geracao(rotas, taxa_mutacao, taxa_crossover)
            avaliar_rotas(rotas)

            print(f'Geração {geracao}')
            exibir_geracao(rotas)

        


    except Exception as e:
        raise e
    finally:
        print('-'*20, 'FIM PROGRAMA', '-'*20)



