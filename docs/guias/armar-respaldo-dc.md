# Armar el respaldo DC del NFT

**En una línea:** montas en GAB-DC una batería LiFePO4 de 12.8 V 100 Ah **siempre en paralelo** con el cargador, con fusible en el borne, seccionador y una fusiblera de 6 vías de la que cuelgan la bomba principal (K1 por contacto NC), la de respaldo (K2) y el nodo NFT; ajustas el cargador al perfil LiFePO4 y mides la autonomía real con agua sola — para que un corte de CFE de 1–8 h ni se note y el fail-safe sea físico, no de software.

!!! info "Antes de empezar"
    - **Tiempo:** 1 tarde (3–4 h) de armado y pruebas + 4 h de prueba de autonomía que corre sola (estimado) · **Costo:** batería Epcom LiFePO4 100 Ah **$4,459** + cargador LiFePO4 14.6 V ~$700–1,400 aprox. + 2 bombas de diafragma 12 V ~$900–1,800 aprox. + fusiblera, seccionador, fusibles y gabinete DC ~$500–900 aprox. + UPS DataShield DS-600 **$1,189** ≈ **$7,700–9,700**; opcional EPEVER LS2024B **$599** + panel Ugreen 100 W **$1,049** + $158 de envío = +$1,806 ([research/eléctrico §3 y §6](../research/electrico-respaldo-seguridad.md), [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv)). GFCI, tierra y electricista van en su propia guía. · **Personas:** 1
    - **Necesitas:** [batería Epcom LI100A12PRO 12.8 V 100 Ah, $4,459](https://www.cyberpuerta.mx/index.php?cl=search&searchparam=bateria+LiFePO4) · [cargador LiFePO4 14.6 V 10–20 A, ~$700–1,400 aprox.](https://listado.mercadolibre.com.mx/cargador-lifepo4-14.6v-10a) · [2 bombas de diafragma 12 V 40–60 W, ~$350–900 c/u aprox.](https://listado.mercadolibre.com.mx/bomba-diafragma-12v) · portafusible con fusible **F0 30 A** (ANL/MIDI), seccionador **S1** 30 A, fusiblera de 6 vías para 12 V con fusibles 10/10/2/5/2 A y un repuesto de cada valor, barra negativa, terminales de ojillo y puntera, cable rojo/negro 10 AWG (1.5 m), 12–14 AWG (bombas) y 18 AWG (nodo): [AG Electrónica](https://agelectronica.com) o tlapalería · [módulo relé de 2 canales con contactos ≥ 10 A](https://uelectronics.com/producto/relevador-5v-de-1-a-8-canales/) (K1/K2, del pedido de [compras Fase 1](../fases/fase-1/compras.md)) · válvula check por bomba ([Fase 2 · NFT](../fases/fase-2/nft.md)) · cargador USB 5 V + optoacoplador PC817 + resistencias 470 Ω/10 kΩ (detector de red) y 47 kΩ/10 kΩ (divisor de batería), ya en el nodo NFT ([Dosificación v2](../fases/fase-2/dosificacion-v2.md)) · [UPS DataShield DS-600 $1,189](https://www.cyberpuerta.mx/index.php?cl=search&searchparam=DataShield+UPS) (o KS800PRO $1,859 con puerto para NUT) · opcional: [EPEVER LS2024B $599](https://www.cyberpuerta.mx/index.php?cl=search&searchparam=controlador+de+carga+solar) + [panel Ugreen 15113 100 W $1,049](https://www.cyberpuerta.mx/index.php?cl=search&searchparam=panel+solar+100W) · [multímetro Steren MUL-005 $99](https://www.steren.com.mx/multimetro-compacto-economico.html) · [termofit](https://www.steren.com.mx/catalogsearch/result/?q=termofit), cinchos, cinta y marcador, llaves con mango aislado, capuchones para los bornes
    - **Prerequisitos:** [Instalar GFCI y tierra](instalar-gfci-y-tierra.md) recibido (sin GFCI no hay 127 V en el patio); [Montar gabinete IP65](montar-gabinete-ip65.md) para GAB-DC y GAB-2; nodo NFT flasheado con [`nodo-nft-v2.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-nft-v2.yaml) ([Flashear ESPHome](flashear-esphome.md)) y HA con las 5 automatizaciones ([Configurar Home Assistant](configurar-home-assistant.md)); bombas y tambo del NFT instalados o al menos una cubeta con agua para probar ([Fase 2 · NFT](../fases/fase-2/nft.md)); [Diseño eléctrico §3](../diseno/electrico.md) leído

## Cómo queda

![Esquema del bus DC-first: CFE 127 V, breaker GFCI QO120GFI, contacto WR, cargador LiFePO4 14.6 V, batería Epcom 100 Ah siempre en paralelo con fusible F0 30 A y seccionador S1, fusiblera de 6 vías, bomba principal por K1 NC y respaldo por K2 NO, nodo NFT ESP32 y panel 100 W con EPEVER opcional](../assets/diagramas/electrico/bus-dc-first.svg)

La batería no "entra" cuando se va la luz: **ya está conectada** al mismo nodo que el cargador. Con CFE presente el cargador flota la batería a ≤ 13.6 V y alimenta las cargas; sin CFE, las cargas siguen colgadas de la batería sin que nada conmute ([03-instalación §2.3](../referencia/03-instalacion.md)).

| Tag | Elemento | Especificación | Por qué |
|---|---|---|---|
| — | Batería | Epcom LI100A12PRO LiFePO4 12.8 V 100 Ah, BMS interno | 90 Ah útiles al 90 % DoD → 28–30 h con bomba de 40 W; ~2.5 días en modo 15/15 |
| — | Cargador | LiFePO4: absorción 14.4–14.6 V, flotación ≤ 13.6 V, 10–20 A | Un cargador de plomo-ácido sobrecarga o subcarga la LiFePO4 |
| F0 | Fusible principal | 30 A ANL/MIDI a ≤ 30 cm del borne + | Protege el cable de batería: un 10 AWG en corto se pone rojo antes de que el BMS reaccione |
| S1 | Seccionador | 30 A entre batería y bus | Trabajar en el bus sin batería viva |
| F1–F6 | Fusiblera 6 vías | F1 10 A P-1 · F2 10 A P-2 · F3 2 A nodo NFT · F4 5 A peristálticas/solenoides · F5 2 A reserva · F6 libre | Cada fusible protege un cable, no una carga |
| K1 | Relé bomba principal | Contacto **NC** → P-1; GPIO32 del nodo | Sin ESP32, sin Wi-Fi, sin HA: la bomba corre |
| K2 | Relé bomba respaldo | Contacto NO → P-2; GPIO14 | Arranca cuando el YF-S201 reporta < 2 L/min con bomba ON |
| P-1 / P-2 | Bombas de diafragma 12 V 40–60 W | 3.3–5 A; 8–16 L/min a 1–2 m de columna | Dos bombas DC cuestan menos que un inversor senoidal; la de 127 V queda para llenado y purga |
| — | Nodo NFT v2 | Desde F3 + buck a 5 V | Sigue midiendo V_bat, flujo y red CFE durante el corte |
| — | EPEVER LS2024B + panel 100 W (opcional) | PWM 20 A con perfil LiFePO4; 450–500 Wh/día en CDMX | Flota la batería sin CFE; **no** corre el huerto (la bomba consume ~960 Wh/día) |
| — | UPS DS-600 (en casa) | 600 VA / 360 W → 45–90 min para Pi + módem | Sin internet no hay alertas |

!!! note "Cargador AC y panel: complemento, no sustituto"
    El esquema lleva **cargador desde CFE obligatorio** y el panel + EPEVER como opción en paralelo: un panel de 100 W produce 450–500 Wh/día y la bomba 24/7 consume ~960 Wh/día, así que solo con solar la batería se vacía en pocos días. [POR VERIFICAR: `bom/fase2.csv` y [compras Fase 2 §5](../fases/fase-2/compras.md) listan el EPEVER "como cargador" sin cargador AC; si vas por esa ruta, confirma con el manual del LS2024B cómo alimentar su entrada desde CFE, o compra el cargador AC y deja el panel para la Fase 2.5.]

## Calibres y fusibles

Criterio: caída ≤ 3 % (0.36 V en 12 V) con ida y vuelta; tabla completa en [Diseño eléctrico · tabla de cableado](../diseno/electrico.md).

| Tramo | Corriente | Calibre | Largo máx. | Protección | Colores |
|---|---|---|---|---|---|
| Borne + de batería → F0 → S1 → fusiblera | 30 A | 10 AWG (u 8 AWG) | 1.5 m | F0 30 A a ≤ 30 cm del borne | rojo / negro |
| Fusiblera → P-1 y → P-2 (por K1/K2 en el positivo) | 3.3–5 A | 14 AWG hasta 4 m; **12 AWG hasta 6 m** (en el layout de Fase 2 son ≈ 4.2 m: 12 AWG) | 4 / 6 m | F1, F2 10 A | rojo / negro |
| Fusiblera → buck del nodo NFT (GAB-2) | 0.7 A | 18 AWG | 5 m (≈ 3.1 m en el layout) | F3 2 A | rojo / negro |
| Fusiblera → driver MOSFET (peristálticas y solenoides) | ≤ 1 A por canal [POR VERIFICAR: ficha del vendedor] | 18 AWG | 8 m | F4 5 A | rojo / negro |
| Buck → VIN del ESP32 | 0.7 A | 18–20 AWG | 0.3 m | — | naranja / negro |
| Bobinas K1/K2 desde el módulo relé | mA | 22 AWG | dentro del gabinete | — | amarillo (señal) |
| Divisor 47 kΩ / 10 kΩ → GPIO36 | µA | 22 AWG | dentro del gabinete | — | amarillo |
| Cargador USB del patio → PC817 → GPIO23 | mA | el cable USB + 22 AWG | ≤ 3 m | — | el GND del USB **no** se une al del nodo |

Los calibres de 127 V (del contacto al cargador) los confirma el electricista contra la tabla de ampacidad de la NOM-001 [POR VERIFICAR: tabla 310-15 y ficha del cable].

## Pasos

### A. En la mesa, sin tocar la batería (30 min)

1. **Mide la batería tal como llega.** Multímetro en CC entre bornes: la lectura debe ser positiva con la punta roja en el borne + y cercana a 12.8 V o más [POR VERIFICAR: voltaje de entrega en la ficha de Epcom]. Si marca mucho menos de 12 V o cero, el BMS está en protección o llegó dañada: reclama antes de conectar nada. Tapa los bornes con capuchones hasta el paso 8.
2. **Arma la placa de GAB-DC en seco:** portafusible F0, seccionador S1, fusiblera, barra negativa, cargador (o EPEVER). **Sin ningún fusible puesto.** Etiqueta cada vía (F1 P-1, F2 P-2, F3 nodo, F4 dosificación, F5 reserva, F6 libre) y pega la bolsita de repuestos dentro de la puerta.
3. **Prepara los cables** con terminales de ojillo crimpadas y termofit; rojo +12 V, negro GND; corta a la medida del layout y deja 20 cm de reserva. *Criterio de listo:* cada cable tiene etiqueta en los dos extremos (origen → destino, calibre) y ninguna terminal se mueve al jalarla.
4. **Confirma el buck del nodo a 5.0 V** antes de conectarle el ESP32 ([alimentación del ESP32](../assets/diagramas/electrico/alimentacion-esp32.svg)); si el nodo ya corrió en la mesa ([Flashear ESPHome](flashear-esphome.md)), este paso ya está.

### B. Orden seguro de conexión (una conexión a la vez)

!!! danger "Antes de la primera conexión"
    Breaker del patio **abajo**; cargador desenchufado; **S1 abierto y F0 fuera**; F1–F6 fuera; panel (si hay) tapado con cartón: al sol entrega 19 V en circuito abierto. Quítate reloj, anillos y pulseras; llaves con mango aislado; una sola mano en el gabinete cuando haya algo vivo. Una LiFePO4 de 100 Ah en corto no "chispea": funde la llave.

5. **Cablea primero las cargas, sin energía:** F1 → contacto NC de K1 → P-1; F2 → contacto NO de K2 → P-2; F3 → buck del nodo (GAB-2); F4 → +12 V del driver MOSFET. El negro de **cada** carga regresa por su propio cable a la barra negativa (tierra en estrella): nunca por el cable de un sensor.
6. **Conecta la salida DC del cargador** al nodo +BUS (después de F0/S1) y a la barra negativa, respetando la polaridad marcada. **Todavía no lo enchufes** a 127 V.
7. **Si hay EPEVER:** BAT+ y BAT− al mismo nodo; PV+ y PV− **aún sin panel**. Los controladores solares piden batería primero para reconocer 12 V; luego panel; las cargas nunca van por su salida LOAD, sino por la fusiblera [POR VERIFICAR: secuencia y menú en el manual del LS2024B].
8. **Ahora la batería:** cable rojo del borne + al portafusible F0 (vacío) y de F0 a S1 (abierto); cable negro del borne − a la barra negativa. Tuerca con arandela de presión, apretada; vuelve a poner los capuchones. *Criterio de listo:* con multímetro, entre +BUS y barra negativa lees **0 V** (S1 abierto, F0 fuera).
9. **Energiza el bus:** inserta F0 → mide después de F0: 12.8 V o más con la punta roja en +. Cierra S1 → +BUS marca lo mismo. Si la lectura sale negativa, abre S1, quita F0 y corrige la polaridad antes de seguir.
10. **Rama por rama:** inserta **F3** → el nodo arranca; en HA `sensor.voltaje_bateria_nft` debe coincidir con el multímetro (afina `number.bateria_factor_divisor`, nominal 5.7). Inserta **F1** → P-1 arranca **sola** (K1 NC, GPIO32 en alto). Inserta **F2** → P-2 no arranca; enciende `switch.bomba_nft_respaldo` → arranca; apágala. Inserta **F4**. *Criterio de listo:* `text_sensor.estado_continuidad_nft` = "normal: x L/min" con 8–16 L/min en `sensor.flujo_nft`.
11. **Enchufa el cargador** (breaker del patio arriba): el bus sube a absorción (14.4–14.6 V) y, con la batería llena, baja a flotación ≤ 13.6 V. Si pasa de 14.6 V, apágalo y corrige el perfil (paso 14). En el nodo, `binary_sensor.red_cfe_presente` debe estar **on** (cargador USB del detector conectado al contacto GFCI del patio).
12. **Panel (si lo compraste):** con el panel tapado, PV+/PV− al EPEVER; destapa; el controlador debe indicar carga. Panel orientado al sur, sin sombra de mediodía ([Fase 2 · Eléctrico y respaldo](../fases/fase-2/electrico-respaldo.md)).
13. **UPS DS-600 en casa:** router + cerebro (HA). Con KS800PRO, integra NUT en HA y usa su estado "OnBattery" como segunda fuente del evento de corte.

### C. Ajustar el cargador y los umbrales (20 min)

14. **Perfil LiFePO4 en el cargador (y en el EPEVER):** absorción **14.4–14.6 V**, flotación **≤ 13.6 V**, corriente 10–20 A. En el LS2024B elige el tipo de batería LiFePO4 o el perfil "User" con esos valores [POR VERIFICAR: en qué menú o botón se configura; algunos modelos requieren el display remoto o el cable USB y el software del fabricante]. *Criterio de listo:* tras una carga completa, con CFE presente, el bus marca **13.3–13.6 V** y la batería está a temperatura ambiente.
15. **Umbrales en el nodo (desde HA, se guardan en flash):** `number.bateria_voltaje_bajo` = 12.9 V (≈ 30–40 % restante); `number.modo_ahorro_minutos_on` / `number.modo_ahorro_minutos_off` = 15 / 15; `number.flujo_gracia_tras_arranque` = 20 s (evita el falso "sin flujo" al restaurar); `number.flujo_segundos_sin_flujo_para_alarma` = 60 s [POR VERIFICAR: ajustar tras medir el caudal real de tus líneas]; `number.flujo_minimo` = 2 L/min.

### D. Probar el fail-safe (15 min, antes de la autonomía)

16. **Sin nodo:** quita F3. P-1 debe **seguir corriendo**. Si se detiene, K1 está cableada en NO: cámbiala al contacto NC. Vuelve a poner F3.
17. **Con nodo:** `switch.bomba_nft` OFF → P-1 se detiene (mantenimiento); ON → arranca. `switch.bomba_nft_respaldo` ON → P-2 corre; OFF → se detiene. Si van en paralelo hidráulico, cada bomba tiene su válvula check (sin ella, la que corre recircula por la apagada).
18. **Reinicio:** oprime `button.nodo_nft_reiniciar`. P-1 no debe apagarse más que un parpadeo (`restore_mode: RESTORE_DEFAULT_ON`).
19. **Corte corto:** breaker del patio abajo 1 min. P-1 sigue; `binary_sensor.red_cfe_presente` pasa a off a los 5 s; a los 30 s llega la notificación "Corte de luz en el patio". Rearma. *Criterio de listo:* los cuatro puntos pasan sin tocar ningún cable.

### E. Prueba de autonomía (4 h con agua sola)

Se hace durante las 48 h de recirculación con agua sola del NFT ([Fase 2 · NFT](../fases/fase-2/nft.md)) o en el [dry-run V3](../validacion/v03-dry-run.md), nunca con plantas la primera vez.

20. **Arranca con la batería llena** (bus en flotación ≥ 1 h) y P-1 recirculando. Anota hora, `sensor.voltaje_bateria_nft` y `sensor.flujo_nft`.
21. **Mide la corriente real de la bomba:** abre S1, multímetro en serie en la rama F1 (escala de 10 A CC) [POR VERIFICAR: que tu multímetro tenga escala de 10 A; si no, pinza amperimétrica de CC], cierra S1, lee (esperado 3.3 A con 40 W, hasta 5 A con 60 W), abre S1, quita el multímetro, restablece F1 y cierra S1.
22. **Bota el breaker del patio y deja correr 4 h.** Cada 30 min anota V_bat y flujo (o exporta el histórico de HA al final).
23. **Calcula:** `autonomía [h] = 100 Ah × 0.9 ÷ I [A]` (la fórmula de [Diseño eléctrico](../diseno/electrico.md) expresada en corriente). Con 3.3 A → ≈ 27 h; con 5 A → ≈ 18 h. Suma el nodo (~2 W [POR VERIFICAR: medir en el banco]) y baja ≈ 1 h.
    *Criterio de listo:* tras 4 h, **V_bat ≥ 12.9 V** (no entró `binary_sensor.bateria_baja`), flujo estable, cero alertas falsas, y la autonomía calculada ≥ 24 h con bomba de 40 W (≥ 18 h con 60 W).
24. **Restaura CFE** y anota cuánto tarda el cargador en volver a flotación (dato de referencia para el simulacro mensual). Una prueba larga de 24 h solo tiene sentido en el V3 con agua sola, si quieres el número real en vez del calculado.

!!! warning "Errores típicos"
    - **Cargador de plomo-ácido (BR-700) en la LiFePO4, o al revés:** perfil equivocado = batería arruinada. El BR-700 es para la variante austera con Steren BR-1224.
    - **Batería sin F0 en el borne:** el cable en corto se pone rojo antes de que el BMS reaccione.
    - **P-1 por contacto NO:** un nodo muerto deja la bomba apagada. NC, siempre.
    - **Cargas colgadas de la salida LOAD del controlador solar:** el esquema las pone en la fusiblera del nodo de batería; el controlador solo carga.
    - **Panel conectado antes que la batería, o al sol mientras lo conectas.**
    - **Unir el GND del cargador USB del detector con el GND del nodo:** pierdes el aislamiento del optoacoplador y metes ruido de 127 V al nodo.
    - **Confiar en HA para que corra el agua:** HA avisa y optimiza; la continuidad es K1 NC + batería en paralelo.
    - **Comprar el respaldo "después":** el primer corte no espera; en CDMX son 3–6 al año de 1–8 h ([07 §2](../referencia/07-puntos-ciegos-y-riesgos.md)).

## Qué pasa cuando se va la luz

![Animación DC-first: se corta CFE, la batería sostiene la bomba sin conmutación, alerta a los 30 s, modo ahorro 15/15 por debajo de 12.9 V y restauración sin falso "sin flujo"](../assets/diagramas/animaciones/dc-first-failover.svg)

| Momento | Qué hace el hardware | Qué hace HA |
|---|---|---|
| Corte | El cargador deja de flotar; la batería, ya en paralelo, sigue alimentando P-1 y el nodo | A los 30 s: "Corte de luz en el patio" con V_bat y autonomía 24–30 h |
| V_bat < 12.9 V por 5 min | `binary_sensor.bateria_baja` on | Enciende `switch.modo_ahorro_15_15`: el nodo cicla P-1 15 min ON / 15 min OFF (≈ 2.5 días) |
| Bomba ON y flujo < 2 L/min por 60 s | El nodo enciende P-2 y apaga P-1 (`binary_sensor.nft_sin_flujo`) | Crítica "NFT SIN FLUJO"; si además no hay red, `binary_sensor.nft_emergencia` repite cada 10 min |
| Regresa CFE | Cargador vuelve a absorción y flotación; 20 s de gracia al flujo | Aviso con `sensor.duracion_ultimo_corte`; apaga el modo ahorro |
| Bus < 12.0 V (corte de días) | BMS protege la batería | Tú: riego manual por gravedad desde el tinaco cada 30 min ([Fase 2 · Eléctrico y respaldo](../fases/fase-2/electrico-respaldo.md)) |

Todo esto se ensaya cada mes: [Simulacro de apagón](simulacro-de-apagon.md).

## Al terminar

- [ ] F0 30 A a ≤ 30 cm del borne +, S1, fusiblera con F1–F5 etiquetados y repuestos en la puerta; barra negativa única
- [ ] Bus en flotación 13.3–13.6 V con CFE presente; perfil LiFePO4 confirmado (absorción ≤ 14.6 V)
- [ ] P-1 corre sin nodo (K1 NC) y sobrevive un reinicio; P-2 arranca desde HA; válvulas check puestas
- [ ] `sensor.voltaje_bateria_nft` = multímetro ± 0.1 V; `binary_sensor.red_cfe_presente` on con luz y off a los 5 s sin luz
- [ ] Prueba de autonomía de 4 h: V_bat ≥ 12.9 V al final y autonomía calculada ≥ 24 h (40 W)
- [ ] UPS DS-600 con router + cerebro; notificación de corte recibida en el celular
- Registrar en `bitacora/electrico.csv` (`fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones`, [Diseño eléctrico](../diseno/electrico.md)): una fila `evento=v_bateria`, `gabinete=GAB-DC`, `rama=bus`, con el voltaje en flotación (`unidad=V`), y una `evento=autonomia_h` con las horas calculadas (`unidad=h`; en `observaciones` la corriente medida y el modelo de bomba). `autonomia_h` es evento nuevo: agrégalo a la lista de Diseño eléctrico.
- Siguiente paso: [Simulacro de apagón](simulacro-de-apagon.md) (primer V11, antes de trasplantar) → [Fase 2 · NFT](../fases/fase-2/nft.md)

## Fuentes

- [research/electrico-respaldo-seguridad §2 (dimensionamiento), §3.1–3.5 (batería, cargadores, UPS, solar), §5 (detector de red, YAML) y §6 (BOM)](../research/electrico-respaldo-seguridad.md)
- [referencia/03-instalacion §2.3](../referencia/03-instalacion.md) — arquitectura DC-first y regla de oro
- [diseno/electrico §3 (bus), tabla de cableado, consumo y autonomía, lista de protecciones](../diseno/electrico.md)
- [diseno/control — lazos de continuidad NFT](../diseno/control.md) · [diseno/layout-patio — GAB-DC y longitudes del bus](../diseno/layout-patio.md)
- [fases/fase-2/electrico-respaldo](../fases/fase-2/electrico-respaldo.md) y [compras §5](../fases/fase-2/compras.md) · [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv)
- [`firmware/esphome/nodo-nft-v2.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-nft-v2.yaml) y [software/firmware](../software/firmware.md) — pines GPIO32/14/23/36, umbrales, modo ahorro
- [referencia/07-puntos-ciegos §2](../referencia/07-puntos-ciegos-y-riesgos.md) — frecuencia de cortes en CDMX
