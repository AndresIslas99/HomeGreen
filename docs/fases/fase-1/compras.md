# Comprar los materiales de la Fase 1

**En una línea:** la lista exacta de [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv)
agrupada por la semana en que la ruta crítica la necesita — todo lo de estructura y agua el
**día 1 de la S7**, la electrónica en la S8, racks, luces y fitosanitario en la S12 — con un
pedido por proveedor y la decisión herrero vs DIY tomada antes de comprar una sola herramienta.

!!! info "Antes de empezar"
    - **Tiempo:** S7: 1 mañana de pedidos en línea + 1 ida a Sodimac/Home Depot + 1 ida en coche a Hydro Environment (Tlalnepantla, ~40 min desde el norte de CDMX) · S8: 2 h de pedidos + 1 ida al Centro (AG Electrónica) · S12: 1 h · **Costo:** **$41,634** ([BOM](../../referencia/bom.md)), de los cuales $4,559 son la seguridad eléctrica de la S13; $40,244 en versión austera · **Personas:** 1 (+ coche o flete para el PTR y el plástico)
    - **Necesitas:** el gate [G0→1](../fase-0/gate.md) pasado; las 3 cotizaciones de herrero pedidas con foto del croquis; tarjeta o SPEI; dónde recibir 15 tramos de PTR de 6 m y un lienzo de plástico de 8 × 6.2 m.
    - **Prerequisitos:** [Antes de gastar un peso](../../empieza-aqui/antes-de-gastar-un-peso.md) — decisión ① (¿se puede perforar la losa? si no, contrapesos de ≥ 80 kg por poste) y ④ (tinaco 750 L o 1,100 L según tandeo); [Estructura del túnel](../../diseno/estructura-tunel.md) para la lista de cortes que le das al herrero.

## Reglas antes de pedir

1. **Nada se compra antes de G0→1.** La pérdida acotada de la Fase 0 es ~$6–9k; la de esta
   fase es ~$38k. El plan es "vender antes de construir"
   ([00 §filosofía](../../referencia/00-plan-maestro.md)).
2. **El día 1 de la S7 se compra todo lo de estructura, cubierta y agua**, aunque el herrero
   no haya empezado: el camino crítico es él, y todo lo demás llega antes si se pide ese día.
   PTR en Sodimac tiene **stock en tienda** y flete gratis en compras > $1,000; anclas, canalón
   y tinaco en Home Depot se **recogen en ~24 h**; plástico, perfil, zigzag y malla se recogen
   en persona en Hydro Environment (Av. Toltecas 41, Tlalnepantla) para sacar la paquetería
   (3–7 días hábiles) de la ruta crítica
   ([research/instalacion-tunel-detalle §5](../../research/instalacion-tunel-detalle.md)).
3. **El tinaco sale de la ruta crítica.** El Resistec 750 L de $2,051 se pide en rotoplas.com.mx
   con envío gratis, pero la fecha exige código postal y el plan asume 10–15 días: pídelo el
   día 1. Si en 10 días no hay fecha, el plan B es Home Depot (recoger en 24 h): Tricapa 750 L
   con accesorios $3,549 o 450 L $2,459.
4. **UNIT Electronics: confirma cada precio en el carrito.** Su web bloquea bots; los precios
   del CSV son de resultados de búsqueda ("aprox.")
   ([research/electronica-automatizacion](../../research/electronica-automatizacion.md)).
5. **Sensores capacitivos: pack × 10, no piezas sueltas.** Entre 20 y 30 % salen malos o
   descalibrados; con 10 tienes los 4 que van al rack, 2 de calibración cruzada y repuestos.
6. **DS18B20 × 3 y ESP32 × 3.** Son el sensor que más se maltrata y la placa que más se quema
   por un cable mal puesto; el tercero es el repuesto de viernes en la noche.
7. **Nada de "grow lights".** T8 18 W 6500 K de $121; el cultivo dura 10 días.
8. **Gnatrol (Bti) se compra ANTES de la primera temporada de lluvias con producción.** Cuando
   aparece la mosca fungosa ya vas tarde ([02 §1](../../referencia/02-restricciones-y-requisitos.md)).
9. **La malla sombra 35 % solo se monta marzo–mayo.** Si tu S12 cae fuera de esos meses, no la
   compres todavía (se quita el resto del año: la albahaca de Fase 2 necesita luz para aroma).
10. **La seguridad eléctrica no está en `bom/fase1.csv`.** Breaker GFCI QO120GFI $1,159,
    tapa intemperie + varilla copperweld + cable cal. 8 ~$900 y electricista ~$2,500
    (**+$4,559**) están en `bom/fase2.csv`, pero [03 §1.3](../../referencia/03-instalacion.md)
    los exige **antes del primer relé en el patio**: van en la S13 de esta fase
    ([automatización v1 §3](automatizacion-v1.md)).

## Decisión previa: herrero o DIY

La estructura de PTR se corta, rola y suelda. Decide esto antes de comprar herramienta, porque
cambia ~$850 del BOM y 2–4 días de tu tiempo.

=== "Herrero (recomendado)"

    Contrátalo **solo para fabricar y montar el esqueleto** (cortes, placas soldadas, pintura de
    fondo, levantar pórticos). Tú haces trazo, barrenos y anclas, perfil zigzag, plástico (con
    2 ayudantes), canaleta y cortinas. Así la mano de obra no rebasa el 20 % del costo del túnel.

    | Concepto | Número | Fuente |
    |---|---|---|
    | Jornada de herrero independiente con herramienta | $600–1,000/día aprox. (el BOM anota $200–400/día como estimado del plan: pide 3 cotizaciones y usa el número real) | [research/instalacion-tunel-detalle §3](../../research/instalacion-tunel-detalle.md) · [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv) |
    | Fabricación + montaje del túnel 3 × 6 m | **2–4 días, $2,500–4,000 aprox.** + 1 día de ayudante $300–400 | ídem |
    | Renglón del BOM "soldadura o herrero + primario + tornillería" | $2,000 aprox. | `bom/fase1.csv` |
    | Herramienta que **no** compras | esmeriladora $629 + careta ~$200 = **~$850 ahorrados** | [04-herramientas](../../referencia/04-herramientas.md) |
    | Dónde pedir las 3 cotizaciones | herrero del barrio ("se hacen protecciones"), [Habitissimo](https://www.habitissimo.com.mx/presupuesto/albaniles), grupos de la alcaldía en Facebook Marketplace | research §3 |

    *Criterio de listo:* 3 números por escrito con fecha de entrega; una cotización aceptada el
    día 1 de la S7 y la segunda guardada por si la fabricación pasa de 6 días de lo pactado.

=== "DIY: soldar tú"

    Solo si ya sueldas. El PTR se compra igual; agregas esmeriladora angular 4½" 700 W ($629
    aprox., [Home Depot](https://www.homedepot.com.mx/p/truper-esmeriladora-angular-41-2-700-w-profesional-truper-esma-4-1-2a12-207858)),
    discos de corte (~$25–40 c/u), careta (~$100–250) y una soldadora
    [POR VERIFICAR: no hay precio de soldadora en los informes; cotizar inversor de electrodo
    en Home Depot o tlapalería y sumar electrodos y careta de soldar]. Lo que **no conviene
    hacer solo** aunque sueldes: rolar arcos y levantar pórticos (mínimo 2 personas).

    Ahorras los $2,500–4,000 del herrero y gastas ~$850 + soldadora; pierdes 2–4 días propios y
    la garantía de que el esqueleto esté a plomo. La guía
    [Estructura del túnel §lista de cortes](../../diseno/estructura-tunel.md) es tu plano.

=== "Plan B sin herrero: kit"

    Si llegas a la S13 sin esqueleto (2 semanas de retraso), el puente es el
    [kit micro túnel 2 × 3.5 m de Hydro Environment](https://hydroenv.com.mx/categoria-de-productos/Invernaderos/invernaderos-caseros/)
    ($5,699.90, piezas numeradas, armado en un día entre 2 personas; sobre pedido 8–15 días
    hábiles). El túnel de PTR se construye entonces en la Fase 2 con la ampliación a 5 × 6 m
    ([Línea de tiempo → si se retrasa el herrero](../../empieza-aqui/linea-de-tiempo.md)).

## Lista de compra por semana

Precios en MXN al 12-sep-2026 tal como están en `bom/fase1.csv`. **Estado:** `verificado` =
ficha abierta ese día; `aprox.` = visto en búsqueda o snippet. Los renglones sin enlace se
compran en tienda física.

=== "S7 · día 1: estructura, cubierta y agua (≈ $19,500)"

    Lo que el herrero y el túnel necesitan. Se compra **todo el mismo día** que aceptas la
    cotización.

    | Categoría | Artículo | Cant. | Precio unit. | Subtotal | Estado | Proveedor | Notas |
    |---|---|---|---|---|---|---|---|
    | Estructura | [PTR 1½" × 1½" cal. 14 × 6 m](https://www.sodimac.com.mx/sodimac-mx/product/433713/ptr-1-1-2x1-1-2-calibre-14/433713) | 15 | $382.85 (5+ pzas; $403 suelto) | $5,743 | verificado | Sodimac (stock en tienda; flete gratis > $1,000) / Aceros Crea por volumen | Túnel 3 × 6 m a dos aguas; pedir al herrero empalmes de la fachada sur atornillados para crecer a 5 × 6 m |
    | Estructura | [PTR 1" largueros y contravientos](https://www.sodimac.com.mx/sodimac-mx/category/cat11448/PTR) | 4 | $275 | $1,100 | aprox. | Sodimac / tlapalería | [Estructura del túnel](../../diseno/estructura-tunel.md) calcula 7 tramos reales con kerf: [POR VERIFICAR al cotizar: subir a 7 tramos o hacer los tirantes en redondo liso] |
    | Estructura | Soldadura o herrero + primario anticorrosivo + tornillería | 1 | $2,000 | $2,000 | aprox. | herrero local / tlapalería | Ver decisión de arriba; el rango real del herrero es $2,500–4,000 |
    | Estructura | [Anclaje: placas 10 × 10 cm (solera 3/16") + anclas de cuña 3/8"](https://www.homedepot.com.mx/s/taquete) | 6 postes | $180 | $1,100 | aprox. | Home Depot (recoger en 24 h) / tlapalería | El procedimiento usa **ancla de cuña 3/8" × 5" a $36 c/u, 4 por placa = 24 = $864** ([research/instalacion-tunel-detalle §1](../../research/instalacion-tunel-detalle.md)); las placas las suelda el herrero. **NUNCA sin anclar** |
    | Cubierta | [Plástico UV cal. 720 blanco lechoso 25 % sombra, 6.2 m de ancho](https://hydroenv.com.mx/producto/metro-de-plastico-para-invernadero-25-sombra-6-2-m-de-ancho-cal-720/) | 8 m | $215/m ($193.50 con descuento en línea) | $1,720 | verificado | Hydro Environment (recoger en Tlalnepantla) | Un solo lienzo: 6 m de túnel + 1 m por cabecera. Alternativa a mitad de precio: corte 7.2 × 10 m de [invernaderosMX](https://www.invernaderosmx.com/collections/plastico-5-transparente) $1,100 (transparente 5 %; confirmar espesor y garantía UV) |
    | Cubierta | [Malla antigranizo 3.7 m de ancho, por metro](https://www.capiagricola.com.mx/product/malla-antigranizo-negra-3-70-m-x-metro/) | 40 m | $40/m | $1,600 | verificado | Capi Agrícola | Va 10–20 cm **SOBRE** el plástico; instalada antes de mayo y no se quita temprano (pico estadístico: agosto). Hanlob **no** la vende; el rollo de 200 m de Hydroenv ($4,799) es sobre pedido 8–10 días hábiles |
    | Cubierta | [Perfil Polygrap + alambre zigzag + cinta reparadora + canaleta PVC](https://hydroenv.com.mx/plastico-para-invernadero-y-campo/) | 1 | $1,100 | $1,100 | aprox. | Hydroenv (perfil $95/2 m, zigzag $103/kg ≈ 22.5 m) / Home Depot (canalón PVC blanco $269/3.07 m) | Para 20 m²: ~14 tramos de perfil ($1,330) + 3 kg de zigzag ($309) según el informe; el canalón nace con la estructura |
    | Agua | [Tinaco Rotoplas Resistec 750 L](https://rotoplas.com.mx/products/almacenamiento/tinacos/) | 1 | $2,051 | $2,051 | verificado | rotoplas.com.mx (envío gratis; fecha exige CP) | Alcaldía con tandeo duro (Tlalpan, Iztapalapa, Xochimilco, Tláhuac, Milpa Alta): Plus+ 1,100 L $3,774. Opaco o a la sombra; base firme (lleno ≈ 750 kg). Plan B en 24 h: Home Depot |
    | Agua | [Captación pluvial DIY: canaleta + tlaloque casero PVC 4" + filtro de hojas](https://www.engineeringforchange.org/wp-content/uploads/2020/07/MANUAL-INSTALACI%C3%93N-KIT-TL%C3%81LOC-12-JUNIO-2019CH.pdf) | 1 | $1,500 | $1,500 | aprox. | tlapalería / Home Depot | Manual oficial gratis (PDF). En Fase 2 se reemplaza por el Paquete Básico Tláloc ($5,300). Aplicar a Cosecha de Lluvia en enero–febrero |
    | Herramientas | Rotomartillo ½" 650 W ($660) + brocas ($215 aprox.) + taquetes + niveles + escuadra, flexómetro, pinzas | 1 | $1,600 | $1,600 | aprox. | Home Depot / tlapalería de barrio (Truper 10–20 % más barato) | Detalle en [04-herramientas §Fase 1](../../referencia/04-herramientas.md). Si suelda el herrero: sin esmeriladora ni careta |
    | | **Subtotal S7** | | | **≈ $19,514** | | | |

    !!! tip "Qué llevas a Tlalnepantla"
        Una sola ida a Hydro Environment cubre plástico (8 m), perfil Polygrap, zigzag y, si
        prefieres, la malla antigranizo por metro. Pide en mostrador sus tres guías gratis
        (armado de microtúnel, invernadero casero en patio, instalación de mallas y plásticos):
        son el manual de armado real del proyecto ([túnel](tunel.md)).

=== "S8: electrónica y cerebro (≈ $8,400)"

    Se pide mientras el herrero fabrica; llega en 1–3 días y se arma en la mesa en la S12.

    | Categoría | Artículo | Cant. | Precio unit. | Subtotal | Estado | Proveedor | Notas |
    |---|---|---|---|---|---|---|---|
    | Automatización | [ESP32 DevKit V1 30 pines (USB-C / micro USB)](https://uelectronics.com/producto/esp32-devkit-v1-30-pines-usb-c-microusb/) | 3 | $130 | $390 | aprox. | UNIT Electronics | 2 nodos + 1 repuesto; pedir la variante USB-C; confirmar en carrito |
    | Automatización | [SHT31 temperatura / humedad ambiente](https://articulo.mercadolibre.com.mx/MLM-2050379399-modulo-de-sensor-de-humedad-sht31-temperatura-sht31-d-microc-_JM) | 2 | $300 | $600 | aprox. | Mercado Libre | Upgrade sobre DHT22: no deriva con HR alta sostenida del túnel. Recorte: DHT22 ~$90–130 en UNIT |
    | Automatización | [DS18B20 sumergible](https://uelectronics.com/producto/ds18b20-sensor-de-temperatura-digital-de-acero-inoxidable-sumergible/) | 3 | $35 | $105 | aprox. | UNIT Electronics | El sensor que más se maltrata |
    | Automatización | [Sensor capacitivo de humedad de sustrato v1.2, pack × 10](https://www.amazon.com.mx/GalaxyElec-capacitivo-resistente-corrosi%C3%B3n-anal%C3%B3gico/dp/B082HV1JMG) | 1 | $300 | $300 | aprox. | Amazon MX | 20–30 % salen malos; sellar el borde de la PCB con esmalte; conector hacia arriba |
    | Automatización | [Módulo relé 4 canales optoacoplado 5 V](https://uelectronics.com/producto/relevador-5v-de-1-a-8-canales/) | 2 | $110 | $220 | aprox. | UNIT Electronics | Riego + ventilador + luces (vía relé de potencia) + reserva; el segundo es repuesto |
    | Automatización | [Fuente 12 V 5 A Steren ELI-1260](https://www.steren.com.mx/eliminador-regulado-de-12-vcc-5-a.html) | 1 | $399 | $399 | verificado | Steren (sucursal) | Circuito crítico con garantía nacional; para intemperie: [Mean Well IP67 XLG-75-12-A](https://uelectronics.com/producto/xlg-75-12-a-fuente-conmutada-12v-5a-ip67-mean-well/) en UNIT |
    | Automatización | [Bomba de diafragma 12 V con presostato](https://listado.mercadolibre.com.mx/bomba-de-agua-diafragma-12v) | 1 | $350 | $350 | aprox. | Mercado Libre (Full) | Da presión para nebulizar; 4–6 L/min |
    | Automatización | [Kit nebulizadores / microaspersores](https://listado.mercadolibre.com.mx/nebulizadores-de-riego) | 1 | $250 | $250 | aprox. | Mercado Libre | 10–30 boquillas con manguera; 2 por nivel N1–N4 |
    | Automatización | [JSN-SR04T nivel de tinaco](https://uelectronics.com/producto/sensor-ultrasonico-jns-sr04t/) | 1 | $150 | $150 | aprox. | UNIT Electronics | Zona muerta ~20 cm sobre el nivel máximo |
    | Automatización | [Cerebro: mini PC ThinkCentre usado i5 / 8 GB / SSD](https://listado.mercadolibre.com.mx/mini-pc-lenovo-thinkcentre) | 1 | $3,000 | $3,000 | aprox. | Mercado Libre | Alternativa: [Pi 5 4 GB $3,069 verificado en Cyberpuerta](https://www.cyberpuerta.mx/Placas-de-Desarrollo-Raspberry/); recorte: Pi 5 2 GB $1,879. El mini PC rinde más para HA + Grafana + Frigate |
    | Automatización | [UPS chico para el cerebro y el router](https://listado.mercadolibre.com.mx/no-break-500va) | 1 | $900 | $900 | aprox. | ML / Cyberpuerta | Sin internet no hay alarmas; el DataShield DS-600 (600 VA) cuesta $1,189 verificado |
    | Automatización | [Gabinete IP65 ~300 × 300 × 90 mm + prensaestopas](https://listado.mercadolibre.com.mx/gabinete-plastico-exterior-ip65) | 2 | $350 | $700 | aprox. | Mercado Libre | Gabinete A (127 V CA) y gabinete B (12 V CC) separados ([Eléctrico](../../diseno/electrico.md)) |
    | Automatización | [Material de soporte: cable, borneras, fusibles y portafusibles, buck LM2596, termofit, cinchos](https://agelectronica.com) | 1 | $1,000 | $1,000 | aprox. | AG Electrónica (Rep. de El Salvador 20-F, Centro; L–V 9–19 h, sáb 10–17 h) | Comprar en persona: piezas de $5–50 donde el envío duplica el costo. De paso conoces al proveedor de emergencia mismo día |
    | | **Subtotal S8** | | | **≈ $8,364** | | | |

    !!! warning "No está en el CSV y lo vas a necesitar en la S13"
        Breaker GFCI Square D QO120GFI **$1,159** (o contacto GFCI Square D $389 como mínimo),
        tapa intemperie "in-use" + varilla copperweld 5/8" × 3 m + cable cal. 8 **~$900**, y
        medio día de electricista certificado **~$2,500** (rango $1,500–3,500 llave en mano con
        tierra ≤ 25 Ω medidos). Están en `bom/fase2.csv` como "seguridad"; súmalos aquí:
        **+$4,559** ([automatización v1 §3](automatizacion-v1.md)).

=== "S12: racks, luces, clima y fitosanitario (≈ $9,400)"

    Se compra cuando el túnel está cerrado: nada de esto sirve antes y todo se recoge en 24 h
    o llega con Full.

    | Categoría | Artículo | Cant. | Precio unit. | Subtotal | Estado | Proveedor | Notas |
    |---|---|---|---|---|---|---|---|
    | Racks | [Estante Husky 5 niveles 183 × 91.4 × 45.7 cm (362.9 kg/repisa)](https://www.homedepot.com.mx/p/husky-estante-de-5-niveles-de-acero-183-x-914-x-457-cm-negro-zrop361872-5llb-150281) | 3 | $2,019 | $6,057 | verificado | Home Depot MX | El rack de Fase 0 se muda al túnel. Con 3 nuevos tienes 4 (los "3–4 racks" del informe); el recorte del CSV compra 2 y deja 3 en el túnel, como dibuja el layout. Forrar entrepaños de MDF con plástico o charola |
    | Iluminación | [Tubo LED T8 18 W 120 cm 6500 K](https://jwjlight.mx/producto/tubo-led-t8-18w-120-cm/) | 8 | $121 | $968 | verificado | JWJ Light | 2 por nivel N1–N4, 12–14 h/día; + canaletas y cable ~$400 (no en el CSV) |
    | Clima | [Tapete térmico de germinación](https://listado.mercadolibre.com.mx/tapete-termico-germinacion) | 1 | $380 | $380 | aprox. | Mercado Libre | Solo dic–feb (germinar a 22 °C); se automatiza con el relé K4 |
    | Clima | [Malla sombra 35 %, 3.7 m de ancho](https://hydroenv.com.mx/producto/malla-sombra-por-metro-al-35-de-3-7-m-de-ancho/) | 6 m | $129/m | $774 | verificado | Hydro Environment | **SOLO marzo–mayo** (UV extremo); comprar en la ida de la S7 si tu S12 cae en esos meses |
    | Fitosanitario | [Jabón potásico 1 kg](https://solucionesnaturalespro.com.mx/product/jabon-potasico/) | 1 | $250 | $250 | verificado | Soluciones Naturales Pro | Pulgón, mosca blanca, trips: 10–15 mL/L al envés |
    | Fitosanitario | [Trampas amarillas pegajosas](https://listado.mercadolibre.com.mx/trampas-amarillas-pegajosas) | 1 paquete | $150 | $150 | aprox. | Mercado Libre | 1 por rack; el indicador temprano más barato |
    | Fitosanitario | [Gnatrol DG (Bti) 500 g](http://www.valent.mx/productos/insecticidas/gnatrol) | 1 | $800 | $800 | aprox. | Valent / ML | Antes de la primera temporada de lluvias (mosca fungosa) |
    | | **Subtotal S12** | | | **≈ $9,379** | | | |

## La versión recortada (~$31,000)

El propio CSV la define: **2 racks en vez de 3** (−$2,019) y **DHT22 en vez de SHT31**
(−~$400). Otros recortes que los informes respaldan, en orden de menor riesgo:

| Recorte | Ahorro | Qué pierdes | Fuente |
|---|---|---|---|
| Plástico transparente 5 % de invernaderosMX (corte 7.2 × 10 m) | ~$620 | La especificación pentacapa documentada y el 25 % de sombra (baja 3–5 °C el pico de mediodía); confirma espesor y garantía UV antes | [research/estructura-invernadero §c](../../research/estructura-invernadero.md) |
| Pi 5 2 GB ($1,879) en vez de mini PC | ~$1,100 | Margen para Grafana/Frigate después | [research/electronica-automatizacion §2](../../research/electronica-automatizacion.md) |
| Contacto GFCI Square D ($389) en vez del breaker QO120GFI ($1,159) | $770 | Protege solo lo que cuelga de ese contacto; todo el patio debe colgar de él | [research/electrico-respaldo-seguridad §3.6](../../research/electrico-respaldo-seguridad.md) |
| Fuente UNIT 12 V 5 A ($139–154) en vez de Steren ELI-1260 | ~$250 | Garantía nacional en el circuito que alimenta la bomba 24/7. No recomendado | ídem §2 |

Lo que **no** se recorta: anclaje, malla antigranizo, GFCI + tierra, gabinetes IP65.

## Un pedido por proveedor

1. **Sodimac** (S7, día 1; en tienda o en línea con flete gratis > $1,000): 15 tramos PTR 1½"
   cal. 14 ($5,743 a precio de 5+) + 4–7 tramos PTR 1" (~$1,100). Si Aceros Crea (tel. 55 5888
   9272) cotiza 10–15 % abajo por volumen, úsalo, pero no a costa de días.
2. **Home Depot** (S7, día 1, recoger en 24 h): 24 anclas de cuña 3/8" × 5" ($36 c/u = $864),
   2–4 tramos de canalón PVC blanco 3.07 m ($269 c/u) + uniones, tapas, bajante y soportes
   (~$40–120 c/u, verificar en tienda), sellador PU, rotomartillo Truper 650 W ($660), brocas.
   En S12: 2–3 racks Husky ($2,019 c/u).
3. **Hydro Environment** (S7, ida a Tlalnepantla; tel. 55 5565-1153): plástico 8 m × 6.2 m
   ($1,720), ~14 tramos de perfil Polygrap ($95/2 m), 3 kg de zigzag ($103/kg), grapas para
   cortina ($29.90 c/u); si toca, malla sombra 35 % 6 m ($774).
4. **Capi Agrícola** (S7, en línea): 40 m de malla antigranizo 3.7 m ($1,600).
5. **Rotoplas** (S7, día 1, en línea con CP): Resistec 750 L ($2,051) o Plus+ 1,100 L ($3,774).
6. **UNIT Electronics** (S8, un solo pedido, 1–3 días): 3 ESP32, 3 DS18B20, 2 relés 4 ch,
   JSN-SR04T (+ DHT22 si recortas). Subtotal ≈ $865 aprox.; confirmar en carrito.
7. **Mercado Libre** (S8, filtrar **Full** y vendedor 4.7★+): 2 SHT31, bomba diafragma 12 V,
   kit nebulizadores, 2 gabinetes IP65, mini PC ThinkCentre usado, UPS. En S12: tapete térmico,
   trampas amarillas, Gnatrol si Valent no vende directo.
8. **Amazon MX** (S8): pack × 10 capacitivos ($300).
9. **Steren** (S8, sucursal): fuente ELI-1260 ($399) y, si te falta, cautín, multímetro,
   protoboard, dupont, termofit ([04-herramientas](../../referencia/04-herramientas.md)).
10. **AG Electrónica** (S8, en persona, Rep. de El Salvador 20-F): cable, borneras, fusibles y
    portafusibles, buck LM2596, diodo Schottky 1N5822, capacitores, cinchos (~$1,000).
11. **JWJ Light** (S12): 8 tubos T8 18 W ($968). **Soluciones Naturales Pro** (S12): jabón
    potásico ($250). **Valent / ML** (S12): Gnatrol DG 500 g (~$800).

!!! warning "Error típico"
    Comprar la electrónica en la S7 "para adelantar" y la malla antigranizo "después, cuando
    llegue mayo". Es al revés: la electrónica llega en 3 días cualquier semana; la malla por
    rollo es sobre pedido (8–10 días hábiles) y el pico de granizo es agosto, pero la temporada
    activa arranca en mayo. Y nunca "ahorrar" quitando anclas: el túnel sin anclar es el que
    sale volando.

## Al terminar

- [ ] 3 cotizaciones de herrero recibidas, 1 aceptada con fecha de entrega por escrito (S7, día 1)
- [ ] PTR, anclas, canalón, sellador y rotomartillo en tu patio; plástico, perfil, zigzag y malla recogidos en Tlalnepantla (S7)
- [ ] Tinaco con fecha de entrega confirmada (o plan B de Home Depot activado a los 10 días)
- [ ] Pedido único a UNIT confirmado en carrito; ML/Amazon/Steren/AG completos (S8)
- [ ] Partida de seguridad eléctrica (+$4,559) apartada para la S13
- [ ] `bom/fase1.csv` actualizado con cada precio real pagado (`estado_precio` = verificado + fecha) — [cómo corregir un precio](../../empieza-aqui/como-usar-esta-guia.md)
- Registrar: issue "Compras Fase 1" con esta lista de tareas; el total pagado va al issue del gate
- Siguiente paso: [Construir y anclar el túnel](tunel.md)

## Fuentes

- [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv) · [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv) (seguridad eléctrica)
- [01-proveedores CDMX §2, §3, §5, §6](../../referencia/01-proveedores-cdmx.md) · [04-herramientas §Fase 1](../../referencia/04-herramientas.md)
- [research/instalacion-tunel-detalle §1, §3, §5](../../research/instalacion-tunel-detalle.md) · [research/estructura-invernadero](../../research/estructura-invernadero.md)
- [research/electronica-automatizacion §2, §4, §5](../../research/electronica-automatizacion.md) · [research/agua-captacion §a](../../research/agua-captacion.md)
- [research/electrico-respaldo-seguridad §3.6, §3.8](../../research/electrico-respaldo-seguridad.md) · [research/herramientas](../../research/herramientas.md)
