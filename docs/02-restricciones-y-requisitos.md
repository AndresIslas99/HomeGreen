# Restricciones y requisitos reales (CDMX, 2026)

Lo que la realidad de la Ciudad de México exige del proyecto: clima a 2,240 msnm, agua con
tandeo, y el marco fiscal/sanitario para venderle a restaurantes. Fuentes y detalle completo:
[research/clima-agronomia.md](research/clima-agronomia.md) ·
[research/agua-captacion.md](research/agua-captacion.md) ·
[research/normativa-fiscal.md](research/normativa-fiscal.md).

---

## 1. Clima (los números duros)

**Normales SMN 1991–2020, estación Tacubaya:** media anual 18.1 °C; máximas 22–28 °C; mínimas
8–14 °C; 847 mm de lluvia/año concentrados de finales de mayo a inicios de octubre.

| Restricción | Dato | Implicación de diseño |
|---|---|---|
| **Granizo** | ~2–3 días/año en un punto fijo + 5–6 eventos severos/temporada; **pico estadístico: agosto** (UNAM 1981–2017); ninguna alcaldía está a salvo | Malla antigranizo desde Fase 1, montada 10–20 cm SOBRE el plástico; no desmontarla temprano (el pico es agosto, no mayo) |
| **Heladas** | Centro/norte urbano: prácticamente nulas (isla de calor). Sur alto (Tlalpan/Xochimilco/Milpa Alta): mínimas extremas de **−1 a −4 °C** dic–feb | En el sur: cerrar túnel de noche en invierno, alarma <6 °C, masa térmica (2 tambos negros de 200 L) o calefactor 500 W en relé para las ~10 noches críticas. **Una helada mata todo el NFT de albahaca** |
| **Germinación dic–feb** | Medias de 15–17 °C, noches de 5–9 °C: ciclos de 8–10 días se van a 12–16 y sube la pudrición | Tapete térmico (~$350) o cuarto de germinación a 22 °C con ESP32 + relé (<$1,000) |
| **UV extremo** | +20–25 % de UV vs nivel del mar; índice 11+ ("extremo") de marzo a septiembre, horas críticas 11:00–16:00 | Microgreens NUNCA al sol directo de mediodía. Malla sombra 35 % sobre las hierbas SOLO marzo–mayo (quitarla el resto del año: la albahaca necesita luz para aroma) |
| **Humedad jun–sep** | HR 70–80 % promedio, picos 89 %: temporada de moho, damping-off y botrytis | **Ventilación forzada por histéresis de HR >70 % es la automatización más importante del proyecto** (más que el riego). Sembrar menos denso jun–sep; riego solo por abajo |
| **Fotoperiodo** | 10 h 58 min (dic) a 13 h 18 min (jun); nov–feb es la época más soleada (cielos despejados) | Fase 0 sin lámparas es viable; para producción consistente en rack de 4 niveles: T8 6500K 12–14 h/día (~$60–90/mes de luz) |

**Calendario de riesgo anual** (detalle en el informe): heladas/germinación lenta nov–feb →
UV extremo mar–may → granizo abr–oct (pico ago) → hongos jun–oct → araña roja en secas.

**Variedades validadas para la altitud:** el límite no es la altitud sino las noches frías.
Albahaca Genovesa/Italian Large Leaf todo el año EN TÚNEL; **Nufar F1** como principal del
NFT (resistente a Fusarium oxysporum, el patógeno que contamina sistemas recirculantes).
Hierbabuena, cilantro y arúgula: cero problema (el cilantro agradece el fresco).

## 2. Agua (la restricción #1 de continuidad)

- **Tandeo formal en ~10 alcaldías / 284 colonias** (2025–2026): Álvaro Obregón, Coyoacán,
  Cuajimalpa, GAM, Iztapalapa, M. Contreras, Milpa Alta, Tláhuac, Tlalpan (94 colonias en
  jun-2025, la más golpeada) y Xochimilco. Consultar la colonia exacta en
  [Agua en tu Colonia (SACMEX)](https://aguaentucolonia.sacmex.cdmx.gob.mx).
- **Regla de diseño (el plan ya la tenía, confirmada):** el sistema corre 100 % desde
  tinaco/cisterna propia; la red solo rellena cuando hay presión. Autonomía mínima: 2 semanas
  (750–1,100 L cubren 2–4 semanas a 1–3 m³/mes de consumo).
- **Calidad de red variable por zona:** poniente/centro (Cutzamala) blanda, EC <0.4 mS/cm —
  sirve directo; oriente/sur (pozos) hasta 0.6–2.5 mS/cm — mala para NFT. **Acción: medir EC
  y pH de la llave del patio 3 días distintos ANTES de diseñar la nutrición del NFT** (esa
  medición decide: red filtrada / mezcla 50-50 con lluvia / lluvia+RO).
- El cloro de red (0.2–1.5 mg/L por norma) daña raíces en NFT → filtro de carbón activado en
  la línea que llena el depósito de solución.
- **La lluvia es la fuente premium:** EC ~0.02–0.06, gratis, 8,800–17,500 L/año captables del
  techo del túnel (15–30 m²). Separador de primeras lluvias obligatorio (el techo junta
  hollín entre tormentas).
- **Subsidio:** programa **Cosecha de Lluvia** (SEDEMA) instala sistemas de ~$20k gratis o con
  subsidio en alcaldías elegibles (histórico: Iztacalco, Iztapalapa, Tláhuac, Tlalpan,
  V. Carranza, Xochimilco y otras). Convocatoria **enero–febrero**; preparar INE, CURP,
  comprobante ≤3 meses y predial. Registro: programascall@sedema.cdmx.gob.mx.

## 3. Fiscal (la decisión más importante del arranque)

1. **La pregunta que decide todo: ¿eres socio/accionista de alguna persona moral?**
   - **NO** → alta en RFC como persona física con actividad **exclusivamente agrícola** en
     **RESICO**: **ISR $0 hasta $900,000/año cobrados** (art. 113-E LISR, noveno párrafo);
     sin declaraciones mensuales cumpliendo requisitos. Es el mejor tratamiento fiscal del
     sistema mexicano.
   - **SÍ** → RESICO PF está vetado (art. 113-E). Arrancar **facturando desde la empresa
     existente** (deduce toda la inversión de Fases 0–2; eficiente mientras el huerto
     empata) y reevaluar a 12 meses.
2. **CFDI 4.0 a restaurantes con IVA tasa 0 %** (vegetales no industrializados, art. 2-A
   LIVA; cortado/empacado sigue siendo "no industrializado"). Tasa 0 % ≠ exento: permite
   acreditar IVA de insumos. Clave de producto: `50404100` (hierbas frescas); unidad `KGM` o
   `H87` (pieza/charola).
3. **Retención 1.25 %:** los restaurantes persona moral retienen 1.25 % de ISR a un RESICO
   PF **salvo** que el CFDI lleve la leyenda de exención del art. 113-E noveno párrafo
   (regla 3.13.26 RMF). Configurarla en el facturador desde el día 1.
4. **PUE vs PPD:** factura PUE solo si el pago cae en el mismo mes; cualquier crédito que
   cruce de mes va como PPD y obliga al **complemento de pago (REP)** a más tardar el día 5
   del mes siguiente al cobro (un REP mensual agrupado por cliente basta; la multa por no
   emitirlo es de $22,300–127,530 por comprobante). En RESICO el ISR se causa sobre lo
   **cobrado**, no lo facturado. Política de cobro completa y machote de acuerdo de
   suministro: [research/cobranza-b2b.md](research/cobranza-b2b.md).
5. La factura es el contrato: formalizar con el administrador del restaurante, no con el
   chef (rotación de chefs = riesgo #4 del plan). Remisión firmada en cada entrega.

## 4. Sanitario y legal (carga real: casi cero, bien jugado)

| Trámite | ¿Obligatorio? | Cuándo | Costo |
|---|---|---|---|
| Aviso de huerto urbano a la alcaldía (art. 28, Ley de Huertos Urbanos CDMX) | Aviso simple; la ley da **derecho** a instalar huerto en propiedad privada (art. 24) | Fase 0; guardar acuse (escudo ante quejas vecinales) | $0 |
| Aviso de Funcionamiento **COFEPRIS-05-018** (DIGIPRiS) | Zona gris: producción primaria no; cortar+empacar habitual, recomendable | Al iniciar Fase 1 | $0, en línea, sin aprobación, no caduca |
| Licencia sanitaria / registro de producto | **NO existe** para vegetales frescos | — | — |
| SENASICA SRRC/BPA | **Voluntaria**; usar los [manuales BPA gratuitos](https://www.gob.mx/senasica/documentos/manuales-buenas-practicas-agricolas) como plantilla de bitácora de inocuidad | Guion desde Fase 1; certificación no (la escala no la amerita) | Manuales $0 |
| NOM-051 (etiquetado) | **NO aplica en B2B** (insumo, no producto preenvasado al consumidor final; charola viva = planta; corte a granel = exclusión textual). Solo aplicaría vendiendo clamshells cerrados a retail | Etiqueta comercial simple de todos modos: marca, variedad, fecha de cosecha, lote, contacto | — |
| SIAPEM / uso de suelo | **NO** sin local abierto al público (producción + entregas a domicilio ≠ establecimiento mercantil) | Solo si algún día hay mostrador | — |
| Seguro RC de producto | No obligatorio; lo piden cadenas/hoteles/comedores corporativos | Cotizar en Fase 2 (GNP RC PyMEs / GMX), ~$3,000–8,000/año aprox. | diferido |
| Apoyos | **Altépetl NO aplica** (solo suelo de conservación). Sí: Cosecha de Lluvia + capacitación gratuita SEDEMA/alcaldía + [Escuela de Huertos Urbanos](https://www.sedema.cdmx.gob.mx/comunicacion/nota/sedema-lanza-convocatoria-para-el-seminario-taller-escuela-de-huertos-urbanos) (convocatoria ~febrero; además es networking con la escena huertera CDMX) | | $0 |

**Nota de inocuidad (importante para el pitch y para no meterse en líos):** microgreens se
cosechan CORTADOS sobre el sustrato — riesgo mucho menor que los *germinados* (sprouts, alto
riesgo mundial de salmonela). Documentar siempre la desinfección de semilla y charolas
(H2O2), y no vender germinados de alfalfa/soya sin protocolo serio. La bitácora BPA + el
histórico de Home Assistant son el argumento de venta: trazabilidad que ningún competidor
encontrado ofrece.

## 5. Electricidad (restricción que el plan no consideraba)

La bomba del NFT corre 24/7. Elegir **sumergible de 65 W (~$45/mes)** en lugar de la
periférica de 370 W (~$260/mes y riesgo de brincar a tarifa DAC). El corte de luz >2 h en NFT
en día caluroso pone las raíces en riesgo: UPS pequeño para el cerebro (HA) + notificación de
corte, y ver [07-puntos-ciegos](07-puntos-ciegos-y-riesgos.md) para el análisis completo de
respaldo eléctrico.
