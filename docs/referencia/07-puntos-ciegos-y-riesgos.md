# Puntos ciegos y riesgos — lo que el plan no estaba considerando

Investigación al 12-sep-2026 con números duros. Fuente completa con todas las referencias:
[research/puntos-ciegos.md](../research/puntos-ciegos.md).

**Veredicto en una línea:** el plan es sólido en lo técnico y lo comercial básico, pero
subestima 4 cosas que sí matan proyectos así: la tarifa DAC de CFE, el tiempo real de
operación, la fragilidad del mercado restaurantero 2026 y la cadena de frío del producto
cortado.

---

## 1. Electricidad: el error más caro del plan original (tarifa DAC)

- CDMX es tarifa 1 doméstica: superar **250 kWh/mes de promedio móvil anual** reclasifica
  automáticamente a **DAC** — de ~$1.1/kWh subsidiado a ~$6.6/kWh + cargo fijo: el recibo se
  multiplica hasta 5×, y al ser promedio móvil, un año de bomba mal elegida te "encarcela"
  en DAC durante meses.
- **La bomba periférica de 0.5 HP del plan (370–450 W, 24/7) consume ~324 kWh/mes: manda a
  DAC ella solita** (~$2,600/mes de recibo). La bomba correcta —sumergible/magnética de
  35–60 W— consume ~32 kWh/mes. Está sobredimensionada ~8×; la diferencia son
  ~$1,600–2,000/mes, 15–20 % del neto proyectado. (Ya corregido en
  [03-instalacion](03-instalacion.md) y [bom/fase2.csv](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv).)
- Fase 2 bien diseñada ≈ 85–90 kWh/mes adicionales al hogar; con un hogar de 150+ kWh/mes
  ya rozas los 250. **Acciones esta semana (~$340):** medidor de enchufe Steren HER-432
  ($336) para auditar el consumo base 7 días; leer el promedio anual en el recibo CFE;
  helper de energía en Home Assistant con alarma en 220 kWh/mes. Si el negocio crece con
  LEDs: contrato **PDBT (negocio) separado** — sin subsidio pero sin castigo DAC y deducible.

## 2. Apagones: 3–6 cortes/año de 1–8 h son tabla de actuario, no paranoia

En NFT las raíces cuelgan en una película de agua: estrés en 1–2 h sin flujo, daño serio en
4+ h. Un corte nocturno de 6 h puede costar las 6–8 líneas (2–4 semanas de ingreso).

- **Un UPS de PC no sirve** (con bomba de 450 W dura 4–8 minutos y ni siquiera arranca el
  motor). La solución correcta: **arquitectura DC-first** — bomba de diafragma 12 V 40–60 W
  colgada de una batería en flotación permanente. Con **LiFePO4 100 Ah (Epcom $4,459,
  verificado)**: 28–30 h continuas o ~2.5 días en modo 15/15; variante austera con AGM
  24 Ah (~$2,500–2,900) para cortes ≤7 h, ampliable después. Paquete completo respaldo +
  seguridad eléctrica (GFCI, tierra física, gabinetes IP65, electricista): **$8,500–14,500**
  — partida obligatoria de Fase 2, detallada en
  [research/electrico-respaldo-seguridad.md](../research/electrico-respaldo-seguridad.md) y
  [03 §2.3](03-instalacion.md).
- Mini-UPS ($529) para módem + cerebro: sin internet no hay alarmas.
- Tras cada corte el sistema debe **auto-recuperarse** (ESPHome/HA arrancan solos) y el
  watchdog "bomba sin flujo tras restauración" (YF-S201) avisa al teléfono.

## 3. Cadena de frío: el producto cortado a temperatura ambiente muere en <1 día

Datos publicados (mostaza, 2023): a **5 °C dura 14 días; a 10 °C, 4 días; a 15 °C, 2 días;
a 20–25 °C, menos de 1 día**. Implicaciones:

- Producto cortado → **refrigerador dedicado a 4–5 °C desde la primera hora** (usado, 9–11
  pies, ~$3–5k; suma ~25–40 kWh/mes al cálculo DAC). No el refri de la casa.
- La **hielera sí basta para el reparto** (45–50 L + 4–6 gel packs: <10 °C por 4–6 h), no
  para almacenar.
- **La charola viva evita todo esto** — es el formato preferente; el cortado solo bajo
  pedido, entregado el día de corte (y ese dato es verificable en el dashboard: pitch real).

## 4. Tiempo real: 15 h/semana, no 6–9

Desglose honesto en régimen Fase 1–2 (30 charolas/sem + NFT + 4–6 clientes): siembra 3.0 +
cosecha/empaque 3.5–4.5 + lavado 1.5 + reparto 3.0–4.0 + ventas/cobranza 1.5–2.0 + sistema
1.0–1.5 + compras 1.0 = **14.5–17.5 h/semana**. La automatización quita riego, ventilación y
vigilancia (5–8 h que serían), pero **no siembra, no corta, no lava, no reparte y no cobra**.
A $10k netos/mes ÷ 65 h ≈ $150/h: decente, pero compáralo contra tu tarifa de consultoría
antes de escalar m² en lugar de precio. El timesheet V9 de
[06-validacion](06-validacion-y-lazos-agenticos.md) existe exactamente para esto.

## 5. El mercado restaurantero 2026 está contraído

- Enero es un cráter estructural (−30–50 % de ventas del sector); chefs vacacionan enero y
  Semana Santa; muchos restaurantes de autor cierran del 24-dic al 6-ene.
- 2026: CANIRAC estima +1.3 % nominal (venden MENOS platillos que 2025); 6 de cada 10
  aperturas fracasan; presión extra de nómina en camino. El microgreen es de lo primero que
  un costero recorta.
- **Modelar enero–febrero con −35 % de ingreso** y Semana Santa −20 %; el colchón de enero
  sale de noviembre–diciembre. **Ningún canal debe pesar >60 %**: sumar suscripción a
  hogares y mercados de productores desde Fase 1 (ver [01 §7](01-proveedores-cdmx.md)).

## 6. Mermas y rechazos que el plan no presupuestaba

- Merma realista en régimen: **10–20 % de charolas sembradas** (año 1: 20–25 % mientras se
  aprende; girasol/chícharo nobles, brócoli/betabel fallan más). **Sembrar 15–20 % más de lo
  comprometido, siempre.**
- Rechazo de restaurantes: 5–10 % de entregas en los primeros 6 meses (marchitez, spec,
  cambio de menú); presupuestar reposiciones como costo comercial. La charola viva reduce el
  rechazo casi a cero.

## 7. CAC real y churn de clientes

Cerrar un cliente cuesta **~$650 out-of-pocket + 8–10 h** (15 visitas → 2–3 clientes). Y la
rotación de chefs + cierres del sector implican **re-adquirir 30–50 % de la cartera cada
año**: $3,000–5,000/año + 30–40 h/año permanentes de labor comercial. Mitigaciones:
formalizar con administrador/dueño, pedir 1 referido a cada chef contento (baja el CAC
~70 %), WhatsApp Business con catálogo vivo.

## 8. Cobranza B2B — vender no es cobrar

El estándar foodservice es crédito de 15–45 días y el proveedor chico es el último de la
fila; el jugador CDMX establecido (MIJARDIIN) lo evita cobrando suscripción prepagada.
Política por fase, machote de acuerdo de suministro de 1 página, señales de alerta de
restaurantes que no van a pagar y protocolo de cobranza escalonado (7/14/45 días) en
[research/cobranza-b2b.md](../research/cobranza-b2b.md). Lo no negociable:

- **Fase 0: SPEI contra entrega, cero excepciones** — estás validando que *pagan*, no que
  *quieren*. Fase 1: factura semanal, pago a 7 días. Crédito a 15 días solo GANADO (8+
  semanas puntuales) y con tope de 2 semanas de pedidos. 30 días solo cadenas/hoteles con
  contrato.
- **Remisión firmada en CADA entrega** (sin firma de recepción no hay deuda demostrable) y
  ningún cliente >25–30 % de las ventas: el peor impago posible debe costar <$3,000.
- 1 factura vencida >7 días → siguiente entrega solo de contado; 2 vencidas → pausa total.
  El apalancamiento real del proveedor de perecederos es la continuidad, no el abogado.
- **Fiscal:** PUE solo si pagan en el mismo mes; crédito que cruza de mes = PPD + REP
  mensual agrupado los días 1–5 (multa por no emitir REP: $22,300–127,530 por comprobante).
  En RESICO el ISR se causa sobre lo COBRADO: la factura emitida no es ingreso.

## 9. Vecinos, condominio y uso del patio — verificar ANTES de invertir en Fase 1

- **Si es condominio:** el Art. 21 de la Ley de Propiedad en Condominio (CDMX) prohíbe
  destinar la unidad a usos distintos de la escritura; el Art. 23 hace **comunes** las
  azoteas — un túnel en área común de uso exclusivo requiere asamblea, y un solo vecino
  quejándose ante PROSOC puede parar el proyecto. **Checklist previo:** ① ¿escritura dice
  uso habitacional / condominio o propiedad plena? ② ¿el patio es privativo o común de uso
  exclusivo? ③ uso de suelo del predio (consulta gratuita SEDUVI en línea).
- **Casa propia:** el riesgo baja a molestias (ruido, escurrimientos, vista). La bomba DC
  chica es casi inaudible (otra razón del rediseño); estética de "invernadero ordenado" +
  comunicación temprana + regalar charolas a vecinos vale más que cualquier argumento legal.

## 10. Seguridad del equipo

CDMX tiene la tasa de victimización más alta del país (ENVIPE 2026: 34,930/100k). Exposición
en Fase 2: ~$8–14k de equipo robable. Mitigación casi gratis: **cerebro y fuente DENTRO de
casa** (solo nodos ESP32 de $150 a la intemperie — reduce el botín 80 %), nada visible desde
la calle, candado+cadena en el túnel (~$600), la ESP32-CAM con detección de movimiento
nocturno activada desde Fase 1, equipo marcado con serie y fotos.

## 11. Seguros: autoasegurarse a esta escala

El seguro de casa puede **rescindirse** por uso comercial no declarado — declararlo. RC de
producto formal: solo por encima de ~$25k/mes de ingreso. Mientras: **fondo de reposición de
$500/mes hasta juntar $10k** + inocuidad documentada (H2O2, análisis anual de agua
~$800–1,500, lote y fecha en cada etiqueta) — esa trazabilidad es con lo que respondes ante
un chef si algo sale mal (el sector acumula 7 recalls en EUA: producto crudo listo-para-comer).

## 12. Residuos: 100–150 kg/mes de coco con raíces

A 25–35 charolas/semana el sustrato usado se acumula rápido; mal manejado atrae fungus
gnats (la misma plaga que se combate con Gnatrol) y en CDMX la separación de orgánicos es
obligatoria. Ruta corta: composta propia en tambo (alimenta las camas de Fase 3), regalarlo
a huertos comunitarios (contactos vía la Escuela de Huertos Urbanos de SEDEMA), o entregarlo separado a la recolección de orgánicos
de la alcaldía. Regla operativa: el sustrato usado sale del área de producción el mismo
día de cosecha (charola con fusarium: a la basura en bolsa cerrada, nunca a la composta).

## 13. Burnout del fundador único: el riesgo estructural

La producción es 52 semanas/año sin pausa; el sistema aguanta 3–4 días solo para riego y
alarmas, **pero no cosecha, no empaca y no entrega** — si faltas un jueves, ese ingreso no
existe y el chef prueba otro proveedor. Punto de quiebre típico: mes 4–6.

- **Plan B desde el mes 4 (no cuando ya estés quemado):** ayudante fijo 6 h/sábado con SOP
  escrito con fotos ≈ **$1,300–1,600/mes** (~$55/h pagando arriba de mercado por
  confiabilidad) ≈ 15 % del neto — compra vacaciones, enfermedad cubierta y el primer
  peldaño del escalamiento.
- **Regla anti-burnout medible:** 3 semanas seguidas por encima de 18 h → se contrata o se
  recortan clientes. Prohibido "aguantar".

## 14. Escalabilidad: el techo no son los 80 m²

El techo real es **energía (DAC), horas-fundador y agua (tandeo)**. Escalera de decisiones
(cada peldaño se paga solo): ① subir precios / lista de espera → ② ayudante 4–8 h/sem →
③ densificación con LED **solo con contrato PDBT separado** → ④ segunda ubicación o alianza
con otro productor (él produce con tu spec, tú vendes con tu marca: el cuello del negocio es
la relación con chefs, no los m²). **Nunca** firmar renta sin lista de espera de 8+ clientes
recurrentes por 2 meses.

---

## El número corregido

Con merma 15–20 %, enero−35 %, CAC recurrente y 15 h/semana, **el neto realista de régimen
baja de "$8,000–13,500" a $6,500–11,000/mes**. Sigue siendo buen negocio secundario — pero
las fases se financian con este número, no con el optimista. Los gates de
[06 §L4](06-validacion-y-lazos-agenticos.md) se evalúan contra esta base.
