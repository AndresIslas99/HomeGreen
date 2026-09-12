# Proveedores CDMX — dónde comprar todo, con enlaces

Guía de compra curada por categoría: **la opción recomendada primero**, alternativas después.
Precios en MXN al 12-sep-2026; "aprox." = visto en resultados de búsqueda sin confirmar en la
ficha. El detalle completo (tablas de precios escalonados, teléfonos, análisis $/charola) está
en los informes de [`docs/research/`](research/) enlazados en cada sección. Las cantidades
exactas por fase están en los BOM: [`bom/fase0.csv`](../bom/fase0.csv) ·
[`bom/fase1.csv`](../bom/fase1.csv) · [`bom/fase2.csv`](../bom/fase2.csv).

## Los 8 proveedores núcleo del proyecto

| Proveedor | Qué comprarle | Por qué |
|---|---|---|
| [Hydro Environment](https://hydroenv.com.mx) (Tlalnepantla, envía a CDMX) | Semilla a granel, coco, plástico UV, malla sombra/antigranizo, canastillas, espuma agrícola, nutriente, bombas sumergibles, filtro malla | El proveedor hidropónico de referencia en México; guías técnicas gratis |
| [UNIT Electronics](https://uelectronics.com) | ESP32, sensores, relés, fuentes, ESP32-CAM | Lo más barato de México en electrónica maker; cubre ~70 % del BOM v1/v2 |
| [Home Depot MX](https://www.homedepot.com.mx) | Racks Husky, PVC sanitario 4", bombas Evans/IUSA, tinaco, herramienta Truper | Precios verificados en línea, recoger en sucursal el mismo día |
| [Mercado Libre](https://www.mercadolibre.com.mx) (filtrar "Full", vendedor 4.7★+) | Bombas de diafragma/peristálticas, solenoides, básculas, gabinetes IP65, sierra copa, clamshells, tambos 200 L | 30–50 % más barato en hidráulica y "cosas raras"; entrega al día siguiente |
| [Steren](https://www.steren.com.mx) (~15 sucursales CDMX) | Cautín, multímetro, dupont, termofit, fuente ELI-1260, termohigrómetro | Garantía nacional y sucursal física para emergencias |
| [AG Electrónica](https://agelectronica.com) (Rep. de El Salvador 20-F, Centro) | Cable, borneras, gabinetes, fusibles, Raspberry Pi 5, refacciones de emergencia | Mostrador con ingenieros; el "plan B mismo día" cuando algo truena en viernes |
| [Hydrocultura](https://hydrocultura.com) (CDMX, tel. 55 9435-6905) | Semilla específica microgreens (incl. finas), blocks de coco lavada, albahaca Nufar, canaletas NFT profesionales | El catálogo más completo de semilla para microgreens en México |
| [Isla Urbana](https://islaurbana.mx) (Coyoacán, tel. 55 5446-4831) | Tlaloque/kits de captación pluvial | El estándar de captación de lluvia en CDMX; manual de instalación gratuito |

---

## 1. Semilla, sustrato, charolas y empaque → [informe completo](research/semillas-sustrato-charolas.md)

| Insumo | Compra recomendada | Precio | Enlace |
|---|---|---|---|
| Girasol (volumen) | Prueba A/B: 1 kg CEDA + 1 kg específico microgreens; si CEDA germina ≥80 %, recompra en costal 5 kg | $34/kg (CEDA) vs $185/kg (específica) | [Mayoreo Online](https://mayoreo.online/products/semilla-de-girasol-con-cascara-jumbo) · [Al Natural](https://www.alnatural.com.mx/tienda/semilla-de-girasol-para-microgreens) |
| Chícharo | Granel Hydro Environment (confirmar "sin tratamiento") | ≈$340/kg (453+ g) | [ficha](https://hydroenv.com.mx/producto/gramo-de-semilla-de-chicharo-variedad-early-perfection/) |
| Rábano / betabel | Granel Hydro Environment, 250–500 g c/u | $4.00/g escalón 100–452 g | [catálogo granel](https://hydroenv.com.mx/categoria-de-productos/semillas-para-siembra-y-plantulas/semillas-de-hortalizas-a-granel/) |
| Brócoli | Hydrocultura (NO Hydroenv: $3,500/kg) | $201/bolsa (confirmar gramaje) | [colección](https://hydrocultura.com/collections/semillas-para-microgreens-o-microvegetales) |
| Finas (amaranto, mostaza, cilantro) | Sobres Hydrocultura o ISLA (CDMX, recoger) — solo muestras hasta que un chef las pida | $70–180/sobre | [Semillas ISLA](https://semillasisla.mx/collections/microgreens) |
| Fibra de coco | Polvillo germinación 50 L Hydroenv (~$2.10/charola); al escalar: tarima 20 blocks lavados Hydrocultura | $115/50 L · $159–175/block (mín. 20) | [polvillo](https://hydroenv.com.mx/producto/polvillo-de-coco-para-germinacion-50-l-sustrato-organico/) · [blocks](https://hydrocultura.com/products/blocks-de-fibra-de-coco-comprimidos-de-60-litros-lavada) |
| Charolas 10×20 (10 perforadas + 10 lisas) | Al Natural mayoreo por WhatsApp; comparar ML | $50–70/pza | [Al Natural](https://www.alnatural.com.mx/tienda/charolas-de-germinacion-venta-mayoreo) · [búsqueda ML](https://listado.mercadolibre.com.mx/charolas-para-microgreens) |
| Clamshells | 100 pzas PET 8 oz por ML para arrancar; al escalar, fabricante en Iztapalapa (Burbumoldes/Etesa) | ~$2.50–4.50/pza aprox. | [búsqueda](https://listado.mercadolibre.com.mx/clamshell) · [Burbumoldes](https://burbumoldes-blister.com/empaques-blister-clamshells.html) |
| Etiquetas | Tiraje chico 200–500 con imprenta CDMX | ~$400–800 aprox. | [Dushi](https://www.imprentacdmx.com/servicios-de-impresion/impresion-de-etiquetas-adhesivas/) · [Pop México](https://popmexico.com.mx/collections/etiquetas-adhesivas) |

**Costo variable por charola de girasol optimizado: $5.50–6.70** (semilla CEDA + coco + agua)
contra venta de $90–120 → margen bruto >90 %.

## 2. Estructura del túnel → [informe completo](research/estructura-invernadero.md)

Veredicto hacer-vs-comprar: **DIY con PTR sale en $550–750/m² vs $1,200–1,600/m² del
prefabricado serio** (y el prefabricado barato de ML no aguanta granizo). Túnel 3×6 m a dos
aguas ≈ **$10,700–15,300** todo incluido.

| Material | Compra recomendada | Precio | Enlace |
|---|---|---|---|
| PTR 1½"×1½" cal. 14 × 6 m | Sodimac (mejor precio en línea verificado); volumen: cotizar Aceros Crea | $403 ($382.85 en 5+) | [Sodimac](https://www.sodimac.com.mx/sodimac-mx/product/433713/ptr-1-1-2x1-1-2-calibre-14/433713) |
| Plástico UV cal. 720 | Blanco lechoso 25 % sombra, 6.2 m ancho, Hydroenv (especificación documentada); barato: corte 7.2×10 m invernaderosMX | $193.50–215/m · $1,100/corte | [Hydroenv](https://hydroenv.com.mx/producto/metro-de-plastico-para-invernadero-25-sombra-6-2-m-de-ancho-cal-720/) · [invernaderosMX](https://www.invernaderosmx.com/collections/plastico-5-transparente) |
| Malla antigranizo | Por metro (no rollo): Capi Agrícola $40/m (3.7 m ancho) o confección a medida ICAPSA/HTA | ~$1,400–1,600 para 40 m lineales | [Capi Agrícola](https://www.capiagricola.com.mx/product/malla-antigranizo-negra-3-70-m-x-metro/) · [ICAPSA](https://www.icapsa.com.mx/pagina-del-producto/malla-antigranizo) |
| Racks | Husky 5 niveles 183×91.4×45.7 cm, 362.9 kg/repisa (forrar entrepaños de MDF) | $2,019 c/u | [Home Depot](https://www.homedepot.com.mx/p/husky-estante-de-5-niveles-de-acero-183-x-914-x-457-cm-negro-zrop361872-5llb-150281) |

⚠️ **Corrección al plan original:** el proveedor "Hunab" no existe — es **Hanlob** (mallas,
Querétaro, [hanlob.com.mx](https://hanlob.com.mx/)). Y el presupuesto de racks era irreal:
$2,000–2,600/rack real, no $1,200–1,800 (esos son racks de 30–50 kg/nivel que se oxidan).

## 3. Electrónica y automatización → [informe completo](research/electronica-automatizacion.md)

Estrategia: **un pedido grande a UNIT** (ESP32, sensores, relés, TDS, ESP32-CAM),
**hidráulica por Mercado Libre Full** (diafragma, peristálticas, solenoides NC),
**pack ×10 de capacitivos por Amazon** (20–30 % vienen malos), **una ida al Centro** (AG,
Salvador 20-F) por gabinetes/cable/borneras y para conocer al proveedor de emergencia.

| Componente clave | Recomendado | Precio | Enlace |
|---|---|---|---|
| ESP32 DevKit ×2–3 | UNIT | ~$126–139 c/u aprox. | [ficha](https://uelectronics.com/producto/esp32-devkit-v1-30-pines-usb-c-microusb/) |
| Fuente 12 V 5 A crítica | Steren ELI-1260 (garantía) o Mean Well IP67 (intemperie, UNIT) | $399 · [IP67](https://uelectronics.com/producto/xlg-75-12-a-fuente-conmutada-12v-5a-ip67-mean-well/) | [Steren](https://www.steren.com.mx/eliminador-regulado-de-12-vcc-5-a.html) |
| Cerebro | Mini PC ThinkCentre usado i5/8GB (ML, mejor para HA+Grafana+Frigate) o Pi 5 4GB Cyberpuerta | $2,500–3,500 aprox. · $3,069 | [búsqueda ML](https://listado.mercadolibre.com.mx/mini-pc-lenovo-thinkcentre) · [Cyberpuerta](https://www.cyberpuerta.mx/Placas-de-Desarrollo-Raspberry/) |
| Sonda pH | Dos etapas: PH-4502C ($329) para desarrollar el lazo; kit DFRobot Gravity ($1,250 Geek Factory) cuando el NFT venda | $329 → $1,250 | [UNIT](https://uelectronics.com/producto/sensor-de-ph-liquido/) · [Geek Factory](https://www.geekfactory.mx/producto/kit-sensor-de-ph-para-arduino-gravity-dfrobot/) |
| EC/TDS | SEN0244 (UNIT) o Keyestudio (Amazon) | $300–550 aprox. | [UNIT](https://uelectronics.com/producto/sensor-tds-meter-v1-0-analogico-sen0244/) |
| Peristálticas ×4 (1 repuesto) | Mercado Libre | $145–280 c/u aprox. | [búsqueda](https://listado.mercadolibre.com.mx/bomba-peristaltica-12v) |
| Dato de contexto | El monitor pH/EC comercial (GroLine HI981420) cuesta **$15,669** — el stack DIY (~$2–3k) queda validado | | [ficha](https://hydroenv.com.mx/producto/medidor-continuo-ph-ce-tds-para-hidroponia-groline-hi981420/) |

Subtotales realistas: **v1 $3,500–5,500 · v2 $2,600–4,600** (dentro del plan).

## 4. NFT e hidroponia → [informe completo](research/hidroponia-nft.md)

⚠️ **Corrección técnica importante:** usar tubo **PVC sanitario** 4" ($415/tramo Amanco en
Home Depot), NO hidráulico cédula 40 ($1,401) — el NFT corre sin presión, la diferencia es
3.4×. Y la **bomba principal del NFT debe ser sumergible** (65 W, ~$45/mes de luz), no la
periférica 0.5 HP del plan (370 W ≈ $260/mes): la periférica queda para trasiego.

| Partida | Recomendado | Precio | Enlace |
|---|---|---|---|
| Tubo sanitario 4" ×4 tramos + conexiones | Home Depot (Amanco blanco) | ≈$2,300–2,800 | [tubo](https://www.homedepot.com.mx/p/amanco-wavin-tubo-sanitario-11-x-600-cm-blanco-amanco-942842-451963) |
| Bomba | Sumergible 4500 LPH Hydroenv (o 2 genéricas ML en paralelo) | $1,199 | [ficha](https://hydroenv.com.mx/producto/bomba-sumergible-4500-lph-para-hidroponia-y-estanques/) |
| Depósito solución | Tambo HDPE 200 L grado alimenticio, bajo sombra | $450–900 aprox. | [búsqueda](https://listado.mercadolibre.com.mx/tambos-de-200-litros) |
| Filtro malla 120 1" | Hydroenv, en el retorno antes de la bomba | $189–230 | [ficha](https://hydroenv.com.mx/producto/filtro-de-malla-para-riego-de-1-pulgada-con-salida-y-entrada-tipo-macho/) |
| Nutriente | Fórmula genérica Hydroenv 1.5 kg ($349/m³); al escalar: costal 25 kg ($202/m³) o sales A/B (~$90–150/m³). **Descartar Flora Series GHE** (10–40× el costo) | $349 arranque | [ficha](https://hydroenv.com.mx/producto/solucion-nutritiva-para-hortalizas-de-1-5-kg-rinde-para-1000-litros/) |
| Germinación | Espuma fenólica nacional 144 bloques ($0.32/planta); nada de peat pellets (tapan el filtro) | $45.50 | [ficha](https://hydroenv.com.mx/producto/semillero-de-foami-agricola-de-144-bloques-30x30-cm/) |
| Canastillas 3" ×80 | Hydroenv | $12.80 c/u | [ficha](https://hydroenv.com.mx/producto/canastilla-hidroponica-de-3-pulgadas/) |
| Calibración | Buffer pH 4.01 ($40, Insumos Cerveceros) + sobres 6.86 (ML) + EC 1413 Hanna ($459) | ~$1,050/año con sonda de repuesto | [buffer](https://insumoscerveceros.mx/inicio/1305-solucion-para-calibracion-de-ph-buffer-401-120-ml.html) · [Hanna](https://hannainst.com.mx/soluci%C3%B3n-de-calibraci%C3%B3n-de-ce-1-413-%C2%B5s-3-cm-valor-hi7031l) |
| Semilla albahaca | **Nufar** (resistente a fusarium — el riesgo #3 del plan) + Genovese/Italian Large Leaf | $549/oz · $21.50/g | [Hydrocultura](https://hydrocultura.com/products/nufar-semillas-organicas-de-albahaca) · [Hydroenv](https://hydroenv.com.mx/producto/1811-gramo-de-semilla-albahaca-var-italian-large-leaf/) |

Sistema NFT completo 8 líneas (sin túnel ni electrónica): **~$7,200–8,700** — 3× la capacidad
del paquete comercial de $5,779 con 5 ductos.

## 5. Agua → [informe completo](research/agua-captacion.md)

| Partida | Recomendado | Precio | Enlace |
|---|---|---|---|
| Tinaco | Rotoplas Resistec 750 L (mejor $/litro); alcaldía con tandeo duro: Plus+ 1,100 L | $2,051 · $3,774 | [rotoplas.com.mx](https://rotoplas.com.mx/products/almacenamiento/tinacos/) |
| Captación Fase 1 | DIY: canaleta + separador de primeras lluvias casero (PVC 4", ~$500) + filtro de hojas | ~$1,200–1,800 | [manual Tláloc PDF gratis](https://www.engineeringforchange.org/wp-content/uploads/2020/07/MANUAL-INSTALACI%C3%93N-KIT-TL%C3%81LOC-12-JUNIO-2019CH.pdf) |
| Captación Fase 2 | Paquete Básico Tláloc Isla Urbana (tlaloque + filtro hojas + axolote) | $5,300 | [ficha](https://islaurbana.mx/product/paquete-basico-tlaloc/) |
| Anticloro (línea NFT) | Dúplex sedimento 5 µm + carbón activado 10" | ~$800–1,200 | [Agua Limpia](https://www.agualimpia.mx/collections/filtro-para-sedimento-y-carbon-activado) |
| **Gratis** | Programa Cosecha de Lluvia SEDEMA (enero–febrero, si la alcaldía califica): sistema de ~$20k sin costo | $0 | [programa](https://www.sedema.cdmx.gob.mx/programas/programa/cosecha-de-lluvia) · programascall@sedema.cdmx.gob.mx |

## 6. Fitosanitario y clima → [informe completo](research/clima-agronomia.md)

Botiquín completo por ~$600: **jabón potásico** 1 kg ($250,
[Soluciones Naturales Pro](https://solucionesnaturalespro.com.mx/product/jabon-potasico/)) +
**trampas amarillas** (~$150, [ML](https://listado.mercadolibre.com.mx/trampas-amarillas-pegajosas)) +
**H2O2 35 % grado alimenticio** 1 L (~$200, [ML](https://listado.mercadolibre.com.mx/peroxido-de-hidrogeno-35%25-grado-alimenticio-oxigeno-liquido)).
Comprar **Gnatrol DG (Bti)** (~$700–900, [Valent](http://www.valent.mx/productos/insecticidas/gnatrol))
ANTES de la primera temporada de lluvias — cuando la mosca fungosa aparece ya vas tarde.
Iluminación: **tubos T8 18 W 6500K estándar ($121 c/u, [JWJ](https://jwjlight.mx/producto/tubo-led-t8-18w-120-cm/))**
— no pagar "grow lights" para un cultivo de 10 días. Tapete térmico (~$300–450 aprox.,
[ML](https://listado.mercadolibre.com.mx/tapete-termico-germinacion)) para germinar dic–feb.
Malla sombra 35 % ($129/m, [Hydroenv](https://hydroenv.com.mx/producto/malla-sombra-por-metro-al-35-de-3-7-m-de-ancho/))
solo marzo–mayo.

## 7. Mercado y precios de venta → [informe completo](research/mercado-precios.md)

El mercado CDMX existe y está poco servido: MIJARDIIN vende clamshells a $100–110/50–60 g
(~$2,000/kg) con suscripciones; Arca Tierra surte >40 restaurantes; no hay líder B2B de
microgreens. **Correcciones a la hoja de precios del plan:**

| Producto | Plan decía | Precio real defendible |
|---|---|---|
| Charola viva girasol/chícharo (restaurante) | $60–90 | **$90–120 lista** ($70–80 volumen 4+/sem; $60–90 solo promo primer mes) |
| Charola viva variedades finas | — | **$130–180** |
| Microgreens cortados | $250–450/kg | **$500–900/kg** ($50–90 por clamshell 100 g) — el plan estaba 2–3× barato |
| Hierbas Fase 2 | $250–450/kg | Cotizar **por manojo: $20–35 B2B premium** (contra CEDA a ~$8–15/manojo no se compite por precio, se compite por frescura y trazabilidad) |

Canales a sumar: **suscripción semanal a hogares** (modelo MIJARDIIN, $260/sem × 10 hogares ≈
$10k/mes extra) y **Mercado el 100** (Roma Sur, domingos —
[solicitar ingreso](https://mercadoel100.org/contacto/)). Logística: ruta propia 2 días
fijos/semana; [DiDi Entrega Light](https://dplnews.com/didi-lanza-servicio-de-entrega-para-pequenos-paquetes-desde-29-pesos-en-mexico/)
(desde $29) para reposiciones. Pedido mínimo sugerido: $350.
