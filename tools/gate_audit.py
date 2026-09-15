#!/usr/bin/env python3
"""Audita los gates de fase (lazo L4) contra la bitácora e imprime Go / No-Go con evidencia.

Los gates y sus umbrales son los de ``docs/referencia/06-validacion-y-lazos-agenticos.md``
§L4 y no se renegocian aquí; el script solo mide:

* **G0-1**  (a) clientes con ≥ 3 compras semanales consecutivas ≥ 2 (``ventas.csv``);
            (b) margen variable en ventas reales ≥ 55 % (``produccion.csv`` + costos del 08).
* **G1-2**  (1) clientes fijos ≥ 4 (recurrentes con pedido en las 2 últimas semanas);
            (2) pedidos rechazados por falta de producto 2 semanas seguidas (filas con
            ``feedback`` "RECHAZADO ..." en ``ventas.csv``);
            (3) automatización v1 estable 30 días: < 2 alarmas críticas/semana (export de HA
            o ``--criticas-por-semana``) y cero charolas perdidas por fallo de riego.
* **G2-3**  (a) neto ≥ $12,000/mes 3 meses seguidos (``cobranza.csv`` cobrado − ``costos.csv``);
            (b) ≤ 9 h/semana medidas, promedio de 4 semanas (``timesheet.csv``).

Uso::

    python3 tools/gate_audit.py --gate G0-1 --ventas bitacora/ventas.csv \\
        --produccion bitacora/produccion.csv --desde 2026-09-21 --hasta 2026-10-30
    python3 tools/gate_audit.py --gate G1-2 --ha bitacora/ha/2027-W05.csv bitacora/ha/2027-W06.csv
    python3 tools/gate_audit.py --gate G2-3 --cobranza bitacora/cobranza.csv \\
        --costos bitacora/costos.csv --timesheet bitacora/timesheet.csv --guardar

Códigos de salida: 0 = GO, 1 = NO-GO (o sin datos suficientes), 2 = error de uso.
Solo biblioteca estándar (Python 3.11). Importa ``kpis.py`` del mismo directorio.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kpis as K  # noqa: E402

GATES = {
    "G0-1": "Fase 0 → 1: validación comercial",
    "G1-2": "Fase 1 → 2: clientes fijos, demanda insatisfecha y automatización v1 estable",
    "G2-3": "Fase 2 → 3: el sistema se paga solo",
}
UMBRAL_G01_RECURRENTES = 2
UMBRAL_G01_MARGEN = 55.0
UMBRAL_G12_FIJOS = 4
UMBRAL_G12_CRITICAS_SEMANA = 2   # PASS si < 2
UMBRAL_G23_NETO_MES = 12_000.0
UMBRAL_G23_MESES = 3
UMBRAL_G23_HORAS = 9.0
SEMANAS_TIMESHEET = 4

COLUMNAS_COBRANZA = ["factura", "cliente", "fecha_emision", "fecha_vencimiento", "fecha_cobro",
                     "monto", "pue_ppd", "rep_emitido", "estado"]
#: Esquema propuesto para costos.csv [POR VERIFICAR: ninguna página lo fija; fase-2/gate.md
#: solo lista las categorías insumos, servicios, reparto, ayudante, reposiciones, fondo].
COLUMNAS_COSTOS = ["fecha", "categoria", "concepto", "monto"]
COLUMNAS_TIMESHEET = ["fecha", "semana", "rubro", "minutos"]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def normalizar_gate(texto: str) -> str:
    t = texto.upper().replace("→", "-").replace("->", "-").replace("_", "-").replace(" ", "")
    t = {"G01": "G0-1", "G12": "G1-2", "G23": "G2-3"}.get(t, t)
    if t not in GATES:
        raise SystemExit(f"gate desconocido '{texto}'; usa G0-1, G1-2 o G2-3")
    return t


def en_ventana(d: date | None, desde: date, hasta: date) -> bool:
    return d is not None and desde <= d <= hasta


def ventana_por_defecto(prod: list[dict], ven: list[dict], desde: str | None, hasta: str | None) -> tuple[date, date]:
    fechas = [f["_fecha_siembra"] for f in prod] + [f["_fecha_cosecha"] for f in prod] + [v["_fecha"] for v in ven]
    fechas = [f for f in fechas if f is not None]
    d = K.parse_fecha(desde) if desde else (min(fechas) if fechas else date.today())
    h = K.parse_fecha(hasta) if hasta else (max(fechas) if fechas else date.today())
    if desde and d is None or hasta and h is None:
        raise SystemExit("--desde/--hasta deben ser AAAA-MM-DD")
    return d, h


def mes_de(d: date) -> str:
    return f"{d.year}-{d.month:02d}"


def meses_en(desde: date, hasta: date) -> list[str]:
    out = []
    y, m = desde.year, desde.month
    while (y, m) <= (hasta.year, hasta.month):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return out


def _pass(ok: bool | None) -> str:
    return "SIN DATO" if ok is None else ("PASS" if ok else "FAIL")


def _pct(v: float | None) -> str:
    return "—" if v is None else f"{v:.1f} %"


# ---------------------------------------------------------------------------
# Piezas comunes: tabla cliente × semana y margen desde producción
# ---------------------------------------------------------------------------

def compras_por_cliente(ventas: list[dict], desde: date, hasta: date) -> tuple[dict[str, dict[str, float]], list[str]]:
    """{cliente: {semana: importe}} solo con ventas cobradas (cantidad y precio > 0) en la ventana."""
    tabla: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for v in ventas:
        if v["_tipo"] != "venta" or not en_ventana(v["_fecha"], desde, hasta):
            continue
        tabla[v["_cliente"]][K.semana_iso(v["_fecha"])] += v["_importe"]
    semanas = K.rango_semanas(K.semana_iso(desde), K.semana_iso(hasta))
    return {c: dict(s) for c, s in tabla.items()}, semanas


def tabla_cliente_semana_md(tabla: dict[str, dict[str, float]], semanas: list[str], extra: dict[str, str] | None = None,
                            titulo_extra: str = "Recurrente (≥ 3)") -> str:
    if not tabla:
        return "_Sin ventas cobradas en la ventana._\n"
    enc = "| Cliente | " + " | ".join(s[5:] for s in semanas) + f" | Racha máx. | {titulo_extra} |"
    sep = "|---|" + "---:|" * len(semanas) + "---:|---|"
    lineas = [f"Semanas ISO {semanas[0]} … {semanas[-1]} (importe cobrado en MXN; · = sin pedido)", "", enc, sep]
    for cliente in sorted(tabla):
        celdas = [f"{tabla[cliente][s]:,.0f}" if s in tabla[cliente] else "·" for s in semanas]
        racha, _ = K.racha_maxima(tabla[cliente].keys())
        marca = (extra or {}).get(cliente, "sí" if racha >= 3 else "no")
        lineas.append(f"| {cliente} | " + " | ".join(celdas) + f" | {racha} | {marca} |")
    return "\n".join(lineas) + "\n"


def margen_desde_produccion(prod: list[dict], ventas: list[dict], desde: date, hasta: date,
                            costos: dict[str, float], reparto: float) -> dict:
    """(Σ precio_mxn − Σ costo variable − paradas × reparto) / Σ precio, charolas cosechadas y vendidas."""
    vendidas = [f for f in prod if f["_vendida"] and en_ventana(f["_fecha_cosecha"], desde, hasta)]
    ingreso = sum(f["_precio"] for f in vendidas)
    insumos = 0.0
    sin_costo: dict[str, int] = defaultdict(int)
    for f in vendidas:
        if f["_variedad"] in costos:
            insumos += costos[f["_variedad"]]
        else:
            sin_costo[f["_variedad"] or "(vacía)"] += 1
    paradas = {(v["_fecha"], v["_cliente"]) for v in ventas if v["_tipo"] == "venta" and en_ventana(v["_fecha"], desde, hasta)}
    rep = len(paradas) * reparto
    ingreso_ventas = sum(v["_importe"] for v in ventas if v["_tipo"] == "venta" and en_ventana(v["_fecha"], desde, hasta))
    margen = (100.0 * (ingreso - insumos - rep) / ingreso) if ingreso > 0 and not sin_costo else None
    return {"charolas": len(vendidas), "ingreso": ingreso, "insumos": insumos, "paradas": len(paradas),
            "reparto": rep, "margen": margen, "sin_costo": dict(sin_costo), "ingreso_ventas": ingreso_ventas}


def margen_md(m: dict, reparto: float) -> str:
    lineas = ["| Concepto | MXN |", "|---|---:|",
              f"| Ingreso de charolas vendidas en `produccion.csv` ({m['charolas']} charolas con destino cliente y precio > 0) | {m['ingreso']:,.0f} |",
              f"| Insumos (costo variable por variedad, 08 §Economía) | {m['insumos']:,.0f} |",
              f"| Reparto ({m['paradas']} paradas × ${reparto:,.0f}) | {m['reparto']:,.0f} |",
              f"| **Margen variable** | **{_pct(m['margen'])}** |", ""]
    dif = m["ingreso"] - m["ingreso_ventas"]
    lineas.append(f"Cruce con `ventas.csv` (Σ cantidad × precio cobrado): ${m['ingreso_ventas']:,.0f}"
                  + (f" — **no cuadra con producción por ${dif:,.0f}; concilia antes de decidir**" if abs(dif) > max(50.0, 0.05 * max(m['ingreso'], 1)) else " — cuadra."))
    if m["sin_costo"]:
        lineas.append("")
        lineas.append("[POR VERIFICAR: variedades sin costo en la tabla del 08 → margen no calculable: "
                      + ", ".join(f"{k} ({n})" for k, n in m["sin_costo"].items()) + ". Usa `--costo variedad=valor`.]")
    return "\n".join(lineas) + "\n"


def kpis_apoyo_md(prod: list[dict], ven: list[dict], costos: dict[str, float], reparto: float, semanas: int = 4) -> str:
    k = K.calcular_kpis(prod, ven, costos, reparto)
    al = K.alertas(k)
    txt = K.tabla_semanal(k, ultimas=semanas)
    if al:
        txt += "\nAlertas L2: " + " · ".join(al) + "\n"
    return txt


# ---------------------------------------------------------------------------
# G0-1
# ---------------------------------------------------------------------------

def evaluar_g01(prod, ven, desde, hasta, costos, reparto) -> tuple[bool, str]:
    tabla, semanas = compras_por_cliente(ven, desde, hasta)
    recurrentes = [c for c, s in tabla.items() if K.racha_maxima(s.keys())[0] >= 3]
    ok_a = len(recurrentes) >= UMBRAL_G01_RECURRENTES
    m = margen_desde_produccion(prod, ven, desde, hasta, costos, reparto)
    ok_b = None if m["margen"] is None else m["margen"] >= UMBRAL_G01_MARGEN
    partes = [
        f"## (a) Clientes con ≥ 3 compras semanales consecutivas — umbral ≥ {UMBRAL_G01_RECURRENTES}\n",
        "Compra semanal = al menos una entrega cobrada (cantidad × precio > 0) en la semana ISO; muestras y "
        "pedidos rechazados no cuentan; una semana sin pedido reinicia la racha.\n\n",
        tabla_cliente_semana_md(tabla, semanas),
        f"\n**Resultado (a): {len(recurrentes)} recurrentes ({', '.join(sorted(recurrentes)) or 'ninguno'}) → {_pass(ok_a)}**\n",
        f"\n## (b) Margen variable en ventas reales — umbral ≥ {UMBRAL_G01_MARGEN:.0f} %\n\n",
        margen_md(m, reparto),
        f"\n**Resultado (b): {_pct(m['margen'])} → {_pass(ok_b)}**\n",
        "\n## KPIs de apoyo (L2, últimas 4 semanas; contexto, no gate)\n\n",
        kpis_apoyo_md(prod, ven, costos, reparto),
    ]
    go = bool(ok_a and ok_b)
    dec = ["\n## Decisión\n"]
    if go:
        dec.append("**GO a Fase 1.** Acepta cotizaciones (herrero, PTR, malla, tinaco), fija fecha del herrero y "
                   "recompra girasol CEDA. Cierra el issue del gate con los dos números y commitea este informe.\n")
    else:
        dec.append("**NO-GO.**\n")
        if not ok_a:
            dec.append(f"- (a) {len(recurrentes)} < {UMBRAL_G01_RECURRENTES} recurrentes → iterar 2 semanas más (cambiar precio, zona o "
                       "producto; 5–8 visitas nuevas) o abortar con pérdida acotada ~$6k. No se renegocia el umbral.\n")
        if ok_b is False:
            dec.append(f"- (b) margen {_pct(m['margen'])} < {UMBRAL_G01_MARGEN:.0f} % → subir precio o bajar costo (girasol CEDA "
                       "validado, quitar variedades caras, agrupar paradas) **antes** de invertir; re-medir 2 semanas.\n")
        if ok_b is None:
            dec.append("- (b) sin dato: no hay charolas vendidas con precio en `produccion.csv` o falta costo por variedad.\n")
    return go, "".join(partes + dec)


# ---------------------------------------------------------------------------
# G1-2
# ---------------------------------------------------------------------------

def cargar_alarmas(rutas: list[str] | None, manual: str | None) -> tuple[dict[str, int], list[str]]:
    """Alarmas críticas por semana ISO desde exports de HA o desde ``--criticas-por-semana``.

    Export de HA [POR VERIFICAR: esquema definitivo en software/home-assistant.md]: se cuenta
    como crítica toda fila con alguna celda que contenga "critic" (crítica/critical) y se fecha
    con la primera celda que parsea como AAAA-MM-DD.
    """
    criticas: dict[str, int] = defaultdict(int)
    avisos: list[str] = []
    for ruta in rutas or []:
        filas, av = K.leer_csv(ruta, [])
        avisos += av
        n = 0
        for f in filas:
            fecha = next((K.parse_fecha(v) for v in f.values() if isinstance(v, str) and K.parse_fecha(v)), None)
            es_critica = any("critic" in K.normalizar(v) for v in f.values() if isinstance(v, str))
            if fecha and es_critica:
                criticas[K.semana_iso(fecha)] += 1
                n += 1
            elif fecha:
                criticas.setdefault(K.semana_iso(fecha), 0)
        avisos.append(f"{ruta}: {len(filas)} filas, {n} críticas")
    if manual:
        for item in manual.split(","):
            if "=" in item:
                s, n = item.split("=", 1)
                criticas[s.strip().upper()] = int(K.parse_num(n) or 0)
    return dict(criticas), avisos


def evaluar_g12(prod, ven, desde, hasta, costos, reparto, ha: list[str] | None, manual: str | None) -> tuple[bool, str]:
    tabla, semanas = compras_por_cliente(ven, desde, hasta)
    ult2 = semanas[-2:]
    fijos = [c for c, s in tabla.items() if K.racha_maxima(s.keys())[0] >= 3 and all(w in s for w in ult2)]
    marcas = {c: ("fijo" if c in fijos else "no") for c in tabla}
    ok_1 = len(fijos) >= UMBRAL_G12_FIJOS
    # (2) demanda insatisfecha
    rech: dict[str, int] = defaultdict(int)
    for v in ven:
        if v["_tipo"] == "rechazado" and en_ventana(v["_fecha"], desde, hasta):
            rech[K.semana_iso(v["_fecha"])] += int(v["_cantidad"] or 1)
    pares = [(a, b) for a, b in zip(semanas, semanas[1:]) if rech.get(a) and rech.get(b)]
    ok_2 = bool(pares)
    # (3) v1 estable 30 días
    ini30 = hasta - timedelta(days=29)
    criticas, av_ha = cargar_alarmas(ha, manual)
    semanas30 = K.rango_semanas(K.semana_iso(ini30), K.semana_iso(hasta))
    perdidas = [f for f in prod if (f["_merma"] or 0) > 0 and "riego" in K.normalizar(f.get("observaciones"))
                and (en_ventana(f["_fecha_cosecha"], ini30, hasta) or en_ventana(f["_fecha_siembra"], ini30, hasta))]
    if criticas:
        faltan = [w for w in semanas30 if w not in criticas]
        max_crit = max(criticas.get(w, 0) for w in semanas30)
        ok_3 = (not faltan) and max_crit < UMBRAL_G12_CRITICAS_SEMANA and not perdidas
    else:
        faltan, max_crit, ok_3 = semanas30, None, None
    partes = [
        f"## (1) Clientes fijos — umbral ≥ {UMBRAL_G12_FIJOS} (meta 4–5)\n",
        f"Fijo = recurrente (≥ 3 compras semanales consecutivas) **y** con pedido en {ult2[0]} y {ult2[-1]}.\n\n",
        tabla_cliente_semana_md(tabla, semanas, marcas, "Fijo"),
        f"\n**Resultado (1): {len(fijos)} fijos ({', '.join(sorted(fijos)) or 'ninguno'}) → {_pass(ok_1)}**\n",
        "\n## (2) Demanda insatisfecha — pedidos rechazados por falta de producto 2 semanas seguidas\n\n",
        "Fila con `feedback` \"RECHAZADO sin capacidad\" (precio 0, entregado no) en `ventas.csv`.\n\n",
        ("| Semana | Charolas rechazadas |\n|---|---:|\n" + "\n".join(f"| {w} | {rech[w]} |" for w in semanas if w in rech) + "\n") if rech else "_Sin pedidos rechazados registrados._\n",
        f"\n**Resultado (2): {('semanas seguidas ' + ' y '.join(pares[-1])) if pares else 'sin dos semanas seguidas'} → {_pass(ok_2)}**\n",
        f"\n## (3) Automatización v1 estable — 30 días ({ini30} a {hasta}) con < {UMBRAL_G12_CRITICAS_SEMANA} críticas/semana y 0 charolas perdidas por riego\n\n",
    ]
    if criticas:
        partes.append("| Semana | Alarmas críticas |\n|---|---:|\n" + "\n".join(f"| {w} | {criticas.get(w, '—')} |" for w in semanas30) + "\n")
        if faltan:
            partes.append(f"\nSemanas sin export de HA: {', '.join(faltan)} → no se puede aprobar sin evidencia.\n")
    else:
        partes.append("_Sin export de HA ni `--criticas-por-semana`: métrica SIN DATO. Exporta las alarmas críticas "
                      "(tinaco < 20 %, nodo caído, corte con pérdida) de los 30 días o pásalas a mano._\n")
    partes.append(f"\nCharolas con merma y \"riego\" en observaciones dentro de los 30 días: {len(perdidas)}"
                  + ("".join(f"\n- {f['siembra_id']}: {f.get('observaciones')}" for f in perdidas)) + "\n")
    if av_ha:
        partes.append("\n" + "\n".join(f"- {a}" for a in av_ha) + "\n")
    partes.append(f"\n**Resultado (3): máx. {max_crit if max_crit is not None else '—'} críticas/semana, {len(perdidas)} pérdidas por riego → {_pass(ok_3)}**\n")
    partes.append("\n## KPIs de apoyo (L2, últimas 4 semanas)\n\n" + kpis_apoyo_md(prod, ven, costos, reparto))
    go = bool(ok_1 and ok_2 and ok_3)
    dec = ["\n## Decisión\n"]
    if go:
        dec.append("**GO a Fase 2.** Compra primero PVC + bomba + depósito; sondas y peristálticas al final. Cierra el issue con los tres números.\n")
    else:
        dec.append("**NO-GO.**\n")
        if not ok_1:
            dec.append(f"- (1) {len(fijos)} < {UMBRAL_G12_FIJOS} fijos → seguir vendiendo con el túnel 4 semanas más (visitas, referidos, suscripción a hogares); NO comprar NFT.\n")
        if not ok_2:
            dec.append("- (2) sin demanda insatisfecha 2 semanas seguidas → hay capacidad ociosa: más clientes, no más m²; iterar 4 semanas.\n")
        if ok_3 is False:
            dec.append("- (3) v1 inestable → corregir la causa raíz y reiniciar el reloj de 30 días; NO agregar NFT sobre una base inestable.\n")
        if ok_3 is None:
            dec.append("- (3) SIN DATO → exporta las alarmas de HA de 30 días (o `--criticas-por-semana 2027-W10=1,...`) y vuelve a correr.\n")
    return go, "".join(partes + dec)


# ---------------------------------------------------------------------------
# G2-3
# ---------------------------------------------------------------------------

def evaluar_g23(prod, ven, desde, hasta, costos, reparto, cobranza: str | None, costos_csv: str | None,
                timesheet: str | None) -> tuple[bool, str]:
    meses = meses_en(desde, hasta)
    partes = [f"## (a) Neto mensual — umbral ≥ ${UMBRAL_G23_NETO_MES:,.0f}/mes durante {UMBRAL_G23_MESES} meses consecutivos\n\n",
              "Neto = cobrado (SPEI conciliado; `cobranza.csv` con `estado` = cobrada y `fecha_cobro` en el mes) − costos "
              "del mes (`costos.csv`: insumos, servicios, reparto, ayudante, reposiciones, fondo). Lo facturado no cobrado no es ingreso.\n\n"]
    avisos: list[str] = []
    cobrado: dict[str, float] = defaultdict(float)
    costos_mes: dict[str, float] = defaultdict(float)
    costos_cat: dict[str, float] = defaultdict(float)
    ok_a: bool | None = None
    if cobranza:
        filas, av = K.leer_csv(cobranza, COLUMNAS_COBRANZA)
        avisos += av
        for f in filas:
            fc = K.parse_fecha(f.get("fecha_cobro"))
            if K.normalizar(f.get("estado")) == "cobrada" and en_ventana(fc, desde, hasta):
                cobrado[mes_de(fc)] += K.parse_num(f.get("monto")) or 0.0
    if costos_csv:
        filas, av = K.leer_csv(costos_csv, COLUMNAS_COSTOS)
        avisos += av
        for f in filas:
            fd = K.parse_fecha(f.get("fecha"))
            if en_ventana(fd, desde, hasta):
                monto = K.parse_num(f.get("monto")) or 0.0
                costos_mes[mes_de(fd)] += monto
                costos_cat[K.normalizar(f.get("categoria")) or "(sin categoría)"] += monto
    entregado_mes: dict[str, float] = defaultdict(float)
    for v in ven:
        if v["_tipo"] == "venta" and en_ventana(v["_fecha"], desde, hasta):
            entregado_mes[mes_de(v["_fecha"])] += v["_importe"]
    if cobranza and costos_csv:
        netos = {m: cobrado.get(m, 0.0) - costos_mes.get(m, 0.0) for m in meses}
        ult3 = meses[-UMBRAL_G23_MESES:]
        ok_a = len(meses) >= UMBRAL_G23_MESES and all(netos[m] >= UMBRAL_G23_NETO_MES for m in ult3)
        partes.append("| Mes | Cobrado | Costos | Neto | ≥ $12,000 |\n|---|---:|---:|---:|---|\n")
        for m in meses:
            partes.append(f"| {m} | {cobrado.get(m, 0):,.0f} | {costos_mes.get(m, 0):,.0f} | {netos[m]:,.0f} | {'sí' if netos[m] >= UMBRAL_G23_NETO_MES else 'no'} |\n")
        if costos_cat:
            partes.append("\nCostos por categoría en la ventana: " + " · ".join(f"{k} ${v:,.0f}" for k, v in sorted(costos_cat.items(), key=lambda kv: -kv[1])) + "\n")
        partes.append(f"\n**Resultado (a): {sum(1 for m in ult3 if netos[m] >= UMBRAL_G23_NETO_MES)} de {len(ult3)} últimos meses ≥ $12,000 → {_pass(ok_a)}**\n")
    else:
        partes.append("_SIN DATO: faltan `--cobranza` y/o `--costos`._ Referencia (NO válida para el gate, es entregado/facturado, no cobrado): "
                      + ", ".join(f"{m} ${entregado_mes.get(m, 0):,.0f}" for m in meses) + "\n")
        partes.append(f"\n**Resultado (a): {_pass(None)}**\n")
    # (b) horas
    partes.append(f"\n## (b) Horas del fundador — umbral ≤ {UMBRAL_G23_HORAS:.0f} h/semana, promedio de {SEMANAS_TIMESHEET} semanas (V9)\n\n")
    ok_b: bool | None = None
    if timesheet:
        filas, av = K.leer_csv(timesheet, COLUMNAS_TIMESHEET)
        avisos += av
        por_sem: dict[str, float] = defaultdict(float)
        por_rubro: dict[str, float] = defaultdict(float)
        for f in filas:
            fd = K.parse_fecha(f.get("fecha"))
            sem = (f.get("semana") or "").strip().upper() or (K.semana_iso(fd) if fd else "")
            if not sem or (fd and not en_ventana(fd, desde, hasta)):
                continue
            mins = K.parse_num(f.get("minutos")) or 0.0
            por_sem[sem] += mins / 60.0
            por_rubro[(sem, K.normalizar(f.get("rubro")) or "otro")] += mins / 60.0
        semanas_ts = sorted(por_sem, key=K.lunes_de)[-SEMANAS_TIMESHEET:]
        if semanas_ts:
            prom = sum(por_sem[s] for s in semanas_ts) / len(semanas_ts)
            rubros: dict[str, float] = defaultdict(float)
            for (s, r), h in por_rubro.items():
                if s in semanas_ts:
                    rubros[r] += h / len(semanas_ts)
            ok_b = prom <= UMBRAL_G23_HORAS and len(semanas_ts) >= SEMANAS_TIMESHEET
            partes.append("| Semana | Horas |\n|---|---:|\n" + "\n".join(f"| {s} | {por_sem[s]:.1f} |" for s in semanas_ts) + "\n")
            partes.append("\nPromedio por rubro (h/semana): " + " · ".join(f"{r} {h:.1f}" for r, h in sorted(rubros.items(), key=lambda kv: -kv[1])) + "\n")
            mayor = max(rubros.items(), key=lambda kv: kv[1])[0] if rubros else "—"
            if len(semanas_ts) < SEMANAS_TIMESHEET:
                partes.append(f"\nSolo {len(semanas_ts)} semanas medidas; V9 pide {SEMANAS_TIMESHEET} seguidas.\n")
            partes.append(f"\n**Resultado (b): {prom:.1f} h/semana; rubro más caro: {mayor} → {_pass(ok_b)}**\n")
            if prom > 12:
                partes.append("\n> 12 h: la automatización tiene un hueco o el proceso tiene un desperdicio; atacar el rubro más caro antes de escalar volumen (06 §V9).\n")
        else:
            partes.append("_`timesheet.csv` sin filas en la ventana._\n\n**Resultado (b): SIN DATO**\n")
    else:
        partes.append("_SIN DATO: falta `--timesheet`._\n\n**Resultado (b): SIN DATO**\n")
    # apoyo
    partes.append("\n## Apoyo (contexto, no gate)\n\n")
    total = sum(entregado_mes.values())
    if total > 0:
        por_cli: dict[str, float] = defaultdict(float)
        for v in ven:
            if v["_tipo"] == "venta" and en_ventana(v["_fecha"], desde, hasta):
                por_cli[v["_cliente"]] += v["_importe"]
        c, imp = max(por_cli.items(), key=lambda kv: kv[1])
        partes.append(f"- Cliente mayor: {c} con {100 * imp / total:.0f} % de las ventas (regla: ningún cliente > 25–30 %).\n")
    if cobranza:
        filas, _ = K.leer_csv(cobranza, COLUMNAS_COBRANZA)
        vencidas = [f for f in filas if K.normalizar(f.get("estado")) in {"emitida", "vencida"}
                    and K.parse_fecha(f.get("fecha_vencimiento")) and K.parse_fecha(f.get("fecha_vencimiento")) + timedelta(days=15) < hasta]
        partes.append(f"- Cartera vencida > 15 días al {hasta}: {len(vencidas)} facturas por ${sum(K.parse_num(f.get('monto')) or 0 for f in vencidas):,.0f}.\n")
    partes.append("\n" + kpis_apoyo_md(prod, ven, costos, reparto))
    if avisos:
        partes.append("\nAvisos: " + " · ".join(avisos) + "\n")
    go = bool(ok_a and ok_b)
    dec = ["\n## Decisión\n"]
    if go:
        dec.append("**GO a Fase 3.** Presupuesto discrecional desde utilidades; elige UN juguete primero.\n")
    else:
        dec.append("**NO-GO: permanecer en Fase 2.**\n")
        if ok_a is False:
            dec.append("- (a) neto < $12,000 en alguno de los 3 meses → escalera: quitar promos y cobrar lista → 10 hogares suscritos → Mercado el 100 → revisar mix por $/charola-semana. Re-gate en 3 meses, mismo umbral.\n")
        if ok_b is False:
            dec.append("- (b) > 9 h/semana → atacar horas: ayudante 6 h/sábado con SOP, ruta de 2 días y ≤ 8 paradas, charola viva en vez de cortado.\n")
        if ok_a is None or ok_b is None:
            dec.append("- Faltan datos (cobranza, costos o timesheet): el gate no se aprueba sin evidencia.\n")
    return go, "".join(partes + dec)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Audita un gate de fase (L4) contra la bitácora e imprime Go / No-Go con evidencia.",
        epilog="Umbrales: docs/referencia/06-validacion-y-lazos-agenticos.md §L4. Salida 0 = GO, 1 = NO-GO, 2 = error.",
    )
    p.add_argument("--gate", required=True, help="G0-1, G1-2 o G2-3")
    p.add_argument("--ventas", default="bitacora/ventas.csv")
    p.add_argument("--produccion", default="bitacora/produccion.csv")
    p.add_argument("--desde", help="AAAA-MM-DD (default: primera fecha en la bitácora)")
    p.add_argument("--hasta", help="AAAA-MM-DD (default: última fecha en la bitácora)")
    p.add_argument("--costo", action="append", metavar="VARIEDAD=MXN", help="sobrescribe costo variable (p. ej. girasol=9.10)")
    p.add_argument("--reparto", type=float, default=K.REPARTO_POR_PARADA_MXN, help="MXN por parada (default 20)")
    p.add_argument("--ha", nargs="*", metavar="CSV", help="G1-2: exports de Home Assistant con alarmas")
    p.add_argument("--criticas-por-semana", metavar="AAAA-Www=N,...", help="G1-2: alarmas críticas por semana, a mano")
    p.add_argument("--cobranza", help="G2-3: bitacora/cobranza.csv")
    p.add_argument("--costos", help="G2-3: bitacora/costos.csv (fecha,categoria,concepto,monto)")
    p.add_argument("--timesheet", help="G2-3: bitacora/timesheet.csv")
    p.add_argument("--guardar", action="store_true", help="escribe el informe en bitacora/gates/<GATE>-<hoy>.md")
    p.add_argument("--dir-gates", default="bitacora/gates", help="carpeta para --guardar")
    p.add_argument("--salida", help="ruta explícita del informe Markdown")
    return p


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    gate = normalizar_gate(args.gate)
    costos, avisos = K.costos_desde_args(args.costo)
    prod, av1 = K.cargar_produccion(args.produccion)
    ven, av2 = K.cargar_ventas(args.ventas)
    avisos += av1 + av2
    desde, hasta = ventana_por_defecto(prod, ven, args.desde, args.hasta)
    hoy = date.today()
    cab = [f"# Gate {gate} — auditoría {hoy.isoformat()}\n",
           f"{GATES[gate]}. Ventana {desde} → {hasta} (semanas {K.semana_iso(desde)} … {K.semana_iso(hasta)}). "
           f"Fuentes: `{args.ventas}` ({len(ven)} filas), `{args.produccion}` ({len(prod)} filas). "
           f"Costos: " + ", ".join(f"{k} ${v:,.2f}" for k, v in sorted(costos.items())) + f"; reparto ${args.reparto:,.0f}/parada.\n\n"]
    if gate == "G0-1":
        go, cuerpo = evaluar_g01(prod, ven, desde, hasta, costos, args.reparto)
    elif gate == "G1-2":
        go, cuerpo = evaluar_g12(prod, ven, desde, hasta, costos, args.reparto, args.ha, args.criticas_por_semana)
    else:
        go, cuerpo = evaluar_g23(prod, ven, desde, hasta, costos, args.reparto, args.cobranza, args.costos, args.timesheet)
    pie = ["\nRegla dura (06 §L4): un gate no alcanzado no se renegocia a la baja; se itera o se detiene. "
           "Commitea este informe: los commits son el registro de que no se movieron los postes.\n"]
    if avisos:
        pie.append("\n## Avisos de captura\n" + "\n".join(f"- {a}" for a in avisos) + "\n")
    informe = "".join(cab) + cuerpo + "".join(pie)
    print(informe)
    ruta = Path(args.salida) if args.salida else (Path(args.dir_gates) / f"{gate}-{hoy.isoformat()}.md" if args.guardar else None)
    if ruta:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(informe, encoding="utf-8")
        print(f"\n(informe guardado en {ruta})")
    print(f"\n=== {gate}: {'GO' if go else 'NO-GO'} ===")
    return 0 if go else 1


if __name__ == "__main__":
    sys.exit(main())
