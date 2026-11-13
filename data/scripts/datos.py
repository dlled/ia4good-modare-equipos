#!/usr/bin/env python3
"""Mantenimiento del dataset de arranque del reto Moda re- (IA 4 Good Lab).

Solo usa la biblioteca estándar de Python 3. Ejecutar desde la carpeta data/:

  python3 scripts/datos.py importar --raw fuentes/ubicaciones_raw.csv   # construye plantas y tiendas desde la lista pública
  python3 scripts/datos.py sinteticos --semilla 2026                    # regenera solo lo SINTÉTICO
  python3 scripts/datos.py sinteticos --sin-confirmadas                 # ignora fuentes/asignaciones_confirmadas.csv
  python3 scripts/datos.py anadir-tienda --nombre "Moda re- Albacete" --municipio Albacete --provincia Albacete --lat 38.994 --lon -1.858
  python3 scripts/datos.py cargar-ong --archivo respuesta_ong.csv --fuente "Moda re-, correo 13/11/2026"
  python3 scripts/datos.py distancias [--todo] [--sin-osrm]
  python3 scripts/datos.py validar

Etiquetas: REAL (fuente y fecha), ESTIMADO (fuente de mercado o método), SINTÉTICO (inventado, editable).
"""
import argparse, csv, datetime, json, math, os, random, sys, time, unicodedata, urllib.request

DATA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(DATA, n)
HOY = datetime.date.today().isoformat()
SEMILLA_DEFECTO = 2026
OSRM_URL = "https://router.project-osrm.org"
OSRM_MAX_COORDS = 100

COLS_PLANTAS = ["id_planta", "nombre", "municipio", "provincia", "direccion", "lat", "lon",
                "ubicacion_etiqueta", "ubicacion_fuente", "activa", "apertura_prevista",
                "estado_etiqueta", "estado_fuente", "capacidad_salida_kg_semana", "capacidad_etiqueta",
                "hora_inicio_carga", "hora_fin_carga", "carga_etiqueta"]
COLS_TIENDAS = ["id_tienda", "id_fuente", "nombre", "subtipo", "empresa_insercion", "direccion", "municipio", "provincia",
                "ccaa", "lat", "lon", "ubicacion_etiqueta", "ubicacion_fuente", "acceso_carretera", "superficie_m2",
                "categoria_tamano", "superficie_etiqueta", "ventas_periodo", "ventas_unidad", "periodo_ventas",
                "ventas_etiqueta", "planta_actual", "asignacion_etiqueta", "asignacion_fuente", "dias_recepcion",
                "ventana_inicio", "ventana_fin", "horario_etiqueta", "horario_fuente", "horario_publicado", "tiempo_descarga_min", "vehiculo_max", "recepcion_etiqueta",
                "en_muestra", "activa", "fecha_alta", "fecha_alta_etiqueta"]
COLS_DIST = ["origen", "destino", "distancia_km", "duracion_min", "duracion_camion_min", "metodo", "etiqueta", "fuente"]

# Plantas: municipio y estado son REALES (ficha del reto y reunión con la ONG). Coordenadas de respaldo = centro
# del municipio (ESTIMADO) si la lista pública no trae la dirección.
PLANTAS_BASE = [
    # id, nombre, municipio, provincia, lat, lon (respaldo), activa, id en la lista pública de research
    ("PL-MAD", "Planta Madrid (Vallecas)", "Madrid", "Madrid", 40.3730, -3.6120, 1, "P01"),
    ("PL-VAL", "Planta Valencia (Riba-roja de Túria)", "Valencia", "Valencia", 39.4699, -0.3763, 1, "P04"),
    ("PL-BCN", "Planta Barcelona (Sabadell)", "Barcelona", "Barcelona", 41.3874, 2.1686, 1, "P02"),
    ("PL-BIO", "Planta Bilbao (Mungia)", "Bilbao", "Bizkaia", 43.2630, -2.9350, 1, "P03"),
    ("PL-AST", "Planta Asturias (próxima apertura)", "Oviedo", "Asturias", 43.3614, -5.8494, 0, "P06"),
    ("PL-SCQ", "Planta Santiago de Compostela (próxima apertura)", "Santiago de Compostela", "A Coruña", 42.8782, -8.5448, 0, "P05"),
]

# provincia normalizada -> (nombre canónico, ccaa, capital)
PROVINCIAS = {
    "a coruna": ("A Coruña", "Galicia", "A Coruña"), "la coruna": ("A Coruña", "Galicia", "A Coruña"),
    "lugo": ("Lugo", "Galicia", "Lugo"), "ourense": ("Ourense", "Galicia", "Ourense"), "orense": ("Ourense", "Galicia", "Ourense"),
    "pontevedra": ("Pontevedra", "Galicia", "Pontevedra"),
    "asturias": ("Asturias", "Principado de Asturias", "Oviedo"), "cantabria": ("Cantabria", "Cantabria", "Santander"),
    "bizkaia": ("Bizkaia", "País Vasco", "Bilbao"), "vizcaya": ("Bizkaia", "País Vasco", "Bilbao"),
    "gipuzkoa": ("Gipuzkoa", "País Vasco", "Donostia-San Sebastián"), "guipuzcoa": ("Gipuzkoa", "País Vasco", "Donostia-San Sebastián"),
    "alava": ("Araba/Álava", "País Vasco", "Vitoria-Gasteiz"), "araba": ("Araba/Álava", "País Vasco", "Vitoria-Gasteiz"),
    "araba/alava": ("Araba/Álava", "País Vasco", "Vitoria-Gasteiz"),
    "navarra": ("Navarra", "Comunidad Foral de Navarra", "Pamplona"), "nafarroa": ("Navarra", "Comunidad Foral de Navarra", "Pamplona"),
    "la rioja": ("La Rioja", "La Rioja", "Logroño"),
    "huesca": ("Huesca", "Aragón", "Huesca"), "zaragoza": ("Zaragoza", "Aragón", "Zaragoza"), "teruel": ("Teruel", "Aragón", "Teruel"),
    "barcelona": ("Barcelona", "Cataluña", "Barcelona"), "girona": ("Girona", "Cataluña", "Girona"), "gerona": ("Girona", "Cataluña", "Girona"),
    "lleida": ("Lleida", "Cataluña", "Lleida"), "lerida": ("Lleida", "Cataluña", "Lleida"), "tarragona": ("Tarragona", "Cataluña", "Tarragona"),
    "leon": ("León", "Castilla y León", "León"), "zamora": ("Zamora", "Castilla y León", "Zamora"), "salamanca": ("Salamanca", "Castilla y León", "Salamanca"),
    "valladolid": ("Valladolid", "Castilla y León", "Valladolid"), "palencia": ("Palencia", "Castilla y León", "Palencia"),
    "burgos": ("Burgos", "Castilla y León", "Burgos"), "soria": ("Soria", "Castilla y León", "Soria"), "segovia": ("Segovia", "Castilla y León", "Segovia"),
    "avila": ("Ávila", "Castilla y León", "Ávila"),
    "madrid": ("Madrid", "Comunidad de Madrid", "Madrid"),
    "toledo": ("Toledo", "Castilla-La Mancha", "Toledo"), "ciudad real": ("Ciudad Real", "Castilla-La Mancha", "Ciudad Real"),
    "cuenca": ("Cuenca", "Castilla-La Mancha", "Cuenca"), "guadalajara": ("Guadalajara", "Castilla-La Mancha", "Guadalajara"),
    "albacete": ("Albacete", "Castilla-La Mancha", "Albacete"),
    "caceres": ("Cáceres", "Extremadura", "Cáceres"), "badajoz": ("Badajoz", "Extremadura", "Badajoz"),
    "valencia": ("Valencia", "Comunitat Valenciana", "Valencia"), "valencia/valencia": ("Valencia", "Comunitat Valenciana", "Valencia"),
    "alicante": ("Alicante", "Comunitat Valenciana", "Alicante"), "alacant": ("Alicante", "Comunitat Valenciana", "Alicante"),
    "alicante/alacant": ("Alicante", "Comunitat Valenciana", "Alicante"),
    "castellon": ("Castellón", "Comunitat Valenciana", "Castellón de la Plana"), "castello": ("Castellón", "Comunitat Valenciana", "Castellón de la Plana"),
    "castellon/castello": ("Castellón", "Comunitat Valenciana", "Castellón de la Plana"),
    "murcia": ("Murcia", "Región de Murcia", "Murcia"), "region de murcia": ("Murcia", "Región de Murcia", "Murcia"),
    "almeria": ("Almería", "Andalucía", "Almería"), "granada": ("Granada", "Andalucía", "Granada"), "jaen": ("Jaén", "Andalucía", "Jaén"),
    "cordoba": ("Córdoba", "Andalucía", "Córdoba"), "malaga": ("Málaga", "Andalucía", "Málaga"), "sevilla": ("Sevilla", "Andalucía", "Sevilla"),
    "cadiz": ("Cádiz", "Andalucía", "Cádiz"), "huelva": ("Huelva", "Andalucía", "Huelva"),
    "illes balears": ("Illes Balears", "Illes Balears", "Palma"), "illes baleares": ("Illes Balears", "Illes Balears", "Palma"), "baleares": ("Illes Balears", "Illes Balears", "Palma"),
    "islas baleares": ("Illes Balears", "Illes Balears", "Palma"),
    "las palmas": ("Las Palmas", "Canarias", "Las Palmas de Gran Canaria"), "santa cruz de tenerife": ("Santa Cruz de Tenerife", "Canarias", "Santa Cruz de Tenerife"),
    "ceuta": ("Ceuta", "Ceuta", "Ceuta"), "melilla": ("Melilla", "Melilla", "Melilla"),
}
SIN_CARRETERA = {"Illes Balears", "Canarias", "Ceuta", "Melilla"}  # requieren transporte marítimo: acceso_carretera = 0
GRANDES_MUNICIPIOS = {"madrid", "barcelona", "valencia", "sevilla", "zaragoza", "malaga", "murcia", "bilbao", "alicante",
                      "cordoba", "valladolid", "vigo", "gijon", "l'hospitalet de llobregat", "hospitalet de llobregat",
                      "vitoria-gasteiz", "a coruna", "granada", "elche", "oviedo", "badalona", "cartagena", "terrassa",
                      "jerez de la frontera", "sabadell", "mostoles", "alcala de henares", "pamplona", "fuenlabrada",
                      "almeria", "leganes", "donostia-san sebastian", "san sebastian", "santander", "burgos", "castellon de la plana",
                      "getafe", "alcorcon", "albacete", "logrono", "salamanca", "huelva", "cadiz", "leon", "tarragona", "jaen",
                      "girona", "lleida", "caceres", "badajoz", "toledo", "pontevedra", "ourense", "lugo", "santiago de compostela"}

# Asignaciones actuales confirmadas por la ONG (REAL): fuentes/asignaciones_confirmadas.csv
# (columnas id_fuente o id_tienda, planta_actual, fuente). Si el archivo no existe, no hay ninguna.
CONFIRMADAS = "fuentes/asignaciones_confirmadas.csv"


def asignaciones_confirmadas():
    out = {}
    for r in leer(CONFIRMADAS):
        k = r.get("id_fuente") or r.get("id_tienda")
        if k:
            out[k] = (r["planta_actual"], r.get("fuente", ""))
    return out
# Desajustes históricos SIMULADOS (provincia -> planta). Solo se aplican si difieren de la planta más cercana.
DESAJUSTES = {"Málaga": "PL-VAL", "Granada": "PL-VAL", "Murcia": "PL-MAD", "Toledo": "PL-VAL", "Alicante": "PL-MAD",
              "Burgos": "PL-MAD", "A Coruña": "PL-BIO", "Pontevedra": "PL-BIO", "Zaragoza": "PL-BIO", "Badajoz": "PL-VAL"}
# Muestra recomendada: plantas Madrid y Valencia y su zona, con Andalucía (caso Sevilla/Jerez/Cádiz ← Barcelona).
CCAA_MUESTRA = {"Comunidad de Madrid", "Castilla-La Mancha", "Comunitat Valenciana", "Región de Murcia", "Andalucía", "Extremadura"}
MAX_MUESTRA = 60


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").strip().lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("  ", " ")


def leer(nombre):
    path = P(nombre)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def escribir(nombre, cols, filas):
    with open(P(nombre), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({c: r.get(c, "") for c in cols})


def parametros():
    out = {}
    for r in leer("parametros.csv"):
        v = r["valor"]
        try:
            v = float(v)
        except ValueError:
            pass
        out[r["clave"]] = v
    return out


def haversine_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def coord(r):
    return float(r["lat"]), float(r["lon"])


def provincia_info(prov):
    k = norm(prov)
    if k in PROVINCIAS:
        return PROVINCIAS[k]
    k2 = k.split("/")[0].strip()
    return PROVINCIAS.get(k2, (prov, "", ""))


def categoria(m2, prm):
    if m2 >= prm["umbral_m2_grande"]:
        return "grande"
    if m2 >= prm["umbral_m2_mediana"]:
        return "mediana"
    return "pequeña"


def limite_kg_semana(cat, prm):
    return prm["entregas_semana_" + cat] * prm["max_palets_entrega_" + cat] * prm["kg_por_palet"]


def ventas_eur(t, prm):
    v = float(t["ventas_periodo"])
    return v / 100 * prm["ventas_media_eur_tienda"] if t.get("ventas_unidad") == "INDICE" else v


def demanda_kg_semana(t, prm):
    return ventas_eur(t, prm) / prm["precio_medio_eur_kg"] / prm["semanas_venta_anio"]


def parse_horario(txt):
    """Primer tramo horario de lunes a viernes de un texto como 'Lunes-Viernes 10:00 - 14:00 y 17:00 - 20:00. Sábado ...'.
    Devuelve (inicio, fin, 'L-V' o 'M-V') o (None, None, None) si no se entiende (se usa entonces la ventana por defecto)."""
    import re
    t = norm(txt).replace("–", "-").replace("—", "-")
    m = re.search(r"(lunes|martes)\s*(?:-|a)\s*(viernes|sabado|domingo)[^0-9]*(\d{1,2})[:.](\d{2})\s*-\s*(\d{1,2})[:.](\d{2})", t)
    if not m:
        return None, None, None
    ini = f"{int(m.group(3)):02d}:{m.group(4)}"
    fin = f"{int(m.group(5)):02d}:{m.group(6)}"
    dias = "L-V" if m.group(1) == "lunes" else "M-V"
    return (ini, fin, dias) if ini < fin else (None, None, None)


# ---------------------------------------------------------------- importar
def cmd_importar(a):
    with open(a.raw, encoding="utf-8-sig", newline="") as f:
        raw = list(csv.DictReader(f))
    previas = {t["id_fuente"]: t for t in leer("tiendas.csv") if t.get("id_fuente")}
    plantas = []
    raw_p = {r.get("id"): r for r in raw if norm(r.get("tipo")) == "planta"}
    for pid, nombre, muni, prov, lat, lon, activa, id_raw in PLANTAS_BASE:
        hit = raw_p.get(id_raw)
        p = {"id_planta": pid, "nombre": nombre, "municipio": muni, "provincia": prov, "direccion": "",
             "lat": lat, "lon": lon, "ubicacion_etiqueta": "ESTIMADO",
             "ubicacion_fuente": "Centro del municipio (no hay ubicación pública)",
             "activa": activa, "apertura_prevista": "" if activa else "próximamente",
             "estado_etiqueta": "REAL",
             "estado_fuente": "Ficha del reto (septiembre de 2026) y reunión con Noema Paniagua (Moda re-), 2026"}
        if hit and hit.get("lat"):
            p.update({"direccion": hit.get("direccion", ""), "municipio": hit.get("localidad") or muni,
                      "lat": round(float(hit["lat"]), 6), "lon": round(float(hit["lon"]), 6),
                      "ubicacion_etiqueta": hit.get("etiqueta") or "ESTIMADO",
                      "ubicacion_fuente": f"{hit.get('fuente_url', '')}, consultado {hit.get('fecha_consulta', '')}; "
                                          f"precisión: {hit.get('precision_geo', '')}. {hit.get('notas', '')}".strip()})
        plantas.append(p)
    escribir("plantas.csv", COLS_PLANTAS, plantas)

    tiendas, fuera = [], []
    for r in raw:
        if norm(r.get("tipo")) != "tienda":
            continue
        prov, ccaa, _ = provincia_info(r.get("provincia", ""))
        if ccaa in SIN_CARRETERA:
            fuera.append(r)
        if not r.get("lat") or not r.get("lon"):
            fuera.append(r)
            continue
        prec = norm(r.get("precision_geo"))
        et = r.get("etiqueta") or "ESTIMADO"
        if prec == "municipio" and et == "REAL":
            et = "ESTIMADO"
        t = dict(previas.get(r.get("id", ""), {}))
        ini, fin, dias = parse_horario(r.get("horario", ""))
        if ini:
            t.update({"dias_recepcion": dias, "ventana_inicio": ini, "ventana_fin": fin, "horario_etiqueta": "REAL",
                      "horario_fuente": f"Horario comercial publicado ({r.get('ficha_url') or r.get('fuente_url', '')}, consultado "
                                        f"{r.get('fecha_consulta', '')}); ventana = primer tramo de L-V. La ficha del reto dice que se recibe en horario comercial"})
        t["horario_publicado"] = r.get("horario", "")
        t.update({"id_fuente": r.get("id", ""), "nombre": r.get("nombre", ""), "subtipo": r.get("subtipo", ""), "empresa_insercion": r.get("empresa_insercion", ""),
                  "direccion": r.get("direccion", ""), "municipio": r.get("localidad", ""), "provincia": prov, "ccaa": ccaa,
                  "lat": round(float(r["lat"]), 6), "lon": round(float(r["lon"]), 6), "ubicacion_etiqueta": et,
                  "ubicacion_fuente": f"{r.get('fuente_url', '')}, consultado {r.get('fecha_consulta', '')}; precisión: {r.get('precision_geo', '')}",
                  "activa": t.get("activa") or 1, "acceso_carretera": 0 if ccaa in SIN_CARRETERA else 1})
        tiendas.append(t)
    tiendas.sort(key=lambda t: (t["ccaa"], t["provincia"], norm(t["municipio"]), norm(t["nombre"])))
    usados = {t["id_tienda"] for t in tiendas if t.get("id_tienda")}
    n = max([int(i[3:]) for i in usados] + [0])
    for t in tiendas:
        if not t.get("id_tienda"):
            n += 1
            t["id_tienda"] = f"TD-{n:03d}"
    marcar_muestra(tiendas, plantas, a.semilla)
    escribir("tiendas.csv", COLS_TIENDAS, tiendas)
    print(f"plantas: {len(plantas)} · tiendas: {len(tiendas)} · sin acceso por carretera o sin coordenadas: {len(fuera)}")
    for r in fuera:
        print(f"  fuera: {r.get('nombre')} · {r.get('localidad')} ({r.get('provincia')})")
    cmd_sinteticos(a)


def marcar_muestra(tiendas, plantas, semilla):
    """Muestra recomendada: tiendas de CCAA_MUESTRA. Si pasan de MAX_MUESTRA, se conserva toda Andalucía y se
    submuestrea el resto de forma reproducible manteniendo al menos una tienda por provincia."""
    cand = [t for t in tiendas if t["ccaa"] in CCAA_MUESTRA and str(t.get("acceso_carretera", 1)) != "0"]
    rng = random.Random(f"{semilla}-muestra")
    elegidas = [t for t in cand if t["ccaa"] == "Andalucía"]
    resto = [t for t in cand if t["ccaa"] != "Andalucía"]
    por_prov = {}
    for t in resto:
        por_prov.setdefault(t["provincia"], []).append(t)
    for prov in sorted(por_prov):
        elegidas.append(por_prov[prov][0])
    quedan = [t for t in resto if t not in elegidas]
    rng.shuffle(quedan)
    elegidas += quedan[: max(0, MAX_MUESTRA - len(elegidas))]
    ids = {t["id_tienda"] for t in elegidas}
    for t in tiendas:
        t["en_muestra"] = 1 if t["id_tienda"] in ids else 0


# ---------------------------------------------------------------- sintéticos
def planta_mas_cercana(t, plantas):
    act = [p for p in plantas if str(p["activa"]) == "1"]
    return min(act, key=lambda p: haversine_km(coord(t), coord(p)))["id_planta"]


def generar_tienda(t, plantas, prm, semilla, confirmadas, empresas_caso):
    rng = random.Random(f"{semilla}-{t['id_tienda']}")
    # Superficie y categoría
    if t.get("superficie_etiqueta") != "REAL":
        # Draw on the base scale (thresholds / escala_tiendas) and rescale, so the same seed gives the
        # same stores at any scale (escala_tiendas = 0.5 halves every synthetic surface).
        escala = prm.get("escala_tiendas", 1.0)
        um, ug = round(prm["umbral_m2_mediana"] / escala), round(prm["umbral_m2_grande"] / escala)
        u = rng.random()
        if u < 0.40:
            m2 = rng.randint(round(0.4 * um), um - 1)
        elif u < 0.80:
            m2 = rng.randint(um, ug - 1)
        else:
            m2 = rng.randint(ug, round(ug * 750 / 350))
        t["superficie_m2"] = math.floor(m2 * escala)
        t["superficie_etiqueta"] = "SINTÉTICO"
    t["categoria_tamano"] = categoria(float(t["superficie_m2"]), prm)
    # Ventas: superficie × densidad de ventas con ruido; capadas para que la demanda quepa en los límites de la categoría
    if t.get("ventas_etiqueta") != "REAL":
        densidad = 900 * math.exp(rng.gauss(0, 0.35))  # €/m²/año
        bruto = float(t["superficie_m2"]) * densidad
        tope = 0.95 * limite_kg_semana(t["categoria_tamano"], prm) * prm["precio_medio_eur_kg"] * prm["semanas_venta_anio"]
        t["ventas_periodo"] = int(round(min(bruto, tope), -3))
        t["ventas_unidad"] = "EUR"
        t["periodo_ventas"] = "2025"
        t["ventas_etiqueta"] = "SINTÉTICO"
    # Asignación actual
    conf = confirmadas.get(t.get("id_fuente")) or confirmadas.get(t["id_tienda"])
    fuente_prev = t.get("asignacion_fuente", "")
    era_confirmada = t.get("asignacion_etiqueta") == "REAL" and fuente_prev.startswith("Reunión con Noema")
    if conf:
        t.update({"planta_actual": conf[0], "asignacion_etiqueta": "REAL", "asignacion_fuente": conf[1]})
    elif t.get("asignacion_etiqueta") != "REAL" or era_confirmada:
        cerca = planta_mas_cercana(t, plantas)
        hist = DESAJUSTES.get(t["provincia"])
        emp = empresas_caso.get(t.get("empresa_insercion"))
        if emp and emp != cerca:
            t.update({"planta_actual": emp, "asignacion_fuente": "Generada: desajuste histórico simulado (misma empresa de inserción que una asignación confirmada)"})
        elif hist and hist != cerca:
            t.update({"planta_actual": hist, "asignacion_fuente": "Generada: desajuste histórico simulado (provincia completa)"})
        else:
            t.update({"planta_actual": cerca, "asignacion_fuente": "Generada: planta activa más cercana en línea recta"})
        t["asignacion_etiqueta"] = "SINTÉTICO"
    # Recepción
    excepcion = rng.random() < 0.10
    if t.get("horario_etiqueta") != "REAL":
        t.update({"dias_recepcion": "L-V",
                  "ventana_inicio": "08:00" if excepcion else prm["ventana_inicio_defecto"],
                  "ventana_fin": "10:00" if excepcion else prm["ventana_fin_defecto"],
                  "horario_etiqueta": "SINTÉTICO", "horario_fuente": "Ventana por defecto de parametros.csv (10 % con ventana temprana 08:00-10:00)"})
    if t.get("recepcion_etiqueta") != "REAL":
        if t.get("subtipo") == "corner":
            vmax = ""  # corner en hipermercado: muelle de carga
        elif norm(t["municipio"]) in GRANDES_MUNICIPIOS:
            vmax = prm["vehiculo_max_centro_urbano"]
        else:
            vmax = "VEH-R12"
        t.update({"tiempo_descarga_min": int(prm["tiempo_descarga_min"]), "vehiculo_max": vmax, "recepcion_etiqueta": "SINTÉTICO"})
    if t.get("fecha_alta_etiqueta") != "REAL":
        d0 = datetime.date(2020, 1, 1).toordinal()
        d1 = datetime.date(2026, 10, 31).toordinal()
        t["fecha_alta"] = datetime.date.fromordinal(rng.randint(d0, d1)).isoformat()
        t["fecha_alta_etiqueta"] = "SINTÉTICO"
    t.setdefault("activa", 1)
    if t.get("acceso_carretera") in (None, ""):
        t["acceso_carretera"] = 0 if t.get("ccaa") in SIN_CARRETERA else 1
    if t.get("en_muestra") in (None, ""):
        t["en_muestra"] = 0


def cmd_sinteticos(a):
    prm = parametros()
    plantas = leer("plantas.csv")
    tiendas = leer("tiendas.csv")
    confirmadas = {} if getattr(a, "sin_confirmadas", False) else asignaciones_confirmadas()
    empresas_caso = {}
    for t in tiendas:
        c = confirmadas.get(t.get("id_fuente")) or confirmadas.get(t["id_tienda"])
        if c and t.get("empresa_insercion"):
            empresas_caso[t["empresa_insercion"]] = c[0]
    for t in tiendas:
        generar_tienda(t, plantas, prm, a.semilla, confirmadas, empresas_caso)
    # Capacidad de planta: 1,3 × la demanda que sirve hoy (activa); mínimo 15 t/semana × escala_tiendas (futura)
    for p in plantas:
        if p.get("capacidad_etiqueta") != "REAL":
            dem = sum(demanda_kg_semana(t, prm) for t in tiendas if t["planta_actual"] == p["id_planta"] and str(t["activa"]) == "1")
            p["capacidad_salida_kg_semana"] = int(round(max(dem * 1.3, 15000 * prm.get("escala_tiendas", 1.0)), -3))
            p["capacidad_etiqueta"] = "SINTÉTICO"
        if p.get("carga_etiqueta") != "REAL":
            p.update({"hora_inicio_carga": "06:00", "hora_fin_carga": "18:00", "carga_etiqueta": "SINTÉTICO"})
    escribir("plantas.csv", COLS_PLANTAS, plantas)
    escribir("tiendas.csv", COLS_TIENDAS, tiendas)
    n_hist = sum(1 for t in tiendas if t["asignacion_fuente"].startswith("Generada: desajuste"))
    n_real = sum(1 for t in tiendas if t["asignacion_etiqueta"] == "REAL")
    print(f"sintéticos regenerados (semilla {a.semilla}): {len(tiendas)} tiendas · asignación REAL {n_real} · desajustes simulados {n_hist}")


# ---------------------------------------------------------------- añadir tienda
def cmd_anadir_tienda(a):
    tiendas = leer("tiendas.csv")
    n = max([int(t["id_tienda"][3:]) for t in tiendas] + [0]) + 1
    prov, ccaa, _ = provincia_info(a.provincia)
    t = {"id_tienda": f"TD-{n:03d}", "id_fuente": "", "nombre": a.nombre, "empresa_insercion": a.empresa or "",
         "direccion": a.direccion or "", "municipio": a.municipio, "provincia": prov, "ccaa": a.ccaa or ccaa,
         "lat": a.lat, "lon": a.lon, "ubicacion_etiqueta": a.ubicacion_etiqueta,
         "ubicacion_fuente": a.ubicacion_fuente or f"Añadida con scripts/datos.py el {HOY}",
         "en_muestra": 1 if a.en_muestra else 0, "activa": 1}
    if a.superficie is not None:
        t.update({"superficie_m2": a.superficie, "superficie_etiqueta": a.etiqueta_datos})
    if a.ventas is not None:
        t.update({"ventas_periodo": a.ventas, "ventas_unidad": "EUR", "periodo_ventas": "2025", "ventas_etiqueta": a.etiqueta_datos})
    if a.planta:
        t.update({"planta_actual": a.planta, "asignacion_etiqueta": a.etiqueta_datos, "asignacion_fuente": a.ubicacion_fuente or "Indicada al añadir la tienda"})
    if a.fecha_alta:
        t.update({"fecha_alta": a.fecha_alta, "fecha_alta_etiqueta": a.etiqueta_datos})
    tiendas.append(t)
    escribir("tiendas.csv", COLS_TIENDAS, tiendas)
    print(f"añadida {t['id_tienda']} · {a.nombre}")
    cmd_sinteticos(a)
    if not a.sin_distancias:
        cmd_distancias(argparse.Namespace(todo=False, sin_osrm=a.sin_osrm, solo_tiempos=False))


# ---------------------------------------------------------------- cargar datos de la ONG
def cmd_cargar_ong(a):
    """Carga un CSV de la ONG con columna id_tienda o id_fuente (o nombre) y cualquiera de: superficie_m2,
    ventas_periodo, ventas_unidad, periodo_ventas, planta_actual, ventana_inicio, ventana_fin, dias_recepcion.
    Los valores cargados pasan a REAL con la fuente indicada."""
    tiendas = leer("tiendas.csv")
    idx = {}
    for t in tiendas:
        for k in ("id_tienda", "id_fuente"):
            if t.get(k):
                idx[t[k]] = t
        idx[norm(t["nombre"])] = t
    with open(a.archivo, encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f))
    n, sin = 0, []
    for r in filas:
        t = idx.get(r.get("id_tienda", "")) or idx.get(r.get("id_fuente", "")) or idx.get(norm(r.get("nombre", "")))
        if not t:
            sin.append(r)
            continue
        fuente = f"{a.fuente}"
        if r.get("superficie_m2"):
            t.update({"superficie_m2": r["superficie_m2"], "superficie_etiqueta": "REAL"})
        if r.get("ventas_periodo"):
            t.update({"ventas_periodo": r["ventas_periodo"], "ventas_unidad": r.get("ventas_unidad") or "EUR",
                      "periodo_ventas": r.get("periodo_ventas") or t.get("periodo_ventas", ""), "ventas_etiqueta": "REAL"})
        if r.get("planta_actual"):
            t.update({"planta_actual": r["planta_actual"], "asignacion_etiqueta": "REAL", "asignacion_fuente": fuente})
        if r.get("ventana_inicio") and r.get("ventana_fin"):
            t.update({"ventana_inicio": r["ventana_inicio"], "ventana_fin": r["ventana_fin"],
                      "dias_recepcion": r.get("dias_recepcion") or t.get("dias_recepcion", "L-V"), "recepcion_etiqueta": "REAL"})
        n += 1
    escribir("tiendas.csv", COLS_TIENDAS, tiendas)
    print(f"cargadas {n} filas de la ONG; sin casar: {len(sin)}")
    for r in sin:
        print("  sin casar:", r)
    cmd_sinteticos(a)


# ---------------------------------------------------------------- distancias
def osrm_table(puntos):
    coords = ";".join(f"{lon:.6f},{lat:.6f}" for lat, lon in puntos)
    url = f"{OSRM_URL}/table/v1/driving/{coords}?annotations=distance,duration"
    req = urllib.request.Request(url, headers={"User-Agent": "dataset-hackathon-educativo/1.0"})
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                d = json.load(resp)
            if d.get("code") == "Ok":
                return d["distances"], d["durations"]
            print("OSRM respondió:", d.get("code"), d.get("message"), file=sys.stderr)
        except Exception as e:  # red caída, límite, etc.
            print(f"OSRM intento {intento + 1} falló: {e}", file=sys.stderr)
        time.sleep(3 * (intento + 1))
    return None, None


def cmd_distancias(a):
    prm = parametros()
    if getattr(a, "solo_tiempos", False):
        filas = leer("distancias.csv")
        for r in filas:
            r["duracion_camion_min"] = round(float(r["duracion_min"]) * prm["factor_tiempo_camion"], 1)
        escribir("distancias.csv", COLS_DIST, filas)
        print(f"duracion_camion_min recalculada con factor_tiempo_camion = {prm['factor_tiempo_camion']:g} ({len(filas)} pares, sin llamar a OSRM)")
        return
    plantas, tiendas = leer("plantas.csv"), leer("tiendas.csv")
    nodos = [(p["id_planta"], coord(p)) for p in plantas] + [(t["id_tienda"], coord(t)) for t in tiendas
                                                              if str(t.get("acceso_carretera", 1)) != "0"]
    ids = {i for i, _ in nodos}
    previas = {} if a.todo else {(r["origen"], r["destino"]): r for r in leer("distancias.csv")
                                  if r["origen"] in ids and r["destino"] in ids}
    muestra = [(p["id_planta"], coord(p)) for p in plantas] + [(t["id_tienda"], coord(t)) for t in tiendas if str(t["en_muestra"]) == "1"]
    fac_cam = prm["factor_tiempo_camion"]
    filas = dict(previas)
    # 1) Muestra por carretera con OSRM: una sola petición /table si cabe (≤ 100 puntos)
    ids_m = [i for i, _ in muestra]
    faltan_m = any((o, d) not in previas or previas[(o, d)]["metodo"] != "OSRM" for o in ids_m for d in ids_m if o != d)
    if faltan_m and not a.sin_osrm:
        if len(muestra) > OSRM_MAX_COORDS:
            print(f"La muestra tiene {len(muestra)} puntos (> {OSRM_MAX_COORDS}); se calcula con haversine", file=sys.stderr)
        else:
            print(f"OSRM: 1 petición /table con {len(muestra)} puntos…")
            dist, dur = osrm_table([c for _, c in muestra])
            if dist:
                fuente = f"OSRM (router.project-osrm.org), datos OpenStreetMap, {HOY}"
                for i, o in enumerate(ids_m):
                    for j, d in enumerate(ids_m):
                        if i == j or dist[i][j] is None or dur[i][j] is None:
                            continue
                        km, mi = dist[i][j] / 1000, dur[i][j] / 60
                        filas[(o, d)] = {"origen": o, "destino": d, "distancia_km": round(km, 1), "duracion_min": round(mi, 1),
                                         "duracion_camion_min": round(mi * fac_cam, 1), "metodo": "OSRM",
                                         "etiqueta": "ESTIMADO", "fuente": fuente}
            time.sleep(1.5)
    # 2) Resto: haversine × factor de rodeo
    fuente_h = (f"Línea recta × {prm['factor_rodeo']} a {prm['velocidad_respaldo_kmh']:.0f} km/h "
                f"(método de respaldo), {HOY}")
    for o, co in nodos:
        for d, cd in nodos:
            if o == d or (o, d) in filas:
                continue
            km = haversine_km(co, cd) * prm["factor_rodeo"]
            mi = km / prm["velocidad_respaldo_kmh"] * 60
            filas[(o, d)] = {"origen": o, "destino": d, "distancia_km": round(km, 1), "duracion_min": round(mi, 1),
                             "duracion_camion_min": round(mi * fac_cam, 1), "metodo": f"HAVERSINE_X{prm['factor_rodeo']:g}",
                             "etiqueta": "ESTIMADO", "fuente": fuente_h}
    orden = {i: k for k, (i, _) in enumerate(nodos)}
    out = sorted(filas.values(), key=lambda r: (orden[r["origen"]], orden[r["destino"]]))
    escribir("distancias.csv", COLS_DIST, out)
    n_osrm = sum(1 for r in out if r["metodo"] == "OSRM")
    print(f"distancias: {len(out)} pares · OSRM {n_osrm} · haversine {len(out) - n_osrm}")


# ---------------------------------------------------------------- validar
def cmd_validar(a):
    prm = parametros()
    errores, avisos = [], []
    plantas, tiendas = leer("plantas.csv"), leer("tiendas.csv")
    veh = {r["id_tipo"] for r in leer("vehiculos.csv")}
    ids_p = {p["id_planta"] for p in plantas}
    ids_t = [t["id_tienda"] for t in tiendas]
    if len(set(ids_t)) != len(ids_t):
        errores.append("id_tienda duplicado")
    etiquetas = {"REAL", "ESTIMADO", "SINTÉTICO"}
    for nombre, filas in (("plantas.csv", plantas), ("tiendas.csv", tiendas), ("vehiculos.csv", leer("vehiculos.csv")),
                          ("tarifas.csv", leer("tarifas.csv")), ("emisiones.csv", leer("emisiones.csv")),
                          ("parametros.csv", leer("parametros.csv")), ("distancias.csv", leer("distancias.csv"))):
        if not filas:
            errores.append(f"{nombre} vacío o no existe")
            continue
        cols = [c for c in filas[0] if c == "etiqueta" or c.endswith("_etiqueta")]
        if not cols:
            errores.append(f"{nombre} sin columna de etiqueta")
        for r in filas:
            for c in cols:
                if r[c] not in etiquetas:
                    errores.append(f"{nombre}: etiqueta '{r[c]}' no válida en {c}")
                    break
    for t in tiendas:
        if t["planta_actual"] not in ids_p:
            errores.append(f"{t['id_tienda']}: planta_actual desconocida {t['planta_actual']}")
        if t["vehiculo_max"] and t["vehiculo_max"] not in veh:
            errores.append(f"{t['id_tienda']}: vehiculo_max desconocido {t['vehiculo_max']}")
        if t["categoria_tamano"] != categoria(float(t["superficie_m2"]), prm):
            errores.append(f"{t['id_tienda']}: categoria_tamano no cuadra con la superficie")
        dem, lim = demanda_kg_semana(t, prm), limite_kg_semana(t["categoria_tamano"], prm)
        if dem > lim:
            avisos.append(f"{t['id_tienda']} ({t['categoria_tamano']}): demanda {dem:.0f} kg/sem > límite {lim:.0f}")
    for p in plantas:
        if str(p["activa"]) == "0" and any(t["planta_actual"] == p["id_planta"] for t in tiendas):
            errores.append(f"{p['id_planta']} está inactiva y tiene tiendas asignadas")
    pares = {(r["origen"], r["destino"]) for r in leer("distancias.csv")}
    ids_c = [t["id_tienda"] for t in tiendas if str(t.get("acceso_carretera", 1)) != "0"]
    nodos = list(ids_p) + ids_c
    sobran = sum(1 for o, d in pares if o not in nodos or d not in nodos)
    if sobran:
        errores.append(f"distancias.csv: {sobran} pares con tiendas sin acceso por carretera o inexistentes")
    for t in tiendas:
        if str(t.get("acceso_carretera")) == "0" and str(t["en_muestra"]) == "1":
            errores.append(f"{t['id_tienda']}: sin acceso por carretera y en la muestra")
    faltan = sum(1 for o in nodos for d in nodos if o != d and (o, d) not in pares)
    if faltan:
        errores.append(f"distancias.csv: faltan {faltan} pares (python3 scripts/datos.py distancias)")
    for r in leer("tarifas.csv") + leer("emisiones.csv"):
        if r["id_tipo"] not in veh:
            errores.append(f"tipo de vehículo desconocido {r['id_tipo']}")
    m = [t for t in tiendas if str(t["en_muestra"]) == "1"]
    print(f"plantas {len(plantas)} · tiendas {len(tiendas)} (muestra {len(m)}) · pares de distancia {len(pares)}")
    for x in avisos:
        print("AVISO:", x)
    for x in errores:
        print("ERROR:", x)
    print("OK" if not errores else f"{len(errores)} errores")
    sys.exit(1 if errores else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("importar", help="Construye plantas.csv y tiendas.csv desde la lista pública de ubicaciones")
    s.add_argument("--raw", default=P("fuentes/ubicaciones_raw.csv"))
    s.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    s.add_argument("--sin-confirmadas", action="store_true")
    s = sub.add_parser("sinteticos", help="Regenera los valores SINTÉTICOS (no toca los REALES)")
    s.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    s.add_argument("--sin-confirmadas", action="store_true",
                   help="Ignora fuentes/asignaciones_confirmadas.csv y asigna todas las tiendas de forma sintética")
    s = sub.add_parser("anadir-tienda", help="Añade una tienda y recalcula sus distancias")
    s.add_argument("--nombre", required=True); s.add_argument("--municipio", required=True)
    s.add_argument("--provincia", required=True); s.add_argument("--ccaa")
    s.add_argument("--lat", type=float, required=True); s.add_argument("--lon", type=float, required=True)
    s.add_argument("--direccion"); s.add_argument("--empresa")
    s.add_argument("--ubicacion-etiqueta", default="ESTIMADO", choices=["REAL", "ESTIMADO", "SINTÉTICO"])
    s.add_argument("--ubicacion-fuente")
    s.add_argument("--superficie", type=int); s.add_argument("--ventas", type=int)
    s.add_argument("--planta"); s.add_argument("--fecha-alta")
    s.add_argument("--etiqueta-datos", default="SINTÉTICO", choices=["REAL", "ESTIMADO", "SINTÉTICO"],
                   help="Etiqueta de superficie/ventas/planta/fecha si se indican")
    s.add_argument("--en-muestra", action="store_true")
    s.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    s.add_argument("--sin-distancias", action="store_true"); s.add_argument("--sin-osrm", action="store_true")
    s = sub.add_parser("cargar-ong", help="Carga datos reales enviados por la ONG")
    s.add_argument("--archivo", required=True); s.add_argument("--fuente", required=True)
    s.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    s = sub.add_parser("distancias", help="Calcula los pares que falten")
    s.add_argument("--todo", action="store_true", help="Recalcula todos los pares")
    s.add_argument("--sin-osrm", action="store_true", help="Solo haversine × factor de rodeo")
    s.add_argument("--solo-tiempos", action="store_true", help="Solo recalcula duracion_camion_min tras cambiar factor_tiempo_camion")
    sub.add_parser("validar", help="Comprueba coherencia del dataset")
    a = ap.parse_args()
    {"importar": cmd_importar, "sinteticos": cmd_sinteticos, "anadir-tienda": cmd_anadir_tienda,
     "cargar-ong": cmd_cargar_ong, "distancias": cmd_distancias, "validar": cmd_validar}[a.cmd](a)


if __name__ == "__main__":
    main()
