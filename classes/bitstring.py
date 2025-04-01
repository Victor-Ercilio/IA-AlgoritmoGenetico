import random

class BitString:


    def __init__(self, bits:int=None, valor:int=None, param:dict[str,int]=None):
        self.bits = bits
        self.valor = valor
        self.param = param
        self.next = None


    def __eq__(self, value) -> bool:
        if isinstance(value, BitString):
            return self.valor == value.valor
        if isinstance(value, int):
            return self.valor == value
        raise TypeError(f'Tipo {value.__class__.__name__} não suportado')


    def __repr__(self):
        return bin(self.valor)


    def __str__(self):
        return f'{self.valor:0{self.bits}b}'
    

    def __xor__(self, other):
        if isinstance(other, BitString):
            return BitString(valor=(self.valor ^ other.valor), bits=self.bits)
        if isinstance(other, int):
            return self.valor | other
        raise TypeError(f'Tipo {other.__class__.__name__} não suportado')


    def __rxor__(self, other):
        return self | other
    

    def __and__(self, other):
        if isinstance(other, BitString):
            return BitString(valor=(self.valor & other.valor), bits=self.bits)
        if isinstance(other, int):
            return self.valor | other
        raise TypeError(f'Tipo {other.__class__.__name__} não suportado')
    

    def __rand__(self, other):
        return self | other
    

    def __or__(self, other):
        if isinstance(other, BitString):
            return BitString(valor=(self.valor | other.valor), bits=self.bits)
        if isinstance(other, int):
            return self.valor | other
        raise TypeError(f'Tipo {other.__class__.__name__} não suportado')
    

    def __ror__(self, other):
        return self | other

    @classmethod
    def getrandom(cls, bits):
        return BitString(valor=random.getrandbits(bits), bits=bits)
        