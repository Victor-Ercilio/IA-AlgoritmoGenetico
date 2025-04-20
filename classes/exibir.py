import math


class Exibir:

    @staticmethod
    def timer_ns(title:str, total: int,  ver:bool=True, file=None) -> None:
        if file:
            print(f'{title}  {total}(nano seconds)  {(total/1e9):.4f} (seconds)', file=file)
        if ver:
            print(f'{title}  {total}(nano seconds)  {(total/1e9):.4f} (seconds)')
    

    @staticmethod
    def relative_time(title:str, total: int, parciais:dict[str,int],  ver:bool=True, file=None) -> None:
        precisao_min = 2
        valores = {}
        for key in parciais:
            valores[key] = parciais[key]/total
            precisao = math.ceil(abs(math.log10(valores[key])))
            if precisao > precisao_min:
                precisao_min = precisao
        
        parcial = ''
        for key in parciais:
            parcial += f'{valores[key]:.{precisao_min}%} ({key})   '
        
        if file:
            print(f'{title} {parcial}', file=file)
        if ver:
            print(f'{title} {parcial}')
            