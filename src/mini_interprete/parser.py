"""De los tokens al AST.

La gramatica que reconoce este parser es:

    expresion := termino  (('+' | '-') termino)*
    termino   := factor   (('*' | '/') factor)*
    factor    := NUMERO | '(' expresion ')'

Los tres niveles son lo que hace que  3 + 4 * 2  se agrupe como  3 + (4 * 2)
y no como  (3 + 4) * 2 : la multiplicacion vive un nivel mas abajo, asi que
se arma primero.
"""

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeSintaxis
from .tokens import TipoToken

OPERADORES_SUMA = (TipoToken.MAS, TipoToken.MENOS)
OPERADORES_PRODUCTO = (TipoToken.POR, TipoToken.ENTRE)


class Parser:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
    #Condición en parsear para verificar que no pasen expresiones incompletas, sobretodo en paréntesis
    def parsear(self):
        """Construye el AST y verifica que no sobren tokens."""
        resultado = self._expresion()
        sobrante = self._actual()
        if sobrante is not None:
            raise ErrorDeSintaxis(
                "sobran tokens al final", sobrante.posicion
            )
        return resultado

    def _actual(self):
        """El token en la posicion actual, o None si ya no quedan."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    #Cambiar el método avanzar para verificar que no se ingrese un operador de manera inváilda
    def _avanzar(self):
        """Consume el token actual y lo regresa."""
        if self.pos >=len(self.tokens):
            raise ErrorDeSintaxis("Se esperaba un operando", posicion = self.pos)
        token =self.tokens[self.pos]
        self.pos +=1
        return token
        

    def _expresion(self):
        return self._operacion_binaria(
            self._termino, OPERADORES_SUMA)

    def _termino(self):
        return self._operacion_binaria(
            self._factor, OPERADORES_PRODUCTO)

    def _operacion_binaria(self, leer_operando, operadores):
        """Construye una operacion del grupo indicado si hay un operador."""
        izquierda = leer_operando()
        actual = self._actual()
        while actual is not None and actual.tipo in operadores:
            operador = self._avanzar()
            derecha = leer_operando()
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
            actual = self._actual()
        return izquierda

    def _factor(self):
        token = self._avanzar()

        if token.tipo == TipoToken.NUMERO:
            return Numero(token.valor)

        if token.tipo == TipoToken.PAR_IZQ:
            nodo = self._expresion()
            cierre = self._avanzar()
            if cierre.tipo != TipoToken.PAR_DER:
                raise ErrorDeSintaxis("se esperaba ')'", cierre.posicion)
            return nodo

        raise ErrorDeSintaxis(f"token inesperado {token.valor!r}", token.posicion)
