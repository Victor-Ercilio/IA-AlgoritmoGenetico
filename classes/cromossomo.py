import random, fractions
from .bitstring import BitString

class Cromossomo(BitString):
    

    def __init__(self, tamanho=None, valor=None, aptidao=0.0, taxa_mutacao=0.0):
        super().__init__(bits=tamanho, valor=valor)
        self.taxa_mutacao: float = taxa_mutacao
        self.aptidao: float = aptidao


    def __xor__(self, other):
        if isinstance(other, Cromossomo):
            bs = super().__xor__(other)
            return Cromossomo(tamanho=bs.bits, bitstring=bs.valor)
    

    def __or__(self, other):
       if isinstance(other, Cromossomo):
            bs = super().__or__(other)
            return Cromossomo(tamanho=bs.bits, bitstring=bs.valor)
       
    
    def __and__(self, other):
        if isinstance(other, Cromossomo):
            bs = super().__and__(other)
            return Cromossomo(tamanho=bs.bits, bitstring=bs.valor)
    

    @property
    def tamanho(self):
        return self.bits
    

    @classmethod
    def getrandom(cls, bits, taxa_mutacao=0.0):
        bs = super().getrandom(bits)
        return Cromossomo(tamanho=bs.bits, bitstring=bs.valor, taxa_mutacao=taxa_mutacao)
    
    
    @classmethod
    def getpopulacao(cls, tamanho: int, bits: int, taxa_mutacao: float):
        if tamanho < 0 or bits < 0:
            raise ValueError('tamanho da população ou da quantidade de bits não pode ser negativo')
        
        return [cls.getrandom(bits, taxa_mutacao=taxa_mutacao) for _ in range(tamanho)]
    

    def aplicar_mutacao(self) -> None:
        fracao = fractions.Fraction(self.taxa_mutacao).limit_denominator()
        num_max = int(fracao.denominator / fracao.numerator)

        for i in range(self.tamanho):
            if random.randrange(0, num_max) == 0:
                self[i] = 1 if self[i] == 0 else 0
                
        self.aptidao = 0.0
