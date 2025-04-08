from random import randrange, random
from enum import Enum
import string, itertools, fractions


class Via(Enum):
    UNICA = 1
    DUPLA = 2


class Custo(Enum):
    MAXIMIZAR = 1
    MINIMIZAR = 2


CUSTO = Custo.MINIMIZAR
VIA = Via.DUPLA

# Máximo 52, exceto 4 que não foi implementado ainda
TOTAL_CIDADES = 5
CIDADES = (string.ascii_uppercase+string.ascii_lowercase)[:TOTAL_CIDADES]
ORIGEM = CIDADES[0]


def realizar_operacao(taxa: float) -> bool:
    """
    Retorna se uma operação qualquer deve ser realizada
    com base em sua frequência de execução.
    :taxa: float entre 0 e 1

    Ex: se uma função precisa ser executada aleatoriamente em 
    30% das vezes que é chamada, sua taxa é de 0.3.
    """
    if taxa < 0 or taxa > 1:
        raise ValueError

    fr = fractions.Fraction(taxa).limit_denominator()
    return randrange(fr.denominator) < fr.numerator


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
        return f'Rota({self.rota}, {self.custo}, {self.custo_prop}, {self.nota}, {self.nota_prop})'
    

    def copy(self):
        return Rotas(self.rota, self.custo, self.custo_prop, self.nota, self.nota_prop)
    

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
    
    if TOTAL_CIDADES > 5 and VIA == Via.UNICA:
        return 1 if rota in CIDADES else 2

    if TOTAL_CIDADES > 5 and VIA == Via.DUPLA:
        if rota in CIDADES:
            return 1
        elif rota in CIDADES[::-1]:
            return 2
        else:
            return 3


def calcular_custo_caminho(caminho: str) -> int:
    if len(caminho) < 2:
        raise ValueError('caminho inválido, mínimo 2 cidades')
    
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
        total += r.custo
        if r.custo > maior_custo:
            maior_custo = r.custo
    
    for r in rotas:
        r.custo_prop = r.custo / total

    if CUSTO == Custo.MINIMIZAR:
        total = 0
        maior_nota = 0
        for r in rotas:
            r.nota = maior_custo - r.custo
            if r.nota > maior_nota:
                maior_nota = r.nota
        
        for r in rotas:
            r.nota = (r.nota * 10.0) / maior_nota
            total += r.nota
        
        for r in rotas:
            r.nota_prop = r.nota / total
        
        rotas.sort(key=lambda rota: rota.nota, reverse=True)

    else:
        for r in rotas:
            r.nota = (r.custo * 10.0) / maior_custo

        rotas.sort(key=lambda rota: rota.custo, reverse=True)   


def selecionar_rota(rotas: list[Rotas]) -> Rotas:
    aleatorio = random()
    total = 0

    for r in rotas:
        total += r.custo_prop if CUSTO == Custo.MAXIMIZAR else r.nota_prop
        if total >= aleatorio:
            return r


def crossover(rota_1: Rotas, rota_2: Rotas, corte: int=None) -> tuple[Rotas, Rotas]:
    if not corte:
        corte = randrange(1,len(rota_1.rota)-1)
    ini1 = rota_1.rota[:corte]
    ini2 = rota_2.rota[:corte]
    fim1 = rota_1.rota[corte:]
    fim2 = rota_2.rota[corte:]

    if set(fim1) ^ set(fim2):
        cidades_dif = set(fim1) ^ set(fim2)
        set_i2f1, set_i1f2 = set(ini2) & set(fim1) & cidades_dif, set(ini1) & set(fim2) & cidades_dif
        set_dif_i2f1, set_dif_i1f2 = set_i2f1 ^ cidades_dif, set_i1f2 ^ cidades_dif

        while len(set_i2f1) > 0:
            ini2 = ini2.replace(set_i2f1.pop(), set_dif_i2f1.pop()) 
        while len(set_i1f2) > 0:
            ini1 = ini1.replace(set_i1f2.pop(), set_dif_i1f2.pop())
        
    return Rotas(ini1+fim2), Rotas(ini2+fim1)


def criar_prox_geracao(rotas: list[Rotas], taxa_mut: float, taxa_cros: float) -> list[Rotas]:
    if CUSTO == Custo.MAXIMIZAR:
        rotas.sort(key=lambda rota: rota.custo, reverse=True)
    else:
        rotas.sort(key=lambda rota: rota.custo)

    tamanho: int = len(rotas)
    prox_gercao:list[Rotas] = []

    # Elitismo - o melhor é copiado direto para próxima geração
    prox_gercao.append(rotas[0].copy())

    while len(prox_gercao) < tamanho:
        r1, r2 = selecionar_rota(rotas), selecionar_rota(rotas)
        if random() <= taxa_cros:
            r1, r2 = crossover(r1, r2)
        r1.aplicar_mutacao(taxa_mut)
        r2.aplicar_mutacao(taxa_mut)
        prox_gercao.append(r1)
        prox_gercao.append(r2)
    
    return prox_gercao


def get_cabecalho(tamanho: int) -> str:
    if CUSTO == Custo.MAXIMIZAR:
        return f'\t{"Rotas":^{tamanho}}  {"Custo":^{tamanho}}  {"Proporção Custo":^{tamanho}}'
    return f'\t{"Rotas":^{tamanho}}  {"Custo":^{tamanho}}  {"Proporção Custo":^{tamanho}}  {"Nota":^{tamanho}}  {"Proporção Nota":^{tamanho}}'


def get_formato_corpo(tamanho: int) -> str:
    if CUSTO == Custo.MAXIMIZAR:
        return f'\t{{:^{tamanho}}}  {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}'
    return f'\t{{:^{tamanho}}} {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}  {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}'


def exibir_geracao(geracao: list[Rotas]) -> None:
    tam = 16
    forma = get_formato_corpo(tam)
    print(get_cabecalho(tam))
    for r in geracao:
        print(forma.format(r.rota, r.custo, r.custo_prop, r.nota, r.nota_prop))


def exibir_problema(taxa_mutacao:float, taxa_crossover:float, total_rotas:int, geracoes:int) -> None:
    print(f"""
    Parâmetros
    Tipo problema: {CUSTO}
    Quantidade de cidades: {TOTAL_CIDADES}
    Cidades: {CIDADES}
    Via: {VIA}

    Gerações: {geracoes}
    Taxa mutação: {taxa_mutacao:.2%}
    Taxa crossover: {taxa_crossover:.2%}
    Quantidade de rotas por geração: {total_rotas+1}

    """)


def exibir_melhores_resultados(melhores: list[tuple[int, Rotas]]) -> None:
    tam = 16
    forma = get_formato_corpo(tam)
    linhas = ''
    geracao = '\tGeração'
    for i in melhores:
        linhas += f'{geracao:>{len(geracao)}} {i[0]}  {forma.format(i[1].rota, i[1].custo, i[1].custo_prop, i[1].nota, i[1].nota_prop)}\n'

    print(f"""
    Melhores Resultados
    {"":{len(geracao)}}\t{get_cabecalho(tam)}
    {linhas}
    """)


def exibir_populacao_incial(rotas: list[Rotas]) -> None:
    print('\nPopulação Inicial')
    exibir_geracao(rotas)


def exibir_custos_todas_rotas_possiveis(rotas: list[Rotas]) -> None:
    # Todas as rotas possíveis
    rotas = [ORIGEM + ''.join(r) + ORIGEM for r in itertools.permutations(CIDADES.replace(ORIGEM, ''))]
    rotas_custos = [ (r, calcular_custo_caminho(r)) for r in rotas ]
    rotas_custos.sort(key=lambda r: r[1])

    for i in rotas_custos:
        print(f'\t{i[0]}\t{i[1]}')


if __name__ == '__main__':
    try:
        print('-'*50, 'INICIO DO PROGRAMA', '-'*50)

        qtd_rotas: int = 8
        geracoes: int = 4
        geracao: int = 0
        taxa_mutacao: float = 0.001
        taxa_crossover: float = 0.7
        melhores_resultados: list[tuple[int, Rotas]] = []

        exibir_problema(taxa_mutacao, taxa_crossover, qtd_rotas, geracoes)

        rotas: list[Rotas] = [ Rotas(gerar_caminho()) for _ in range(qtd_rotas) ]
        avaliar_rotas(rotas)
        exibir_populacao_incial(rotas)
        while geracao < geracoes:
            geracao += 1

            rotas = criar_prox_geracao(rotas, taxa_mutacao, taxa_crossover)
            avaliar_rotas(rotas)

            melhores_resultados.append((geracao, rotas[0].copy()))
            print(f'Geração {geracao}')
            exibir_geracao(rotas)

        exibir_melhores_resultados(melhores_resultados)

    except Exception as e:
        print(f'Erro: {e}')
    finally:
        print('-'*50, 'FIM PROGRAMA', '-'*50)
