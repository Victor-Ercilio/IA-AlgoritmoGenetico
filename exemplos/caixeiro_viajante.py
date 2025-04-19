from random import randrange, random
from enum import Enum
import string
import itertools
import functools
import fractions
import os, sys, time, math
import multiprocessing as mp


class Processamento(Enum):
    SINGLE_CORE = 1
    MULTI_CORE = 2


class Via(Enum):
    UNICA = 1
    DUPLA = 2


class Custo(Enum):
    MAXIMIZAR = 1
    MINIMIZAR = 2


CUSTO = Custo.MINIMIZAR
VIA = Via.DUPLA

# Máximo 52, exceto 4 que não foi implementado ainda
TOTAL_CIDADES = 15
CIDADES = (string.ascii_uppercase+string.ascii_lowercase)[:TOTAL_CIDADES]
ORIGEM = CIDADES[0]


def realizar_operacao(taxa: float) -> bool:
    """
    Retorna se uma operação qualquer deve ser realizada
    com base em sua frequência de execução.
    :taxa: float entre 0 e 1

    Ex: se uma função precisa ser executada aleatoriamente em 
    30% das vezes que é chamada, sua taxa é de 0.3 ou 3/10.
    Um número aleatório é escolhido de 0 até 9 (10-1) e se for
    menor que 3 então é retornado verdadeiro.
    """
    if taxa < 0 or taxa > 1:
        raise ValueError

    fr = fractions.Fraction(taxa).limit_denominator()
    return randrange(fr.denominator) < fr.numerator


class Contador:

    def __init__(self):
        self.mutacoes = 0
        self.crossovers = 0
        self.total_mut = 0
        self.total_cros = 0
        self.generacao_timer = 0
        self.total_generacao_timer = 0
        self.crossover_timer = 0
        self.total_crossover_timer = 0
        self.mutacao_timer = 0
        self.total_mutacao_timer = 0
        self.selecao_timer = 0
        self.total_selecao_timer = 0
        self.timer = 0
    

    def mutacao(self, n:int=1) -> None:
        self.mutacoes += n


    def crossover(self, n:int=1) -> None:
        self.crossovers += n


    def start_generation_timer(self):
        self.generacao_timer = time.monotonic()
    

    def end_generation_timer(self):
        self.generacao_timer = time.monotonic() - self.generacao_timer
    
    
    def start_timer(self):
        self.timer = time.monotonic()
    

    def end_timer(self):
        self.timer = time.monotonic() - self.timer
    
    
    def start_crossover_timer(self):
        self.crossover_timer = time.monotonic()
    

    def end_crossover_timer(self):
        self.crossover_timer = time.monotonic() - self.crossover_timer


    def start_mutacao_timer(self):
        self.mutacao_timer = time.monotonic()
    

    def end_mutacao_timer(self):
        self.mutacao_timer = time.monotonic() - self.mutacao_timer


    def start_selecao_timer(self):
        self.selecao_timer = time.monotonic()
    

    def end_selecao_timer(self):
        self.selecao_timer = time.monotonic() - self.selecao_timer


    def reset(self) -> None:
        self.total_mut += self.mutacoes
        self.total_cros += self.crossovers
        self.total_generacao_timer += self.generacao_timer
        self.total_selecao_timer += self.selecao_timer
        self.total_crossover_timer += self.crossover_timer
        self.total_mutacao_timer += self.mutacao_timer
        self.mutacoes = 0
        self.crossovers = 0
        self.generacao_timer = 0
        self.selecao_timer = 0
        self.crossover_timer = 0
        self.mutacao_timer = 0


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
    

    def aplicar_mutacao(self, taxa: float, contador: Contador=None):
        cidades = self.rota[1:len(self.rota)-1]

        if len(cidades) > 1:
            for i in range(len(cidades)):
                if realizar_operacao(taxa):
                    if contador:
                        contador.mutacao()
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


def resultado() -> str:
    if TOTAL_CIDADES == 4:
        raise NotImplementedError('função custo para 4 cidades não implementado')
    
    if CUSTO == Custo.MINIMIZAR:
        if TOTAL_CIDADES == 5 and VIA == Via.DUPLA:
            index = CIDADES.index(ORIGEM)
            return ORIGEM+CIDADES[:index:-1]+CIDADES[:index]+ORIGEM
        
        index = CIDADES.index(ORIGEM)
        return CIDADES[index:]+CIDADES[:index]+ORIGEM
    
    return ""


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
    Calcula o custo individual de cada rota e sua proporção
    com relação a de maior custo.
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
        
        if maior_nota == 0:
            for r in rotas:
                    r.nota = 10.0
        else:
            for r in rotas:
                r.nota = (r.nota * 10.0) / maior_nota
        
        total = sum([ r.nota for r in rotas ])
        
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
    if CUSTO == Custo.MAXIMIZAR:
        for r in rotas:
            total += r.custo_prop
            if total >= aleatorio:
                return r
    else:
        for r in rotas:
            total += r.nota_prop
            if total >= aleatorio:
                return r


def crossover(rota_1: Rotas, rota_2: Rotas, corte: int=None) -> tuple[Rotas, Rotas]:
    if not corte:
        corte = randrange(1,len(rota_1.rota)-1)
    ini1 = rota_1.rota[:corte]
    ini2 = rota_2.rota[:corte]
    fim1 = rota_1.rota[corte:]
    fim2 = rota_2.rota[corte:]

    cidades_duplicadas = set(fim1) ^ set(fim2)
    
    if cidades_duplicadas:
        cidades_a_substituir_i2f1 = set(ini2) & set(fim1) & cidades_duplicadas
        cidades_a_substituir_i1f2 = set(ini1) & set(fim2) & cidades_duplicadas
        
        cidades_substitutas_i2f1 = cidades_a_substituir_i2f1 ^ cidades_duplicadas
        cidades_substitutas_i1f2 = cidades_a_substituir_i1f2 ^ cidades_duplicadas

        while len(cidades_a_substituir_i2f1) > 0:
            ini2 = ini2.replace(cidades_a_substituir_i2f1.pop(), cidades_substitutas_i2f1.pop()) 
            
        while len(cidades_a_substituir_i1f2) > 0:
            ini1 = ini1.replace(cidades_a_substituir_i1f2.pop(), cidades_substitutas_i1f2.pop())
        
    return Rotas(ini1+fim2), Rotas(ini2+fim1)


def criar_prox_geracao(rotas: list[Rotas], taxa_mut: float, taxa_cros: float, contador: Contador=None) -> list[Rotas]:
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
        
        if realizar_operacao(taxa_cros):
            if contador:
                contador.crossover()
            r1, r2 = crossover(r1, r2)
        
        r1.aplicar_mutacao(taxa_mut, contador)
        r2.aplicar_mutacao(taxa_mut, contador)

        if (tamanho - len(prox_gercao)) >= 2:
            prox_gercao.append(r1)
            prox_gercao.append(r2)
        else:
            prox_gercao.append(r1 if realizar_operacao(0.5) else r2)

    return prox_gercao


def distribuir_trabalhos_igualmente(trabalhos: int, trabalhadores: int) -> list[int]:
    qtd_min_trabalho = math.floor(trabalhos/trabalhadores)
    resto = trabalhos - qtd_min_trabalho*trabalhadores
    distribuicao = []
    
    for i in range(trabalhadores):
        if resto > 0:
            distribuicao.append(qtd_min_trabalho + 1)
            resto -= 1
        else:
            distribuicao.append(qtd_min_trabalho)

    return distribuicao


def eh_impar(valor: int) -> bool:
    return valor % 2 != 0


def calcular_quantidade_crossovers(taxa:float, trabalhos:int, trabalhadores:int) -> int:
    quantidade = taxa * (trabalhos / 2)
    quantidade = math.floor(quantidade) if eh_impar(trabalhos) else math.ceil(quantidade)
    return quantidade


def mutacao(rota: Rotas, taxa:float, contador:Contador=None) -> Rotas:
    rota.aplicar_mutacao(taxa=taxa, contador=contador)
    return rota, contador


def criar_prox_geracao_mult_process(trabalhadores: int, rotas: list[Rotas], taxa_mut: float, taxa_cros: float, contador: Contador=None) -> list[Rotas]:
    if CUSTO == Custo.MAXIMIZAR:
        rotas.sort(key=lambda rota: rota.custo, reverse=True)
    else:
        rotas.sort(key=lambda rota: rota.custo)

    individuos: int = len(rotas)
    prox_geracao: list[Rotas] = []

    prox_geracao.append(rotas[0].copy())

    with mp.Pool(processes=trabalhadores) as pool:
        if contador:
            contador.start_selecao_timer()
        selecao_rotas_fixa = functools.partial(selecionar_rota, rotas=rotas)

        selecionados = pool.starmap(selecao_rotas_fixa, (tuple() for _ in range((individuos - len(prox_geracao)))) )
        if contador:
            contador.end_selecao_timer()

        for selecionado in selecionados:
            prox_geracao.append(selecionado)
        
        if contador:
            contador.start_crossover_timer()
        quantidade_crossovers = calcular_quantidade_crossovers(taxa_cros, individuos, trabalhadores)

        cruzados: list[tuple[Rotas, Rotas]] = pool.starmap(crossover, ((prox_geracao.pop(0), prox_geracao.pop(1)) for _ in range(quantidade_crossovers)))
        if contador:
            contador.crossover(quantidade_crossovers)
            contador.end_crossover_timer()

        for c1, c2 in cruzados:
            prox_geracao.append(c1)
            prox_geracao.append(c2)
        

        if contador:
            contador.start_mutacao_timer()
        mutados: list[tuple[Rotas, Contador]] = pool.starmap(mutacao, ((prox_geracao.pop(0), taxa_mut, Contador()) for _ in range(len(prox_geracao))) )
        if contador:
            contador.end_mutacao_timer()


        for individuo, cont in mutados:
            if contador:
                contador.mutacao(cont.mutacoes)
            prox_geracao.append(individuo)

    return prox_geracao


def hilight_resultado() -> str:
    return f'\033[92m{resultado()}\033[00m'


def get_cabecalho(tamanho: int) -> str:
    if CUSTO == Custo.MAXIMIZAR:
        return f'\t{{:^{{}}}}  {"Custo":^{tamanho}}  {"Proporção Custo":^{tamanho}}'
    return f'\t{{:^{{}}}}  {"Custo":^{tamanho}}  {"Proporção Custo":^{tamanho}}  {"Nota":^{tamanho}}  {"Proporção Nota":^{tamanho}}'


def get_formato_corpo(tamanho: int) -> str:
    if CUSTO == Custo.MAXIMIZAR:
        return f'\t{{:^{{}}}}  {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}'
    return f'\t{{:^{{}}}} {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}  {{:^{tamanho}.2f}}  {{:^{tamanho}.2%}}'


def get_cabecalho_melhores(tamanho: int):
    return f'\t{{:^{{}}}}  {"Custo":^{tamanho}}  {"Média Custo":^{tamanho}}  {"Crossovers":^{tamanho}}  {"Mutações":^{tamanho}}'


def get_formato_corpo_melhores(tamanho: int):
    return f'\t{{:^{{}}}} {{:^{tamanho}.2f}}  {{:^{tamanho}.2f}}  {{:^{tamanho}}}  {{:^{tamanho}}}'


def exibir_geracao(geracao: list[Rotas], file=None) -> None:
    tam = 16
    tam_rota = len(geracao[0].rota) + 2
    forma = get_formato_corpo(tam)
    print(get_cabecalho(tam).format("Rotas", tam_rota), file=file)
    for r in geracao:
        print(forma.format(r.rota, tam_rota, r.custo, r.custo_prop, r.nota, r.nota_prop), file=file)


def exibir_geracao_numero(tag: str, atual:int, total: int):
    """
    Exibe uma tag fixa e vai atualizando a numeração na mesma 
    linha de exibição.
    Utilizar quando a quantidade de gerações é muito grande e
    não se deseja ver cada individuo de cada geração, mas, sim,
    visualizar o progresso das gerações (em um terminal).
    """
    tam = len(str(total))
    limpa_num = '\b'*tam + ' '*tam + '\b'*tam
    
    tag = f'{tag} '
    limpa_tag = '\b'*len(tag) + ' '*len(tag) + '\b'*len(tag)

    intervalo = f' de {total}'
    voltar_intervalo = '\b'*len(intervalo)
    limpa_intervalo = ' '*len(intervalo) + voltar_intervalo

    if atual == 1:
        print(f'{tag}{(atual):0>{tam}}{intervalo}', end='', flush=True)
        print(voltar_intervalo, end='', flush=True)
    elif atual == total:
        print(f'{limpa_intervalo}{limpa_num}{limpa_tag}', end='\n', flush=True)
    else:
        print(f'{limpa_num}{(atual):0>{tam}}', end='', flush=True)


def exibir_problema(taxa_mutacao:float, taxa_crossover:float, total_rotas:int, geracoes:int, file=None) -> None:
    print(f"""
    Parâmetros
    Tipo problema: {CUSTO}
    Quantidade de cidades: {TOTAL_CIDADES}
    Cidades: {CIDADES}
    Via: {VIA}

    Gerações: {geracoes}
    Taxa mutação: {taxa_mutacao:.2%}
    Taxa crossover: {taxa_crossover:.2%}
    Quantidade de rotas por geração: {total_rotas}

    """, file=file)


def exibir_melhores_resultados(melhores: list[tuple[int, Rotas, float, int, int]], file=None) -> None:
    tam = 13
    tam_rota = len(CIDADES) + 3
    forma = get_formato_corpo_melhores(tam)
    linhas = ''
    label = '\tGeração'
    resposta = resultado()
    len_geracoes = len(str(len(melhores)))


    if file:
        for i in melhores:
            geracao, rota, media, qtd_cross, qtd_mut = i
            linhas += f'{label} {geracao:>{len_geracoes+1}}  {forma.format(rota.rota, tam_rota, rota.custo, media, qtd_cross, qtd_mut)}\n'
    else:
        for i in melhores:
            geracao, rota, media, qtd_cross, qtd_mut = i
            nome_rota = str(rota) if str(rota) != resposta else f'\033[92m{rota}\033[00m'
            linhas += f'{label} {geracao}  {forma.format(nome_rota, tam_rota, rota.custo, media, qtd_cross, qtd_mut)}\n'

    print(f"""
    Solução: {hilight_resultado() if not file else resultado()}  Custo: {calcular_custo_caminho(resultado())}

    Melhores Resultados
    {"":{len(label)}}\t{get_cabecalho_melhores(tam).format("Rotas", tam_rota)}

    {linhas}

    Total 
        Crossovers: {contador.total_cros}
        Mutações: {contador.total_mut}

    """, file=file)


def exibir_populacao_incial(rotas: list[Rotas], file=None) -> None:
    print('População Inicial', file=file)
    exibir_geracao(rotas, file=file)


def exibir_custos_todas_rotas_possiveis(rotas: list[Rotas], file=None) -> None:
    # Todas as rotas possíveis
    rotas = [ORIGEM + ''.join(r) + ORIGEM for r in itertools.permutations(CIDADES.replace(ORIGEM, ''))]
    rotas_custos = [ (r, calcular_custo_caminho(r)) for r in rotas ]
    rotas_custos.sort(key=lambda r: r[1])

    for i in rotas_custos:
        print(f'\t{i[0]}\t{i[1]}', file=file)


def executar_single_processor(rotas: list[Rotas], taxa_mutacao: float, taxa_crossover: float, contador: Contador):
    # start = time.perf_counter_ns()
    rotas = criar_prox_geracao(rotas, taxa_mutacao, taxa_crossover, contador)
    # print(f'Singleprocess {((time.perf_counter_ns()-start)/1e9):.2f} segundos')
    
    # start = time.perf_counter_ns()
    avaliar_rotas(rotas)
    # print(f'avaliar rota {(time.perf_counter_ns()-start)/1e9}')

    return rotas


def executar_mult_processor(trabalhadores:int, rotas: list[Rotas], taxa_mutacao: float, taxa_crossover: float, contador: Contador):
    # start = time.perf_counter_ns()
    rotas = criar_prox_geracao_mult_process(trabalhadores, rotas, taxa_mutacao, taxa_crossover, contador)
    # print(f'Multprocess {((time.perf_counter_ns()-start)/1e9):.2f} segundos')
    avaliar_rotas(rotas)
    return rotas


if __name__ == '__main__':
    try:
        terminal_size = os.get_terminal_size(sys.stdout.fileno()).columns
        print(f'{{:-^{terminal_size}}}'.format(' INICIO DO PROGRAMA '))
        multi_process = True
        cores = 2
        qtd_rotas: int = 3000
        geracoes: int = 50
        geracao: int = 0
        taxa_mutacao: float = 0.001
        taxa_crossover: float = 0.7
        melhores_resultados: list[tuple[int, Rotas, float, int, int]] = []
        contador: Contador = Contador()
        contador.start_timer()
        file_name = f'AG-Resultados-{"N_PROCESS" if multi_process else "SINGLE_PROCESS"}-{CUSTO.name}_{VIA.name}_C{TOTAL_CIDADES}_R{qtd_rotas}_G{geracoes}.txt'
        file = None

        # try:
            # file = open(file_name, 'x',encoding="utf-8")
        # except FileExistsError:
            # print(f'O arquivo {file_name}  já existe.')
            # file = None

        if file:
            print(f'\nSalvando em {file_name}')

        exibir_problema(taxa_mutacao, taxa_crossover, qtd_rotas, geracoes, file)

        rotas: list[Rotas] = [ Rotas(gerar_caminho()) for _ in range(qtd_rotas) ]
        avaliar_rotas(rotas)

        if qtd_rotas < 100:
            exibir_populacao_incial(rotas, file=file)
        while geracao < geracoes:
            geracao += 1
            contador.start_generation_timer()

            if multi_process:
                rotas = executar_mult_processor(cores, rotas, taxa_mutacao, taxa_crossover, contador)
            else:
                rotas = executar_single_processor(rotas, taxa_mutacao, taxa_crossover, contador)

            contador.end_generation_timer()
            media = sum([r.custo for r in rotas]) / len(rotas)
            melhores_resultados.append((geracao, rotas[0].copy(), media, contador.crossovers, contador.mutacoes))
            
            if geracoes < 10 and qtd_rotas < 20:
                print(f'Geração {geracao}', file=file)
                exibir_geracao(rotas, file=file)
            else:
                exibir_geracao_numero('\n\nGeração', geracao, geracoes)
            contador.reset()

        exibir_melhores_resultados(melhores_resultados, file=file)
        contador.end_timer()
        print(f'Tempo total decorrido: {contador.timer:.2f}s')
        print(f'Tempo total em seleção: {contador.total_selecao_timer:.2f}s')
        print(f'Tempo total em crossover: {contador.total_crossover_timer:.2f}s')
        print(f'Tempo total em mutação: {contador.total_mutacao_timer:.2f}s')

        print(f'Tempo médio de geraçoes: {(contador.total_generacao_timer/geracoes):.2f}s')

    except Exception as e:
        print(f'Erro: {e}')
        print(e)
    finally:
        if file:
            file.close()
        print(f'{{:-^{terminal_size}}}'.format(' FIM DO PROGRAMA '))
