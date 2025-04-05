import random

class BitString:


    def __init__(self, bits:int=None, valor:int=None, param:dict[str,int]=None):
        if bits <= 0:
            raise ValueError
        
        self.bits: int = bits
        self.valor: int = valor
        self.param: dict = param
        self.next: BitString = None


    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.bits}, {bin(self.valor)})'


    def __str__(self):
        return f'{self.valor:0{self.bits}b}'


    def __getitem__(self, index) -> int:
        if index < 0 or index >= self.bits:
            raise IndexError('indice fora do intervalo')
        
        return 0 if (self.valor & (1 << index)) == 0 else 1


    def __setitem__(self, index, value) -> None:
        if index < 0 or index >= self.bits:
            raise IndexError('indice fora do intervalo')
        
        if value == 1:
            self.valor |= (1 << index)
        else:
            self.valor -= self[index] * 2**index


    def __eq__(self, value) -> bool:
        if isinstance(value, BitString):
            return self.valor == value.valor
        if isinstance(value, int):
            return self.valor == value
        
        raise TypeError(f'Tipo {value.__class__.__name__} não suportado')
    

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


    def __add__(self, other):
        pass


    @classmethod
    def getrandom(cls, bits):
        return BitString(valor=random.getrandbits(bits), bits=bits)
        