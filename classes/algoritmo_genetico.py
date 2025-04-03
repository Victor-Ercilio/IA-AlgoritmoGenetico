from collections.abc import Callable
from typing import Union
from .cromossomo import Cromossomo
from enums.metodos_selecao import Selecao


Populacao = list[Cromossomo]
FuncAptidao = Callable[[Cromossomo], Union[float, int]]


class AlgoritmoGenetico:

    def __init__(self,
                 tamanho_bits:int, 
                 populacao:Populacao, 
                 total_geracoes:int, 
                 total_individuos_por_geracao:int,
                 func_aptidao:FuncAptidao,
                 taxa_crossover:float,
                 taxa_mutacao:float,
                 tipo_selecao: Selecao
                ):
        self.bits = tamanho_bits
        self.pop = populacao
        self.pop_intermediaria: list[Cromossomo] = []
        self.geracao = 0
        self.total_geracoes = total_geracoes
        self.N = total_individuos_por_geracao
        self.aptidao = func_aptidao
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao
        self.tipo_selecao = tipo_selecao


    def __str__(self):
        header = f"""
                {'População Inicial' if self.geracao == 0 else f'Geração {self.geracao:02}'}
        {self.__formato_header().format('Posição', 'Cromossomo', 'Valor', 'Aptidão', 'Apt. Acumulada')}
        """
        body = """"""
        forma = self.__formato_body()
        for i, cr in enumerate(self.pop):
            line = forma.format(i, str(cr[0]), cr[0].valor, cr[0].aptidao, cr[1])
            body += f"""
        {line}\n"""
    

        return header + '\n' + body


    def __iter__(self):
        return self
    

    def __next__(self):
        if self.geracao >= self.total_geracoes:
            raise StopIteration
        self.geracao += 1
        self.selecionar_populacao()
        self.realizar_crossover()
        self.realizar_mutacao()
        self.avaliar_populacao()
        return self
    
    
    def iniciar_populacao(self):
        if not self.pop:
            self.pop = []
        for _ in range(self.N):
            self.pop.append(Cromossomo.getrandom(self.bits, self.taxa_mutacao))


    def avaliar_populacao(self):
        if self.tipo_selecao == Selecao.ROLETA:
            total = 0.0
            for cromossomo in self.pop:
                aptidao = self.aptidao(cromossomo)
                cromossomo.aptidao = aptidao
                total += aptidao
        elif self.tipo_selecao == Selecao.TORNEIO:
            pass
        elif self.tipo_selecao == Selecao.ORDEM:
            pass
        else:
            if self.tipo_selecao not in Selecao:
                raise NotImplementedError('tipo de seleção desconhecida')
            else:
                raise NotImplementedError('tipo de seleção não implementada')


    def selecionar_populacao(self):
        pass


    def realizar_crossover(self):
        pass
    

    def realizar_mutacao(self):
        for cromossomo in  self.pop_intermediaria:
            cromossomo.aplicar_mutacao()


    def __formato_header(self) -> str:
        tam_n = len(str(self.N))
        posicao = f'{{:^{tam_n if tam_n >= 8 else 8}}}'
        cromossomo = f'{{:^{self.bits+4 if self.bits+4 >= 12 else 12}}}'
        valor = '{:^10}'
        aptidao = '{:^10}'
        aptidao_acum = '{:^13}'

        return f'{posicao}{cromossomo}{valor}{aptidao}{aptidao_acum}'


    def __formato_body(self) -> str:
        tam_n = len(str(self.N))
        posicao = f'{{:^{tam_n if tam_n >= 8 else 8}}}'
        cromossomo = f'{{:^{self.bits+4 if self.bits+4 >= 12 else 12}}}'
        valor = '{:^10.2f}'
        aptidao = '{:^10.2f}'
        aptidao_acum = '{:^13.2f}'

        return f'{posicao}{cromossomo}{valor}{aptidao}{aptidao_acum}'
    
