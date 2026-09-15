# V9 · Timesheet honesto

**En una línea:** cuatro semanas seguidas cronometrando TODO lo que el huerto te quita (siembra, lavado, cosecha, empaque, reparto, ventas, cobranza, mantenimiento) para saber si son las 6–9 h/semana que promete el plan o las 14.5–17.5 de la cuenta honesta; si da más de 12 h, la automatización tiene un hueco o el proceso un desperdicio y se ataca **antes** de escalar volumen — es la validación que casi nadie hace y la razón #1 de burnout en microgranjas.

!!! info "Antes de empezar"
    - **Cuándo:** 4 semanas seguidas en régimen (Fase 1 con 25–35 charolas/semana; obligatorio en Fase 2, S30–33, antes de [G2→3](gates.md)); después, **una semana completa al mes**; siempre que un rubro "se sienta" pesado · **Tiempo:** 30 s por evento + 10 min el domingo · **Costo:** $0 · **Personas:** 1 (solo tus horas; las del ayudante van como costo, no como tiempo)
    - **Necesitas:** cronómetro del teléfono, `bitacora/timesheet.csv` con la lista de rubros **fija**, `tools/gate_audit.py` o una hoja de cálculo para promediar
    - **Guía paso a paso:** [Llevar el timesheet semanal](../guias/timesheet-semanal.md) · **Desbloquea:** [G2→3 (b)](gates.md) (≤ 9 h/semana); la decisión de contratar ayudante o recortar clientes

## Propósito

La automatización quita riego, ventilación y vigilancia (5–8 h que serían), pero **no siembra, no corta, no lava, no reparte y no cobra** ([07 §4](../referencia/07-puntos-ciegos-y-riesgos.md)). El desglose honesto en régimen Fase 1–2 (30 charolas/semana + NFT + 4–6 clientes) da **14.5–17.5 h/semana**. A $10k netos/mes ÷ 65 h ≈ $150/h: buen negocio secundario, pero hay que compararlo contra tu tarifa antes de escalar m² en lugar de precio. Y la regla anti-burnout es medible: **3 semanas seguidas por encima de 18 h → se contrata o se recortan clientes; prohibido "aguantar"** ([07 §13](../referencia/07-puntos-ciegos-y-riesgos.md)).

## Los rubros (no se cambian a media medición)

| `rubro` | Qué incluye (de puerta a puerta) | h/semana que espera la cuenta honesta |
|---|---|---|
| `siembra` | Pesar, sanitizar, remojar, hidratar coco, sembrar, apilar (2 sesiones) | 3.0 |
| `cosecha_empaque` | Inspección, corte, pesado, etiqueta, refrigerador; hierbas NFT | 3.5–4.5 |
| `lavado` | Charolas, mesa, tijera, hielera | 1.5 |
| `reparto` | Cargar, ruta, remisiones, recoger charolas | 3.0–4.0 |
| `ventas_cobranza` | WhatsApp con chefs, fresh sheet, visitas, facturas, REP, conciliación | 1.5–2.0 |
| `sistema` | Calibrar sondas, limpiar depósito, ajustes de HA, cambio de solución | 1.0–1.5 |
| `compras` | Insumos, imprevistos, ir por semilla o coco | 1.0 |
| `otro` | Vecinos, alcaldía, laboratorio, informe L3 | — |
| **Total** | | **14.5–17.5** |

## Procedimiento

1. **Fija la lista de rubros y el lunes de arranque.** No agregues ni renombres rubros durante las 4 semanas. *Criterio de listo:* encabezado del CSV escrito y `semana` ISO de inicio anotada.
2. **Cronometra cada sesión de puerta a puerta**, preparar y limpiar incluidos; sesión interrumpida = dos filas; la fila se escribe al terminar la sesión, nunca el domingo. *Criterio de listo:* cada fila tiene `minutos` y, cuando aplica, `unidades` (charolas, paradas, facturas).
3. **Cuenta lo invisible:** WhatsApp desde el sillón, la llamada al administrador que no pagó, la ida por gel packs, los 20 min del informe L3. *Criterio de listo:* ningún día con horas de huerto y cero filas.
4. **Domingo (10 min): suma por rubro y total**; calcula `minutos ÷ unidades` en siembra, cosecha y reparto. *Criterio de listo:* 8 números (7 rubros + total) junto a los KPIs L2.
5. **Semana 4: promedia y compara** con la tabla de umbrales; identifica el rubro más caro y su palanca ([guía · palancas por rubro](../guias/timesheet-semanal.md)). *Criterio de listo:* promedio, rubro mayor y una acción con fecha.
6. **Aplica la palanca —un solo cambio ([V6](v06-experimento-ab.md))— y vuelve a medir 4 semanas.** *Criterio de listo:* el rubro atacado bajó ≥ 10 % sin subir otro.
7. **En régimen: una semana completa al mes**, y las 4 semanas seguidas antes de cada gate. *Criterio de listo:* al menos una semana completa por mes en el CSV.

## Criterio de aceptación y lectura

| Promedio de 4 semanas (solo tus horas) | Lectura | Acción |
|---|---|---|
| **≤ 9 h** | Cumple [G2→3 (b)](gates.md) | Medir 1 semana al mes |
| 9–12 h | Lo que el plan prometía "más o menos" | Atacar el rubro más caro con su palanca |
| **> 12 h** | "La automatización tiene un hueco o el proceso un desperdicio" ([06 §V9](../referencia/06-validacion-y-lazos-agenticos.md)) | Atacar el rubro más caro **antes** de escalar volumen; no sembrar más |
| 14.5–17.5 h | La cuenta honesta de régimen ([07 §4](../referencia/07-puntos-ciegos-y-riesgos.md)) | $150/h: compáralo con tu tarifa; palancas de precio y ayudante, no de m² |
| **≥ 18 h tres semanas seguidas** | Regla anti-burnout ([07 §13](../referencia/07-puntos-ciegos-y-riesgos.md)) | **Contratar** ayudante 6 h/sábado con SOP con fotos ($1,300–1,600/mes, ~15 % del neto) **o recortar clientes.** Prohibido aguantar |

!!! example "El método se considera ejecutado (no 'aprobado') si"
    - Hay **4 semanas ISO consecutivas** con una fila por sesión, sin reconstruir de memoria, con la lista de rubros fija y la semana "mala" incluida.
    - Está calculado el promedio semanal total y por rubro, y el rubro más caro tiene una acción escrita con fecha.
    - Para el gate: el promedio es **≤ 9 h/semana** → pasa G2→3 (b). Si no, no se renegocia: se ataca el rubro y se re-mide.

!!! info "La tensión que hay que entender"
    G2→3 pide ≤ 9 h medidas; la cuenta honesta da 14.5–17.5 h. Operando bien, lo normal es **no** pasar (b) en el primer intento. No se suben las horas a 15 "porque 07 lo dice": 07 corrige el pronóstico, no el criterio de entrada a una fase que solo gasta. Se permanece en Fase 2 aplicando la escalera (precio → ayudante → LED solo con contrato PDBT → segunda ubicación) y se re-evalúa en 3 meses ([Fase 2 · Gate §2](../fases/fase-2/gate.md)).

## Plantilla de registro

`bitacora/timesheet.csv` (esquema de la [guía](../guias/timesheet-semanal.md)):

```csv
fecha,semana,rubro,minutos,unidades,observaciones
2027-04-05,2027-W14,siembra,85,10,"10 charolas: 6 girasol + 4 rabano; remojo aparte"
2027-04-06,2027-W14,cosecha_empaque,140,9,"9 charolas vivas + 2 clamshell; etiquetas"
2027-04-06,2027-W14,reparto,110,6,"ruta martes 6 paradas; 20 min de trafico extra en Insurgentes"
2027-04-06,2027-W14,ventas_cobranza,25,3,"3 facturas + recordatorios; 1 conciliacion"
2027-04-08,2027-W14,lavado,45,12,"tanda del jueves"
2027-04-11,2027-W14,sistema,40,,"calibracion quincenal pH/EC"
2027-04-11,2027-W14,otro,20,,"informe L3 y plan de siembra"
```

Resumen semanal para el gate (propuesta; lo puede generar `tools/gate_audit.py` a partir del CSV `[POR VERIFICAR: interfaz en software/herramientas-cli.md]`), `bitacora/validacion/v09-resumen.csv`:

```csv
semana,siembra_h,cosecha_empaque_h,lavado_h,reparto_h,ventas_cobranza_h,sistema_h,compras_h,otro_h,total_h,charolas_sem,min_por_charola_siembra,min_por_charola_cosecha,min_por_parada,observaciones
2027-W14,2.8,4.2,1.5,3.7,1.9,0.7,1.0,0.3,16.1,30,8.5,15.6,18.3,"reparto es el rubro mayor: 2 paradas a > 8 km"
2027-W15,3.0,4.5,1.4,3.9,2.2,0.5,0.8,0.5,16.8,31,8.7,15.0,19.5,
2027-W16,2.9,4.0,1.6,3.5,1.6,1.4,1.2,0.2,16.4,29,8.9,14.8,17.5,"cambio de solucion NFT"
2027-W17,3.1,4.4,1.5,3.8,1.8,0.6,0.9,0.4,16.5,31,8.6,15.2,19.0,"promedio 4 sem: 16.5 h -> > 12 h: atacar reparto (ruta 2 dias, <= 8 paradas, radio 5-8 km)"
```

## Si falla

| Rubro disparado | Palanca (con datos de esta wiki) |
|---|---|
| `reparto` (3–4 h) | Radio ≤ 5–8 km, 2 días fijos, ≤ 8 paradas ordenadas por zona, pedido mínimo $350–400; un cliente a 12 km cuesta 40 min por ruta ([Ruta de reparto](../guias/ruta-de-reparto.md)) |
| `cosecha_empaque` (3.5–4.5 h) | Charola viva en lugar de cortado: 5 min vs 15–20 por charola y sin cadena de frío; cortado solo bajo pedido ([Cosechar y empacar](../guias/cosechar-y-empacar.md)) |
| `siembra` (3 h) | Dos sesiones fijas; semilla pesada por adelantado en bolsas por charola; coco hidratado en tanda |
| `lavado` | En tanda el día de cosecha; pila de remojo con jabón mientras cosechas |
| `ventas_cobranza` | Fresh sheet única del domingo por lista de difusión; REP agrupado los días 1–5; un referido por chef contento (CAC −70 %) |
| `sistema` | Calibración quincenal con alarma de HA, no "cuando se ve raro"; cambio de solución el mismo día |
| `compras` | Pedido grande mensual (costal de 5 kg, coco por tarima) en lugar de idas semanales |
| Total ≥ 18 h × 3 semanas | Ayudante 6 h/sábado con SOP; o recortar el cliente que más tiempo cuesta por peso (el de 12 km, el que no paga) |

!!! warning "Errores típicos"
    - Reconstruir el domingo de memoria: siempre sale menos de lo real.
    - Contar solo "trabajo en el patio": reparto, WhatsApp y cobranza son 4.5–6 h y son las que nadie cuenta.
    - Cronometrar "una semana buena": V9 son 4 seguidas, con la mala incluida.
    - Contar el trabajo de un familiar como $0 y como 0 h: si no está en el timesheet ni en el costo, el gate miente.
    - Optimizar el rubro chico porque es fácil.

## Al terminar

- [ ] 4 semanas seguidas con una fila por sesión y `unidades` donde aplica
- [ ] Promedio total y por rubro; rubro más caro identificado con acción y fecha
- [ ] Ninguna semana con horas de huerto y cero filas
- [ ] Regla de 18 h revisada (¿3 semanas seguidas?)
- [ ] Una semana de medición al mes agendada
- Registrar: `bitacora/timesheet.csv` y el resumen de 4 semanas en `bitacora/validacion/v09-resumen.csv`; el promedio y el rubro mayor en el informe del gate (`bitacora/gates/`)
- Siguiente paso: [Gates → G2→3](gates.md); si el rubro mayor es reparto, [Ruta de reparto](../guias/ruta-de-reparto.md); si es cosecha, mover clientes a charola viva

## Fuentes

- [06 · Validación §V9 y §L4](../referencia/06-validacion-y-lazos-agenticos.md): 4 semanas cronometrando TODO, 6–9 h prometidas, > 12 h = hueco, gate ≤ 9 h, "la razón #1 de burnout".
- [07 · Puntos ciegos §4, §13, §14](../referencia/07-puntos-ciegos-y-riesgos.md) y [research/puntos-ciegos §(l)](../research/puntos-ciegos.md): desglose 14.5–17.5 h, $150/h, regla de 18 h × 3, ayudante $1,300–1,600/mes, escalera de escalamiento.
- [Guía · Timesheet semanal](../guias/timesheet-semanal.md): esquema del CSV, palancas por rubro.
- [Fase 2 · Gate](../fases/fase-2/gate.md): la tensión entre el gate y el número corregido; cómo se promedia.
- [00 · Plan maestro §Números](../referencia/00-plan-maestro.md): "6–9 h/semana según el plan; se verifica con V9".
