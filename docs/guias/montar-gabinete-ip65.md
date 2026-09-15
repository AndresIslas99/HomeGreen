# Montar un gabinete IP65 en el patio

**En una línea:** fijas cada gabinete del patio (GAB-A de 127 V; GAB-1, GAB-2 y GAB-DC de 12 V) con todas las prensaestopas por la cara de abajo, un solo voltaje por caja, cada cable con lazo de goteo y etiqueta en los dos extremos, y los sensores con el conector hacia arriba — porque el patio es "lugar mojado" y la electrónica "al aire" o en caja de interior es la fuente goteada que un día se incendia o dispara el GFCI.

!!! info "Antes de empezar"
    - **Tiempo:** 2–3 h el primer gabinete, la mitad los siguientes (estimado) · **Costo:** gabinete IP65 ~300 × 300 × 90 mm ~$250–600 c/u aprox. (el BOM de Fase 1 presupuesta 2 × $350 = $700 con prensaestopas), prensaestopas PG ~$10–20 c/u aprox., termofit desde $13 el tramo, cinchos ~$40–90 las 100 pzas; borneras, barra, fusibles y cable dentro del material de soporte (~$1,000 en AG Electrónica) ([research/herramientas §c](../research/herramientas.md), [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv)) · **Personas:** 1
    - **Necesitas:** [gabinete plástico IP65 para exterior](https://listado.mercadolibre.com.mx/gabinete-plastico-exterior-ip65) (ABS, sello de silicón, −20 a 60 °C; alternativa [Bsai 300 × 300 × 90 mm](https://www.bsai.com.mx/products/gabinete-plastico-para-exterior-ip65-de-300-x-300-x-90-mm-cierre-por-tornillos), precio [POR VERIFICAR: la tienda devolvió error al verificar]) · prensaestopas PG, **uno por cable**, del diámetro del cable, más tapones ciegos · placa de montaje (si el gabinete no la trae, una de acrílico o MDF sellado [POR VERIFICAR: si el modelo comprado incluye placa]) · borneras, barra negativa (12 V) o bornera de tierra (127 V), fusiblera o portafusibles, separadores y tornillería · [termofit](https://www.steren.com.mx/catalogsearch/result/?q=termofit), cinchos, cinta y marcador indeleble ([Steren](https://www.steren.com.mx/herramientas)) · taladro con broca o sierra copa del diámetro de la rosca del prensaestopa [POR VERIFICAR: mide la rosca del prensaestopa comprado] · para muro: [rotomartillo Truper 650 W $660](https://www.homedepot.com.mx/p/truper-rotomartillo-1-2-650w-truper-pro-roto-1-2a7-231999) y [taquetes](https://www.homedepot.com.mx/s/taquete); para columna de PTR: abrazaderas o cinchos metálicos · nivel torpedo · [multímetro](https://www.steren.com.mx/multimetro-compacto-economico.html) · atomizador con agua (prueba de estanqueidad) · [lentes de seguridad $40](https://www.homedepot.com.mx/s/lentes+seguridad)
    - **Prerequisitos:** [Instalar GFCI y tierra](instalar-gfci-y-tierra.md) recibido; [Diseño eléctrico](../diseno/electrico.md) leído (esquemas, tabla de cableado, colores, protecciones); posición de cada gabinete en [Layout del patio](../diseno/layout-patio.md); el nodo ya flasheado y probado en la mesa ([Flashear ESPHome](flashear-esphome.md)) — al gabinete solo llega electrónica que ya funcionó en banco ([03-instalación §1.3](../referencia/03-instalacion.md))

## Qué gabinete va dónde

![Tablero del patio: del contacto WR con tapa in-use, clavija de uso rudo al gabinete A de 127 V y de ahí 12 V al gabinete B; tierra de equipo al chasis de ambos y a la barra del tablero](../assets/diagramas/electrico/tablero-gfci-tierra.svg)

| Gabinete | Voltaje | Contenido | Dónde (layout) | Fase |
|---|---|---|---|---|
| **GAB-A** | 127 V CA | Bornera L/N/T, fuente Steren ELI-1260 12 V 5 A, relé de potencia K5 (tubos T8 y extractor), fusible F5 2 A de luces; en Fase 2 recibe el cargador LiFePO4 | Pared de la casa bajo el cobertizo, a 1.5 m; cordón SJT de uso rudo de 1 m desde el contacto WR con tapa "in-use" | 1 |
| **GAB-1** | 12 V CC | Nodo de riego v1: ESP32, módulo relé 4 ch, buck 5 V, fusibles F0 5 A · F1 5 A bomba · F2 2 A extractor · F3 1 A bobina K5, barra GND, borneras de MT-1…4, SHT31, DS18B20, JSN-SR04T | Columna NE interior del túnel, a 2.0 m: ≤ 1.5 m del rack testigo, ≤ 2 m del tinaco y de P-1 [POR VERIFICAR: [Fase 1 · Automatización v1](../fases/fase-1/automatizacion-v1.md) lo ubica en el poste sureste a 1.2 m; decide con el patio real y corrige la página que no aplique] | 1 |
| **GAB-2** | 12 V CC | Nodo NFT v2: ESP32, driver MOSFET 5 ch, módulo relé 2 ch (K1/K2), buck, placa pH y TDS, detector de red (PC817), divisor 47k/10k | Columna sur del túnel (x ≈ 4.6 m), a 1.5 m: 1.6 m a las sondas del retorno, 1.7 m a las bombas, 0.6 m del bus 12 V | 2 |
| **GAB-DC** | 12 V CC (potencia) | Batería LiFePO4 100 Ah, cargador/EPEVER, F0 30 A, S1, fusiblera 6 vías, barra negativa | Pared de la casa bajo el cobertizo, batería a 30 cm del piso, **caja separada de GAB-A** | 2 |
| GAB-3 | 12 V CC | Driver del gantry | Pared de la casa | 3 |

Los gabinetes de interior Steren ([GP-14 $199, GP-02/04](https://www.steren.com.mx/catalogsearch/result/?q=gabinete)) sirven **solo bajo techo** (cuarto de cosecha, cerebro); nada de lo que se moja va en ellos. El cerebro (mini PC + router + UPS) vive dentro de casa, no en el túnel: humedad y robo ([07 §10](../referencia/07-puntos-ciegos-y-riesgos.md)).

## Distribución interior

Regla 2 del diseño: **127 V CA y 12 V CC nunca en el mismo gabinete** ni compartiendo prensaestopa ([Diseño eléctrico](../diseno/electrico.md)). Dentro de cada caja: potencia abajo, lógica arriba, señales por un lado y potencia por el otro.

=== "Gabinete de 12 V (GAB-1 / GAB-2)"

    ```text
    ┌──────────────────────────────────────────────┐  ← tapa con empaque: NUNCA se perfora
    │  LÓGICA (mitad superior)                      │
    │  [ESP32 DevKit]   [buck LM2596 a 5.0 V]       │  buck → VIN ≤ 30 cm; nada metálico delante de la antena
    │  [borneras de sensores: 3V3 · GND · señal]    │  22–24 AWG; amarillo = analógico, azul/blanco = I2C
    │  [placa pH / TDS]   [PC817 detector de red]   │  (solo GAB-2)
    ├──────────────────────────────────────────────┤
    │  POTENCIA (mitad inferior)                    │
    │  [fusiblera / portafusibles etiquetados]      │  cada fusible protege un cable
    │  [módulo relé 4 ch]  o  [MOSFET + relé 2 ch]  │  módulo relé alimentado del 5 V del buck (VCC y JD-VCC)
    │  [barra GND en estrella]   [bornera +12 V]    │  cada carga regresa por su propio negro
    └──┬────┬────┬────┬────┬────┬──────────────────┘
       PG   PG   PG   PG   PG   PG   ← cara INFERIOR: un prensaestopa por cable, lazo de goteo debajo
      12 V bomba vent. sens. sens. tapón
    ```

    - Señal (sensores) por la mitad izquierda, potencia (bomba, extractor) por la derecha; no corren juntas pegadas en paralelo.
    - La tierra física de 127 V **no** llega a la barra GND de 12 V; en un gabinete de CC solo hay tierra de equipo si tiene placa metálica.
    - GAB-DC es solo potencia: batería en el fondo (a 30 cm del piso), F0 a ≤ 30 cm del borne +, S1, fusiblera y barra en la mitad superior; el cargador o el EPEVER con aire alrededor ([Armar el respaldo DC](armar-respaldo-dc.md)).

=== "Gabinete de 127 V (GAB-A)"

    ```text
    ┌──────────────────────────────────────────────┐
    │  [bornera L · N · T]  ← cordón SJT 3 × 14 AWG del contacto WR (prensaestopa propio)
    │  [fuente 12 V 5 A ELI-1260]   [cargador LiFePO4 (Fase 2)]
    │  [relé de potencia K5: T8 + extractor]   [F5 2 A luces]
    │  [bornera de tierra] → chasis de la fuente, canaleta de los T8, rack
    └──┬─────────┬─────────┬──────────┬────────────┘
       PG        PG        PG         PG
       127 V     12 V → GAB-1   T8 (127 V)   bobina K5 (12 V, señal desde GAB-1)
    ```

    - Solo el verde del cordón, la bornera de tierra y los chasis metálicos tocan la tierra física; N y T **nunca** se unen aquí (el puente vive en el centro de carga).
    - Las salidas de 12 V y la señal de K5 salen por prensaestopas propios hacia la troncal aérea (a 2.2 m, con mensajero de acero) rumbo a GAB-1.

## Pasos

### A. Planear en seco (20 min)

1. **Acomoda los componentes sobre la placa fuera del gabinete** según el croquis de arriba; deja un dedo de aire alrededor de fuente, buck y relés (calientan). Foto de referencia.
2. **Cuenta los cables que entran y salen** y asigna un prensaestopa a cada uno, más uno de repuesto con tapón. En GAB-1 son típicos: 12 V de entrada, bomba, extractor, 4 capacitivos (o un multiconductor), SHT31, DS18B20, JSN-SR04T. *Criterio de listo:* lista escrita cable → prensaestopa → diámetro.
3. **Marca la posición en el patio** con el layout: altura, lado de apertura de la puerta (no cruza el pasillo), sombra, fuera del goteo del techo y del alcance de los nebulizadores.

### B. Perforar (30 min)

4. **Solo la cara inferior.** Marca los centros de los prensaestopas en la cara de abajo, separados al menos un diámetro entre sí para que giren las tuercas; **nunca** la tapa, la cara superior ni los laterales: el agua entra por donde escurre.
5. **Perfora** con broca o sierra copa del diámetro de la rosca; desbarba por dentro y por fuera; empaque del prensaestopa por fuera, tuerca por dentro, apretado a mano más un cuarto de vuelta. Lentes puestos.
6. **Fijación del gabinete:** usa las orejas de montaje exteriores si las trae; si hay que perforar el fondo, cada tornillo lleva arandela de neopreno o un punto de silicón por dentro. *Criterio de listo:* con el gabinete a contraluz no se ve ningún hueco sin sellar.

### C. Montar la placa y los componentes (30 min)

7. **Placa con separadores** (nada atornillado directo al fondo); fusiblera y seccionador donde se alcancen sin desmontar nada; barra GND en la zona de potencia; borneras de sensores arriba.
8. **Fusibles etiquetados con valor y rama** ([lista de protecciones](../diseno/electrico.md)); bolsita con un repuesto de cada valor pegada por dentro de la puerta.

### D. Cablear (60 min)

9. **Colores:** CC rojo +12 V, negro GND, naranja +5 V, amarillo señales analógicas, azul/blanco I2C; CA negro L, blanco N, verde T. Calibres por tramo en la [tabla de cableado](../diseno/electrico.md): bomba 14 AWG, nodo 18 AWG, sensores 22–24 AWG, cordón SJT 3 × 14 AWG.
10. **Terminales crimpadas** (puntera en bornera, ojillo en barra) y **termofit en cada empalme**: obligatorio en 12 V que vive en humedad ([research/herramientas §c](../research/herramientas.md)). Cero cinta como aislamiento; cero empalmes fuera de caja.
11. **Tierra en estrella:** el negro de cada carga (bomba, extractor, peristálticas) regresa a la barra por su propio cable, nunca por el GND de un sensor; el módulo relé se alimenta del 5 V del buck (VCC y JD-VCC), no del 3V3 del ESP32.
12. **Buck ajustado a 5.0 V con multímetro antes de conectar el ESP32**; cable buck → VIN de 18–20 AWG y ≤ 30 cm; C4 100 nF en EN y capacitores del bloque de alimentación puestos ([alimentación del ESP32](../assets/diagramas/electrico/alimentacion-esp32.svg)).
13. **Lazo de goteo:** cada cable exterior baja por debajo del prensaestopa y sube para entrar, así el agua escurre antes de la rosca. Deja 20–30 cm de reserva enrollada dentro. *Criterio de listo:* tirando de cualquier cable desde fuera nada se mueve dentro (el prensaestopa lo sujeta).

### E. Sensores (30 min)

14. **Capacitivos de sustrato: conector HACIA ARRIBA y sellado** con esmalte o epóxica en el borde de la PCB; mueren por corrosión del conector, no del sensor. Cable de 3 hilos 22–24 AWG, máximo ~3 m. Del pack de 10, 20–30 % salen malos: prueba cada uno en la mesa antes de encintarlo ([research/electronica-automatizacion](../research/electronica-automatizacion.md)).
15. **SHT31 a 1.5 m en el centro del túnel**, protegido del goteo directo, cable blindado ≤ 2 m con pull-ups de 4.7 kΩ si el módulo no los trae. **DS18B20** sumergido (hasta 10 m con 4.7 kΩ). **JSN-SR04T** en la tapa del tinaco apuntando al agua sin obstáculos, sin alargar su cable más de 5 m [POR VERIFICAR: ficha del módulo]. **YF-S201** con divisor 10k/20k dentro del nodo.
16. **Electrodo de pH: el coaxial BNC no se alarga.** La placa pH queda a menos de 1 m del retorno (en GAB-2 o en una cajita IP65 chica junto al retorno) y lo que viaja al ESP32 es el cable de 3V3/señal.
17. **Cada sensor entra por su propio prensaestopa** (o un multiconductor por prensaestopa): nunca por el mismo que la bomba.

### F. Fijar, aterrizar y cerrar (30 min)

18. **Fija el gabinete** a la altura del layout: a muro con taquetes (rotomartillo), a columna de PTR con abrazaderas; nivelado; puerta hacia el lado con espacio. GAB-DC bajo techo, batería a 30 cm del piso, en caja distinta de GAB-A.
19. **Tierra de equipo (solo GAB-A):** verde del cordón SJT → bornera de tierra → chasis de la fuente y canaleta de los T8/rack. Nunca a tubería de agua ni al neutro; nunca a la barra GND de 12 V ([tablero](../assets/diagramas/electrico/tablero-gfci-tierra.svg)).
20. **Cierra:** empaque de la tapa limpio y en su canal, tornillos en cruz, prensaestopas apretadas sobre el cable, tapones ciegos en las vías sin cable. Opcional: una bolsita de sílica gel dentro contra la condensación de la temporada de lluvias (cámbiala cuando cambie de color).

### G. Probar (15 min)

21. **Con el breaker del patio abajo:** continuidad de tierra desde el chasis de la fuente en GAB-A hasta la barra de tierra del tablero ≈ 0 Ω (multímetro en continuidad).
22. **Prueba de agua:** atomizador (o manguera a chorro suave) 1 min sobre tapa, prensaestopas y lazos de goteo; abre: todo seco. Si entró agua es el empaque o un prensaestopa flojo; corrige antes de energizar.
23. **Breaker arriba:** el GFCI **no** dispara; el nodo aparece en HA; cada relé actúa desde HA; los sensores leen ([Configurar Home Assistant](configurar-home-assistant.md)). *Criterio de listo:* 10 min energizado sin disparo del GFCI ni reinicios del nodo.

### H. Etiquetar (15 min)

24. **Cada cable en los dos extremos** (origen → destino, calibre); **cada fusible** (valor + rama); **cada gabinete** con su nombre (GAB-A, GAB-1…), voltaje ("127 V" en ámbar) y fecha de montaje. Por dentro de la puerta: el esquema impreso ([Diseño eléctrico](../diseno/electrico.md)), la tabla de pines del nodo ([Firmware](../software/firmware.md)), la lista de fusibles y un cuadro para anotar la fecha del último TEST del GFCI y del último simulacro.

!!! warning "Error típico: prensaestopa por arriba o de lado"
    "Así el cable llega derecho". Y así también el agua. Toda entrada por abajo, con lazo de goteo; si un cable llega por arriba, se baja por fuera del gabinete y entra por abajo.

!!! warning "Error típico: un prensaestopa para dos cables"
    Ni dos cables cualesquiera (no sella) ni, peor, 127 V con 12 V. Un cable, un prensaestopa; un voltaje, un gabinete.

!!! warning "Error típico: caja de interior en el patio"
    El GP-14 de Steren es para el cuarto de cosecha. En el túnel, con lluvia y nebulizadores, solo IP65 con prensaestopas ([03-instalación §1.3](../referencia/03-instalacion.md)).

!!! warning "Error típico: conector del capacitivo hacia abajo"
    Dura una temporada de lluvias. Conector arriba, sellado, encintado.

!!! warning "Error típico: nodo que funcionaba en la mesa y no en el gabinete"
    GPIO12 quedó alto al encender (cable largo o módulo relé activo en bajo en ese pin), buck sin ajustar, o cable buck → VIN largo (brownout al transmitir Wi-Fi). Solución en [Firmware · problemas](../software/firmware.md).

## Al terminar

- [ ] Un voltaje por gabinete; GAB-A separado de GAB-1/GAB-2/GAB-DC; ningún prensaestopa compartido
- [ ] Todas las entradas por la cara inferior con lazo de goteo; tapa sin perforar; prueba de agua de 1 min en seco
- [ ] Buck a 5.0 V, tierra en estrella, termofit en todos los empalmes, fusibles etiquetados con repuestos en la puerta
- [ ] Sensores con conector hacia arriba y sellado; BNC del pH sin alargar
- [ ] Continuidad chasis → barra del tablero ≈ 0 Ω (GAB-A); GFCI no dispara con todo energizado; nodo en línea en HA
- [ ] Etiquetas en cables, fusibles y gabinete; esquema y tabla de pines dentro de la puerta
- Registrar en `bitacora/electrico.csv` (`fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones`): una fila `evento=gabinete_montado` por gabinete, con la lista de prensaestopas y "prueba de agua OK" en `observaciones` (evento nuevo: agrégalo a la lista de [Diseño eléctrico](../diseno/electrico.md)); foto del interior con la bitácora
- Siguiente paso: GAB-1 → [Fase 1 · Automatización v1](../fases/fase-1/automatizacion-v1.md) y [Dry-run V3](../validacion/v03-dry-run.md); GAB-2 y GAB-DC → [Armar el respaldo DC](armar-respaldo-dc.md)

## Fuentes

- [referencia/03-instalacion §1.3](../referencia/03-instalacion.md) — gabinete IP65, prensaestopas, conector hacia arriba, banco de pruebas primero
- [research/electrico-respaldo-seguridad §4](../research/electrico-respaldo-seguridad.md) — equipo apto para ambiente húmedo (Art. 110-11), gabinetes separados
- [research/herramientas §c](../research/herramientas.md) y [referencia/04-herramientas](../referencia/04-herramientas.md) — gabinete IP65 (ML/Bsai), prensaestopas PG, termofit, cinchos, Steren GP-14 solo bajo techo
- [diseno/electrico](../diseno/electrico.md) — reglas 2 y 6, tabla de cableado y colores, lista de protecciones, errores típicos · [diseno/layout-patio](../diseno/layout-patio.md) — posición de GAB-A/1/2/DC
- [fases/fase-1/automatizacion-v1 §3–4](../fases/fase-1/automatizacion-v1.md) — gabinetes A y B, fusibles del nodo de riego, sensores
- [research/electronica-automatizacion](../research/electronica-automatizacion.md) — capacitivos (20–30 % malos), AG Electrónica
- [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv) — gabinetes IP65 y material de soporte
