# V6 · Protocolo de experimento A/B (mejora continua)

**En una línea:** un solo cambio a la vez, siempre con control, mínimo 3 charolas por brazo con posiciones alternadas, métrica primaria definida **antes** de sembrar, y el cambio entra al SOP solo si mejora ≥ 10 % esa métrica sin empeorar las secundarias; el agente L3 propone, tú ejecutas y el resultado se commitea.

!!! info "Antes de empezar"
    - **Cuándo:** cuando el informe L3 del domingo propone un experimento, cuando un KPI está en ámbar sin causa clara, o cuando quieres mover una receta (densidad, remojo, oscuridad, setpoint). **Máximo un experimento activo a la vez**; enero (cráter de ventas) es buen mes para correrlos · **Tiempo:** 1 ciclo de cultivo (7–18 días según especie) + 15 min de diseño + 15 min de análisis · **Costo:** el costo variable de 6 charolas (girasol CEDA $9.10; rábano $49.30; arúgula $35.30 c/u) · **Personas:** 1
    - **Necesitas:** un [V2](v02-rendimiento.md) aprobado de esa variedad (CV < 15 % en el control: si el proceso no está controlado, el A/B mide ruido); semilla de un solo lote; básculas; `bitacora/validacion/v06-experimentos.csv`; la plantilla de abajo
    - **Guías relacionadas:** [Sembrar una charola](../guias/sembrar-una-charola.md) · [Diseño · Datos §5 (el informe L3)](../diseno/datos.md) · [Software · Firmware → Cambiar setpoints](../software/firmware.md) · **Desbloquea:** cambiar el SOP, una densidad o un setpoint con un commit que cita la evidencia

## Propósito

Sin control, cualquier mejora es una anécdota: "esta semana rindió más" puede ser la semilla, el clima, la posición o el cambio que hiciste. El A/B aísla el cambio. Y el umbral del 10 % existe para no perseguir mejoras que caben dentro de la variación normal de tres charolas ([06 §V6](../referencia/06-validacion-y-lazos-agenticos.md)). Con el tiempo, el historial de experimentos + decisiones se vuelve el manual de operación real del huerto ([06 §L3](../referencia/06-validacion-y-lazos-agenticos.md)).

Ejemplos de la fuente: densidad **100 g vs 120 g** de girasol; remojo **8 h vs 12 h**; **3 vs 4 días** de oscuridad. El primero de la Fase 0 es semilla **CEDA vs Al Natural** a 135 g ([Fase 0 · Siembra](../fases/fase-0/siembra.md)).

## Reglas

| Regla | Por qué |
|---|---|
| **Un solo cambio** entre los dos brazos; todo lo demás idéntico (lote, densidad, sanitización, remojo, coco, día, riego) | Si cambian dos cosas no sabes cuál actuó |
| **Mínimo 3 charolas por brazo** (6 en total); mejor 4–5 si el rack lo permite | Con menos, una charola rara decide el resultado |
| **Posiciones alternadas** en la pila de oscuridad y en el rack (A/B/A/B/A/B), no un brazo por nivel | El nivel (luz, corriente de aire, boquilla) es un factor escondido |
| **Métrica primaria definida antes** de sembrar: g/charola o % de merma; una sola | Elegirla después es elegir la que salió bien |
| **Secundarias fijadas antes**: merma, CV, moho, días a cosecha, cáscaras pegadas, estiramiento | "No empeorar" solo se puede juzgar si están escritas |
| **Adoptar solo si mejora ≥ 10 %** la primaria y las secundarias del brazo de prueba no salen peor que las del control | Umbral de la fuente; por debajo es ruido |
| **Un experimento activo a la vez** | Dos A/B en el mismo rack se contaminan |
| **El agente propone; tú ejecutas; el resultado se commitea** | El agente nunca cambia densidades ni setpoints solo |

Tolerancia de las secundarias: la fuente pide "sin empeorar"; propuesta operativa: la secundaria del brazo de prueba no es peor que la del control **más allá del CV del control** medido en V2 `[POR VERIFICAR: 06 no fija tolerancia; ajustar con los primeros 3 experimentos]`.

## Procedimiento

1. **Escribe la hipótesis y la plantilla** (abajo) antes de tocar semilla: variable, brazo control (la receta actual del SOP), brazo prueba, n, métrica primaria, criterio de éxito (≥ 10 %), secundarias, fechas. Si el experimento viene del informe L3, copia su propuesta y ajusta lo que no sea viable. *Criterio de listo:* archivo `bitacora/experimentos/EXP-AAAAMMDD-nombre.md` con todos los campos llenos.
2. **Siembra los dos brazos el mismo día**, mismo lote `Sxxx`, alternando posiciones; etiqueta cada charola con su `siembra_id` y en `observaciones` `EXP-… brazo A` / `brazo B`. *Criterio de listo:* 6 filas en `bitacora/produccion.csv` con el `experimento_id` en observaciones.
3. **Trata igual a los dos brazos** durante el ciclo. Cualquier evento (riego a mano, mover una charola) se anota en las dos. *Criterio de listo:* cero diferencias no planeadas.
4. **Cosecha el mismo día, pesa cada charola** y registra las secundarias por charola (merma %, moho sí/no, días a cosecha). *Criterio de listo:* 6 pesos y 6 juegos de secundarias.
5. **Analiza**: media y CV por brazo; `mejora_pct = (media_prueba − media_control) ÷ media_control × 100` (con merma como primaria, la mejora es la **reducción**). Compara cada secundaria. *Criterio de listo:* fila en `v06-experimentos.csv`.
6. **Decide**: `adoptar` (≥ 10 % y secundarias OK), `rechazar`, o `repetir` (resultado entre 5 y 10 %, o CV del control > 15 %). *Criterio de listo:* decisión escrita con fecha.
7. **Si adoptas: commit al SOP.** La receta en tu copia de [08](../referencia/08-recetas-y-economia-unitaria.md) o de [Sembrar una charola](../guias/sembrar-una-charola.md), o el setpoint en `firmware/` con el `experimento_id` en el mensaje del commit. El agente ve el cambio la semana siguiente en el paquete de datos. *Criterio de listo:* hash del commit en la fila.

## Criterio de aceptación

!!! example "Adoptar el cambio solo si"
    - **≥ 3 charolas por brazo**, mismo lote, mismo día, posiciones alternadas, **un solo cambio**.
    - La métrica primaria (fijada antes) mejora **≥ 10 %** en el brazo de prueba respecto al control.
    - **Ninguna secundaria empeora** (merma, CV, moho, días a cosecha…).
    - El CV del brazo control es < 15 % (el proceso estaba controlado; si no, el experimento es inválido y primero se corre [V2](v02-rendimiento.md)).
    - El resultado y la decisión están en `v06-experimentos.csv` y, si se adopta, en un commit.

## Plantilla de experimento

Copia a `bitacora/experimentos/EXP-AAAAMMDD-nombre.md` y llénala **antes** de sembrar:

```markdown
# EXP-20261005-girasol-densidad

- **Propuesto por:** informe L3 2026-W40 / yo
- **Pregunta:** ¿120 g de girasol CEDA rinden ≥ 10 % más g/charola que 100 g sin subir la merma?
- **Variable manipulada:** densidad de semilla seca por charola 1020
- **Brazo A (control, SOP actual):** 100 g
- **Brazo B (prueba):** 120 g
- **Todo lo demás igual:** lote S004, H2O2 3 % 60 °C 5 min, remojo 8 h, coco lote C-2026-09, 3 días de oscuridad con 3 kg, riego por abajo, cosecha día 10
- **n por brazo:** 3 (posiciones en pila y rack: A/B/A/B/A/B; niveles N4–N3–N2)
- **Métrica primaria:** g cosechados por charola · **Criterio de éxito:** media B ≥ media A × 1.10
- **Secundarias (no deben empeorar):** merma %, CV %, moho (sí/no), cáscaras pegadas (%), estiramiento (cm de tallo)
- **Fechas:** siembra 2026-10-05 · destape 2026-10-08 · cosecha 2026-10-15
- **siembra_id:** A: GIR-261005-S004-R1N4, -R1N3, -R1N2 · B: GIR-261005-S004-R1N4b, -R1N3b, -R1N2b
- **Costo del experimento:** 6 × $9.10 = $54.60 de insumo + 6 posiciones de rack por 10 días

## Resultado (llenar al cosechar)
| Brazo | g_1 | g_2 | g_3 | media | CV % | merma % | moho | cáscaras % | estiramiento |
|---|---|---|---|---|---|---|---|---|---|
| A 100 g | | | | | | | | | |
| B 120 g | | | | | | | | | |

- **Mejora primaria:** ___ % (criterio ≥ 10 %) · **Secundarias OK:** sí / no (cuál empeoró)
- **Decisión:** adoptar / rechazar / repetir · **Fecha:** · **Commit:**
- **Qué aprendimos (1–2 líneas):**
```

## Plantilla de registro

`bitacora/validacion/v06-experimentos.csv` (una fila por experimento, cerrada al decidir):

```csv
experimento_id,fecha_inicio,fecha_fin,propuesto_por,variedad,variable,control,prueba,n_por_brazo,metrica_primaria,control_media,prueba_media,mejora_pct,cv_control_pct,cv_prueba_pct,secundarias_ok,decision,commit,observaciones
EXP-20260921-girasol-semilla,2026-09-21,2026-10-01,fase0,girasol,lote de semilla,S002 Al Natural,S001 CEDA,3,g_charola,455,420,-7.7,4.1,5.9,si,adoptar,a1b2c3d,"CEDA rinde 92 % del especifico a 1/5 del costo: margen manda; recompra 5 kg"
EXP-20261005-girasol-densidad,2026-10-05,2026-10-15,L3 2026-W40,girasol,densidad_g,100,120,3,g_charola,388,441,13.7,6.2,7.0,si,adoptar,d4e5f6a,"merma igual (3 %); sin moho; SOP a 120 g en secas"
EXP-20261019-rabano-oscuridad,2026-10-19,2026-10-28,yo,rabano,dias_oscuridad,2,3,3,g_charola,262,270,3.1,8.6,9.4,si,rechazar,,"dentro del ruido; se queda en 2 dias"
```

- En el experimento de semilla la "mejora" fue negativa en gramos y aun así se adoptó CEDA: la métrica primaria real era **margen por charola** (decidida antes: $9.10 vs $29.50 de semilla). Escribe la primaria correcta desde el inicio.
- `commit`: hash del cambio en el SOP o en `firmware/`; vacío si se rechaza.

## Si falla

| Situación | Qué hacer |
|---|---|
| CV del control > 15 % | Experimento inválido: el proceso no está controlado. Corre [V2](v02-rendimiento.md), arregla la causa, repite |
| Mejora entre 5 y 10 % | `repetir` con 4–5 charolas por brazo; no adoptar "porque casi" |
| Mejora ≥ 10 % pero una secundaria empeora (p. ej. +14 % de gramos, +8 % de merma) | `rechazar` o rediseñar: la merma se paga en charolas tiradas y en [V8](v08-sanitaria.md) |
| El brazo de prueba falló por completo (moho, no germinó) | Resultado válido: `rechazar` y anota por qué; no repitas la misma prueba en lluvias si el moho fue el problema |
| Dos experimentos "urgentes" a la vez | Uno. El otro espera al siguiente ciclo; anótalo como cola en el informe L3 |
| Adoptaste sin commit | No existe: el SOP y el firmware en Git son la única verdad; haz el commit con el `experimento_id` |

!!! warning "Errores típicos"
    - Cambiar densidad **y** remojo en el mismo brazo.
    - Poner el brazo B en el nivel de arriba "porque cabe": la posición es un factor.
    - Elegir la métrica primaria después de ver los pesos.
    - Correr el A/B con semilla de dos costales distintos.
    - Dejar que el agente "aplique" el cambio: propone; el commit es tuyo.

## Al terminar

- [ ] Plantilla llena antes de sembrar, con primaria y secundarias fijadas
- [ ] 3+ charolas por brazo, mismo lote y día, posiciones alternadas, un solo cambio
- [ ] Pesos y secundarias por charola en `bitacora/produccion.csv`
- [ ] Fila cerrada en `bitacora/validacion/v06-experimentos.csv` con `mejora_pct` y `decision`
- [ ] Si se adoptó: commit con el `experimento_id`; si no, anotado en el informe L3
- Registrar: `bitacora/experimentos/EXP-….md` (plantilla) y la fila del CSV
- Siguiente paso: el siguiente domingo el informe L3 recibe el resultado en el paquete de datos ([Datos §5](../diseno/datos.md))

## Fuentes

- [06 · Validación §V6 y §L3](../referencia/06-validacion-y-lazos-agenticos.md): un cambio a la vez, control, ≥ 3 charolas por brazo, posiciones alternadas, primaria definida antes, ≥ 10 % sin empeorar secundarias, el agente propone y el resultado se commitea; ejemplos 100 vs 120 g, 8 vs 12 h, 3 vs 4 días.
- [08 · Recetas y economía unitaria](../referencia/08-recetas-y-economia-unitaria.md): rangos de densidad y costos por charola; A/B CEDA vs específica.
- [Fase 0 · Siembra](../fases/fase-0/siembra.md): el primer A/B (semilla) como V2 + V6 y sus reglas de decisión.
- [Diseño · Datos §5](../diseno/datos.md): contrato del informe L3 (máximo un experimento, formato V6) y el flujo de aprobación.
- [Guía · Germinar en invierno](../guias/germinar-en-invierno.md): enero como mes de experimentos.
