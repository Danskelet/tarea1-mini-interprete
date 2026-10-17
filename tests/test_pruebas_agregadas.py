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