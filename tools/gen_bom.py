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
SALIDA_ONLINE = RAIZ / "docs" / "referencia" / "compra-en-linea.md"
# Vistas por fase. Existian antes como fuente de verdad y estan enlazadas desde ~50
# paginas de la wiki; ahora se DERIVAN del maestro para que no puedan contradecirlo.
VISTAS = {f: RAIZ / "bom" / f"fase{f}.csv" for f in ("0", "1", "2")}
ENVIOS = RAIZ / "bom" / "envios.csv"

MOTIVOS = {"", "informativo", "condicional", "etapa2", "ya_comprado_en_fase_anterior", "recurrente"}
RECOMENDACIONES = {"default", "alternativa", "alternativa_austera", "alternativa_etapa2", "descartada"}

NOMBRE_FASE = {
    "0": "Fase 0 · Validación comercial",
    "1": "Fase 1 · Túnel y automatización v1",
    "2": "Fase 2 · NFT y automatización v2",
}


def cargar() -> tuple[list[dict], list[dict], list[dict]]:
    with open(PARTIDAS, encoding="utf-8") as f:
        partidas = list(csv.DictReader(f))
    with open(OPCIONES, encoding="utf-8") as f:
        opciones = list(csv.DictReader(f))
    with open(ENVIOS, encoding="utf-8") as f:
        envios = list(csv.DictReader(f))
    return partidas, opciones, envios


def num(s: str) -> float:
    return float(s) if s not in ("", None) else 0.0


def validar(partidas: list[dict], opciones: list[dict], envios: list[dict]) -> list[str]:
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

    # Escenario en linea: cada partida apunta a su opcion de compra por internet, o
    # a PRESENCIAL cuando sencillamente no viaja por paqueteria.
    bloques = {b["bloque_id"] for b in envios}
    for o in opciones:
        if o["bloque_envio"] and o["bloque_envio"] not in bloques:
            errores.append(f"{o['opcion_id']}: bloque_envio {o['bloque_envio']!r} no existe en envios.csv")
        if o["tienda_fisica"] == "no" and not o["bloque_envio"]:
            errores.append(f"{o['opcion_id']}: es opcion en linea y no dice por que bloque de envio llega")

    for p in partidas:
        d = p["opcion_default_online"]
        if d in ("", "PRESENCIAL"):
            continue
        if d not in conjunto_oids:
            errores.append(f"{p['partida_id']}: opcion_default_online {d} no existe en opciones.csv")

    return errores


def total_online(partidas: list[dict], opciones: list[dict], envios: list[dict]) -> dict:
    """Cuanto cuesta comprar el BOM por internet, envios incluidos.

    El envio no se reparte por partida: se paga por BLOQUE. Ese es justo el punto.
    Mercado Libre Full junta productos de vendedores distintos en un solo paquete,
    y una tienda propia manda todo su pedido en un solo flete. Por eso el calculo
    agrupa primero y cobra el envio una vez por grupo, no una vez por cosa.
    """
    por_id = {o["opcion_id"]: o for o in opciones}
    reglas = {b["bloque_id"]: b for b in envios}

    grupos: dict[str, dict] = {}
    presencial_forzoso: list[dict] = []
    sin_dato: list[dict] = []

    for p in partidas:
        if p["cuenta_en_total"] != "si":
            continue
        d = p["opcion_default_online"]
        if d == "PRESENCIAL":
            presencial_forzoso.append(p)
            continue
        o = por_id.get(d)
        if not o:
            sin_dato.append(p)
            continue
        b = o["bloque_envio"] or "presencial"
        if b == "presencial":
            presencial_forzoso.append(p)
            continue
        g = grupos.setdefault(b, {"bloque": reglas.get(b, {}), "partidas": [], "productos": 0.0})
        g["partidas"].append({"partida": p, "opcion": o})
        g["productos"] += num(p["cantidad"]) * num(o["precio_unit_mxn"])

    total_prod = 0.0
    total_envio = 0.0
    for b, g in grupos.items():
        r = g["bloque"]
        umbral = num(r.get("umbral_envio_gratis_mxn", ""))
        base = num(r.get("envio_mxn", ""))
        # Un umbral solo aplica si existe: Hydro Environment no tiene, y cobrar $0
        # ahi seria mentir sobre el costo real de comprar por internet.
        g["envio"] = 0.0 if (umbral and g["productos"] >= umbral) else base
        g["envio_gratis_por_umbral"] = bool(umbral and g["productos"] >= umbral)
        total_prod += g["productos"]
        total_envio += g["envio"]

    # Lo que no viaja se sigue pagando: se compra en persona, al precio presencial.
    prod_presencial = sum(num(p["subtotal_mxn"]) for p in presencial_forzoso)
    prod_sin_dato = sum(num(p["subtotal_mxn"]) for p in sin_dato)

    return {
        "grupos": grupos,
        # Las dos razones para no comprar en linea se tratan igual porque para el
        # bolsillo lo son: hay que ir por ellas. Una es "no viaja", la otra es
        # "no encontramos donde comprarlo por internet".
        "presencial_forzoso": presencial_forzoso + sin_dato,
        "solo_no_viaja": presencial_forzoso,
        "sin_dato": sin_dato,
        "productos_en_linea": total_prod,
        "envio": total_envio,
        "productos_presencial": prod_presencial + prod_sin_dato,
        "total": total_prod + total_envio + prod_presencial + prod_sin_dato,
        "pedidos": len(grupos),
    }


def totales(partidas: list[dict]) -> dict[str, float]:
    t: dict[str, float] = {}
    for p in partidas:
        if p["cuenta_en_total"] == "si":
            t[p["fase"]] = t.get(p["fase"], 0.0) + num(p["subtotal_mxn"])
    return t


def total_austero(partidas: list[dict], opciones: list[dict]) -> dict[str, float]:
    """Total por fase cambiando cada partida a su opcion austera, donde exista.

    Existia como frase suelta en las notas del CSV viejo ("version austera ~$6,700")
    y nadie la recalculaba: por eso decia cosas imposibles, como que comprar 250 g
    de rabano en vez de 500 sale mas barato cuando el escalon de precio lo encarece.
    Aqui se deriva, asi que no puede desfasarse.
    """
    austeras = {
        o["partida_id"]: num(o["precio_unit_mxn"])
        for o in opciones
        if o["recomendacion"] == "alternativa_austera" and num(o["precio_unit_mxn"]) > 0
    }
    t: dict[str, float] = {}
    for p in partidas:
        if p["cuenta_en_total"] != "si":
            continue
        pu = austeras.get(p["partida_id"], num(p["precio_unit_mxn"]))
        t[p["fase"]] = t.get(p["fase"], 0.0) + num(p["cantidad"]) * pu
    return t


def mxn(v: float) -> str:
    return f"${v:,.0f}"


def generar_markdown(partidas: list[dict], opciones: list[dict], envios: list[dict]) -> str:
    por_partida: dict[str, list[dict]] = {}
    for o in opciones:
        por_partida.setdefault(o["partida_id"], []).append(o)

    t = totales(partidas)
    ta = total_austero(partidas, opciones)
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
    A("| Fase | Inversión que sí se desembolsa | Versión austera |")
    A("|---|---:|---:|")
    for f in sorted(t):
        A(f"| {NOMBRE_FASE[f]} | {mxn(t[f])} | {mxn(ta[f])} |")
    A(f"| **Acumulado Fases 0–2** | **{mxn(acumulado)}** | **{mxn(sum(ta.values()))}** |")
    A("")
    A("La columna austera cambia cada partida a la opción marcada como")
    A("`alternativa_austera` en `opciones.csv` (rack Adir en vez de Husky, contacto GFCI en vez")
    A("de breaker, batería AGM en vez de LiFePO4, plástico de invernaderosMX). **La calcula el")
    A("script**, así que no puede desfasarse como la frase suelta que traía el CSV viejo, que")
    A("afirmaba que comprar 250 g de rábano salía más barato que 500 g cuando el escalón de")
    A("precio lo encarece $200.")
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


def generar_online_md(partidas, opciones, envios) -> str:
    on = total_online(partidas, opciones, envios)
    t = totales(partidas)
    presencial = sum(t.values())
    reglas = {b["bloque_id"]: b for b in envios}
    por_id = {o["opcion_id"]: o for o in opciones}

    L: list[str] = []
    A = L.append
    A("# Comprar en línea: en cuántos pedidos cabe y cuánto es de envío")
    A("")
    A("La duda que da origen a esta página es concreta: *si compro en muchas páginas voy a pagar")
    A("muchos costos de envío*. La respuesta corta es que **sí, si compras mal, y no, si agrupas**.")
    A("Y hay una segunda respuesta que importa más:")
    A("")
    A("!!! danger \"La mitad del proyecto hay que ir a buscarla, compres donde compres\"")
    A(f"    **{len(on['presencial_forzoso'])} partidas, {mxn(on['productos_presencial'])}"
      f" — el {round(100 * on['productos_presencial'] / on['total'])} % del dinero** — no se")
    A("    resuelven por internet, por dos razones distintas:")
    A("")
    A(f"    - **{len(on['solo_no_viaja'])} no viajan por paquetería.** Exceden el techo físico de")
    A("      todas las paqueterías de México: ningún lado puede pasar de 150 cm y el tope es 70 kg")
    A("      entre peso real y volumétrico. El PTR y el PVC vienen en tramos de 6 m, el rack mide")
    A("      183 cm de alto y el tinaco de 750 L pesa 256 kg volumétricos aunque esté vacío. A eso")
    A("      se suman los servicios (herrero, electricista) y lo restringido por ser oxidante.")
    A(f"    - **{len(on['sin_dato'])} no se encontraron a la venta en línea** en esta investigación.")
    A("      Puede que existan y no aparecieran: son las que conviene volver a buscar tú.")
    A("")
    A("    Así que la pregunta no es *presencial o en línea*, sino **qué parte conviene de cada forma**.")
    A("")
    A("## Los dos escenarios, lado a lado")
    A("")
    A("| | Comprando en persona | Comprando en línea |")
    A("|---|---:|---:|")
    A(f"| Producto | {mxn(presencial)} | {mxn(on['productos_en_linea'] + on['productos_presencial'])} |")
    A(f"| Envíos | $0 | {mxn(on['envio'])} |")
    A(f"| **Total** | **{mxn(presencial)}** | **{mxn(on['total'])}** |")
    A(f"| Diferencia | — | **{'+' if on['total'] >= presencial else ''}{mxn(on['total'] - presencial)}** |")
    A(f"| Pedidos o salidas | varias rutas en auto | {on['pedidos']} pedidos + lo que no viaja |")
    A("")
    A("El envío consolidado **no es lo caro**. Lo que mueve la aguja son los productos que en línea")
    A("solo existen en una versión distinta: el refrigerador nuevo en vez de usado, el tinaco de otra")
    A("marca, el kit de captación en vez del tlaloque casero de tlapalería. Cada uno de esos está")
    A("anotado en su fila del BOM.")
    A("")
    A("## Cómo se consolida de verdad: Mercado Libre Full")
    A("")
    A("!!! tip \"El dato que cambia la cuenta\"")
    A("    En Mercado Libre, **los productos Full de vendedores distintos salen en UN SOLO paquete**.")
    A("    Todos están en la misma bodega de Mercado Libre, así que 8 productos de 5 vendedores")
    A("    diferentes llegan juntos y el envío es gratis si el carrito suma $299.")
    A("")
    A("    **Sin Full no hay consolidación entre vendedores**: se paga un envío por cada vendedor.")
    A("    Por eso conviene filtrar siempre por Full, aunque el producto cueste 5–10 % más: el")
    A("    sobreprecio casi siempre es menor que el envío que te ahorras.")
    A("")
    A("    No contrates Meli+ ni Prime para esto. Bajan el umbral a $149, pero los carritos de este")
    A("    BOM rebasan $299 por mucho: pagarías una suscripción por un beneficio que ya tienes.")
    A("")
    A("## Los pedidos, uno por uno")
    A("")

    orden = sorted(on["grupos"].items(), key=lambda x: -x[1]["productos"])
    for i, (b, g) in enumerate(orden, 1):
        r = reglas.get(b, {})
        A(f"### Pedido {i} · {r.get('nombre', b)}")
        A("")
        envio_txt = ("**envío $0**" + (" (el carrito pasa el umbral de $"
                     + r.get("umbral_envio_gratis_mxn", "") + ")" if g["envio_gratis_por_umbral"] else "")
                     if g["envio"] == 0 else f"**envío {mxn(g['envio'])}**"
                     + (" *(estimado, se ve en el carrito)*" if r.get("estado") != "verificado" else ""))
        A(f"{len(g['partidas'])} partidas · producto **{mxn(g['productos'])}** · {envio_txt}")
        A("")
        if r.get("nota"):
            A(f"!!! note \"{r.get('nombre', b)}\"")
            A(f"    {r['nota']}")
            A("")
        A("| Partida | Cant. | P. unit. | Subtotal | Producto en línea |")
        A("|---|---:|---:|---:|---|")
        for it in sorted(g["partidas"], key=lambda x: -num(x["partida"]["cantidad"]) * num(x["opcion"]["precio_unit_mxn"])):
            p, o = it["partida"], it["opcion"]
            sub = num(p["cantidad"]) * num(o["precio_unit_mxn"])
            prod = o["producto"][:70] + ("…" if len(o["producto"]) > 70 else "")
            enl = f"[{esc_md(prod)}]({o['enlace']})" if o["enlace"].startswith("http") else esc_md(prod)
            A(f"| {esc_md(p['partida'])} | {num(p['cantidad']):g} {p['unidad']} | "
              f"{mxn(num(o['precio_unit_mxn']))} | {mxn(sub)} | {enl} |")
        A("")

    A("## Lo que hay que comprar en persona de todos modos")
    A("")
    A(f"{len(on['presencial_forzoso'])} partidas, {mxn(on['productos_presencial'])}. La ruta en auto")
    A("desde Coyoacán está en [Proveedores presenciales](proveedores-presenciales.md).")
    A("")
    A("| Partida | Subtotal | Por qué no viaja |")
    A("|---|---:|---|")
    for p in sorted(on["presencial_forzoso"], key=lambda x: -num(x["subtotal_mxn"])):
        o = por_id.get(p["opcion_default"], {})
        motivo = o.get("notas", "").split(" · ")[0][:150] if o else ""
        A(f"| {esc_md(p['partida'])} | {mxn(num(p['subtotal_mxn']))} | {esc_md(motivo)} |")
    A("")
    A("## La recomendación")
    A("")
    A("**Mixto, y el reparto no es opinión: lo dicta la paquetería.**")
    A("")
    A("1. **Electrónica → recoger en UNIT Copilco**, Av. Copilco 357, Coyoacán, a 3 km. Son 12")
    A("   partidas y la recolección es gratis; enviarlas cuesta $59–79 y va limitada a 5 kg.")
    A("   Es el único bloque que conviene recoger aunque estés comprando todo lo demás por internet.")
    A("2. **Lo chico y no peligroso → un carrito de Mercado Libre Full o de Amazon.** Un solo envío,")
    A("   gratis pasando $299.")
    A("3. **Semilla, sustrato y nutriente → un solo pedido a Hydro Environment**, y ojo con el peso:")
    A("   pasando 70 kg se va por fletera y se encarece. Conviene partirlo en dos.")
    A("4. **Estructura, tinaco, racks, refrigerador → presencial sin discusión.** No hay alternativa.")
    A("")
    A("<!-- Generado por tools/gen_bom.py. No editar a mano: los cambios van en los CSV. -->")
    return "\n".join(L) + "\n"


def esc_md(s: str) -> str:
    return str(s).replace("|", "·")


def main() -> int:
    solo_check = "--check" in sys.argv
    partidas, opciones, envios = cargar()

    errores = validar(partidas, opciones, envios)
    if errores:
        print(f"BOM inválido: {len(errores)} error(es)\n", file=sys.stderr)
        for e in errores:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    t = totales(partidas)
    ta = total_austero(partidas, opciones)
    on = total_online(partidas, opciones, envios)
    print(f"BOM válido: {len(partidas)} partidas, {len(opciones)} opciones, {len(envios)} bloques de envío")
    for f in sorted(t):
        print(f"  Fase {f}: {mxn(t[f]):>10}   austero {mxn(ta[f]):>10}")
    print(f"  Acumulado: {mxn(sum(t.values())):>8}   austero {mxn(sum(ta.values())):>10}")
    print()
    print(f"  Comprando en línea: {on['pedidos']} pedidos · producto {mxn(on['productos_en_linea'])} "
          f"+ envío {mxn(on['envio'])} + {mxn(on['productos_presencial'])} que no viaja "
          f"= {mxn(on['total'])}")
    for b, g in sorted(on["grupos"].items(), key=lambda x: -x[1]["productos"]):
        libre = " (envío gratis por umbral)" if g["envio_gratis_por_umbral"] else ""
        print(f"    {b:14} {len(g['partidas']):3} partidas  {mxn(g['productos']):>10}  "
              f"envío {mxn(g['envio']):>7}{libre}")
    print(f"    {'no viaja':14} {len(on['presencial_forzoso']):3} partidas  "
          f"{mxn(on['productos_presencial']):>10}  presencial o fletera")

    if solo_check:
        return 0

    SALIDA.write_text(generar_markdown(partidas, opciones, envios), encoding="utf-8")
    escribir_vistas(partidas, opciones)
    SALIDA_ONLINE.write_text(generar_online_md(partidas, opciones, envios), encoding="utf-8")
    print(f"\nRegenerado {SALIDA.relative_to(RAIZ)} y {SALIDA_ONLINE.relative_to(RAIZ)}")
    print("Regeneradas las vistas por fase: " + ", ".join(
        str(v.relative_to(RAIZ)) for v in VISTAS.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
