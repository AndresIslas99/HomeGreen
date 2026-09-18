# BOM por fase

Lista de materiales del proyecto. **Una fila = una cosa que se compra una vez.**
Las alternativas de proveedor no viven aquí: viven en
[`bom/opciones.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/opciones.csv),
que **no tiene columna de subtotal** y por lo tanto no puede inflar ningún total.

!!! info "Cómo leer esta página"
    - **Las partidas en *cursiva*, con el subtotal entre paréntesis, no suman.**
      Siguen aquí porque son información útil (un precio de referencia, una compra
      condicional, algo que ya pagaste en la fase anterior), pero el total de la fase
      no las incluye. La razón de cada una está en su nota y en la tabla de abajo.
    - **El subtotal siempre es `cantidad × precio unitario`.**
      [`tools/gen_bom.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gen_bom.py)
      falla si alguna fila no multiplica, así que no puede volver a desalinearse.
    - **El precio es el de la opción marcada como predeterminada.** Cambiar de
      proveedor es cambiar `opcion_default` y volver a correr el script: el total
      se recalcula solo.
    - Para comprar **en persona**, la ruta en auto está en
      [Proveedores presenciales](proveedores-presenciales.md).

## Resumen

| Fase | Inversión que sí se desembolsa | Versión austera |
|---|---:|---:|
| Fase 0 · Validación comercial | $8,814 | $8,095 |
| Fase 1 · Túnel y automatización v1 | $41,634 | $40,244 |
| Fase 2 · NFT y automatización v2 | $27,251 | $24,082 |
| **Acumulado Fases 0–2** | **$77,699** | **$72,421** |

La columna austera cambia cada partida a la opción marcada como
`alternativa_austera` en `opciones.csv` (rack Adir en vez de Husky, contacto GFCI en vez
de breaker, batería AGM en vez de LiFePO4, plástico de invernaderosMX). **La calcula el
script**, así que no puede desfasarse como la frase suelta que traía el CSV viejo, que
afirmaba que comprar 250 g de rábano salía más barato que 500 g cuando el escalón de
precio lo encarece $200.

??? warning "Qué cambió respecto del BOM viejo, y por qué el total bajó"
    El BOM anterior publicaba **$86,500** acumulados. Este publica **$77,699**.
    La diferencia no es que se haya recortado el proyecto: es que el total viejo
    cobraba cosas dos veces o cobraba alternativas entre las que hay que elegir una. Son $12,138 repartidos en 8 filas que ahora siguen visibles pero en cero:

    | Partida | Importe | Por qué no suma |
    |---|---:|---|
    | Separador de primeras lluvias (Paquete Basico Tlaloc) | $5,300 | misma función que una partida ya pagada antes |
    | Electricista certificado | $2,500 | misma función que una partida ya pagada antes |
    | No-break del cerebro y el router | $1,189 | misma función que una partida ya pagada antes |
    | Breaker GFCI del circuito del patio | $1,159 | misma función que una partida ya pagada antes |
    | Tapa intemperie + varilla copperweld + cable cal. 8 | $900 | misma función que una partida ya pagada antes |
    | Responsabilidad civil PyMEs con RC de productos | $500 | gasto mensual, no inversión de capital |
    | Chicharo Early Perfection a granel | $340 | precio de referencia; el propio proyecto dice que no se compra |
    | Hipoclorito de calcio 65% (estandar duro 20,000 ppm) | $250 | solo si se da el supuesto que la nota describe |

## Fase 0 · Validación comercial

**Total de la fase: $8,814**

| Partida | Cant. | P. unitario | Subtotal | Dónde comprarla | Notas |
|---|---:|---:|---:|---|---|
| Rack de produccion 5 niveles (183x91x46 cm) | 1 pza | $2,019 | $2,019 | Home Depot Copilco *(+1 opc.)* | 362.9 kg/repisa. Forrar entrepanos con plastico o charola colectora |
| Charola 10x20 PERFORADA (la de adentro del par) | 10 pza | $60 | $600 | Al Natural | Flujo de doble charola: la perforada va DENTRO de la lisa. Se compran juntas, 10 pares |
| Charola 10x20 LISA (la de afuera: riego por fondo y blackout) | 10 pza | $60 | $600 | Al Natural | NO es duplicado de la perforada: es la otra mitad del par. Tambien sirve de tapa para la oscuridad |
| Girasol: prueba A/B de semilla (juego de 2 lotes de 1 kg) | 1 juego | $219 | $219 | Central de Abasto | NO son dos compras del mismo insumo: es UN experimento. 3 charolas gemelas de cada lote. Si el de CEDA germina >=80% en V1, la recompra es costal d… |
| *Chicharo Early Perfection a granel* | 1 kg | $340 | — *($340)* | Central de Abasto | NO COMPRAR. A $340/kg y 275 g por charola son $93.50 de semilla: pierde dinero. Conseguir arvejon grado alimento en CEDA (~$40-60/kg) antes de semb… |
| Rabano Champion a granel | 500 g | $2 | $800 | Hydro Environment | Rinde 25-30 g por charola. SIEMPRE comprar 500 g: el escalon de 453+ g cuesta $1.60/g contra $4.00/g de 100-452 g. Comprar 250 g para ahorrar SALE … |
| Betabel Early Wonder a granel | 500 g | $2 | $800 | Hydro Environment | Ciclo mas largo que el rabano: sembrar menos volumen. Mismo escalon de precio que el rabano |
| Brocoli para brotes | 1 bolsa | $201 | $201 | Central de Abasto *(+1 opc.)* | NO comprar en Hydro Environment: $3,500/kg. Confirmar gramaje de la bolsa antes de pagar |
| Variedades finas para muestras (amaranto, mostaza, cilantro) | 3 sobre | $100 | $300 | Ignacio Allende 21 | Solo muestras a chefs. Pasar a granel cuando haya pedido recurrente |
| Polvillo de coco para germinacion 50 L | 2 pza | $115 | $230 | Hydro Environment *(+1 opc.)* | ~$2.10 por charola. Al escalar: tarima de 20 blocks lavados |
| Bascula de cosecha 1 g (hasta 5-10 kg) | 1 pza | $120 | $120 | Steren Miguel Angel de Quevedo | Pesa la cosecha y arma pedidos. NO puede hacer el trabajo de la de dosificacion |
| Bascula de dosificacion 0.1 g (hasta 500 g) | 1 pza | $180 | $180 | Steren Miguel Angel de Quevedo | Dosifica semilla por charola y despues sales A/B. NO puede hacer el trabajo de la de cosecha |
| Tijera recta de acero inoxidable | 1 pza | $90 | $90 | Costco Coapa | Mejor que tijera de jardin para microgreens |
| Atomizador 1 L | 2 pza | $80 | $160 | Home Depot Copilco | Son 2 a proposito: uno queda EXCLUSIVO para H2O2 y etiquetado. Mezclarlos contamina el agua de riego |
| Guantes de nitrilo (caja 100) | 1 caja | $250 | $250 | Home Depot Copilco *(+1 opc.)* |  |
| Sanitizante de semilla y charolas (H2O2 35% grado alimenticio) | 1 L | $200 | $200 | Cerrada de Colima 2 *(+1 opc.)* | Se diluye 1:11 para llegar a 3%: 1 L rinde ~11 L de solucion de trabajo. DILUIR SIEMPRE |
| Agua oxigenada 3% de farmacia (puente del dia 1) | 2 pza | $30 | $60 | Farmacias del Ahorro/Guadalajara | Es el puente mientras llega el H2O2 al 35%. No es duplicado: es la presentacion lista para usar del dia 1 |
| *Hipoclorito de calcio 65% (estandar duro 20,000 ppm)* | 1 kg | $250 | — *($250)* | Cualquier super de Coyoacan *(+1 opc.)* | Solo si un cliente hotelero o corporativo exige el estandar duro. 31 g/L 15 min + triple enjuague |
| Clamshell PET 8 oz | 100 pza | $4 | $350 | Reno 45 *(+1 opc.)* | Al escalar, cotizar fabricante |
| Etiquetas adhesivas (tiraje chico) | 300 pza | $2 | $600 | Jose Maria Bustillos 19-A | Marca + variedad + fecha de cosecha + lote + contacto. El lote es lo que hace posible un recall |
| Termometro de cocina | 1 pza | $150 | $150 | Steren Miguel Angel de Quevedo | Doble uso: precalentado a 60 C para sanitizar semilla y registro de cadena de frio en entregas |
| Microgreens: The Insiders Secrets (Donny Greens) | 1 pza | $397 | $397 | **solo en línea** | El libro de VENDER a chefs. Leer antes de las visitas |
| El jardinero horticultor (Fortier) | 1 pza | $488 | $488 | El Pendulo | Siembras escalonadas y canal directo |

## Fase 1 · Túnel y automatización v1

**Total de la fase: $41,634**

| Partida | Cant. | P. unitario | Subtotal | Dónde comprarla | Notas |
|---|---:|---:|---:|---|---|
| PTR 1.5x1.5 pulg cal. 14 x 6 m (porticos del tunel) | 15 tramo | $383 | $5,743 | Sodimac Gran Sur *(+2 opc.)* | Tunel 3x6 m a dos aguas. Disenar empalmes desde ahora para poder ampliar a 5x6 en Fase 2 |
| PTR 1 pulg (largueros y contravientos) | 4 tramo | $275 | $1,100 | Sodimac Gran Sur | POR VERIFICAR ANTES DE LA S7: docs/diseno/estructura-tunel.md calcula 7 tramos con kerf, no 4. Si son 7, esta partida sube a $1,925 (+$825) |
| Herreria: soldadura, primario y tornilleria | 1 servicio | $2,000 | $2,000 | Pedir referencias en el mostrador de Perfiles Pacifico o Aceros Mixcoac | Pedir 3 cotizaciones POR ESCRITO. El herrero trae su equipo, asi evitas comprar esmeriladora y careta |
| Anclaje: placas base 10x10 + anclas de cuna 3/8 x 3 | 6 juego | $180 | $1,080 | Home Depot Coapa del Hueso | 2-4 anclas por placa sobre firme de concreto. NUNCA sin anclar: hay rachas de 50-80 km/h. El subtotal viejo decia $1,100 y la multiplicacion da $1,080 |
| Plastico UV cal. 720 blanco lechoso 25% sombra, 6.2 m de ancho | 8 m | $215 | $1,720 | Hydro Environment *(+1 opc.)* | Blanco lechoso, no transparente: difunde la luz y baja el golpe de calor |
| Malla antigranizo 3.7 m de ancho | 40 m | $40 | $1,600 | Hydro Environment *(+1 opc.)* | Va montada 10-20 cm SOBRE el plastico, no pegada. Instalar antes de mayo: el pico estadistico de granizo es agosto |
| Perfil zigzag + resorte + cinta reparadora + canaleta PVC | 1 lote | $1,100 | $1,100 | Hydro Environment *(+1 opc.)* | La canaleta nace con la estructura: es la que alimenta la captacion pluvial |
| Racks de produccion ADICIONALES (3 mas: total 4 con el de Fase 0) | 3 pza | $2,019 | $6,057 | Home Depot Copilco | NO es recompra: el rack de Fase 0 se muda al tunel y estos 3 amplian capacidad. El recorte austero compra 2 y deja 3 en total |
| Tinaco de almacenamiento 750 L | 1 pza | $2,051 | $2,051 | Home Depot Coapa del Hueso *(+1 opc.)* | Sombreado u opaco. Si tu alcaldia tiene tandeo duro, subir a 1,100 L |
| Separador de primeras lluvias + filtro de hojas | 1 sistema | $1,500 | $1,500 | Ferreteria Copilco / Home Depot Coyoacan *(+2 opc.)* | DECIDIR UNA SOLA VEZ, antes de gastar: si aplicas a Cosecha de Lluvia de SEDEMA en enero-febrero y calificas, NO compres ninguna de las dos. El DIY… |
| ESP32 DevKit V1 30 pines | 3 pza | $130 | $390 | UNIT Electronics Copilco | 2 nodos + 1 de repuesto. El repuesto no es lujo: es lo que evita parar una semana |
| Sensor de temperatura y humedad ambiente | 2 pza | $91 | $182 | UNIT Electronics Copilco *(+1 opc.)* | Upgrade sobre el DHT22: no deriva con la humedad alta sostenida del tunel |
| DS18B20 sumergible | 3 pza | $35 | $105 | UNIT Electronics Copilco | Comprar 3: es el sensor que mas se maltrata |
| Sensor capacitivo de humedad de sustrato | 6 pza | $26 | $156 | UNIT Electronics Copilco *(+1 opc.)* | 20-30% salen malos de fabrica. Comprando en mostrador puedes revisarlos antes de pagar, por eso 6 y no 10. Sellar el borde del PCB con esmalte y mo… |
| Modulo rele 4 canales optoacoplado | 2 pza | $110 | $220 | UNIT Electronics Copilco | Riego + ventilador + luces + reserva |
| Fuente 12 V 5 A del circuito critico | 1 pza | $399 | $399 | Steren Miguel Angel de Quevedo *(+1 opc.)* |  |
| Bomba de nebulizacion del rack (diafragma 12 V con presostato) | 1 pza | $350 | $350 | Hydro Environment *(+1 opc.)* | Da presion para nebulizar, 4-6 L/min. NO es la misma bomba que la de recirculacion NFT de Fase 2 |
| Kit de nebulizadores / microaspersores | 1 kit | $250 | $250 | Hydro Environment | 10-30 boquillas con manguera |
| Sensor de nivel del tinaco (JSN-SR04T) | 1 pza | $150 | $150 | UNIT Electronics Copilco | Zona muerta de ~20 cm por encima del nivel maximo: montarlo con esa holgura |
| Cerebro (servidor de Home Assistant) | 1 pza | $3,000 | $3,000 | AG Electronica *(+1 opc.)* | Corre Home Assistant + Grafana. Si ademas quieres Frigate para vision, el mini PC rinde mas que la Pi |
| No-break del cerebro y el router | 1 pza | $900 | $900 | Steren Miguel Angel de Quevedo *(+1 opc.)* | Sin internet no hay alarmas. Esta partida NO se vuelve a comprar en Fase 2: es la misma |
| Gabinete IP65 ~300x300x90 + prensaestopas | 2 pza | $350 | $700 | Home Depot Coapa del Hueso | Uno para el nodo del tunel y otro para el nodo de bomba |
| Material de soporte: cable, borneras, fusibles, termofit, cinchos | 1 lote | $1,000 | $1,000 | AG Electronica *(+1 opc.)* | Comprar en persona y de paso conocer al proveedor de emergencia del mismo dia |
| Tubo LED T8 18 W 120 cm 6500 K | 8 pza | $121 | $968 | Home Depot Copilco *(+1 opc.)* | 2 por nivel. NO pagar grow lights para un ciclo de 10 dias: no se amortizan |
| Canaletas y cable para los tubos T8 | 1 lote | $400 | $400 | Home Depot Copilco | PARTIDA NUEVA: las notas del BOM viejo la mencionaban y ningun renglon la sumaba |
| Tapete termico de germinacion | 1 pza | $380 | $380 | **solo en línea** | CUESTIONA ESTA PARTIDA ANTES DE COMPRARLA: en CDMX, para girasol, chicharo y rabano, la germinacion bajo blackout con charolas apiladas suele basta… |
| Malla sombra 35% 3.7 m de ancho | 6 m | $129 | $774 | Hydro Environment *(+1 opc.)* | SOLO de marzo a mayo, por el UV extremo. Se quita el resto del ano: la albahaca de Fase 2 necesita luz. Si tu S12 no cae en marzo-mayo, difierela |
| Jabon potasico 1 kg | 1 kg | $250 | $250 | Mercado de Cuemanco / El Chino *(+1 opc.)* | Pulgon, mosca blanca y trips: 10-15 ml/L aplicado al enves de la hoja |
| Trampas amarillas pegajosas | 1 paquete | $150 | $150 | Mercado de Cuemanco / El Chino | Una por rack. Es el indicador temprano mas barato que existe |
| Bti para mosca fungosa (Gnatrol DG o equivalente) | 1 pza | $800 | $800 | Av. Guadalupe I. Ramirez *(+1 opc.)* | Comprar ANTES de la primera temporada de lluvias, no cuando ya hay mosca |
| Herramienta de Fase 1 (rotomartillo, brocas, taquetes, niveles) | 1 lote | $1,600 | $1,600 | Home Depot Copilco | Si suelda el herrero, no hace falta esmeriladora ni careta |
| Breaker GFCI del circuito del patio | 1 pza | $1,159 | $1,159 | Home Depot Coapa del Hueso *(+1 opc.)* | MOVIDA DESDE EL BOM DE FASE 2: docs/fases/fase-1/compras.md la exige en la S13, antes del primer rele en el patio. Estaba presupuestada en las dos … |
| Tapa intemperie in-use + varilla copperweld 5/8 x 3 m + cable cal. 8 | 1 lote | $900 | $900 | Home Depot Coapa del Hueso | MOVIDA DESDE EL BOM DE FASE 2. NOM-001: un patio es lugar mojado. Tierra <=25 ohms MEDIDOS, no supuestos |
| Electricista certificado (GFCI, tierra fisica y contacto exterior) | 1 servicio | $2,500 | $2,500 | Pedir referencias en Electrica Evolucion (Col. Espartaco | MOVIDA DESDE EL BOM DE FASE 2. Pedir 3 cotizaciones. Medio dia a dia, llave en mano $1,500-3,500 |

## Fase 2 · NFT y automatización v2

**Total de la fase: $27,251**

| Partida | Cant. | P. unitario | Subtotal | Dónde comprarla | Notas |
|---|---:|---:|---:|---|---|
| Tubo PVC SANITARIO 4 pulg x 6 m (lineas NFT) | 4 tramo | $415 | $1,660 | Home Depot Coapa del Hueso | SANITARIO, no hidraulico cedula 40 ($1,401): el NFT corre sin presion y la diferencia es 3.4x. Blanco porque refleja el calor |
| Codos 90/45, tapas y adaptadores de drenaje 4 pulg | 1 lote | $600 | $600 | Home Depot Coapa del Hueso | Codo de 90 $28.80, codo de 45 $18.31 |
| Tuberia de distribucion 1/2-3/4, retorno 2 pulg y valvulas de compuerta por linea | 1 lote | $750 | $750 | Home Depot Coapa del Hueso | Caudal objetivo 1-2 L/min por linea: se mide con botella de 1 L y cronometro |
| Cemento para PVC, limpiador, teflon y lima de desbarbar | 1 lote | $280 | $280 | Home Depot Coapa del Hueso | PARTIDA NUEVA: las notas del BOM viejo la mencionaban y ningun renglon la sumaba. Sin desbarbar, el borde corta la raiz |
| Canastilla hidroponica 3 pulg | 80 pza | $13 | $1,024 | Hydro Environment *(+1 opc.)* | COMPRARLAS ANTES DE PERFORAR. Medir el cuerpo bajo el labio para elegir la sierra copa |
| Sierra copa bimetalica del diametro medido + mandril | 1 pza | $300 | $300 | Home Depot Copilco | UN SOLO diametro, el que midas de la canastilla. Tipico 44-48 mm para canastilla de 2 pulg; aqui es de 3 pulg, asi que MIDE |
| Bomba de llenado, purga y trasiego (sumergible 4500 LPH) | 1 pza | $1,199 | $1,199 | Hydro Environment | 65 W (~$45/mes de luz) contra 370 W de una periferica (~$260/mes). NO es la bomba de recirculacion 24/7: esa es de 12 V y cuelga de la bateria |
| Filtro de malla 120 mesh 1 pulg | 1 pza | $230 | $230 | Hydro Environment | Va en el RETORNO, antes de la bomba |
| Deposito de solucion nutritiva 200 L grado alimenticio | 1 pza | $700 | $700 | Home Depot Coapa del Hueso *(+1 opc.)* | Bajo sombra. La solucion ideal va a 18-22 C. Cambio completo cada 2-3 semanas |
| Semillero de foami agricola 144 bloques | 2 pza | $46 | $91 | Hydro Environment | $0.32 por planta. NO usar peat pellets: tapan el filtro |
| Solucion nutritiva para hortalizas (rinde 1,000 L) | 2 pza | $349 | $698 | Hydro Environment *(+1 opc.)* | Al pasar de 2 m3/mes conviene el costal de 25 kg ($202/m3) o sales A/B ($90-150/m3). DESCARTAR Flora Series GHE: cuesta 10-40x |
| Acido regulador pH- AquAcid (REACTIVO de dosificacion) | 1 pza | $516 | $516 | Hydro Environment *(+1 opc.)* | Es el reactivo que dosifica la peristaltica para bajar el pH de la solucion. NO confundir con los estandares de calibracion, que son otra cosa aunq… |
| Estandar de calibracion pH 4.01 | 2 pza | $40 | $80 | **solo en línea** | ESTANDAR DE CALIBRACION, no toca el cultivo. Calibracion quincenal, con evento programado en Home Assistant |
| Estandar de calibracion pH 6.86 (o 7.01) | 1 botella | $150 | $150 | HANNA: Vainilla 462 *(+1 opc.)* | El segundo punto de la calibracion. 6.86 y 7.01 son dos estandares distintos pero equivalentes para este uso: usa el que consigas |
| Solucion de calibracion EC 1413 uS/cm | 1 pza | $459 | $459 | Vainilla 462 *(+1 opc.)* | Caducidad de 5 anos cerrada. Presupuesto anual de calibracion mas sonda: ~$1,050 |
| Sonda de pH del deposito NFT | 1 pza | $318 | $318 | UNIT Electronics Copilco *(+1 opc.)* | Etapa 1: valida el lazo de control. El kit DFRobot NO se compra hasta que el NFT facture: su electrodo caduca a los 12-18 meses aunque siga en la caja |
| Sonda EC/TDS FIJA del retorno (SEN0244) | 1 pza | $253 | $253 | UNIT Electronics Copilco | Es la sonda fija que lee ESPHome, montada en el RETORNO. No confundir con el medidor de mano, que es el arbitro |
| Bombas peristalticas 12 V (A, B, pH- y repuesto) | 4 pza | $225 | $900 | **solo en línea** | La manguera interna es consumible: se reemplaza, no se repara |
| Valvula solenoide 12 V 1/2 NC | 2 pza | $128 | $256 | UNIT Electronics Copilco | NC (normalmente cerrada): un corte de luz NO vacia el tinaco |
| ESP32-CAM OV2640 | 1 pza | $260 | $260 | UNIT Electronics Copilco | Timelapse e inspeccion remota |
| Sensor de flujo YF-S201 | 1 pza | $64 | $64 | UNIT Electronics Copilco | Watchdog de bomba tapada o linea rota |
| *Separador de primeras lluvias (Paquete Basico Tlaloc)* | 1 sistema | $5,300 | — *($5,300)* | — | NO SUMA: es la MISMA funcion que la partida F1-010, que ya se decidio y se pago en Fase 1. Si en Fase 1 elegiste el DIY de $1,500 y ahora quieres e… |
| Filtro duplex de sedimento 5 um + carbon activado 10 pulg | 1 juego | $1,000 | $1,000 | Home Depot Coapa del Hueso | Solo en la linea que llena el deposito NFT: quita el cloro. Los CARTUCHOS son consumible cada 4-6 meses, no compra unica |
| Medidor de mano pH + EC (arbitro de calibracion) | 1 pza | $450 | $450 | Vainilla 462 *(+1 opc.)* | Es el ARBITRO: con el operas en manual las primeras semanas y con el detectas que la sonda fija se descalibro. No sustituye a la sonda fija ni al r… |
| Semilla de albahaca para el NFT | 1 oz | $549 | $549 | Ignacio Allende 21 *(+1 opc.)* | Nufar es resistente a fusarium, que es el riesgo tecnico #3 del plan. Estaba AGOTADA al 12-sep-2026: si no hay reabasto, cambia a la opcion Genoves… |
| Cultivos hidroponicos (Resh, 5a ed. en espanol) | 1 pza | $899 | $899 | El Pendulo Coyoacan (pedido) | Comprar con los ingresos de Fase 1. Es el porque de las bandas de pH y EC |
| Bateria LiFePO4 12.8 V 100 Ah | 1 pza | $4,459 | $4,459 | Solar Center: Av. Central 154 *(+2 opc.)* | 28-30 h de recirculacion continua. Es el corazon de la arquitectura DC-first: un apagon no mata el NFT |
| Bombas de recirculacion NFT 24/7 DC (principal + respaldo) | 2 pza | $650 | $1,300 | Hydro Environment *(+1 opc.)* | ARQUITECTURA DC-FIRST: la bomba del NFT que corre 24/7 es de 12 V y cuelga del bus de bateria. La de 127 V solo hace llenado y purga. POR VERIFICAR… |
| Controlador de carga solar (cargador de la LiFePO4) | 1 pza | $599 | $599 | Vallejo (Solar Center *(+1 opc.)* | Requisito duro: que tenga perfil LiFePO4 configurable |
| Panel solar 100 W | 1 pza | $1,049 | $1,049 | Abaco Solaris: Calle de America 173-1 *(+1 opc.)* | Opcional pero recomendado: flota la bateria sin CFE. Un corte diurno se vuelve sostenible indefinidamente |
| Fusiblera 12 V, seccionador DC y gabinete del bus | 1 lote | $700 | $700 | AutoZone y Steren en Coyoacan; el seccionador DC en Vallejo | PARTIDA NUEVA: las notas del BOM viejo la estimaban en $500-900 y ningun renglon la sumaba |
| Envio de las partidas que no tienen mostrador (panel, bateria) | 1 lote | $158 | $158 | **solo en línea** | PARTIDA NUEVA: el envio del panel aparecia en las notas y nunca se sumaba. Si compras presencial en Vallejo o Coyoacan, esta partida se va a cero |
| *No-break del cerebro y el router* | 1 pza | $1,189 | — *($1,189)* | — | NO SUMA: es la misma funcion que F1-021, ya comprada. Solo se recompra si el de Fase 1 no sostiene 45 min con el cerebro y el modem. Comprobalo con… |
| *Breaker GFCI del circuito del patio* | 1 pza | $1,159 | — *($1,159)* | — | NO SUMA: movida a F1-032. El proyecto la exige en la S13 de Fase 1, antes de energizar el primer rele del patio. Estaba presupuestada en las dos fases |
| *Tapa intemperie + varilla copperweld + cable cal. 8* | 1 lote | $900 | — *($900)* | — | NO SUMA: movida a F1-033 |
| *Electricista certificado* | 1 servicio | $2,500 | — *($2,500)* | — | NO SUMA: movida a F1-034 |
| Refrigerador 9-11 pies (producto cortado a 4-5 C) | 1 pza | $4,000 | $4,000 | Home Depot Coapa del Hueso *(+1 opc.)* | Cortado a 20-25 C dura menos de un dia; a 5 C dura 14. Suma 25-40 kWh/mes al calculo de la tarifa DAC: metelo en la cuenta antes de comprarlo |
| Hielera rigida 45-50 L + 6 gel packs (reparto) | 1 juego | $1,300 | $1,300 | Home Depot Coapa del Hueso | Pre-enfriar el producto la noche anterior. Objetivo: menos de 10 C durante 4-6 h de ruta |
| *Responsabilidad civil PyMEs con RC de productos* | 1 poliza | $500 | — *($500)* | Agentes en CDMX | NO SUMA AL TOTAL DE INVERSION porque es un gasto RECURRENTE (~$500/mes, $3,000-8,000/ano), no capital. Solo cuando entre un cliente corporativo u h… |

## Archivos fuente

| Archivo | Qué es |
|---|---|
| [`bom/partidas.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/partidas.csv) | Las 96 partidas. Una fila = una compra. |
| [`bom/opciones.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/opciones.csv) | Las 135 opciones de proveedor. Sin subtotal: no puede inflar nada. |
| [`tools/gen_bom.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gen_bom.py) | Valida la aritmética y regenera esta página. |

De las 96 partidas, **86 tienen al menos una opción con mostrador físico**.

<!-- Generado por tools/gen_bom.py. No editar a mano: los cambios van en los CSV. -->
