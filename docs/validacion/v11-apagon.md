# V11 · Simulacro mensual de apagón

**En una línea:** una vez al mes botas el breaker del patio 10 minutos con el celular en la mano: la bomba del NFT debe seguir corriendo desde la batería sin que nada conmute, deben llegar las alertas de "corte de CFE" y de restauración, y al regresar la luz no debe haber falso "sin flujo" — porque un respaldo que no se prueba mensualmente es un respaldo que falla el día del corte real.

!!! info "Antes de empezar"
    - **Cuándo:** primero al comisionar el bus DC-first (S28, **antes de trasplantar** la primera línea); después **cada mes**, como evento en `calendar.huerto`; un corte real de ≥ 10 min bien documentado cuenta como el simulacro del mes, pero el botón TEST del GFCI se hace igual · **Tiempo:** 25 min (5 antes · 10 de corte · 5 de prueba de flujo · 5 de registro) · **Costo:** $0 · **Personas:** 1
    - **Necesitas:** celular con la app de HA y notificaciones críticas; acceso al breaker QO120GFI (o al contacto GFCI); una lámpara en el contacto del patio como carga visible; batería en flotación (13.3–13.6 V) y no recién salida de un corte real; día sin entrega; manos secas; `bitacora/electrico.csv`
    - **Guía paso a paso:** [Hacer el simulacro mensual de apagón](../guias/simulacro-de-apagon.md) · [Armar el respaldo DC](../guias/armar-respaldo-dc.md) · [Fase 2 · Eléctrico y respaldo §C](../fases/fase-2/electrico-respaldo.md) · **Desbloquea:** trasplantar en NFT; el checklist de [G2→3](gates.md) pide 3 simulacros aprobados por trimestre

## Propósito

CDMX tiene 3–6 cortes al año de 1–8 h; en NFT las raíces cuelgan en una película de 1–3 mm y llegan a marchitez irreversible en **2–4 h** sin flujo: un corte nocturno de 6 h puede costar 6–8 líneas (2–4 semanas de ingreso) ([07 §2](../referencia/07-puntos-ciegos-y-riesgos.md), [research/electrico-respaldo §1](../research/electrico-respaldo-seguridad.md)). La arquitectura DC-first —bomba de diafragma 12 V 40–60 W colgada de una LiFePO4 100 Ah siempre en paralelo— da 28–30 h continuas o ~2.5 días en modo 15/15, **si** el cableado, el cargador, las automatizaciones y el teléfono hacen lo que se supone. El simulacro valida las tres capas a la vez: que el GFCI dispara, que la continuidad es física y que los avisos llegan.

![Animación DC-first: se corta CFE, la batería sostiene la bomba sin conmutación, alerta a los 30 s, modo ahorro por debajo de 12.9 V y restauración sin falso "sin flujo"](../assets/diagramas/animaciones/dc-first-failover.svg)

## Lo que debe pasar, con tiempos

```mermaid
sequenceDiagram
    participant T as Tú
    participant G as GFCI del patio
    participant B as Bus 12.8 V
    participant N as Nodo NFT
    participant H as Home Assistant
    T->>G: botón TEST (t = 0), la palanca salta
    G-->>B: se va el 127 V; el cargador deja de flotar
    Note over B: batería siempre en paralelo: P-1 ni parpadea
    N->>H: red_cfe_presente = off (t + 5 s)
    H->>T: "Corte de luz en el patio" con V_bat y autonomía (t + 30 s)
    Note over N: 10 min × 3.3 A ≈ 0.55 Ah: V_bat sigue > 12.9 V
    T->>G: rearme OFF → ON (t = 10 min)
    N->>H: red_cfe_presente = on; duracion_ultimo_corte ≈ 10 min
    H->>T: aviso de luz restaurada con la duración
    Note over N: 20 s de gracia al flujo: sin falso "sin flujo"
    T->>N: cierra el manifold 60 s (prueba de flujo)
    N->>H: nft_sin_flujo = on; P-2 ON; P-1 OFF
    H->>T: crítica "NFT SIN FLUJO"
    T->>N: abre el manifold y rearma
```

## Procedimiento

1. **Antes (t − 5 min): estado base.** `sensor.voltaje_bateria_nft` 13.3–13.6 V, `sensor.flujo_nft` 8–16 L/min, `binary_sensor.red_cfe_presente` on, `switch.respaldo_automatico_por_flujo` on, `switch.modo_ahorro_15_15` off, sin alarmas activas; lámpara encendida en el contacto del patio; celular con sonido. Si V_bat < 13.0 V o hay alarma, **no hagas el simulacro**: arregla eso primero. *Criterio de listo:* valores base anotados.
2. **t = 0: oprime TEST en el QO120GFI** (o en el contacto GFCI). La palanca salta y la lámpara se apaga al instante: es la prueba mensual del GFCI. *Criterio de listo:* disparó con TEST.
3. **t + 0–5 s: mira la bomba.** P-1 sigue sin interrupción; el flujo no cambia. `red_cfe_presente` pasa a off a los 5 s. *Criterio de listo:* cero parpadeo.
4. **t + 30–40 s: llega la notificación "Corte de luz en el patio"** con V_bat y autonomía estimada (24–30 h). *Criterio de listo:* captura de pantalla con la hora.
5. **t + 1–10 min: observa.** `text_sensor.estado_continuidad_nft` "en batería"; `tiempo_en_bateria_actual` cuenta; V_bat baja apenas y se queda > 12.9 V (`bateria_baja` off). El nodo de riego v1 (127 V) queda sin señal: es normal; no debe llegar ninguna crítica del NFT. *Criterio de listo:* V_bat a los 10 min anotado.
6. **t = 10 min: rearma el breaker** (OFF completo y luego ON `[POR VERIFICAR: secuencia de rearme en la hoja del QO120GFI]`; en contacto GFCI: RESET). La lámpara enciende y el GFCI **no** vuelve a disparar. *Criterio de listo:* re-energizado sin disparo.
7. **t + 30–40 s: aviso de luz restaurada** con `duracion_ultimo_corte` ≈ 10 min; **no** llega "NFT SIN FLUJO" (gracia de 20 s). El nodo de riego regresa solo en 1–2 min; V_bat sube (absorción y luego flotación ≤ 13.6 V). *Criterio de listo:* segundo aviso capturado; cero alarma falsa.
8. **t = 12–16 min: prueba de flujo.** Cierra la válvula de compuerta del manifold con P-1 ON y cronometra: flujo < 2 L/min; a los **60 s** P-2 arranca y P-1 se apaga; llega la crítica "NFT SIN FLUJO" en ≤ 90 s. Abre la válvula y oprime `button.rearmar_alarma_de_flujo`: P-1 ON, P-2 OFF, flujo de vuelta. *Criterio de listo:* P-2 arrancó, crítica llegó, rearme hecho **antes de irte**.
9. **t = 16–20 min: registra** dos filas en `bitacora/electrico.csv` (abajo) y marca el evento del calendario. *Criterio de listo:* filas escritas con los tiempos.
10. **Trimestral (10 min más):** escalación (prueba de flujo **durante** el corte → `nft_emergencia` on y alerta cada 10 min), modo ahorro (poner los `number` de 15/15 en 1/1 y ver ciclar P-1), nodo caído (Wi-Fi 30 min). **Anual:** repetir la prueba de autonomía de 4 h con agua sola ([Armar el respaldo DC §E](../guias/armar-respaldo-dc.md)).

## Criterio de aceptación

!!! example "Aprobar el simulacro si"
    - **La bomba NFT siguió corriendo desde la batería** durante los 10 min, sin interrupción ni conmutación (P-1 ni parpadeó).
    - **Llegaron las alertas de "corte de CFE"**: la de corte (≈ 30 s, con V_bat y autonomía) y la de restauración (con la duración del corte).
    - **Al restaurar no hubo falso "sin flujo"** ni ninguna otra alarma falsa; el nodo de riego regresó solo.
    - Además (ampliación de la [guía](../guias/simulacro-de-apagon.md) y de [Fase 2 §C](../fases/fase-2/electrico-respaldo.md)): el GFCI **disparó con TEST** y no volvió a disparar al rearmar; en la prueba de flujo **P-2 arrancó y llegó la crítica**.

    Una falla en la continuidad de la bomba o en el arranque del respaldo significa que el NFT **no tiene respaldo real**: no se trasplanta nada nuevo hasta corregirla y repetir ([06 §V11](../referencia/06-validacion-y-lazos-agenticos.md)).

## Plantilla de registro

`bitacora/electrico.csv` (campos de [Diseño · Eléctrico](../diseno/electrico.md); dos filas por simulacro):

```csv
fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones
2027-07-05,test_gfci,GAB-A,QO120GFI,OK,,tu_nombre,"dispara al TEST; rearme OK; no dispara al re-energizar"
2027-07-05,simulacro_apagon,GAB-DC,bus,10,min,tu_nombre,"Vbat 13.4->13.3 V; corte avisado a 32 s; restauracion avisada (10 min); sin falso sin-flujo; prueba flujo: P-2 en 65 s y critica OK; nodo riego online en 1 min; resultado=aprobado"
2027-08-02,simulacro_apagon,GAB-DC,bus,FALLA,,tu_nombre,"fila 1.4: no llego alerta de corte (router sin UPS: se apago con el corte); bomba OK; repetir tras conectar router al DS-600"
2027-08-03,simulacro_apagon,GAB-DC,bus,10,min,tu_nombre,"repeticion: alertas OK a 31 s y al restaurar; resultado=aprobado"
```

- `valor_medido = FALLA` y en `observaciones` la fila del procedimiento (1.4, 2.3, 3.2…) y lo que viste; la repetición va en una fila nueva.
- [Fase 2 · Eléctrico y respaldo](../fases/fase-2/electrico-respaldo.md) propone registrar en `bitacora/nft.csv` con `evento=simulacro_V11` `[POR VERIFICAR: unificar en un solo archivo; esta sección, la guía y Diseño · Eléctrico usan electrico.csv]`.
- Guarda las capturas de las notificaciones con fecha; anota la fecha del simulacro en el cuadro de la puerta del gabinete.

## Si falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El TEST no dispara el GFCI | Breaker mal cableado (el neutro del circuito debe ir al breaker) o defectuoso | **No sigas:** electricista; el patio no se energiza sin GFCI que dispare ([Instalar GFCI y tierra](../guias/instalar-gfci-y-tierra.md)) |
| La bomba se detiene al irse la luz | P-1 colgada de la salida del cargador o de la fuente y no del bus; K1 en NO; fusible F1; seccionador abierto; BMS en protección | [Armar el respaldo DC §B y §D](../guias/armar-respaldo-dc.md); no hay respaldo real hasta corregir |
| `red_cfe_presente` no cambia | Cargador USB del detector desconectado o en un contacto que no es del patio; optoacoplador; GPIO sin pull-down | [Fase 2 · Dosificación v2](../fases/fase-2/dosificacion-v2.md), [Firmware](../software/firmware.md) |
| No llega la alerta | Router o cerebro sin UPS (se apagaron con el corte); notificaciones bloqueadas; automatización deshabilitada; nodo NFT alimentado de 127 V y no del bus | UPS DS-600 al cerebro **y al router**; revisar la app ([Configurar HA](../guias/configurar-home-assistant.md)) |
| V_bat cae rápido o `bateria_baja` en 10 min | Batería no llena, cargador sin flotar, perfil equivocado (plomo-ácido en LiFePO4) | [Armar el respaldo DC §C](../guias/armar-respaldo-dc.md); repetir la prueba de autonomía |
| El GFCI dispara al rearmar | Fuga real en alguna carga del patio (fuente goteada, cable pelado, N–T unidos) | Desconectar cargas una por una hasta hallar la que dispara; nunca puentear el GFCI |
| Llega "NFT SIN FLUJO" al restaurar | Gracia tras arranque corta; aire en el YF-S201; P-1 tardó en cebar | Subir `number.flujo_gracia_tras_arranque` a 30–40 s; purgar aire; válvula check |
| P-2 no arranca o no llega la crítica | `respaldo_automatico_por_flujo` off; fusible F2; K2; la válvula no cerró del todo; segundos de alarma | [Armar el respaldo DC §D](../guias/armar-respaldo-dc.md); repetir |
| Corte real > 12 h | Fuera del simulacro | Modo 15/15 automático desde 12.9 V; si el bus baja de 12.0 V, riego manual por gravedad desde el tinaco cada 30 min, checklist impreso en el gabinete ([Fase 2 §C](../fases/fase-2/electrico-respaldo.md)) |

!!! warning "Errores típicos"
    - "Primero el NFT, luego el respaldo": el primer corte no espera.
    - Probar el GFCI "una vez" y nunca más: botón TEST mensual junto con el V11.
    - Hacer el simulacro con la batería a medias y culpar al sistema.
    - Abrir el manifold y no rearmar: el respaldo no se apaga solo; rearma antes de irte.
    - Contar un corte real sin registro como "ya probamos este mes".

## Al terminar

- [ ] GFCI disparó con TEST y rearmó sin volver a disparar
- [ ] P-1 no se detuvo en ningún momento del corte de 10 min
- [ ] 2 alertas de corte (corte y restauración) con V_bat y duración; ninguna falsa "sin flujo"
- [ ] Prueba de flujo: P-2 arrancó, crítica llegó, rearme OK
- [ ] Nodo de riego regresó solo; bus de vuelta en flotación 13.3–13.6 V
- Registrar: filas `test_gfci` y `simulacro_apagon` en `bitacora/electrico.csv`; fecha en la puerta del gabinete; capturas
- Siguiente paso: nada hasta el mes que viene (evento en `calendar.huerto`); si falló, corregir y repetir antes de trasplantar; 3 registros aprobados por trimestre para [G2→3](gates.md)

## Fuentes

- [06 · Validación §V11 y §watchdogs](../referencia/06-validacion-y-lazos-agenticos.md): breaker 10 min una vez al mes, bomba desde batería, alertas de corte, sin falso "sin flujo".
- [research/electrico-respaldo-seguridad §1, §2.3, §5](../research/electrico-respaldo-seguridad.md): 2–4 h a marchitez, autonomía 28–30 h / 2.5 días en 15/15, YAML de las 5 automatizaciones, "prueba mensual: botar el breaker 10 min y verificar que llegan las 2 alertas", UPS DS-600.
- [07 · Puntos ciegos §2](../referencia/07-puntos-ciegos-y-riesgos.md): 3–6 cortes/año de 1–8 h; auto-recuperación y watchdog tras restauración.
- [Guía · Simulacro de apagón](../guias/simulacro-de-apagon.md): tiempos exactos, tabla de diagnóstico, extras trimestrales, plantilla de `electrico.csv`.
- [Fase 2 · Eléctrico y respaldo §B–C](../fases/fase-2/electrico-respaldo.md) y [03 · Instalación §commissioning Fase 2](../referencia/03-instalacion.md): primer simulacro antes de trasplantar; protocolo para cortes > 12 h.
- [Diseño · Control · Lazo 4](../diseno/control.md): estados Normal → EnBatería → ModoAhorro → Respaldo → Emergencia.
