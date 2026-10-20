# Análisis — Tarea 1

**Integrantes:**

1. Arteaga Sánchez Danhé Mahetsi
2. Sánchez Segura Luis Yamil Antonio
3. Sosa Aranda Miguel

**Fork:** https://github.com/Danskelet/tarea1-mini-interprete
**Rama de entrega:** `main`, una vez revisado y fusionado el pull request correspondiente.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | Texto de una expresión. | Tokens con tipo, valor y posición. | Realiza el análisis léxico: reconoce números, operadores y paréntesis, ignora espacios y rechaza caracteres inválidos. |
| `parser` | Lista de tokens. | Árbol de sintaxis abstracta (AST). | Verifica la estructura de la expresión y construye el árbol respetando precedencia, asociatividad y paréntesis. |
| `ast` | Valores y operandos para crear nodos; un árbol para representarlo. | Nodos `Numero` y `OperacionBinaria`, y una representación textual del árbol. | Define los nodos y permite visualizar el árbol construido por el parser. |
| `evaluator` | Un nodo del AST. | Resultado numérico o error de evaluación. | Recorre el árbol, calcula las operaciones y controla errores como la división entre cero. |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

| Etapa | Representación de `(3 + 4) * 2` |
|---|---|
| Texto | `"(3 + 4) * 2"` |
| Tokens, abreviados | `PAR_IZQ, NUMERO(3), MAS, NUMERO(4), PAR_DER, POR, NUMERO(2)` |
| AST | `OperacionBinaria("*", OperacionBinaria("+", Numero(3), Numero(4)), Numero(2))` |
| Resultado | `14` |

Los objetos `Token` también conservan el valor y la posición dentro del texto.
El árbol tiene esta forma:

```text
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```

El lexer transforma el texto en tokens. El parser construye el árbol y los
paréntesis hacen que la suma sea el operando izquierdo de la multiplicación.
El evaluador calcula primero `3 + 4 = 7` y después `7 * 2 = 14`.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

Se cuentan los operadores aritméticos de la expresión de entrada, no el
`==` del `assert`. Los paréntesis delimitan agrupaciones y no se cuentan
como operadores aritméticos.

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| `test_tokeniza_un_numero_solo` | Lexer | `42` se reconoce como un único token numérico con su valor y posición. | 0 | Normal |
| `test_tokeniza_una_suma` | Lexer | `3+4` produce los tokens esperados, con sus valores y posiciones. | 1 | Normal |
| `test_los_espacios_no_producen_tokens` | Lexer | Una suma con espacios produce tres tokens. | 1 | Normal |
| `test_tokeniza_parentesis` | Lexer | `(3)` produce los tipos de token de apertura, número y cierre. | 0 | Normal |
| `test_construye_el_arbol_de_una_suma` | Parser | El árbol de `3 + 4` tiene la estructura esperada. | 1 | Normal |
| `test_la_multiplicacion_se_agrupa_antes_que_la_suma` | Parser | El árbol de `3 + 4 * 2` representa `3 + (4 * 2)`. | 2 | Normal |
| `test_los_parentesis_cambian_la_agrupacion` | Parser | El árbol de `(3 + 4) * 2` coloca la suma como operando de la multiplicación. | 2 | Normal |
| `test_suma` | Interpretación completa, resultado del evaluador | `3 + 4` produce `7`. | 1 | Normal |
| `test_resta` | Interpretación completa, resultado del evaluador | `10 - 3` produce `7`. | 1 | Normal |
| `test_multiplicacion` | Interpretación completa, resultado del evaluador | `6 * 7` produce `42`. | 1 | Normal |
| `test_division` | Interpretación completa, resultado del evaluador | `10 / 2` compara igual a `5`; esta prueba no distingue entre `5` y `5.0`. | 1 | Normal |
| `test_precedencia_sin_parentesis` | Interpretación completa | `3 + 4 * 2` produce `11`. | 2 | Normal |
| `test_precedencia_con_parentesis` | Interpretación completa | `(3 + 4) * 2` produce `14`. | 2 | Normal |

Son 13 pruebas. `arbol_de(texto)` es una función auxiliar, no una prueba.
Las pruebas que llaman a `interpretar()` también recorren el lexer y el
parser; no prueban el evaluador de manera aislada.

### 2.2 ¿Qué comportamientos no estaban probados?

- División con resultado no entero y división entre cero, incluido un divisor calculado como cero.
- Asociatividad de operadores del mismo nivel, especialmente resta y división.
- Precedencia con resta y división, y paréntesis anidados.
- Ceros iniciales y resultados negativos obtenidos mediante resta.
- Entrada vacía, operandos faltantes y paréntesis vacíos o incompletos.
- Caracteres inválidos, literales decimales y números consecutivos sin operador.
- Consumo completo de los tokens y precisión de las posiciones de error.

Las pruebas iniciales no incluían casos inválidos ni verificaban errores.
Aunque había expresiones con dos operadores, ninguna encadenaba dos del
mismo nivel para distinguir la agrupación por la izquierda de la derecha.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

La categoría indica el aspecto principal que comprueba cada prueba.
Una entrada frontera, como la cadena vacía, también puede ser inválida.

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| tests/test_pruebas_agregadas.py::test_resultado_numero_decimal | `3 / 2` | `1.5` | Normal | La división es real y puede producir resultados decimales. |
| tests/test_pruebas_agregadas.py::test_precedencia_sin_parentesis_con_division_y_multiplicacion | `12 / 4 * 2` | `6` | Normal | Operadores de igual precedencia se agrupan a la izquierda: `(12 / 4) * 2`. |
| tests/test_pruebas_agregadas.py::test_precedencia_sin_parentesis_con_suma_y_resta | `12 - 4 + 5` | `13` | Normal | Operadores de igual precedencia se agrupan a la izquierda: `(12 - 4) + 5`. |
| tests/test_pruebas_agregadas.py::test_doble_parentesis | `((3+2))` | `5` | Normal | Comprueba una expresión con paréntesis anidados. |
| tests/test_pruebas_agregadas.py::test_precedencia_con_division | `(8-4) / 2` | `2.0` | Normal | Los paréntesis hacen que la resta se evalúe antes de la división. |
| tests/test_pruebas_agregadas.py::test_precedencia_sin_parentesis_con_division | `8 - 4 / 2` | `6.0` | Normal | La división tiene mayor precedencia que la resta. |
| tests/test_pruebas_agregadas.py::test_expresion_con_muchos_espacios | `3       + 9     *  2` | `21` | Normal | Los espacios deben ignorarse sin alterar la precedencia. |
| tests/test_pruebas_agregadas.py::test_cero_a_la_izquierda | `003 + 0006` | `9` | Frontera | Comprueba la representación de enteros con ceros iniciales, admitida por el README. |
| tests/test_pruebas_agregadas.py::test_operacion_con_negativos | `(0-9) + 8` | `-1` | Normal | Utiliza un valor negativo obtenido por resta, sin recurrir al menos unario. |
| tests/test_pruebas_agregadas.py::test_resultado_negativo | `0 - 9` | `-9` | Normal | Una resta válida puede producir un resultado negativo. |
| tests/test_pruebas_agregadas.py::test_error_division_con_divisor_evaluado_en_cero | `12 / (5 - 5)` | `ErrorDeEvaluacion` | Frontera | El divisor llega a cero después de evaluar una subexpresión. |
| tests/test_pruebas_agregadas.py::test_error_division_entre_cero | `0 / 0` | `ErrorDeEvaluacion` | Frontera | Comprueba el valor cero como divisor, prohibido por la semántica declarada. |
| tests/test_pruebas_agregadas.py::test_lista_sin_tokens | Cadena vacía: `""` | `ErrorDeSintaxis` | Frontera | Comprueba una entrada de longitud cero que no permite construir una expresión. |
| tests/test_pruebas_agregadas.py::test_parentesis_incompleto | `(3 + 8` | `ErrorDeSintaxis` | Entrada inválida | Falta el paréntesis de cierre. |
| tests/test_pruebas_agregadas.py::test_sin_numeros | `+ -` | `ErrorDeSintaxis` | Entrada inválida | Hay operadores sin operandos y no se admite menos unario. |
| tests/test_pruebas_agregadas.py::test_caracter_invalido | `2@3` | `ErrorDeSintaxis` | Entrada inválida | `@` no pertenece a los símbolos admitidos. |
| tests/test_pruebas_agregadas.py::test_operacion_con_numero_no_entero | `3 + 4.5` | `ErrorDeSintaxis` | Entrada inválida | Los literales admitidos son enteros; el punto decimal es inválido. |
| tests/test_pruebas_agregadas.py::test_operador_sin_operandos | `+` | `ErrorDeSintaxis` | Entrada inválida | El operador no tiene operandos. |
| tests/test_pruebas_agregadas.py::test_solo_numeros | `3 2` | `ErrorDeSintaxis` | Entrada inválida | Hay dos números consecutivos sin un operador entre ellos. |
| tests/test_pruebas_agregadas.py::test_parentesis_vacios | `()` | `ErrorDeSintaxis` | Entrada inválida | Los paréntesis no contienen una expresión. |
| tests/test_pruebas_agregadas.py::test_operadores_consecutivos | `3 +-4` | `ErrorDeSintaxis` | Entrada inválida | No se admite el menos unario después del operador de suma. |
| tests/test_parser.py::test_parentesis_sobrante | `(3 + 4) ) / 5` | `ErrorDeSintaxis` | Entrada inválida | Aparece un paréntesis de cierre sin apertura correspondiente. |
| tests/test_parser.py::test_parentesis_vacios | `(4 + 3) () / 5` | `ErrorDeSintaxis` | Entrada inválida | Tras una expresión completa aparecen paréntesis vacíos sin un operador intermedio. |
| tests/test_parser.py::test_operador_incompleto_al_final | `4+3 *` | `ErrorDeSintaxis` | Entrada inválida | La entrada termina sin el operando derecho de la multiplicación. |
| tests/test_parser.py::test_la_division_se_agrupa_antes_que_la_resta | `20 - 8 / 2` | AST equivalente a `20 - (8 / 2)` | Normal | Comprueba la precedencia de división sobre resta mediante la estructura del árbol. |

**Corrección de expectativas.** Se corrigieron tres pruebas conforme a la
sección 7, “Semántica declarada”, del README:

- **Asociatividad:** `12 / 4 * 2` debe producir `6` y `12 - 4 + 5`
  debe producir `13`, en lugar de `1.5` y `3`, porque los operadores
  de igual precedencia se agrupan a la izquierda.
- **Números y entrada inválida:** `3 + 4.5` debe lanzar `ErrorDeSintaxis`,
  no `ErrorDeEvaluacion`, porque los literales admitidos son enteros.

Las expectativas se corrigieron en el commit `0c4352e`.

La suite integrada contiene 38 pruebas: 13 originales y 25 adicionales.
En la última ejecución local, las 38 pasaron.
---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

En el historial de `master`, la primera prueba nueva fallida fue
`test_parentesis_sobrante`, agregada en `32c7501`. La entrada
`(3 + 4) ) / 5` debía rechazarse, pero el parser original devolvía el árbol
de la primera expresión sin comprobar que hubiera consumido todos los tokens.

Después se detectaron accesos fuera de la lista de tokens, caracteres
inválidos ignorados y agrupación incorrecta de operadores de igual precedencia.

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

La sección 7 del README establece que:

- Una entrada inválida debe producir `ErrorDeSintaxis`, nunca un error interno de Python.
- Los literales de entrada son enteros: `3 + 4.5` es inválido, aunque una división pueda producir decimales.
- Los operadores de igual precedencia se agrupan a la izquierda.
- Los mensajes de error deben indicar la posición dentro del texto.

Estas reglas justifican rechazar tokens sobrantes y caracteres inválidos,
controlar las expresiones incompletas y corregir la asociatividad. No se
consideró incorrecto un comportamiento solamente porque una prueba fallara:
también se corrigieron expectativas de las pruebas que contradecían el README.

### 4.3 ¿Qué cambio realizaron?

En la tabla, “Commit verde” identifica un estado comprobado con la suite en
verde que incluye la solución. Los commits donde se implementó cada cambio
se detallan después, porque algunos todavía tenían otros fallos pendientes.

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| Aceptaba tokens después de una expresión completa. | `(3 + 4) ) / 5` | No lanzaba la excepción esperada. | `ErrorDeSintaxis`. | `32c7501` | `ef04613`, con las 16 pruebas de ese momento. |
| Accedía a la lista después de agotar los tokens. | `4+3 *` | `IndexError`. | `ErrorDeSintaxis`. | `db98e5b` | `ef04613`, con las 16 pruebas de ese momento. |
| Ignoraba caracteres inválidos. | `2@3` | No lanzaba la excepción esperada. | `ErrorDeSintaxis` en la posición de `@`. | `0c4352e` | `ffeb95a` |
| Omitía el punto decimal. | `3 + 4.5` | No rechazaba la entrada. | `ErrorDeSintaxis`. | `0c4352e`, con la expectativa corregida. | `ffeb95a` |
| Permitía exactamente un token sobrante. | `3 2` | Aceptaba el primer número e ignoraba el segundo. | `ErrorDeSintaxis` en la posición del segundo número. | `0c4352e` | `ffeb95a` |
| Agrupaba operadores del mismo nivel por la derecha. | `12 / 4 * 2`; `12 - 4 + 5` | `1.5`; `3`. | `6`; `13`. | `0c4352e` | `ffeb95a` |

Cambios realizados:

- `ef04613`: comprobación de agotamiento en `_avanzar()` y primera validación
  de tokens sobrantes. Esta última todavía permitía que sobrara un token.
- `6341eb0`: el lexer lanza `ErrorDeSintaxis` ante caracteres desconocidos,
  indicando su posición en el texto.
- `cf711b4`: `parsear()` rechaza cualquier token sobrante y utiliza su
  atributo `posicion` en el error.
- `ffeb95a`: los ciclos de `_expresion()` y `_termino()` construyen las
  operaciones por la izquierda. Las 37 pruebas disponibles pasaron.

Después se integró la prueba adicional de precedencia y se adaptó el método
auxiliar de `yamil-d` a la lógica corregida. La suite integrada pasó 38 pruebas.

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

Las correcciones aplican reglas generales, sin condiciones específicas para
los números o las cadenas utilizadas por las pruebas:

- El lexer rechaza los caracteres que no reconoce, no solamente `@`.
- El parser comprueba cualquier token sobrante, no solamente la entrada `3 2`.
- La comprobación de agotamiento protege el acceso a la lista en diferentes expresiones incompletas.
- Los ciclos procesan operadores del mismo nivel y acumulan el árbol por la izquierda.

Se ejecutó la suite completa, que incluye operaciones de ambos niveles,
paréntesis, entradas inválidas y división entre cero. La última ejecución
local integrada obtuvo 38 pruebas aprobadas y no reportó problemas con
`git diff --check`. Esto respalda los cambios, pero no demuestra ausencia
de todos los errores posibles.

**Limitación pendiente:** al agotarse los tokens, `_avanzar()` todavía usa
`self.pos`, que es un índice de tokens, como posición del error. Con espacios
o números de varios dígitos puede no coincidir con la posición en el texto.
Las pruebas actuales no comprueban esa precisión. No se afirma que todos
los mensajes de error ya cumplan completamente ese requisito.

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?
   
**1. Duplicación de código en el parser.**
   
En el archivo parser.py, los métodos _expresion() y _termino() tenían una estructura muy similar. Ambos obtenían el operando izquierdo, revisaban el token actual, verificaban si corresponde a un operador permitido y construían un nodo `OperacionBinaria`. Las diferencias están en el grupo de operadores que aceptan y en los métodos que llaman para obtener los operandos.

Esta repetición dificulta el mantenimiento: si se necesita modificar la lógica compartida, habría que revisar ambos métodos. Existe el riesgo de cambiar uno y olvidar el otro, causando comportamientos inconsistentes.

**2. Amplificación del cambio al agregar un operador.**

La información necesaria para admitir un operador está distribuida entre varios componentes. Por ejemplo, para agregar `%` con la misma precedencia que la multiplicación habría que modificar cuatro archivos:

- tokens.py: definir el nuevo tipo de token.
- lexer.py: asociar el símbolo % con ese token.
- parser.py: incluirlo en el grupo de operadores con la precedencia correspondiente.
- evaluator.py: implementar la operación.

Aunque cada componente tiene una responsabilidad distinta, agregar un operador requiere coordinar cambios en todos ellos. Si se omite alguno, el soporte del operador queda incompleto. Esto representa una limitación de mantenibilidad y extensibilidad.


### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

Se extrajo la lógica duplicada de `_expresion()` y `_termino()` a un
método auxiliar llamado `_operacion_binaria()`.

En la versión final, el auxiliar recibe un método para leer los operandos
y el grupo de operadores permitido. `_expresion()` utiliza `_termino()`
para leer sus operandos, mientras que `_termino()` utiliza `_factor()`.
Así se conservan los niveles de precedencia.

El auxiliar utiliza un ciclo que incorpora cada operación al árbol
acumulado en el lado izquierdo. Esto conserva la asociatividad por la
izquierda de la versión corregida: por ejemplo, `12 / 4 * 2` se agrupa
como `(12 / 4) * 2`.

La corrección de asociatividad y la refactorización son cambios distintos.
La primera corrigió el comportamiento del programa; la segunda reorganiza
la lógica corregida sin cambiar el orden de consumo de los tokens ni
la estructura de los árboles resultantes.

Inicialmente, las 17 pruebas disponibles pasaron antes y después de la
primera refactorización. Tras integrar las nuevas pruebas y correcciones
de `main`, se adaptó el auxiliar a la agrupación por la izquierda.
La versión integrada pasó las 38 pruebas.

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?


Consideramos que ninguno de estos patrones es necesario para los cambios realizados.

Factory Method permite delegar en subclases la elección del objeto concreto que se crea. En este intérprete, el parser construye directamente nodos Numero y OperacionBinaria, y no existe una necesidad actual de variar su creación mediante subclases. Incorporar este patrón añadiría estructura sin resolver la duplicación identificada. Podría ser pertinente si existieran distintas variantes del parser que necesitaran crear diferentes tipos de nodos mediante una interfaz común.

Adapter permite que componentes con interfaces incompatibles trabajen juntos. Actualmente, el lexer entrega los tokens que espera el parser y este construye los nodos que utiliza el evaluador, por lo que no identificamos una incompatibilidad que requiera un adaptador. Podría ser útil si se integrara un lexer externo cuyo formato de tokens fuera distinto del que acepta nuestro parser.

Para eliminar la duplicación entre _expresion() y _termino() fue suficiente extraer la lógica compartida a _operacion_binaria(). Este método auxiliar no constituye por sí mismo un Factory Method ni un Adapter. Por ello, preferimos mantener una solución sencilla y no incorporar patrones sin una necesidad concreta.


### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?


La principal dificultad sería coordinar los cambios entre los componentes.
Para agregar `%` como operador binario con la misma precedencia que la
multiplicación, habría que modificar cuatro archivos de implementación:

- `tokens.py`: definir el tipo de token.
- `lexer.py`: asociar el símbolo `%` con ese tipo en `SIMBOLOS`.
- `parser.py`: incluir el token en el grupo de precedencia correspondiente.
- `evaluator.py`: implementar el cálculo y definir los errores aplicables.

El AST ya representa operaciones binarias mediante `OperacionBinaria`,
por lo que su estructura puede reutilizarse para este operador.

Además, habría que documentar las reglas del nuevo operador en el README
y agregar pruebas. Cambiar únicamente el README o definir un token no
hace que los demás componentes reconozcan y evalúen automáticamente
el operador.


---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.
