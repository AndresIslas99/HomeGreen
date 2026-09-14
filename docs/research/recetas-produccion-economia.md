# Recetas de producción por especie y economía unitaria verificada (charola 1020)
### Densidad de siembra, remojo, oscuridad, días a cosecha, rendimiento, merma y margen bruto por charola
**Fecha de investigación: 12 de septiembre de 2026.** Precios en MXN salvo indicación. Tipo de cambio de referencia usado para comparativos: ~18.5 MXN/USD (aprox.). Los datos marcados "aprox." o "estimación" no provienen de una ficha abierta hoy; el resto se confirmó abriendo la fuente (WebFetch/curl) hoy.

**Nota de método:** el presupuesto de WebSearch de la sesión estaba agotado (200/200), así que el descubrimiento se hizo con los buscadores internos de cada sitio (Shopify `/search`), la API pública de WooCommerce de Hydro Environment, descarga directa de PDFs de Johnny's y fetch de fichas de producto. Donny Greens quedó inaccesible (Cloudflare; además hoy es una landing de cursos sin datos abiertos). Se cumplió el cruce con 3+ fuentes de la lista pedida: **Bootstrap Farmer, Johnny's Selected Seeds y True Leaf Market**, más Hydro Environment para precios MXN.

---

## 1. Fuentes primarias abiertas hoy (por qué son confiables)

| Fuente | Qué aporta | Enlace |
|---|---|---|
| **Johnny's Selected Seeds — Micro Greens Yield Trial 2017** (PDF, 2 pp) | El ÚNICO dataset público con semilla pesada en gramos y rendimiento medido por charola 1020 para 29 variedades (≥3 repeticiones por variedad, cosecha a primera hoja verdadera, outliers excluidos) | PDF: https://www.johnnyseeds.com/on/demandware.static/-/Library-Sites-JSSSharedLibrary/default/dwa67c24b8/assets/information/micro-greens-yield-trial-results-tech-sheet.pdf · Landing: https://www.johnnyseeds.com/growers-library/vegetables/microgreens/micro-greens-yield-trial-results-tech-sheet.html |
| **Johnny's — Microgreens Comparison Chart** (PDF, 4 pp, rev. dic-2024) | Clasificación rápida/lenta por especie, precios USD por lb (referencia para detectar sobreprecio local), guía de cultivo (18–24 °C ambiente, >24 °C sube presión de enfermedad) | PDF: https://www.johnnyseeds.com/on/demandware.static/-/Library-Sites-JSSSharedLibrary/default/dw82bb95b4/assets/information/microgreens-comparison-chart-pdf.pdf · Landing: https://www.johnnyseeds.com/growers-library/vegetables/microgreens/micro-greens-comparison-chart.html |
| **Johnny's — Key Growing Information (microgreens)** | Método general: siembra al voleo 1/8–1/4" entre semillas, 24 °C suelo para germinar luego 16 °C, rápido = 10–15 días, lento = 16–25 | https://www.johnnyseeds.com/growers-library/vegetables/microgreens-key-growing-information.html |
| **Bootstrap Farmer — The Ultimate Microgreen Cheat Sheet** | Densidades g/1020, remojo y ventanas de cosecha por especie | https://www.bootstrapfarmer.com/blogs/microgreens/the-ultimate-microgreen-cheat-sheet |
| **Bootstrap Farmer — Top Ten Microgreens to Grow** | Segunda lectura de densidades + días de oscuridad/apilado por especie | https://www.bootstrapfarmer.com/blogs/microgreens/top-ten-microgreens |
| **Bootstrap Farmer — Mold on Microgreens** | Factores de merma: girasol, cilantro y chícharo son las semillas "sucias" que más se benefician de desinfección; densidad excesiva = "tormenta perfecta" de moho; humedad objetivo 40–60% | https://www.bootstrapfarmer.com/blogs/microgreens/microgreens-how-to-combat-and-prevent-mold |
| **True Leaf Market — fichas de producto** (girasol, chícharo, amaranto, betabel) | Tasas de siembra, remojo, blackout y días por especie; precios USD/lb de referencia | girasol: https://www.trueleafmarket.com/products/sunflower-black-oil-microgreens-seeds · chícharo: https://www.trueleafmarket.com/products/pea-microgreens-seeds · amaranto: https://www.trueleafmarket.com/products/amaranth-sprouting-red-garnet-seeds-conventional · betabel: https://www.trueleafmarket.com/products/beet-seeds-microgreens |
| **Hydro Environment (MX)** — fichas por gramo con escalones de volumen | Precio MXN/kg real para las 8 especies (ver §3) | ver tabla de proveedores |
| **On The Grow — guías de siembra gratuitas (PDF)** | Existen (43 variedades, por tamaño de charola, con pesos de cosecha promedio) pero requieren "checkout" con correo; no se pudieron extraer los números hoy | https://onthegrow.net/products/free-microgreen-seeding-guide-pdf y https://onthegrow.net/products/free-tray-specific-microgreen-seeding-guide-pdf |

**Descargados a disco (respaldo):** `scratchpad/research/johnnys-yield-trial.pdf` y `scratchpad/research/johnnys-comparison-chart.pdf`.

---

## 2. TABLA OPERATIVA POR ESPECIE — charola 1020 estándar (25×50 cm)

Receta recomendada = síntesis de las 3 fuentes; entre paréntesis, el dato de cada fuente. Rendimientos de Johnny's convertidos de oz a g (1 oz = 28.35 g), medidos a primera hoja verdadera — cosechando 1–2 días más tarde (estándar comercial en México) se puede superar el rango.

| Especie | Semilla g/charola (recomendado) | Remojo | Oscuridad / peso | Días totales a cosecha | Rendimiento g/charola | Merma típica* |
|---|---|---|---|---|---|---|
| **Girasol** (black oil) | **120–150 g secos** (BF cheat: 150 g; BF top-ten: 250 g — exceso, favorece moho; TLM: 9 oz YA remojada ≈ 150–170 g secas) | 6–12 h (BF); 3–6 h agua fría (TLM); 8 h sin reusar agua (Johnny's ficha shoots) + pre-germinado 1–2 d en colador (BF) | 2–3 d apilado con peso (BF) | **8–12 d** (BF, TLM); ideal 10 (BF) | **300–500 g** (estimación de consenso: multiplicador 2–3.3× la semilla seca; coherente con informe interno mercado-precios; Johnny's no lo incluyó en su trial) — VERIFICAR en 1as siembras | 5–10% (semilla "sucia" según BF-mold; cáscaras pegadas; moho si >200 g/charola) |
| **Chícharo** | **250–300 g secos** (BF cheat: 200–275 g; BF top-ten: 12 oz = 340 g; TLM: 10 oz = 283 g) | 6–12 h agua fría (BF); TLM: 6–24 h, ideal 18–20 h | 3–5 d (BF); TLM: 3–4 d con ~2.3 kg encima | **9–13 d** (BF 8–12; TLM 6–14) | **350–600 g** (estimación: multiplicador 1.4–2×; sin dato medido público) — VERIFICAR | 3–8% (germina casi siempre; riesgo = moho por remojo largo) |
| **Rábano** (Champion/daikon) | **25–30 g** (BF: 30 g; BF cheat: 30–35 g; Johnny's trial: 22.5–28.5 g) | No | 1–2 d germinación (BF); 2–3 d práctica común | **7–10 d** (Johnny's midió 8–9.5 d; BF 5–12) | **225–325 g medidos** (Johnny's: daikon 8 oz=227 g, Red Arrow 10 oz=283 g, Hong Vit 11.5 oz=326 g) | 2–5% (la especie más noble; ideal para aprender) |
| **Betabel** (Early Wonder/Bull's Blood) | **25–35 g** (Johnny's trial: 23 g; BF cheat: 20–30 g; TLM: 1–1.5 oz = 28–42 g) | 4–8 h (BF); TLM: 4 h | **6–8 d** de blackout (TLM) — el más largo de la lista | **13–18 d** (Johnny's midió 17; BF 10–14; TLM 12–23) | **180–270 g** (Johnny's: 7.5 oz = 213 g) | 8–12% (germinación irregular del glomérulo; cáscara pegada a cotiledón) |
| **Brócoli** (Waltham 29) | **13–18 g** (Johnny's trial: 13 g; BF: 15–20 g) | No | 2–3 d (BF) | **9–13 d** (Johnny's midió 12.5; BF 7–10) | **250–330 g** (Johnny's: 11.5 oz = 326 g — de los mejores rendimientos/g de semilla del trial) | 5–10% (damping-off si se excede densidad) |
| **Amaranto** | **8–12 g** (Johnny's trial: 7.5 g; TLM recomienda 1 oz = 28 g — caro e innecesario) | No (TLM: no-soak) | 2–4 d (TLM) | **14–18 d** (Johnny's midió 17; TLM 8–12 cosechando chico) | **120–200 g** (Johnny's: 6.5 oz = 184 g con 7.5 g de semilla) | 10–15% (sensible a frío <18 °C y a exceso de humedad; charolas noche fría CDMX invierno) |
| **Cilantro** | **30–40 g entera** (BF cheat: 30–40 g; BF top-ten: 30 g partida/split; Johnny's trial: 26 g monogerm) | 2–4 h + baño H2O2 5–10 min (BF) | 7–9 d apilado (BF) — germinación lenta | **18–24 d** (Johnny's midió 20; BF 15–20; BF cheat 3–4 sem) | **140–200 g** (Johnny's: 6 oz = 170 g) | 8–12% (ciclo largo = más ventana de hongos; semilla "sucia" según BF-mold) |
| **Arúgula** | **10–12 g** (Johnny's trial: 10 g; BF: 12 g) | No (semilla mucilaginosa: NUNCA remojar) | 3–4 d (BF) | **10–14 d** (Johnny's midió 14; BF 6–12) | **200–285 g** (Johnny's: 10 oz = 283 g — 28× su semilla, el mejor multiplicador del trial) | 5–8% (tallo frágil: regar SOLO por fondo) |

\* **Merma**: NINGUNA fuente pública tabula porcentajes de pérdida (Bootstrap Farmer lo confirma: solo advierte "pérdidas significativas de charolas" sin cifras). Los % son **supuestos de planeación propios**, jerarquizados con los factores de riesgo documentados por Bootstrap Farmer (semillas sucias: girasol/cilantro/chícharo; densidad excesiva; humedad >60%; falta de flujo de aire). Úsalos como provisión financiera (global ~8%) y sustitúyelos por datos propios desde la semana 2. La bitácora por charola (fecha, especie, g semilla, g cosechados, incidencias) en Home Assistant es la herramienta: en 4 semanas tendrás mejores números que cualquier fuente.

### Notas críticas por especie
1. **Girasol — la trampa "presoaked":** TLM siembra "9 oz ya remojadas"; remojada pesa ~1.5–1.8×. No copiar "250 g" (BF top-ten) con semilla seca: 120–150 g secos es el punto dulce costo/moho.
2. **Chícharo — el falso barato:** $340/kg suena bien hasta que multiplicas por 275 g/charola = $93.50 SOLO de semilla (ver §4). Es la única especie donde Hydro Environment NO es viable.
3. **Amaranto — ojo con la variedad:** lo rentable del amaranto micro es el COLOR fucsia (Garnet Red, *A. tricolor/hypochondriacus* rojo). El "Amaranto Producción Nacional" de Hydroenv ($300/kg) es criollo de grano (*A. hypochondriacus*), casi seguro VERDE: germinará, pero puede no alcanzar el precio "fino". Sembrar 1 charola de prueba y comparar contra sobre Garnet Red de Hydrocultura/ISLA antes de apostarle.
4. **Cilantro — entera vs monogerm:** HE vende semilla entera (doble embrión, germinación lenta/desigual). Johnny's recomienda monogerm/partida para micros. Con entera: subir a 35–40 g y aceptar 2–3 días más.
5. **Betabel/acelga:** pertenecen al mismo género; la acelga Bright Lights de Johnny's rindió 9.5 oz (269 g) en 16.5 días — considerar como sustituto más rendidor del betabel si el chef acepta tallos multicolor.
6. **Temperatura CDMX:** el rango óptimo de Johnny's (18–24 °C; >24 °C sube enfermedad) es básicamente el clima de la CDMX bajo sombra — la ventaja estructural del proyecto. En invierno, amaranto y albahaca sufrirán (<18 °C nocturno): calendarizarlos abril–octubre.

---

## 3. Precio de semilla verificado HOY en México (base del costo por charola)

Todos los escalones confirmados abriendo la ficha (tabla "Cantidad/Precio" de cada producto Hydro Environment; escalón 453+ g = precio "por kilo efectivo"):

| Especie | Producto y ficha | $/g en 453+ g | ≈ $/kg | Cruce internacional (aprox., 25 lb) |
|---|---|---|---|---|
| Girasol | HE "Girasol Forrajero Var. Nacional" https://hydroenv.com.mx/producto/gramo-de-semilla-de-girasol-forrajero-var-nacional/ (escalones $10.90/$4.50/$0.90/**$0.30**) | $0.30 | **$300** | TLM 25 lb ⇒ ~$141/kg |
| Girasol (alternativas ya verificadas en informe semillas) | Al Natural (específica microgreens) **$185/kg** https://www.alnatural.com.mx/tienda/semilla-de-girasol-para-microgreens · CEDA Mayoreo Online **$24–34/kg** https://mayoreo.online/products/semilla-de-girasol-con-cascara-jumbo | — | $24–185 | — |
| Chícharo | HE Early Perfection https://hydroenv.com.mx/producto/gramo-de-semilla-de-chicharo-variedad-early-perfection/ | $0.34 | **$340** | TLM 25 lb ⇒ ~$106/kg (HE cuesta 3.2×) |
| Rábano | HE Champion https://hydroenv.com.mx/producto/gramo-de-semilla-de-rabano-var-champion/ | $1.60 | **$1,600** | Johnny's daikon 25 lb ⇒ ~$430/kg (HE 3.7×) |
| Betabel | HE Early Wonder https://hydroenv.com.mx/producto/gramo-de-semilla-de-betabel-o-remolacha-variedad-early-wonder/ | $1.60 | **$1,600** | Johnny's Early Wonder 1 lb $18 USD |
| Brócoli | HE Waltham 29 https://hydroenv.com.mx/producto/gramo-de-semilla-de-brocoli-variedad-waltham-29/ | $3.50 | **$3,500** | Johnny's 25 lb ⇒ ~$440/kg (¡HE 8×!) |
| Amaranto | HE Producción Nacional https://hydroenv.com.mx/producto/gramo-de-semilla-de-amaranto-para-siembra-produccion-nacional/ (escalones $10.90/$4.70/$1.00/**$0.30**) — ver nota de variedad §2.3 | $0.30 | **$300** | TLM Garnet Red 1 lb $34.25 USD ⇒ ~$635/kg |
| Cilantro | HE Var Líder https://hydroenv.com.mx/producto/gramo-de-semilla-de-cilantro-var-lider/ (escalones $10.90/$4.50/$1.00/**$0.45**) | $0.45 | **$450** | Johnny's monogerm 1 lb $22.60 USD |
| Arúgula | HE https://hydroenv.com.mx/producto/gramo-de-semilla-arugula/ (escalones $18.50/$11.00/$6.70/**$2.80**) | $2.80 | **$2,800** | Johnny's 25 lb ⇒ ~$590/kg (HE 4.7×) |

**Hallazgos nuevos de hoy vs el informe de semillas:** (1) HE SÍ vende girasol a granel (forrajero, $300/kg) — puente útil mientras validas el de CEDA; (2) cilantro a $450/kg y amaranto a $300/kg en HE completan por fin el abasto nacional de las 8 especies; (3) la arúgula HE a $2,800/kg es 4.7× el precio internacional: úsala solo para arrancar y presiona cotización a Hydrocultura.

**Otros insumos por charola** (verificados en informe semillas-sustrato-charolas del 12-sep-2026):
- Polvillo de coco germinación 50 L HE $115 ⇒ **$2.00–2.30/charola** (https://hydroenv.com.mx/producto/polvillo-de-coco-para-germinacion-50-l-sustrato-organico/)
- Agua + energía (bombeo/ventilación DIY) ⇒ ~$1.00/charola
- H2O2/desinfección ⇒ ~$0.30/charola
- Etiqueta + film para charola viva ⇒ ~$1.00/charola
- Clamshell PET 8 oz (SOLO venta cortada) ⇒ aprox. $2.50–4.50/pza (https://listado.mercadolibre.com.mx/clamshell)
- Amortización de charola ($60–70 ÷ ~25 ciclos) ⇒ ~$2.50/charola (súmalo si la charola viva viaja y no regresa: cóbrala o pide depósito)

---

## 4. ECONOMÍA UNITARIA POR CHAROLA (charola viva, B2B restaurante)

**Fórmula:** costo variable = semilla (densidad recomendada media × $/g escalón 453+) + $4.50 de base (coco 2.20 + agua/energía 1.00 + desinfección 0.30 + etiqueta/film 1.00). Precios de venta = lista corregida del informe mercado-precios: girasol/chícharo **$90–120**, finas **$130–180**.

| Especie | g/charola | $ semilla | Costo variable total | Precio B2B | **Margen bruto $/charola** | Margen % |
|---|---|---|---|---|---|---|
| Girasol (semilla CEDA $34/kg, tras prueba de germinación) | 135 | $4.60 | **$9.10** | $90–120 | **$81–111** | 90–92% |
| Girasol (Al Natural $185/kg, específica micros) | 135 | $25.00 | $29.50 | $90–120 | $61–91 | 67–75% |
| Girasol (HE forrajero $300/kg) | 135 | $40.50 | $45.00 | $90–120 | $45–75 | 50–63% |
| **Chícharo (HE $340/kg)** | 275 | **$93.50** | **$98.00** | $90–120 | **−$8 a +$22** | **−9% a 18%** ⚠️ |
| Chícharo (arvejón CEDA, aprox. $40–60/kg, POR VALIDAR) | 275 | $11–16.50 | $15.50–21.00 | $90–120 | $69–105 | 77–87% |
| Rábano (HE $1,600/kg) | 28 | $44.80 | $49.30 | $130–180 | **$81–131** | 62–73% |
| Betabel (HE $1,600/kg) | 30 | $48.00 | $52.50 | $130–180 | $78–128 | 60–71% |
| Brócoli (HE $3,500/kg) | 15 | $52.50 | $57.00 | $130–180 | $73–123 | 56–68% |
| Amaranto (HE nacional $300/kg — nota color §2.3) | 10 | $3.00 | **$7.50** | $130–180 | **$123–173** | 94–96% |
| Cilantro (HE $450/kg) | 35 | $15.75 | $20.25 | $130–180 | $110–160 | 84–89% |
| Arúgula (HE $2,800/kg) | 11 | $30.80 | $35.30 | $130–180 | $95–145 | 73–81% |

**Ajustes a aplicar sobre el margen bruto:** merma global de planeación 8% del ingreso (≈$8–14/charola) + amortización de charola $2.50 + entrega (~$15–25/parada en ruta propia, prorrateable entre 3–6 charolas por cliente). Aun con todo, girasol-CEDA, amaranto, cilantro y arúgula quedan arriba del 65% neto variable.

### Venta cortada (clamshell) — segunda lectura
Una charola de rábano (283 g) llena ~2.5–3 clamshells de 100 g. A $50–90/clam B2B (rango del informe mercado-precios): ingreso $125–270 por charola equivalente, menos $10.50 de clamshells (3 × $3.50) y ~30 min extra de trabajo de corte/empaque. **El clamshell paga mejor por charola pero peor por hora**; conviene solo para rutas de suscripción a hogares o clientes que no aceptan charola viva.

### Margen por charola-SEMANA de rack (la métrica que decide qué sembrar)
El rack es el recurso escaso; el margen hay que dividirlo entre las semanas que la charola ocupa el rack (días ciclo ÷ 7). A precio medio ($105 girasol/chícharo, $155 finas):

| Especie | Margen $/charola | Ciclo (d) | **$/charola-semana** |
|---|---|---|---|
| **Rábano** | $105.70 | 9 | **$82** |
| **Arúgula** | $119.70 | 12 | **$70** |
| Amaranto (si logra precio fino) | $147.50 | 16 | $65 |
| Brócoli | $98.00 | 11 | $62 |
| **Girasol (CEDA)** | $95.90 | 11 | **$61** |
| Chícharo (CEDA validado) | $87.00 | 11 | $55 |
| Betabel | $102.50 | 15 | $48 |
| Cilantro | $134.75 | 21 | $45 |
| Chícharo (semilla HE) | $7.00 | 11 | $4.50 ☠️ |

---

## 5. ¿Dónde quedan cortos los números del plan original?

1. **"$60–90/charola (girasol/chícharo)": solo funciona para girasol con semilla de CEDA.** A $60: girasol-CEDA deja 85% de margen (bien), pero chícharo con semilla HE pierde $38/charola, rábano deja $10.70 (18%), brócoli $3 (5%) y betabel $7.50 (13%). Ninguna especie fina paga el trabajo a $60–90. **Adoptar la lista corregida del informe de mercado: $90–120 girasol/chícharo, $130–180 finas; $60–80 únicamente como precio de volumen (4+ charolas/sem) para girasol.**
2. **"Costo variable 25–35%": es correcto SOLO con la combinación precios-corregidos + semilla optimizada.** Con los precios del plan y semilla HE, el costo variable real de finas es 39–65% del ingreso y el de chícharo >100%. Con la lista corregida el mix queda en ~15–30% — el plan se salva por el lado del precio, no del costo.
3. **El plan no distinguía el costo de semilla POR CHAROLA.** El error conceptual: el chícharo ($340/kg, "barato") cuesta $93.50/charola porque lleva 275 g, mientras el brócoli ($3,500/kg, "carísimo") solo cuesta $52.50 porque lleva 15 g. La densidad manda tanto como el $/kg.
4. **Ingreso Fase 1 revalidado:** 30 charolas/sem con mix 15 girasol ($105) + 15 finas ($155) = $3,900/sem ≈ **$16,900/mes bruto** con costo variable ~$805/sem (21%) ⇒ margen variable ≈ $13,000/mes. El objetivo del plan ($7,000–12,000 bruto) es alcanzable incluso con 20–22 charolas/sem vendidas — hay colchón para la curva de aprendizaje y la merma.
5. **Costo oculto no presupuestado:** la brecha MX vs internacional en semilla de brassicas (brócoli 8×, arúgula 4.7×, rábano 3.7× el precio de 25 lb de Johnny's/TLM). A partir de Fase 2 (>40 charolas/sem de finas), evaluar importación directa (requiere permiso fitosanitario SENASICA y mínimos de compra) o negociar mayoreo real con Hydrocultura — es la palanca más grande de margen que queda sobre la mesa.

---

## 6. Tabla de proveedores (esta dimensión)

| Nombre | Qué | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Hydro Environment (CDMX/EdoMex) | Girasol forrajero a granel | $0.30/g en 453+ g (≈$300/kg) | https://hydroenv.com.mx/producto/gramo-de-semilla-de-girasol-forrajero-var-nacional/ | Confirmado hoy vía tabla de volumen de la ficha |
| Hydro Environment | Cilantro Var Líder a granel | $0.45/g en 453+ (≈$450/kg) | https://hydroenv.com.mx/producto/gramo-de-semilla-de-cilantro-var-lider/ | Semilla entera (no monogerm): subir densidad a 35–40 g |
| Hydro Environment | Amaranto nacional a granel | $0.30/g en 453+ (≈$300/kg) | https://hydroenv.com.mx/producto/gramo-de-semilla-de-amaranto-para-siembra-produccion-nacional/ | Criollo de grano: probablemente micro VERDE, probar color |
| Hydro Environment | Arúgula a granel | $2.80/g en 453+ (≈$2,800/kg) | https://hydroenv.com.mx/producto/gramo-de-semilla-arugula/ | 4.7× precio internacional; usar solo para arrancar |
| Hydro Environment | Chícharo, rábano, betabel, brócoli a granel | $340 / $1,600 / $1,600 / $3,500 por kg | fichas en informe semillas-sustrato-charolas | Verificados 12-sep-2026 |
| Al Natural Grow Shop (CDMX) | Girasol específico microgreens 1 kg | $185 | https://www.alnatural.com.mx/tienda/semilla-de-girasol-para-microgreens | Plan B si el de CEDA no germina |
| Mayoreo Online (Central de Abastos) | Girasol c/cáscara jumbo 1 kg / 5 kg / bulto | $34 / $140 / $24/kg | https://mayoreo.online/products/semilla-de-girasol-con-cascara-jumbo | Grado alimento: prueba de germinación obligatoria |
| Hydrocultura | Semillas microgreens (todas las finas, incl. Garnet Red) | $120–309 por bolsa (gramaje por confirmar) | https://hydrocultura.com/collections/semillas-para-microgreens-o-microvegetales | Pedir tabla precio/gramaje por WhatsApp +52 55 9435-6905 |
| Johnny's Selected Seeds (EUA) | Yield Trial 2017 + Comparison Chart (datos, no compra) | gratis | https://www.johnnyseeds.com/growers-library/vegetables/microgreens/micro-greens-yield-trial-results-tech-sheet.html | La referencia de rendimientos por 1020 |
| Bootstrap Farmer (EUA) | Cheat sheet + guías (datos) | gratis | https://www.bootstrapfarmer.com/blogs/microgreens/the-ultimate-microgreen-cheat-sheet | Densidades y remojos por especie |
| True Leaf Market (EUA) | Fichas con tasas de siembra y blackout | gratis (semilla 1 lb US$8.90–34.25) | https://www.trueleafmarket.com/products/pea-microgreens-seeds | Cruce de girasol/chícharo/amaranto/betabel |
| On The Grow (EUA) | Guía gratuita de densidades 43 variedades con pesos de cosecha (PDF por correo) | gratis | https://onthegrow.net/products/free-tray-specific-microgreen-seeding-guide-pdf | DESCARGARLA (checkout $0) — completaría los rendimientos de girasol/chícharo |
| Mercado Libre | Clamshells PET 1 lb/8 oz | aprox. $2.50–4.50/pza por caja | https://listado.mercadolibre.com.mx/clamshell | Fichas volátiles; usar búsqueda |

---

## Recomendación concreta

**Qué sembrar las primeras 6 semanas (Fase 0) y por qué:**
1. **Girasol** — el producto ancla de volumen. Comprar 1 kg CEDA ($34) + 1 kg Al Natural ($185) y correr la prueba A/B de germinación YA (es la decisión de mayor impacto: mueve el costo de $45 a $9/charola). Receta: 135 g secos, remojo 8 h, 2–3 d apilado, cosecha día 10.
2. **Rábano** — el mejor $/charola-semana ($82) y el de menor riesgo operativo: sin remojo, 9 días, semilla disponible HOY en HE aunque cueste $1,600/kg. Receta: 28 g, 2 d oscuridad, cosecha día 8–9. Es la "fina" para la primera hoja de precios ($130–180).
3. **Arúgula** — segunda fina de arranque: $70/charola-semana, 12 días, demanda chef garantizada. Receta: 11 g, sin remojo, riego solo por fondo.
4. **Amaranto (charola de PRUEBA, no de venta)** — margen potencial 94–96% con semilla nacional a $300/kg, PERO hay que validar el color: sembrar 1 charola HE nacional vs 1 sobre Garnet Red (Hydrocultura/ISLA). Si el nacional sale verde, el Garnet Red importado sigue dejando ~90% por lo poco que se usa (10 g).
5. **NO arrancar con chícharo** hasta conseguir arvejón grado alimento validado (~$40–60/kg CEDA, por confirmar): con semilla HE a $340/kg pierde dinero a cualquier precio ≤$98. Preguntar arvejón entero en Mayoreo Online/La Molinera esta semana.
6. **Brócoli y betabel: segunda ola** (semanas 4–8), cuando Hydrocultura confirme gramaje/precio de mayoreo — a precios HE dan 56–71%, aceptable pero mejorable a >85% con semilla a precio internacional.
7. **Cilantro: solo bajo pedido** confirmado de un chef (21 días de rack a $45/charola-semana no compiten por espacio en Fase 0–1).

**Reglas económicas para operar:**
- Cobrar con la lista corregida ($90–120 / $130–180); usar $60–80 SOLO como promoción de volumen de girasol. Los $60–90 del plan original destruyen el margen de todo lo demás.
- Presupuestar merma 8% global y registrar la real por especie en Home Assistant desde la charola #1 (fecha, g sembrados, g cosechados, incidencia). En 4 semanas tendrás tu propia tabla de rendimientos —mejor que cualquiera de estas fuentes— y sabrás tu multiplicador real de girasol/chícharo, el único dato que ninguna fuente pública midió.
- Descargar la guía gratuita de On The Grow (checkout de $0) para cerrar el gap de rendimientos por charola de girasol/chícharo con una 4ª fuente.
- Meta de mezcla Fase 1: 50% girasol + 50% finas (rábano/arúgula/amaranto) ⇒ ~$3,900/sem brutos con 30 charolas y costo variable ~21% — cumple y supera el objetivo del plan con margen para errores.

---

## Lo que falta verificar (gaps)
1. **Rendimiento medido de girasol y chícharo por charola 1020**: ninguna fuente abierta hoy lo publica con datos pesados (Johnny's no los incluyó en el trial; BF/TLM no publican yields; On The Grow lo tiene pero detrás de formulario). El rango 300–500 g (girasol) y 350–600 g (chícharo) es estimación de consenso — pesar las primeras 6 charolas.
2. **Merma % por especie**: no existe fuente pública cuantificada; los % de la tabla son supuestos de planeación.
3. **Color/variedad del amaranto nacional de HE** (¿verde o rojo?) y si su precio "fino" se sostiene en verde.
4. **Arvejón/chícharo entero grado alimento en CEDA** (precio y % de germinación) — condición para que el chícharo sea negocio.
5. **Gramaje de las bolsas de Hydrocultura** ($120–309) — cambia el costo de brócoli/amaranto rojo/finas.
6. **Si la semilla HE (forrajero girasol, cilantro Líder, etc.) viene sin tratamiento químico** — indispensable para consumo; preguntar por WhatsApp antes de comprar.
7. **Donny Greens**: inaccesible (Cloudflare) y aparentemente convertido en landing de cursos; no aportó datos.
8. **Precios de clamshell en Mercado Libre**: siguen siendo aprox. (bloqueo 403 al scraping).
9. **Importación de semilla de brassicas** (brócoli/rábano/arúgula a precio 25 lb de Johnny's/TLM, 4–8× más barata): viabilidad de permiso fitosanitario SENASICA y costo logístico — palanca de margen para Fase 2+.
10. Los PDFs de Johnny's citados son del trial 2017 (metodología sólida pero de una sola temporada, Maine, EUA; cosecha a primera hoja verdadera): los rendimientos en CDMX con cosecha más tardía pueden ser 10–30% mayores.
