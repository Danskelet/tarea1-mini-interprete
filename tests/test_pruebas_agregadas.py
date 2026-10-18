"""Pruebas agregadas"""
import pytest

"""Lexer"""
from mini_interprete.lexer import tokenizar
from mini_interprete.tokens import Token, TipoToken

"""Parser"""
from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.lexer import tokenizar
from mini_interprete.parser import Parser

"""Evaluator"""
from mini_interprete.cli import interpretar
from mini_interprete.evaluator import ErrorDeEvaluacion
from mini_interprete.parser import ErrorDeSintaxis




def arbol_de(texto):
    return Parser(tokenizar(texto)).parsear()

"""Pruebas normales"""

def test_resultado_numero_decimal():
    assert interpretar("3 / 2") == 1.5
 
def test_precedencia_sin_parentesis_con_division_y_multiplicacion():
    assert interpretar("12 / 4 * 2") == 1.5

def test_precedencia_sin_parentesis_con_suma_y_resta():
    assert interpretar("12 - 4 + 5") == 3

def test_doble_parentesis():
    assert interpretar("((3+2))") == 5

def test_precedencia_con_division():
    assert interpretar("(8-4) / 2") == 2

def test_precedencia_sin_parentesis_con_division():
    assert interpretar("8 - 4 / 2") == 6

def test_expresion_con_muchos_espacios():
    assert interpretar("3       + 9     *  2") == 21

def test_cero_a_la_izquierda():
    assert interpretar("003 + 0006") == 9 


def test_operacion_con_negativos():
    assert interpretar("(0-9) + 8") == -1

def test_resultado_negativo():
    assert interpretar("0 - 9") == -9


""""Pruebas frontera"""""

def test_error_division_con_divisor_evaluado_en_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("12 / (5 - 5)")

def test_error_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("0 / 0")

def test_lista_sin_tokens():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("")

def test_parentesis_incompleto():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("(3 + 8")

def test_sin_numeros():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("+ -")

"""Entradas inválidas"""

def test_caracter_invalido():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("2@3")

def test_operacion_con_numero_no_entero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("3 + 4.5")

def test_operador_sin_operandos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("+")

def test_solo_numeros():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("3 2")

def test_parentesis_vacios():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("()")

def test_operadores_consecutivos():
    with pytest.raises(ErrorDeSintaxis):
        arbol_de("3 +-4")
