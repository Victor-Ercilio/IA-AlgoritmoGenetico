from random import randrange

from classes.utils import Utils
from classes.contador import Contador


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
                if Utils.realizar_operacao(taxa):
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
