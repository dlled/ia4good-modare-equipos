# Rúbrica del jurado · Reto Moda re-

**Reto:** «Optimización de la red de distribución entre plantas y tiendas» (Moda re-, IA 4 Good Lab, Fundación Ingenieros ICAI) · **Equipos:** Azul y Amarillo · **Jurado:** los 6 mentores del hackathon y quizá más personas (ver «Quién puntúa») · **Pitch y demo:** domingo 15/11/2026, de 16:00 a 17:30 (unos 15 minutos por equipo); deliberación de 17:30 a 18:00 · **Versión:** 13/11/2026

## Para qué sirve

La rúbrica está alineada con lo que pide la ficha oficial del reto (septiembre de 2026), en concreto con dos de sus apartados:

- **«Resultado esperado del hackathon».** El prototipo debe cargar una muestra de datos, permitir definir hipótesis de suministro y transporte y generar una propuesta para un periodo. Debe incluir la asignación planta-tienda, la segmentación y el nivel de suministro, las rutas con su secuencia, el tipo y la capacidad de los vehículos, un mapa y una comparación de escenarios con kilómetros, tiempo, ocupación, coste, emisiones y nivel de servicio.
- **Lo que la ficha dice que «se valorará especialmente»:** que el prototipo **explique sus supuestos**, que **permita modificarlos con facilidad** y que **diferencie los resultados calculados con datos reales de los obtenidos con parámetros estimados**.

Por eso esos tres puntos pesan un 35 % entre los criterios 1 y 2. El núcleo técnico (criterio 3) pesa un 25 %, porque la ficha deja claro que el reto es de analítica, optimización y simulación, no de IA generativa.

## Quién puntúa

El jurado lo forman los 6 mentores del IA 4 Good Lab, quizá con alguien más, por confirmar con la Fundación. Dani Lledó y David Soler son los mentores de este reto. Cada miembro puntúa por separado con la misma hoja y la nota final es la media. Los mentores aportan además el contexto técnico de lo que han visto durante el fin de semana (qué funciona de verdad, qué es real y qué estimado). Si alguien de Moda re- está en el jurado, puntúa como uno más.

## Cómo puntuar

1. **Antes de que empiecen** (2 min por equipo): marca la lista de entregables.
2. **Durante la demo:** el jurado puede pedir en directo una prueba sobre la herramienta. Pesa más lo que se ve funcionar que lo que se cuenta en las diapositivas.
3. **Al terminar:** puntúa cada criterio de 1 a 5 con los descriptores. Cada miembro del jurado puntúa por separado, con su propia hoja; la nota final de cada equipo es la media de todas las hojas.
4. Puntuación final = Σ (nota × peso) / 5 × 100, con el peso en tanto por uno (0,20, no 20). Sale sobre 100 puntos. Después se aplican los ajustes, si procede, y el total se recorta a un máximo de 100.

Puedes poner notas intermedias (por ejemplo, 3,5) si el equipo está entre dos descriptores.

## Lista de entregables de la ficha

Sirve para comprobar que nada falta. No puntúa por sí sola, pero alimenta los criterios 3 y 4.

| Entregable (según la ficha) | Azul | Amarillo |
|---|:-:|:-:|
| Carga una muestra de datos (la del dataset de arranque u otra) | ☐ | ☐ |
| Permite definir hipótesis de suministro y transporte | ☐ | ☐ |
| Propone una asignación planta → tienda | ☐ | ☐ |
| Segmenta las tiendas y les asigna un nivel teórico de suministro | ☐ | ☐ |
| Agrupa las tiendas en rutas con su secuencia de visita | ☐ | ☐ |
| Indica el tipo y la capacidad de los vehículos a contratar | ☐ | ☐ |
| Dibuja las rutas sobre un mapa | ☐ | ☐ |
| Compara escenarios: km, tiempo, ocupación, coste, emisiones y nivel de servicio | ☐ | ☐ |
| Toma la red actual como escenario de referencia | ☐ | ☐ |

## Criterios

### 1. Supuestos explícitos y separación de lo real y lo estimado · 20 %

*Ficha:* «que el prototipo explique sus supuestos [...] y diferencie los resultados calculados con datos reales de los obtenidos con parámetros estimados».

| Nota | Descriptor |
|:-:|---|
| 1 | No se sabe qué dato es real y cuál inventado. Los supuestos no aparecen o están enterrados en el código. |
| 2 | Hay una lista de supuestos en las diapositivas, pero la herramienta no la muestra. Las etiquetas son parciales. |
| 3 | La herramienta muestra los supuestos principales y los datos llevan etiquetas (real, estimado o sintético), aunque los resultados no heredan la etiqueta. |
| 4 | Cada dato y cada parámetro tiene su etiqueta y su fuente. Los indicadores dicen si dependen de datos estimados o sintéticos. |
| 5 | Lo anterior, y además el equipo sabe decir qué resultados cambiarían si un supuesto fuera falso y qué dato real pediría a Moda re- para cerrarlo. |

### 2. Hipótesis modificables y escenarios · 15 %

*Ficha:* «permita modificarlos con facilidad»; «diseñar y comparar escenarios».

| Nota | Descriptor |
|:-:|---|
| 1 | Hay un único resultado fijo. Cambiar algo exige tocar el código. |
| 2 | Algunos parámetros se pueden cambiar en un archivo de configuración y volviendo a ejecutar. |
| 3 | Desde la interfaz se cambian los parámetros clave (frecuencias, flota, tarifas, asignación fija o flexible) y se recalcula. |
| 4 | Lo anterior, y además se guardan varios escenarios con nombre y se pueden añadir tiendas o plantas nuevas (por ejemplo, una tienda en Albacete o la planta de Asturias). |
| 5 | Lo anterior, y además un planificador sin conocimientos técnicos crea un escenario nuevo en menos de 2 minutos durante la demo. |

### 3. Núcleo de optimización y analítica · 25 %

*Ficha:* «el núcleo técnico del reto será la combinación de analítica de datos, optimización matemática y simulación». Las piezas son la segmentación, la asignación, las rutas (VRP), la selección de flota y los escenarios.

| Nota | Descriptor |
|:-:|---|
| 1 | No hay optimización: las rutas se hacen a mano o la asignación es arbitraria. (Si el núcleo es un modelo de lenguaje, se aplica el ajuste «el núcleo es un chatbot».) |
| 2 | Hay heurísticas sencillas (vecino más cercano, la planta más próxima) sin restricciones de capacidad ni de horario. |
| 3 | Hay un VRP con capacidad resuelto con un solver o una heurística razonable, una segmentación con reglas claras y una asignación por coste o distancia. |
| 4 | Lo anterior, y además se respetan la capacidad, la ventana de lunes a viernes y la jornada; se elige la flota entre varios tipos y tarifas; y las piezas están conectadas (la segmentación determina la demanda, la demanda las rutas y las rutas la flota). |
| 5 | Lo anterior, y además el equipo justifica sus decisiones de modelado (distancias, unidades, el porqué del solver), modela la carga en kg, m³ y palés y muestra cuál de las tres limita en cada ruta, conoce sus límites y comprueba que los resultados son coherentes (por ejemplo, que la ocupación nunca supera el 100 %). |

### 4. Comparación de escenarios con indicadores · 15 %

*Ficha:* «comparación de escenarios mediante kilómetros, tiempo, ocupación, coste estimado, emisiones y cumplimiento del nivel de servicio», con la red actual como referencia y «bajo supuestos comunes».

| Nota | Descriptor |
|:-:|---|
| 1 | No hay comparación, o se compara contra algo que no es la red actual. |
| 2 | Se compara un solo indicador, normalmente los kilómetros. |
| 3 | Hay al menos 4 de los 6 indicadores en una tabla, frente a la red actual. |
| 4 | Están los 6 indicadores, con los mismos supuestos en todos los escenarios, y se ve el efecto de cambiar la asignación, la frecuencia o la flota. |
| 5 | Lo anterior, y además el equipo presenta las diferencias como comparación prospectiva, sin hablar de «ahorros reales» ni presentar como hallazgo un ahorro que depende de datos sintéticos (por ejemplo, de la asignación actual), y explica los compromisos entre indicadores (por ejemplo, más servicio implica más kilómetros). |

### 5. Utilidad y continuidad para Moda re- · 15 %

*Ficha:* el usuario es quien planifica la distribución y el siguiente paso es «completar la captura de datos operativos y probarlo con una zona y un periodo reales». La Fundación busca que haya continuidad con voluntarios.

| Nota | Descriptor |
|:-:|---|
| 1 | Solo lo puede usar el equipo que lo ha hecho. |
| 2 | Funciona, pero hace falta instalar cosas raras o editar código para usarlo. |
| 3 | Se arranca con un comando o una URL, tiene un README y acepta datos en un formato sencillo (CSV o Excel). |
| 4 | Lo anterior, y además deja claro qué datos debería empezar a recoger Moda re- y cómo cargarlos. Responde a casos concretos que plantee la ONG. |
| 5 | Lo anterior, y además propone un piloto concreto (zona, periodo y datos) y el código lo podría mantener un voluntario: es legible y tiene pocas dependencias. |

### 6. Demo y comunicación · 10 %

| Nota | Descriptor |
|:-:|---|
| 1 | No hay demo en vivo, o la demo falla y no hay plan B. |
| 2 | La demo es un vídeo o unas capturas, y el relato se pierde. |
| 3 | La demo en vivo funciona, se ajusta al tiempo y el mensaje se entiende. |
| 4 | La demo cuenta una historia (situación actual, propuesta y diferencia) y el equipo responde con soltura. |
| 5 | Lo anterior, y además alguien de la ONG entendería qué hacer el lunes con la herramienta. |

## Ajustes sobre el total

| Ajuste | Cuándo se aplica |
|---|---|
| **El núcleo es un chatbot:** el criterio 3 tiene como nota máxima 2 | Si un modelo de lenguaje decide la asignación, las rutas o la flota, en lugar de explicar o normalizar. La ficha dice que la IA generativa «no es necesaria para resolver el problema principal». |
| **Ahorros sin base:** −5 puntos | Si se afirma que se ahorran X € o X km «frente a hoy» como si fuera un dato medido. La ficha lo excluye mientras no haya una línea base histórica. |
| **Predicción de demanda con aprendizaje automático sobre datos inventados:** −5 puntos | Si se presenta como resultado. La ficha la deja fuera del alcance. |
| **Uso justificado de la IA generativa:** +3 puntos como máximo | Si se usa para normalizar datos desordenados de la ONG o para explicar un escenario en lenguaje natural, sobre resultados calculados por el motor. |
