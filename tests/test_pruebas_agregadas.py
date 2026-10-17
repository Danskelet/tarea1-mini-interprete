"""Pruebas agregadas"""

"""Lexer"""
from mini_interprete.lexer import tokenizar
from mini_interprete.tokens import Token, TipoToken

"""Parser"""
from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.lexer import tokenizar
from mini_interprete.parser import Parser

"""Evaluator"""
from mini_interprete.cli import interpretar




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
