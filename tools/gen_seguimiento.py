#!/usr/bin/env python3
"""Genera docs/assets/datos/seguimiento.json, los datos del tablero de seguimiento.

El tablero (docs/seguimiento.md) no guarda una copia de las partidas ni de los
umbrales: los lee de aqui, y este archivo sale de bom/partidas.csv y de los
criterios escritos en docs/validacion/gates.md. Asi el tablero no puede
desincronizarse del BOM, que es el error que este repo ya tuvo una vez.

Uso:
    python3 tools/gen_seguimiento.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "assets" / "datos" / "seguimiento.json"


def num(s: str) -> float:
    return float(s) if s else 0.0


# Umbrales copiados de docs/validacion/gates.md. Son EDITABLES desde el tablero
# (tras la contrasena) porque el usuario puede querer simular escenarios, pero el
# valor de partida es siempre el que esta escrito en la wiki.
GATES = [
    {
        "id": "G0-1",
        "nombre": "G0→1 · ¿los chefs pagan?",
        "cuando": "Cierre de la semana 6",
        "criterios": [
            {"id": "g01a", "metrica": "Clientes con ≥3 compras semanales consecutivas",
             "umbral": 2, "unidad": "clientes", "comparador": ">=", "fuente": "bitacora/ventas.csv"},
            {"id": "g01b", "metrica": "Margen variable en ventas reales",
             "umbral": 55, "unidad": "%", "comparador": ">=", "fuente": "bitacora/produccion.csv + precios cobrados"},
        ],
        "decision": "Go / iterar 2 semanas más / abortar con pérdida acotada",
        "aviso": "Este gate no tiene holgura: los primeros pedidos caen en S4 y quedan S4, S5 y S6 "
                 "para un umbral de 3 semanas consecutivas. Decide ANTES de la primera venta si la "
                 "fecha se mueve a S7 cuando la primera entrega cobrada caiga en S5.",
    },
    {
        "id": "G1-2",
        "nombre": "G1→2 · ¿la base aguanta?",
        "cuando": "Cierre de la semana 18",
        "criterios": [
            {"id": "g12a", "metrica": "Clientes fijos", "umbral": 4, "unidad": "clientes",
             "comparador": ">=", "fuente": "bitacora/ventas.csv"},
            {"id": "g12b", "metrica": "Semanas seguidas rechazando pedidos (demanda insatisfecha)",
             "umbral": 2, "unidad": "semanas", "comparador": ">=", "fuente": "bitacora/ventas.csv"},
            {"id": "g12c", "metrica": "Días con automatización v1 estable", "umbral": 30, "unidad": "días",
             "comparador": ">=", "fuente": "Home Assistant"},
            {"id": "g12d", "metrica": "Alarmas críticas por semana", "umbral": 2, "unidad": "alarmas",
             "comparador": "<", "fuente": "Home Assistant"},
            {"id": "g12e", "metrica": "Pérdidas por fallo de riego", "umbral": 0, "unidad": "charolas",
             "comparador": "==", "fuente": "bitacora/produccion.csv"},
        ],
        "decision": "Go. Si falla: NO agregar NFT sobre una base inestable",
        "aviso": "El reloj de 30 días y la fecha del gate no cuadran en el Gantt de la wiki: "
                 "está marcado como pendiente de resolver en «Arranque real».",
    },
    {
        "id": "G2-3",
        "nombre": "G2→3 · ¿el sistema se paga solo?",
        "cuando": "Tres meses consecutivos",
        "criterios": [
            {"id": "g23a", "metrica": "Neto mensual cobrado", "umbral": 12000, "unidad": "MXN/mes",
             "comparador": ">=", "fuente": "Contabilidad (cobrado, no facturado)"},
            {"id": "g23b", "metrica": "Meses consecutivos cumpliendo el neto", "umbral": 3, "unidad": "meses",
             "comparador": ">=", "fuente": "Contabilidad"},
            {"id": "g23c", "metrica": "Horas del fundador por semana", "umbral": 9, "unidad": "h/semana",
             "comparador": "<=", "fuente": "bitacora/timesheet.csv (V9, 4 semanas)"},
        ],
        "decision": "Go a Fase 3. Si falla: atacar el rubro más caro en tiempo antes de escalar",
    },
]

VALIDACIONES = [
    ("V1", "Germinación del lote", 0, "≥80 % en 50 semillas entre toalla. NO se siembra nada que no haya pasado V1"),
    ("V2", "Rendimiento por charola", 0, "Pesar cada charola completa, sin sustrato ni cáscaras. Tres pesos, no un promedio"),
    ("V3", "Dry-run HIL", 1, "El lazo de riego corre en la mesa antes de tocar el patio"),
    ("V4", "Smoke test comercial", 0, "El embudo de 15 restaurantes, medido cada semana"),
    ("V5", "Prueba de ausencia", 1, "El sistema sobrevive un fin de semana sin nadie"),
    ("V6", "Experimento A/B", 0, "Girasol CEDA contra girasol específico, 3 charolas gemelas de cada uno"),
    ("V7", "Agua", 1, "EC y pH de la toma, 3 mediciones en días distintos"),
    ("V8", "Sanitaria", 1, "Protocolo de sanitización verificado"),
    ("V9", "Timesheet", 2, "4 semanas midiendo horas reales. Es lo que decide el gate G2→3"),
    ("V10", "Mock recall", 2, "Simulacro: de un clamshell al lote y a todos sus clientes en menos de 4 h"),
    ("V11", "Simulacro de apagón", 2, "Corte de CFE real: la bomba del NFT no se detiene"),
]

# Parametros economicos editables. Salen de los documentos citados.
PARAMETROS = [
    {"id": "precio_charola_viva", "nombre": "Precio de charola viva", "valor": 105, "unidad": "MXN",
     "fuente": "Mercado real: $90–120 (docs/guias/hoja-de-precios.md)"},
    {"id": "precio_clamshell", "nombre": "Precio de clamshell 100 g", "valor": 70, "unidad": "MXN",
     "fuente": "Mercado real: $50–90"},
    {"id": "costo_variable_charola", "nombre": "Costo variable por charola de girasol", "valor": 9,
     "unidad": "MXN", "fuente": "Semilla CEDA + coco + agua + desinfección + etiqueta"},
    {"id": "rendimiento_girasol", "nombre": "Rendimiento por charola de girasol", "valor": 400,
     "unidad": "g", "fuente": "ESTIMADO, no medido. Es lo que V2 tiene que confirmar"},
    {"id": "merma_objetivo", "nombre": "Merma objetivo", "valor": 10, "unidad": "%",
     "fuente": "KPI: meta ≤10 %, umbral rojo >20 %"},
    {"id": "sell_through_objetivo", "nombre": "Sell-through objetivo", "valor": 90, "unidad": "%",
     "fuente": "KPI: meta ≥90 %, umbral rojo <75 % dos semanas seguidas"},
    {"id": "horas_semana_objetivo", "nombre": "Horas por semana objetivo", "valor": 9, "unidad": "h",
     "fuente": "Umbral del gate G2→3"},
]


def main() -> int:
    with open(RAIZ / "bom" / "partidas.csv", encoding="utf-8") as f:
        partidas = list(csv.DictReader(f))
    with open(RAIZ / "bom" / "opciones.csv", encoding="utf-8") as f:
        opciones = list(csv.DictReader(f))

    por_partida: dict[str, list[dict]] = {}
    for o in opciones:
        por_partida.setdefault(o["partida_id"], []).append(o)

    compras = []
    for p in partidas:
        opts = [o for o in por_partida.get(p["partida_id"], []) if o["recomendacion"] != "descartada"]
        fisicas = [o for o in opts if o["tienda_fisica"] == "si"]
        compras.append({
            "id": p["partida_id"],
            "fase": int(p["fase"]),
            "bloque": p["bloque"],
            "categoria": p["categoria"],
            "nombre": p["partida"],
            "cantidad": num(p["cantidad"]),
            "unidad": p["unidad"],
            "precio": num(p["precio_unit_mxn"]),
            "subtotal": num(p["subtotal_mxn"]),
            "cuenta": p["cuenta_en_total"] == "si",
            "motivo": p["motivo_si_no_cuenta"],
            "temporada": p["temporada"],
            "notas": p["notas"],
            "presencial": bool(fisicas),
            "donde": fisicas[0]["sucursal_o_zona"] if fisicas else (opts[0]["proveedor"] if opts else ""),
            "opciones": [
                {"proveedor": o["proveedor"], "producto": o["producto"],
                 "precio": num(o["precio_unit_mxn"]), "fisica": o["tienda_fisica"] == "si",
                 "zona": o["sucursal_o_zona"], "enlace": o["enlace"],
                 "recomendacion": o["recomendacion"]}
                for o in opts
            ],
        })

    totales = {}
    for c in compras:
        if c["cuenta"]:
            totales[str(c["fase"])] = totales.get(str(c["fase"]), 0) + c["subtotal"]

    datos = {
        "generado_por": "tools/gen_seguimiento.py",
        "compras": compras,
        "totales_plan": totales,
        "gates": GATES,
        "validaciones": [
            {"id": v, "nombre": n, "fase": f, "nota": d} for v, n, f, d in VALIDACIONES
        ],
        "parametros": PARAMETROS,
    }

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito {SALIDA.relative_to(RAIZ)}: {len(compras)} partidas, "
          f"{len(GATES)} gates, {len(VALIDACIONES)} validaciones, {len(PARAMETROS)} parámetros")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
