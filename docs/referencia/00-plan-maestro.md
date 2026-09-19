# Plan maestro — Huerto comercial automatizado (patio 80 m², CDMX)

Versión madurada del plan original (`proyecto-huerto-cdmx.pdf`), con gates medibles,
referencias cruzadas a proveedores, requisitos e instalación, y el sistema de validación
que gobierna cada avance.

## Filosofía

1. **Vender antes de construir.** Cada fase se financia con lo que ya se vende; la
   inversión de la siguiente fase solo se libera al pasar el gate (ver
   [06 §L4](06-validacion-y-lazos-agenticos.md)).
2. **Automatización DIY.** ESP32 + ESPHome + Home Assistant (~$3–5k) en lugar de
   controladores comerciales de hidroponia ($15–30k).
3. **Producto de ciclo corto primero.** Microgreens (7–14 días) para iterar y cobrar
   rápido; hierbas NFT (mayor ticket recurrente) después.

## Mapa de fases

| Fase | Qué | Cuándo | Inversión (MXN) | Meta | Gate de salida |
|---|---|---|---|---|---|
| 0 | Validación comercial con rack de microgreens | Semanas 1–6 | $4,000–6,000 | 2 clientes recurrentes | G0→1: ≥2 clientes con 3 compras semanales seguidas Y margen variable ≥55 % |
| 1 | Túnel 15–20 m² + producción formal + automatización v1 | Meses 2–4 | $18,000–28,000 | $6–10k/mes netos | G1→2: 4–5 clientes fijos, demanda insatisfecha 2 semanas, y v1 estable 30 días |
| 2 | Túnel a 25–30 m² + NFT de hierbas + automatización v2 (pH/EC) | Meses 5–9 | $35,000–55,000 | $12–18k/mes netos | G2→3: neto ≥$12k/mes ×3 meses con ≤9 h/semana medidas |
| 3 | Consolidación + camas personales + gantry/visión (testbed agtech) | Mes 10+ | discrecional | cero presión comercial | — |

Inversión total acumulada: **$60–90k MXN en ~9 meses, condicionada a ventas.** Si G0→1
falla, la pérdida total es ~$6k y termina el experimento.

## Fase 0 — Validación comercial (Semanas 1–6)

Rack bajo techo, sin túnel, sin NFT. Equipo: rack 4–5 niveles, 20 charolas 10×20, semilla
(girasol, chícharo, rábano, betabel, brócoli), fibra de coco, atomizador, báscula, empaques.
BOM completa con enlaces: [`bom/fase0.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase0.csv).

Proceso productivo: [03 §Fase 0](03-instalacion.md). Antes de la primera compra grande de
semilla: prueba de germinación **V1**; antes de vender una variedad: ensayo de rendimiento
**V2**.

La parte que decide todo (semanas 3–6) — smoke test comercial **V4**:

- Lista de 10–15 restaurantes/cafés/dark kitchens en radio de 5 km. Prioridad: cocina de
  autor, brunch, pokés/ensaladas, coctelería.
- Muestra física gratis + hoja de precios de 1 página. Sin cita: martes–jueves 10–12 am,
  preguntar por el chef.
- Oferta gancho: entrega semanal fija, charola viva o cortado el mismo día, sin mínimo el
  primer mes.
- Registrar el embudo completo: visitados → probaron → pidieron → recurrentes.

## Fase 1 — Producción formal + automatización v1 (Meses 2–4)

- **Estructura:** túnel ligero PTR/tubo galvanizado 15–20 m², malla antigranizo
  (obligatoria: granizo mayo–septiembre), plástico UV a dos aguas. Anclada.
- **Agua:** tinaco 450–750 L + captación pluvial con separador de primeras lluvias.
  El sistema corre 100 % de reserva propia (tandeo). Ver [02 §Agua](02-restricciones-y-requisitos.md).
- **Automatización v1:** 2×ESP32, sensores T/HR/sustrato/nivel/temp-agua, relés, bomba 12 V
  con nebulizadores, Home Assistant en Raspberry/mini-PC. Riego, ventilación y alarmas
  automáticos. BOM: [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv). Antes de producción: dry-run **V3**.
- **Producción objetivo:** 25–35 charolas/semana vendidas (siembras lunes y jueves).
- **Precios corregidos con mercado real 2026** (ver [01 §7](01-proveedores-cdmx.md)):
  charola viva girasol/chícharo **$90–120 lista** ($70–80 en volumen; el $60–90 del plan
  original solo como promo del primer mes); variedades finas $130–180; clamshell 100 g a
  restaurante $50–90 (el "$250–450/kg" del plan estaba 2–3× barato para microgreens).
- **Segundo canal desde Fase 1:** suscripción semanal a hogares (modelo MIJARDIIN, ~$260/sem
  por 3 clamshells); 10 hogares ≈ $10k/mes extra y desriesga la dependencia de 4–5
  restaurantes.
- **Realidad presupuestal:** la Fase 1 completa con racks de verdad ($2,000–2,600 c/u, no
  $1,200–1,800), iluminación T8, UPS y seguridad eléctrica sale en **$41,634** (BOM detallada:
  [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv)); el rango $18–28k del plan original era optimista.

## Fase 2 — Túnel NFT de hierbas + automatización v2 (Meses 5–9)

- **Cultivos:** albahaca **Nufar** (resistente a fusarium) + genovesa y morada, hierbabuena,
  cilantro, arúgula. Precio: por manojo/pieza ($20–35 B2B premium), no por kilo.
- **Sistema:** 6–8 líneas NFT de PVC **sanitario** 4" DIY (~$310–380/línea, confirmado, vs
  ~$1,156/línea comercial), **bomba sumergible 65 W** (no periférica de 370 W: $45 vs
  $260/mes de luz), filtro malla 120, depósito 200 L grado alimenticio aislado del sol,
  germinación en espuma agrícola nacional ($0.32/planta). Construcción:
  [03 §Fase 2](03-instalacion.md).
- **Automatización v2:** sondas pH y EC, 3 peristálticas (A, B, pH−), solenoides,
  ESP32-CAM, sensor de flujo. Control por histéresis con tiempo de mezcla; interlocks por
  nivel. BOM: [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv).
- **Mantenimiento honesto:** calibración quincenal de sondas (buffers 4.0/6.86), sonda pH
  nueva cada año (~$400/año), cambio completo de solución cada 2–3 semanas.
- El dashboard con histórico pH/EC/temp es también material de venta: "hierbas
  monitoreadas 24/7, cosechadas el día de entrega".

## Fase 3 — Consolidación y juguetes (Mes 10+)

Solo si las fases anteriores se pagan solas: camas elevadas personales con goteo colgado de
HA; gantry XY tipo FarmBot (V-slot + NEMA17 + GRBL/Klipper) o visión con cámara fija +
modelo ligero para cobertura foliar y detección temprana de plagas. Es el postre y el
testbed de percepción/manipulación agtech — no es el negocio.

## Números conservadores consolidados (mes 9–12)

| Concepto | Mensual (MXN) |
|---|---|
| Ingreso microgreens (30 charolas/sem) | $8,000–11,000 |
| Ingreso hierbas NFT (5–8 restaurantes) | $6,000–10,000 |
| **Bruto** | **$14,000–21,000** |
| Insumos (semilla, sustrato, nutriente, empaque) | −$3,500–5,000 |
| Agua, luz, calibración, mermas | −$1,000–1,500 |
| Gasolina/entregas | −$800–1,200 |
| **Neto realista** | **$8,000–13,500** |

Tiempo en régimen: 6–9 h/semana **según el plan; se verifica con el timesheet V9** — si da
más de 12 h, se ataca el desperdicio antes de escalar.

## Riesgos principales

Detalle y mitigaciones completas (incluyendo lo que el plan original no consideraba):
[07-puntos-ciegos-y-riesgos.md](07-puntos-ciegos-y-riesgos.md).

1. **No vender** (riesgo #1): la Fase 0 existe para acotarlo a ~$6k.
2. **Granizo:** malla antigranizo desde Fase 1, sin excepciones.
3. **Plagas/hongos:** desinfección H2O2, ventilación forzada, tirar charola contaminada
   sin dudar (umbral V8).
4. **Rotación de chefs:** el cliente es el restaurante, no el chef; formalizar con el
   administrador y facturar.
5. **Ausencias:** el sistema aguanta 3–4 días con alarmas remotas (validado con V5).

## Checklist — próximos 14 días

- [ ] Comprar rack, 20 charolas, semilla (girasol, chícharo, rábano) y coco — enlaces en [`bom/fase0.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase0.csv)
- [ ] Prueba de germinación V1 del lote recibido
- [ ] Primera siembra de prueba: 6 charolas, 2 variedades
- [ ] Mapear 15 restaurantes objetivo en radio de 5 km
- [ ] Hoja de precios de 1 página + nombre/marca simple
- [ ] Segunda siembra escalonada (día 4)
- [ ] Primera ronda de visitas con muestras (día 10–14)
- [ ] Pedir cotización de malla antigranizo y PTR (número listo si la validación pega)
- [ ] Arrancar bitácora (`bitacora/produccion.csv`) desde la charola #1
