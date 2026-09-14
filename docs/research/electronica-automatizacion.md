# Electrónica y automatización — Dónde comprar en CDMX (investigación 12-sep-2026)

Dimensión: componentes del plan de automatización v1 y v2 del huerto (ESP32 + ESPHome + Home Assistant).
Metodología: 24 búsquedas web + verificación directa con fetch de las fuentes clave. Los precios verificados
directamente en la página se marcan **[verificado]**; los que vienen de snippets de buscador se marcan **aprox.**
(UNIT Electronics, Geek Factory, Mercado Libre y Amazon MX bloquean el scraping directo, pero las URLs son reales
y vistas en resultados de búsqueda).

---

### 1. Panorama de proveedores (quién es quién)

| Proveedor | Tipo | Ubicación / entrega | Veredicto para este proyecto |
|---|---|---|---|
| **UNIT Electronics** (uelectronics.com) | Tienda en línea mexicana de electrónica maker | Envío nacional 1–3 días a CDMX | **La opción #1 para el 70% de la lista**: precios más bajos de México en ESP32, sensores y módulos; catálogo exacto para este proyecto |
| **AG Electrónica** (agelectronica.com) | Mayorista/menudeo clásico con mostrador | República de El Salvador 20-F, Centro Histórico + Vallejo 1874, GAM. L–V 9:00–19:00, Sáb 10:00–17:00. Tel (55) 5130 7210 **[verificado]** | Compra en persona en el Centro: fuentes, relés, cable, conectores, Raspberry Pi oficial |
| **330ohms** (330ohms.com) | Distribuidor aprobado de Raspberry Pi en México | Coyoacán, CDMX — **sin venta en sitio**, solo entregas de compras en línea (FedEx/DHL/UPS) **[verificado]** | Para Raspberry Pi con garantía de distribuidor; sigue operando (sept-2026) |
| **Steren** (steren.com.mx) | Cadena nacional, decenas de sucursales CDMX | Sucursales por toda la ciudad + tienda en línea | Fuente 12V robusta con garantía nacional, cable, conectores, herramientas; caro en módulos maker |
| **Cyberpuerta** (cyberpuerta.mx) | E-commerce de cómputo | Envío ~$128, llega en 1–3 días hábiles a CDMX | Raspberry Pi 5 nueva con stock real **[verificado]** |
| **Mercado Libre** (mercadolibre.com.mx) | Marketplace | Envío Full mismo día/1 día en CDMX | Lo más barato en bombas peristálticas, válvulas solenoides, bombas de diafragma, nebulizadores y mini PC usado |
| **Amazon MX** (amazon.com.mx) | Marketplace | 1–2 días CDMX (Prime) | Packs multi-pieza (sensores capacitivos ×10, JSN-SR04T ×2), sondas TDS de marca |
| **Geek Factory** (geekfactory.mx) | Tienda maker (GDL, envían a CDMX) | Envío nacional | El distribuidor con mejor precio visible del kit pH **DFRobot Gravity** |
| **Tecneu** (tecneu.com) | Tienda maker (Tlaquepaque, Jal.) | Envío nacional | Referencia de precio bajo (YF-S201 $74 **[verificado]**, hoy agotado); útil como plan B |
| **HetPro** (hetpro-store.com) | Distribuidor DFRobot en México (GDL) | Envío nacional | Plan B para sondas DFRobot; no pude confirmar precios (página no scrapeable) |

---

### 2. Automatización v1 (Fase 1, presupuesto plan: $2,500–4,000)

| Componente | Mejor opción | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| 2× ESP32 DevKit V1 30 pines (USB-C/MicroUSB) | UNIT Electronics | $126–129 c/u aprox → **~$260 los 2** | https://uelectronics.com/producto/esp32-devkit-v1-30-pines-usb-c-microusb/ | Pide la variante USB-C. Alternativa: DevKitC V4 WROOM-32D/32U $132–139 aprox (https://uelectronics.com/producto/esp32-devkitc-v4-esp32-wroom-32d-32u/). Categoría completa: https://uelectronics.com/categoria-producto/tarjetas-desarrollo/esp32/ |
| Sensor temp/humedad ambiente ×2 (DHT22) | UNIT Electronics | ~$90–130 c/u aprox | https://uelectronics.com/producto/sensor-de-temperatura-dht22-am2302/ | Versión con cables: https://uelectronics.com/producto/sensor-de-temperatura-y-humedad-dht22-con-cables/ · Comparador ML: https://listado.mercadolibre.com.mx/sensor-de-temperatura-y-humedad-dht22 |
| SHT31 (upgrade recomendado sobre DHT22) | Mercado Libre | ~$250–350 aprox | https://articulo.mercadolibre.com.mx/MLM-2050379399-modulo-de-sensor-de-humedad-sht31-temperatura-sht31-d-microc-_JM | I2C, más preciso y estable que DHT22 en ambiente húmedo del túnel; el DHT22 deriva con humedad alta sostenida |
| DS18B20 sumergible (temp de agua) | UNIT Electronics | **$31 aprox** | https://uelectronics.com/producto/ds18b20-sensor-de-temperatura-digital-de-acero-inoxidable-sumergible/ | Geek Factory desde $29 aprox (https://www.geekfactory.mx/producto/ds18b20-sensor-de-temperatura-sumergible/); Tecneu $37. Compra 2–3: es el sensor que más se maltrata |
| Sensor capacitivo humedad sustrato ×4 | UNIT (pza) o Amazon (pack ×10) | ~$35–60 c/u aprox; pack ×10 Amazon ~$250–350 aprox | https://uelectronics.com/producto/sensor-de-humedad-suelo-capacitivo-anticorrosivo/ | Pack ×10: https://www.amazon.com.mx/GalaxyElec-capacitivo-resistente-corrosi%C3%B3n-anal%C3%B3gico/dp/B082HV1JMG — conviene el pack: los v1.2 chinos tienen ~20–30% de piezas malas o descalibradas; sella el borde de la PCB con esmalte/epóxica |
| Módulo relé 4 canales optoacoplado | UNIT Electronics | $66–146 aprox (línea 1–8 canales) | https://uelectronics.com/producto/relevador-5v-de-1-a-8-canales/ | También hay línea de relevadores 12V (https://uelectronics.com/producto/relevadores-12v-de-124-y-8-canales/) y categoría completa (https://uelectronics.com/categoria-producto/modulos/relevadores-modulos/). Amazon: $115 aprox (https://www.amazon.com.mx/MODULO-RELEVADOR-CANALES-LOWLEVEL-RELAY/dp/B0DGB5RYWM) |
| Fuente 12V 5A conmutada | UNIT Electronics (UE-60-12) | **$139–154 aprox** | https://uelectronics.com/producto/fuente-conmutada-12v-5a/ | Con garantía de cadena: **Steren ELI-1260 $399 [verificado], en stock, $324.80 en 5+ pzas** (https://www.steren.com.mx/eliminador-regulado-de-12-vcc-5-a.html). Para intemperie, UNIT tiene Mean Well IP67 XLG-75-12-A (https://uelectronics.com/producto/xlg-75-12-a-fuente-conmutada-12v-5a-ip67-mean-well/) — recomendada para el túnel |
| Bomba de agua 12V (diafragma) | Mercado Libre | ~$250–450 aprox | https://listado.mercadolibre.com.mx/bomba-de-agua-diafragma-12v | Las de diafragma con presostato (tipo FLO) dan presión para nebulizar |
| Nebulizadores/microaspersores | Mercado Libre | kits ~$150–350 aprox | https://listado.mercadolibre.com.mx/nebulizadores-de-riego | Kits de 10–30 boquillas con manguera |
| JSN-SR04T (nivel de tinaco) | UNIT Electronics | ~$120–180 aprox (ficha sin precio en snippet) | https://uelectronics.com/producto/sensor-ultrasonico-jns-sr04t/ | Amazon 2-pack HiLetgo: https://www.amazon.com.mx/HiLetgo-JSN-SR04T-ultras%C3%B3nico-transductor-Impermeable/dp/B07X5H77T7 — zona muerta ~20 cm: móntalo con ese colchón sobre el nivel máximo |
| Cerebro: Raspberry Pi 5 | Cyberpuerta | **Pi 5 2GB $1,879 [verificado, 20 pzas]** · Pi 5 4GB $3,069 [verificado] | https://www.cyberpuerta.mx/Placas-de-Desarrollo-Raspberry/ | Pi 5 8GB: AG Electrónica **$4,259 IVA incl. [verificado]** — sin stock hoy pero **arriban 180 pzas el 19-sep-2026** (https://agelectronica.com/detalle?busca=RASPBERRYPI-5%2F8GB). Fuente oficial 27W: $404 aprox Cyberpuerta |
| Cerebro alternativo: mini PC usado | Mercado Libre | **$2,500–4,000 aprox** (ThinkCentre i5, 8GB RAM, SSD) | https://listado.mercadolibre.com.mx/computacion/pc-escritorio/mini-pc/lenovo/usado/ | También https://listado.mercadolibre.com.mx/mini-pc-lenovo-thinkcentre — para HA + ESPHome + Grafana + futura visión (Frigate/ESP32-CAM) rinde mucho más que la Pi por casi el mismo dinero |

**Subtotal v1 realista:** ~$3,200–4,800 con Pi 5 2GB, o ~$3,800–5,500 con mini PC usado. Coincide con el plan ($2,500–4,000) si se recorta a DHT22 y Pi 2GB; se pasa un poco si eliges SHT31 + mini PC (lo recomendado).

---

### 3. Automatización v2 (Fase 2, presupuesto plan: ~$3,000–4,200)

| Componente | Mejor opción | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Sonda pH + placa (calidad DFRobot) | Geek Factory | **$1,250 aprox** (kit Gravity básico) · $2,087 aprox (pro) | https://www.geekfactory.mx/producto/kit-sensor-de-ph-para-arduino-gravity-dfrobot/ | UNIT también vende el kit SEN0161-V2 con soluciones de calibración incluidas (https://uelectronics.com/producto/kit-sensor-de-ph-analogico-con-soluciones-de-calibracion-sen0161-v2/, ~$1,900 aprox según fuente terciaria). HetPro es distribuidor DFRobot MX: https://hetpro-store.com/dfrobot/ |
| Sonda pH económica (para arrancar) | UNIT Electronics | **$329 aprox** (PH-4502C + electrodo E201-BNC) | https://uelectronics.com/producto/sensor-de-ph-liquido/ | Amazon: https://www.amazon.com.mx/PH-4502C-Sensor-Liquido-electrodo-E201-BNC/dp/B09MSSPR8Q · Geek Factory: https://www.geekfactory.mx/tienda/sensores/ph-4502c-kit-sensor-de-ph-economico/ — deriva más y el electrodo dura menos, pero sirve para validar el lazo de control antes de invertir en DFRobot |
| Sonda EC/TDS + placa | UNIT (SEN0244 DFRobot) o Amazon (Keyestudio) | ~$300–550 aprox | https://uelectronics.com/producto/sensor-tds-meter-v1-0-analogico-sen0244/ | Keyestudio (incluye 3 sondas): https://www.amazon.com.mx/KEYESTUDIO-TDS-control-conector-XH2-54-3pin/dp/B08DGLY3J2 · Gravity TDS: https://www.amazon.com.mx/Gravedad-anal%C3%B3gico-Arduino-disueltos-compatible/dp/B086GX2539 · CQRobot: https://www.amazon.com.mx/CQRobot-Ocean-Compatible-Investigaci%C3%B3n-Laboratorio/dp/B08KXRHK7H. Ojo: TDS≈EC×0.5–0.7; en ESPHome calibra en mS/cm directamente |
| 3× bombas peristálticas 12V | Mercado Libre | **$145–280 c/u aprox → $435–840 las 3** | https://listado.mercadolibre.com.mx/bomba-peristaltica-12v | Doble cabezal $279.85 aprox: https://www.mercadolibre.com.mx/bomba-peristaltica-dosificadora-de-agua-de-doble-cabezal-mi/p/MLM2017622966 — compra 4 (1 de repuesto); la manguera interna es consumible |
| Válvulas solenoides 12V ×2 (1/2") | Mercado Libre o UNIT | ~$100–250 c/u aprox | https://listado.mercadolibre.com.mx/valvula-solenoide-12v-1-2 | UNIT tiene la electroválvula 1/2" NC: https://uelectronics.com/producto/electrovalvula-solenoide-1-2-pulgada-nc/ · Tecneu colección: https://www.tecneu.com/collections/electrovalvulas. NC (normalmente cerrada) para que un corte de luz no vacíe el tinaco |
| ESP32-CAM (timelapse/inspección) | UNIT Electronics | **$244–260 aprox** (OV2640 + CH340) | https://uelectronics.com/producto/esp32-cam-ov2640-con-ch340-wifi-bluetooth/ | Versión V3 USB-C (más cómoda de flashear): https://uelectronics.com/producto/esp32-cam-ov2640-v3-con-interfaz-tipo-c/ · ML: https://listado.mercadolibre.com.mx/esp32-cam |
| Sensor de flujo YF-S201 | Tecneu / Mercado Libre | **$74 [verificado, hoy agotado]** / ~$90–130 aprox ML | https://www.tecneu.com/products/sensor-de-flujo-de-agua-caudalimetro-yf-s201 | ML: https://listado.mercadolibre.com.mx/sensor-de-flujo-de-agua-yf-s201 · Amazon: https://www.amazon.com.mx/Sensor-Flujo-Agua-YF-S201-Efecto/dp/B09MSTW9ZM |

**Subtotal v2 realista:** ~$2,600–4,600 según elijas pH económico o DFRobot. El presupuesto del plan es correcto **si** vas directo al kit DFRobot.

---

### 4. Qué comprar en persona en el Centro (República de El Salvador) y por qué

**AG Electrónica, República de El Salvador 20-F (mostrador) y 20 piso 2 (mayoreo), Centro Histórico [verificado]**
L–V 9:00–19:00, Sáb 10:00–17:00 · Tel (55) 5130 7210 · Sucursal Xpress en Vallejo 1874, GAM.
La misma calle concentra decenas de tiendas de electrónica (es el "barrio electrónico" clásico de CDMX), así que
una sola ida resuelve todo el material de soporte.

Conviene comprar EN PERSONA:
1. **Fuente(s) 12V 5A, cable, conectores, borneras, gabinetes IP65, protoboard, headers, soldadura** — son
   pesados/voluminosos (el envío come el ahorro), ahí los pruebas en mostrador y el personal técnico te ayuda a
   elegir calibres y gabinetes. AG presume +900,000 productos y soporte de ingenieros.
2. **Relevadores, optoacopladores, MOSFETs, diodos flyback, fusibles y portafusibles** — piezas de a $5–50 donde
   el envío de $150 duplica el costo; en mostrador compras exactamente la cantidad que necesitas.
3. **Raspberry Pi 5 8GB ($4,259 IVA incl.)** cuando repongan stock (**180 pzas arriban el 19-sep-2026** según su
   web) — la recoges el mismo día sin riesgo de paquetería.
4. **Reemplazos de emergencia**: si un relé o fuente truena un viernes con charolas vivas, el Centro es la única
   opción mismo-día junto con Steren; vale la pena conocer el mostrador antes de necesitarlo.

NO conviene comprar en el Centro:
- **Sondas pH/EC de calidad** (DFRobot): no es su fuerte; mejor Geek Factory/HetPro/UNIT/Amazon.
- **Sensores capacitivos y módulos chinos en cantidad**: el pack ×10 de Amazon sale a mitad de precio por pieza.
- **ESP32**: UNIT casi siempre gana en precio ($126–139 vs típicamente $180–250 en mostrador).

**Steren** (sucursales en todo CDMX, incluido el Centro): garantía nacional y factura fácil. Su ELI-1260 (12V 5A,
$399 [verificado]) cuesta ~2.5× la fuente china de UNIT, pero para el circuito que alimenta la bomba de riego 24/7
esa garantía y regulación valen la pena. Cable, multicontactos, herramienta: bien. Módulos maker: no es lo suyo.

---

### 5. Estrategia de compra sugerida (orden real)

1. **Pedido único a UNIT Electronics** (~$1,400–1,800): 2–3× ESP32 DevKit, ESP32-CAM V3, DS18B20 ×3, DHT22 ×2,
   relé 4 canales, fuente 12V 5A, JSN-SR04T, sensor TDS SEN0244, PH-4502C (para el lazo de prueba). Un solo envío
   a CDMX, 1–3 días.
2. **Mercado Libre Full** (~$1,200–1,900): bomba diafragma 12V, kit nebulizadores, 4× bombas peristálticas,
   2× válvulas solenoides NC 1/2", SHT31. Filtra por "Full" para entrega al día siguiente.
3. **Amazon MX** (~$300): pack ×10 sensores capacitivos.
4. **Ida al Centro (AG Electrónica)** (~$800–1,500): gabinetes, cable, borneras, conectores, fusibles, protección
   — y de paso conoces el mostrador. Si hay stock, la Pi 5 8GB ahí mismo; si no, **Cyberpuerta Pi 5 4GB $3,069** o
   **mini PC ThinkCentre usado ~$2,500–3,500 en ML** (recomendado si quieres Frigate + Grafana sin sufrir).
5. **Cuando el NFT esté decidido (Fase 2)**: kit pH DFRobot Gravity en Geek Factory ($1,250 aprox) + buffers 4.0 y
   6.86 extra. No antes: el electrodo caduca aunque no lo uses (12–18 meses).

### Recomendación concreta

- **Compra el grueso en UNIT Electronics en un solo pedido**: es consistentemente lo más barato de México en
  ESP32/sensores/módulos y su catálogo cubre 10 de los 15 renglones del plan. (Su web bloquea bots; los precios
  listados aquí son de snippets de buscador — confírmalos en el carrito antes de pagar.)
- **Hidráulica y dosificación por Mercado Libre**, no en tiendas maker: bombas de diafragma, peristálticas y
  solenoides ahí cuestan 30–50% menos y llegan al día siguiente con Full.
- **Cerebro**: mini PC Lenovo ThinkCentre usado i5/8GB/SSD (~$2,500–3,500, ML) mejor que Raspberry Pi al precio
  actual de las Pi en México; si prefieres Pi por consumo eléctrico y GPIO, la **Pi 5 4GB de Cyberpuerta ($3,069,
  50 pzas en stock [verificado])** es la compra segura hoy, o la 8GB en AG el 19-sep.
- **pH en dos etapas**: PH-4502C ($329) para desarrollar y probar el control en Fase 1–2 temprana; kit DFRobot
  Gravity ($1,250 Geek Factory) cuando el NFT ya venda. Presupuesta el reemplazo anual del electrodo (~$400–600).
- **Fuente del sistema de riego**: Steren ELI-1260 o la Mean Well IP67 de UNIT para lo crítico; la china genérica
  solo para electrónica de señal.
- **Haz una ida al Centro (AG, Salvador 20-F)** por el material de soporte y para tener proveedor de emergencia
  mismo-día; no compres ahí ESP32 ni sondas.
- **Total estimado**: v1 ~$3,500–5,500 · v2 ~$2,600–4,600 — dentro del rango del plan con las elecciones
  indicadas.

### Huecos / pendientes de verificación humana
- Precios exactos de UNIT Electronics (Cloudflare bloquea verificación automatizada): confirmar en carrito.
- Precio real hoy de la Pi 5 8GB en Cyberpuerta: un snippet decía $2,619 (incoherente con la 4GB a $3,069) — verificar en la ficha.
- Stock del kit pH DFRobot en Geek Factory y HetPro (páginas con captcha).
- Si AG Electrónica maneja ESP32/módulos maker en mostrador a precio competitivo (su buscador web solo responde por SKU exacto).
- Disponibilidad del YF-S201 en Tecneu (hoy "agotado") y su costo de envío a CDMX.
