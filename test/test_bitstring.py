import pytest
from classes.bitstring import BitString


@pytest.fixture
def quantidadeBits():
    return 4


@pytest.fixture
def valorBits():
    return 0b0110


@pytest.fixture
def bitStringComValor(quantidadeBits):
    return BitString(quantidadeBits)


@pytest.fixture
def bitStringComValor(valorBits, quantidadeBits):
    return BitString(valor=valorBits, bits=quantidadeBits)


def test_criar_bitstring_apenas_com_quantidade_bits_deve_funcionar():
    tamanho = 4

    bs = BitString(4)

    assert isinstance(bs, BitString) == True, 'não retornou uma instancia de BitString'
    assert bs.bits == tamanho, 'tamanho e quantidade de bits incompatíveis'

# Manter simples
@pytest.mark.skip
def test_criar_bitstring_com_parametros_deve_funcionar():
    parametros = {
        'a': 4,
        'b': 5
    }

    bs = BitString(parametros)

    assert bs.bits == 4+5, 'não retornou a quantidade de bits correta'


def test_criar_bitstring_com_bits_e_valor_deve_funcionar():
    tamanho = 4
    valor = 0b1011
    
    bs = BitString(bits=tamanho, valor=valor)

    assert isinstance(bs, BitString) == True, 'não retornou uma instancia de BitString'
    assert bs.bits == tamanho, 'quantidade de bits errada'
    assert bs.valor == valor, 'valor errado'
    assert bs == valor and valor == bs, 'operador de igualdade não funciona'


def test_get_random_deve_retornar_bitstring(quantidadeBits):
    bs = BitString.getrandom(quantidadeBits)

    assert isinstance(bs, BitString) == True, 'não retornou una instancia de BitString'
    assert bs.bits == quantidadeBits, 'não retornou a quantidade correta de bits'


def test_str_deve_retornar_uma_string_representando_os_bits(bitStringComValor, valorBits, quantidadeBits):
    string = bitStringComValor.__str__()

    assert string == f'{valorBits:0{quantidadeBits}b}', 'representação binária em string errada'


def test_pode_realizar_operacao_or_bit_a_bit():
    bs1 = BitString(valor=0b0011, bits=4)
    bs2 = BitString(valor=0b1100, bits=4)
    esperado = BitString(valor=0b1111, bits=4)
    
    resultado = bs1 | bs2

    assert resultado == esperado


def test_pode_realizar_operacao_xor_bit_a_bit():
    bs1 = BitString(valor=0b0100, bits=4)
    bs2 = BitString(valor=0b1000, bits=4)
    esperado = BitString(valor=0b1100, bits=4)
    
    resultado = bs1 ^ bs2

    assert resultado == esperado


def test_pode_realizar_operacao_and_bit_a_bit():
    bs1 = BitString(valor=0b1011, bits=4)
    bs2 = BitString(valor=0b1100, bits=4)
    esperado = BitString(valor=0b1000, bits=4)
    
    resultado = bs1 & bs2

    assert resultado == esperado
    
