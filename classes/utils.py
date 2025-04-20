from random import randrange
from fractions import Fraction


class Utils:
    """
    Funções úteis que não têm uma área particular ou contexto específico.
    """

    @staticmethod
    def realizar_operacao(taxa: float) -> bool:
        """
        Retorna se uma operação qualquer deve ser realizada
        com base em sua frequência de execução.
        :taxa: float entre 0 e 1

        Ex: se uma função precisa ser executada aleatoriamente em 
        30% das vezes que é chamada, sua taxa é de 0.3.
        Um número aleatório é escolhido de 0 até 9 (10-1) e se for
        menor que 3 então é retornado True, se não False.
        """
        if taxa < 0 or taxa > 1:
            raise ValueError(f'Taxa ({taxa}) fora do intervalo [0,1]')

        fr = Fraction(taxa).limit_denominator()
        return randrange(fr.denominator) < fr.numerator


    @staticmethod
    def eh_impar(numero: int) -> bool:
        """
        Retorna se um número inteiro é ímpar.
        """
        return numero % 2 != 0
