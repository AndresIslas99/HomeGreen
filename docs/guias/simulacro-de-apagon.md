# Hacer el simulacro mensual de apagón

**En una línea:** una vez al mes, con el celular en la mano, disparas el GFCI del patio con su botón TEST y lo dejas abajo 10 minutos: la bomba del NFT debe seguir en batería, deben llegar las alertas de corte y de restauración y, al regresar la luz, no debe haber falso "sin flujo"; después provocas 60 s "sin flujo" para ver arrancar el respaldo y anotas todo — porque un respaldo que no se prueba cada mes es un respaldo que falla el día del corte real (método V11).

!!! info "Antes de empezar"
    - **Tiempo:** 25 min (5 antes · 10 de corte · 5 de prueba de flujo · 5 de registro) · **Costo:** $0 · **Personas:** 1
    - **Necesitas:** celular con la app de Home Assistant y notificaciones críticas habilitadas; acceso al breaker QO120GFI del centro de carga (o al contacto GFCI, si elegiste esa opción); una lámpara o cargador con LED conectado al contacto del patio (carga visible); esta tabla impresa o abierta; `bitacora/electrico.csv`; opcional: multímetro
    - **Prerequisitos:** [Armar el respaldo DC](armar-respaldo-dc.md) con prueba de autonomía pasada; automatizaciones 1–5 en HA ([Configurar Home Assistant](configurar-home-assistant.md)); evento mensual en `calendar.huerto` ([Datos](../diseno/datos.md)); batería en flotación (13.3–13.6 V) y no recién salida de un corte real; día sin entrega; manos secas

## Lo que debe pasar

![Animación DC-first: se corta CFE, la batería sostiene la bomba sin conmutación, alerta a los 30 s, modo ahorro por debajo de 12.9 V y restauración sin falso "sin flujo"](../assets/diagramas/animaciones/dc-first-failover.svg)

```mermaid
sequenceDiagram
    participant T as Tú
    participant G as GFCI del patio
    participant B as Bus 12.8 V
    participant N as Nodo NFT
    participant H as Home Assistant
    T->>G: botón TEST (t = 0)
    G-->>B: se va el 127 V, el cargador deja de flotar
    Note over B: la batería ya estaba en paralelo: P-1 ni parpadea
    N->>H: red_cfe_presente = off (t + 5 s)
    H->>T: "Corte de luz en el patio" con V_bat (t + 30 s)
    T->>G: rearme OFF → ON (t = 10 min)
    N->>H: red_cfe_presente = on; duracion_ultimo_corte ≈ 10 min
    H->>T: aviso de luz restaurada con la duración
    Note over N: 20 s de gracia al flujo: sin falso "sin flujo"
    T->>N: cierra el manifold 60 s (prueba de flujo)
    N->>H: nft_sin_flujo = on, P-2 ON, P-1 OFF
    H->>T: crítica "NFT SIN FLUJO"
    T->>N: abre el manifold y rearma
```

Tres cosas se validan en una sola sesión ([06 · V11](../referencia/06-validacion-y-lazos-agenticos.md)): que el GFCI dispara (botón TEST), que la continuidad es física (la bomba sigue sin que nada conmute) y que la capa de avisos funciona (2 alertas de corte + 1 crítica de flujo).

## Procedimiento y resultados esperados

Marca la última columna en el momento; lo que no se anota en el minuto se olvida.

### Antes (t − 5 min)

| # | Qué haces | Dónde miras | Esperado | OK / falla |
|---|---|---|---|---|
| 0.1 | Anota el estado base | `sensor.voltaje_bateria_nft` · `sensor.flujo_nft` · `text_sensor.estado_continuidad_nft` · `binary_sensor.red_cfe_presente` | 13.3–13.6 V (flotando) · 8–16 L/min · "normal: x L/min" · on | |
| 0.2 | Verifica que el respaldo automático esté armado y el modo ahorro apagado | `switch.respaldo_automatico_por_flujo` · `switch.modo_ahorro_15_15` · `binary_sensor.nft_sin_flujo` | on · off · off | |
| 0.3 | Lámpara encendida en el contacto del patio; celular con sonido | — | — | |

Si V_bat < 13.0 V o hay una alarma activa, **no hagas el simulacro**: primero arregla eso ([diagnóstico](#si-algo-falla)).

### El corte (t = 0 → 10 min)

| # | Qué haces | Dónde miras | Esperado | OK / falla |
|---|---|---|---|---|
| 1.1 | **t = 0:** oprime **TEST** en el breaker QO120GFI (o en el contacto GFCI) | palanca del breaker · lámpara del patio | La palanca salta y la lámpara se apaga **al instante** (prueba mensual del GFCI, [Instalar GFCI y tierra](instalar-gfci-y-tierra.md)) | |
| 1.2 | t + 0–5 s: escucha o mira la bomba | P-1 · `sensor.flujo_nft` | P-1 sigue corriendo sin interrupción; el flujo no cambia (batería siempre en paralelo, cero conmutación) | |
| 1.3 | t + 5 s | `binary_sensor.red_cfe_presente` | off (filtro `delayed_off: 5s`) | |
| 1.4 | t + 30–40 s | celular | Notificación **"Corte de luz en el patio"** con V_bat y autonomía estimada 24–30 h (automatización 2) | |
| 1.5 | t + 1–10 min | `text_sensor.estado_continuidad_nft` · `sensor.tiempo_en_bateria_actual` · `sensor.voltaje_bateria_nft` | "en bateria: 13.x V, N min" · cuenta minutos · V_bat baja apenas (10 min × 3.3 A ≈ 0.55 Ah de 90) y se queda **> 12.9 V**; `binary_sensor.bateria_baja` off | |
| 1.6 | Mientras tanto | nodo de riego v1 (GAB-1) en HA | Queda **sin señal**: se alimenta de la fuente de 127 V, es normal; no debe llegar ninguna crítica por el NFT | |
| 1.7 | t + 5 min | luces T8, extractor, refrigerador de cosecha | T8 y extractor apagados (127 V del patio); el refrigerador y el cerebro siguen (otros circuitos + UPS) | |

### La restauración (t = 10 min)

| # | Qué haces | Dónde miras | Esperado | OK / falla |
|---|---|---|---|---|
| 2.1 | **t = 10 min:** rearma el breaker (palanca a **OFF** completo y luego a **ON** [POR VERIFICAR: secuencia de rearme en la hoja del QO120GFI]; en contacto GFCI: **RESET**) | lámpara · breaker | La lámpara enciende; el GFCI **no** vuelve a disparar al re-energizar | |
| 2.2 | t + 5 s | `binary_sensor.red_cfe_presente` | on | |
| 2.3 | t + 30–40 s | celular · `sensor.duracion_ultimo_corte` | Aviso de **luz restaurada** con la duración (≈ 10 min); **no** llega "NFT SIN FLUJO" (gracia de 20 s tras el arranque) | |
| 2.4 | t + 1–2 min | nodo de riego en HA · `sensor.voltaje_bateria_nft` | El nodo de riego regresa **solo** (auto-recuperación); V_bat sube: el cargador entra en absorción y luego flota ≤ 13.6 V | |
| 2.5 | Si tenías el modo ahorro activo por una prueba anterior | `switch.modo_ahorro_15_15` | HA lo apaga al regresar la red; P-1 continua | |

### Prueba de flujo (t = 12 → 16 min)

| # | Qué haces | Dónde miras | Esperado | OK / falla |
|---|---|---|---|---|
| 3.1 | Cierra la válvula de compuerta del manifold (o pellizca la manguera de salida) con P-1 encendida; cronómetro | `sensor.flujo_nft` | Cae por debajo de 2 L/min (`number.flujo_minimo`) | |
| 3.2 | A los 60 s (`number.flujo_segundos_sin_flujo_para_alarma`; en el informe original eran 2 min) | P-2 · P-1 · `binary_sensor.nft_sin_flujo` · celular | **P-2 arranca y P-1 se apaga** (protección en seco); `nft_sin_flujo` on; crítica **"NFT SIN FLUJO"** en ≤ 90 s (automatización 1). Con red presente, `binary_sensor.nft_emergencia` sigue off | |
| 3.3 | Abre la válvula; oprime `button.rearmar_alarma_de_flujo` | P-1 · P-2 · `text_sensor.estado_continuidad_nft` | P-1 ON, P-2 OFF, flujo de vuelta a 8–16 L/min, estado "normal" | |

!!! tip "Si abres el manifold y no rearmas"
    El nodo sigue en alarma con P-2 corriendo: es correcto (el respaldo no se apaga solo; lo rearmas tú tras revisar en sitio). Rearma siempre antes de irte.

### Registro (t = 16 → 20 min)

Dos filas en `bitacora/electrico.csv` (campos `fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones`, [Diseño eléctrico](../diseno/electrico.md)):

```csv
fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones
2026-10-05,test_gfci,GAB-A,QO120GFI,OK,,tu_nombre,dispara al TEST; rearme OK; no dispara al re-energizar
2026-10-05,simulacro_apagon,GAB-DC,bus,10,min,tu_nombre,Vbat 13.4->13.3 V; corte avisado a 32 s; restauracion avisada; sin falso sin-flujo; prueba flujo: P-2 en 65 s y critica OK; nodo riego online en 1 min
```

Si algo falló, `valor_medido=FALLA` y en `observaciones` el número de fila (1.4, 2.3, 3.2…) y lo que viste. Marca el evento del calendario como hecho y guarda una captura de las notificaciones. **Un corte real de ≥ 10 min documentado con estas mismas columnas cuenta como el simulacro del mes**, pero el TEST del GFCI (1.1) se hace igual.

## Si algo falla

| Fila | Síntoma | Causa probable | Qué hacer |
|---|---|---|---|
| 1.1 | El TEST no dispara el GFCI | Breaker mal cableado (el neutro del circuito debe ir al breaker) o defectuoso | No sigas: llama al electricista; no se energiza el patio sin GFCI que dispare ([Instalar GFCI y tierra](instalar-gfci-y-tierra.md)) |
| 1.2 | La bomba se detiene al irse la luz | P-1 colgada de la salida del cargador o de la fuente y no del bus; K1 en NO; F1 fundido; S1 abierto; BMS en protección | [Armar el respaldo DC §B y §D](armar-respaldo-dc.md) |
| 1.3 | `red_cfe_presente` no cambia | Cargador USB del detector desconectado o en un contacto que no es del patio; PC817 o resistencia; GPIO23 sin pull-down | [Dosificación v2 · hardware](../fases/fase-2/dosificacion-v2.md), [Firmware](../software/firmware.md) |
| 1.4 / 2.3 | No llega la alerta | Router o cerebro sin UPS (se apagaron con el corte); notificaciones bloqueadas en el celular; automatización deshabilitada; nodo NFT alimentado de 127 V y no de F3 | UPS DS-600 al cerebro; revisa la app; [Configurar Home Assistant](configurar-home-assistant.md) |
| 1.5 | V_bat cae rápido o `bateria_baja` se enciende en 10 min | Batería no estaba llena, cargador sin flotar, perfil equivocado, F0/S1 | [Armar el respaldo DC §C](armar-respaldo-dc.md); repite la prueba de autonomía |
| 2.1 | El GFCI dispara al rearmar | Fuga real en alguna carga del patio (fuente goteada, cable pelado, N–T unidos) | Desconecta cargas una por una y rearma hasta hallar la que dispara; nunca puentees el GFCI |
| 2.3 | Llega "NFT SIN FLUJO" al restaurar | Gracia tras arranque muy corta; aire en el YF-S201; P-1 tardó en cebar | Sube `number.flujo_gracia_tras_arranque` a 30–40 s; purga aire; válvula check |
| 2.4 | El nodo de riego no regresa solo | Fuente ELI-1260, GPIO12 alto al arrancar, Wi-Fi | [Firmware · problemas](../software/firmware.md) |
| 3.2 | P-2 no arranca o no llega la crítica | `switch.respaldo_automatico_por_flujo` off; F2; K2; el flujo no bajó de 2 L/min (la válvula no cerró del todo); umbral de segundos | [Armar el respaldo DC §D](armar-respaldo-dc.md) |

Una falla en 1.2 o 3.2 significa que el NFT **no tiene respaldo real**: no trasplantes nada nuevo hasta corregirla y repetir el simulacro.

## Extras trimestrales (10 min más)

| Prueba | Cómo | Esperado |
|---|---|---|
| Escalación (automatización 3) | Haz la prueba de flujo (3.1–3.2) **durante** el corte, antes de rearmar | `binary_sensor.nft_emergencia` on y la alerta se repite cada 10 min hasta rearmar |
| Modo ahorro (automatización 4) | Pon `number.modo_ahorro_minutos_on` y `number.modo_ahorro_minutos_off` en 1 y enciende `switch.modo_ahorro_15_15` | P-1 cicla 1 min ON / 1 min OFF (`estado_continuidad_nft` = "modo ahorro…"); apaga el switch, P-1 queda ON; regresa los valores a 15/15 |
| Nodo caído (automatización 5) | Apaga el Wi-Fi 30 min (como en el [dry-run V3](../validacion/v03-dry-run.md)) | Alerta "Nodo NFT sin señal" a los 5 min; P-1 sigue corriendo todo el rato; al volver el Wi-Fi, nada que rearmar |
| Autonomía (anual) | Repite la prueba de 4 h de [Armar el respaldo DC §E](armar-respaldo-dc.md) con agua sola | Autonomía calculada igual o cercana a la del primer año; una caída fuerte es envejecimiento de la batería |

## Al terminar

- [ ] GFCI disparó con TEST y rearmó sin volver a disparar
- [ ] P-1 no se detuvo en ningún momento del corte de 10 min
- [ ] Llegaron las 2 alertas de corte (corte y restauración) con V_bat y duración; ninguna falsa "sin flujo"
- [ ] Prueba de flujo: P-2 arrancó, llegó la crítica, rearme OK
- [ ] Nodo de riego regresó solo; bus de vuelta en flotación 13.3–13.6 V
- Registrar en `bitacora/electrico.csv`: filas `test_gfci` y `simulacro_apagon` (plantilla arriba); anotar la fecha en el cuadro de la puerta del gabinete
- Siguiente paso: nada hasta el mes que viene (evento en `calendar.huerto`); si algo falló, la guía de la tabla de diagnóstico y repetir antes de trasplantar. Resultado del método en [Validación · V11](../validacion/v11-apagon.md)

## Fuentes

- [referencia/06-validacion-y-lazos-agenticos — V11 y watchdogs](../referencia/06-validacion-y-lazos-agenticos.md)
- [research/electrico-respaldo-seguridad §5 (automatizaciones 1–5, prueba mensual) y §2.3 (autonomía)](../research/electrico-respaldo-seguridad.md)
- [fases/fase-2/electrico-respaldo §C](../fases/fase-2/electrico-respaldo.md) — primer simulacro y rutina mensual · [referencia/03-instalacion — commissioning Fase 2](../referencia/03-instalacion.md)
- [`firmware/esphome/nodo-nft-v2.yaml`](https://github.com/AndresIslas99/HomeGreen/blob/main/firmware/esphome/nodo-nft-v2.yaml) — `red_cfe_presente` (5 s), gracia de 20 s, umbral de 60 s, modo ahorro, botón de rearme · [diseno/control](../diseno/control.md) · [diseno/datos](../diseno/datos.md) — entidades y `calendar.huerto`
- [referencia/07-puntos-ciegos §2](../referencia/07-puntos-ciegos-y-riesgos.md) — 3–6 cortes/año de 1–8 h; auto-recuperación tras el corte
