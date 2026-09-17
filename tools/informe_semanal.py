#!/usr/bin/env python3
"""Arma el paquete semanal del lazo agéntico L3 (sin llamar a ninguna API).

Crea ``informes/AAAA-Www/`` con:

* ``produccion.csv`` y ``ventas.csv``: extracto de la semana analizada y las 4 anteriores
  (5 semanas ISO; el contrato pide comparar "la semana vs las 4 anteriores").
* ``ha-*.csv``: copia de los exports de Home Assistant que pases con ``--ha`` (opcional).
* ``kpis.md``: KPIs L2 de esas semanas (``tools/kpis.py``), por variedad y alertas.
* ``prompt.md``: el contrato **exacto** del lazo L3 de
  ``docs/referencia/06-validacion-y-lazos-agenticos.md`` §L3, seguido del contexto, los
  KPIs, los experimentos V6 activos y los CSV en línea, listo para pegar en un LLM
  (Claude vía API, una sesión de Claude Code por cron, o un chat).

El agente responde en ≤ 1 página; el humano aprueba o corrige el plan y lo commitea en
``bitacora/informes/AAAA-Www.md``. El agente nunca ejecuta compras ni cambia setpoints solo.

Uso::

    python3 tools/informe_semanal.py                       # semana ISO de hoy
    python3 tools/informe_semanal.py --semana 2026-W44 \\
        --produccion bitacora/produccion.csv --ventas bitacora/ventas.csv \\
        --ha bitacora/ha/ --experimentos bitacora/validacion/v06-experimentos.csv
    python3 tools/informe_semanal.py --semana auto         # última semana con datos

Solo biblioteca estándar (Python 3.11). Importa ``kpis.py`` del mismo directorio.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kpis as K  # noqa: E402

#: Contrato del lazo L3, copiado sin cambios de 06 §L3. NO editar aquí: si cambia, cambia en la fuente.
CONTRATO_L3 = """Eres el agrónomo/analista de un microhuerto comercial en CDMX. Con los CSV adjuntos:
1. ANOMALÍAS: desviaciones de la semana vs las 4 anteriores (ambiente, consumo de agua,
   dosificación, rendimiento por variedad). Solo las significativas, con evidencia numérica.
2. CAUSA PROBABLE: para cada anomalía, hipótesis rankeadas y qué dato falta para confirmar.
3. EXPERIMENTO: propone máximo UN experimento A/B para la semana entrante (formato V6),
   con métrica, tamaño de muestra (charolas) y criterio de éxito.
4. PLAN: borrador de plan de siembra de la semana (variedades y cantidades) a partir de
   pedidos recurrentes + sell-through, con su razonamiento.
5. RIESGO: la única cosa que más probabilidad tiene de salir mal la próxima semana.
Responde en ≤ 1 página. No inventes datos: si un CSV está vacío o roto, dilo.
"""


def encabezado_csv(ruta: str | Path) -> list[str]:
    p = Path(ruta)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8-sig") as fh:
        return next(csv.reader(fh), [])


def escribir_extracto(ruta_origen: str | Path, filas: list[dict], destino: Path, columnas_default: list[str]) -> int:
    """Escribe ``filas`` (sin las claves internas ``_x``) con el encabezado original del CSV."""
    cols = encabezado_csv(ruta_origen) or columnas_default
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow({k: v for k, v in f.items() if not k.startswith("_")})
    return len(filas)


def resolver_semana(texto: str, prod: list[dict], ven: list[dict]) -> str:
    if texto and texto.lower() != "auto":
        try:
            K.lunes_de(texto)
        except (ValueError, AttributeError):
            raise SystemExit(f"--semana '{texto}' inválida; usa AAAA-Www (p. ej. 2026-W44) o 'auto'")
        return texto.upper()
    if texto and texto.lower() == "auto":
        fechas = [f["_fecha_siembra"] for f in prod] + [f["_fecha_cosecha"] for f in prod] + [v["_fecha"] for v in ven]
        fechas = [f for f in fechas if f]
        if fechas:
            return K.semana_iso(max(fechas))
    return K.semana_iso(date.today())


def archivos_ha(rutas: list[str] | None, semanas: list[str]) -> list[Path]:
    """Acepta archivos o carpetas; en carpetas prefiere los CSV cuyo nombre contenga una semana del paquete."""
    out: list[Path] = []
    for r in rutas or []:
        p = Path(r)
        if p.is_dir():
            todos = sorted(p.glob("*.csv"))
            filtrados = [f for f in todos if any(s in f.name.upper() for s in semanas)]
            out += filtrados or todos
        elif p.exists():
            out.append(p)
    return out


def bloque_csv(ruta: Path, max_filas: int) -> str:
    lineas = ruta.read_text(encoding="utf-8-sig").splitlines()
    if not lineas or len(lineas) == 1:
        return "_(vacío: solo encabezado o sin contenido)_\n"
    cuerpo = lineas[: max_filas + 1]
    nota = f"\n_(recortado a {max_filas} de {len(lineas) - 1} filas; el archivo completo va adjunto)_" if len(lineas) - 1 > max_filas else ""
    return "```csv\n" + "\n".join(cuerpo) + "\n```" + nota + "\n"


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Arma informes/AAAA-Www/ con extractos de la bitácora, kpis.md y prompt.md del lazo L3 (sin llamar a ninguna API).",
        epilog="Contrato: docs/referencia/06-validacion-y-lazos-agenticos.md §L3.",
    )
    p.add_argument("--produccion", default="bitacora/produccion.csv")
    p.add_argument("--ventas", default="bitacora/ventas.csv")
    p.add_argument("--ha", nargs="*", metavar="CSV|DIR", help="exports de Home Assistant (archivos o carpeta bitacora/ha/)")
    p.add_argument("--experimentos", help="bitacora/validacion/v06-experimentos.csv (se incluye tal cual)")
    p.add_argument("--semana", default="", help="AAAA-Www a analizar; 'auto' = última semana con datos; default: semana de hoy")
    p.add_argument("--semanas-previas", type=int, default=4, help="semanas anteriores a incluir (default 4)")
    p.add_argument("--salida", default="informes", help="carpeta base (default informes/, ignorada por Git)")
    p.add_argument("--costo", action="append", metavar="VARIEDAD=MXN", help="sobrescribe costo variable")
    p.add_argument("--reparto", type=float, default=K.REPARTO_POR_PARADA_MXN)
    p.add_argument("--contar-muestras", action="store_true")
    p.add_argument("--max-filas-inline", type=int, default=400, help="máximo de filas de cada CSV pegadas en prompt.md")
    return p


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    costos, avisos = K.costos_desde_args(args.costo)
    prod_todo, av1 = K.cargar_produccion(args.produccion)
    ven_todo, av2 = K.cargar_ventas(args.ventas)
    avisos += av1 + av2

    semana = resolver_semana(args.semana, prod_todo, ven_todo)
    primera = semana
    for _ in range(args.semanas_previas):
        primera = K.semana_anterior(primera)
    semanas = K.rango_semanas(primera, semana)
    d0 = K.lunes_de(primera)
    d1 = K.lunes_de(semana) + timedelta(days=6)

    prod = [f for f in prod_todo if (f["_fecha_siembra"] and d0 <= f["_fecha_siembra"] <= d1)
            or (f["_fecha_cosecha"] and d0 <= f["_fecha_cosecha"] <= d1)
            or (f["_fecha_siembra"] and f["_fecha_siembra"] < d0 and not f["_cerrada"])]  # en rack desde antes
    ven = [v for v in ven_todo if v["_fecha"] and d0 <= v["_fecha"] <= d1]

    carpeta = Path(args.salida) / semana
    carpeta.mkdir(parents=True, exist_ok=True)
    n_p = escribir_extracto(args.produccion, prod, carpeta / "produccion.csv", K.COLUMNAS_PRODUCCION)
    n_v = escribir_extracto(args.ventas, ven, carpeta / "ventas.csv", K.COLUMNAS_VENTAS)

    copiados: list[Path] = []
    for f in archivos_ha(args.ha, semanas):
        dest = carpeta / f"ha-{f.name}"
        shutil.copyfile(f, dest)
        copiados.append(dest)
    exp_txt = None
    if args.experimentos:
        pe = Path(args.experimentos)
        if pe.exists():
            shutil.copyfile(pe, carpeta / "experimentos.csv")
            exp_txt = bloque_csv(carpeta / "experimentos.csv", args.max_filas_inline)
        else:
            avisos.append(f"{pe}: no existe")

    kp = K.calcular_kpis(prod, ven, costos, args.reparto, args.contar_muestras, semanas)
    avisos += kp["avisos"]
    kpis_md = K.informe_markdown(kp, K.resumen_variedades(prod), costos, args.reparto, avisos,
                                 titulo=f"KPIs L2 — semana {semana} y las {args.semanas_previas} anteriores")
    (carpeta / "kpis.md").write_text(kpis_md, encoding="utf-8")

    # estado de los CSV: decirlo, no inventar
    estado = []
    for nombre, n, total in (("produccion.csv", n_p, len(prod_todo)), ("ventas.csv", n_v, len(ven_todo))):
        if total == 0:
            estado.append(f"- `{nombre}`: **VACÍO** (0 filas en la bitácora). No hay base para anomalías de ese rubro.")
        elif n == 0:
            estado.append(f"- `{nombre}`: {total} filas en total pero **ninguna en {primera}…{semana}**; revisa `--semana`.")
        else:
            estado.append(f"- `{nombre}`: {n} filas de {total} (ventana {d0} → {d1}).")
    if copiados:
        estado.append("- Export de HA: " + ", ".join(f"`{c.name}`" for c in copiados) + ".")
    else:
        estado.append("- Export de HA: **no adjunto** (T, HR, pH, EC, riegos, dosificación, alarmas). Sin él, el punto 1 solo "
                      "puede hablar de rendimiento y ventas; dilo en el informe. [POR VERIFICAR: exportar `recorder` → "
                      "`bitacora/ha/AAAA-Www.csv` cada domingo, software/home-assistant.md]")
    if exp_txt is None:
        estado.append("- Experimentos V6: sin archivo (`--experimentos bitacora/validacion/v06-experimentos.csv`). "
                      "Asume que no hay experimento activo salvo que la bitácora diga lo contrario (observaciones con 'V6').")
    if avisos:
        estado.append("- Avisos de captura: " + " · ".join(avisos))

    partes = [
        f"# Prompt del lazo L3 — semana {semana} ({K.lunes_de(semana)} → {d1})\n\n",
        "Pega este archivo completo en el LLM (o solo el contrato + los CSV adjuntos). El contrato es el de "
        "`docs/referencia/06-validacion-y-lazos-agenticos.md` §L3, sin cambios. El humano aprueba o corrige el plan; "
        "el agente nunca ejecuta compras ni cambia setpoints solo. Guarda la respuesta y tu decisión en "
        f"`bitacora/informes/{semana}.md`.\n\n---\n\n",
        CONTRATO_L3,
        "\n---\n\n## Contexto del paquete\n\n",
        f"- Semana analizada: **{semana}** (lunes {K.lunes_de(semana)} a domingo {d1}). Comparar contra: {', '.join(semanas[:-1])}.\n",
        "\n".join(estado) + "\n",
        "\n## KPIs L2 (tools/kpis.py)\n\n", K.tabla_semanal(kp), "\n### Por variedad\n\n", K.tabla_variedades(K.resumen_variedades(prod)),
        "\n### Alertas L2\n\n" + ("\n".join(f"- {a}" for a in K.alertas(kp)) or "- Ninguna.") + "\n",
        "\n## Experimentos V6\n\n" + (exp_txt or "_Sin registro adjunto._\n"),
        "\n## produccion.csv (extracto)\n\n", bloque_csv(carpeta / "produccion.csv", args.max_filas_inline),
        "\n## ventas.csv (extracto)\n\n", bloque_csv(carpeta / "ventas.csv", args.max_filas_inline),
    ]
    if copiados:
        for c in copiados:
            partes.append(f"\n## {c.name} (export de Home Assistant)\n\n" + bloque_csv(c, args.max_filas_inline))
    else:
        partes.append("\n## Export de Home Assistant\n\n_No adjunto esta semana._\n")
    (carpeta / "prompt.md").write_text("".join(partes), encoding="utf-8")

    print(f"Paquete L3 en {carpeta}/")
    for nombre in ("produccion.csv", "ventas.csv", "kpis.md", "prompt.md"):
        print(f"  {nombre:16s} {(carpeta / nombre).stat().st_size:>7,d} bytes")
    for c in copiados:
        print(f"  {c.name:16s} {c.stat().st_size:>7,d} bytes")
    print(f"Semanas: {', '.join(semanas)} · produccion {n_p} filas · ventas {n_v} filas")
    for e in estado:
        if "VACÍO" in e or "ninguna" in e:
            print("AVISO:", e.lstrip("- "))
    print("Siguiente paso: pega prompt.md en el LLM; guarda la respuesta y tu decisión en "
          f"bitacora/informes/{semana}.md y commitea.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
