# Análisis — Tarea 1

**Integrantes:**
1. Arteaga Sánchez Danhé Mahetsi
2. Sánchez Segura Luis Yamil Antonio
3. Sosa Aranda Miguel

**Fork:**
**Rama:**

> Contesten en este archivo. Respuestas breves y concretas: se califica que
> hayan entendido, no la extensión.

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | Cadena de texto con la expresión aritmética. | Una lista de objetos tipo Token que tienen su nombre, valor y posición dentro de la expresión. | Se encarga de hacer el análisis sintático, reconociendo cada token como un número, operador binario o hasta un paréntesis. |
| `parser` | Lista de tokens generada por el lexer. | Crea la estructura para el AST. | Se encarga de hacer el análisis sintático para revisar que los tokens recibidos respeten las reglas de la expresión aritmética, así como la prescedencia de operaciones. |
| `ast` | Recibe la construcción del árbol hecha por el parser. | Entrega una cadena de texto con la reppresentación del árbol AST de la expresión aritmética. | Crea nodos con los números y las operaciones binarias, leyende de izquierda a derecha la expresión aritmética para representarla correctamente. |
| `evaluator` | Recibe un nodo del AST. | El valor resultante del nodo. | Se encarga de que la semántica sea la correcta y si es así resuelve las operaciones de cada nodo para al final regresar el resultado numérico de la expresión aritmética. |

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

> Usen `(3 + 4) * 2` como ejemplo y muestren cómo se ve entre etapa y etapa.

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | [PAR_IZQ, NUMERO(3), MAS, NUMERO(4), PAR_DER, POR, NUMERO(2)] |
| AST | 
```text
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```
|
| resultado | 14 |

> Para el renglón del AST, dibújenlo **primero ustedes** y después comprueben
> con `python3 interprete.py --arbol "(3 + 4) * 2"`. Si su dibujo y el del
> programa no coinciden, uno de los dos está mal, y averiguar cuál es
> justamente el trabajo.

---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| test_tokeniza_un_numero_solo() | La función test_tokeniza_un_numero_solo, método de tokenizar(“42”), el objeto [Token(TipoToken.NUMERO, 42, 0)] y el assert que valida. | Este test revisa que el número a tokenizar sea entregado como un solo número entero sin tener problemas al pasar dos dígitos. Esos dos dígitos se deben de leer como un sólo número. | 1: operador de comparación. | Normal. |
| test_tokeniza_una_suma() | La función test_tokeniza_una_suma, el assert que valida, el método tokenizar(“3+4”), la lista de tokens con sus valores y posiciones. | El test se encarga de que a la cadena de texto que se le aplique el método tokenizar pase exactamente como una lista de 3 tokens (en este caso) con sus propios valores y posiciones. | 2: suma y operador de comparación. | Normal. | 
| test_los_espacios_no_producen_tokens() | La función test_los_espacios_no_producen_tokens, el assert que valida, la función len(..) con la función tokenizar y su cadena de texto y el número 3. | Este test checa que los espacios dentro de la cadena de texto sean ignorados por el lexer y que solo se cuenten los dígitos que son números u operaciones binarias. Regresa un número entero que debe coincidir con la longitud de los tokens. | 2: suma y operador de comparación. | Normal. |
| test_tokeniza_parentesis() | La función test_tokeniza_parentesis, tipos que es una lista de tokens la cual se itera de acuerdo a la cadena de texto que tokenizar recibe, el assert que valida que tipos sea igual a la lista de tokens que el lexer devolvió del string en su parámetro. | Se encarga de checar que la variable tipos que inicialmente era una lista la cual se itera en base a lo que el lexer tokenize (en este caso un string con paréntesis) sea igual a una lista de tokens clasificados principalmente como paréntesis y número. | 2: los operadores de comparación. | Normal. |
| arbol_de(texto) | La función arbol_de con el parámetro texto que es una cadena de carácteres, el objeto de Parser que utiliza el método parsear del texto tokenizado. |  Crea un nuevo árbol en base del Parser para realizar las siguientes pruebas. | Ninguno. | Normal. |
| test_construye_el_arbol_de_una_suma() | La función test_construye_el_arbol_de_una_suma, el assert que valida, la función arbol_de(..) que construye un árbol de acuerdo al texto dado, el objeto OperacionBinaria que devuelve el resultado directo de los valores dados. | Se encarga de checar que el árbol construido siga la misma forma que la operación binaria dada. | 3: la suma y la operación de comparación. | Normal. |
| test_la_multiplicacion_se_agrupa_antes_que_la_suma() | La función test_la_multiplicacion_se_agrupa_antes_que_la_suma, el assert que valida, la función arbol_de(..) que crea un árbol de sus parámetros, OperacionBinaria con parámetros de otro objeto de OperacionBinaria, un número y otra operación. | Revisa que el árbol resultante siga la misma forma que la operación binaria, esto siguiendo las reglas de que la multiplicación/división se hace antes que la suma/resta. | 5: las sumas, las multiplicaciones y el operador de comparación. | Normal. |
| test_los_parentesis_cambian_la_agrupacion() | La función test_los_parentesis_cambian_la_agrupacion, el assert que valida, la función arbol_de(...) que genera un árbol, el objeto OperacionBinaria que recibe la operación, un número y otro objeto OperacionBinaria. | Se encarga de revisar que el árbol generado siga la misma forma que la operación binaria, esto tomando en cuenta que se pasaron paréntesis que agrupan dentro de la cadena de texto. | 5: las sumas, las multiplicaciones y el operador de comparación. | Frontera. |
| test_suma() | La función test_suma, el assert que valida, el método interpretar(..) y el valor 7. | Se encarga de que el método interpretar devuelva el resultado correspondiente de la cadena de texto. | 2: la suma y el operador de comparación. | Normal. |
| test_resta() | La función test_resta, el assert que valida, el método interpretar(..) y el valor 7. | Se encarga de que el método interpretar devuelva el resultado correspondiente de la cadena de texto. | 2: La resta y el operador de comparación. | Normal. |
| test_multiplicacion() | La función test_multiplicacion, el assert que valida, el método interpretar(..) y el valor 42. | Se encarga de que el método interpretar devuelva el resultado correspondiente de la cadena de texto. | 2: La multiplicación y el operador de comparación. | Normal. |
| test_division() | La función test_division, el assert que valida, el método interpretar(..) y el valor 5. | Se encarga de que el método interpretar devuelva el resultado correspondiente de la cadena de texto. | 2: La división y el operador de comparación. | Normal. |
| test_precedencia_sin_parentesis() | La función test_precedencia_sin_parentesis, el assert que valida, el método interpretar(..) y el valor 11. | Se encarga de que el método interpretar devuelve el resultado correspondiente de la cadena de texto. Respetando las reglas de que la multiplicación/división se realizan primero y después la suma/resta. | 3: la suma, la multiplicación y el operador de comparación. |
| test_precedencia_con_parentesis() | La función test_precedencia_con_parentesis, el assert que valida, el método interpretar(..) y el valor 14. | Se encarga de que el método interpretar devuelve el resultado correspondiente de la cadena de texto. Respetando la agrupación que realizan los paréntesis. | 3: la suma, la multiplicación y el operador de comparación. | Frontera. | 

> La función arbol_de(texto) solo es un auxiliar para las siguientes pruebas

> Llenen la tabla **completa**, con las 13. Es tediosa a propósito: la única
> forma de saber qué no está cubierto es caracterizar sistemáticamente lo que
> sí. Cuando terminen, léanla como columna, no como renglones, y pregúntense
> qué combinación **no aparece nunca**.

### 2.2 ¿Qué comportamientos **no** estaban probados?

> Ésta es la pregunta importante de toda la tarea. Tómense su tiempo.
- La división entre 0.
- La prescedencia de operadores utilizando la división y la resta.
- Paréntesis vacíos.
- Operaciones entre números negativos.
- La asociatividad en sus distintas formas.
- Operaciones con números como "003" o "074".
---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| test_resultado_numero_decimal() | interpretar("3 / 2") | 1.5 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_precedencia_sin_parentesis_con_division_y_multiplicacion() | interpretar("12 / 4 * 2") | 1.5 | Normal. | Cumple las reglas con las que se definió el modelo del programa. |
| test_precedencia_sin_parentesis_con_suma_y_resta() | interpretar("12 - 4 + 5") | 3 | Normal. | Cumple las reglas con las que se definió el modelo del programa. |
| test_doble_parentesis() | interpretar("((3+2))") | 5 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_precedencia_con_division() | interpretar("(8-4) / 2") | 2 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_precedencia_sin_parentesis_con_division() | interpretar("8 - 4 / 2") | 6 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_expresion_con_muchos_espacios() | interpretar("3       + 9     *  2") | 21 | Normal. | Cumple con las reglas definidas del modelo del programa.  |
| test_cero_a_la_izquierda() | interpretar("003 + 0006") | 9 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_operacion_con_negativos() | interpretar("(0-9) + 8") | -1 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_resultado_negativo() | assert interpretar("0 - 9") | -9 | Normal. | Cumple con las reglas definidas del modelo del programa. |
| test_error_division_con_divisor_evaluado_en_cero() | interpretar("12 / (5 - 5)") | pytest.raises(ErrorDeEvaluacion) | Frontera. | Una operación que da como resultado un cero que divide otro número no es parte de las reglas pero es algo que se debe tomar en cuenta. |
| test_error_division_entre_cero() | interpretar("0 / 0") | pytest.raises(ErrorDeEvaluacion) | Frontera. | Una división entre dos ceros que no está definida en el modelo. |
| test_lista_sin_tokens() | arbol_de("") | pytest.raises(ErrorDeSintaxis) | Frontera. | Una lista sin tokens no se le puede crear un AST. |
| test_parentesis_incompleto() | arbol_de("(3 + 8") | pytest.raises(ErrorDeSintaxis) | Frontera. | La operación aritmética está bien escrita pero hace falta cerrar el paréntesis. |
| test_sin_numeros() | arbol_de("+ -") | pytest.raises(ErrorDeSintaxis) | Frontera. | No se puede crear un árbol con solo operandos. |
| test_caracter_invalido() | arbol_de("2@3") | pytest.raises(ErrorDeSintaxis) | Entrada inválida. | Se usan carácteres que no son parte de la sintática del modelo del programa. |
| test_operacion_con_numero_no_entero() | interpretar("3 + 4.5") | pytest.raises(ErrorDeEvaluacion) | Entrada inválida. | Aunque la semántica pida que sean números enteros, no se levanta ninguna excepción cuando se ponen decimales en la entrada del intérprete. |
| test_operador_sin_operandos() | interpretar("+") | pytest.raises(ErrorDeSintaxis) | Entrada inválida. | No se puede evaluar una operación sin números. |
| test_solo_numeros() | arbol_de("3 2") | pytest.raises(ErrorDeSintaxis) | Entrada inválida. | No se puede generar un AST de solo números. |
| test_parentesis_vacios() | arbol_de("()") | pytest.raises(ErrorDeSintaxis) | Entrada inválida. | No hay ningún número u operador que se pueda evaluar. |
| test_operadores_consecutivos() | arbol_de("3 +-4") | pytest.raises(ErrorDeSintaxis) | Entrada inválida. | No se puede generar un AST con dos operandores consecutivos. |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?
Que no se tomaban en cuenta distintas entradas inválidas que un usuario puede colocar al usar el intérprete sin saber la semántica declarada en el modelo del código. Al igual que el mismo código original presentaba diferentes señales de mal diseño o inestabilidad, como duplicación o amplificación.

### 4.2 ¿Por qué el comportamiento observado era incorrecto?
Dejando a un lado que salían commits rojos después de correr las pruebas, se comparó más que nada con las entradas que se pedían en la semántica declarada del modelo original del programa. La mayoría de estos commits son debido a entradas inválidas en el uso del intérprete o en la creación del árbol de análisis sintático. En el modelo original no se tomaron en cuenta casos vacíos (como una lista de tokens vacía para crear un AST o una cadena de texto vacía en el intérprete), los paréntesis no cerrados (regla de la precedencia), operaciones con números no enteros (regla de los números) y operaciones con solo números (regla de la entrada inválida). 

> No basta con "daba mal". Digan contra qué lo están comparando: qué regla,
> qué línea de la semántica declarada del README.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| El programa levanta un error de sintaxis al tratar de construir un árbol con una lista de tokens vacía. | arbol_de("") | IndexError: list index out of range | Lanzar un ErrorDeSintaxis | | |
| El programa no levanta un error de sintaxis cuando se pasa una expresión aritmética con un paréntesis sin cerrar. | arbol_de("(3 + 8") | IndexError: list index out of range | Lanzar un ErrorDeSintaxis | | |
| El programa no levanta un error de sintaxis cuando se pasa una expresión sin un operando válido. | arbol_de("2@3") | Failed: DID NOT RAISE ErrorDeSintaxis | Lanzar un ErrorDeSintaxis | | |
| El programa no levanta un error de evaluación al tratar de hacer una operación con un número que no cumple con la semántica del modelo del programa. | interpretar("3 + 4.5") | Failed: DID NOT RAISE ErrorDeEvaluacion | Lanzar un ErrorDeEvaluacion | | |
| El programa no levanta un error de sintaxis cuando se pasan solo números al intérprete. | arbol_de("3 2") | Failed: DID NOT RAISE ErrorDeSintaxis | Lanzar un ErrorDeSintaxis | | |


### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

Como el código original contiene ciertas señales de mal diseño que se fueron revelando a lo largo de las pruebas, llegamos a la conclusión de que corrigiendo gran parte de este muchos de los tests que quedaron en rojo podían pasar sin necesidad de hacer una refactorización demasiado específica para cada uno. También se tomó en cuenta aquellas pruebas que sí pasaron desde el principio para no tener otro error o problema dentro de ellas al ejecutarlas.


## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?
   
   1.- Duplicacion del codigo en en el parser.
   
En el archivo parser.py, los métodos _expresion() y _termino() tienen una estructura muy similar. Ambos obtienen el operando izquierdo, revisan el token actual, verifican si corresponde a un operador permitido y construyen un nodo OperacionBinaria. Las diferencias están en el grupo de operadores que aceptan y en los métodos que llaman para obtener los operandos.

Esta repetición dificulta el mantenimiento: si se necesita modificar la lógica compartida, habría que revisar ambos métodos. Existe el riesgo de cambiar uno y olvidar el otro, causando comportamientos inconsistentes.

   2.- Amplificación del cambio al agregar un operador.

La información necesaria para admitir un operador está distribuida entre varios componentes. Por ejemplo, para agregar %con la misma precedencia que la multiplicación habría que modificar cuatro archivos:
- tokens.py: definir el nuevo tipo de token.
- lexer.py: asociar el símbolo % con ese token.
- parser.py: incluirlo en el grupo de operadores con la precedencia correspondiente.
- evaluator.py: implementar la operación.
Aunque cada componente tiene una responsabilidad distinta, agregar un operador requiere coordinar cambios en todos ellos. Si se omite alguno, el soporte del operador queda incompleto. Esto representa una limitación de mantenibilidad y extensibilidad.

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

Consideramos que ninguno de estos patrones es necesario para los cambios realizados.
Factory Method permite delegar en subclases la elección del objeto concreto que se crea. En este intérprete, el parser construye directamente nodos Numero y OperacionBinaria, y no existe una necesidad actual de variar su creación mediante subclases. Incorporar este patrón añadiría estructura sin resolver la duplicación identificada. Podría ser pertinente si existieran distintas variantes del parser que necesitaran crear diferentes tipos de nodos mediante una interfaz común.
Adapter permite que componentes con interfaces incompatibles trabajen juntos. Actualmente, el lexer entrega los tokens que espera el parser y este construye los nodos que utiliza el evaluador, por lo que no identificamos una incompatibilidad que requiera un adaptador. Podría ser útil si se integrara un lexer externo cuyo formato de tokens fuera distinto del que acepta nuestro parser.
Para eliminar la duplicación entre _expresion() y _termino() fue suficiente extraer la lógica compartida a _operacion_binaria(). Este método auxiliar no constituye por sí mismo un Factory Method ni un Adapter. Por ello, preferimos mantener una solución sencilla y no incorporar patrones sin una necesidad concreta.


### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

> Por ejemplo `%`. ¿Cuántos archivos hay que tocar? ¿Por qué?

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
