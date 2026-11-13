# Reto Moda re- · Material de arranque para los equipos

**IA 4 Good Lab · Fundación Ingenieros ICAI · 14 y 15 de noviembre de 2026** · Equipos Azul y Amarillo

Reto: **«Optimización de la red de distribución entre plantas y tiendas»**, propuesto por Moda re- (Cáritas). Los dos equipos parten exactamente de este material.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [`brief-equipos.md`](brief-equipos.md) · [HTML](brief-equipos.html) | Una página de arranque: el reto, los entregables, el dataset, cómo empezar, las reglas y el calendario |
| [`rubrica-equipos.md`](rubrica-equipos.md) · [HTML](rubrica-equipos.html) | Cómo se evalúa: 6 criterios con su peso, descriptores del 1 al 5 y ajustes |
| [`data/`](data/) | Dataset de arranque: 7 CSV, su esquema ([`ESQUEMA.md`](data/ESQUEMA.md)), un [README](data/README.md) y `scripts/datos.py` |

La ficha oficial del reto la tenéis por la Fundación; no se incluye aquí.

## El dataset en 30 segundos

- CSV en UTF-8: distancias en km, tiempos en minutos, pesos en kg, dinero en € sin IVA.
- **Cada dato lleva su etiqueta:** **REAL** (de Moda re- o su web pública, con fuente y fecha), **ESTIMADO** (de mercado, con fuente) o **SINTÉTICO** (inventado para poder trabajar; cambiadlo con libertad). Vuestra herramienta debe conservarla y enseñarla.
- La ubicación de plantas y tiendas es REAL (web pública de Moda re-). El tamaño, las ventas y la planta que sirve hoy a cada tienda son SINTÉTICOS.
- `python3 data/scripts/datos.py validar` comprueba el dataset; el mismo script añade tiendas nuevas y regenera los valores sintéticos.

## Reglas clave

- El núcleo es **optimización y analítica** (segmentación, asignación, rutas VRP, flota y escenarios), no un chatbot.
- Nada de predecir la demanda con aprendizaje automático (no hay histórico) ni de «ahorramos un X % frente a hoy».
- Lo que se aclare a un equipo se aclara también al otro.

Si os bloqueáis, llamad a los mentores.
