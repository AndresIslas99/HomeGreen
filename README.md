# HomeGreen — Huerto comercial automatizado en CDMX

**Guía-brújula, nivel wiki, para construir y operar un huerto comercial de microgreens y
hierbas NFT en un patio de 80 m² en la Ciudad de México**, automatizado con ESP32 + ESPHome +
Home Assistant, por fases y financiado con ventas. Todo lo que hay aquí es accionable: qué
comprar (con enlace y precio verificado), cómo instalarlo (con diagramas eléctricos,
hidráulicos y CAD), cómo operarlo (guías paso a paso), cómo validar cada avance (métodos
V1–V11 y gates), y el firmware listo para flashear.

> **Sitio web de la wiki:** https://andresislas99.github.io/HomeGreen/ — se publica solo desde
> `main` con GitHub Actions ([`.github/workflows/docs.yml`](.github/workflows/docs.yml)).
> La primera vez: *Settings → Pages → Source: GitHub Actions*. Para verla en local:
> `pip install mkdocs-material mkdocs-glightbox && mkdocs serve`.

## Empieza aquí (en este orden)

1. **[Antes de gastar un peso](docs/empieza-aqui/antes-de-gastar-un-peso.md)** — la semana 0:
   escritura/condominio, contador (¿eres socio de alguna empresa?), consumo eléctrico, tandeo y
   agua de tu llave, aviso de huerto, curso gratis. Cuesta $0–740 y evita los errores caros.
2. **[Cómo usar esta guía](docs/empieza-aqui/como-usar-esta-guia.md)** — convenciones, cómo
   marcar tu avance, cómo funcionan los gates.
3. **[Línea de tiempo](docs/empieza-aqui/linea-de-tiempo.md)** — 40 semanas con hitos, gates y
   calendario de riesgos climáticos.
4. **[Fase 0 · Validación comercial](docs/fases/fase-0/index.md)** — rack, 20 charolas, dos
   clientes recurrentes en 6 semanas. Si no se logra, perdiste ~$6k y comes microgreens.

## Mapa del proyecto

| Fase | Qué | Cuándo | Inversión (MXN) | Gate para pasar |
|---|---|---|---|---|
| [0 · Validación comercial](docs/fases/fase-0/index.md) | Rack bajo techo, microgreens, vender a chefs | Semanas 1–6 | $8,814 | ≥2 clientes con 3 compras semanales seguidas, margen ≥55 % |
| [1 · Túnel + automatización v1](docs/fases/fase-1/index.md) | Túnel PTR 3×6 m, tinaco + captación pluvial, nodo ESP32 de riego/ambiente | Meses 2–4 | $41,634 | 4–5 clientes fijos, demanda insatisfecha, v1 estable 30 días |
| [2 · NFT + automatización v2](docs/fases/fase-2/index.md) | Túnel 5×6 m, 8 líneas NFT, pH/EC, respaldo DC-first, cadena de frío | Meses 5–9 | $27,251 | Neto ≥$12k/mes × 3 meses con ≤9 h/semana medidas |
| [3 · Consolidación](docs/fases/fase-3/index.md) | Camas elevadas, gantry/visión, testbed agtech | Mes 10+ | discrecional | — |

> **Los montos salen de [`bom/partidas.csv`](bom/partidas.csv)** y los calcula
> [`tools/gen_bom.py`](tools/gen_bom.py), que falla si alguna fila no multiplica. El acumulado de
> las tres fases es **$77,699**, no los ~$86,500 que se publicaban antes: la diferencia es que el
> total viejo cobraba dos veces la partida de seguridad eléctrica y el no-break, y sumaba
> alternativas entre las que hay que elegir una. No se recortó nada del alcance; ver
> [BOM por fase](docs/referencia/bom.md).
>
> La Fase 1 sube y la Fase 2 baja porque el GFCI, la tierra física y el electricista ($4,559)
> estaban presupuestados en las dos, y el proyecto los exige en la S13 de la Fase 1.

## Qué contiene la wiki

| Sección | Para qué |
|---|---|
| [Fases](docs/fases/fase-0/index.md) | Por cada fase: compras exactas, montaje, operación, ventas y gate — con "cómo se verá" (planta + render 3D) |
| [Guías](docs/guias/sembrar-una-charola.md) | Una tarea = una página: sembrar, sanitizar semilla, armar línea NFT, calibrar sondas, instalar GFCI y tierra, flashear ESPHome, visitar a un chef, facturar, cobrar… |
| [Diseño](docs/diseno/index.md) | Arquitectura del sistema: [eléctrico](docs/diseno/electrico.md) (esquemas + pines), [hidráulico](docs/diseno/hidraulico.md) (P&ID), [control](docs/diseno/control.md) (lazos e histéresis), [datos](docs/diseno/datos.md), [layout del patio](docs/diseno/layout-patio.md), [estructura del túnel](docs/diseno/estructura-tunel.md) (CAD) |
| [Validación](docs/validacion/index.md) | Lazos L0–L4, métodos V1–V11 con checklists imprimibles, [KPIs](docs/validacion/kpis.md) y [gates](docs/validacion/gates.md) |
| [Software](docs/software/index.md) | [Firmware ESPHome](docs/software/firmware.md), [Home Assistant](docs/software/home-assistant.md) (automatizaciones y dashboard), [herramientas CLI](docs/software/herramientas-cli.md) |
| [Aprendizaje](docs/aprendizaje/videos.md) | Videos verificados (incrustados), libros y cursos por fase |
| [Referencia](docs/referencia/bom.md) | BOM por fase, normativa, clima, glosario, FAQ, [verificación de enlaces](docs/referencia/enlaces.md), los 9 documentos base y los 17 informes de investigación |

## Archivos que no son documentación

```
firmware/esphome/        nodo-riego-v1.yaml · nodo-ambiente.yaml · nodo-nft-v2.yaml (listos para ESPHome)
firmware/homeassistant/  automations.yaml · dashboard-huerto.yaml · configuration-snippets.yaml
hardware/electrico/      scripts schemdraw que generan los esquemas eléctricos (SVG)
hardware/cad/            modelos OpenSCAD paramétricos (túnel, rack, línea NFT, patio) + renders
hardware/hidraulico/     generador de diagramas P&ID
bom/                     listas de materiales por fase (CSV con enlace y estado del precio)
bitacora/                plantillas CSV (producción, ventas, cobranza, costos, timesheet) + datos de ejemplo
tools/                   check_links.py · kpis.py · informe_semanal.py · gate_audit.py (Python 3.11, sin dependencias)
.github/workflows/       docs.yml (publica la wiki) · links.yml (verifica enlaces cada lunes)
docs/assets/diagramas/   SVG eléctricos, hidráulicos, plantas, animaciones; PNG de CAD
```

## Los 6 números que cambiaron el plan original

1. La bomba periférica de 0.5 HP consumía ~324 kWh/mes → tarifa DAC (~$2,600/mes). Se rediseñó a
   **bomba 12 V DC colgada de una batería LiFePO4** (DC-first): ~32 kWh/mes y un apagón no mata el NFT.
2. **PVC sanitario** 4" ($415/tramo), no cédula 40 ($1,401): el NFT corre sin presión.
3. Precios de venta corregidos con mercado real: **charola viva $90–120**, clamshell $50–90/100 g.
4. **El chícharo con semilla a $340/kg pierde dinero** (275 g/charola): requiere arvejón de CEDA.
5. Racks reales cuestan **$2,000–2,600**; "Hunab" no existe (es Hanlob y no vende antigranizo).
6. **Neto realista $6,500–11,000/mes** con merma, enero −35 %, CAC recurrente y 15 h/semana reales.
7. **UNIT Electronics tiene mostrador en Av. Copilco 357, Coyoacán** — el resto de la wiki lo
   trataba como proveedor solo en línea. Cubre casi todo el BOM de automatización, y ahí el
   sensor SHT41 cuesta **$91** contra los $300 del SHT31 que traía el BOM. La ruta de compra
   presencial completa está en [Proveedores presenciales](docs/referencia/proveedores-presenciales.md).

## Filosofía

1. **Vender antes de construir** — cada fase se financia con la anterior; los gates se escriben
   y se versionan antes de gastar.
2. **Fail-safe físico, no de software** — la bomba NFT cuelga del bus de batería; Home Assistant
   avisa y optimiza, pero el agua nunca depende de que esté vivo.
3. **Todo desde el tinaco, nunca de la toma** — CDMX tiene tandeo.
4. **Operación como sistema de control** — todo se mide y se registra; un lazo agéntico semanal
   (LLM sobre la bitácora y Home Assistant) convierte los datos en decisiones.

## Contribuir

Los precios caducan: si encuentras uno distinto, corrige la fila en `bom/*.csv` o en
`docs/referencia/01-proveedores-cdmx.md` con la fecha y abre un PR.

Dos comprobaciones corren solas y conviene correrlas antes de abrir el PR:

```bash
mkdocs build --strict        # falla con cualquier enlace interno, ancla o imagen rota
python3 tools/check_links.py # verifica los ~680 enlaces externos
```

`--strict` valida las 112 páginas: enlaces relativos, anclas, imágenes y que no haya páginas
fuera del `nav`. `check_links.py` corre cada lunes (workflow `links.yml`) y **solo falla con un
enlace muerto nuevo**: los ya conocidos y anotados viven en
[`tools/enlaces-muertos-conocidos.txt`](tools/enlaces-muertos-conocidos.txt), así un `dead`
nuevo —una partida del BOM que ya no se puede comprar— no se pierde entre el ruido viejo.
