# Brief de arranque · Reto Moda re- · Equipos Azul y Amarillo

**IA 4 Good Lab, Fundación Ingenieros ICAI** · sábado 14 y domingo 15 de noviembre de 2026 · Mentores: Dani Lledó y David Soler

## El reto en tres líneas

Moda re- (Cáritas) clasifica ropa usada en sus plantas y la vende en unas 190 tiendas de toda España. Hoy cada tienda recibe de una planta asignada por motivos históricos, y cada empresa de inserción contrata su propio transporte, sin coordinación. Hay tiendas que reciben desde plantas muy lejanas, cada una por su lado.

**Pregunta:** ¿cómo abastecer bien las tiendas con menos kilómetros, menos coste y mejor uso de la capacidad de transporte contratada?

## Qué tenéis que entregar el domingo

Un **prototipo de apoyo a la planificación** que cargue los datos, deje definir las hipótesis y proponga un plan para una semana con:

1. la asignación planta → tienda;
2. la segmentación de las tiendas y su nivel de suministro;
3. las rutas, con la secuencia de visita;
4. el tipo, la capacidad y el número de vehículos a contratar;
5. las rutas sobre un mapa;
6. la comparación de escenarios frente a la red actual: km, tiempo, ocupación, coste, emisiones y nivel de servicio.

**Nivel de servicio** (definición **sintética**, pendiente de que la valide Moda re-): el porcentaje de la necesidad semanal en kg de cada tienda que se entrega dentro de su ventana de recepción y con la frecuencia objetivo de su segmento, por tienda y como media de la red ponderada por kg.

Lo que más se valorará, según la ficha del reto: que **explique sus supuestos**, que **se puedan cambiar con facilidad** y que **distinga lo calculado con datos reales de lo calculado con datos estimados**.

## El dataset de arranque

Lo reciben igual los dos equipos. Son CSV en UTF-8, con distancias en km, tiempos en minutos, pesos en kg y dinero en euros sin IVA.

| Archivo | Qué trae |
|---|---|
| `plantas.csv` | Plantas de origen; las aún no abiertas (Asturias, Santiago) aparecen marcadas como inactivas |
| `tiendas.csv` | Toda la red peninsular: ubicación, superficie, ventas, planta actual, ventana de recepción y vehículo máximo que admite el acceso. Una columna marca la muestra recomendada |
| `vehiculos.csv` | Tipos de vehículo: capacidad en kg, m³ y palés, velocidad y jornada |
| `tarifas.csv` | Tarifas por operador y vehículo: fijo por día, por km y por hora, y unidades disponibles |
| `emisiones.csv` | kg CO₂e/km en vacío y lleno; para cargas intermedias se interpola |
| `distancias.csv` | Distancias y tiempos por carretera entre todos los puntos (estimados). Para camión, usad `duracion_camion_min`, no la duración de turismo |
| `parametros.csv` | Fuente única de reglas y supuestos editables: precio medio por kg, kg por palé, densidad de la ropa (kg/m³), umbrales de tamaño, frecuencias por segmento, ventana por defecto, conducción máxima, rutas de varios días y pernocta, nivel de servicio objetivo… |

El documento del esquema del dataset (`ESQUEMA.md`) describe cada columna. Un pequeño script en Python (`scripts/datos.py`) añade tiendas nuevas con sus distancias, regenera los valores sintéticos y valida el dataset.

**Cada dato lleva una etiqueta**, y vuestra herramienta debe conservarla y enseñarla:

- **REAL:** viene de Moda re- o de su web pública. Lleva fuente y fecha.
- **ESTIMADO:** valor de mercado o calculado con un método conocido. Lleva la fuente.
- **SINTÉTICO:** inventado para poder trabajar. Cambiadlo con libertad.

**Una pista:** el sur de España queda a más de una jornada de conducción de cualquier planta. Vuestro modelo tendrá que manejar rutas de varios días. Y las 7 tiendas de Baleares están marcadas en el dataset como fuera del alcance de las rutas por carretera.

**Lo que no trae, a propósito:** la demanda en kg de cada tienda, la frecuencia de entrega y la segmentación. Eso lo construís vosotros con reglas a partir del tamaño y las ventas.

## Cómo os proponemos empezar

1. **Primera hora:** leed la ficha, abrid el dataset y elegid el alcance. Con la muestra y una o dos plantas basta.
2. **Fijad los supuestos y etiquetadlos.** Si una duda dura más de 15 minutos, fijad un valor, marcadlo como SINTÉTICO, hacedlo editable y seguid.
3. **Primero el flujo completo, aunque sea tosco:** datos → necesidad por tienda → asignación → rutas → flota → indicadores. La interfaz y el mapa, después.
4. **Calculad la red actual con el mismo motor y los mismos supuestos** que las alternativas. Es vuestro escenario de referencia.
5. **El domingo, mejorad y preparad la demo.** Congelad funcionalidades a las 13:30, antes de comer, y ensayad entre las 14:30 y las 15:30.

## Reglas del juego

- **El núcleo es optimización y analítica**, no IA generativa: segmentación, asignación, rutas de vehículos (VRP), selección de flota y escenarios. Usad la IA generativa para construir más rápido y, si queréis, para limpiar datos desordenados o explicar un escenario a partir de los números de vuestro motor. Un chatbot que decide las rutas no resuelve el reto.
- **Nada de predecir la demanda con aprendizaje automático:** no hay histórico.
- **Nada de «ahorramos un X % frente a hoy»:** es una comparación prospectiva con supuestos comunes, no un ahorro medido.
- **Tecnología libre:** usad la que mejor dominéis; no hay ningún lenguaje ni herramienta obligatoria.
- **Pensad en quien lo use después:** un planificador de Moda re- y voluntarios que lo mantengan. Un README con un único comando de arranque y la posibilidad de añadir una tienda nueva (por ejemplo, en Albacete).

## Calendario

| Cuándo | Qué |
|---|---|
| Sáb 09:00-10:15 | Recepción, bienvenida, presentación de los retos por las ONG y organización de los equipos |
| Sáb 10:15-12:00 | Análisis del reto e ideación |
| **Sáb 12:00-12:30** | **Primera validación de propuestas con las ONG:** traed una propuesta que se pueda contar en 3 minutos |
| Sáb 12:30-14:00 | Desarrollo |
| Sáb 14:00-15:15 | Comida y presentación de la Fundación |
| Sáb 15:15-18:30 | Desarrollo con los mentores |
| **Sáb 18:30-19:00** | **Revisión de avances con mentores y ONG:** traed un flujo de punta a punta |
| Dom 09:00-11:30 | Apertura y desarrollo |
| **Dom 11:30-12:00** | **Segunda validación con las ONG:** la red actual frente a vuestra propuesta |
| Dom 12:00-13:30 | Ajustes y preparación de la presentación. **Congelad funcionalidades a las 13:30**, antes de comer |
| Dom 14:30-15:30 | Ensayo de la presentación y entrega de la documentación |
| Dom 15:30-16:00 | Preparación de la demo y cierre de entregas |
| **Dom 16:00-17:30** | **Pitch y demo:** unos 15 minutos por equipo |
| Dom 17:30-19:00 | Deliberación del jurado, premios y clausura |

## Cómo se evalúa

| Criterio | Peso |
|---|:-:|
| Supuestos explícitos y separación de lo real y lo estimado | 20 % |
| Hipótesis modificables y escenarios | 15 % |
| Núcleo de optimización y analítica | 25 % |
| Comparación de escenarios con los 6 indicadores | 15 % |
| Utilidad y continuidad para Moda re- | 15 % |
| Demo y comunicación | 10 % |

Cómo se evalúa: [`criterios-evaluacion.md`](criterios-evaluacion.md). Si os bloqueáis, llamadnos: estamos para eso.
