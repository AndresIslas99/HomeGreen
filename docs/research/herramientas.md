# Herramientas para el huerto automatizado (Fases 0–2) — Investigación de proveedores y precios

**Fecha:** 12 de septiembre de 2026 · **Zona:** CDMX · **Moneda:** MXN
**Metodología:** 9 búsquedas web + 19 fichas/categorías abiertas con WebFetch (Home Depot MX, Steren en línea). Mercado Libre bloquea la lectura automatizada (HTTP 403), por lo que sus URLs son de búsqueda y los precios de ML van marcados "aprox.". En varias fichas de Home Depot el precio se leyó sin punto decimal (ej. "$62,900" = $629.00); esos precios van marcados "aprox." y están en la lista de verificación.

**Convención de columnas:** "¿Maker la tiene?" = probabilidad de que alguien que ya arma ESP32/impresión 3D/electrónica hobbista la tenga en casa (Sí / Probable / No).

---

### (a) Construcción de estructura (Fase 1: PTR/tubo galvanizado, anclaje a piso/muro, malla antigranizo)

| Herramienta | ¿Maker la tiene? | Precio MXN | Dónde | Notas |
|---|---|---|---|---|
| Rotomartillo Truper PRO 1/2" 650 W (ROTO-1/2A7) | Probable (taladro sí; rotomartillo no siempre) | **$660.00 (verificado)** | [Home Depot MX](https://www.homedepot.com.mx/p/truper-rotomartillo-1-2-650w-truper-pro-roto-1-2a7-231999) | Suficiente para taquetes de 1/4"–3/8" en concreto de patio. Alternativa inalámbrica Truper 20V (ROTI-20A) en la misma tienda, más cara. Catálogo completo: [Rotomartillos y taladros](https://www.homedepot.com.mx/b/herramientas/rotomartillos-y-taladros) |
| Juego de brocas Truper 9 pzas (madera/concreto/metal) | Probable | aprox. $215 | [Búsqueda HD "brocas para concreto"](https://www.homedepot.com.mx/s/brocas+para+concreto) | SKU 192928, 4.8★. Lo importante: broca de concreto de 1/4" y 5/16" para taquete |
| Taquetes expansor 1/4" c/tornillo (4 pzas) | No (consumible) | aprox. $81 el pack; taquetes de plástico desde ~$20 | [Búsqueda HD "taquete"](https://www.homedepot.com.mx/s/taquete) | Para anclar la estructura y racks al piso/muro. Comprar 4–6 packs (Fase 1). En tlapalería de barrio salen más baratos a granel |
| Pijas + taquetes de nylon surtidos | No (consumible) | $50–150 aprox. | Tlapalería / [HD taquetes](https://www.homedepot.com.mx/s/taquete) | Caja surtida 1/4" y 5/16" para malla antigranizo y soportería ligera |
| Flexómetro Truper 3 m | Sí | **$66.00 (verificado)** | [Búsqueda HD "flexometro truper"](https://www.homedepot.com.mx/s/flexometro+truper) | Para la obra conviene mejor uno de 5 m (~$90–130 aprox. en tlapalería, Truper FH-5M) |
| Nivel torpedo Truper NTX-9 10" magnético | Probable | aprox. $199 | [Búsqueda HD "nivel torpedo"](https://www.homedepot.com.mx/s/nivel+torpedo) | Magnético = útil sobre PTR. Para racks y pendiente NFT (1–3 %) conviene sumar nivel de 24" (~$150–250 aprox. tlapalería) |
| Escuadra metálica de carpintero | Probable | $80–150 aprox. | Tlapalería (Truper E-24 / Pretul) | No verificada en línea; cualquier tlapalería la tiene |
| Pinzas de presión (perras) Truper 10" | Probable | aprox. $225 | [Búsqueda HD "pinzas de presion"](https://www.homedepot.com.mx/s/pinzas+de+presion) | SKU 942164. Tercer "ayudante" al soldar/atornillar PTR |
| Arco con segueta (Truper ATG-24 o similar) | Probable | $100–180 aprox. | Tlapalería / HD | No verificado en línea. Suficiente para PVC y tubo pared delgada si no se compra esmeriladora |
| Esmeriladora angular Truper 4-1/2" 700 W (ESMA-4-1/2A12) | Probable | aprox. $629 | [Home Depot MX](https://www.homedepot.com.mx/p/truper-esmeriladora-angular-41-2-700-w-profesional-truper-esma-4-1-2a12-207858) | Solo necesaria si se corta PTR en sitio. Con discos de corte metal (~$25–40 c/u). Versión industrial 950W ESMA-4590N también en HD |
| Careta facial / careta para esmerilar | No | $100–250 aprox. | Tlapalería / ML: [búsqueda "careta esmerilar truper"](https://listado.mercadolibre.com.mx/careta-esmerilar-truper) | No encontré ficha verificable; obligatoria si se usa esmeriladora |
| Guantes de carnaza/trabajo | Probable | $60–120 aprox. | Tlapalería (Truper/Pretul) | Para manejo de PTR, malla y esmeril |

**Subtotal categoría (a) si se compra todo:** ~$2,400–2,900. **Si ya se tiene taladro/pinzas/flexómetro/nivel:** ~$1,000–1,400 (rotomartillo + brocas + taquetes + careta).

Nota: si la estructura se manda hacer con herrero (recomendado en el plan para PTR soldado), la esmeriladora y careta se vuelven opcionales y el subtotal baja a ~$400–600.

---

### (b) Plomería PVC (Fase 2: líneas NFT de 4", retorno, depósito)

| Herramienta | ¿Maker la tiene? | Precio MXN | Dónde | Notas |
|---|---|---|---|---|
| Corte de PVC 4": segueta (la del arco de arriba) | Probable | — | — | Los cortadores de trinquete llegan a ~1-5/8"; para tubo de 4" se usa segueta o esmeriladora con disco fino. El [cortador Husky 1-5/8" ($275, verificado)](https://www.homedepot.com.mx/s/cortador+pvc) solo sirve para tubería de 1/2"–1-1/4" del retorno |
| Cemento PVC Contact 240 ml transparente | No (consumible) | **$71.00 (verificado)** | [Home Depot MX](https://www.homedepot.com.mx/p/cemento-para-pvc-240-ml-transparente-contact-104028-104028) | Para NFT basta el cemento regular (no hay presión). Categoría completa: [pegamentos y soldaduras](https://www.homedepot.com.mx/b/plomeria/tuberias-y-conexiones/soldadura-pastas-y-accesorios) |
| Limpiador PVC (Oatey 118 ml) | No (consumible) | aprox. $73 | [Categoría HD pegamentos](https://www.homedepot.com.mx/b/plomeria/tuberias-y-conexiones/soldadura-pastas-y-accesorios) | Opcional pero mejora la unión en tubo sucio/asoleado |
| Cinta teflón 1/2" | Sí/consumible | **$6–25 (verificado)** | [Búsqueda HD "cinta teflon"](https://www.homedepot.com.mx/s/cinta+teflon) | Southland y Coflex. Comprar 3–4 rollos: bomba, válvulas, conexiones roscadas |
| **Sierra copa para canastillas de 2"** | No | aprox. $150–350 (Truper); kit Milwaukee 9 pzas aprox. $2,129 | ML: [búsqueda "truper sierra corta circulos bimetalica"](https://listado.mercadolibre.com.mx/truper-sierra-corta-circulos-bimetalica) · [Búsqueda HD "sierra copa"](https://www.homedepot.com.mx/s/sierra+copa) | **CRÍTICO — diámetro:** la canastilla "de 2 pulgadas" se sostiene por el labio; el barreno correcto es de **1-3/4" (44 mm) a 1-7/8" (48 mm)** según el fabricante de la canastilla, NUNCA 2" exactas (se cae). Comprar la canastilla primero, medir el cuerpo bajo el labio y entonces comprar la sierra copa. Línea Truper COBI existe en varios diámetros (COBI-1-3/4 etc., visto en [Amazon MX](https://www.amazon.com.mx/Truper-COBI-1-1-Cortac%C3%ADrculos-bimet%C3%A1licos-1-1/dp/B013R1P8QO)); HD en línea casi no lista piezas sueltas |
| Árbol/mandril para sierra copa | No | $80–150 aprox. | Misma búsqueda ML | Algunas COBI ya integran broca piloto; verificar |
| Lima o cuchilla para desbarbar perforaciones | Probable | $40–80 aprox. | Tlapalería | Rebabas de PVC en el canal NFT atoran raíces y flujo |

**Subtotal categoría (b):** ~$400–700 (sin contar tubería/conexiones, que son material, no herramienta).

---

### (c) Electrónica (Fases 1–2: nodos ESP32, relés, sondas, gabinetes)

Steren tiene 15+ sucursales en CDMX y tienda en línea con entrega local; es la referencia natural.

| Herramienta | ¿Maker la tiene? | Precio MXN | Dónde | Notas |
|---|---|---|---|---|
| Cautín lápiz 35 W con accesorios (punta extra, pasta, soldadura, desarmador) | Sí | **$199.00 (verificado)** | [Steren](https://www.steren.com.mx/cautin-economico-tipo-lapiz-de-35-watts-con-accesorios.html) | Versión sin accesorios: $99 ([Steren](https://www.steren.com.mx/cautin-economico-tipo-lapiz-de-35-watts.html)). Categoría: [cautines](https://www.steren.com.mx/herramientas/cautines-y-accesorios) |
| Estaño 60/40: tubo chico $59; rollo 450 g $565 | Sí | **verificado (snippet Steren)** | [Rollo 450 g Steren](https://www.steren.com.mx/rollo-de-450-gramos-de-soldadura-con-aleacion-esta-o-plomo-60-40.html) | Para el proyecto basta un rollo chico (~$59–120); pasta $49 |
| Multímetro Steren MUL-005 compacto | Sí | **$99.00 (oferta $89.32, verificado)** | [Steren MUL-005](https://www.steren.com.mx/multimetro-compacto-economico.html) · [categoría](https://www.steren.com.mx/herramientas/multimetros) | Si se quiere mejor: MUL-281 profesional $399 (oferta $324.80). Imprescindible para depurar relés/fuentes 12 V |
| Pinzas de punta y de corte para electrónica | Sí | $60–150 c/u aprox. | [Steren herramientas](https://www.steren.com.mx/herramientas) / tlapalería (Truper/Pretul) | No verificadas pieza por pieza; Steren y cualquier Steren Shop las tienen |
| Protoboard 830 pts (ensamble a presión 509-010) | Sí | **$127.60 (verificado, precio con descuento)** | [Búsqueda Steren "protoboard"](https://www.steren.com.mx/catalogsearch/result/?q=protoboard) | Mini protoboard desde $40.60 |
| Cables Dupont: 80 pzas 15 cm $49.88 · 120 pzas 20 cm $71.92 | Sí | **verificado** | [Búsqueda Steren "protoboard"](https://www.steren.com.mx/catalogsearch/result/?q=protoboard) | Modelos ARD-310 / ARD-312 |
| Termofit (tubo termorretráctil) surtido | Sí | desde **$13/tramo (verificado)**; kit ~$60–120 aprox. | [Búsqueda Steren "termofit"](https://www.steren.com.mx/catalogsearch/result/?q=termofit) | Obligatorio en empalmes 12 V que viven en humedad |
| Cinchos (bridas) 100 pzas | Sí | $40–90 aprox. | Steren / tlapalería / HD | Consumible; comprar 2 bolsas (cableado + sujetar líneas) |
| Gabinete interior Steren GP-14 (22×9×14 cm) | Probable | **$199.00 (verificado)** | [Búsqueda Steren "gabinete"](https://www.steren.com.mx/catalogsearch/result/?q=gabinete) | Solo para nodos BAJO techo. GP-02 $99, GP-04 $149 |
| **Gabinete IP65 para exterior** (300×300×90 mm aprox.) | No | $250–600 aprox. según tamaño | ML: [búsqueda "gabinete plastico exterior ip65"](https://listado.mercadolibre.com.mx/gabinete-plastico-exterior-ip65) · alternativa [Bsai](https://www.bsai.com.mx/products/gabinete-plastico-para-exterior-ip65-de-300-x-300-x-90-mm-cierre-por-tornillos) | Para el nodo del túnel y el de la bomba: ABS, sello de silicón, −20 a 60 °C. Comprar 2 (Fase 1: riego; Fase 2: dosificación). Con glándulas/prensaestopas PG (~$10–20 c/u en ML) |

**Subtotal categoría (c) si se compra todo:** ~$1,200–1,800. **Maker típico (ya tiene cautín, multímetro, protoboard, dupont):** solo gabinetes IP65 + termofit + cinchos ≈ **$600–1,300**.

---

### (d) Operación diaria (Fases 0–2: siembra, cosecha, venta, respaldo de sensores)

| Herramienta | ¿Maker la tiene? | Precio MXN | Dónde | Notas |
|---|---|---|---|---|
| Báscula digital de cocina (1 g, 5–10 kg) | Probable (en casa) | desde ~$77–150 aprox. | ML: [búsqueda "bascula digital cocina"](https://listado.mercadolibre.com.mx/bascula-digital-cocina) | Tipo SF-400. Para pesar charolas cosechadas y armar pedidos por kg |
| Báscula de precisión 0.1 g (500 g cap.) | Probable | ~$100–250 aprox. | ML: [búsqueda "bascula de precision 0.1g"](https://listado.mercadolibre.com.mx/bascula-de-precision-0.1g) | Para dosificar semilla por charola (girasol 100–120 g, brócoli 25–30 g) y sales nutrientes en Fase 2 |
| Tijera Truper para plantas y tallos 3/4" (mango engomado) | No | **$180.00 (verificado)** | [Home Depot MX](https://www.homedepot.com.mx/p/truper-tijera-para-plantas-y-tallos-3-4-de-pulgada-naranja-truper-08-2018-820031) | Para hierbas NFT (albahaca). Para microgreens es mejor tijera recta de cocina de acero inoxidable ($60–120 aprox., cualquier súper) o cuchillo cebollero afilado |
| Tijera de poda Truper T-45 8" | No | aprox. $149 | [Home Depot MX](https://www.homedepot.com.mx/p/truper-tijera-para-poda-de-8-pulgadas-naranja-truper-t-45-824798) | Respaldo/uso general de jardín (Fase 3) |
| Atomizadores 1 L (2 pzas) | Probable | aprox. $137–179 el par | [Búsqueda HD "atomizador"](https://www.homedepot.com.mx/s/atomizador) | Uno para agua, otro EXCLUSIVO para H2O2 (etiquetarlos). Atomizador simple desde ~$16–44 |
| Fumigador de presión previa 1.5–2 L (Truper) | No | $250–450 aprox. | Tlapalería / [HD jardín](https://www.homedepot.com.mx/b/jardin/herramientas-para-jardin) | Opcional: acelera el riego de charolas en Fase 0 antes de automatizar. Precio no verificado |
| Cubetas de 19–20 L + jarra graduada 1–2 L | Probable | $60–120 cubeta; $40–80 jarra aprox. | Tlapalería / HD / súper | Marcar la cubeta con litros (báscula: 1 L = 1 kg) para preparar nutriente sin comprar nada especial |
| Termohigrómetro digital Steren TER-120 | Probable | **$199.00 (oferta $150.80, verificado)** | [Steren termómetros](https://www.steren.com.mx/casa-y-oficina/termometros-digitales) | Respaldo analógico-independiente de los SHT31/DHT22 del ESP32. Mini TER-090 $149 (oferta $114.84) |
| Medidor pH de bolsillo + medidor TDS/EC (respaldo de las sondas DFRobot) | No | pluma pH ~$150–350; TDS ~$100–250; combo 3-en-1 ~$300–600 (todo aprox.) | ML: [búsqueda "medidor ph tds ec"](https://listado.mercadolibre.com.mx/medidor-ph-tds-ec) | Imprescindible en Fase 2: es el árbitro cuando la sonda fija se descalibra. Comprar también buffers 4.0/6.86 y solución de calibración 1413 µS (mismos listados). Opción seria: Hanna HI98130 (pH/EC/TDS impermeable), en México ronda $4,000–6,000 aprox. — solo si las hierbas ya facturan |

**Subtotal categoría (d):** ~$900–1,600 (con combo pH/EC económico).

---

### (e) Seguridad e higiene

| Herramienta | ¿Maker la tiene? | Precio MXN | Dónde | Notas |
|---|---|---|---|---|
| Lentes de seguridad policarbonato (Cabel) | Probable | **$40.00 (verificado)** | [Búsqueda HD "lentes seguridad"](https://www.homedepot.com.mx/s/lentes+seguridad) | Jyrsa $58, 3M desde $75. Para taladrar concreto y cortar metal |
| Guantes de nitrilo desechables, caja 100 (Forte, uso rudo) | No (consumible) | **$369.00 (verificado)** | [Home Depot MX](https://www.homedepot.com.mx/p/forte-caja-de-100-guantes-medianos-de-nitrilo-desechables-para-uso-rudo-93252-206899) | Cosecha e higiene de alimentos + manejo de H2O2/pH−. Alternativa Truper GU-852A caja 100 en [Amazon MX](https://www.amazon.com.mx/GU-852A-nitrilo-desechable-mediano-Mediana/dp/B07ZWS2L2K). En ML hay cajas desde ~$180 aprox. |
| Cubrebocas (para manejo de semilla y siembra) | Sí (post-pandemia) | $50–100 caja 50 aprox. | Farmacia / súper / ML | Las semillas con fungicida (raro en microgreens, verificar etiqueta) y el polvo de fibra de coco lo ameritan. KN95 solo si se lija/esmerila |
| Botiquín básico + extintor ABC chico | Probable | $300–600 aprox. | HD / ferretería | Recomendado al meter fuentes 12 V y bomba 0.5 HP en zona húmeda; no verificado en línea |

**Subtotal categoría (e):** ~$450–800.

---

### Presupuesto consolidado de herramientas

| Escenario | Fase 0 | Fase 1 | Fase 2 | Total |
|---|---|---|---|---|
| **Maker ya equipado** (tiene taladro, multímetro, cautín, protoboard, pinzas, flexómetro, lentes) | ~$700 (básculas, tijeras, atomizadores, guantes) | ~$1,300–1,900 (rotomartillo o brocas+taquetes, gabinetes IP65, termofit, nivel) | ~$900–1,500 (sierra copa, cemento/limpiador PVC, pH/EC de mano, buffers) | **~$2,900–4,100** |
| **Desde cero** | ~$1,000 | ~$3,500–4,500 | ~$1,500–2,200 | **~$6,000–7,700** |
| **Desde cero + esmeriladora y careta** (corta su propio PTR) | — | +$800–900 | — | **~$6,800–8,600** |

Coherente con la filosofía del plan: las herramientas se compran POR FASE, no todas el día 1. En Fase 0 solo se necesitan ~$700–1,000 de esta lista.

---

### Directorio de proveedores

| Proveedor | Qué comprarle | Entrega CDMX | Enlace raíz |
|---|---|---|---|
| Home Depot México | Rotomartillo, brocas, taquetes, PVC (cemento/teflón), tijeras Truper, guantes, lentes | Sí (a domicilio y recoger en tienda; varias sucursales CDMX) | https://www.homedepot.com.mx |
| Steren | Todo lo de electrónica: cautín, estaño, multímetro, protoboard, dupont, termofit, gabinetes interiores, termohigrómetro | Sí (en línea + ~15 sucursales CDMX) | https://www.steren.com.mx |
| Mercado Libre MX | Sierra copa Truper, gabinete IP65, básculas, medidor pH/EC, careta, cajas de guantes baratas | Sí (Full = 1–2 días CDMX) | https://listado.mercadolibre.com.mx |
| Tlapalería de barrio (referencia Truper/Pretul) | Flexómetro 5 m, nivel 24", escuadra, arco/segueta, pinzas, cinchos, cubetas, pijas a granel | Inmediata | — (catálogo de referencia: https://www.truper.com) |
| Amazon MX | Alternativa para sierra copa COBI y guantes Truper GU-852A | Sí | https://www.amazon.com.mx |

---

### Recomendación concreta

1. **No comprar nada de golpe.** Fase 0 solo requiere: báscula de cocina (~$120), báscula 0.1 g (~$150), tijera recta inox de cocina (~$80), 2 atomizadores (~$150), caja de guantes de nitrilo ($369 HD o ~$200 ML) y cubrebocas. Total ≈ **$900**. Todo lo demás espera al gate de 2 clientes.
2. **Fase 1 — decidir "herrero vs. DIY" antes de comprar:** si un herrero suelda la estructura de PTR (recomendado: cobra $200–400/día y trae su equipo), NO comprar esmeriladora ni careta (ahorro ~$850). Solo comprar: rotomartillo Truper 650 W ($660), juego de brocas ($215 aprox.), taquetes/pijas (~$200), nivel torpedo ($199 aprox.) — y rentar/pedir prestado lo demás.
3. **Electrónica: comprar en Steren en una sola visita** (sucursal física evita envíos): cautín 35 W con kit $199, MUL-005 $99 (si no se tiene multímetro), dupont 120 pzas $72, protoboard $128, termofit y cinchos ~$150. Los **gabinetes IP65 solo en Mercado Libre** (Steren no maneja IP65): 2 piezas de ~300×200×130 mm con prensaestopas, ~$700 total aprox.
4. **Sierra copa: comprar DESPUÉS de tener las canastillas en mano.** Medir el diámetro del cuerpo bajo el labio (típico 44–48 mm para canastilla "2 pulgadas") y comprar UNA sierra copa Truper COBI del diámetro medido (~$150–350 en ML) con mandril. No comprar kits de 9 piezas ($2,100+): se usan 1 o 2 diámetros en todo el proyecto.
5. **pH/EC de mano se compra en Fase 2, no antes** (los microgreens no lo necesitan): combo económico 3-en-1 de ML (~$400 aprox.) + buffers 4.0/6.86 + solución 1413 µS. Presupuestar recambio anual (el plan ya lo contempla con $400/año). Subir a Hanna HI98130 solo cuando las hierbas facturen >$6k/mes.
6. **Regla de compra:** todo lo que sea Truper/Pretul, cotizar primero en tlapalería de barrio (suele estar 10–20 % abajo de HD en herramienta manual); todo lo electrónico, Steren; todo lo "raro" (IP65, sierra copa suelta, básculas, pH), Mercado Libre con vendedor 4.7★+.

---

### Pendientes de verificación (para el verificador)

- Precios de Home Depot marcados "aprox.": el scraper leyó los montos sin punto decimal (ej. esmeriladora "62,900" ⇒ $629.00; taquetes "8,100" ⇒ $81.00; pinzas "22,500" ⇒ $225.00; nivel "19,900" ⇒ $199.00; brocas "21,500" ⇒ $215.00). Confirmar en la ficha.
- Sierra copa Truper COBI en 1-3/4" o 1-7/8": SKU y precio exacto en ML/Amazon MX (no pude abrir ML, 403).
- Gabinete IP65: Bsai devolvió 503; precios de ML sin confirmar.
- Careta para esmerilar Truper, fumigador de presión previa y arco/segueta: sin ficha de precio verificada.
- Medidor pH/EC combos en ML: rango $300–600 es estimado de mercado, no verificado.
- Hanna HI98130 en México: solo encontré tienda española (fertitienda.com, 235,95 €); falta proveedor mexicano con precio MXN.
