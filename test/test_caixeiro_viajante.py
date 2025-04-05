from exemplos.caixeiro_viajante import *
import pytest

def test_gerar_caminho_retorna_string_cidades_menos_origem():
    s = gerar_caminho()

    assert len(s) == TOTAL_CIDADES+1, f'tamanho do caminho ({len(s)}) diferente de ({CIDADES-1})'
    assert s.startswith(ORIGEM), f'cidade de origem não inclusa no começo caminho {s}'
    assert s.endswith(ORIGEM), f'cidade de origem não inclusa no fim caminho {s}'
    assert (set(s.replace(ORIGEM, '')) ^ set(CIDADES)) == set(ORIGEM), 'nem todas as cidades foram inclusas {s}'


def test_gerar_caminho_duas_vezes_consecutivas_deve_gerar_caminhos_diferentes():
    assert gerar_caminho() != gerar_caminho(), 'caminhos iguais'


@pytest.mark.parametrize(
        'caminho, custo',
        [
            ('ABC', 5),
            ('ABCDEA', 21),
            ('ACDEBA', 19)
        ]
)
def test_calcular_custo_caminho_deve_funcionar(caminho, custo):
    calculado = calcular_custo_caminho(caminho)

    assert  calculado == custo, f'custo calculado {calculado} diferente de esperado {custo}'


def test_avaliar_custo_rotas():
    rotas = [Rotas('AEC'), Rotas('ABC')]
    custos_calc = calcular_custo_caminho(rotas[0].rota), calcular_custo_caminho(rotas[1].rota)
    maior_custo = custos_calc[0] if custos_calc[0] > custos_calc[1] else custos_calc[1]
    custos_finais = maior_custo - custos_calc[0], maior_custo - custos_calc[1]
    porporcao = custos_finais[0] / sum(custos_finais), custos_finais[1] / sum(custos_finais) 

    avaliar_rotas(rotas)

    assert rotas[0].custo == custos_finais[0], f'custos diferentes {rotas[0].custo} <> {custos_finais[0]}'
    assert rotas[1].custo == custos_finais[1], f'custos diferentes {rotas[1].custo} <> {custos_finais[1]}'
    assert rotas[0].custo_prop == porporcao[0], f'proporcão diferente {rotas[0].custo_prop} <> {porporcao[0]}'
    assert rotas[1].custo_prop == porporcao[1], f'proporcão diferente {rotas[1].custo_prop} <> {porporcao[1]}'


def test_aplicar_mutaco():
    rota = 'ABCDEF'
    r = Rotas(rota)

    r.aplicar_mutacao(1)

    assert rota != r.rota, f'mutacao nao alterou rota {rota} <> {r.rota}'

@pytest.mark.parametrize(
        'caminho1, caminho2, corte, fim1, fim2',
        [
            ('ABCDEA', 'ABCEDA', 3, 'EDA', 'DEA'),
            ('ABCDEA', 'AEDCBA', 3, 'CBA', 'DEA')
        ]
)
def test_crossover_entre_ciades(caminho1, caminho2, corte, fim1, fim2):
    r1, r2 = crossover(Rotas(caminho1), Rotas(caminho2), corte)

    assert r1.rota.endswith(fim1), f'final diferente {r1.rota} <> {fim1}' 
    assert r2.rota.endswith(fim2), f'final diferente {r2.rota} <> {fim2}' 