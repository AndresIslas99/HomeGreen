# Instalar el tinaco y la captación pluvial

**En una línea:** pones un tinaco de 750 L sobre base firme, le conectas el canalón del túnel
con filtro de hojas y separador de primeras lluvias, sacas de ahí toda la línea de riego (nunca
de la toma directa), mides EC y pH del agua de red y de lluvia, y dejas lista la solicitud a
Cosecha de Lluvia — para que el tandeo de tu alcaldía no decida cuándo riegas.

!!! info "Antes de empezar"
    - **Tiempo:** base y tinaco medio día (S8–9, mientras el herrero fabrica) · canalón, filtro y tlaloque medio día (S11–12, con el esqueleto montado) · línea de riego y cebado 2 h (S12) · medir EC/pH 5 min × 3 días · **Costo:** tinaco $2,051 + captación DIY ~$1,500 (`bom/fase1.csv`); rango del informe $4,500–5,500 con medidor de mano ([research/agua-captacion](../../research/agua-captacion.md)) · **Personas:** 1 (2 para mover el tinaco)
    - **Necesitas:** tinaco Rotoplas Resistec 750 L (o Plus+ 1,100 L), 2–4 tramos de canalón PVC blanco 3.07 m con uniones, tapas, soportes y bajante de 3", tubo PVC 4" + tapón de registro para el tlaloque casero, malla inoxidable para el filtro de hojas, brida y multiconector 1½", válvula de paso, filtro de sedimentos, manguera y kit de nebulizadores, bomba de diafragma 12 V, medidor pH/TDS-EC de mano (~$300–600 aprox., [ML](https://listado.mercadolibre.com.mx/medidor-ph-tds-ec)), nivel de 24", taladro, teflón, cinta métrica ([compras S7](compras.md), [04-herramientas](../../referencia/04-herramientas.md)).
    - **Prerequisitos:** decisión ④ de [Antes de gastar un peso](../../empieza-aqui/antes-de-gastar-un-peso.md) (tandeo de tu colonia en [Agua en tu Colonia](https://aguaentucolonia.sacmex.cdmx.gob.mx)); esqueleto del túnel montado para la canaleta ([túnel §14](tunel.md)); [Hidráulico](../../diseno/hidraulico.md) para los porqués y las secuencias de llenado y purga.

## Cómo queda

![P&ID de captación pluvial: techo del túnel, canalón PVC con pendiente 0.5–1 %, bajante, filtro de hojas, separador de primeras lluvias, tinaco de 750 L con rebosadero a la coladera, flotador de red SACMEX, sensor de nivel JSN-SR04T y DS18B20](../../assets/diagramas/hidraulico/captacion-pluvial.svg)

Techo del túnel → canalón con pendiente 0.5–1 % → bajante de 3" → **F-3 filtro de hojas**
(sólidos > 1 mm) → **SP-1 separador de primeras lluvias** (los primeros 20–40 L que lavan
polvo y hollín se quedan en un tubo ciego con purga) → **TK-1 tinaco 750 L** por la tapa →
rebosadero a la coladera. La red entra por la válvula de flotador FV-1 y **solo rellena cuando
hay presión**. LT-1 (JSN-SR04T) en la tapa y TT-1 (DS18B20) sumergido van al nodo de riego.

![P&ID del riego de microgreens: tinaco 750 L, válvula V-1, filtro de sedimentos F-1, bomba de diafragma 12 V con presostato P-1, manifold con una válvula por nivel y nebulizadores en los niveles N1–N4 del rack; drenaje a la coladera](../../assets/diagramas/hidraulico/riego-microgreens.svg)

TK-1 → **V-1** válvula de paso → **F-1** filtro de sedimentos → **P-1** bomba de diafragma 12 V
con presostato (4–6 L/min, ~20 W, relé K1 del nodo) → manifold con una válvula manual por
nivel → 2 nebulizadores por nivel en N1–N4. N5 (oscuridad) se atomiza a mano. El drenaje de
las charolas va a una charola colectora y a la coladera: **no recircula** (agua con sustrato y
raíces = moho).

!!! danger "La regla de esta página"
    **Todo el sistema corre desde el tinaco, nunca de la toma directa.** Hay tandeo formal en
    ~10 alcaldías / 284 colonias (2025–2026); la red solo rellena el tinaco cuando hay presión y
    el flotador lo hace solo. Autonomía mínima: 2 semanas
    ([02 §2](../../referencia/02-restricciones-y-requisitos.md)).

## Pasos

### Tinaco (S8–S9, mientras el herrero fabrica)

1. **Elige el tamaño con el tandeo de tu colonia.** Resistec 750 L ($2,051, mejor $/litro) es
   la reserva de Fase 1; en alcaldía de tandeo duro (Tlalpan, Iztapalapa, Xochimilco, Tláhuac,
   Milpa Alta) sube a Plus+ 1,100 L ($3,774) desde ahora, no como upgrade. Con consumo de
   1–3 m³/mes, 750 L cubren 7–22 días y 1,100 L 11–33 días
   ([Hidráulico §4](../../diseno/hidraulico.md)).
   *Criterio de listo:* tamaño decidido con la consulta de SACMEX impresa o capturada.
2. **Arma la base al nivel del patio, junto a la coladera** (posición del layout: esquina
   noreste, bajo la bajante). Piso firme y plano: **lleno pesa ~750 kg; nunca sobre estructura
   ligera** ni tapando la coladera. Sombra u opaco: luz + agua = algas; si le pega el sol,
   fórralo o píntalo.
   *Criterio de listo:* nivel de 24" en dos direcciones sobre la base; rebosadero apuntando a
   la coladera.
3. **Conecta la red a FV-1 (flotador) y deja llenar** hasta que cierre. Cronometra el llenado:
   es tu referencia de presión de red. El Resistec es la línea "sin accesorios"
   [POR VERIFICAR: precio del flotador, jarro de aire y multiconector sueltos en Home Depot;
   alternativa: Tricapa 750 L "con accesorios" $3,549 que trae flotador, jarro de aire,
   multiconector y filtro de sedimentos]. Brida 2.3" $48 y multiconector 1½" $97 en la misma
   línea de Home Depot.
4. **Salida inferior:** multiconector → V-1 válvula de paso → F-1 filtro de sedimentos (el
   estándar del tinaco equipado basta para microgreens; suelto, Polyspun 1–5 µm $825 en
   [Agua Limpia](https://www.agualimpia.mx/collections/filtro-para-sedimento-y-carbon-activado)).
   Abre V-1 sin bomba unos segundos para arrastrar el polvo de fábrica; cierra.
   *Criterio de listo:* sin goteo en brida ni multiconector tras 24 h lleno.

### Captación (S11–S12, con el esqueleto montado)

5. **Canalón en cada alero** con soportes al larguero bajo y pendiente **0.5–1 % (1 cm por cada
   2 m)** hacia la bajante: 2 tramos de 3.07 m por alero de 6 m ($269 c/u en Home Depot;
   uniones, tapas y soportes ~$40–120 c/u, verificar en tienda). Alero norte → bajante NE al
   tinaco; alero sur → bajante SE y colector aéreo a 2 m hacia la NE. El canalón galvanizado
   "de invernadero" ($1,849/3 m) está sobredimensionado para 18 m².
   Paso a paso con cortes y uniones: [Instalar canaleta y captación](../../guias/instalar-canaleta-y-captacion.md).
   *Criterio de listo:* un vaso de agua en el extremo alto llega a la bajante sin charcos.
6. **Filtro de hojas F-3** en la boca de la bajante: malla inoxidable que retiene sólidos
   > 1 mm, accesible para limpiarlo con la mano.
7. **Separador de primeras lluvias casero (tlaloque) SP-1:** un tramo **vertical de PVC de 4"
   con tapón de registro abajo**, en T con la bajante antes del tinaco. La lluvia llena primero
   ese tubo ciego (los primeros 20–40 L que lavan el techo); cuando está lleno, el agua limpia
   sigue al tinaco. Diseño idéntico al Tlaloque de Isla Urbana; material ~$400–800 de
   tlapalería; el
   [manual oficial del Kit Tláloc (PDF gratis)](https://www.engineeringforchange.org/wp-content/uploads/2020/07/MANUAL-INSTALACI%C3%93N-KIT-TL%C3%81LOC-12-JUNIO-2019CH.pdf)
   trae las figuras. [POR VERIFICAR: un tubo de 4" guarda ~7.9 L por metro (aritmética
   π × 0.05² × 1,000); para 20–40 L necesitas 2.5–5 m de tubo o un cuerpo de 6" (~18 L/m):
   dimensiona el volumen con el manual y el largo disponible bajo el alero]. Video DIY (no
   verificado): [filtro de primeras aguas](https://www.youtube.com/watch?v=V7mJn552myA).
   *Criterio de listo:* con la manguera sobre el techo, el tubo ciego se llena primero y luego
   sale agua clara al tinaco; el tapón de purga abre y cierra sin fuga.
8. **Entrada al tinaco por la tapa** con rebosadero a la coladera. En Fase 2 se agrega el
   reductor de turbulencia (Axolote) del Paquete Básico Tláloc ($5,300) o se aplica al programa
   gratuito (paso 12).
9. **Purga después de cada tormenta:** abrir el tapón del tlaloque, vaciar, cerrar. Va en el
   ritmo semanal del [índice](index.md). Sin separador, la primera lluvia mete hollín al tinaco.

### Sensores y línea de riego (S12)

10. **LT-1 y TT-1:** JSN-SR04T en la tapa apuntando al agua sin obstáculos, con **≥ 20 cm de
    colchón sobre el nivel máximo** (zona muerta); DS18B20 sumergido. Se conectan al nodo en
    [automatización v1 §4](automatizacion-v1.md); alarma "tinaco bajo" desde el día 1.
    *Criterio de listo:* HA lee 100 % con el flotador cerrado y baja al abrir V-1 a chorro.
11. **Ceba y ajusta la línea:** V-1 abierta → P-1 (autocebante: en < 30 s sale agua por el
    nivel más lejano; si no, F-1 tapado o aire en la succión) → ajusta cada válvula del
    manifold hasta que las boquillas de N1–N4 rocíen parejo; anota la posición. Purga de
    temporada cada 2–3 meses: quitar boquillas, 1 min a chorro por nivel, lavar el cartucho de
    F-1 ([Hidráulico §5.2](../../diseno/hidraulico.md)). Diámetro de la manguera del kit
    [POR VERIFICAR: en la ficha del kit de nebulizadores que compres].
    *Criterio de listo:* los 4 niveles rocían parejo con el presostato cortando solo al cerrar
    todas las válvulas.

### Medir el agua (V7) y aplicar a Cosecha de Lluvia

12. **Mide EC y pH de la llave 3 días distintos** con el medidor de mano (adelanta esa compra
    de Fase 2, ~$400) y del agua captada tras la primera tormenta útil. Ese número decide la
    ruta del NFT de Fase 2 ([V7](../../validacion/v07-agua.md)):

    | EC del agua de red | Diagnóstico | Acción |
    |---|---|---|
    | < 0.4 mS/cm (típico poniente/centro, Cutzamala) | Excelente | Directo; solo carbón activado para el cloro en la línea NFT |
    | 0.4–0.8 mS/cm | Usable | OK para microgreens; para NFT mezclar 50/50 con lluvia y restar Ca/Mg del agua a la fórmula |
    | > 0.8–1.0 mS/cm (oriente/sur, pozos) | Mala para NFT | La banda objetivo 1.2–1.8 mS/cm ya incluye nutrientes: lluvia como fuente principal o RO |

    El agua de lluvia debe salir con **EC 0.02–0.06 mS/cm**, sin cloro: es la fuente premium
    para NFT y un argumento de venta con los chefs.
    *Criterio de listo:* 3 lecturas de red + 1 de lluvia con fecha, en el issue de V7
    [POR VERIFICAR: si `tools/kpis.py` va a leer un `bitacora/agua.csv`, definir columnas
    `fecha,fuente,ec_ms_cm,ph`].
13. **Cosecha de Lluvia (SEDEMA): gratis si tu alcaldía califica.** Convocatoria
    **enero–febrero**; alcaldías elegibles en convocatorias recientes: Iztacalco, Iztapalapa,
    Tláhuac, Tlalpan, Venustiano Carranza y Xochimilco (colonias específicas). Requisitos:
    mayor de edad en colonia elegible, CURP, INE vigente, comprobante de domicilio ≤ 3 meses,
    boleta predial (hasta 2 años) u opinión técnica de uso de suelo, carta compromiso,
    pláticas comunitarias y visitas técnicas. Pre-registro:
    **programascall@sedema.cdmx.gob.mx** y portal
    [cosechalluvia.sedema.cdmx.gob.mx](https://cosechalluvia.sedema.cdmx.gob.mx/)
    ([página del programa](https://www.sedema.cdmx.gob.mx/programas/programa/cosecha-de-lluvia)).
    Instalan un sistema tipo Isla Urbana de ~$20,000 sin costo. Si no calificas: Paquete
    Básico Tláloc $5,300 en Fase 2. Guía completa: [Aplicar a Cosecha de Lluvia](../../guias/aplicar-cosecha-de-lluvia.md).
    *Criterio de listo:* documentos escaneados en una carpeta desde diciembre; correo de
    pre-registro enviado la primera semana de la convocatoria.

!!! example "Cuánta agua es"
    Regla: **1 mm de lluvia = 1 L por m² de techo.** Techo de 18 m² con coeficiente 0.9: una
    tormenta de 30 mm ≈ 490 L (el informe redondea 500–600 L para 15–20 m²); al año, con la
    media de 650 mm que usa el informe, ≈ 10,500 L (8,800 L para 15 m²; Tacubaya registra
    847 mm/año, concentrados de finales de mayo a inicios de octubre). El sistema consume
    ~1–3 m³/mes: **en temporada de lluvias la captación cubre 80–100 %**
    ([research/agua-captacion §b](../../research/agua-captacion.md)).

!!! warning "Error típico"
    Tinaco negro al sol sin forrar (algas en 2 semanas y agua a 30 °C que la bomba manda a las
    charolas), canalón "a nivel" que se encharca y desborda por el lado equivocado, y placas
    del túnel o el propio tinaco tapando la coladera: la tormenta que capturas por arriba te
    inunda por abajo.

## Puesta en marcha del agua

- [ ] Tinaco nivelado sobre base firme, opaco o a la sombra, rebosadero a la coladera, sin goteos a las 24 h
- [ ] Flotador cierra; tiempo de llenado de red anotado
- [ ] Canalón con pendiente verificada; filtro de hojas y tlaloque montados; el tubo ciego se llena primero
- [ ] **Captación llenando el tinaco** con una lluvia real (o manguera sobre el techo) y **EC del agua captada medida** ([03 §commissioning Fase 1](../../referencia/03-instalacion.md))
- [ ] LT-1 lee en HA; alarma "tinaco < 40 %" configurada
- [ ] Línea de riego cebada, 4 niveles parejos, drenaje a coladera

## Al terminar

- [ ] Checklist de puesta en marcha completo
- [ ] 3 lecturas de EC/pH de red + 1 de lluvia registradas con fecha
- [ ] Documentos de Cosecha de Lluvia en carpeta; fecha de la convocatoria en el calendario
- Registrar: issue "Agua" con este checklist; lecturas de V7 en su issue; en `bitacora/produccion.csv` la primera siembra regada desde el tinaco lleva `observaciones` "riego desde tinaco"
- Siguiente paso: [Armar la automatización v1](automatizacion-v1.md)

## Fuentes

- [research/agua-captacion](../../research/agua-captacion.md) §a (tinacos), §b (captación y dimensionamiento), §c (Cosecha de Lluvia), §d (tandeo), §e (calidad y tabla de EC), §f (filtros)
- [research/instalacion-tunel-detalle §4](../../research/instalacion-tunel-detalle.md) (canalón, pendiente, purga de primeras lluvias, peso del tinaco)
- [03-instalación §1.2](../../referencia/03-instalacion.md) · [02 §2 agua](../../referencia/02-restricciones-y-requisitos.md) · [Hidráulico §1, §3, §4, §5](../../diseno/hidraulico.md)
- [06-validación V7](../../referencia/06-validacion-y-lazos-agenticos.md) · [01-proveedores §5](../../referencia/01-proveedores-cdmx.md) · [research/tutoriales-videos §f](../../research/tutoriales-videos.md)
