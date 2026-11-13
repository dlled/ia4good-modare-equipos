# Esquema del dataset de arranque · Reto Moda re- (IA 4 Good Lab)

Versión 1.3 · 11/11/2026 (1.3: `subtipo`, horario real con `horario_etiqueta`/`horario_fuente`/`horario_publicado`, factor de rodeo medido 1,26)

Este documento describe los archivos CSV del dataset de arranque que reciben por igual los equipos Azul y Amarillo. Se entiende sin abrir ningún otro archivo.

## Convenciones

- CSV en UTF-8, separador coma, punto decimal, cabecera en `snake_case`, una fila por registro. Los textos con comas van entre comillas dobles.
- Horas en formato `HH:MM`. Fechas en formato `AAAA-MM-DD`. Distancias en km, tiempos en minutos, pesos en kg, volúmenes en m³ y dinero en euros sin IVA.
- Celda vacía significa "sin dato" o "sin límite"; se indica en cada columna.
- Identificadores estables: `PL-xxx` (planta), `TD-nnn` (tienda), `VEH-xxx` (tipo de vehículo), `TAR-xxx` (tarifa).

### Etiquetas de procedencia

La ficha del reto pide distinguir lo real de lo estimado. Todo dato lleva una de estas tres etiquetas:

| Etiqueta | Significado | Qué debe acompañarla |
|---|---|---|
| `REAL` | Dato que procede de Moda re- o de una fuente pública sobre Moda re- (o de una norma, como el reglamento de tiempos de conducción) | Fuente y fecha |
| `ESTIMADO` | Valor razonable de mercado o calculado con un método conocido | Fuente de mercado o método |
| `SINTÉTICO` | Valor inventado para poder trabajar. Editable | Nada; se puede cambiar libremente |

Cuando un archivo mezcla datos de distinta procedencia, cada grupo de columnas tiene su propia columna `*_etiqueta` (y, si hace falta, `*_fuente`). Así una fila puede tener ubicación `REAL` y ventas `SINTÉTICO`. Cuando la ONG facilite un dato real, se sustituye el valor y su etiqueta pasa a `REAL`.

## Archivos

| Archivo | Contenido | Filas aprox. |
|---|---|---|
| `plantas.csv` | Plantas de clasificación (orígenes) | 6 |
| `tiendas.csv` | Tiendas (destinos) con tamaño, ventas, recepción y asignación actual | red completa publicada; columna `en_muestra` para la muestra recomendada |
| `vehiculos.csv` | Tipos de vehículo de la flota estándar de un operador | 5 |
| `tarifas.csv` | Tarifas por operador y tipo de vehículo | ~10 |
| `emisiones.csv` | Factores de emisión por tipo de vehículo | 5 |
| `distancias.csv` | Distancias y tiempos por carretera entre todos los puntos | n·(n−1) |
| `parametros.csv` | Reglas de negocio y supuestos editables | ~30 |

### plantas.csv

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `id_planta` | texto | | `PL-MAD` | Identificador: `PL-MAD`, `PL-VAL`, `PL-BCN`, `PL-BIO`, `PL-AST`, `PL-SCQ` |
| `nombre` | texto | | `Planta Madrid-Vallecas` | |
| `municipio`, `provincia` | texto | | `Madrid`, `Madrid` | |
| `direccion` | texto | | | Vacía si no se conoce |
| `lat`, `lon` | decimal | grados WGS84 | `40.3700`, `-3.6150` | |
| `ubicacion_etiqueta` | etiqueta | | `REAL` | `REAL` si la dirección es pública; `ESTIMADO` si solo se conoce el municipio (se usa su centro) |
| `ubicacion_fuente` | texto | | `URL, consultado 2026-11-11` | |
| `activa` | 0/1 | | `1` | `0` para las plantas que aún no han abierto (Asturias, Santiago) |
| `apertura_prevista` | texto | | `próximamente` | Vacía si ya está abierta. La ONG no ha dado fecha |
| `estado_etiqueta`, `estado_fuente` | | | `REAL`, `Reunión con Noema Paniagua (Moda re-), 2026` | Procedencia de `activa` y `apertura_prevista` |
| `capacidad_salida_kg_semana` | entero | kg/semana | `60000` | Lo que la planta puede enviar a tiendas por semana. Vacía = sin límite |
| `capacidad_etiqueta` | etiqueta | | `SINTÉTICO` | |
| `hora_inicio_carga`, `hora_fin_carga` | hora | | `06:00`, `18:00` | Horas en que pueden salir camiones cargados |
| `carga_etiqueta` | etiqueta | | `SINTÉTICO` | |

### tiendas.csv

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `id_tienda` | texto | | `TD-001` | Identificador |
| `id_fuente` | texto | | | Identificador en la lista pública de origen (para cruzar con datos que mande la ONG) |
| `nombre` | texto | | `Moda re- Córdoba` | |
| `subtipo` | texto | | `tienda_calle` | `tienda_calle` o `corner` (punto de venta dentro de un hipermercado). REAL |
| `empresa_insercion` | texto | | | Empresa de inserción que gestiona la tienda, si se conoce |
| `direccion` | texto | | | Vacía si no se conoce |
| `municipio`, `provincia`, `ccaa` | texto | | `Córdoba`, `Córdoba`, `Andalucía` | |
| `lat`, `lon` | decimal | grados WGS84 | `37.8847`, `-4.7792` | |
| `ubicacion_etiqueta` | etiqueta | | `REAL` | `REAL`: dirección publicada; `ESTIMADO`: municipio real con coordenada aproximada; `SINTÉTICO`: tienda inventada (por ejemplo, una apertura hipotética) |
| `ubicacion_fuente` | texto | | | URL y fecha de consulta |
| `acceso_carretera` | 0/1 | | `1` | `0` = fuera del alcance de rutas por carretera (requiere transporte marítimo: Baleares). Esas tiendas no tienen filas en `distancias.csv` ni están en la muestra. REAL |
| `superficie_m2` | entero | m² | `90` | Superficie de venta (sintética: de 30 a 375 m² con `escala_tiendas` = 0,5) |
| `categoria_tamano` | texto | | `mediana` | `pequeña` / `mediana` / `grande`, derivada de la superficie con `umbral_m2_mediana` y `umbral_m2_grande` de `parametros.csv`. Hereda la etiqueta de la superficie |
| `superficie_etiqueta` | etiqueta | | `SINTÉTICO` | |
| `ventas_periodo` | número | ver `ventas_unidad` | `155000` | Ventas del periodo |
| `ventas_unidad` | texto | | `EUR` | `EUR` (euros) o `INDICE` (100 = tienda media), por si la ONG prefiere no dar euros |
| `periodo_ventas` | texto | | `2025` | Periodo común a todas las tiendas (año natural) |
| `ventas_etiqueta` | etiqueta | | `SINTÉTICO` | |
| `planta_actual` | texto | | `PL-MAD` | Planta que la sirve hoy (escenario de referencia) |
| `asignacion_etiqueta` | etiqueta | | `REAL` | `REAL` solo donde lo ha confirmado la ONG |
| `asignacion_fuente` | texto | | `Moda re-, correo de 13/11/2026` | Para las sintéticas dice cómo se generaron (ver más abajo) |
| `dias_recepcion` | texto | | `L-V` | Días en que acepta entregas |
| `ventana_inicio`, `ventana_fin` | hora | | `10:00`, `14:00` | Ventana de recepción: primer tramo de lunes a viernes del horario comercial publicado. Si no hay horario, la de `parametros.csv` |
| `horario_etiqueta`, `horario_fuente` | | | `REAL` | Procedencia de `dias_recepcion`, `ventana_inicio` y `ventana_fin` |
| `horario_publicado` | texto | | `Lunes-Viernes 10:00 - 14:00 y 17:00 - 20:00. Sábado 10:00 - 14:00` | Horario tal como aparece en la web (REAL) |
| `tiempo_descarga_min` | entero | min | `30` | Tiempo de parada para descargar |
| `vehiculo_max` | texto | | `VEH-R75` | Vehículo más grande que admite el acceso. Vacío = sin restricción |
| `recepcion_etiqueta` | etiqueta | | `SINTÉTICO` | Procedencia de `tiempo_descarga_min` y `vehiculo_max` (los corners de hipermercado no tienen restricción: muelle) |
| `en_muestra` | 0/1 | | `1` | `1` si forma parte de la muestra recomendada para el hackathon |
| `activa` | 0/1 | | `1` | `0` = tienda prevista o cerrada |
| `fecha_alta` | fecha | | `2021-03-01` | Fecha de apertura |
| `fecha_alta_etiqueta` | etiqueta | | `SINTÉTICO` | |

**Cómo se genera la asignación actual sintética.** La reunión con la ONG dejó claro que la asignación actual responde a motivos históricos y políticos, no a la eficiencia. Para que el escenario de referencia se parezca a eso: (1) las asignaciones que la ONG ha confirmado son `REAL` y llevan su fuente; (2) la mayoría de las tiendas se asigna a la planta activa más cercana (`SINTÉTICO`, fuente "generada: planta más cercana"); (3) algunas provincias enteras, y las demás tiendas de una empresa de inserción con asignación confirmada, se asignan a una planta más lejana, como si fueran herencias históricas (`SINTÉTICO`, fuente "generada: desajuste histórico simulado"). Así optimizar la asignación tiene recorrido.

### vehiculos.csv

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `id_tipo` | texto | | `VEH-R12` | `VEH-FUR`, `VEH-R75`, `VEH-R12`, `VEH-R18`, `VEH-ART` |
| `descripcion` | texto | | `Camión rígido 12 t` | |
| `mma_t` | decimal | t | `12` | Masa máxima autorizada |
| `carga_util_kg` | entero | kg | `6000` | |
| `volumen_m3` | decimal | m³ | `36` | Volumen útil de caja |
| `capacidad_palets` | entero | palés europeos | `15` | Palés de 1,2 × 0,8 m que caben. Con ropa suele limitar antes el palé que el peso (ver `kg_por_palet`) |
| `etiqueta`, `fuente` | | | `ESTIMADO` | |

Los tiempos de conducción, pausas y jornada son iguales para todos los vehículos y están en `parametros.csv`. El tiempo de viaje está en `distancias.csv`.

### tarifas.csv

Un mismo tipo de vehículo puede ofrecerlo más de un operador con tarifas distintas.

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `id_tarifa` | texto | | `TAR-A-R12` | |
| `operador` | texto | | `Operador A` | Operadores ficticios |
| `id_tipo` | texto | | `VEH-R12` | Referencia a `vehiculos.csv` |
| `coste_fijo_dia_eur` | decimal | €/día | `255.31` | Se cobra por cada día que dura la ruta (una ruta de 2 días paga 2 veces) |
| `coste_km_eur` | decimal | €/km | `0.4392` | |
| `coste_hora_eur` | decimal | €/h | `31.91` | Coste por hora de servicio del conductor y el vehículo (0 si no aplica) |
| `unidades_disponibles` | entero | vehículos/día | `3` | Vacío = sin límite |
| `etiqueta`, `fuente` | | | `ESTIMADO` | |

La pernocta del conductor en rutas de varios días se suma aparte con `coste_pernocta_eur` de `parametros.csv`.

### emisiones.csv

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `id_tipo` | texto | | `VEH-R12` | |
| `combustible` | texto | | `diésel` | |
| `kgco2e_km_vacio` | decimal | kg CO₂e/km | `0.5506` | Con 0 % de carga |
| `kgco2e_km_lleno` | decimal | kg CO₂e/km | `0.7060` | Con 100 % de carga |
| `etiqueta`, `fuente` | | | `ESTIMADO` | |

Para una ocupación intermedia `o` (de 0 a 1) se interpola: `vacio + o · (lleno − vacio)`.

### distancias.csv

Formato largo: una fila por par ordenado origen → destino entre todas las plantas y las tiendas con `acceso_carretera = 1`. Los pares de la muestra (planta↔tienda y tienda↔tienda con `en_muestra = 1`) van por carretera con OSRM; el resto de la red, con el respaldo haversine × `factor_rodeo`. La columna `metodo` lo dice en cada fila.

| Columna | Tipo | Unidad | Ejemplo | Descripción |
|---|---|---|---|---|
| `origen`, `destino` | texto | | `PL-BCN`, `TD-012` | |
| `distancia_km` | decimal | km | `998.4` | |
| `duracion_min` | decimal | min | `560.0` | Tiempo en turismo según el motor de rutas |
| `duracion_camion_min` | decimal | min | `700.0` | Tiempo en camión: `duracion_min × factor_tiempo_camion` (de `parametros.csv`). **Usad esta** para que los resultados sean comparables |
| `metodo` | texto | | `OSRM` | `OSRM` (por carretera, red de OpenStreetMap) o `HAVERSINE_X<factor>`, p. ej. `HAVERSINE_X1.26` (línea recta × `factor_rodeo`, a `velocidad_respaldo_kmh`) |
| `etiqueta` | etiqueta | | `ESTIMADO` | Siempre `ESTIMADO` |
| `fuente` | texto | | `OSRM (router.project-osrm.org), datos OpenStreetMap, 2026-11-11` | |

### parametros.csv

Columnas: `clave`, `valor`, `unidad`, `etiqueta`, `fuente`, `descripcion`. Es la fuente única de los supuestos: si un valor cambia, se cambia aquí.

| Clave | Valor | Unidad | Etiqueta | Para qué sirve |
|---|---|---|---|---|
| `precio_medio_eur_kg` | 12 | €/kg | SINTÉTICO | Pasar de € vendidos a kg: `kg_semana = ventas_periodo / precio_medio_eur_kg / semanas_venta_anio` |
| `semanas_venta_anio` | 50 | semanas | SINTÉTICO | Semanas de apertura al año |
| `ventas_media_eur_tienda` | 150000 | €/año | SINTÉTICO | Solo si `ventas_unidad = INDICE`: € = índice / 100 × este valor |
| `kg_por_palet` | 250 | kg/palé | SINTÉTICO | Kg de ropa clasificada por palé o unidad de carga equivalente |
| `densidad_kg_m3` | 150 | kg/m³ | SINTÉTICO | Para limitar por volumen: m³ = kg / densidad. Con ropa, desde el rígido de 12 t limita antes el volumen o los palés que el peso |
| `umbral_m2_mediana` | 75 | m² | SINTÉTICO | Desde aquí la tienda es mediana |
| `umbral_m2_grande` | 175 | m² | SINTÉTICO | Desde aquí la tienda es grande |
| `escala_tiendas` | 0,5 | | SINTÉTICO | Escala de las superficies sintéticas, y con ellas de las ventas (1 = 60-750 m²; 0,5 = 30-375 m²). Misma semilla, mismas tiendas a otra escala |
| `entregas_semana_pequeña` / `_mediana` / `_grande` | 0,5 / 1 / 2 | entregas/semana | SINTÉTICO | Frecuencia de reposición por categoría |
| `max_palets_entrega_pequeña` / `_mediana` / `_grande` | 2 / 4 / 8 | palés | SINTÉTICO | Lo que cabe en la tienda por entrega. Límite semanal = frecuencia × palés × kg/palé (pequeña: 250 kg/semana) |
| `dias_reparto_semana` | 5 | días | REAL | Lunes a viernes (ficha del reto) |
| `ventana_inicio_defecto` / `ventana_fin_defecto` | 10:00 / 14:00 | HH:MM | SINTÉTICO | Ventana de recepción por defecto |
| `tiempo_descarga_min` | 30 | min | SINTÉTICO | Parada por tienda |
| `tiempo_carga_planta_min` | 45 | min | SINTÉTICO | Carga en planta antes de salir |
| `vehiculo_max_centro_urbano` | VEH-R75 | id_tipo | SINTÉTICO | Vehículo máximo en centro urbano (≤7,5 t) |
| `conduccion_max_dia_h` | 9 | h | REAL | Conducción diaria máxima (Reglamento (CE) 561/2006) |
| `pausa_min_cada_4_5h` | 45 | min | REAL | Pausa obligatoria tras 4,5 h de conducción (mismo reglamento) |
| `jornada_max_h` | 13 | h | ESTIMADO | Jornada total del conductor (conducción + pausas + cargas, descargas y esperas); 24 h − 11 h de descanso diario del mismo reglamento. Para un escenario prudente, 11 h |
| `permitir_rutas_multidia` | 1 | 0/1 | SINTÉTICO | Si vale 1, una ruta puede durar varios días con pernocta, como hace un operador de larga distancia |
| `dias_max_ruta` | 3 | días | SINTÉTICO | Días desde la salida de planta hasta la última entrega; la vuelta a planta en vacío no cuenta para el límite, pero suma km, coste, CO2 y pernoctas. Debe caber en L-V |
| `coste_pernocta_eur` | 93 | €/noche | ESTIMADO | Dietas y alojamiento del conductor por noche fuera (Observatorio de Costes, enero 2026) |
| `multiplicador_tarifas` | 1 | | SINTÉTICO | Multiplica todas las tarifas para escenarios de precio (1,089 ≈ actualización a julio 2026) |
| `factor_tiempo_camion` | 1,2 | | ESTIMADO | Camión frente a turismo, calibrado con OSRM (turismo ≈ 89 km/h en tramos >100 km) → camión ≈ 74 km/h. Tras cambiarlo: `python3 scripts/datos.py distancias --solo-tiempos` |
| `factor_rodeo` | 1,26 | | ESTIMADO | Carretera frente a línea recta (mediana medida con OSRM), solo para el respaldo sin OSRM |
| `velocidad_respaldo_kmh` | 90 | km/h | ESTIMADO | Velocidad de turismo para el respaldo sin OSRM (mediana medida con OSRM) |
| `kg_retorno_por_kg_entregado` | 0,3 | kg/kg | SINTÉTICO | Logística inversa: sacas, jaulas o género no vendido que puede volver a planta |
| `nivel_servicio_def` | texto | | SINTÉTICO | Definición única: «% de la necesidad semanal en kg de cada tienda entregada dentro de su ventana de recepción y con la frecuencia objetivo de su segmento; por tienda y media de la red ponderada por kg». Pendiente de validar por Moda re- |
| `nivel_servicio_objetivo` | 0,95 | fracción | SINTÉTICO | Objetivo de nivel de servicio |
| `horizonte_planificacion_dias` | 5 | días | SINTÉTICO | Días laborables que se planifican (una semana) |

## Script de mantenimiento

`scripts/datos.py` (Python 3, solo biblioteca estándar). Desde la carpeta `data/`:

| Comando | Qué hace |
|---|---|
| `python3 scripts/datos.py sinteticos --semilla 2026` | Regenera los valores `SINTÉTICO` de tiendas y plantas (superficie, ventas, asignación, recepción, fecha de alta, capacidad). No toca lo `REAL` |
| `python3 scripts/datos.py anadir-tienda --nombre "Moda re- Albacete" --municipio Albacete --provincia Albacete --lat 38.994 --lon -1.858` | Añade una tienda (lo que no se indique se rellena como `SINTÉTICO`) y calcula sus distancias |
| `python3 scripts/datos.py distancias` | Calcula los pares que falten en `distancias.csv` (OSRM para la muestra en una sola petición; resto y respaldo, haversine × `factor_rodeo`) |
| `python3 scripts/datos.py validar` | Comprueba identificadores, etiquetas, matriz completa y que la demanda cabe en los límites por categoría |
| `python3 scripts/datos.py importar --raw fuentes/ubicaciones_raw.csv` | Reconstruye plantas y tiendas desde la lista pública (copia en `fuentes/`), conservando los `id_tienda`, y regenera lo sintético |
| `python3 scripts/datos.py cargar-ong --archivo respuesta.csv --fuente "…"` | Carga datos reales de la ONG (superficie, ventas, planta actual, ventanas) por `id_tienda`, `id_fuente` o `nombre`, y los marca `REAL` |
| `python3 scripts/datos.py sinteticos --sin-confirmadas` | Ignora las asignaciones confirmadas de `fuentes/asignaciones_confirmadas.csv` y asigna todas las tiendas de forma sintética |

## Lo que el dataset NO trae, a propósito

La demanda en kg por tienda, la frecuencia elegida y la segmentación no vienen calculadas: son parte del trabajo de los equipos. `parametros.csv` trae un punto de partida editable para que nadie se bloquee.
