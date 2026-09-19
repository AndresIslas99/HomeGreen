# Fase 2: hierbas en NFT, dosificación v2 y continuidad eléctrica

**En una línea:** en los meses 5–9, con el túnel ampliado a 25–30 m², montas 8 líneas NFT de
albahaca y hierbas con dosificación automática de pH/EC, y antes de sembrar la primera línea
dejas resuelto lo que el plan original no presupuestaba: respaldo eléctrico DC, GFCI y tierra,
cadena de frío y una política de cobro que convierta ventas en caja.

!!! info "La fase en números"
    | | |
    |---|---|
    | **Objetivo** | Segundo producto de ticket recurrente (hierbas por manojo, $20–35 B2B premium) sobre una base automatizada que aguante apagones y no te mande a tarifa DAC |
    | **Inversión** | **$27,251** calculados desde [`bom/partidas.csv`](../../referencia/bom.md); $24,082 en versión austera. Bajó de los ~$39,000 que publicaba antes porque la seguridad eléctrica, el no-break y la captación pluvial se pagan en la Fase 1 y se cobraban otra vez aquí; el NFT puro de 8 líneas sigue en $7,200–8,700 ([compras](compras.md)) |
    | **Meta del plan** | $12,000–18,000/mes netos; **el neto corregido con merma, enero y 15 h/semana es $6,500–11,000/mes** ([07](../../referencia/07-puntos-ciegos-y-riesgos.md)) |
    | **Duración** | Meses 5–9: 2–3 fines de semana de construcción + 2 ciclos completos de albahaca + 3 meses de régimen para el gate |
    | **Prerequisito** | [G1→2](../fase-1/gate.md) aprobado: 4–5 clientes fijos, demanda insatisfecha 2 semanas y automatización v1 estable 30 días. **No se agrega NFT sobre una base inestable** |
    | **Gate de salida** | [G2→3](gate.md): neto ≥ $12k/mes × 3 meses con ≤ 9 h/semana medidas (V9) |

La lógica sigue siendo **vender antes de construir**: el NFT se compra por partes (PVC + bomba
+ depósito primero; sondas y peristálticas al final, porque el NFT funciona días en manual
mientras la dosificación se afina — [03 §orden de compra](../../referencia/03-instalacion.md)).
Lo que sí se compra completo y ANTES de la primera línea es el paquete de continuidad y
seguridad eléctrica: en NFT las raíces cuelgan en una película de 1–3 mm y sin recirculación
se marchitan en 2–4 h con el túnel caliente ([03 §2.3](../../referencia/03-instalacion.md)).

## Cómo se verá

![Planta del patio en Fase 2: túnel ampliado a 5 × 6 m con 8 líneas NFT en dos bancadas de 4, tambo de 200 L a la sombra, gabinete DC con batería LiFePO4, refrigerador y zona de cosecha junto a la casa, tinaco 750 L con tlaloque, tierra física y GFCI](../../assets/diagramas/layout/patio-fase-2.svg)

??? note "Leyenda y notas clave del plano"

    --8<-- "assets/diagramas/layout/patio-fase-2.notas.md"

El túnel pasa de 3 × 6 m a **5 × 6 m (30 m²)**: los racks de microgreens se quedan en su
mitad y las dos bancadas de 4 líneas NFT de 3 m ocupan la otra, con pendiente 2–3 % hacia el
retorno. El tambo de 200 L va tapado y a la sombra; las peristálticas dosifican al tambo junto
a la succión; las sondas de pH/EC leen en el retorno. Junto a la casa: mesa de cosecha de
acero inoxidable o polietileno, refrigerador dedicado a 4–5 °C, tina de lavado, hielera de
45–50 L y una cortina plástica que separa corte de cultivo (NOM-251). El gabinete DC (batería
+ controlador + fusiblera) va a 30 cm del piso y lejos del 127 V; el cerebro (mini-PC + router
+ UPS) sigue dentro de casa. El patio del dibujo es un **supuesto de 10 × 8 m, casa al sur,
acceso al norte**; si el tuyo difiere, lo que se conserva es: tambo a la sombra, retorno por
gravedad, cerebro bajo techo y nada tapa la coladera ([layout del patio](../../diseno/layout-patio.md)).

![Render 3D del patio en Fase 2 con túnel 5 × 6, bancadas NFT, tinaco y gabinetes](../../assets/diagramas/cad/patio-fase-2-3d.png)

![Render CAD del túnel ampliado a 5 × 6 m en PTR 1½" con techo a dos aguas](../../assets/diagramas/cad/tunel-5x6.png)

Modelos paramétricos: [`hardware/cad/patio_fase2.scad`](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/patio_fase2.scad),
[`tunel_5x6.scad`](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/tunel_5x6.scad) y
[`linea_nft.scad`](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/linea_nft.scad).

!!! warning "La ampliación del túnel no está en `bom/fase2.csv`"
    El BOM de Fase 2 cubre NFT, nutrición, automatización v2, respaldo, seguridad, frío, agua y
    semilla. El PTR, plástico, malla y anclas para pasar de 3 × 6 a 5 × 6 m se cotizan con la
    misma lista y el mismo herrero de [Fase 1 · Túnel](../fase-1/tunel.md) escalada a la nueva
    planta (lista de cortes en `tunel_5x6.scad`). [POR VERIFICAR: pedir 3 cotizaciones al
    herrero con la lista de cortes de `tunel_5x6.scad` y sumar el resultado al presupuesto de
    la fase antes de decidir el Go.]

## Los 5 meses de un vistazo

```mermaid
gantt
    title Fase 2 · meses 5–9 (ejemplo: mes 5 = febrero 2027, siguiendo la línea de tiempo de Fase 0)
    dateFormat YYYY-MM-DD
    axisFormat %b
    section Preparar
    Compras por bloques (seguridad y respaldo primero)      :c1, 2027-02-01, 14d
    Cotizar ampliación del túnel (3 herreros)                :c2, 2027-02-01, 10d
    Cosecha de Lluvia SEDEMA (convocatoria ene–feb)          :milestone, m0, 2027-02-05, 0d
    section Eléctrico
    Electricista: GFCI + tierra ≤ 25 Ω + contacto in-use     :e1, 2027-02-08, 5d
    Bus DC-first: batería, cargador, fusiblera, 2 bombas 12 V :e2, 2027-02-13, 7d
    Primer simulacro de apagón V11                           :milestone, m1, 2027-02-21, 0d
    section Construir
    Ampliar túnel a 5 × 6 m (herrero + plástico + malla)      :b1, 2027-02-15, 14d
    8 líneas NFT: perforar, bancadas, retorno, tambo          :b2, 2027-03-01, 10d
    Commissioning 48 h con agua sola                          :b3, 2027-03-11, 2d
    section Automatizar
    Nodo NFT v2 en banco + flasheo                            :a1, 2027-03-01, 7d
    Dry-run de dosificación en el tambo con agua              :a2, 2027-03-13, 3d
    Calibración quincenal (evento HA, recurrente)             :a3, 2027-03-16, 120d
    section Producir
    Germinar albahaca en foami (tapete térmico en feb–mar)    :p1, 2027-02-25, 14d
    Ciclo 1 de albahaca (trasplante → cosecha)                :p2, 2027-03-16, 35d
    Ciclo 2 + hierbabuena/cilantro/arúgula                    :p3, 2027-04-20, 35d
    section Vender y cobrar
    Hoja de precios de hierbas (por manojo) + acuerdos firmados :v1, 2027-03-01, 20d
    Suscripción a hogares + solicitud Mercado el 100          :v2, 2027-03-15, 30d
    Régimen: 3 meses de neto medido                           :v3, 2027-04-01, 91d
    section Decidir
    Timesheet V9 (4 semanas)                                  :d1, 2027-06-01, 28d
    Gate G2→3                                                 :milestone, g2, 2027-06-30, 0d
```

Detalle semana por semana en [Línea de tiempo](../../empieza-aqui/linea-de-tiempo.md).

## Páginas de la fase (en orden)

| # | Página | Qué logras | Cuándo |
|---|---|---|---|
| 1 | [Comprar por bloques](compras.md) | Lista exacta de `bom/fase2.csv` en 8 bloques con orden de compra, los 3 escenarios de presupuesto y la lista de lo que NO se compra (Flora Series, cédula 40, periférica 0.5 HP, DFRobot antes de tiempo) | Semana 1–2 |
| 2 | [Dejar la electricidad segura y con respaldo](electrico-respaldo.md) | GFCI + tierra ≤ 25 Ω + gabinetes IP65; bus DC-first con LiFePO4 100 Ah (28–30 h) y 2 bombas 12 V; UPS del cerebro; primer V11. **Obligatorio antes de la primera línea** | Semana 2–3 |
| 3 | [Construir las 8 líneas NFT](nft.md) | Tubo sanitario 4" perforado tras medir la canastilla, pendiente 2–3 %, retorno por gravedad, tambo a la sombra, manifold con 1–2 L/min por línea, germinación en foami; 48 h de commissioning con agua | Semana 3–6 |
| 4 | [Dosificar pH/EC automáticamente](dosificacion-v2.md) | Nodo NFT v2: sondas en el retorno, peristálticas al tambo, histéresis con tiempo muerto, interlocks, calibración quincenal, cambio de solución cada 2–3 semanas | Semana 5–8 |
| 5 | [Vender hierbas, cobrar y no perder producto](clientes-y-cobranza.md) | Precio por manojo, política de pago por fase, acuerdo de 1 página, protocolo 7/14/45, cadena de frío (refri + hielera), suscripción a hogares, Mercado el 100, cuándo asegurar | Semana 5 en adelante |
| 6 | [Pasar el gate G2→3](gate.md) | Medir neto ≥ $12k × 3 meses y ≤ 9 h/semana con `tools/gate_audit.py`; entender la tensión con el neto corregido de $6.5–11k y decidir sin mover los postes | Fin del mes 9 |

## Qué NO es la Fase 2

- **No es "encender la bomba y ya".** Sin GFCI, tierra y bus de batería no se siembra la primera
  línea: un corte nocturno de 6 h sin respaldo cuesta las 8 líneas (2–4 semanas de ingreso) y
  un patio mojado con 127 V sin GFCI es el escenario clásico de electrocución
  ([research/eléctrico](../../research/electrico-respaldo-seguridad.md)).
- **No es la periférica de 0.5 HP.** A 370 W las 24 h consume ~324 kWh/mes y te reclasifica a
  DAC ella sola (~$2,600/mes de recibo). La bomba de recirculación es de 12 V y 40–60 W; la de
  127 V solo llena, purga y trasiega ([07 §1](../../referencia/07-puntos-ciegos-y-riesgos.md)).
- **No es vender albahaca por kilo.** Contra la Central de Abastos (~$8–15/manojo) no se compite
  por precio: se vende por manojo o pieza a $20–35 B2B, cosechada el día de entrega y con
  histórico de pH/EC en el dashboard ([research/mercado](../../research/mercado-precios.md)).
- **No es una fase de 6–9 h/semana.** Con 30 charolas + NFT + 4–6 clientes son 14.5–17.5 h; el
  timesheet V9 lo mide y el gate lo exige ([07 §4](../../referencia/07-puntos-ciegos-y-riesgos.md)).
- **No se compra el kit pH DFRobot ni el Hanna de mano de $4–6k el día 1**: el electrodo caduca a
  los 12–18 meses aunque no se use; entran cuando las hierbas facturen ([compras](compras.md)).

## Ritmo semanal en régimen

| Cuándo | Qué | Tiempo |
|---|---|---|
| Diario | Panel de excepciones de HA (pH/EC fuera de banda, flujo, voltaje de batería), inspección de 2 min (pulgón en 5 hojas marcadas de albahaca, moho), bitácora | 10 min |
| Lunes y jueves | Siembra de microgreens + germinación de albahaca en foami + lavado | 3 h |
| Martes y viernes | Cosecha en la mañana (hierbas cortadas el día de entrega o en canastilla viva), hielera, ruta, remisión firmada | 3.5–4.5 h |
| Quincenal | Calibrar sondas pH/EC con buffers 4.01/6.86 y patrón 1.413 mS/cm (evento en HA con alarma) | 30 min |
| Cada 2–3 semanas | Cambio completo de solución del tambo, lavado de filtro malla 120, registro en bitácora | 1 h |
| Mensual | Simulacro de apagón V11: botar el breaker del patio 10 min | 20 min |
| Domingo | KPIs L2, informe del agente L3, plan de siembra, factura semanal y REP los días 1–5 | 1–1.5 h |

Total honesto: **14.5–17.5 h/semana** ([07 §4](../../referencia/07-puntos-ciegos-y-riesgos.md)).
Desde el mes 4 del proyecto el plan B es un ayudante fijo de 6 h/sábado (~$1,300–1,600/mes) con
SOP escrito; si 3 semanas seguidas pasas de 18 h, se contrata o se recortan clientes.

## Commissioning de la fase

Nada entra en producción sin pasar esta lista ([03 §Commissioning Fase 2](../../referencia/03-instalacion.md)):

- [ ] Todas las líneas con pendiente verificada y sin encharcamiento a media línea
- [ ] 48 h de recirculación con agua sola: sin fugas, caudal por línea en rango (1–2 L/min)
- [ ] Dry-run de dosificación en el tambo con agua: pH baja/EC sube según lo esperado y los interlocks disparan
- [ ] Primer ciclo de albahaca completo con pH/EC dentro de banda ≥ 90 % del tiempo (dato de HA, no de memoria)
- [ ] Simulacro de apagón: breaker del patio abajo 10 min → la bomba sigue, llegan las 2 alertas y al restaurar no hay falso "sin flujo"

## El gate

| Métrica | Umbral | Fuente del dato | Si falla |
|---|---|---|---|
| Neto mensual (cobrado − insumos − agua/luz/calibración/mermas − reparto − ayudante) | **≥ $12,000/mes durante 3 meses seguidos** | `bitacora/ventas.csv` conciliada con SPEI + costos | Permanecer en Fase 2 y subir la escalera: precios / lista de espera → ayudante → suscripción a hogares. No se baja el umbral |
| Horas del fundador por semana | **≤ 9 h/semana medidas 4 semanas (V9)** | `bitacora/timesheet.csv` | Atacar el rubro más caro en tiempo antes de escalar; ayudante 6 h/sábado |

Cómo medirlas, por qué el neto corregido de $6.5–11k tensiona este gate y qué decisión tomar en
cada caso: [gate.md](gate.md).

## Fuentes

- [00-plan maestro](../../referencia/00-plan-maestro.md) · [03-instalación §Fase 2](../../referencia/03-instalacion.md)
- [06-validación (L0, L4, V3, V7, V9, V11)](../../referencia/06-validacion-y-lazos-agenticos.md)
- [07-puntos ciegos y riesgos](../../referencia/07-puntos-ciegos-y-riesgos.md) (DAC, apagones, cadena de frío, 15 h/semana, el número corregido)
- [research/hidroponia-nft](../../research/hidroponia-nft.md) · [research/electrico-respaldo-seguridad](../../research/electrico-respaldo-seguridad.md) · [research/cobranza-b2b](../../research/cobranza-b2b.md) · [research/mercado-precios](../../research/mercado-precios.md)
- [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv)
