# HomeGreen — Huerto comercial automatizado en CDMX

Plan maduro y ejecutable para un huerto comercial de **microgreens + hierbas NFT** en un
patio de 80 m² en la Ciudad de México, con automatización DIY (ESP32 + ESPHome +
Home Assistant), por fases y financiado con ventas ("vender antes de construir").

Este repositorio es la fuente de verdad del proyecto: plan, proveedores con enlaces de
compra, requisitos reales, procedimientos, y el sistema de validación con el que se decide
cada avance de fase.

## Documentación

| Doc | Contenido |
|---|---|
| [00-plan-maestro.md](docs/00-plan-maestro.md) | El plan por fases madurado: metas, inversiones, gates |
| [01-proveedores-cdmx.md](docs/01-proveedores-cdmx.md) | Dónde comprar TODO en CDMX, con enlaces y precios |
| [02-restricciones-y-requisitos.md](docs/02-restricciones-y-requisitos.md) | Clima, agua, normativa, fiscal: lo que la realidad exige |
| [03-instalacion.md](docs/03-instalacion.md) | Procedimiento de instalación paso a paso por fase |
| [04-herramientas.md](docs/04-herramientas.md) | Herramientas necesarias, precios y dónde |
| [05-aprendizaje.md](docs/05-aprendizaje.md) | Tutoriales, canales, libros y cursos para tener criterio |
| [06-validacion-y-lazos-agenticos.md](docs/06-validacion-y-lazos-agenticos.md) | Métodos de validación V1–V9 y lazos de control L0–L4 |
| [07-puntos-ciegos-y-riesgos.md](docs/07-puntos-ciegos-y-riesgos.md) | Todo lo que el plan original no estaba considerando |
| [bom/](bom/) | Listas de materiales (BOM) por fase, en CSV |

## Filosofía

1. **Vender antes de construir** — cada fase se financia con la anterior; los gates
   Go/No-Go están escritos y versionados antes de gastar.
2. **Automatización DIY** — ESP32 + ESPHome + Home Assistant en lugar de controladores
   comerciales; lazos de histéresis con watchdogs, no optimismo.
3. **Ciclo corto primero** — microgreens (7–14 días) para iterar y cobrar rápido; hierbas
   NFT después.
4. **Operación como sistema de control** — todo se mide, todo se registra, y un lazo
   agéntico semanal (LLM sobre la bitácora y los datos de Home Assistant) convierte los
   datos en decisiones. Ver [docs/06](docs/06-validacion-y-lazos-agenticos.md).
