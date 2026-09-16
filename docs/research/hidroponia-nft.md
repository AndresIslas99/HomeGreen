# Sistema NFT DIY en CDMX — Investigación de proveedores y costos
**Fecha de investigación: 12 de septiembre de 2026.** Precios en MXN; los marcados "aprox." vienen de snippets de búsqueda no verificados en la página. Los precios sin "aprox." fueron confirmados abriendo la página del producto (WebFetch o descarga directa del HTML con JSON-LD).

Contexto del plan (Fase 2): 6–8 líneas NFT en túnel de 25–30 m² para albahaca, hierbabuena, cilantro y arúgula. Presupuesto de fase: $35–55k MXN. La meta era validar el supuesto "~$350/línea DIY vs ~$1,500/línea comercial" — **se confirma, con matices** (ver más abajo).

---

### (a) Tubo PVC 4" y conexiones — la ruta DIY

Hallazgo clave: hay que distinguir **PVC sanitario** (pared delgada, sin presión, el estándar de facto para NFT DIY) de **PVC hidráulico cédula 40** (pared gruesa, 15.4 kg/cm² de presión — innecesario para NFT, que corre sin presión). La diferencia de precio es 3.4×:

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Tubo **sanitario** PVC 4" (11 cm) × 6 m, Amanco Wavin | **$415/tramo** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/amanco-wavin-tubo-sanitario-11-x-600-cm-blanco-amanco-942842-451963 | Blanco (mejor que naranja: refleja calor). $69/m |
| Tubo **hidráulico** PVC C-40 4" × 6 m, Cresco | **$1,401.28/tramo** (verificado) | Bricomark | https://bricomark.mx/producto/tubo-pvc-hidraulico-cedula-40-x-6-metros-de-4-15-40-kg-cm2-futura/ | Solo si se quisiera pared gruesa; no se necesita |
| Codo 90° PVC sanitario 4" Amanco | **$28.80** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/amanco-wavin-codo-pvc-4-513695-513695 | Para retorno al depósito |
| Codo 45° PVC sanitario 4" Amanco | **$18.31** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/amanco-wavin-codo-45-pvc-4-513766-513766 | |
| Tubos 4" × 6 m (varios vendedores) | $400–700 aprox | Mercado Libre (búsqueda) | https://listado.mercadolibre.com.mx/tubo-pvc-4-pulgadas-6-metros | Fichas volátiles; usar búsqueda |
| Categoría tubería sanitaria | — | Home Depot México | https://www.homedepot.com.mx/b/plomeria/tuberias-y-conexiones/sanitarias | También tienen 2" y 3" para retorno |

**Costo estimado por línea NFT DIY de 3 m** (½ tramo sanitario $208 + 2 tapas/caps ~$60 + adaptador de drenaje ~$40 + perforación de 9–10 hoyos de 2"–3" con broca sierra): **~$310–380/línea**. El supuesto del plan (~$350/línea) es correcto usando tubo **sanitario**, no hidráulico. Para 8 líneas de 3 m: 4 tramos ($1,660) + conexiones (~$600) ≈ **$2,300–2,800 total en PVC**.

Nota técnica: para albahaca/cilantro el tubo redondo de 4" funciona, pero el fondo curvo hace charco si el caudal es bajo; pendiente recomendada 2–3% y caudal 1–2 L/min por línea.

### (b) Canaletas NFT comerciales (comparación)

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Paquete Básico Sistema NFT (5 ductos + bomba + timer, ~25 plantas) | **$5,779** (verificado) | Hydro Environment (Tlalnepantla, Edomex — entrega toda la República) | https://hydroenv.com.mx/producto/paquete-basico-para-sistema-nft/ | ≈ $1,156/línea equipada → confirma el "~$1,500 comercial" del plan |
| Canaleta hidropónica por metro, 35 cm ancho (5×25×5 cm) | **$39.90/m** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/canaleta-hidroponica-por-metro-de-largo-35cm-de-ancho-5x25x5/ | Ojo: es canaleta abierta tipo charola (para bolsas/sustrato), no gully NFT cerrado; útil como cama de drenaje |
| Canaleta/ducto NFT "UL" PVC grado alimenticio | Cotización (la web muestra $0.00) | Hydrocultura | https://hydrocultura.com/products/canaleta-o-ductos-para-sistema-hidroponia-nft-ul | Tel +52 (55) 9435-6905; venden tapa riego, tapa drenaje y conector por separado |
| Canaleta NFT móvil MGS 100 mm × 37 mm (+riel 13 mm), PVC virgen | Cotización | Hydrocultura | https://hydrocultura.com/products/canaleta-o-ductos-para-sistema-hidroponico-nft-movil-mgs | Perfil rectangular profesional, el que usan lechugueros comerciales |
| Paquete completo NFT con medidores pH/EC | — (catálogo viejo) | Hydro Environment | https://hydroenv.com.mx/catalogo/index.php?main_page=product_info&products_id=140 | URL de catálogo antiguo. **[enlace muerto al 2026-09-16 — `tools/check_links.py`]** Buscar el paquete en el catálogo nuevo de hydroenv.com.mx. |

Conclusión (b): el DIY con PVC sanitario cuesta **~25–30% de lo comercial equipado**. La canaleta rectangular profesional (Hydrocultura) solo se justificaría si se escala a >20 líneas o se quiere trasplante/cosecha más rápida.

### (c) Bombas: periférica 0.5 HP vs sumergible

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Evans bomba periférica 0.5 HP, 20 L/min (BP1ME050) | **$799** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/evans-bomba-de-agua-periferica-05-hp-20-l-min-bp1me050-201712 | Marca sólida, refacciones fáciles |
| IUSA bomba periférica 0.5 HP, 30 L/min, 120 V (QB60) | **$599** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/iusa-bomba-de-agua-periferica-05-hp-30-l-min-120-v-qb60-203068 | La más barata verificada |
| Truper BOAP-1/2A2 periférica 0.5 HP (40 L/min, 40 m) | sin precio confirmado | Mercado Libre (ficha) | https://www.mercadolibre.com.mx/bomba-electrica-periferica-para-agua-truper-12-hp-periferica-127-v-60-hz-boap-12a2-color-negro/p/MLM16110430 | Búsqueda: https://listado.mercadolibre.com.mx/bomba-periferica-truper |
| Bomba sumergible 3000 LPH para hidroponía/estanques | **$1,299** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/bomba-sumergible-3000-lph-para-hidroponia-y-estanques/ | Línea completa: 600/1500/3000/4500/6500 LPH |
| Bomba sumergible 4500 LPH | **$1,199** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/bomba-sumergible-4500-lph-para-hidroponia-y-estanques/ | Hoy más barata que la de 3000 (probable promo) |
| Sumergible genérica 3000 L/h, 65 W, 3 m columna | $449–650 aprox | Mercado Libre | https://listado.mercadolibre.com.mx/bombas-sumergible-para-estanque | Tipo fuente/acuario; consumo 65 W vs ~370 W de la periférica |

**Análisis para 6–8 líneas NFT**: el caudal requerido es apenas 8–16 L/min con carga de 1.5–2 m. Una periférica de 0.5 HP (370 W) está sobredimensionada y gastaría ~$260/mes de luz corriendo 24/7 (tarifa doméstica CDMX escalón alto), mientras una sumergible de 65 W cuesta ~$45/mes. **Recomendación: sumergible 3000–4500 LPH como bomba principal 24/7** (las hierbas en NFT necesitan flujo continuo o ciclos muy cortos), y si se quiere redundancia, una segunda sumergible barata de ML en paralelo antes que una periférica. La periférica 0.5 HP del plan tiene más sentido para el traslado cisterna→tinaco o riego presurizado de las camas de Fase 3.

### (d) Filtro malla 120 y depósitos 200–450 L

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Filtro de malla 120 mesh 1", entrada/salida macho | **$230 lista / $189 con desc.** (JSON verificado $230; desc. aprox del snippet) | Hydro Environment | https://hydroenv.com.mx/producto/filtro-de-malla-para-riego-de-1-pulgada-con-salida-y-entrada-tipo-macho/ | Suficiente para NFT recirculante |
| Filtro malla 120 mesh 1¼" | — | RIEGOPRO | https://riegopro.com/filtros-para-riego-por-goteo/de-malla/filtro-de-malla-1-14 | Especialista en riego, envían a CDMX |
| Filtro 1" malla 120 mesh Palaplast | — | BASCOMEX | https://bascomex.com/products/filtro-de-1-pulgada-malla-palaplast-120-mesh | Marca griega Palaplast |
| Filtro malla 120 mesh 2" p/goteo | — | Amazon México | https://www.amazon.com.mx/Filtro-Malla-pulgadas-capacidad-filtraci%C3%B3n/dp/B0BTLG17Q2 | Vendedor MILCO |
| Filtros 120 mesh 1" (varios) | $150–350 aprox | Mercado Libre (búsqueda) | https://listado.mercadolibre.com.mx/filtro-para-agua-120-mesh-1-pulgada | |
| Tinaco Rotoplas Tricapa 450 L con accesorios | **$2,565** (verificado) | Home Depot México | https://www.homedepot.com.mx/p/rotoplas-tinaco-tricapa-450-l-con-accesorios-500023-133219 | Capa interior blanca antibacterial; opaco (clave: sin luz = sin algas) |
| Tambo HDPE 200 L grado alimenticio | $450–900 aprox | Mercado Libre (búsqueda) | https://listado.mercadolibre.com.mx/tambos-de-200-litros | La opción barata para el depósito NFT |
| Tambo abierto 200 L (A-55) | — | Plastank | https://www.plastank.mx/products/tambos-de-200-litros-abiertos | Fabricante MX, resinas USFDA |

**Recomendación (d)**: depósito de la solución NFT = **tambo HDPE 200 L grado alimenticio ($450–900)**, pintado de negro/envuelto o bajo sombra (el plan ya lo dice: aislado del sol). El tinaco 450 L Rotoplas se queda como reserva de agua cruda/captación pluvial, no como depósito de nutriente (200 L de solución bastan para 8 líneas × ~30 plantas y se renuevan cada 1–2 semanas).

### (e) Nutrientes hidropónicos en México — precio y rendimiento por m³

| Producto | Precio MXN | Rinde | **Costo por m³ de solución** | Proveedor / enlace |
|---|---|---|---|---|
| Solución Nutritiva p/ Hortalizas 1.5 kg (polvo, pH 6.2–6.3, CE 1.0–1.5) | **$349** (verificado) | 1,000 L | **~$349/m³** | Hydro Environment — https://hydroenv.com.mx/producto/solucion-nutritiva-para-hortalizas-de-1-5-kg-rinde-para-1000-litros/ |
| Ídem en costal 25 kg | **$3,359** (verificado) | ~16,600 L | **~$202/m³** | Hydro Environment — https://hydroenv.com.mx/producto/solucion-nutritiva-para-hidroponia-hortalizas-en-costal-de-25-kg/ |
| GHE/General Hydroponics Flora Series Trial Pack (Gro+Micro+Bloom) | **$1,600** (verificado) | ~200–400 L a dosis media | **~$4,000–8,000/m³** | Selva Grow Shop — https://shopselva.com/products/general-hydroponics-flora-series-mexico-grow-shop |
| Flora Series 1 galón c/u (trío) | **$3,300** (verificado) | ~1,500–2,500 L | **~$1,300–2,200/m³** | Selva Grow Shop (misma URL); también https://listado.mercadolibre.com.mx/general-hydroponics-flora-series |
| Hakaphos Violeta 13-40-13, 25 kg (Compo Expert) | $1,600 aprox | a 1 g/L → 25,000 L | **~$64/m³ (+Ca)** | Mercado Libre — https://listado.mercadolibre.com.mx/fertilizante-hakaphos-violeta ; distribuidor: https://aldase.com.mx/producto/hakaphos-violeta-13-40-13-25-kg/ |
| Nitrato de calcio soluble 25 kg | $850–1,485 aprox | a 0.8 g/L → 31,000 L | ~$27–48/m³ | Mercado Libre — https://listado.mercadolibre.com.mx/nitrato-calcio-25-kg |
| Nitrato de calcio 1 kg (para probar) | **$56.50** (verificado) | 1,250 L a 0.8 g/L | — | Hydro Environment — https://hydroenv.com.mx/producto/nitrato-de-calcio-para-plantas-1-kg/ |
| Nitrato de potasio 1 kg | **$119.90** (verificado) | — | — | Hydro Environment — https://hydroenv.com.mx/producto/nitrato-de-potasio-para-plantas-1-kg/ |

**Lectura del costo real**: con recirculación NFT y ~1–2 m³/mes de reposición (dato del plan), el gasto mensual de nutriente sería:
- Sales por separado (Hakaphos/genérico + nitrato de calcio): **~$90–150/mes** ← ganador en costo, requiere báscula y 2 tanques concentrados (A/B)
- Genérico Hydro Environment 25 kg: **~$200–400/mes** ← ganador en simplicidad/riesgo; ya viene balanceado para hortalizas de hoja
- Flora Series GHE: **$1,300–8,000/mes equivalente** ← queda descartado para producción; es producto de autocultivo boutique

Ojo con Hakaphos **Violeta** (13-40-13): es alto fósforo (floración). Para hoja/hierba conviene un Hakaphos de perfil vegetativo (Base/Verde) o la fórmula genérica de Hydro Environment; en cualquier caso el nitrato de calcio va SIEMPRE en tanque separado (B) porque precipita con fosfatos/sulfatos.

### (f) Germinación: espuma agrícola / lana de roca / peat pellets

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Semillero foami agrícola (espuma fenólica) 100 bloques 30×30 cm | **$67.90** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/semillero-de-foami-agricola-de-100-bloques-30x30-cm/ | **$0.68/planta** |
| Semillero foami 144 bloques 30×30 | **$45.50** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/semillero-de-foami-agricola-de-144-bloques-30x30-cm/ | **$0.32/planta** — el más barato |
| Semillero foami 196 bloques 30×30 | **$45.50** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/semillero-de-foami-agricola-de-196-bloques-30x30-cm/ | $0.23/planta, bloque chico |
| Cilindro foami 4.3×5 cm | **$2.90 c/u** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/cilindro-de-foami-agricola-de-4-3-x-5-cm/ | Para canastilla 3" |
| Categoría Peatfoam completa | — | Hydro Environment | https://hydroenv.com.mx/categoria-de-productos/sustratos-para-plantas/peatfoam/ | |
| Canastilla hidropónica 3" | **$12.80 c/u** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/canastilla-hidroponica-de-3-pulgadas/ | 8 líneas × 10 = 80 pzas ≈ $1,024 |
| Cubos lana de roca p/germinación (49 pzas) | precio en ficha volátil | Mercado Libre | https://listado.mercadolibre.com.mx/cubos-lana-de-roca-hidroponia | Grodan Plantop desde ~$18.6/cubo aprox |
| Espuma Oasis AeroMax 3.7 | — | Inverfarms | https://inverfarms.com/product/espuma-hidroponica-oasis-aero-max/ | Marca Oasis (Smithers), estándar de la industria |
| Cubo lana de roca 3×3×2.5 | — | Cultivarte | http://www.cultivarte.com.mx/producto/cubo-lana-de-roca-3x3x25 | Tienda CDMX. **[enlace muerto al 2026-09-16 — `tools/check_links.py`]** Cotizar por teléfono o usar Hydro Environment. |

**Recomendación (f)**: espuma fenólica nacional de Hydro Environment ($0.32–0.68/planta) para albahaca/arúgula; la lana de roca importada (Grodan) cuesta 5–20× más por planta y solo aporta ventaja en cultivos largos (jitomate). Peat pellets (Jiffy) no convienen en NFT: sueltan turba que tapa la malla 120 y ensucia la solución.

### (g) Calibración pH/EC — buffers y soluciones

| Producto | Precio MXN | Proveedor | Enlace | Notas |
|---|---|---|---|---|
| Solución estándar EC 1413 µS/cm, 500 mL (Hanna HI7031L) | **$459.36** (verificado, 1,404 pzas en stock) | Hanna Instruments México (tienda oficial, envío gratis >$2,552) | https://hannainst.com.mx/soluci%C3%B3n-de-calibraci%C3%B3n-de-ce-1-413-%C2%B5s-3-cm-valor-hi7031l | Caducidad 5 años cerrada |
| Buffer pH 4.01, 120 mL | **$40** (verificado) | Insumos Cerveceros (GDL, envían) | https://insumoscerveceros.mx/inicio/1305-solucion-para-calibracion-de-ph-buffer-401-120-ml.html | Baratísimo; comprar 2 |
| Kit buffers 4.01/7.00/10.01, 60 mL (Orion) | — | CTR Scientific (Monterrey, envían) | https://ctrscientific.com/products/14342-solucion-buffer-ph-4-01-ph-7-00-y-ph-10-01-60ml-p-calibracion-orion | Proveedor de laboratorio serio |
| Sobres de polvo buffer 4.01/6.86/9.18 | $10–40/sobre aprox | Mercado Libre (búsqueda) | https://listado.mercadolibre.com.mx/solucion-buffer-para-calibrar-ph | Los sobres 6.86 son el estándar chino que usan las sondas DFRobot |
| Solución EC 1413 (alternativas) | — | Equiglass | https://equiglass.com.mx/product/solucion-estandar-conductividad-1413-hanna-hi7031l/ | Distribuidor Hanna |
| Kit medición TDS/EC p/hidroponía | **$1,019.90** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/kit-de-medicion-tds-ec-para-hidroponia/ | Medidor de bolsillo + soluciones |
| AquAcid buffer para BAJAR pH (regulador hidroponía) | **$516** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/aquacid-buffer-para-bajar-ph-regulador-de-ph-para-hidroponia/ | Para la bomba peristáltica de pH− ; alternativa barata: ácido fosfórico/cítrico grado alimenticio |
| Monitor continuo pH/CE/TDS GroLine HI981420 (comercial) | **$15,669** (verificado) | Hydro Environment | https://hydroenv.com.mx/producto/medidor-continuo-ph-ce-tds-para-hidroponia-groline-hi981420/ | **Valida el plan**: el monitor comercial cuesta $15.7k vs ~$2–3k del stack ESP32+DFRobot |

Presupuesto anual de calibración (quincenal, según plan): 2 frascos pH 4.01 ($80) + sobres 6.86 (~$100) + 1 frasco EC 1413 Hanna ($459) ≈ **$650/año**, más sonda de repuesto (~$400) = **~$1,050/año**. Coincide con el "~$400/año + costo oculto" del plan; presupuestar $1,000–1,200/año es lo honesto.

---

### Costo total estimado del sistema NFT (8 líneas de 3 m, Fase 2)

| Partida | Costo MXN |
|---|---|
| PVC sanitario 4": 4 tramos + codos + tapas + pegamento | $2,300–2,800 |
| Estructura/soportes (PTR ya contemplado en túnel) | — |
| Bomba sumergible 4500 LPH Hydro Environment (o 2× genérica ML en paralelo) | $1,199 (o ~$900–1,300) |
| Filtro malla 120 1" | $189–230 |
| Tambo 200 L grado alimenticio (depósito solución) | $450–900 |
| Tubería de distribución ½"–¾" + retorno 2" + válvulas | $600–900 |
| 80 canastillas 3" | $1,024 |
| Semilleros foami (arranque, 300 plantas) | $150–200 |
| Nutriente arranque (1.5 kg × 2) | $698 |
| Buffers pH 4.0/6.86 + EC 1413 | $600–700 |
| **Total sistema NFT (sin túnel ni electrónica)** | **~$7,200–8,700** |

Contra $5,779 del paquete comercial de solo 5 ductos/25 plantas (sin depósito grande, sin filtro, sin 80 sitios), el DIY da **~3× la capacidad por un precio similar**. El supuesto del plan se sostiene.

### Recomendación concreta

1. **Comprar el PVC en Home Depot (sucursal CDMX) como tubo sanitario Amanco 4" blanco, $415/tramo** — no pagar cédula 40 ($1,401): NFT corre sin presión. 4 tramos + conexiones ≈ $2,800. Perforar con broca sierra de 3" (≈$150 en ML) a 20 cm entre centros.
2. **Bomba principal: sumergible 4500 LPH de Hydro Environment ($1,199)** o dos genéricas de 3000 L/h de ML (~$550 c/u) en paralelo para redundancia. Dejar la periférica 0.5 HP (IUSA $599 si se quiere) solo para trasiego/captación pluvial; a 370 W continuos, la periférica cuesta más de luz al año que su precio de compra.
3. **Depósito: tambo HDPE 200 L grado alimenticio de ML ($450–900), bajo sombra**, con el filtro malla 120 de 1" de Hydro Environment ($189–230) en el retorno, antes de la bomba.
4. **Nutriente: arrancar con la fórmula genérica de Hydro Environment 1.5 kg/$349 (rinde 1 m³)**; al pasar de ~2 m³/mes de consumo, migrar a costal 25 kg ($3,359, ~$202/m³) o a sales por separado (Hakaphos vegetativo + nitrato de calcio, ~$90–150/m³) cuando ya haya rutina de pesado A/B. **Descartar Flora Series GHE para producción** (10–40× el costo por m³; es producto de autocultivo).
5. **Germinación: espuma fenólica nacional (semillero 144 bloques, $45.50)** — $0.32/planta; nada de peat pellets en NFT (tapan el filtro).
6. **Calibración: buffer pH 4.01 de Insumos Cerveceros ($40/120 mL), sobres 6.86 de ML, y EC 1413 Hanna oficial ($459/500 mL)**. Presupuestar ~$1,000–1,200/año incluyendo sonda de repuesto — coincide con el "costo oculto" que el plan ya reconoce.
7. **Hacer una sola cotización a Hydrocultura (55 9435-6905)** por 8 canaletas MGS 100×37 mm para tener el precio comercial real por escrito; si sale <$700/línea instalada, reconsiderar en la ampliación (mejor manejo y limpieza que el tubo redondo), pero no detener la Fase 2 por ello.
8. **El monitoreo continuo comercial (GroLine HI981420) cuesta $15,669 confirmados** — el stack ESP32 + sondas DFRobot del plan (~$2–3k) queda validado como decisión económica correcta.

### Fuentes principales (verificadas hoy)
- Hydro Environment (hydroenv.com.mx) — Tlalnepantla, Edomex; envíos a toda la República; múltiples precios verificados vía JSON-LD de producto.
- Home Depot México (homedepot.com.mx) — precios verificados vía JSON-LD: tubo sanitario 4" $415, codo 4" $28.80, Evans 0.5 HP $799, IUSA 0.5 HP $599, tinaco Rotoplas 450 L $2,565.
- Bricomark (bricomark.mx) — tubo hidráulico C-40 4"×6 m $1,401.28 (verificado WebFetch).
- Selva Grow Shop (shopselva.com) — Flora Series $1,600 / $3,300 (verificado JSON de variantes Shopify).
- Hanna Instruments México (hannainst.com.mx) — HI7031L $459.36 (verificado WebFetch).
- Insumos Cerveceros (insumoscerveceros.mx) — buffer pH 4.01 $40 (verificado WebFetch).
- Hydrocultura (hydrocultura.com) — canaletas NFT profesionales, precio por cotización (verificado WebFetch).
- Mercado Libre México — URLs de búsqueda para fichas volátiles (tubos, tambos, bombas, buffers, Hakaphos, nitrato de calcio).
