import random, fractions
from .bitstring import BitString

class Cromossomo(BitString):
    

    def __init__(self, tamanho=None, bitstring=None, aptidao=0.0, taxa_mutacao=0.0):
        super().__init__(bits=tamanho, valor=bitstring)
        self.aptidao = aptidao
        self.taxa_mutacao = taxa_mutacao


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
    def getrandom(cls, bits):
        bs = super().getrandom(bits)
        return Cromossomo(tamanho=bs.bits, bitstring=bs.valor)
    

    def aplicar_mutacao(self) -> None:
        fracao = fractions.Fraction(self.taxa_mutacao).limit_denominator()
        num_max = fracao.denominator / fracao.numerator
        novo_valor = ''

        for i in f'{super().__str__()}':
            if random.randrange(0, num_max) == 0:
                novo_valor += '1' if i == '0' else '0'
                continue
            novo_valor += i
        
        self.valor = int(novo_valor, base=2)
        self.aptidao = 0.0
    
