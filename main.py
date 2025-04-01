from classes.algoritmo_genetico import AlgoritmoGenetico
from classes.bitstring import BitString
from classes.cromossomo import Cromossomo

def aptidao(c: Cromossomo) -> float:
    return str(c).count('1')


if __name__ == '__main__':
    tamanho = 5
    populacao_inicial = []
    geracoes = 1
    total_individuos = 10
    tx_cross = 0.1
    tx_muta = 0.0001
    

    AG = AlgoritmoGenetico(
        tamanho_bits=tamanho,
        populacao=populacao_inicial,
        total_geracoes=geracoes,
        total_individuos_por_geracao=total_individuos,
        func_aptidao=aptidao,
        taxa_crossover=tx_cross,
        taxa_mutacao=tx_muta,
        tipo_selecao='roleta'
    )

    AG.iniciar_populacao()
    AG.avaliar_populacao()
    print(AG)

    for geracao in AG:
        print(geracao)
        print('-'*60)

    # cr = Cromossomo(tamanho=5, bitstring=0b01101)

    # ct = (cr, 0.0)
    # forma = AG.formato_body()
    # print(forma)
    # print(forma.format(1,str(ct[0]), ct[0].valor, ct[0].aptidao, ct[1]))
    

        
