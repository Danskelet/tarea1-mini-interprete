"""Pruebas del parser: de los tokens al AST."""
import pytest
from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.lexer import tokenizar
from mini_interprete.parser import Parser
from mini_interprete.errores import ErrorDeSintaxis

def arbol_de(texto):
    return Parser(tokenizar(texto)).parsear()


def test_construye_el_arbol_de_una_suma():
    assert arbol_de("3 + 4") == OperacionBinaria("+", Numero(3), Numero(4))


def test_la_multiplicacion_se_agrupa_antes_que_la_suma():
    # 3 + 4 * 2  debe agruparse como  3 + (4 * 2)
    assert arbol_de("3 + 4 * 2") == OperacionBinaria(
        "+", Numero(3), OperacionBinaria("*", Numero(4), Numero(2))
    )


def test_los_parentesis_cambian_la_agrupacion():
    # (3 + 4) * 2  debe agruparse al reves
    assert arbol_de("(3 + 4) * 2") == OperacionBinaria(
        "*", OperacionBinaria("+", Numero(3), Numero(4)), Numero(2)
    )
#Nuevas Pruebas
def test_parentesis_sobrante():
    # (3 + 4) )/ 5 Debe ser un error sintáctico

    with pytest.raises(ErrorDeSintaxis):
        arbol_de("(3 + 4) ) / 5")
def test_parentesis_vacios():
    #(4 + 3) () / 5 Debe lanzar un error por lo paŕentesis vacíos
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("(4 + 3) () / 5")
def test_operador_incompleto_al_final():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("4+3 *")

def test_la_division_se_agrupa_antes_que_la_resta():
    # 20 - 8 / 2 debe agruparse como 20 - (8 / 2).
    assert arbol_de("20 - 8 / 2") == OperacionBinaria(
        "-", Numero(20), OperacionBinaria("/", Numero(8), Numero(2))
    )
