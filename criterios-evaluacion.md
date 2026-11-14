# Cómo se evalúa · Reto Moda re-

**Reto:** «Optimización de la red de distribución entre plantas y tiendas» (Moda re-, IA 4 Good Lab, Fundación Ingenieros ICAI) · **Pitch y demo:** domingo 15/11/2026, de 16:00 a 17:30 · **Jurado:** los mentores del hackathon y, si la Fundación lo confirma, alguna persona más.

El jurado valora seis criterios, cada uno con su peso. Están sacados de lo que pide la ficha oficial del reto y, sobre todo, de lo que la ficha dice que «se valorará especialmente»: que el prototipo **explique sus supuestos**, que **permita modificarlos con facilidad** y que **diferencie lo calculado con datos reales de lo obtenido con parámetros estimados**.

En la demo pesa más lo que se ve funcionar en directo que lo que se cuenta en las diapositivas. El jurado puede pediros una prueba sobre la herramienta durante la demo.

## Resumen

| # | Criterio | Peso |
|:-:|---|:-:|
| 1 | Supuestos explícitos y separación de lo real y lo estimado | 20 % |
| 2 | Hipótesis modificables y escenarios | 15 % |
| 3 | Núcleo de optimización y analítica | 25 % |
| 4 | Comparación de escenarios con los 6 indicadores | 15 % |
| 5 | Utilidad y continuidad para Moda re- | 15 % |
| 6 | Demo y comunicación | 10 % |

## 1. Supuestos explícitos y separación de lo real y lo estimado · 20 %

Muchos datos del reto no existen todavía y hay que suponerlos. Eso está bien siempre que se vea. Se valora que:

- cada dato y cada parámetro lleve su etiqueta (**REAL**, **ESTIMADO** o **SINTÉTICO**) y su fuente, y que la herramienta la muestre, no solo las diapositivas;
- los resultados digan si dependen de datos estimados o sintéticos;
- sepáis explicar qué resultado cambiaría si un supuesto fuera falso y qué dato real le pediríais a Moda re- para cerrarlo.

## 2. Hipótesis modificables y escenarios · 15 %

La herramienta tiene que servir para preguntar «¿y si…?». Se valora que:

- los parámetros clave (frecuencias de entrega, flota, tarifas, asignación fija o libre, plantas activas) se cambien desde la interfaz y se recalcule, sin tocar código;
- se puedan guardar varios escenarios con nombre;
- se puedan añadir tiendas o plantas nuevas (por ejemplo, una tienda en Albacete o la futura planta de Asturias);
- una persona sin perfil técnico, como un planificador de Moda re-, pueda crear un escenario nuevo en un par de minutos.

## 3. Núcleo de optimización y analítica · 25 %

Es el criterio que más pesa: el reto es de analítica, optimización y simulación, no de IA generativa. Se valora que:

- haya optimización de verdad en las piezas del problema: segmentación de tiendas, asignación de cada tienda a una planta, rutas de reparto con capacidad (VRP) y elección de vehículos;
- se respeten las restricciones reales: capacidad de los vehículos y de las plantas, días y horarios de recepción, jornada del conductor;
- las piezas estén conectadas: la segmentación determina la demanda, la demanda las rutas y las rutas la flota;
- sepáis justificar vuestras decisiones de modelado (por qué ese método o ese solver, cómo medís las distancias, qué unidad limita la carga) y comprobéis que los resultados tienen sentido (por ejemplo, que ningún camión va por encima del 100 %).

Si un modelo de lenguaje es quien decide la asignación, las rutas o la flota, este criterio queda muy limitado. La IA generativa sí suma si se usa para limpiar datos desordenados o para explicar un escenario a partir de los números que calcula vuestro motor.

## 4. Comparación de escenarios con los 6 indicadores · 15 %

La ficha pide comparar escenarios con **seis indicadores**, siempre frente a la **red actual** y con los **mismos supuestos** en todos:

| Indicador | Qué mide |
|---|---|
| Kilómetros | Distancia total que recorren las rutas |
| Tiempo | Horas de conducción y de servicio (carga, descargas, pausas y noches fuera) |
| Ocupación | Lo cargado que va cada vehículo frente a su capacidad (en kg, m³ o palés, la que limite) |
| Coste estimado | Coste del transporte con tarifas de mercado |
| Emisiones | CO₂ equivalente según el vehículo, los km y la carga |
| Nivel de servicio | Parte de la necesidad de cada tienda que se entrega a tiempo y con la frecuencia prevista |

Se valora que estén los seis, que se vea el efecto de cambiar la asignación, la frecuencia o la flota, y que expliquéis los compromisos entre indicadores (por ejemplo, más frecuencia da más servicio pero más kilómetros).

Ojo: como no hay datos históricos, las diferencias son una **comparación con supuestos**, no un ahorro medido. Decir «ahorramos un X % frente a hoy» como si fuera un dato real penaliza.

## 5. Utilidad y continuidad para Moda re- · 15 %

La herramienta tiene que poder usarse y mantenerse después del hackathon. Se valora que:

- arranque con un solo comando o una URL y tenga un README claro;
- acepte datos en un formato sencillo (CSV o Excel);
- deje claro qué datos debería empezar a recoger Moda re- y cómo cargarlos;
- propongáis un piloto concreto (una zona, un periodo y los datos necesarios);
- el código sea legible y con pocas dependencias, para que lo pueda mantener un voluntario.

## 6. Demo y comunicación · 10 %

Se valora que:

- la demo sea en directo, funcione y se ajuste al tiempo;
- cuente una historia: cómo es hoy, qué proponéis y qué diferencia hay;
- respondáis con soltura a las preguntas;
- alguien de Moda re- entienda qué podría hacer con la herramienta el lunes.

## Lo que resta

- Que un chatbot sea el núcleo que decide.
- Presentar ahorros «frente a hoy» como si fueran medidos.
- Predecir la demanda con aprendizaje automático sobre datos inventados: no hay histórico.
