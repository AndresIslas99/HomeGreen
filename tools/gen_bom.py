#!/usr/bin/env python3
"""Valida bom/partidas.csv y bom/opciones.csv y regenera docs/referencia/bom.md.

Por que existe este script
--------------------------
El BOM viejo eran tres CSV con una fila TOTAL escrita a mano. Eso permitia tres
cosas que costaban dinero de verdad:

  1. Sumar ALTERNATIVAS como si fueran compras. La sonda de pH aparecia dos veces
     (la economica de $329 y el kit DFRobot de $1,250) y el total cobraba las dos,
     aunque la propia pagina de compras dijera "sin DFRobot".
  2. Cobrar DOS VECES entre fases. El no-break y toda la partida de seguridad
     electrica estaban presupuestados en Fase 1 y otra vez en Fase 2: $8,659 de
     riesgo de doble conteo.
  3. Que el total no cuadrara con la suma de sus filas, sin que nada lo detectara.

El esquema nuevo lo hace estructuralmente imposible:

  - Una PARTIDA es una cosa que se compra UNA vez. Vive en partidas.csv con su
    cantidad, su unidad y su subtotal.
  - Las OPCIONES DE PROVEEDOR viven en opciones.csv y NO TIENEN COLUMNA DE SUBTOTAL,
    asi que no pueden inflar nada por construccion. Una partida puede tener las
    opciones que quieras.
  - Solo suman al total las partidas con cuenta_en_total = si. Lo informativo, lo
    condicional, lo de etapa 2 y lo ya comprado en otra fase sigue VISIBLE pero en cero.
  - subtotal_mxn = cantidad x precio_unit_mxn, siempre. Este script falla si no.

Uso:
    python3 tools/gen_bom.py            # valida y regenera docs/referencia/bom.md
    python3 tools/gen_bom.py --check    # solo valida, no escribe (para CI)

Sin dependencias: Python 3.11+ de la biblioteca estandar.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PARTIDAS = RAIZ / "bom" / "partidas.csv"
OPCIONES = RAIZ / "bom" / "opciones.csv"
SALIDA = RAIZ / "docs" / "referencia" / "bom.md"
# Vistas por fase. Existian antes como fuente de verdad y estan enlazadas desde ~50
# paginas de la wiki; ahora se DERIVAN del maestro para que no puedan contradecirlo.
VISTAS = {f: RAIZ / "bom" / f"fase{f}.csv" for f in ("0", "1", "2")}

MOTIVOS = {"", "informativo", "condicional", "etapa2", "ya_comprado_en_fase_anterior", "recurrente"}
RECOMENDACIONES = {"default", "alternativa", "alternativa_austera", "alternativa_etapa2", "descartada"}

NOMBRE_FASE = {
    "0": "Fase 0 · Validación comercial",
    "1": "Fase 1 · Túnel y automatización v1",
    "2": "Fase 2 · NFT y automatización v2",
}


def cargar() -> tuple[list[dict], list[dict]]:
    with open(PARTIDAS, encoding="utf-8") as f:
        partidas = list(csv.DictReader(f))
    with open(OPCIONES, encoding="utf-8") as f:
        opciones = list(csv.DictReader(f))
    return partidas, opciones


def num(s: str) -> float:
    return float(s) if s not in ("", None) else 0.0


def validar(partidas: list[dict], opciones: list[dict]) -> list[str]:
    """Devuelve la lista de errores. Vacia = todo bien."""
    errores: list[str] = []

    if "subtotal_mxn" in (opciones[0].keys() if opciones else {}):
        errores.append(
            "opciones.csv tiene una columna subtotal_mxn. No debe tenerla: es lo que "
            "impide que las alternativas de proveedor inflen el total."
        )

    ids = [p["partida_id"] for p in partidas]
    for pid in {x for x in ids if ids.count(x) > 1}:
        errores.append(f"partida_id repetido: {pid}")

    oids = [o["opcion_id"] for o in opciones]
    for oid in {x for x in oids if oids.count(x) > 1}:
        errores.append(f"opcion_id repetido: {oid}")

    conjunto_ids, conjunto_oids = set(ids), set(oids)

    for p in partidas:
        pid = p["partida_id"]

        # La regla dura: el subtotal es una multiplicacion, no un numero a mano.
        esperado = round(num(p["cantidad"]) * num(p["precio_unit_mxn"]), 2)
        declarado = round(num(p["subtotal_mxn"]), 2)
        if abs(esperado - declarado) > 0.01:
            errores.append(
                f"{pid}: {p['cantidad']} x {p['precio_unit_mxn']} = {esperado:g} "
                f"pero subtotal_mxn dice {declarado:g}"
            )

        if p["cuenta_en_total"] not in ("si", "no"):
            errores.append(f"{pid}: cuenta_en_total debe ser si o no, dice {p['cuenta_en_total']!r}")

        if p["motivo_si_no_cuenta"] not in MOTIVOS:
            errores.append(f"{pid}: motivo_si_no_cuenta desconocido: {p['motivo_si_no_cuenta']!r}")

        # Nada sale del total sin decir por que: es justo lo que se perdia antes.
        if p["cuenta_en_total"] == "no" and not p["motivo_si_no_cuenta"]:
            errores.append(f"{pid}: no suma al total pero no dice por que (motivo_si_no_cuenta vacio)")
        if p["cuenta_en_total"] == "si" and p["motivo_si_no_cuenta"]:
            errores.append(f"{pid}: suma al total pero trae motivo_si_no_cuenta {p['motivo_si_no_cuenta']!r}")

        if p["ya_comprado_en"] and p["motivo_si_no_cuenta"] != "ya_comprado_en_fase_anterior":
            errores.append(f"{pid}: dice ya_comprado_en={p['ya_comprado_en']} pero el motivo no lo refleja")

        if p["opcion_default"] and p["opcion_default"] not in conjunto_oids:
            errores.append(f"{pid}: opcion_default {p['opcion_default']} no existe en opciones.csv")

    for o in opciones:
        if o["partida_id"] not in conjunto_ids:
            errores.append(f"{o['opcion_id']}: apunta a la partida {o['partida_id']}, que no existe")
        if o["recomendacion"] not in RECOMENDACIONES:
            errores.append(f"{o['opcion_id']}: recomendacion desconocida: {o['recomendacion']!r}")
        if o["tienda_fisica"] not in ("si", "no"):
            errores.append(f"{o['opcion_id']}: tienda_fisica debe ser si o no")

    # El precio de la partida tiene que ser el de su opcion por defecto: si no,
    # el total dice una cosa y la tienda a la que vas cobra otra.
    por_id = {o["opcion_id"]: o for o in opciones}
    for p in partidas:
        oid = p["opcion_default"]
        if not oid or oid not in por_id:
            continue
        precio_opcion = num(por_id[oid]["precio_unit_mxn"])
        if precio_opcion == 0:
            continue  # precio por confirmar en piso
        if abs(precio_opcion - num(p["precio_unit_mxn"])) > 0.01:
            errores.append(
                f"{p['partida_id']}: precio_unit_mxn es {p['precio_unit_mxn']} pero su opcion "
                f"por defecto {oid} cuesta {por_id[oid]['precio_unit_mxn']}"
            )

    # Una partida sin ninguna opcion es una partida que no sabes donde comprar.
    # Se exceptuan las filas "sombra": la copia visible, con subtotal en cero, de algo
    # que ya se pago en una fase anterior. Sus opciones viven en la partida original,
    # y su opcion_default apunta ahi a proposito.
    con_opciones = {o["partida_id"] for o in opciones}
    for p in partidas:
        if p["partida_id"] in con_opciones or p["ya_comprado_en"]:
            continue
        errores.append(f"{p['partida_id']}: no tiene ninguna opcion de proveedor en opciones.csv")

    return errores


def totales(partidas: list[dict]) -> dict[str, float]:
    t: dict[str, float] = {}
    for p in partidas:
        if p["cuenta_en_total"] == "si":
            t[p["fase"]] = t.get(p["fase"], 0.0) + num(p["subtotal_mxn"])
    return t


def mxn(v: float) -> str:
    return f"${v:,.0f}"


def generar_markdown(partidas: list[dict], opciones: list[dict]) -> str:
    por_partida: dict[str, list[dict]] = {}
    for o in opciones:
        por_partida.setdefault(o["partida_id"], []).append(o)

    t = totales(partidas)
    acumulado = sum(t.values())

    L: list[str] = []
    A = L.append

    A("# BOM por fase")
    A("")
    A("Lista de materiales del proyecto. **Una fila = una cosa que se compra una vez.**")
    A("Las alternativas de proveedor no viven aquí: viven en")
    A("[`bom/opciones.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/opciones.csv),")
    A("que **no tiene columna de subtotal** y por lo tanto no puede inflar ningún total.")
    A("")
    A("!!! info \"Cómo leer esta página\"")
    A("    - **Las partidas en *cursiva*, con el subtotal entre paréntesis, no suman.**")
    A("      Siguen aquí porque son información útil (un precio de referencia, una compra")
    A("      condicional, algo que ya pagaste en la fase anterior), pero el total de la fase")
    A("      no las incluye. La razón de cada una está en su nota y en la tabla de abajo.")
    A("    - **El subtotal siempre es `cantidad × precio unitario`.**")
    A("      [`tools/gen_bom.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gen_bom.py)")
    A("      falla si alguna fila no multiplica, así que no puede volver a desalinearse.")
    A("    - **El precio es el de la opción marcada como predeterminada.** Cambiar de")
    A("      proveedor es cambiar `opcion_default` y volver a correr el script: el total")
    A("      se recalcula solo.")
    A("    - Para comprar **en persona**, la ruta en auto está en")
    A("      [Proveedores presenciales](proveedores-presenciales.md).")
    A("")
    A("## Resumen")
    A("")
    A("| Fase | Inversión que sí se desembolsa |")
    A("|---|---:|")
    for f in sorted(t):
        A(f"| {NOMBRE_FASE[f]} | {mxn(t[f])} |")
    A(f"| **Acumulado Fases 0–2** | **{mxn(acumulado)}** |")
    A("")

    no_suman = [p for p in partidas if p["cuenta_en_total"] == "no"]
    ahorro = sum(num(p["subtotal_mxn"]) for p in no_suman)
    A("??? warning \"Qué cambió respecto del BOM viejo, y por qué el total bajó\"")
    A("    El BOM anterior publicaba **$86,500** acumulados. Este publica"
      f" **{mxn(acumulado)}**.")
    A("    La diferencia no es que se haya recortado el proyecto: es que el total viejo")
    A(f"    cobraba cosas dos veces o cobraba alternativas entre las que hay que elegir una."
      f" Son {mxn(ahorro)} repartidos en {len(no_suman)} filas que ahora siguen visibles pero en cero:")
    A("")
    A("    | Partida | Importe | Por qué no suma |")
    A("    |---|---:|---|")
    explica = {
        "informativo": "precio de referencia; el propio proyecto dice que no se compra",
        "condicional": "solo si se da el supuesto que la nota describe",
        "etapa2": "compra de una etapa posterior, no de esta fase",
        "ya_comprado_en_fase_anterior": "misma función que una partida ya pagada antes",
        "recurrente": "gasto mensual, no inversión de capital",
    }
    for p in sorted(no_suman, key=lambda x: -num(x["subtotal_mxn"])):
        A(f"    | {p['partida']} | {mxn(num(p['subtotal_mxn']))} | {explica[p['motivo_si_no_cuenta']]} |")
    A("")

    for f in sorted(t):
        filas = [p for p in partidas if p["fase"] == f]
        A(f"## {NOMBRE_FASE[f]}")
        A("")
        A(f"**Total de la fase: {mxn(t[f])}**")
        A("")
        A("| Partida | Cant. | P. unitario | Subtotal | Dónde comprarla | Notas |")
        A("|---|---:|---:|---:|---|---|")
        for p in filas:
            cant = f"{num(p['cantidad']):g} {p['unidad']}"
            pu = mxn(num(p["precio_unit_mxn"]))
            if p["cuenta_en_total"] == "si":
                sub = mxn(num(p["subtotal_mxn"]))
                nombre = p["partida"]
            else:
                sub = f"— *({mxn(num(p['subtotal_mxn']))})*"
                nombre = f"*{p['partida']}*"

            opts = por_partida.get(p["partida_id"], [])
            vivas = [o for o in opts if o["recomendacion"] != "descartada"]
            fisicas = [o for o in vivas if o["tienda_fisica"] == "si"]
            if fisicas:
                donde = fisicas[0]["sucursal_o_zona"].split(",")[0]
                if len(vivas) > 1:
                    donde += f" *(+{len(vivas) - 1} opc.)*"
            elif vivas:
                donde = "**solo en línea**"
                if len(vivas) > 1:
                    donde += f" *(+{len(vivas) - 1} opc.)*"
            else:
                donde = "—"

            nota = p["notas"].replace("|", "·")
            if len(nota) > 150:
                nota = nota[:147] + "…"
            A(f"| {nombre} | {cant} | {pu} | {sub} | {donde} | {nota} |")
        A("")

    A("## Archivos fuente")
    A("")
    A("| Archivo | Qué es |")
    A("|---|---|")
    A("| [`bom/partidas.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/partidas.csv) "
      f"| Las {len(partidas)} partidas. Una fila = una compra. |")
    A("| [`bom/opciones.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/opciones.csv) "
      f"| Las {len(opciones)} opciones de proveedor. Sin subtotal: no puede inflar nada. |")
    A("| [`tools/gen_bom.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gen_bom.py) "
      "| Valida la aritmética y regenera esta página. |")
    A("")
    fis = len({o["partida_id"] for o in opciones if o["tienda_fisica"] == "si"})
    A(f"De las {len(partidas)} partidas, **{fis} tienen al menos una opción con mostrador físico**.")
    A("")
    A("<!-- Generado por tools/gen_bom.py. No editar a mano: los cambios van en los CSV. -->")
    return "\n".join(L) + "\n"


def escribir_vistas(partidas: list[dict], opciones: list[dict]) -> None:
    """Regenera bom/fase0.csv, fase1.csv y fase2.csv como vistas del maestro.

    Se conservan porque media wiki las enlaza. Lo que cambia respecto de los
    originales es que ya no se editan a mano: salen de partidas.csv, traen la
    columna cuenta_en_total y no llevan fila TOTAL escrita a mano.
    """
    por_partida: dict[str, list[dict]] = {}
    for o in opciones:
        por_partida.setdefault(o["partida_id"], []).append(o)

    cols = [
        "partida_id", "bloque", "categoria", "partida", "cantidad", "unidad",
        "precio_unit_mxn", "subtotal_mxn", "cuenta_en_total", "motivo_si_no_cuenta",
        "proveedor_default", "tienda_fisica", "sucursal_o_zona", "enlace",
        "opciones_de_proveedor", "temporada", "notas",
    ]
    for fase, destino in VISTAS.items():
        filas = []
        for p in (x for x in partidas if x["fase"] == fase):
            opts = por_partida.get(p["partida_id"], [])
            default = next((o for o in opts if o["opcion_id"] == p["opcion_default"]), None)
            vivas = [o for o in opts if o["recomendacion"] != "descartada"]
            filas.append({
                "partida_id": p["partida_id"],
                "bloque": p["bloque"],
                "categoria": p["categoria"],
                "partida": p["partida"],
                "cantidad": p["cantidad"],
                "unidad": p["unidad"],
                "precio_unit_mxn": p["precio_unit_mxn"],
                "subtotal_mxn": p["subtotal_mxn"] if p["cuenta_en_total"] == "si" else "0",
                "cuenta_en_total": p["cuenta_en_total"],
                "motivo_si_no_cuenta": p["motivo_si_no_cuenta"],
                "proveedor_default": default["proveedor"] if default else "",
                "tienda_fisica": default["tienda_fisica"] if default else "",
                "sucursal_o_zona": default["sucursal_o_zona"] if default else "",
                "enlace": default["enlace"] if default else "",
                "opciones_de_proveedor": len(vivas),
                "temporada": p["temporada"],
                "notas": p["notas"],
            })
        with open(destino, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(filas)


def main() -> int:
    solo_check = "--check" in sys.argv
    partidas, opciones = cargar()

    errores = validar(partidas, opciones)
    if errores:
        print(f"BOM inválido: {len(errores)} error(es)\n", file=sys.stderr)
        for e in errores:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    t = totales(partidas)
    print(f"BOM válido: {len(partidas)} partidas, {len(opciones)} opciones de proveedor")
    for f in sorted(t):
        print(f"  Fase {f}: {mxn(t[f])}")
    print(f"  Acumulado: {mxn(sum(t.values()))}")

    if solo_check:
        return 0

    SALIDA.write_text(generar_markdown(partidas, opciones), encoding="utf-8")
    escribir_vistas(partidas, opciones)
    print(f"\nRegenerado {SALIDA.relative_to(RAIZ)}")
    print("Regeneradas las vistas por fase: " + ", ".join(
        str(v.relative_to(RAIZ)) for v in VISTAS.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
