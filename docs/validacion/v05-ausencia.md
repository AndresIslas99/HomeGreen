# V5 · Prueba de estrés de ausencia

**En una línea:** cuatro días sin tocar nada —en casa, mirando el dashboard, pero sin abrir una válvula ni regar "tantito" salvo alarma crítica— y el sistema demuestra con datos, no con optimismo, que la promesa "aguanta vacaciones" es cierta para el riego y las alarmas (y te recuerda que no lo es para cosechar, empacar ni entregar).

!!! info "Antes de empezar"
    - **Cuándo:** con el sistema **en producción** y el [V3](v03-dry-run.md) aprobado: una vez en Fase 1 dentro de la ventana de "v1 estable 30 días" (S16–17) y otra vez en Fase 2 con NFT, después del primer [V11](v11-apagon.md) (S29–30); repetir tras cualquier cambio mayor · **Tiempo:** 4 días (96 h) de no hacer nada + 20 min de registro · **Costo:** $0 · **Personas:** 1 (mirando, no tocando)
    - **Necesitas:** charolas reales en los 4 niveles regados (y líneas NFT con plantas en Fase 2); tinaco lleno al inicio; notificaciones críticas probadas; `bitacora/validacion/v05-ausencia.csv`; el calendario de siembra ajustado para que no haya cosecha ni entrega en esos 4 días
    - **Guías relacionadas:** [Automatización v1](../fases/fase-1/automatizacion-v1.md) · [Diseño · Control](../diseno/control.md) · [Configurar Home Assistant](../guias/configurar-home-assistant.md) · **Desbloquea:** la afirmación "el sistema aguanta 3–4 días solo" con evidencia; insumo de [G1→2 (b)](gates.md)

## Propósito

El plan dice que el sistema aguanta 3–4 días solo con alarmas remotas ([00 · Riesgos](../referencia/00-plan-maestro.md)). Es cierto para riego, ventilación y vigilancia; **es falso para cosechar, empacar y entregar**: si faltas un jueves, ese ingreso no existe y el chef prueba otro proveedor ([07 §13](../referencia/07-puntos-ciegos-y-riesgos.md)). V5 valida la primera mitad de la promesa con datos y hace visible la segunda: lo que el sistema no cubre lo cubre el ayudante con SOP desde el mes 4.

## Reglas del juego

| Permitido | Prohibido (cuenta como intervención) |
|---|---|
| Mirar el dashboard y el histórico cuantas veces quieras | Regar a mano, abrir o cerrar válvulas, mover charolas de nivel |
| Inspección visual desde fuera, sin tocar charolas | Cambiar un setpoint, reiniciar un nodo o HA "por si acaso" |
| Atender una **alarma crítica** (flujo cero, nodo caído, nivel < 20 %) y anotarla como intervención **prevista** | Atender una advertencia (tinaco < 40 %, HR alta) antes de que se vuelva crítica |
| Cosechar o sembrar **fuera** de la ventana (antes de empezar o después de terminar) | Cosechar, sembrar o entregar dentro de las 96 h |

Ventana natural con entregas martes y viernes: **del viernes después de la entrega al martes antes de la cosecha** (≈ 4 días: sábado, domingo, lunes completos + tarde del viernes y madrugada del martes). Mueve la siembra del lunes al martes después de cosechar, esa semana. Con ayudante sabatino, la ventana puede caer donde quieras: él cosecha con el SOP, tú no tocas el sistema.

## Procedimiento

1. **Día −1 · Prepara el estado inicial.** Tinaco al 100 % (con tandeo, verifica que el flotador cerró), tambo NFT recién rellenado (Fase 2), bandas y setpoints commiteados, sin alarmas activas, teléfono con la crítica en un canal que suene en silencio. Anota los valores de partida: humedad por nivel, nivel del tinaco, HR, pH/EC, V_bat. *Criterio de listo:* fila de arranque en el CSV con los valores base.
2. **Día −1 · Ajusta el calendario.** Sin cosecha, siembra ni entrega en las 96 h; charolas que estarían "en su día" se cosechan antes o se planea que aguanten 1–2 días más (ventana de cosecha de [08](../referencia/08-recetas-y-economia-unitaria.md): rábano 7–10, girasol 8–12). *Criterio de listo:* nada en el calendario entre la hora de inicio y la de fin.
3. **Hora 0 · Empieza y no toques nada.** Registra la hora. *Criterio de listo:* último contacto con el patio anotado.
4. **Cada día (10 min, solo mirando).** Lazo L1 de lectura: panel de excepciones, histórico de riegos por día, humedad mínima y máxima por nivel, HR máxima, ciclos de ventilación, nivel del tinaco, pH/EC en banda (Fase 2). Anota en el CSV lo que ves; **no actúes**. *Criterio de listo:* 4 filas diarias de observación.
5. **Si llega una crítica:** atiéndela (es lo que el sistema pide), anota hora, causa y qué hiciste; sigue la prueba. *Criterio de listo:* la intervención queda como `prevista` con causa raíz escrita.
6. **Si te dan ganas de intervenir sin crítica** (una charola "se ve seca", HR "muy alta"): no lo hagas; anota el momento y qué te preocupó. Ese impulso es dato: dice qué advertencia debería escalar antes o qué banda está mal. *Criterio de listo:* "impulsos" anotados en `observaciones`.
7. **Hora 96 · Cierra.** Inspección completa con las manos: charolas perdidas (moho, secas, estiradas), estado de raíces en NFT, nivel del tinaco consumido, kWh si mides. Exporta el histórico de HA de los 4 días. *Criterio de listo:* fila de cierre con resultado.
8. **Decide** con el criterio de abajo; si hubo hallazgo, corrige la causa raíz y **repite** V5 antes de decir que el sistema aguanta vacaciones. *Criterio de listo:* `resultado` y `hallazgo` escritos.

## Criterio de aceptación

!!! example "Aceptar si"
    - **Cero pérdida de cultivo**: ninguna charola ni línea tirada por causa atribuible a riego, ventilación, nivel o dosificación durante las 96 h (una charola con moho por densidad o semilla sucia se anota, pero se juzga en [V8](v08-sanitaria.md)).
    - **Cero intervención no prevista**: no tocaste nada que no te haya pedido una alarma crítica.
    - El histórico de HA muestra los lazos operando dentro de banda (riego, HR, nivel, pH/EC) los 4 días.

    Si hubo **una crítica atendida**: el método pasa "con hallazgo" — el sistema avisó como debía — pero abre una acción de causa raíz (tinaco chico para tu tandeo, boquilla tapada, nodo con Wi-Fi débil) y se repite V5 después de corregir. Dos V5 seguidos con crítica por la misma causa = el sistema **no** aguanta y G1→2 (b) no se evalúa hasta arreglarlo ([06 §V5](../referencia/06-validacion-y-lazos-agenticos.md)).

## Plantilla de registro

`bitacora/validacion/v05-ausencia.csv` (una fila de arranque, una por día de observación, una de cierre):

```csv
fecha_hora,fase,tipo,nivel_tinaco_pct,humedad_min_pct,humedad_max_pct,hr_max_pct,riegos_dia,ph,ec_ms_cm,v_bat,advertencias,criticas,intervencion,charolas_perdidas,observaciones
2027-05-07 18:30,1,arranque,100,62,78,68,,,,,0,0,,,"tinaco lleno; 18 charolas en rack; ultima entrega hecha"
2027-05-08 09:00,1,dia,91,58,79,74,5,,,,0,0,,,"ventilador 3 ciclos noche; N3 el mas seco"
2027-05-09 09:00,1,dia,82,55,80,77,6,,,,1,0,,,"advertencia HR alta 6 h a las 03:10; NO intervine; impulso: abrir cortina"
2027-05-10 09:00,1,dia,71,56,78,71,6,,,,0,0,,,
2027-05-11 07:00,1,cierre,63,57,79,,6,,,,1,0,ninguna,0,"0 perdidas; 37 % del tinaco en 4 dias; HR alta de madrugada -> revisar banda de ventilacion nocturna"
2027-05-11 07:05,1,resultado,,,,,,,,,,,,,"resultado=aprobado; hallazgo=HR 77 % 6 h en madrugada del sabado; accion: forzado nocturno 10 min/h en lluvias (V6) antes del 2027-05-18"
```

- `tipo`: `arranque` · `dia` · `cierre` · `resultado`.
- `intervencion`: `ninguna` · `prevista` (por crítica, con causa en `observaciones`) · `no_prevista` (reprueba).
- En Fase 2 llena `ph`, `ec_ms_cm` y `v_bat`; en Fase 1 quedan vacíos.
- Guarda el export de HA de los 4 días como `bitacora/ha/v05-AAAA-MM-DD.csv`: es evidencia de "v1 estable 30 días".

## Si falla

| Lo que pasó | Causa probable | Qué hacer antes de repetir |
|---|---|---|
| Charolas secas en un nivel | Boquilla tapada, válvula del manifold cerrada de más, sensor de ese nivel leyendo húmedo sin estarlo (conector corroído) | Purga de boquillas, recalibrar capacitivo en seco/húmedo, conector hacia arriba y encintado ([Automatización v1 §4](../fases/fase-1/automatizacion-v1.md)) |
| Moho generalizado en 4 días | HR > 75 % sostenida de noche; densidad alta en lluvias; riego sobre follaje | Banda de ventilación nocturna, forzado 10 min/h jun–sep, −10 % de densidad, riego solo por abajo ([V8](v08-sanitaria.md)) |
| Tinaco < 20 % (crítica) | Tandeo + tinaco chico para tu consumo | Subir a 1,100 L o captación; el interlock funcionó, el dimensionamiento no ([Fase 1 · Agua](../fases/fase-1/agua.md)) |
| Nodo caído (crítica) | Wi-Fi débil en el túnel, fuente con caída, reinicios por relé en 3V3 | Antena o repetidor, buck a 5.0 V con carga, relé al 5 V del buck ([Firmware · problemas](../software/firmware.md)) |
| NFT sin flujo (crítica) con P-2 arrancando | Filtro malla 120 tapado, aire en la succión | El respaldo funcionó; lavar filtro semanal es del ritmo de Fase 2 ([Fase 2 · NFT](../fases/fase-2/nft.md)) |
| Interviniste sin crítica | Una advertencia te asustó | O la banda está mal (corrige y commitea) o la advertencia debería ser crítica (cámbiala). Repite V5 |
| Todo bien pero perdiste una entrega | El sistema aguanta; el negocio no | Plan B del mes 4: ayudante 6 h/sábado con SOP con fotos, $1,300–1,600/mes ([07 §13](../referencia/07-puntos-ciegos-y-riesgos.md)) |

!!! warning "Errores típicos"
    - "Solo voy a mover esta charola": ya no es V5.
    - Empezar con el tinaco a medias y luego culpar al sistema por la crítica de nivel.
    - Hacer V5 la semana del cambio de solución NFT o de la calibración: son intervenciones programadas; muévelas.
    - Declarar "aguanta vacaciones" con un V5 de Fase 1 y usarlo para el NFT: en NFT las raíces mueren en 2–4 h sin flujo; el V5 de Fase 2 es otro.

## Al terminar

- [ ] 96 h sin cosecha, siembra, entrega ni intervención no prevista
- [ ] 4 filas diarias + arranque + cierre + resultado en `bitacora/validacion/v05-ausencia.csv`
- [ ] Cero charolas o líneas perdidas por riego, ventilación, nivel o dosificación
- [ ] Export de HA de los 4 días guardado
- [ ] Si hubo hallazgo: acción de causa raíz con fecha y V5 repetido en el calendario
- Registrar: filas de arriba; en `bitacora/produccion.csv`, `observaciones` = "V5 sin intervención AAAA-MM-DD a AAAA-MM-DD" en las charolas que pasaron por la prueba
- Siguiente paso: [Gate G1→2](../fases/fase-1/gate.md) (Fase 1) · [Timesheet V9](v09-timesheet.md) (Fase 2, para medir lo que el sistema no hace por ti)

## Fuentes

- [06 · Validación §V5, §L0 watchdogs, §escalamiento](../referencia/06-validacion-y-lazos-agenticos.md): 4 días sin tocar nada, aceptar sin pérdida ni intervención no prevista; qué es crítica y qué advertencia.
- [07 · Puntos ciegos §13](../referencia/07-puntos-ciegos-y-riesgos.md) y [research/puntos-ciegos §(l)](../research/puntos-ciegos.md): "aguanta 3–4 días solo" es cierto para riego/alarmas y falso para cosechar/entregar; ayudante desde el mes 4.
- [00 · Plan maestro §Riesgos](../referencia/00-plan-maestro.md): ausencias validadas con V5.
- [research/electrico-respaldo-seguridad §1 y §2.3](../research/electrico-respaldo-seguridad.md): 2–4 h sin flujo en NFT; autonomía 28–30 h con LiFePO4 100 Ah.
- [Diseño · Control](../diseno/control.md): bandas, interlocks y "cómo se prueba" (V3 → V5 → V11).
