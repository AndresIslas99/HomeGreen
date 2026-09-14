# Procedimiento de instalación del túnel (15–20 m²) sobre losa de patio en CDMX

**Fecha de investigación:** 12 de septiembre de 2026.
**Alcance:** anclaje sobre losa/firme de concreto, secuencia de armado paso a paso, mano de obra (herrero/albañil), manejo del agua de lluvia del techo, y tabla de lead times + ruta crítica de 4–6 semanas para la Fase 1.

**Nota metodológica:** el buscador web de la sesión estaba agotado, así que todo se verificó abriendo directamente los sitios (curl/WebFetch): Hydro Environment (guías + fichas de producto + tabla oficial de tiempos de entrega), Home Depot MX (búsquedas del sitio con precios extraídos del JSON de la página), Sodimac MX (ficha PTR + política de entregas), talent.com (salarios MX), hanlob.com.mx y rotoplas.com.mx. Los precios sin verificación directa están marcados "aprox.". Mercado Libre bloqueó el fetch (muro anti-bot): solo se dan URLs de búsqueda, sin precio.

---

### 1. Métodos de anclaje sobre losa de concreto, comparados

Contexto de viento: en CDMX las rachas de tormenta de mayo–septiembre alcanzan 50–80 km/h. A 80 km/h la presión dinámica es ~300 Pa; sobre un costado de túnel de 5 × 2.2 m (~11 m²) son ~330 kgf de empuje lateral, y la succión (levantamiento) sobre un techo curvo/dos aguas con plástico es del mismo orden (estimación propia, no es cálculo estructural). Moraleja: el problema no es el peso del túnel (~150–250 kg), es que el plástico trabaja como vela. La guía de Hydro Environment (que cita a Oklahoma State University) insiste exactamente en esto: "el anclaje debe evitar tanto el desplazamiento lateral como el levantamiento o volteo".

| Método | Qué es | Costo materiales (túnel 6 columnas) | Pros | Contras | Veredicto para rachas 50–80 km/h |
|---|---|---|---|---|---|
| **A. Placa base + anclas de cuña (taquete expansivo) 3/8"** | Placa de acero (10–15 cm, solera 3/16"–1/4") soldada al pie de cada columna, fijada con 4 anclas de cuña 3/8" × 5" a la losa | 24 anclas × $36 = **$864** (Home Depot) + placas/soldadura del herrero (~$400–800 aprox.) | El estándar; resiste tracción y cortante; desmontable (se destuercan); barato | Perfora la losa (sellar contra filtración); exige losa sana ≥10 cm y ≥15 cm al borde | **La opción recomendada.** Una ancla de cuña 3/8" bien colocada en concreto sano resiste cientos de kg a extracción; 4 por placa dan margen holgado |
| **B. Ancla de cuña 1/2"** | Igual que A pero con ancla 1/2" × 3-3/4" | 24 × $60 = **$1,440** (Home Depot) | Más capacidad; útil si la losa es de mala calidad o el túnel crece a 25–30 m² en Fase 2 | Broca y rotomartillo más grandes; sobredimensionado para 15–20 m² | Buena si planeas ampliar sobre las mismas bases |
| **C. Placas soldadas a elementos existentes** | Soldar la estructura a herrería existente (castillos con placa, barandal estructural) | Solo mano de obra del herrero | Sin perforar losa | Casi nunca hay puntos aprovechables en un patio; calidad desconocida del punto de apoyo | Solo como complemento (p. ej., amarrar una cabecera al muro con taquetes al muro) |
| **D. Contrapesos de concreto (sin perforar)** | Dados de concreto colados en cubeta de 19 L (~42 kg) o cimbra 40×40×25 cm (~85 kg) con el poste embebido o con espárrago | Saco de concreto premezclado 25 kg = $144 (rinde ~11–12 L). Dado de 40 L ≈ 3.5 sacos ≈ $500; 6 dados ≈ **$3,000** + cimbra | No perfora: única opción real en renta/condominio donde no autoricen barrenos; recuperable | Caro y pesado de mover; para resistir el volteo con rachas de 70–80 km/h los dados chicos NO bastan: se requieren ~80–100 kg por poste + cables a los 4 vientos; ocupa piso; la guía de Hydro Environment advierte no resolver el anclaje "únicamente aumentando el peso de las bases" | Aceptable solo con túnel bajo (≤2.2 m cumbrera), dados de ≥80 kg por poste, largueros bien triangulados y cortinas que se abren en tormenta. Plan B, no plan A |

Precios verificados hoy en Home Depot MX (búsqueda del sitio, MXN, IVA incluido):

| Producto (Home Depot MX) | Precio | Enlace |
|---|---|---|
| Ancla de expansión de cuña 3/8" × 5" (pieza) | $36 | https://www.homedepot.com.mx/s/ancla%20de%20cu%C3%B1a |
| Ancla de expansión de cuña 1/2" × 3-3/4" (pieza) | $60 | ídem |
| Ancla de expansión de cuña 1/4" × 2-1/4" (pieza) | $26 | ídem |
| Ancla de expansión de cuña 5/8" × 6" (pieza) | $128 | ídem |
| Taquete/anclaje expansivo de 3/8" (pieza) | $26 | https://www.homedepot.com.mx/s/taquete%20expansivo |
| Cemento Extra gris CEMEX 25 kg | $142 | https://www.homedepot.com.mx/s/cemento%20gris |
| Concreto premezclado listo para uso, saco 25 kg | $144 | ídem |

Reglas prácticas de anclaje (de la guía "Cómo hacer un invernadero para casa: patio, terraza o azotea" de Hydro Environment + práctica estándar):
- Antes de perforar, saber **qué hay bajo el acabado**: impermeabilización, tuberías o cableado. En patio a nivel de suelo el riesgo es bajo; aun así, sella cada ancla con sellador PU (Sikaflex) o silicón estructural.
- No anclar a menos de ~15 cm del borde de la losa ni en concreto agrietado.
- Las bases **no deben crear presas**: que no bloqueen la pendiente ni las coladeras del patio.
- Perforación: rotomartillo + broca de concreto del diámetro del ancla, profundidad = longitud de empotramiento + 1 cm; soplar/aspirar el polvo antes de meter el ancla (el polvo reduce la carga de extracción hasta a la mitad).
- Referencia técnica citada por la guía: para túneles con postes enterrados en tierra, OSU recomienda 60–90 cm de empotramiento; para cimentación permanente, concreto ≥2,500 psi (~17 MPa). Sobre losa, la combinación placa+ancla+concreto debe ser compatible con las cargas — no "cualquier tornillo en las 4 perforaciones".

### 2. Secuencia de armado paso a paso (túnel PTR 15–20 m², patio de concreto)

Fuentes reales de armado: guía de armado de microtúnel de Hydro Environment (piezas numeradas, 9 secciones), guía de invernadero casero patio/terraza/azotea (estructura desde cero) y guía "Paso a Paso: Instala Mallas y Plásticos al Invernadero" (perfil + zigzag), con video del propio proveedor (https://www.youtube.com/watch?v=kShJ07HwPDw, canal https://www.youtube.com/@HydroEnvironment01).

**Día 0 — Croquis y trazo (tú, 2–3 h)**
1. Croquis con: ancho/largo/altura, puerta, pasillos, racks, zonas de ventilación, ubicación del tinaco y de la coladera del patio (la guía de Hydro Environment trae esta lista textual).
2. Orientación: cumbrera a lo largo del eje del viento dominante si se puede; laterales de malla hacia donde corre el aire.
3. Trazo con hilo y escuadra 3-4-5; marcar los 6 (o 8) puntos de columna. Verificar planicidad con nivel de manguera o láser; los desniveles se corrigen con la placa/base, nunca rellenando la losa.

**Semana de taller — Fabricación (herrero, 2–4 días)**
4. Cortar PTR: columnas, arcos (rolados) o cabios a dos aguas, cumbrera, largueros laterales, travesaños de cabecera, poste central de puerta, diagonales.
5. Soldar placas base (solera con 4 barrenos 7/16" para ancla 3/8") al pie de columna; soldar orejas/conectores. Fondo anticorrosivo + esmalte (el patio moja la base: pintar bien los primeros 30 cm).

**Día de montaje 1 — Bases y esqueleto (herrero + tú, 1 día)**
6. Presentar pórticos, marcar barrenos por placa, perforar con rotomartillo, limpiar polvo, colocar anclas de cuña 3/8" × 5" y apretar a torque firme (llave de 9/16").
7. Levantar pórticos (2 personas mínimo, dice la guía del microtúnel), plomo y nivel en cada columna antes de apretar.
8. Largueros: laterales primero, luego el superior/cumbrera, **por la cara interior** para que ninguna arista roce el plástico (recomendación textual de la guía). Separación entre arcos/pórticos: 60–120 cm en estructuras ligeras; menos separación = plástico que no se pandea.
9. Travesaños de cabecera (uno bajo, uno alto), poste central y refuerzo del vano de puerta; diagonales/contravientos en esquinas (lo que realmente aguanta la racha).
10. Retocar pintura en soldaduras de campo; sellar el perímetro de cada placa con sellador PU.

**Día de montaje 2 — Cubiertas (3 personas, medio día; hacerlo al MEDIODÍA, con sol y SIN viento)**
11. Atornillar perfil sujetador (Polygrap/C-22) con autoperforantes **solo en tramos rectos**: largueros perimetrales, travesaños de cabecera y postes; nunca siguiendo la curva del arco. El canal hacia afuera; en el larguero bajo lateral, hacia adentro si ahí solo se fija malla (para dejar el plástico como cortina).
12. Pasar el lienzo de plástico UV **de una sola pieza** sobre los arcos (una persona arriba afuera, una adentro, una alimentando desde el suelo); sujetar provisionalmente las esquinas con tramos cortos de zigzag.
13. Centrar, tensar uniforme y fijar con alambre zigzag dentro del perfil. El truco térmico de la guía: tensar con calor de mediodía; al enfriar, el plástico se contrae y queda tenso.
14. Malla antigranizo sobre el techo (por fuera, con sujetadores o segundo zigzag) y malla antiáfidos fija por el interior de los laterales; el plástico lateral queda libre como cortina enrollable (grapas para cortina $29.90 c/u o malacate $529 si se quiere mecanizar).
15. Cabeceras y puerta (corrediza, abatible o traslape de malla con velcro/imanes — las 3 opciones vienen en la guía). Re-tensar todo al tercer día de sol y viento.

**Qué NO conviene hacer solo:** rolado de arcos, soldadura de placas y montaje de pórticos (herrero); subir/tensar el lienzo de plástico (mínimo 3 personas, la guía lo dice explícito); trabajar la cumbrera sin escalera estable. Sí puedes hacer solo: trazo, barrenos y anclas, perfil zigzag, canaleta, cortinas, pintura.

### 3. Mano de obra CDMX 2026

Verificado (salarios formales de mercado, talent.com, septiembre 2026, base nacional):

| Oficio | Mediana anual | Por hora | Jornada 8 h (calculada) | Fuente |
|---|---|---|---|---|
| Soldador | $100,800 | $51.69 | ~$410–415 | https://mx.talent.com/salary?job=soldador |
| Herrero | $86,400 | $44.31 | ~$355 | https://mx.talent.com/salary?job=herrero |
| Albañil | $67,200 | $34.46 | ~$275 | https://mx.talent.com/salary?job=alba%C3%B1il |

Lectura práctica: esos son sueldos de nómina. Un **herrero independiente por chamba en CDMX cobra la jornada con herramienta a $600–1,000/día aprox.** y suele cotizar la obra completa "material + mano de obra"; para una techumbre/túnel ligero de PTR de 15–20 m² el rango de mercado anda en **$1,000–1,800 por m² con material, o $8,000–15,000 solo mano de obra + fabricación aprox.** (no verificable en línea sin cotización: pídelas). Dónde pedir 3 cotizaciones reales: Habitissimo México (categoría albañiles/herrería: https://www.habitissimo.com.mx/presupuesto/albaniles), grupos de la alcaldía en Facebook Marketplace, y el herrero del barrio (el clásico "se hacen protecciones"). Presupuesto razonable para este proyecto: **2–4 días de herrero ($2,500–4,000 aprox.) + 1 día de ayudante ($300–400)** si tú compras todo el material y ayudas en el montaje.

Indeed bloqueó el fetch (403); Habitissimo no publica tarifario abierto por jornada — sus páginas son formularios de presupuesto. Queda como verificación humana.

### 4. Manejo del agua: canaleta del túnel → captación pluvial

- El techo del túnel de 15–20 m² capta ~15–20 L por cada mm de lluvia: una tormenta de 30 mm son ~500–600 L. **No lo dejes caer al patio**: canaleta en el alero hacia el tinaco ya presupuestado.
- **Canalón PVC blanco 3.07 m: $269 en Home Depot MX** (≈$88/m; búsqueda "canalon": https://www.homedepot.com.mx/s/canalon — aparecen "CANALÓN TRADICIONAL BLANCO 307 CM" y "CANALÓN BLANCO 306 × 11 × 5 CM", ambos $269). Para un túnel de 5 m a dos aguas: 2 tramos ($538) o 1 tramo si el techo es a un agua. Los accesorios (uniones, tapas, bajante redondo, soportes) existen en la misma línea pero la búsqueda del sitio los mezcla con canaleta eléctrica: verificar en tienda (aprox. $40–120 por pieza).
- Alternativa "de invernadero": canaleta galvanizada para invernadero de Hydro Environment, 3 m — $1,849 (https://hydroenv.com.mx/producto/canaleta-para-invernadero-canalon-3m-de-largo/). Es sobredimensionada y cara para 20 m²; el canalón PVC doméstico basta.
- Montaje: soportes atornillados al larguero bajo del alero, **pendiente ~1 cm por cada 2 m (0.5–1%)** hacia la bajante; bajante de PVC 3" o manguera reforzada al tinaco.
- Antes del tinaco: **filtro de hojas + separador de primeras lluvias** (un tramo vertical de 4" con tapón de registro abajo: los primeros 20–40 L, que lavan el polvo del techo, se purgan). El plan ya presupuestó filtro de sedimentos; esto lo complementa gratis.
- Tinaco: **450 L vertical $2,459 (oferta $2,215) y 450 L "equipado" $2,879 (oferta $2,565) en Home Depot** (https://www.homedepot.com.mx/s/tinaco%20450; la marca del listado no se pudo confirmar — verificar si es Rotoplas). Accesorios ahí mismo: brida 2.3" $48, multiconector 1½" $97. **Importante: el tinaco lleno pesa ~470 kg** — va sobre el piso del patio, nunca sobre estructura ligera, y con rebosadero dirigido a la coladera.
- El túnel debe respetar el drenaje existente del patio: no tapar coladeras con las placas ni con el tinaco (advertencia textual de la guía de Hydro Environment).

### 5. Lead times por proveedor y ruta crítica

Tiempos verificados hoy:

| Proveedor | Material | Tiempo verificado | Fuente |
|---|---|---|---|
| Sodimac MX | PTR (6 m): ¾"×¾" cal 14 $182 · 1½"×1½" cal 14 $403 · 2"×1" cal 14 $403 · 2"×2" cal 18 $431 | **Stock en tienda** (ficha muestra "Stock en tienda / Envío a domicilio / Retiro en un punto"); servicios de entrega mismo día / 24 h / 48 h / fecha programada; **flete gratis en compras >$1,000** | https://www.sodimac.com.mx/sodimac-mx/product/433713/ptr-1-1-2x1-1-2-calibre-14 · https://sodimac.com.mx/sodimac-mx/content/tipos-de-entrega/ |
| Home Depot MX | Anclas de cuña, cemento, canalón, tinaco 450 L | **Recoger en tienda ~24 h** después de la compra; envío a domicilio con fecha al momento del checkout; promoción de envío gratis en el sitio (con condiciones) | https://www.homedepot.com.mx/ayuda-tipos-entrega · https://www.homedepot.com.mx/condiciones-envios-linea |
| Hydro Environment (Tlalnepantla, Edomex) | Plástico UV por metro ($215/m en 6.2 m de ancho, cal 720; $299/m en 8.4 m), perfil Polygrap 2 m $95, zigzag $103/kg (~22.5 m), grapas cortina $29.90 | Menudeo: existencia — recoger en Av. Toltecas 41, Tlalnepantla (54030) o paquetería (días, aprox. 3–7 hábiles). **Tabla oficial de mayoreo:** malla antigranizo (≥10 rollos) 8–10 días hábiles; plástico blanco (≥15 rollos) 15–20; **invernaderos MiniGreen sobre pedido 8–15 días hábiles**; ductos NFT (≥300 m) 30–35 | https://hydroenv.com.mx/tiempos-de-entrega/ |
| Hydro Environment | Malla antigranizo rollo 200 × 3.7 m $4,799; anti-heladas por metro $17.90/m (1.8 m) | Rollo completo puede ser sobre pedido (8–10 días hábiles); por metro: existencia | https://hydroenv.com.mx/producto/rollo-de-malla-antigranizo-de-200-x-3-7-m/ |
| Rotoplas (tienda en línea) | Tinaco 450–750 L | "Envío GRATIS en toda la tienda"; el catálogo y la fecha exigen código postal (no verificable sin CP). El plan asume 10–15 días: **compra mejor el tinaco en Home Depot (24 h–7 días)** y quita a Rotoplas de la ruta crítica | https://rotoplas.com.mx/tinacos/ |
| Hanlob (hanlob.com.mx) | Malla sombra raschel 35–90 %, rollos y confeccionada | Tienda en línea activa, PERO **su catálogo público no muestra malla antigranizo** (solo malla sombra, ground cover, borde separador). Para antigranizo: Hydro Environment o Mercado Libre (búsqueda: https://listado.mercadolibre.com.mx/malla-antigranizo) | https://hanlob.com.mx/ |
| Herrero local | Fabricación + montaje | 3 cotizaciones: 2–5 días para cotizar; 2–6 días de fabricación; 1–2 días de montaje (aprox., depende de agenda) | Habitissimo: https://www.habitissimo.com.mx/presupuesto/albaniles |
| Kit alternativo (sin herrero) | Micro túnel 2 × 3.5 m $5,699.90 · Invernadero 2 × 3 m dos aguas $5,999.90 · Hydro Crop patio 2×3 m $15,915 · hidropónico 5×6 m $38,779 · Mini Green 6×6 m (36 m²) $59,999 | Kits chicos: existencia/8–15 días; armado DIY con manual de piezas numeradas (guía + video del proveedor) | https://hydroenv.com.mx/categoria-de-productos/Invernaderos/invernaderos-caseros/ |

**Ruta crítica Fase 1 (objetivo: 4 semanas; colchón: 6).** El camino crítico es HERRERO (cotizar+fabricar) — todo lo demás llega antes si se pide el día 1.

- **Semana 1:** croquis y medidas; pedir 3 cotizaciones de herrero (con foto del croquis); comprar PTR en Sodimac (retiro mismo día o flete 24–48 h, gratis >$1,000); comprar anclas + cemento + canalón en Home Depot (recoger en 24 h); encargar a Hydro Environment plástico UV por metro + perfil Polygrap + zigzag + malla antigranizo por metro (recoger en Tlalnepantla la misma semana, ~40 min desde el norte de CDMX; o paquetería 3–7 días). Pedir tinaco en Home Depot.
- **Semana 2:** herrero fabrica (placas, cortes, rolado/soldadura). Riesgo #1 de la ruta: si tarda >6 días, activar cotización 2. Mientras: recibes tinaco, armas base de tinaco y compras tornillería/autoperforantes.
- **Semana 3:** montaje del esqueleto + anclaje a losa (1–2 días con el herrero); pintura de retoque y sellado de placas; instalación de canaleta y bajante.
- **Semana 4:** plástico + mallas al mediodía sin viento (3 personas, medio día); cabeceras y puerta; re-tensado al tercer día; conexión de bajante al tinaco con purga de primeras lluvias; mudar racks adentro.
- **Semanas 5–6 (colchón):** lluvia vespertina de temporada (instalar cubiertas por la mañana), retraso del herrero, o malla antigranizo sobre pedido (8–10 días hábiles).

**Presupuesto de instalación (sin estructura PTR, ya cotizada en el informe de estructura):** anclas $864 + sellador ~$150 aprox. + perfil/zigzag para 20 m² (~14 tramos Polygrap $1,330 + 3 kg zigzag $309) + canaleta y bajante ~$700 aprox. + mano de obra herrero $2,500–4,000 aprox. ≈ **$6,000–7,500 MXN**.

### Recomendación concreta

1. **Ancla: placa base soldada + 4 anclas de cuña 3/8" × 5" por columna** ($36 c/u en Home Depot, ~$864 el túnel completo) con sellador PU sobre cada placa. Es la combinación más barata que aguanta rachas de 50–80 km/h. Contrapesos de concreto **solo** si el patio es rentado y no autorizan perforar: entonces dados de ≥80 kg por poste (~3.5 sacos de concreto de $144 c/u por dado) + cumbrera baja + cables a 4 vientos, aceptando que es inferior.
2. **Compra el PTR en Sodimac el día 1** (stock en tienda, flete gratis >$1,000) y **el plástico UV por metro ($215/m, 6.2 m de ancho) + perfil Polygrap ($95/2 m) + zigzag ($103/kg) directamente en Hydro Environment en Tlalnepantla** — es zona metropolitana: ir en coche elimina la paquetería de la ruta crítica. La malla antigranizo por metro/rollo ahí mismo (Hanlob NO la tiene en catálogo).
3. **Contrata al herrero solo para fabricar y montar el esqueleto (2–4 días, $2,500–4,000 aprox.)**; tú haces trazo, barrenos, anclas, perfil zigzag, plástico (con 2 ayudantes, al mediodía y sin viento, como manda la guía), canaleta y cortinas. Con eso la mano de obra no rebasa el 20 % del costo del túnel.
4. **Tinaco 450 L en Home Depot ($2,459, recoger en 24 h)** en lugar de esperar 10–15 días a Rotoplas en línea; canalón PVC de $269/3.07 m con pendiente 0.5–1 % y purga de primeras lluvias antes del tinaco.
5. **Sigue las tres guías de Hydro Environment** (armado de microtúnel, invernadero casero en patio, e instalación de mallas y plásticos) + su video (kShJ07HwPDw): son el manual de armado real más cercano a este proyecto, del mismo proveedor donde se compra el material, y gratis.
6. Si el gate comercial de Fase 0 pega antes de conseguir herrero, el **plan B sin herrero** es el kit micro túnel 2 × 3.5 m de $5,699.90 (piezas numeradas, armado en un día entre 2 personas) como puente, y el túnel de PTR se construye en Fase 2 con la ampliación a 25–30 m².

### Fuentes abiertas y verificadas hoy
- https://hydroenv.com.mx/como-hacer-un-invernadero-para-casa-patio-terraza-o-azotea/ (guía 33 min: anclaje patio/terraza/azotea, cargas, viento, zapatas, drenaje)
- https://hydroenv.com.mx/armado-de-invernadero-para-jardin-tipo-microtunel-de-3-5-x-2-x-2/ (armado por piezas numeradas, 9 secciones)
- https://hydroenv.com.mx/paso-a-paso-instala-mallas-y-plasticos-al-invernadero/ (perfil sujetador C-22 + zigzag, técnica de tensado al mediodía, 3 personas)
- https://hydroenv.com.mx/tiempos-de-entrega/ (tabla oficial de lead times)
- https://hydroenv.com.mx/producto/perfil-para-invernadero-polygrap-tramo-de-2-metros/ · https://hydroenv.com.mx/producto/alambre-zig-zag-para-invernadero-por-kilo-aprox-22-5-m/ · https://hydroenv.com.mx/producto/metro-de-plastico-para-invernadero-25-sombra-6-2-m-de-ancho-cal-720/ · https://hydroenv.com.mx/producto/rollo-de-malla-antigranizo-de-200-x-3-7-m/ · https://hydroenv.com.mx/categoria-de-productos/Invernaderos/invernaderos-caseros/
- https://www.homedepot.com.mx/s/ancla%20de%20cu%C3%B1a · /s/taquete%20expansivo · /s/canalon · /s/tinaco%20450 · /s/cemento%20gris · https://www.homedepot.com.mx/ayuda-tipos-entrega · https://www.homedepot.com.mx/condiciones-envios-linea
- https://www.sodimac.com.mx/sodimac-mx/search?Ntt=ptr · https://www.sodimac.com.mx/sodimac-mx/product/433713/ptr-1-1-2x1-1-2-calibre-14 · https://sodimac.com.mx/sodimac-mx/content/tipos-de-entrega/
- https://mx.talent.com/salary?job=soldador · ?job=herrero · ?job=alba%C3%B1il
- https://hanlob.com.mx/ · https://rotoplas.com.mx/tinacos/ · https://www.habitissimo.com.mx/presupuesto/albaniles
- Video de armado: https://www.youtube.com/watch?v=kShJ07HwPDw (canal https://www.youtube.com/@HydroEnvironment01)
