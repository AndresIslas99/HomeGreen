# tools/

Seis scripts de Python que convierten la bitácora en decisiones y mantienen el BOM honesto. **Solo biblioteca
estándar de Python 3.11**: sin `pip install`, sin entorno virtual, sin dependencias.

La documentación completa (opciones, convenciones de la bitácora, ejemplos de salida) está
en la wiki: **[Software → Herramientas CLI](../docs/software/herramientas-cli.md)**.

| Script | Lazo | Qué hace |
|---|---|---|
| `kpis.py` | L2 | Sell-through, merma, entregas a tiempo, recompra, margen variable y feedback por semana ISO, con semáforo contra las metas del 06. |
| `informe_semanal.py` | L3 | Arma `informes/AAAA-Www/` con los CSV, los KPIs y el `prompt.md` del contrato agéntico. No llama a ninguna API. |
| `gate_audit.py` | L4 | Evalúa G0-1, G1-2 o G2-3 contra la bitácora e imprime GO/NO-GO con evidencia. Salida 0 = GO, 1 = NO-GO, 2 = error de uso. |
| `check_links.py` | — | Verifica que las URL de `docs/**/*.md` y `README.md` sigan vivas. Salida 1 solo si hay enlaces muertos. |
| `gen_bom.py` | — | Valida `bom/partidas.csv` y `bom/opciones.csv` y regenera `docs/referencia/bom.md` y las tres vistas por fase. **Falla si alguna fila no multiplica**, si una partida no tiene proveedor o si algo sale del total sin decir por qué. |
| `gen_seguimiento.py` | — | Genera `docs/assets/datos/seguimiento.json`, los datos del [tablero de seguimiento](../docs/seguimiento.md), desde el BOM y los umbrales de los gates. |

`informe_semanal.py` y `gate_audit.py` importan `kpis.py`: los tres se mantienen juntos.

**Después de tocar cualquiera de los dos CSV del BOM, corre los dos generadores**, en este
orden. El segundo lee lo que deja el primero:

```bash
python3 tools/gen_bom.py && python3 tools/gen_seguimiento.py
```

`gen_bom.py --check` valida sin escribir: es lo que conviene correr en CI.

## Uso rápido

Desde la raíz del repositorio:

```bash
python3 tools/kpis.py --semanas 4
python3 tools/informe_semanal.py --semana auto
python3 tools/gate_audit.py --gate G0-1 --desde 2026-09-21 --hasta 2026-10-30 --guardar
python3 tools/check_links.py --only-dead
```

Cada script trae `--help` con todas sus opciones.

## Probarlos sin datos propios

`bitacora/ejemplo/` tiene seis semanas de Fase 0 con datos realistas (incluida una charola
enmohecida y una entrega tarde), para ver la salida antes de tener bitácora:

```bash
python3 tools/kpis.py --produccion bitacora/ejemplo/produccion.csv \
                      --ventas bitacora/ejemplo/ventas.csv
python3 tools/gate_audit.py --gate G0-1 \
    --produccion bitacora/ejemplo/produccion.csv \
    --ventas bitacora/ejemplo/ventas.csv
```

## Lo que estos scripts nunca hacen

- **No cambian setpoints ni tocan el firmware.** El agente L3 propone; tú apruebas desde el
  dashboard y commiteas el valor en `firmware/esphome/*.yaml` con su evidencia.
- **No negocian umbrales.** Los de los gates son los de
  `docs/referencia/06-validacion-y-lazos-agenticos.md`; `gate_audit.py` mide, no opina.
- **No inventan datos.** Un CSV faltante o una variedad sin costo se reportan como aviso, no
  se rellenan con un supuesto.
