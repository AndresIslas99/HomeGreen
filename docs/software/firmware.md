# Firmware ESPHome de los nodos

**En una línea:** tres archivos YAML listos para compilar convierten cada ESP32 en un
controlador que riega, ventila, dosifica y protege la bomba del NFT por sí solo; aquí
está la tabla de pines de cada nodo, cómo instalar ESPHome, flashear por USB la primera
vez y por OTA después, calibrar cada sensor, cambiar setpoints y arreglar lo que suele fallar.

!!! info "Antes de empezar"
    - **Tiempo:** 1 h por nodo la primera vez (flasheo + verificación en la mesa); 10 min por OTA; calibración de capacitivos 20 min, de pH/EC 20 min cada 15 días. · **Costo:** $0 en software; cable USB de datos; buffers pH 4.01 $40 y patrón EC 1.413 mS/cm $459.36 verificados ([`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv)). · **Personas:** 1
    - **Necesitas:** laptop con Python 3.11+ (o el add-on de ESPHome en Home Assistant), cable micro-USB o USB-C **de datos**, multímetro, el ESP32 en la mesa con su buck ajustado a 5.0 V ([electrico.md §5](../diseno/electrico.md)), los sensores que vas a calibrar y un vaso de agua.
    - **Prerequisitos:** [Diseño eléctrico](../diseno/electrico.md) (gabinetes, buck, divisores), [Diseño de control](../diseno/control.md) (qué hace cada lazo), [Software](index.md) (red, cerebro, versiones). Guías paso a paso: [Flashear ESPHome](../guias/flashear-esphome.md), [Calibrar sondas pH/EC](../guias/calibrar-sondas-ph-ec.md).

## Los tres nodos

| Archivo | Fase | Dónde vive | Qué hace solo (sin HA) | Alimentación |
|---|---|---|---|---|
| [`nodo-riego-v1.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-riego-v1.yaml) | 1 | Gabinete B junto al rack | Riego por histéresis por nivel de rack (4 capacitivos), interlock por nivel de tinaco, máx. ciclos/h y duración máx. por ciclo; ventilación por HR/T con tiempo mínimo y forzado 10 min/h; fotoperiodo de luces T8; nivel y temperatura del tinaco; heartbeat | Fuente 12 V 5 A → buck 5 V |
| [`nodo-ambiente.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-ambiente.yaml) | 1+ (opcional) | Donde haga falta medir: a media longitud del túnel, zona de germinación o dentro de casa en invierno | T/HR con el segundo SHT31 del BOM, punto de rocío, VPD, alarmas de HR alta, T alta y helada; sin actuadores | Cargador USB 5 V |
| [`nodo-nft-v2.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-nft-v2.yaml) | 2 | Gabinete B del NFT, en el **bus de batería** | pH/EC calibrados con compensación de temperatura; dosificación por histéresis con tiempo muerto de mezcla (A → B → pH−) e interlocks por nivel, bomba y flujo; watchdog "bomba ON sin flujo" que arranca el respaldo; detector de red CFE; voltaje de batería; modo ahorro 15/15; llenado y purga con tiempo máximo; timeout de 30 s en cada peristáltica | F3 de la fusiblera del bus 12.8 V → buck 5 V |
| [`secrets.example.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/secrets.example.yaml) | — | Se copia a `secrets.yaml` (no se sube a Git) | Wi-Fi, clave API por nodo, contraseña OTA, red de rescate | — |

Los tres se validaron con `esphome config` **y compilaron completos** con `esphome compile` en
ESPHome 2026.6.5 (ESP-IDF 5.5.4, toolchain xtensa 14.2): riego 52.7 % de flash / 16.5 % de RAM,
NFT 52.3 % / 16.9 %, ambiente 50.3 % / 14.3 %. Exigen `min_version: 2025.1.0`. Framework `esp-idf`,
board `esp32dev` (DevKit V1 de 30 pines, [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv)).
Lo que **no** está probado todavía es el comportamiento en la placa real: eso lo hacen las pruebas
de la sección "Probar sin plantas" y el dry-run V3.
Los nombres de las entidades que exponen están en [datos.md §2](../diseno/datos.md).

## Tabla de pines por nodo

Regla: los pines viven en tres lugares — el YAML, el script del esquema en `hardware/electrico/`
y [electrico.md](../diseno/electrico.md). Si cambias uno, cámbialo en los tres. Solo **ADC1
(GPIO32–39)** para señales analógicas: ADC2 deja de funcionar en cuanto el Wi-Fi está activo.

### Nodo de riego v1

| GPIO | Función | Periférico | Componente ESPHome | Notas de cableado |
|---|---|---|---|---|
| 32 | ADC1_CH4 | Capacitivo MT-1 (nivel 1) | `adc` 12 dB → `copy` con `median` + `calibrate_linear` + `clamp` | Conector hacia arriba y sellado; ≤ 3 m de cable |
| 33 | ADC1_CH5 | Capacitivo MT-2 (nivel 2) | ídem | |
| 34 | ADC1_CH6 | Capacitivo MT-3 (nivel 3) | ídem | Solo entrada, sin pull-up interno |
| 35 | ADC1_CH7 | Capacitivo MT-4 (nivel 4) | ídem | Solo entrada |
| 21 | SDA | SHT31 (0x44) | `i2c` + `sht3xd` | Pull-ups 4.7 kΩ a 3V3 si el módulo no los trae; 1–2 m máx. |
| 22 | SCL | SHT31 | `i2c` | |
| 4 | 1-Wire | DS18B20 del tinaco (TT-1) | `one_wire` + `dallas_temp` | Pull-up 4.7 kΩ entre DQ y 3V3 |
| 5 | TRIG | JSN-SR04T (LT-1) | `ultrasonic` | Pin de arranque; como salida no estorba |
| 18 | ECHO | JSN-SR04T | `ultrasonic` | **Divisor 10 kΩ / 20 kΩ**: ECHO es de 5 V |
| 25 | K1 | Bomba diafragma 12 V (riego) | `switch` gpio `inverted: true` | Módulo relé activo en bajo |
| 26 | K2 | Ventilador 12 V | `switch` | |
| 27 | K3 | Luces T8 127 V vía relé de potencia K5 | `switch` | K5 vive en el gabinete de CA |
| 14 | K4 | Reserva: tapete térmico dic–feb o luz del nivel 5 | `switch`, `RESTORE_DEFAULT_OFF` | Emite un pulso al arrancar: por eso es la reserva |
| VIN | 5 V | Buck LM2596 | — | Nunca USB y VIN a la vez |
| 3V3 | 3.3 V | Capacitivos, SHT31, DS18B20 | — | Solo sensores |

### Nodo de ambiente (opcional)

| GPIO | Función | Periférico | Componente ESPHome | Notas |
|---|---|---|---|---|
| 21 | SDA | SHT31 (0x44; 0x45 con el puente ADDR) | `i2c` + `sht3xd` | Segundo SHT31 de `bom/fase1.csv` |
| 22 | SCL | SHT31 | `i2c` | |
| 4 | 1-Wire | DS18B20 extra (opcional) | `dallas_temp` (bloque comentado) | Tapete térmico, agua de remojo |
| 16 | Salida | LED de estado (opcional) | `status_led` (comentado) | Con 330 Ω a GND |
| USB | 5 V | Cargador de celular | — | |

### Nodo NFT v2

| GPIO | Función | Periférico | Componente ESPHome | Notas de cableado |
|---|---|---|---|---|
| 34 | ADC1_CH6 | Placa pH PH-4502C (Po) | `adc` 12 dB → `copy` con calibración de 2 puntos y compensación de T | RC 1 kΩ / 100 nF; Po ≤ 3.05 V ajustando el offset en buffer 4.01 |
| 35 | ADC1_CH7 | Placa TDS SEN0244 (AOUT) | `adc` → `copy` (EC en mS/cm, compensada a 25 °C, factor k) | RC 1 kΩ / 100 nF |
| 36 | ADC1_CH0 (VP) | Divisor 47 kΩ / 10 kΩ del bus 12.8 V | `adc` → `copy` × 5.7 (ajustable) | 14.6 V → 2.56 V |
| 4 | 1-Wire | DS18B20 del tambo (TT-2) | `one_wire` + `dallas_temp` | Pull-up 4.7 kΩ |
| 27 | PCNT | YF-S201 (FT-1), ≈ 450 pulsos/L | `pulse_counter` + `total` en litros | Divisor 10k/20k (señal Hall de 5 V) |
| 23 | Entrada | Detector de red CFE (PC817 desde cargador USB) | `binary_sensor` gpio `INPUT_PULLDOWN`, `delayed_on/off: 5s` | El GND del cargador USB **no** se une al del nodo |
| 25 | MOSFET | Peristáltica A (DP-1) | `switch`, timeout ≤ 30 s | 220 Ω gate, 10 kΩ pull-down, 1N5819 flyback |
| 26 | MOSFET | Peristáltica B (DP-2) | `switch`, timeout ≤ 30 s | |
| 33 | MOSFET | Peristáltica pH− (DP-3, AquAcid) | `switch`, timeout ≤ 30 s | |
| 12 | MOSFET | Solenoide llenado SV-1 (½" NC) | `switch`, timeout `llenado_max_min` | **Pin de arranque: pull-down 10 kΩ obligatorio**; nunca por módulo relé activo en bajo |
| 13 | MOSFET | Solenoide purga SV-2 (½" NC) | `switch`, timeout `purga_max_min` | |
| 32 | Relé K1 (contacto **NC**) | Bomba NFT principal P-1 | `switch` `inverted: false`, `RESTORE_DEFAULT_ON` | GPIO alto = relé sin excitar = NC cerrado = **bomba corriendo**; sin ESP32 la bomba corre |
| 14 | Relé K2 (contacto NO) | Bomba NFT respaldo P-2 | `switch` `inverted: true`, `RESTORE_DEFAULT_OFF` | El pulso de arranque de GPIO14 solo parpadea el respaldo |
| 16 | Entrada | Flotador "tambo alto" (LT-2) | `binary_sensor` `INPUT_PULLUP`, `inverted: true` | Contacto entre GPIO y GND que **cierra cuando la boya sube** (lleno) `[POR VERIFICAR: LT-2 no está en bom/fase2; flotador con contacto o segundo JSN-SR04T]` |
| 17 | Entrada | Flotador "tambo bajo" (LT-2) | `binary_sensor` `INPUT_PULLUP`, `inverted: true`, `delayed_on/off: 10s` | Contacto que **cierra cuando la boya cae** (nivel bajo). Sin flotador, los dos pines leen "abierto" y el interlock de nivel queda desactivado |
| VIN | 5 V | Buck desde F3 del bus | — | |

!!! note "Diferencia con la tabla de electrico.md"
    La tabla de [electrico.md](../diseno/electrico.md) propone K1 en GPIO14 y K2 en GPIO32 y lo marca
    `[POR VERIFICAR: que coincida con el YAML]`. El firmware usa **GPIO32 para la principal (K1 NC) y
    GPIO14 para el respaldo (K2 NO)**, porque GPIO14 emite un pulso breve al arrancar el ESP32: en el
    respaldo (normalmente apagado) es un parpadeo inofensivo; en la principal sería un corte breve
    en cada reinicio. El YAML es la fuente de verdad; la tabla de electrico.md y el script
    `hardware/electrico/nodo_nft_v2.py` deben actualizarse `[POR VERIFICAR]`. Los pines del YAML
    del informe ([research/electrico-respaldo-seguridad §5.1](../research/electrico-respaldo-seguridad.md))
    también difieren (usaba GPIO34 batería, GPIO26 red, GPIO25/33 bombas); la lógica es la misma.

## Instalar ESPHome

=== "Add-on en Home Assistant (recomendado)"

    1. En HA: **Ajustes → Complementos → Tienda de complementos → ESPHome** → Instalar → Iniciar → activa "Mostrar en la barra lateral".
    2. Abre ESPHome → menú ⋮ (arriba a la derecha) → **Secrets** → pega el contenido de [`secrets.example.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/secrets.example.yaml) con tus valores (las claves API se generan con `openssl rand -base64 32` o con el botón del propio add-on). *Criterio de listo:* el editor guarda sin error.
    3. **+ New device → Continue** → nombre `nodo-riego-v1` → elige ESP32 → al terminar el asistente, **Edit** y sustituye todo el contenido por el YAML del repo. Repite para cada nodo.
    4. Botón **Validate**: debe terminar en "Configuration is valid". Si marca un secret faltante, revisa el paso 2.

=== "Laptop con Python (línea de comandos)"

    1. Crea un entorno e instala ESPHome:
       ```bash
       python3 -m venv ~/esphome-venv && source ~/esphome-venv/bin/activate
       pip install esphome
       esphome version
       ```
    2. Entra a la carpeta del firmware y crea tus secretos:
       ```bash
       cd HomeGreen/firmware/esphome
       cp secrets.example.yaml secrets.yaml      # edítalo; no lo subas a Git
       ```
    3. Valida sin compilar:
       ```bash
       esphome config nodo-riego-v1.yaml
       ```
       *Criterio de listo:* no aparece "Failed config". La primera compilación descarga el toolchain de ESP-IDF (varios cientos de MB): hazla con buen internet y paciencia.

!!! warning "Error típico: usar las claves del ejemplo"
    Las claves de `secrets.example.yaml` son texto de relleno y ESPHome las rechaza ("Invalid key
    format, please check it's using base64"). Genera una clave distinta por nodo; nunca reutilices
    una que esté en un repositorio.

## Flashear por USB la primera vez

1. **Prepara la alimentación.** Ajusta el buck a 5.0 V con multímetro **antes** de conectar nada y, para el primer flasheo, **desconecta VIN**: el ESP32 se alimenta solo del USB. Nunca USB y VIN a la vez ([electrico.md → errores típicos](../diseno/electrico.md)).
2. **Conecta el cable USB de datos** a la laptop (muchos cables de carga no llevan datos). En Windows puede pedir el driver del puente USB-serie del DevKit `[POR VERIFICAR: mira el chip junto al conector — CP2102 o CH340 — y descarga el driver de su fabricante]`; en Linux y macOS suele reconocerse solo.
3. **Flashea.**
   ```bash
   esphome run nodo-riego-v1.yaml
   ```
   Elige el puerto serie (`/dev/ttyUSB0`, `/dev/cu.usbserial…` o `COMx`). Desde el add-on: **Install → Plug into this computer** (necesita un navegador con Web Serial, como Chrome o Edge). Si se queda en "Connecting…", mantén presionado el botón **BOOT** de la placa hasta que empiece a escribir y suéltalo.
4. **Lee el log.** Al terminar, el mismo comando abre el log por USB. *Criterio de listo:* ves `WiFi Connected`, la IP, `Found i2c device at address 0x44` (SHT31) y `Found sensors` con la dirección del DS18B20; y al abrir HA, **Ajustes → Dispositivos e integraciones** descubre el nodo (pide la clave API si no la toma sola del add-on).
5. **Reserva la IP.** Anota la MAC del log y haz una reserva DHCP en el router. Apunta en `bitacora/electrico.csv` (`evento = flasheo`, versión de ESPHome).
6. **Ahora sí, a campo:** desconecta el USB, conecta VIN al buck. Todo lo demás será por OTA.

!!! warning "Error típico: el nodo NFT no arranca en campo"
    Arranca en la mesa por USB y no en el gabinete: GPIO12 quedó alto al encender (cable largo o
    driver equivocado). Pull-down de 10 kΩ y MOSFET, nunca un módulo relé activo en bajo en ese pin.

## Actualizar por OTA (todas las veces siguientes)

1. Edita el YAML (setpoint, calibración, pin) y valida: `esphome config nodo-riego-v1.yaml`.
2. Flashea inalámbrico:
   ```bash
   esphome run nodo-riego-v1.yaml          # elige "OTA (nodo-riego-v1.local)"
   ```
   Desde el add-on: **Install → Wirelessly**. Pide `ota_password`. El nodo compila en tu laptop/HA, recibe el binario, verifica y **se reinicia solo al final**: el firmware viejo sigue corriendo hasta ese instante.
3. *Criterio de listo:* el log muestra el nuevo `project.version` o tu cambio, y en HA la entidad `Nodo … versión ESPHome` cambió.

!!! tip "Cuándo flashear"
    Con el riego en "reposo" y sin dosis en curso (`Estado dosificación` = "midiendo / en banda").
    Al reiniciar, todo vuelve al estado seguro: la bomba NFT queda **ON**, el resto **OFF**, y los
    lazos deciden de nuevo en segundos. Nunca la víspera de una entrega ni durante un corte de luz.

## Calibrar sensores paso a paso

Cada calibración va a la bitácora: `bitacora/electrico.csv` con `evento = calibracion_<sensor>`,
`valor_medido` y `unidad` (campos de [electrico.md](../diseno/electrico.md)). Sin registro no hay
tendencia, y la tendencia es lo que dice cuándo cambiar una sonda.

### Capacitivos de sustrato (nodo de riego)

Los cuatro sensores se calibran **uno por uno** (del pack de 10, 20–30 % salen malos o desviados;
[research/electronica-automatizacion](../research/electronica-automatizacion.md)). El nodo expone
el voltaje crudo `MT-n voltaje` (categoría diagnóstico) y el % calibrado `Humedad sustrato Nn`.

1. **Seco.** Sensor conectado, limpio y al aire 1 min. Anota `MT-1 voltaje` estable. *Criterio de listo:* el valor no se mueve más de 0.02 V en 30 s.
2. **Húmedo.** Sumerge el sensor en un vaso de agua **hasta la línea marcada en la PCB** (nunca los componentes ni el conector). Anota el voltaje estable.
3. **Escribe los dos valores** en `substitutions:` del YAML (`mt1_seco`, `mt1_humedo`) y flashea por OTA. Repite para MT-2…4.
4. **Verifica:** al aire lee ≈ 0 %, en el vaso ≈ 100 %. En sustrato de coco recién regado y drenado lee un valor intermedio que anotas: es tu "saturado de campo" `[POR VERIFICAR: con ese dato y 4 charolas testigo fijas las bandas de germinación/desarrollo en el dry-run V3]`.
5. **Sella** el borde de la PCB con esmalte o epóxica y monta con el conector hacia arriba y encintado: mueren por el conector, no por el sensor.

La guía de referencia con el mismo procedimiento y YAML (`median` + `calibrate_linear`) está en
[SmartHomeScene](https://smarthomescene.com/diy/diy-capacitive-soil-moisture-sensor-v1-2-with-esphome/)
(verificada en [research/tutoriales-videos](../research/tutoriales-videos.md)).

### Nivel del tinaco JSN-SR04T (nodo de riego)

1. Monta el sensor en la tapa apuntando al agua, sin obstáculos, con **≥ 20 cm** entre su cara y el nivel máximo (zona muerta).
2. Mide con flexómetro: **altura de la cara del sensor al fondo** y **altura del fondo al nivel máximo** (flotador cerrado). Escríbelas en `Tinaco altura sensor a fondo` y `Tinaco altura agua max` (números de HA, sin reflashear). Ajusta `Tinaco capacidad nominal` (750 L o 1,100 L).
3. *Criterio de listo:* con el tinaco lleno `Nivel tinaco` ≈ 100 %; `Distancia tinaco` coincide con el flexómetro ± 2 cm.

### pH (nodo NFT)

Materiales: buffer pH 4.01 (Insumos Cerveceros, $40), sobre 6.86 (el estándar de las placas
chinas), agua limpia, papel absorbente, un termómetro o el propio DS18B20 en el vaso. Cada 15 días
([06 §Resumen](../referencia/06-validacion-y-lazos-agenticos.md)); guía completa en
[calibrar-sondas-ph-ec](../guias/calibrar-sondas-ph-ec.md).

1. Enciende el switch **Modo calibración**: pausa la dosificación y el watchdog de "sonda no confiable" (que si no, dispararía con el salto entre buffers).
2. **Solo la primera vez, ajusta el offset de la placa:** sonda en buffer 4.01 → gira el potenciómetro de la PH-4502C hasta que `pH voltaje` quede **≤ 3.05 V** (el ADC satura en ~3.1 V) y comprueba que en 6.86 quede por encima de 0.2 V.
3. **Buffer 4.01:** sonda 2 min hasta que `pH voltaje` se estabilice. Anota el voltaje y escríbelo en `pH calibración V en buffer 4.01`.
4. **Enjuaga, seca sin frotar, buffer 6.86:** anota y escribe en `pH calibración V en buffer 6.86`.
5. Escribe la **temperatura de los buffers** en `pH calibración temperatura`. La compensación (Nernst) es pequeña, menos de 0.1 pH en ±10 °C a pH 6, pero es gratis.
6. **Verifica:** en 6.86 debe leer 6.86 ± 0.05 y en 4.01 igual. Apaga **Modo calibración** y presiona **Rearmar dosificación**. *Criterio de listo:* `Estado dosificación` vuelve a "midiendo / en banda" y `pH NFT` coincide con el medidor de mano en la solución ± 0.1.
7. Bitácora: fecha, los dos voltajes y la pendiente (V por pH). Si la pendiente se acorta mes a mes, el electrodo se agota (dura 12–18 meses aunque no se use; reemplazo anual, [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv)).

!!! tip "Alternativa con calibración desde botones en HA"
    El componente externo [r0bb10/ESPHome-DFRobot-pH-Meter](https://github.com/r0bb10/ESPHome-DFRobot-pH-Meter)
    (verificado en [research/tutoriales-videos](../research/tutoriales-videos.md)) hace calibración de 2–3
    puntos con botones y guarda en EEPROM. Es el camino cuando pases al kit DFRobot Gravity; el YAML
    de este repo hace lo mismo con `number` y no depende de componentes externos.

### EC (nodo NFT)

La placa TDS entrega un voltaje; el nodo lo convierte a **EC en mS/cm** (compensado a 25 °C) y lo
multiplica por un factor `k` que tú fijas con el patrón (Hanna HI7031L 1.413 mS/cm, $459.36).

1. Pon `EC factor de calibración k` = **1.000**. Sonda en el patrón a temperatura conocida (el DS18B20 en el mismo vaso ayuda), 2 min. Anota la lectura `EC NFT` = L.
2. Calcula **k = 1.413 ÷ L** y escríbelo en `EC factor de calibración k`.
3. *Criterio de listo:* ahora `EC NFT` lee 1.413 ± 0.03. Enjuaga la sonda; nunca la dejes en el patrón (lo contamina).
4. Cada 15 días repite; si k se aleja más de 20 % del valor anterior, limpia la sonda o revisa el RC y el cable. Recuerda que TDS ≠ EC: la placa vende "ppm", este nodo reporta EC directo ([research/electronica-automatizacion §3](../research/electronica-automatizacion.md)).

### Peristálticas: mL por segundo (nodo NFT)

1. Ceba la manguera (deja correr hasta que salga líquido) y pon la salida en una probeta o jeringa graduada.
2. Con `Dosis tope de seguridad` en 30 s, enciende `Peristáltica A` desde HA: se apaga sola a los 30 s.
3. **mL medidos ÷ 30** → `Peristáltica A mL por segundo`. Repite para B y pH−. *Criterio de listo:* `mL dosificados hoy A` sube exactamente lo medido en la siguiente dosis.
4. Recalibra cada vez que cambies la manguera interna (es consumible) y anota en bitácora.

### Voltaje de batería y caudal (nodo NFT)

- **Batería:** multímetro en el bus (bornes de la fusiblera) vs `Voltaje batería NFT`. Nuevo factor = 5.7 × (V multímetro ÷ V leído) → `Batería factor divisor`. *Criterio de listo:* diferencia < 0.05 V.
- **Caudal YF-S201:** con la bomba corriendo, llena una cubeta de 10 L cronometrando y compara con `Volumen NFT acumulado`. Si difiere > 10 %, cambia el `450.0f` de la lambda del `pulse_counter` por el factor real `[POR VERIFICAR: cada pieza varía; el dato importa para el umbral de "sin flujo"]`.
- **DS18B20:** vaso con hielo y agua → ≈ 0 °C. Si hay desviación fija, añade un filtro `offset` al sensor.

## Cambiar setpoints

Los setpoints son entidades `number`, `select` y `switch` del nodo (categoría "Configuración"
en HA). Se cambian desde HA sin reflashear, se guardan en la flash del ESP32 y sobreviven
reinicios y cortes.

| Lazo | Entidades (nombre en HA) | Valor inicial | Fuente |
|---|---|---|---|
| Riego | `Riego humedad min/max germinacion`, `Riego humedad min/max desarrollo`, `Etapa nivel 1…4` (opciones `vacio` / `germinacion` / `desarrollo`; "vacio" = ese nivel no riega) | 60–80 % y 45–70 % `[POR VERIFICAR en V3]` | [control.md Lazo 1](../diseno/control.md) |
| Riego watchdogs | `Riego duracion max ciclo` (120 s), `Riego ciclos max por hora` (4) | `[POR VERIFICAR en V3]` | [06 §L0](../referencia/06-validacion-y-lazos-agenticos.md) |
| Tinaco | `Tinaco nivel minimo interlock` (20 %), `Tinaco nivel rearme` (25 %), `Tinaco nivel advertencia` (40 %) | 06 §L0 | [hidraulico §6](../diseno/hidraulico.md) |
| Ventilación | `Ventilacion HR encender` (75 %), `HR apagar` (70 %), `T encender` (28 °C), `T apagar` (26 °C), `tiempo minimo ON` (5 min), switch `Ventilacion forzada cada hora` (jun–sep) | 06 §L0; banda `[POR VERIFICAR]` | [control.md Lazo 3](../diseno/control.md) |
| Luces | `Luces hora encender` (6), `Luces hora apagar` (20), switch `Luces automaticas` | 14 h `[POR VERIFICAR: 12–14 h]` | [electrico.md](../diseno/electrico.md) |
| pH / EC | `pH minimo` (5.8), `pH maximo` (6.2), `EC minima` (1.2), `EC maxima` (1.8 mS/cm) | 06 §L0 | [control.md Lazo 2](../diseno/control.md) |
| Dosificación | `Dosis A/B/pH- segundos`, `Tiempo muerto de mezcla` (12 min), `Dosis maximas por dia` (12), `Dosis tope de seguridad` (30 s) | dosis `[POR VERIFICAR en el dry-run de Fase 2]` | [03 §2.2](../referencia/03-instalacion.md) |
| Continuidad | `Flujo minimo` (2 L/min), `Flujo segundos sin flujo para alarma` (60 s), `Flujo gracia tras arranque` (20 s), `Bateria voltaje bajo` (12.9 V), `Modo ahorro minutos ON/OFF` (15/15) | research §5 | [control.md Lazo 4](../diseno/control.md) |

Procedimiento (regla de [control.md](../diseno/control.md): el agente propone, tú commiteas):

1. Cambia el valor en HA y observa 24–48 h (o corre el experimento V6).
2. Si se queda, edita el `initial_value` en el YAML y haz commit con el mensaje
   `setpoint: <lazo> <valor anterior> → <nuevo> · evidencia`.
3. Flashea por OTA. **Ojo:** como los números tienen `restore_value: true`, el nodo conserva el
   valor guardado en su flash; `initial_value` solo aplica en un nodo recién borrado. Por eso el
   paso 1 va primero: el YAML documenta, el nodo ya lo tiene.

## Probar sin plantas

Antes del dry-run V3 de 72 h ([validacion/v03](../validacion/v03-dry-run.md)), estas pruebas de
5 minutos en la mesa con agua sola:

| Prueba | Cómo | Qué debe pasar |
|---|---|---|
| Interlock de tinaco | Baja `Tinaco nivel minimo interlock` por encima del nivel actual | `Tinaco crítico` ON, `Bomba riego` no enciende ni a mano; al bajar el umbral, `Estado riego` vuelve a "reposo" |
| Riego por histéresis | Sensor MT-1 al aire, `Etapa nivel 1` = desarrollo | `Estado riego` = "regando N1"; se apaga por `t_max`; al 5.º arranque en una hora, `Riego saturado` ON |
| Ciclo manual | Botón `Riego ciclo manual` | Bomba `Riego ciclo manual duracion` segundos |
| Ventilación | Sopla al SHT31 hasta HR > 75 % | `Ventilador` ON; no se apaga antes de `tiempo minimo ON` |
| Peristáltica con timeout | Enciende `Peristaltica A` a mano | Se apaga sola a los 30 s; `mL dosificados hoy A` sube |
| Sin flujo | Bomba NFT ON con el YF-S201 desconectado | A los 60 s (+ 20 s de gracia): `NFT sin flujo` ON, `Bomba NFT respaldo` ON, principal OFF; botón `Rearmar alarma de flujo` lo regresa |
| Corte de CFE | Desenchufa el cargador USB del detector | `Red CFE presente` OFF a los 5 s; `Tiempo en bateria actual` cuenta; al enchufar, `Duracion ultimo corte` se publica |
| Sonda mintiendo | Sonda pH del buffer 4.01 al 6.86 sin `Modo calibración` | En ≤ 5 min `Sonda confiable` OFF y `Dosificacion suspendida` ON |

## Problemas frecuentes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Un capacitivo lee 4095 crudo / ~3.1–3.3 V fijo / 0 % siempre | Cable AOUT roto o suelto; sensor sin 3V3; alimentado a 5 V (su salida rebasa el ADC); pieza muerta del pack | Ver abajo |
| Los cuatro capacitivos "se vuelven locos" al conectar Wi-Fi | Estaban en pines de ADC2 | Solo GPIO32–35 (ADC1) |
| `dallas_temp` sin sensores en el log | Falta el pull-up de 4.7 kΩ; hilos cambiados; sensor falso; cable largo | Ver abajo |
| `Temperatura tinaco` lee 85 °C o −127 °C | Lectura de reset (85) o error de bus (−127): alimentación parásita, pull-up flojo | Alimentar a 3V3 con los 3 hilos, pull-up firme, cable ≤ 10 m |
| pH que deriva o salta | Electrodo seco, BNC húmedo, cable alargado, sin RC, GND por el cable de señal, sonda vieja | Ver abajo |
| El nodo se reinicia al arrancar la bomba | Brownout: buck sin capacitores, relés alimentados del 3V3, cable largo al VIN | [electrico.md §5](../diseno/electrico.md): 470 µF en VIN, VCC/JD-VCC del módulo relé al 5 V, buck a < 30 cm |
| Las lecturas saltan cuando enciende una carga | Retorno de la carga por el negro del sensor | Cada carga regresa por su propio cable a la barra de tierra en estrella |
| El relé hace lo contrario | Módulo activo en alto / en bajo distinto al supuesto | Cambia `inverted` en ese `switch`; en `Bomba NFT` verifica que "ON" = bomba corriendo |
| El nodo NFT no arranca en campo | GPIO12 alto al encender | Pull-down 10 kΩ y MOSFET en SV-1 |
| `Found i2c device` no aparece | SDA/SCL cruzados, sin pull-ups, cable > 2 m, dirección 0x45 | Cruza los hilos, 4.7 kΩ a 3V3, acorta; prueba `address: 0x45` |
| `NFT sin flujo` falso justo al volver la luz | Pulsos tardan unos segundos en aparecer | Sube `Flujo gracia tras arranque`; la 07 lo advierte ([07 §2](../referencia/07-puntos-ciegos-y-riesgos.md)) |
| OTA falla a medias | Señal Wi-Fi débil, contraseña OTA distinta, binario grande | Mira `Nodo … señal WiFi` (> −70 dBm), revisa `secrets.yaml`; si no, USB |
| El nodo no aparece en HA pero sí en la red | Clave API distinta a la de `secrets.yaml` | Elimina el dispositivo en HA y vuelve a agregarlo con la clave correcta |
| El nodo no se conecta al Wi-Fi | Red de 5 GHz, SSID con caracteres raros, contraseña con `!` sin comillas | Solo 2.4 GHz; pon SSID y clave entre comillas en `secrets.yaml`; conéctate a la red "… rescate" para diagnosticar |

### Sensor capacitivo que lee 4095 (o 3.1–3.3 V fijo)

Un ADC del ESP32 a 12 dB satura en ~3.1 V, que es lo mismo que "4095" en cuentas crudas. El
capacitivo v1.2 alimentado a 3.3 V nunca debería llegar ahí ni al aire.

1. **Multímetro en AOUT del sensor** (contra GND): si marca lo mismo que `MT-n voltaje`, el sensor es el problema; si marca menos, el cable o el pin.
2. **¿Tiene 3.3 V en VCC?** Sin alimentación la salida flota y el ADC lee ruido o tope. Si lo alimentaste a 5 V, la salida supera 3.3 V: **cámbialo a 3V3**; el sensor funciona bien a 3.3 V.
3. **Cable:** los tres hilos de 22–24 AWG, ≤ 3 m, conector hacia arriba. Un conector corroído da un valor fijo (el sensor "se seca para siempre" y el watchdog `Riego saturado` te avisa).
4. **Prueba cruzada:** conecta ese sensor al GPIO de otro que sí funciona. Si el problema viaja con el sensor, es una pieza mala del pack (20–30 %): a la basura, no se repara.
5. Si lee **0 % o 100 % siempre** pero el voltaje sí cambia, la calibración está invertida o fuera de rango: revisa `mtn_seco` > `mtn_humedo` en el YAML.

### DS18B20 no detectado

1. El log al arrancar debe decir `Found sensors:` con una dirección `0x…`. Si dice que no encontró ninguno, es cableado en el 95 % de los casos.
2. **Pull-up de 4.7 kΩ entre DQ y 3V3**: sin él, el bus no funciona nunca. Es la causa número uno.
3. **Hilos:** en los sumergibles chinos los colores varían `[POR VERIFICAR: la ficha del que compraste; lo habitual es rojo VCC, negro GND, amarillo DQ]`. Con VCC y DQ cruzados el sensor se calienta: desconecta y revisa.
4. **Alimentación:** a 3V3 con los tres hilos (no "modo parásito"); cable ≤ 10 m.
5. **Sensor falso o dañado:** compraste 3 por eso ([`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv)); prueba otro en el mismo cable. Si tienes dos en el bus, cada `dallas_temp` necesita su `address` del log.

### pH que deriva

Las sondas baratas fallan **mintiendo**, no callando ([06 §Watchdogs](../referencia/06-validacion-y-lazos-agenticos.md)).

1. **Electrodo seco.** Se guarda siempre con la tapa llena de solución de almacenamiento (KCl 3 M) o, a falta, buffer 4.01; **nunca en agua destilada** (la mata). Un electrodo que estuvo seco necesita 24 h de remojo y a veces no vuelve.
2. **Conector BNC húmedo o cable alargado.** La sonda es de altísima impedancia: cada gota o cada metro extra suma deriva. Placa a < 1 m del retorno; lo que se alarga es el cable de 3.3 V al nodo ([electrico.md](../diseno/electrico.md)).
3. **Ruido del ADC y de las bombas.** Filtro RC 1 kΩ / 100 nF en la entrada; el retorno de las peristálticas por su propio cable; sondas en el **retorno**, nunca junto a la salida de dosificación ([03 §2.2](../referencia/03-instalacion.md)).
4. **Temperatura.** Si la solución cambia 10 °C entre día y noche, escribe `pH calibración temperatura` correcta; sin DS18B20 el nodo asume la de calibración.
5. **Edad.** Si la pendiente entre 4.01 y 6.86 se acorta calibración tras calibración, el electrodo se agota (12–18 meses). Cámbialo; el presupuesto anual de ~$1,050 ya lo incluye ([research/hidroponia-nft §g](../research/hidroponia-nft.md)).
6. **Mientras tanto,** el nodo se protege solo: un salto > 1.5 pH en 5 min o un voltaje fuera de rango apaga `Sonda confiable` y suspende la dosificación. No rearmes sin calibrar y sin confirmar con el medidor de mano (el "árbitro" del BOM).

## Al terminar

- [ ] Los tres YAML validan (`esphome config`) con tu `secrets.yaml`; `secrets.yaml` no está en Git.
- [ ] Cada nodo aparece en HA con las entidades de [datos.md §2](../diseno/datos.md) y el `Nodo … estado` en ON.
- [ ] Capacitivos calibrados uno por uno (8 voltajes en la bitácora); nivel de tinaco lee 100 % lleno.
- [ ] pH y EC calibrados con buffers y patrón, evento quincenal en el calendario de HA.
- [ ] mL/s de las tres peristálticas y factor de batería medidos; `Estado dosificación` en "midiendo / en banda".
- [ ] Las pruebas de la tabla "Probar sin plantas" pasaron; el dry-run V3 está agendado.
- Registrar en bitácora: `bitacora/electrico.csv` (`fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones`) con eventos `flasheo`, `calibracion_capacitivo`, `calibracion_ph`, `calibracion_ec`, `calibracion_peristaltica`, `v_bateria`.
- Siguiente paso: [Configurar Home Assistant](../guias/configurar-home-assistant.md) → [Home Assistant](home-assistant.md) (automatizaciones y dashboard) → [Dry-run V3](../validacion/v03-dry-run.md).

## Fuentes

- [research/electrico-respaldo-seguridad.md](../research/electrico-respaldo-seguridad.md) §5 — YAML base del nodo NFT (flujo, batería, red CFE, bombas) y automatizaciones.
- [referencia/06-validacion-y-lazos-agenticos.md](../referencia/06-validacion-y-lazos-agenticos.md) — lazos L0, watchdogs, calibración quincenal.
- [referencia/03-instalacion.md](../referencia/03-instalacion.md) §1.3 (banco de pruebas, USB primero y OTA después) y §2.2 (dosificación, sondas en el retorno).
- [diseno/electrico.md](../diseno/electrico.md) — pines, divisores, buck, errores típicos; [diseno/control.md](../diseno/control.md) — setpoints; [diseno/datos.md](../diseno/datos.md) — entidades; [diseno/hidraulico.md](../diseno/hidraulico.md) §5–6.
- [research/electronica-automatizacion.md](../research/electronica-automatizacion.md) — capacitivos (20–30 % malos), placas pH/TDS, proveedores.
- [research/hidroponia-nft.md](../research/hidroponia-nft.md) §g — buffers, patrón EC, presupuesto de calibración.
- [research/tutoriales-videos.md](../research/tutoriales-videos.md) — guía SmartHomeScene (capacitivo + ESPHome) y componente r0bb10 (pH).
- [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv) y [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv).
