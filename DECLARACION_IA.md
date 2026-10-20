# Declaración de uso de Inteligencia Artificial

**Actividad:** Tarea 1 — Mini intérprete de expresiones  
**Fecha:** 19 de octubre de 2026

**Integrantes**

- Arteaga Sánchez Danhé Mahetsi
- Sánchez Segura Luis Yamil Antonio
- Sosa Aranda Miguel 

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.**
- [x] **Sí.**

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|---|---|
| Codex | Modelo específico no registrado. |

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
|---|---|
| Obtener sugerencias y pistas para revisar el funcionamiento del intérprete y contrastar observaciones sobre el código. | Análisis del sistema. |
| Recibir sugerencias de pruebas y propuestas para reducir duplicación, verificando los cambios incorporados. | Pruebas y refactorización. |
| Comprender cómo funciona un pull request, cómo se crea y qué debe revisarse antes de integrar una rama. | Flujo de trabajo en GitHub. |

---

## 3. Prompts principales

Las siguientes formulaciones resumen las consultas realizadas.
No son transcripciones literales de los mensajes originales.

```text
Proporciona sugerencias y pistas para revisar este mini intérprete:
qué comportamientos conviene probar según el enunciado y qué partes
del código podrían dificultar su mantenimiento. Justifica tus observaciones.
```

```text
Explica cómo funciona un pull request en GitHub, cómo se crea desde una
rama de trabajo hacia main dentro del mismo fork y qué debemos revisar
antes de fusionarlo.
```

> La plantilla solicita prompts textuales. Antes de entregar, sustituir
> estos resúmenes por los mensajes originales seleccionados.

---

## 4. Cómo se incorporó o se descartó lo obtenido

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|---|---|---|---|
| Sugerencias y observaciones sobre las pruebas y la mantenibilidad. | Revisadas y utilizadas como apoyo. | Se contrastaron con el código y las reglas de la práctica. | Análisis del sistema. |
| Código de una prueba de precedencia de división sobre resta. | Aceptado. | Permite comprobar el árbol de `20 - 8 / 2` antes y después de modificar el parser. | `tests/test_parser.py`, commit `f5a3b9a`. |
| Código para extraer la lógica repetida del parser a un método auxiliar. | Aceptado. | Reduce duplicación conservando las llamadas y la construcción de los nodos. | `src/mini_interprete/parser.py`, commit `7e1cde7`. |
| Explicación del proceso de creación y revisión de un pull request. | Consultado como orientación. | Ayuda a distinguir entre subir commits, solicitar su revisión e integrar una rama. | Preparación del proceso de integración en GitHub. |
| Apoyo en la redacción de las explicaciones y de esta declaración. | Revisado y modificado. | Se ajustó el contenido para describir el alcance del trabajo realizado. | Documentación de la práctica. |

### 4.1. Si la usaron para el análisis: el contraste

En la revisión asistida aquí documentada se consultó la IA antes de completar
un análisis independiente. Por ello, no se presenta como una comparación
entre un análisis propio previo y otro posterior de la herramienta.

| Pregunta | Respuesta |
|---|---|
| ¿Qué encontró la herramienta que no se había notado? | Señaló duplicación en el parser, cambios repartidos entre archivos al agregar operadores y comportamientos que las pruebas existentes no detectaban. |
| ¿Qué no encontró que en este curso sí se considera un problema? | No se registró un hallazgo propio previo que permita responder esta comparación con evidencia. |

### 4.2. ¿Cómo verificaron que lo incorporado era correcto?

- Se ejecutaron las pruebas existentes: **16 aprobadas**.
- Después de agregar la prueba de precedencia: **17 aprobadas**.
- Después de aplicar la refactorización: **17 aprobadas**.
- Se revisó el diff para comprobar las modificaciones realizadas.
- Se comparó el código anterior y posterior para verificar que se conservaran
  las llamadas, su orden, los operadores admitidos y la construcción del árbol.
- El commit `7e1cde7` mostró una comprobación aprobada en GitHub.

Estos resultados respaldan los cambios incorporados, pero no demuestran
que el intérprete esté libre de otros defectos.

---

## 5. Reflexión

### 5.1. ¿Qué limitación concreta observaron en esta actividad?

Una explicación propuesta mezclaba la refactorización con un defecto
de funcionamiento que no se corregía mediante ese cambio. Fue necesario
separar ambos temas para describir con precisión qué se había realizado
y qué seguía pendiente.

### 5.2. ¿Qué harían distinto la próxima vez?

Registrar primero las observaciones propias sobre el código y después
utilizar la IA para contrastarlas. También conservar los prompts originales
y anotar qué propuestas se aceptaron, modificaron o descartaron, junto
con las verificaciones correspondientes.

---

## Firma

Declaramos que entendemos y podemos explicar todo lo que entregamos,
independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|---|---|
| Arteaga Sánchez Danhé Mahetsi| 323122748 |
| Sánchez Segura Luis Yamil Antonio | 323028774 |
| Sosa Aranda Miguel | 323174826 |