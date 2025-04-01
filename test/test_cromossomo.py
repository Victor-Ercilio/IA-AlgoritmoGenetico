import pytest
from classes.cromossomo import Cromossomo


@pytest.fixture
def tamanhoCromo():
    return 4


@pytest.fixture
def valorCromo():
    return 0b1001


@pytest.fixture
def novoCromo(tamanhoCromo, valorCromo):
    return Cromossomo(tamanho=tamanhoCromo, bitstring=valorCromo)


def test_criar_cromossomo_vazio_deve_funcionar():
    cr = Cromossomo()

    assert isinstance(cr, Cromossomo) == True, 'não retornou uma instancia de Cromossomo'


def test_criar_cromossomo_com_valor_e_tamanho_deve_funcionar(tamanhoCromo, valorCromo):
    cr = Cromossomo(tamanho=tamanhoCromo, bitstring=valorCromo)

    assert isinstance(cr, Cromossomo) == True, 'não retornou uma instancia de Cromossomo'
    assert cr.tamanho == tamanhoCromo, 'tamanho diferente do configurado'
    assert cr.valor == valorCromo, 'valor diferente do configurado'


def test_criar_cromossomo_com_tamanho_nulo_gera_erro():
    
    with pytest.raises(ValueError) as excinfo:
        Cromossomo(tamanho=0)

    assert excinfo.type is ValueError, 'não gerou erro de valor'

    
def test_getrandom_cromossomo_deve_funcionar(tamanhoCromo):
    cr = Cromossomo.getrandom(tamanhoCromo)

    assert isinstance(cr, Cromossomo) == True, 'não retornou uma instancia de Cromossomo'
    assert cr.tamanho == tamanhoCromo, 'tamanho diferente do configurado'
    assert isinstance(cr.valor, int) == True, 'valor tem tipo diferente de int'


def test_pode_realizar_operacao_or_bit_a_bit():
    cr1 = Cromossomo(bitstring=0b0011, tamanho=4)
    cr2 = Cromossomo(bitstring=0b1100, tamanho=4)
    esperado = Cromossomo(bitstring=0b1111, tamanho=4)
    
    resultado = cr1 | cr2

    assert isinstance(resultado, Cromossomo) == True, f'não retornou uma instancia de Cromossomo{type(resultado)}'
    assert resultado == esperado


def test_pode_realizar_operacao_xor_bit_a_bit():
    cr1 = Cromossomo(bitstring=0b0100, tamanho=4)
    cr2 = Cromossomo(bitstring=0b1000, tamanho=4)
    esperado = Cromossomo(bitstring=0b1100, tamanho=4)
    
    resultado = cr1 ^ cr2

    assert isinstance(resultado, Cromossomo) == True, f'não retornou uma instancia de Cromossomo{type(resultado)}'
    assert resultado == esperado


def test_pode_realizar_operacao_and_bit_a_bit():
    cr1 = Cromossomo(bitstring=0b1011, tamanho=4)
    cr2 = Cromossomo(bitstring=0b1100, tamanho=4)
    esperado = Cromossomo(bitstring=0b1000, tamanho=4)
    
    resultado = cr1 & cr2

    assert isinstance(resultado, Cromossomo) == True, f'não retornou uma instancia de Cromossomo: {type(resultado)}'
    assert resultado == esperado

def test_aplicar_mutacao_com_taxa_um_deve_alterar_todos_os_bits():
    taxa = 1.0
    bi = 0b0001
    bf = 0b1110
    cr = Cromossomo(tamanho=4, bitstring=bi, taxa_mutacao=taxa)

    cr.aplicar_mutacao()

    assert cr.valor == bf, f'mutação não alterou os valores de {bi} para {bf}'


def test_aplicar_mutacao_com_taxa_um_quarto_deve_alterar_alguns_bits():
    taxa = 0.3
    bi = 0b0001
    cr = Cromossomo(tamanho=4, bitstring=bi, taxa_mutacao=taxa)

    cr.aplicar_mutacao()

    assert cr.valor != bi, f'mutação não alterou os valores de {bi} para {cr.valor}'

