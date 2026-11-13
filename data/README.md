# Dataset de arranque · Reto Moda re- (IA 4 Good Lab)

Datos de partida para el reto **«Optimización de la red de distribución entre plantas y tiendas»** de Moda re-. Es el mismo dataset para los dos equipos (Azul y Amarillo). Podéis cambiar cualquier valor `SINTÉTICO` o `ESTIMADO`. Lo importante es que vuestra herramienta deje claro qué resultados salen de datos reales y cuáles de supuestos.

> Versión 1 · 11/11/2026 · 6 plantas (4 activas y 2 futuras) · 182 tiendas (156 de calle y 26 corners en hipermercados; 7 en Baleares sin acceso por carretera) · muestra recomendada de 53 tiendas · 32.580 pares de distancias

## Qué hay aquí

| Archivo | Qué contiene |
|---|---|
| `plantas.csv` | Las 4 plantas de clasificación activas (Madrid-Vallecas, Valencia, Barcelona, Bilbao) y las 2 que abrirán pronto (Asturias, Santiago de Compostela), desactivadas con `activa = 0` |
| `tiendas.csv` | Las 182 tiendas publicadas en la web de Moda re-, con ubicación, tipo (`tienda_calle` o `corner` en hipermercado), superficie, ventas anuales, ventana de recepción y la planta que las sirve hoy. La columna `en_muestra = 1` marca la **muestra recomendada** |
| `vehiculos.csv` | Cinco tipos de vehículo, de furgoneta a tráiler: carga útil, volumen y palés |
| `tarifas.csv` | Lo que cobran dos operadores ficticios por cada tipo de vehículo |
| `emisiones.csv` | kg de CO₂e por km de cada vehículo, vacío y lleno |
| `distancias.csv` | Distancia y tiempo por carretera entre todos los pares de puntos (plantas y tiendas) |
| `parametros.csv` | Todas las reglas de negocio y supuestos editables: kg por palé, frecuencias, ventanas, jornada del conductor, nivel de servicio… |
| `ESQUEMA.md` | Descripción de cada columna, con unidades y ejemplos |
| `scripts/datos.py` | Script para añadir tiendas, recalcular distancias y regenerar los datos sintéticos |

Todos los CSV están en UTF-8, separados por comas y con punto decimal. Se abren en Excel, Google Sheets, pandas o cualquier lenguaje.

## Real, estimado y sintético

La ficha del reto pide distinguir lo real de lo supuesto. Cada dato lleva una etiqueta, ya sea en una columna `etiqueta` o en columnas `*_etiqueta` por grupo de datos:

- **REAL**: viene de Moda re- (su web pública, la ficha del reto o la reunión con la ONG) o de una norma. Lleva fuente y fecha.
- **ESTIMADO**: valor de mercado o calculado con un método conocido (Observatorio de Costes del Ministerio de Transportes, factores de emisión de DEFRA, motor de rutas OSRM). Lleva su fuente.
- **SINTÉTICO**: inventado para poder trabajar. Cambiadlo sin miedo.

Resumen de lo que hay hoy:

| Dato | Etiqueta |
|---|---|
| Qué plantas están abiertas o pendientes | REAL. La «Barcelona» de la ficha está en Sabadell, la «Bilbao» en Mungia y la «Valencia» en Riba-roja de Túria |
| Ubicación de plantas y tiendas | REAL (web de Moda re-, 11/11/2026), salvo 2 tiendas con solo el municipio (ESTIMADO) y la planta de Asturias, sin ubicación pública (SINTÉTICO, en Siero); ver `ubicacion_etiqueta` |
| Superficie, ventas y fecha de apertura de las tiendas | SINTÉTICO |
| Planta que sirve hoy a cada tienda | SINTÉTICO, salvo las asignaciones que la ONG haya confirmado (REAL, con fuente); ver `asignacion_etiqueta` |
| Días y ventana de recepción | REAL: primer tramo de lunes a viernes del horario comercial publicado (`horario_publicado`). La ficha dice que se recibe en horario comercial. Una tienda con horario irregular usa la ventana por defecto (SINTÉTICO) |
| Tiempo de descarga y vehículo máximo por tienda | SINTÉTICO |
| Capacidad y horario de carga de las plantas | SINTÉTICO |
| Carga útil de vehículos, tarifas, pernocta | ESTIMADO (Observatorio de Costes, enero 2026) |
| Emisiones | ESTIMADO (DEFRA 2025) |
| Distancias y tiempos | ESTIMADO (OSRM o línea recta × 1,26; ver `metodo`) |
| Tiempos de conducción y descanso | REAL (Reglamento (CE) 561/2006) |

## Por dónde empezar

1. **Trabajad con la muestra** (`en_muestra = 1`): 53 tiendas de Madrid, Castilla-La Mancha, Comunitat Valenciana, Región de Murcia, Extremadura y Andalucía. Las distancias entre las 6 plantas y estas tiendas, y entre ellas, son por carretera (OSRM). La ficha dice que para 20 horas basta con una o dos plantas y un conjunto acotado de tiendas. La red completa está para quien quiera escalar.
2. **Calculad la necesidad de cada tienda.** No viene hecha: es parte del reto. Un punto de partida con `parametros.csv`:
   `kg por semana = ventas_periodo / precio_medio_eur_kg / semanas_venta_anio`
   y de ahí, palés con `kg_por_palet`. Con los valores de partida, las tiendas tienen de 30 a 375 m² (mediana de 91 m²), venden una mediana de 80.000 € al año y necesitan unos 130 kg por semana (mediana); la red entera, unas 34 t por semana. Si os parece que la escala no encaja, cambiad `escala_tiendas` y regenerad. Cada categoría de tamaño (`pequeña`, `mediana`, `grande`) tiene una frecuencia de entrega y un máximo de palés por entrega. Con los valores por defecto, la demanda de todas las tiendas cabe en esos límites.
3. **El escenario de referencia** es la asignación de `planta_actual`. No es la más eficiente: la ONG cuenta que viene de motivos históricos y políticos, así que la asignación actual incluye casos históricos poco eficientes. La columna `asignacion_etiqueta` dice cuáles son reales y cuáles sintéticos. Comparad vuestras alternativas contra este escenario con los mismos supuestos.
4. **Usad `duracion_camion_min`** de `distancias.csv` para los tiempos de viaje (es la duración en turismo × `factor_tiempo_camion`). Así los resultados de los dos equipos son comparables.

## Reglas de transporte que conviene conocer

- **Rutas de varios días.** Desde ninguna planta se llega a Andalucía, se entrega y se vuelve en una jornada (Madrid → Sevilla son unos 530 km). Por eso `permitir_rutas_multidia = 1`: una ruta puede durar hasta `dias_max_ruta` días, contados desde la salida de planta hasta la última entrega, con el conductor durmiendo fuera (la vuelta en vacío no cuenta para el límite, pero sí suma km, coste, CO₂ y pernoctas), como hace cualquier operador de larga distancia. Cada noche fuera cuesta `coste_pernocta_eur`. El conductor no puede pasar de `conduccion_max_dia_h` horas de volante al día, con una pausa de `pausa_min_cada_4_5h` minutos cada 4,5 h, y su jornada total (conducción, pausas, cargas y descargas) no pasa de `jornada_max_h`.
- **Cómo se cobra.** El *Operador A* cobra por km (`coste_km_eur`) y por hora de servicio (`coste_hora_eur`). El *Operador B* cobra un fijo por cada día de ruta (`coste_fijo_dia_eur`) más los km, tiene pocos vehículos (`unidades_disponibles`) y no tiene tráileres. Las dos tarifas salen del mismo coste del Observatorio más un 8 % de margen; cambia la forma de cobrar. Para simular subidas de precio, usad `multiplicador_tarifas`.
- **Capacidad.** Con ropa se llena antes el espacio que el peso: con `densidad_kg_m3` = 150, del rígido de 12 t hacia arriba limita el volumen (o los palés), no los kg. Limitad por kg, m³ y palés, y tomad como ocupación la mayor de las tres.
- **Acceso.** `vehiculo_max` dice el vehículo más grande que puede llegar a cada tienda: en ciudades grandes, como mucho un rígido de 7,5 t; en el resto, un rígido de 12 t. Los corners de hipermercado (`subtipo = corner`) no tienen límite porque tienen muelle.
- **Emisiones.** Interpolad entre `kgco2e_km_vacio` y `kgco2e_km_lleno` según la ocupación en peso.
- **Nivel de servicio** (`nivel_servicio_def`): % de la necesidad semanal en kg de cada tienda entregada dentro de su ventana de recepción y con la frecuencia objetivo de su segmento; por tienda y media de la red ponderada por kg. El objetivo por defecto es `nivel_servicio_objetivo`.
- **Logística inversa.** `kg_retorno_por_kg_entregado` estima lo que podría volver a planta en el viaje de vuelta. La ONG dice que hoy no se aprovecha.

## Añadir una tienda nueva

La herramienta tiene que admitir tiendas nuevas (Moda re- abre unas 15 al año). Hay dos formas:

- **A mano:** añadid una fila a `tiendas.csv` y calculad sus distancias como queráis.
- **Con el script** (Python 3, sin instalar nada), desde esta carpeta:

```bash
python3 scripts/datos.py anadir-tienda --nombre "Moda re- Albacete" --municipio Albacete \
  --provincia Albacete --lat 38.994 --lon -1.858 --en-muestra
```

El script le asigna el siguiente `TD-nnn`, rellena como `SINTÉTICO` lo que no le digáis (superficie, ventas, planta, ventana) y calcula sus distancias (por carretera si está en la muestra y hay conexión; si no, en línea recta × `factor_rodeo`). Admite `--superficie`, `--ventas`, `--planta` y `--direccion`. Después, `python3 scripts/datos.py validar` comprueba que todo cuadra.

Otros comandos:

| Comando | Para qué |
|---|---|
| `python3 scripts/datos.py sinteticos --semilla 7` | Genera otro juego de superficies, ventas y asignaciones sintéticas (lo REAL no cambia). Útil para probar la robustez de vuestra solución |
| `python3 scripts/datos.py distancias` | Calcula los pares de distancias que falten |
| `python3 scripts/datos.py distancias --solo-tiempos` | Recalcula `duracion_camion_min` si cambiáis `factor_tiempo_camion` |
| `python3 scripts/datos.py validar` | Comprueba identificadores, etiquetas, distancias completas y límites de demanda |

Con la misma semilla, el resultado es siempre el mismo.

## Limitaciones que debéis conocer

- Las 7 tiendas de Baleares están en `tiendas.csv` con `acceso_carretera = 0`: quedan fuera del alcance de rutas por carretera (requieren transporte marítimo), no tienen distancias y no están en la muestra.
- La web publica 182 tiendas; la ficha habla de unas 190 y la ONG de unas 192. La lista pública puede no estar completa.
- La planta de Asturias no tiene ubicación pública: está en Siero como supuesto (SINTÉTICO). La de Madrid está geolocalizada a nivel de polígono.
- Las distancias fuera de la muestra son en línea recta × 1,26 (factor medido con OSRM en 160 pares). Valen para comparar órdenes de magnitud, no para rutas finas.
- Las ventas, las superficies y la asignación actual son inventadas. Las conclusiones del tipo «ahorraríamos X €» valen como comparación entre escenarios con los mismos supuestos, no como ahorro real (lo dice la ficha).
- Los factores de emisión son británicos (DEFRA); se usan como referencia europea.

## Créditos

- Ubicaciones de tiendas y plantas: web pública de Moda re- (URL y fecha en cada fila).
- Distancias por carretera: [OSRM](https://project-osrm.org/) con datos de © colaboradores de OpenStreetMap (licencia ODbL).
- Costes: Observatorio de Costes del Transporte de Mercancías por Carretera, Ministerio de Transportes, enero de 2026.
- Emisiones: UK DESNZ/DEFRA GHG Conversion Factors 2025.
