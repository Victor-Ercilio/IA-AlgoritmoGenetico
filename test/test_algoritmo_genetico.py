import pytest
from classes.algoritmo_genetico import AlgoritmoGenetico


def test_criar_algoritmo_genetico_deve_funcionar():
    ag = AlgoritmoGenetico()

    assert ag 