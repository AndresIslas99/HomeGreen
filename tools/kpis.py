#!/usr/bin/env python3
"""Calcula los KPIs del lazo comercial semanal (L2) a partir de la bitácora.

Lee ``bitacora/produccion.csv`` y ``bitacora/ventas.csv`` (esquema de
``docs/referencia/06-validacion-y-lazos-agenticos.md``, sección "Esquema de datos") y
calcula, por semana ISO (``AAAA-Www``):

* **Sell-through**: charolas vendidas / charolas cosechadas para venta. Las muestras
  (destino ``muestra``) son CAC deliberado y quedan fuera del denominador (``--contar-muestras``
  las incluye); las charolas que se quedan en ``casa`` cuentan como no vendidas.
* **Merma de producción**: charolas tiradas (``merma_pct`` = 100) / charolas sembradas ya
  cerradas (con ``fecha_cosecha`` o tiradas). Se agrupa por semana de siembra.
* **Entregas a tiempo**: paradas (fecha + cliente) con todo ``entregado_a_tiempo`` = si /
  paradas cobradas.
* **Recompra**: clientes que compraron esta semana y la anterior / clientes de la anterior.
* **Margen variable (aprox.)**: (ingreso - insumos - reparto) / ingreso, con el costo
  variable por charola de ``docs/referencia/08-recetas-y-economia-unitaria.md`` y $20 por
  parada de reparto (rango $15-25 de la misma fuente).
* **Feedback**: paradas con algún ``feedback`` no vacío / paradas cobradas.

Metas y umbrales rojos: 06 §L2. Las reglas de decisión (sell-through < 75 % dos semanas
seguidas, merma > 20 %, cliente sin pedir 2 semanas) se imprimen como alertas.

Solo biblioteca estándar (Python 3.11). Tolera CSV vacíos o inexistentes: reporta y sigue.

Uso::

    python3 tools/kpis.py --produccion bitacora/produccion.csv --ventas bitacora/ventas.csv
    python3 tools/kpis.py --semanas 4 --costo girasol=9.10 --reparto 20
    python3 tools/kpis.py --json > kpis.json

Este archivo también es el módulo compartido que importan ``informe_semanal.py`` y
``gate_audit.py`` (carga de CSV, semanas ISO, rachas, costos y cálculo de KPIs).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes de la fuente de verdad
# ---------------------------------------------------------------------------

#: Formato de lote ``VAR-AAMMDD-Slote-posición`` (06 §Esquema de datos; diseno/datos.md).
RE_SIEMBRA_ID = re.compile(r"^[A-Z]{3}-\d{6}-S\d{3}-R\dN\d$")

#: Costo variable por charola 1020 en MXN (08 §Economía por charola; semilla + $4.50 de base:
#: coco, agua/energía, desinfección, etiqueta/film). Valor conservador por variedad:
#: girasol con semilla Al Natural ($185/kg); con semilla CEDA validada por V1 usa
#: ``--costo girasol=9.10``. Chícharo con semilla Hydro Environment ($340/kg): con arvejón
#: CEDA validado usa ``--costo chicharo=18``.
COSTO_VARIABLE_MXN: dict[str, float] = {
    "girasol": 29.50,   # CEDA validado: 9.10 · Hydro Environment forrajero: 45.00
    "chicharo": 98.00,  # arvejón CEDA por validar: 15.50-21.00
    "rabano": 49.30,
    "betabel": 52.50,
    "brocoli": 57.00,
    "amaranto": 7.50,
    "cilantro": 20.25,
    "arugula": 35.30,
}
#: Clamshell PET 8 oz, aprox. $3.50/pza; una charola de rábano llena ~2.5-3 clamshells de
#: 100 g (research/recetas-produccion-economia.md §4).
COSTO_CLAMSHELL_MXN = 3.50
CLAMSHELLS_POR_CHAROLA = 2.75
#: Reparto en ruta propia: $15-25 por parada (08 / research §4). Se prorratea por parada.
REPARTO_POR_PARADA_MXN = 20.0

#: Metas y umbrales rojos de 06 §L2 (en %).
UMBRALES = {
    "sell_through": {"meta": 90.0, "rojo": 75.0, "mayor_mejor": True},
    "merma": {"meta": 10.0, "rojo": 20.0, "mayor_mejor": False},
    "entregas": {"meta": 100.0, "rojo": 90.0, "mayor_mejor": True},
    "recompra": {"meta": 80.0, "rojo": None, "mayor_mejor": True},
    "margen": {"meta": 60.0, "rojo": 45.0, "mayor_mejor": True},
    "feedback": {"meta": 50.0, "rojo": None, "mayor_mejor": True},
}

VARIEDADES = (
    "girasol", "chicharo", "rabano", "betabel", "brocoli", "amaranto", "cilantro",
    "arugula", "albahaca", "hierbabuena",
)
DESTINOS_NO_VENTA = {"", "muestra", "muestras", "casa", "basura", "merma", "prueba", "tirada"}
DESTINOS_MUESTRA = {"muestra", "muestras"}

COLUMNAS_PRODUCCION = [
    "siembra_id", "fecha_siembra", "variedad", "lote_semilla", "densidad_g", "dias_oscuridad",
    "fecha_cosecha", "rendimiento_g", "merma_pct", "destino", "precio_mxn", "observaciones",
]
COLUMNAS_VENTAS = [
    "fecha", "cliente", "producto", "cantidad", "precio_unit_mxn", "entregado_a_tiempo",
    "feedback",
]


# ---------------------------------------------------------------------------
# Utilidades de texto, fechas y semanas ISO
# ---------------------------------------------------------------------------

def normalizar(texto: str | None) -> str:
    """Minúsculas, sin acentos ni espacios sobrantes (``Rábano`` -> ``rabano``)."""
    t = unicodedata.normalize("NFKD", (texto or "").strip().lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def parse_fecha(texto: str | None) -> date | None:
    """``AAAA-MM-DD`` -> ``date``; acepta un prefijo de fecha en un timestamp. None si no parsea."""
    t = (texto or "").strip()
    if not t:
        return None
    try:
        return date.fromisoformat(t[:10])
    except ValueError:
        return None


def parse_num(texto: str | None) -> float | None:
    """Número con punto o coma decimal y símbolo $ opcional; None si vacío o inválido."""
    t = (texto or "").strip().replace("$", "").replace(",", "").replace("%", "")
    if not t:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def semana_iso(d: date) -> str:
    """``date`` -> ``AAAA-Www`` (semana ISO 8601)."""
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def lunes_de(semana: str) -> date:
    """``AAAA-Www`` -> fecha del lunes de esa semana."""
    y, w = semana.upper().split("-W")
    return date.fromisocalendar(int(y), int(w), 1)


def semana_siguiente(semana: str) -> str:
    return semana_iso(lunes_de(semana) + timedelta(days=7))


def semana_anterior(semana: str) -> str:
    return semana_iso(lunes_de(semana) - timedelta(days=7))


def rango_semanas(desde: str, hasta: str) -> list[str]:
    """Lista continua de semanas ISO entre ``desde`` y ``hasta`` (inclusive)."""
    if lunes_de(desde) > lunes_de(hasta):
        desde, hasta = hasta, desde
    semanas = [desde]
    while semanas[-1] != hasta:
        semanas.append(semana_siguiente(semanas[-1]))
    return semanas


def racha_maxima(semanas: set[str] | list[str]) -> tuple[int, list[str]]:
    """Longitud máxima de semanas ISO consecutivas y la racha correspondiente."""
    orden = sorted(set(semanas), key=lunes_de)
    mejor: list[str] = []
    actual: list[str] = []
    for s in orden:
        if actual and semana_siguiente(actual[-1]) == s:
            actual.append(s)
        else:
            actual = [s]
        if len(actual) > len(mejor):
            mejor = list(actual)
    return len(mejor), mejor


# ---------------------------------------------------------------------------
# Carga de CSV
# ---------------------------------------------------------------------------

def leer_csv(ruta: str | Path, columnas_esperadas: list[str]) -> tuple[list[dict], list[str]]:
    """Lee un CSV con ``csv.DictReader``. Devuelve (filas, avisos). Nunca lanza por CSV vacío."""
    avisos: list[str] = []
    p = Path(ruta)
    if not p.exists():
        avisos.append(f"{p}: no existe (se trata como vacío)")
        return [], avisos
    with p.open(newline="", encoding="utf-8-sig") as fh:
        lector = csv.DictReader(fh)
        if not lector.fieldnames:
            avisos.append(f"{p}: CSV vacío, sin encabezado")
            return [], avisos
        faltan = [c for c in columnas_esperadas if c not in lector.fieldnames]
        if faltan:
            avisos.append(f"{p}: faltan columnas {faltan} (esquema de 06 §Esquema de datos)")
        filas = []
        for n, fila in enumerate(lector, start=2):
            if all(not (v or "").strip() for v in fila.values()):
                continue  # línea en blanco
            fila = {k: (v or "").strip() for k, v in fila.items() if k is not None}
            fila["_linea"] = n
            filas.append(fila)
    if not filas:
        avisos.append(f"{p}: solo encabezado, 0 filas")
    return filas, avisos


def cargar_produccion(ruta: str | Path) -> tuple[list[dict], list[str]]:
    """Carga y tipifica ``produccion.csv``. Filas con formato raro se reportan, no se descartan."""
    filas, avisos = leer_csv(ruta, COLUMNAS_PRODUCCION)
    out = []
    for f in filas:
        sid = f.get("siembra_id", "")
        if not RE_SIEMBRA_ID.match(sid):
            avisos.append(
                f"línea {f['_linea']}: siembra_id '{sid}' no cumple VAR-AAMMDD-Slote-RxNy "
                "(se conserva la fila)"
            )
        f["_fecha_siembra"] = parse_fecha(f.get("fecha_siembra"))
        f["_fecha_cosecha"] = parse_fecha(f.get("fecha_cosecha"))
        f["_variedad"] = normalizar(f.get("variedad"))
        f["_densidad"] = parse_num(f.get("densidad_g"))
        f["_rendimiento"] = parse_num(f.get("rendimiento_g"))
        f["_merma"] = parse_num(f.get("merma_pct"))
        f["_precio"] = parse_num(f.get("precio_mxn")) or 0.0
        f["_destino"] = normalizar(f.get("destino"))
        f["_tirada"] = (f["_merma"] or 0) >= 100 or f["_destino"] in {"basura", "tirada"}
        f["_cerrada"] = f["_fecha_cosecha"] is not None or f["_tirada"]
        f["_es_muestra"] = f["_destino"] in DESTINOS_MUESTRA
        f["_vendida"] = (f["_destino"] not in DESTINOS_NO_VENTA) and f["_precio"] > 0 and not f["_tirada"]
        if f["_fecha_siembra"] is None:
            avisos.append(f"línea {f['_linea']}: fecha_siembra inválida '{f.get('fecha_siembra')}'")
        if f.get("fecha_cosecha") and f["_fecha_cosecha"] is None:
            avisos.append(f"línea {f['_linea']}: fecha_cosecha inválida '{f.get('fecha_cosecha')}'")
        out.append(f)
    return out, avisos


def clasificar_venta(fila: dict) -> str:
    """``venta`` (cobrada), ``muestra`` (precio 0), ``rechazado`` (pedido no surtido) o ``sin_importe``.

    Convención de ``docs/fases/fase-1/gate.md``: un pedido rechazado por falta de producto se
    registra con ``precio_unit_mxn`` = 0, ``entregado_a_tiempo`` = no y ``feedback`` que
    empieza con "RECHAZADO". Las muestras llevan precio 0 y "muestra" en producto o feedback.
    """
    precio = parse_num(fila.get("precio_unit_mxn")) or 0.0
    cantidad = parse_num(fila.get("cantidad")) or 0.0
    fb = normalizar(fila.get("feedback"))
    prod = normalizar(fila.get("producto"))
    if fb.startswith("rechazado") or "rechazado sin capacidad" in fb:
        return "rechazado"
    if precio > 0 and cantidad > 0:
        return "venta"
    if "muestra" in prod or fb.startswith("muestra"):
        return "muestra"
    return "sin_importe"


def cargar_ventas(ruta: str | Path) -> tuple[list[dict], list[str]]:
    """Carga y tipifica ``ventas.csv``."""
    filas, avisos = leer_csv(ruta, COLUMNAS_VENTAS)
    out = []
    for f in filas:
        f["_fecha"] = parse_fecha(f.get("fecha"))
        f["_cliente"] = (f.get("cliente") or "").strip()
        f["_cantidad"] = parse_num(f.get("cantidad")) or 0.0
        f["_precio"] = parse_num(f.get("precio_unit_mxn")) or 0.0
        f["_importe"] = f["_cantidad"] * f["_precio"]
        f["_a_tiempo"] = normalizar(f.get("entregado_a_tiempo")) in {"si", "s", "1", "true", "yes"}
        f["_tipo"] = clasificar_venta(f)
        f["_producto"] = normalizar(f.get("producto"))
        if f["_fecha"] is None:
            avisos.append(f"línea {f['_linea']}: fecha inválida '{f.get('fecha')}'")
        out.append(f)
    return out, avisos


# ---------------------------------------------------------------------------
# Costos
# ---------------------------------------------------------------------------

def costos_desde_args(sobrescrituras: list[str] | None) -> tuple[dict[str, float], list[str]]:
    """``["girasol=9.10", "chicharo=18"]`` -> tabla de costos con esos valores sustituidos."""
    costos = dict(COSTO_VARIABLE_MXN)
    avisos = []
    for item in sobrescrituras or []:
        if "=" not in item:
            avisos.append(f"--costo '{item}' ignorado: usa variedad=valor")
            continue
        var, val = item.split("=", 1)
        v = parse_num(val)
        if v is None:
            avisos.append(f"--costo '{item}' ignorado: valor no numérico")
            continue
        costos[normalizar(var)] = v
    return costos, avisos


def variedad_de_producto(producto: str) -> str | None:
    """Detecta la variedad en el texto de ``producto`` (``charola girasol`` -> ``girasol``)."""
    p = normalizar(producto)
    for v in VARIEDADES:
        if v in p:
            return v
    return None


def costo_unitario(producto: str, costos: dict[str, float]) -> tuple[float | None, str | None]:
    """Costo variable de una unidad vendida según el texto de ``producto``.

    ``charola <variedad>`` -> costo de la tabla; ``clamshell`` -> costo/2.75 + $3.50;
    hierbas por manojo (NFT) -> sin dato en 08 -> (None, aviso).
    """
    p = normalizar(producto)
    var = variedad_de_producto(p)
    if var is None or var not in costos:
        return None, f"producto '{producto}': variedad sin costo en la tabla del 08 [POR VERIFICAR: agrega --costo {var or 'variedad'}=valor]"
    base = costos[var]
    if "clamshell" in p or "cortad" in p:
        return base / CLAMSHELLS_POR_CHAROLA + COSTO_CLAMSHELL_MXN, None
    if "manojo" in p or "canastilla" in p:
        return None, f"producto '{producto}': hierbas NFT sin costo por manojo en 08 [POR VERIFICAR: costo de canastilla + nutriente]"
    return base, None


# ---------------------------------------------------------------------------
# Cálculo de KPIs
# ---------------------------------------------------------------------------

def _pct(num: float, den: float) -> float | None:
    return None if not den else 100.0 * num / den


def semaforo(valor: float | None, clave: str) -> str:
    """``verde`` / ``ambar`` / ``ROJO`` / ``—`` según UMBRALES de 06 §L2."""
    if valor is None:
        return "—"
    u = UMBRALES[clave]
    if u["mayor_mejor"]:
        if valor >= u["meta"]:
            return "verde"
        if u["rojo"] is not None and valor < u["rojo"]:
            return "ROJO"
        return "ambar"
    if valor <= u["meta"]:
        return "verde"
    if u["rojo"] is not None and valor > u["rojo"]:
        return "ROJO"
    return "ambar"


def calcular_kpis(
    produccion: list[dict],
    ventas: list[dict],
    costos: dict[str, float] | None = None,
    reparto_por_parada: float = REPARTO_POR_PARADA_MXN,
    contar_muestras: bool = False,
    semanas: list[str] | None = None,
) -> dict:
    """Devuelve ``{"semanas": {AAAA-Www: {...}}, "orden": [...], "avisos": [...], "clientes": {...}}``."""
    costos = costos or dict(COSTO_VARIABLE_MXN)
    avisos: list[str] = []
    S: dict[str, dict] = defaultdict(lambda: {
        "sembradas": 0, "cerradas": 0, "tiradas": 0, "merma_suma": 0.0,
        "cosechadas": 0, "muestras": 0, "casa": 0, "vendidas": 0,
        "entregas": 0, "a_tiempo": 0, "feedback": 0, "rechazados": 0, "muestras_entregadas": 0,
        "ingreso": 0.0, "insumos": 0.0, "paradas_info": {}, "clientes": set(), "unidades": 0.0,
    })
    # --- producción ---
    for f in produccion:
        if f["_fecha_siembra"] is not None:
            w = semana_iso(f["_fecha_siembra"])
            S[w]["sembradas"] += 1
            if f["_cerrada"]:
                S[w]["cerradas"] += 1
                S[w]["merma_suma"] += min(f["_merma"] or 0.0, 100.0)
                if f["_tirada"]:
                    S[w]["tiradas"] += 1
        if f["_fecha_cosecha"] is not None and not f["_tirada"]:
            w = semana_iso(f["_fecha_cosecha"])
            S[w]["cosechadas"] += 1
            if f["_es_muestra"]:
                S[w]["muestras"] += 1
            elif f["_destino"] in {"casa", "prueba", ""}:
                S[w]["casa"] += 1
            if f["_vendida"]:
                S[w]["vendidas"] += 1
    # --- ventas ---
    clientes_semanas: dict[str, set[str]] = defaultdict(set)
    for v in ventas:
        if v["_fecha"] is None:
            continue
        w = semana_iso(v["_fecha"])
        if v["_tipo"] == "rechazado":
            S[w]["rechazados"] += int(v["_cantidad"] or 1)
            continue
        if v["_tipo"] == "muestra":
            S[w]["muestras_entregadas"] += int(v["_cantidad"] or 1)
            continue
        if v["_tipo"] != "venta":
            continue
        # una "entrega" es una parada (fecha + cliente); varios productos = una entrega
        info = S[w]["paradas_info"].setdefault((v["_fecha"], v["_cliente"]), {"a_tiempo": True, "feedback": False})
        info["a_tiempo"] = info["a_tiempo"] and v["_a_tiempo"]
        info["feedback"] = info["feedback"] or bool((v.get("feedback") or "").strip())
        S[w]["ingreso"] += v["_importe"]
        S[w]["unidades"] += v["_cantidad"]
        S[w]["clientes"].add(v["_cliente"])
        clientes_semanas[v["_cliente"]].add(w)
        cu, aviso = costo_unitario(v.get("producto", ""), costos)
        if cu is None:
            if aviso and aviso not in avisos:
                avisos.append(aviso)
            S[w]["insumos_sin_dato"] = True
        else:
            S[w]["insumos"] += cu * v["_cantidad"]
    # --- eje de semanas continuo ---
    if semanas is None:
        if not S:
            return {"semanas": {}, "orden": [], "avisos": avisos, "clientes": {}}
        todas = sorted(S.keys(), key=lunes_de)
        semanas = rango_semanas(todas[0], todas[-1])
    out: dict[str, dict] = {}
    prev_clientes: set[str] | None = None
    for w in semanas:
        s = S.get(w) or S.default_factory()
        s["entregas"] = len(s["paradas_info"])
        s["a_tiempo"] = sum(1 for i in s["paradas_info"].values() if i["a_tiempo"])
        s["feedback"] = sum(1 for i in s["paradas_info"].values() if i["feedback"])
        # muestras = CAC deliberado, fuera del denominador; "casa" = no vendida, cuenta en contra
        den_st = s["cosechadas"] if contar_muestras else s["cosechadas"] - s["muestras"]
        sell_through = _pct(s["vendidas"], den_st) if den_st > 0 else None
        merma = _pct(s["tiradas"], s["cerradas"]) if s["cerradas"] else None
        merma_media = (s["merma_suma"] / s["cerradas"]) if s["cerradas"] else None
        entregas_pct = _pct(s["a_tiempo"], s["entregas"]) if s["entregas"] else None
        feedback_pct = _pct(s["feedback"], s["entregas"]) if s["entregas"] else None
        if prev_clientes:
            recompra = _pct(len(s["clientes"] & prev_clientes), len(prev_clientes))
        else:
            recompra = None
        reparto = len(s["paradas_info"]) * reparto_por_parada
        if s["ingreso"] > 0 and not s.get("insumos_sin_dato"):
            margen = _pct(s["ingreso"] - s["insumos"] - reparto, s["ingreso"])
        else:
            margen = None
        nuevos = [c for c in s["clientes"] if min(clientes_semanas[c], key=lunes_de) == w]
        out[w] = {
            "semana": w,
            "lunes": lunes_de(w).isoformat(),
            "sembradas": s["sembradas"], "cerradas": s["cerradas"], "tiradas": s["tiradas"],
            "merma_pct": merma, "merma_media_pct": merma_media,
            "cosechadas": s["cosechadas"], "muestras": s["muestras"], "casa": s["casa"],
            "vendidas": s["vendidas"], "sell_through_pct": sell_through,
            "entregas": s["entregas"], "a_tiempo": s["a_tiempo"], "entregas_pct": entregas_pct,
            "clientes": sorted(s["clientes"]), "clientes_nuevos": sorted(nuevos),
            "recompra_pct": recompra,
            "ingreso_mxn": round(s["ingreso"], 2), "insumos_mxn": round(s["insumos"], 2),
            "reparto_mxn": round(reparto, 2), "paradas": len(s["paradas_info"]),
            "unidades_vendidas": s["unidades"], "margen_pct": margen,
            "feedback_pct": feedback_pct, "rechazados": s["rechazados"],
            "muestras_entregadas": s["muestras_entregadas"],
        }
        if s["clientes"]:
            prev_clientes = set(s["clientes"])
        elif prev_clientes is not None:
            prev_clientes = set()  # semana sin ventas: la recompra de la siguiente será sobre 0
    return {"semanas": out, "orden": list(semanas), "avisos": avisos, "clientes": dict(clientes_semanas)}


def resumen_variedades(produccion: list[dict]) -> list[dict]:
    """Rendimiento medio, CV (V2: aceptar < 15 %), merma y multiplicador por variedad."""
    por_var: dict[str, list[dict]] = defaultdict(list)
    for f in produccion:
        if f["_variedad"]:
            por_var[f["_variedad"]].append(f)
    filas = []
    for var, fs in sorted(por_var.items()):
        cerradas = [f for f in fs if f["_cerrada"]]
        pesadas = [f["_rendimiento"] for f in cerradas if not f["_tirada"] and f["_rendimiento"]]
        media = statistics.fmean(pesadas) if pesadas else None
        cv = (100 * statistics.stdev(pesadas) / media) if len(pesadas) >= 2 and media else None
        dens = [f["_densidad"] for f in cerradas if f["_densidad"]]
        mult = (media / statistics.fmean(dens)) if media and dens else None
        tiradas = sum(1 for f in cerradas if f["_tirada"])
        filas.append({
            "variedad": var, "sembradas": len(fs), "cerradas": len(cerradas),
            "pesadas": len(pesadas), "rendimiento_medio_g": media, "cv_pct": cv,
            "multiplicador": mult, "merma_pct": _pct(tiradas, len(cerradas)) if cerradas else None,
            "en_rack": len(fs) - len(cerradas),
        })
    return filas


def alertas(kpis: dict) -> list[str]:
    """Reglas de decisión escritas de antemano (06 §L2)."""
    out: list[str] = []
    orden = kpis["orden"]
    sem = kpis["semanas"]
    # sell-through < 75 % dos semanas seguidas
    for a, b in zip(orden, orden[1:]):
        sa, sb = sem[a]["sell_through_pct"], sem[b]["sell_through_pct"]
        if sa is not None and sb is not None and sa < 75 and sb < 75:
            out.append(f"Sell-through < 75 % en {a} y {b} (seguidas): NO sembrar más volumen; el problema es venta, no producción.")
    for w in orden:
        m = sem[w]["merma_pct"]
        if m is not None and m > 20:
            out.append(f"Merma > 20 % en {w} ({m:.0f} %): congelar variedad nueva, correr V8 y revisar densidad de siembra.")
        e = sem[w]["entregas_pct"]
        if e is not None and e < 90:
            out.append(f"Entregas a tiempo < 90 % en {w} ({e:.0f} %): revisar ruta y cosecha de la mañana.")
        g = sem[w]["margen_pct"]
        if g is not None and g < 45:
            out.append(f"Margen variable < 45 % en {w} ({g:.0f} %): subir precio o bajar costo (semilla, paradas).")
    # cliente sin pedir 2 semanas (solo clientes con >= 2 semanas de compra)
    if len(orden) >= 2:
        ult2 = set(orden[-2:])
        for cliente, semanas_c in sorted(kpis["clientes"].items()):
            if len(semanas_c) >= 2 and not (semanas_c & ult2):
                ultima = max(semanas_c, key=lunes_de)
                out.append(f"Cliente '{cliente}' sin pedir en {orden[-2]} ni {orden[-1]} (última compra {ultima}): visita presencial esta semana, no mensaje.")
    return out


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------

def _f(v: float | None, unidad: str = " %", dec: int = 0) -> str:
    return "—" if v is None else f"{v:,.{dec}f}{unidad}"


def tabla_semanal(kpis: dict, ultimas: int | None = None) -> str:
    """Tabla Markdown por semana con semáforo verde/ambar/ROJO."""
    orden = kpis["orden"][-ultimas:] if ultimas else kpis["orden"]
    if not orden:
        return "_Sin datos: ambas bitácoras están vacías o sin fechas válidas._\n"
    lineas = [
        "| Semana | Semb. | Cosech. | Muestras | Vend. | Sell-through | Merma (tiradas) | Entregas a tiempo | Recompra | Ingreso | Margen var. | Feedback |",
        "|---|---:|---:|---:|---:|---|---|---|---|---:|---|---|",
    ]
    for w in orden:
        s = kpis["semanas"][w]
        st = s["sell_through_pct"]
        lineas.append(
            f"| {w} | {s['sembradas']} | {s['cosechadas']} | {s['muestras']} | {s['vendidas']} "
            f"| {_f(st)} {semaforo(st, 'sell_through')} "
            f"| {_f(s['merma_pct'])} {semaforo(s['merma_pct'], 'merma')} "
            f"| {_f(s['entregas_pct'])} {semaforo(s['entregas_pct'], 'entregas')} "
            f"| {_f(s['recompra_pct'])} {semaforo(s['recompra_pct'], 'recompra')} "
            f"| ${s['ingreso_mxn']:,.0f} "
            f"| {_f(s['margen_pct'])} {semaforo(s['margen_pct'], 'margen')} "
            f"| {_f(s['feedback_pct'])} {semaforo(s['feedback_pct'], 'feedback')} |"
        )
    lineas.append("")
    lineas.append(
        "Metas (06 §L2): sell-through ≥ 90 % (rojo < 75 % dos semanas seguidas) · merma ≤ 10 % "
        "(rojo > 20 %) · entregas a tiempo 100 % (rojo < 90 %) · recompra ≥ 80 % · margen "
        "variable ≥ 60 % (rojo < 45 %) · feedback ≥ 50 %. Sell-through excluye las muestras del "
        "denominador (CAC deliberado; `--contar-muestras` las incluye); las charolas que se quedan "
        "en casa cuentan como no vendidas. Entregas y feedback se cuentan por parada (fecha + cliente)."
    )
    return "\n".join(lineas) + "\n"


def tabla_variedades(filas: list[dict]) -> str:
    if not filas:
        return "_Sin filas de producción._\n"
    lineas = [
        "| Variedad | Sembradas | En rack | Pesadas | Rendimiento medio | CV (V2 < 15 %) | Multiplicador | Merma (tiradas) |",
        "|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for r in filas:
        cv = r["cv_pct"]
        cv_txt = "—" if cv is None else f"{cv:.0f} % {'verde' if cv < 15 else 'ROJO'}"
        lineas.append(
            f"| {r['variedad']} | {r['sembradas']} | {r['en_rack']} | {r['pesadas']} "
            f"| {_f(r['rendimiento_medio_g'], ' g')} | {cv_txt} | {_f(r['multiplicador'], 'x', 1)} "
            f"| {_f(r['merma_pct'])} {semaforo(r['merma_pct'], 'merma')} |"
        )
    return "\n".join(lineas) + "\n"


def tabla_costos(costos: dict[str, float], reparto: float) -> str:
    items = " · ".join(f"{k} ${v:,.2f}" for k, v in sorted(costos.items()))
    return (f"Costos variables por charola usados (08 §Economía; cambia con `--costo var=valor`): "
            f"{items} · reparto ${reparto:,.0f}/parada.\n")


def informe_markdown(kpis: dict, variedades: list[dict], costos: dict[str, float], reparto: float,
                     avisos: list[str], ultimas: int | None = None, titulo: str = "KPIs L2") -> str:
    partes = [f"# {titulo}\n", tabla_semanal(kpis, ultimas), "\n## Por variedad\n", tabla_variedades(variedades),
              "\n", tabla_costos(costos, reparto)]
    al = alertas(kpis)
    partes.append("\n## Alertas (reglas de decisión 06 §L2)\n")
    partes.append("\n".join(f"- {a}" for a in al) + "\n" if al else "- Ninguna.\n")
    if avisos:
        partes.append("\n## Avisos de captura\n")
        partes.append("\n".join(f"- {a}" for a in avisos) + "\n")
    return "".join(partes)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="KPIs del lazo comercial L2 por semana ISO desde bitacora/produccion.csv y ventas.csv.",
        epilog="Fuente: docs/referencia/06-validacion-y-lazos-agenticos.md §L2 y 08-recetas-y-economia-unitaria.md.",
    )
    p.add_argument("--produccion", default="bitacora/produccion.csv", help="ruta a produccion.csv")
    p.add_argument("--ventas", default="bitacora/ventas.csv", help="ruta a ventas.csv")
    p.add_argument("--semanas", type=int, default=None, help="mostrar solo las últimas N semanas")
    p.add_argument("--costo", action="append", metavar="VARIEDAD=MXN",
                   help="sobrescribe el costo variable por charola (p. ej. girasol=9.10)")
    p.add_argument("--reparto", type=float, default=REPARTO_POR_PARADA_MXN,
                   help="costo por parada de reparto en MXN (default 20; rango 15-25)")
    p.add_argument("--contar-muestras", action="store_true",
                   help="incluye muestras y charolas para casa en el denominador del sell-through")
    p.add_argument("--json", action="store_true", help="imprime los KPIs en JSON en vez de Markdown")
    return p


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    costos, avisos = costos_desde_args(args.costo)
    prod, av1 = cargar_produccion(args.produccion)
    ven, av2 = cargar_ventas(args.ventas)
    avisos += av1 + av2
    kpis = calcular_kpis(prod, ven, costos, args.reparto, args.contar_muestras)
    avisos += kpis["avisos"]
    if args.json:
        salida = {"semanas": kpis["semanas"], "orden": kpis["orden"], "variedades": resumen_variedades(prod),
                  "alertas": alertas(kpis), "avisos": avisos, "costos": costos, "reparto_por_parada": args.reparto}
        print(json.dumps(salida, ensure_ascii=False, indent=2, default=str))
        return 0
    print(informe_markdown(kpis, resumen_variedades(prod), costos, args.reparto, avisos, args.semanas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
