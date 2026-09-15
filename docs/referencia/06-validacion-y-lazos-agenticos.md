# Validación y lazos agénticos

El proyecto se opera como un sistema de control por capas: cada capa es un lazo cerrado
(medir → comparar contra referencia → actuar → registrar), con su propia frecuencia y su
propio responsable (firmware, humano o agente LLM). Nada avanza "por fe": cada fase, cada
compra grande y cada cambio de proceso pasa por un método de validación explícito.

## Arquitectura de lazos (L0–L4)

```
L4  Lazo de fase (gates Go/No-Go)          ── mensual/por fase ── humano
L3  Lazo agéntico LLM (análisis + plan)    ── semanal          ── agente + humano aprueba
L2  Lazo comercial (KPIs de negocio)       ── semanal          ── humano
L1  Lazo del operador (bitácora + muestreo)── diario, 10 min   ── humano
L0  Lazos de máquina (riego, pH/EC, alarmas)── seg–min          ── ESP32/ESPHome/HA
```

Regla de diseño: **una capa solo escala problemas hacia arriba, nunca los resuelve dos veces.**
Si L0 puede corregirlo (riego, dosificación), L1 no lo toca; si L1 lo detecta pero no lo
explica (rendimiento cayendo), lo empuja a L3.

---

## L0 — Lazos de máquina (ESPHome / Home Assistant)

Lazos de histéresis simples, sin PID: las plantas son procesos lentos y la histéresis con
banda muerta es más robusta que un PID mal sintonizado con sondas baratas.

| Lazo | Sensor | Referencia | Actuador | Regla |
|---|---|---|---|---|
| Riego microgreens | Humedad capacitiva de sustrato ×4 | banda por etapa (germinación vs desarrollo) | Bomba 12 V + nebulizadores | ON si < límite inferior, OFF si > superior; máx. N ciclos/h |
| pH NFT | Sonda pH | 5.8–6.2 | Peristáltica pH− | dosis fija pequeña → esperar T_mezcla (10–15 min) → re-medir |
| EC NFT | Sonda EC | 1.2–1.8 mS/cm según cultivo | Peristálticas A y B | igual: dosis + tiempo muerto de mezcla, nunca dosificación continua |
| Nivel tinaco | JSN-SR04T | > 20 % | Válvula de llenado / bloqueo | bloqueo de dosificación y bomba con nivel bajo (interlock) |
| Ventilación | SHT31 (T/HR) | HR < 75 %, T < 28 °C | Ventilador | ON por histéresis; forzado 10 min/h en temporada de lluvia |

### Watchdogs (la parte que evita perder un cultivo)

Un lazo que actúa sin verificar que la acción ocurrió no es un lazo, es una esperanza.

- **Bomba tapada / línea rota:** si `bomba = ON` y el sensor de flujo YF-S201 reporta
  `< X L/min` durante 60 s → alarma crítica + apagar bomba (protege la bomba en seco).
- **Sonda descalibrada / muerta:** si pH o EC no cambian nada en 24 h con dosificaciones
  hechas, o saltan > 1.5 unidades en 5 min → marcar sensor "no confiable", suspender
  dosificación automática, alarma. (Las sondas baratas fallan *mintiendo*, no callando.)
- **Nodo caído:** heartbeat de cada ESP32 hacia Home Assistant; sin señal 10 min → alarma.
- **Corte de luz:** HA en Raspberry con UPS pequeño; al volver la energía, notificación con
  duración del corte (en NFT, > 2 h sin recirculación en día caluroso = raíces en riesgo).
- **Deriva de dosificación:** contador de mL dosificados/día; si excede 2× el promedio móvil
  de 7 días → alarma (fuga, sonda mintiendo o depósito contaminado).

### Escalamiento de alarmas

| Severidad | Ejemplo | Canal | Tiempo de respuesta esperado |
|---|---|---|---|
| Info | ciclo de riego ejecutado | log/dashboard | ninguno |
| Advertencia | tinaco < 40 %, HR alta 6 h | push (app HA) | mismo día |
| Crítica | flujo cero con bomba ON, nodo caído, nivel < 20 % | push repetido + Telegram/llamada (HA puede llamar vía Twilio o similar) | < 1 h |

---

## L1 — Lazo del operador (10 minutos diarios)

Checklist dirigido por excepciones: el dashboard muestra solo lo que salió de banda; lo
demás no se revisa "por si acaso".

1. Revisar panel de excepciones (alarmas de la noche, tendencias fuera de banda).
2. Inspección visual de 2 minutos: moho (pelusa *azul/verde/negra* = tirar charola;
   los pelos radiculares blancos y uniformes son normales), color, estiramiento.
3. Muestreo de germinación: contar 1 charola marcada por lote (ver V2).
4. Registrar en bitácora (30 s por evento — ver esquema de datos abajo).

---

## L2 — Lazo comercial semanal (30–60 min, mismo día siempre)

| KPI | Definición | Meta | Umbral rojo |
|---|---|---|---|
| Sell-through | charolas vendidas / charolas cosechadas | ≥ 90 % | < 75 % dos semanas seguidas |
| Merma de producción | charolas tiradas / sembradas | ≤ 10 % | > 20 % |
| Entregas a tiempo | entregas en ventana pactada / totales | 100 % | < 90 % |
| Recompra | clientes que repiten pedido semana a semana | ≥ 80 % | cliente ancla sin pedir 2 semanas |
| Margen variable | (precio − insumos − reparto) / precio | ≥ 60 % | < 45 % |
| CAC | horas de venta + muestras regaladas / cliente cerrado | tender a la baja | > 3 visitas y 3 muestras por cliente |
| Feedback | 1 pregunta por WhatsApp a cada chef tras entrega ("¿algo que cambiarías del producto de esta semana?") | respuesta de ≥ 50 % | 2 quejas del mismo tipo |

Reglas de decisión (escritas de antemano para no autoengañarse):

- Sell-through < 75 % dos semanas → **no sembrar más volumen**; el problema es venta, no producción.
- Merma > 20 % → congelar variedad nueva, correr V8 (auditoría sanitaria) y revisar densidad de siembra.
- Cliente ancla sin pedir 2 semanas → visita presencial esa semana, no mensaje.

---

## L3 — Lazo agéntico LLM (semanal)

El lazo "divertido" y el que convierte los datos en criterio. Un agente (Claude vía API, o
una sesión de Claude Code corrida por cron) recibe cada domingo:

1. Export CSV de Home Assistant/InfluxDB de la semana (T, HR, pH, EC, riegos, alarmas).
2. La bitácora de producción (siembras, cosechas, mermas).
3. El log de ventas y feedback de clientes.
4. El estado de los KPIs de L2 y los experimentos activos.

Y produce un **informe semanal** con este contrato:

```text
Eres el agrónomo/analista de un microhuerto comercial en CDMX. Con los CSV adjuntos:
1. ANOMALÍAS: desviaciones de la semana vs las 4 anteriores (ambiente, consumo de agua,
   dosificación, rendimiento por variedad). Solo las significativas, con evidencia numérica.
2. CAUSA PROBABLE: para cada anomalía, hipótesis rankeadas y qué dato falta para confirmar.
3. EXPERIMENTO: propone máximo UN experimento A/B para la semana entrante (formato V6),
   con métrica, tamaño de muestra (charolas) y criterio de éxito.
4. PLAN: borrador de plan de siembra de la semana (variedades y cantidades) a partir de
   pedidos recurrentes + sell-through, con su razonamiento.
5. RIESGO: la única cosa que más probabilidad tiene de salir mal la próxima semana.
Responde en ≤ 1 página. No inventes datos: si un CSV está vacío o roto, dilo.
```

**El humano aprueba o corrige el plan; el agente nunca ejecuta compras ni cambia setpoints
solo.** Con el tiempo, el histórico de informes + decisiones se vuelve el manual de
operación real del huerto (y material de venta ante chefs: "monitoreo 24/7 con análisis
semanal").

Nivel 2 del lazo agéntico (opcional, fase 2+): darle al agente acceso de *lectura* a la API
de Home Assistant para que consulte lo que necesite al redactar el informe, y permitirle
abrir *pull requests* contra este repositorio (cambios a SOPs, densidades de siembra,
setpoints propuestos en YAML). El merge lo hace el humano: el PR es el mecanismo de
aprobación.

---

## L4 — Gates de fase (Go / No-Go medibles)

Los gates del plan original, convertidos en criterios que un tercero podría auditar:

| Gate | Métrica | Umbral | Fuente de dato | Decisión |
|---|---|---|---|---|
| G0→1 | clientes con ≥ 3 compras semanales consecutivas | ≥ 2 | log de ventas | Go / iterar 2 semanas más / abortar (pérdida acotada ~$6k) |
| G0→1 (b) | margen variable en ventas reales | ≥ 55 % | bitácora + precios | si falla: subir precio o bajar costo antes de invertir |
| G1→2 | clientes fijos + demanda insatisfecha | 4–5 fijos y pedidos rechazados 2 semanas seguidas | log de ventas | Go |
| G1→2 (b) | automatización v1 estable | 30 días con < 2 alarmas críticas/semana y cero pérdidas por fallo de riego | HA | si falla: NO agregar NFT sobre una base inestable |
| G2→3 | el sistema se paga solo | neto ≥ $12k/mes por 3 meses y ≤ 9 h/semana medidas (ver V9) | contabilidad + timesheet | Go a "juguetes" |

Regla dura: **un gate no alcanzado no se renegocia a la baja; se itera o se detiene.** Las
condiciones se escriben aquí, en Git, antes de empezar la fase — los commits son el registro
de que no se movieron los postes.

---

## Métodos de validación V1–V11

Protocolos concretos, cada uno de una página mental: qué, cómo, criterio de aceptación.

### V1 — Prueba de germinación por lote de semilla
Antes de sembrar (y antes de comprar > 1 kg de un proveedor nuevo): 50 semillas entre toalla
húmeda, bolsa, 3–5 días a temperatura ambiente. **Aceptar lote si ≥ 85 % germina** (girasol y
chícharo ≥ 80 %). Registrar % por `lote_semilla` en la bitácora; un lote malo se reclama o se
descarta, nunca se siembra "a ver qué pasa".

### V2 — Ensayo de rendimiento por variedad
3 charolas idénticas por variedad nueva (misma densidad, mismo lote): pesar gramos cosechados
por charola. **Aceptar si el coeficiente de variación < 15 %** y el rendimiento medio cubre el
costo con el margen meta. Si CV ≥ 15 %, el proceso no está controlado: revisar densidad,
riego o presión de peso antes de vender esa variedad.

### V3 — Dry-run de automatización (HIL casero)
Antes de poner una sola planta bajo el sistema: 72 h corriendo con agua sola, con inyección
deliberada de fallas — desconectar la bomba, vaciar el tinaco por debajo del 20 %, pellizcar
la línea, apagar un ESP32, cortar el WiFi 30 min. **Aceptar si el 100 % de las fallas produjo
la alarma correcta en el canal correcto** y ningún actuador quedó en estado inseguro.
Documentar como tabla FMEA-lite: falla → efecto → detección → respuesta observada.

### V4 — Smoke test comercial (vender antes de construir)
La Fase 0 completa es este método, formalizado: 15 restaurantes mapeados → visitas con
muestra física → medir el embudo: `visitados → probaron → pidieron una vez → recurrentes`.
**Registrar las cuatro cifras cada semana.** La conversión visitado→recurrente esperable es
10–20 %; si tras 15 visitas reales hay 0 recurrentes, el problema es producto/precio/zona y
se pivota ANTES de la Fase 1.

### V5 — Prueba de estrés de ausencia
Con el sistema en producción: 4 días sin tocar nada (quedarse en casa, pero sin intervenir
salvo alarma crítica). **Aceptar si no hubo pérdida de cultivo ni intervención no prevista.**
Esto valida la promesa de "el sistema aguanta vacaciones" con datos, no con optimismo.

### V6 — Protocolo de experimento A/B (mejora continua)
Un solo cambio a la vez, siempre con control: p. ej. densidad 100 g vs 120 g de girasol,
remojo 8 h vs 12 h, 3 vs 4 días de oscuridad. Mínimo 3 charolas por brazo, misma posición en
rack alternada. Métrica primaria definida ANTES (g/charola, o % merma). **Adoptar el cambio
solo si mejora ≥ 10 % la métrica primaria sin empeorar las secundarias.** El agente de L3
propone; el humano ejecuta; el resultado se commitea al SOP.

### V7 — Validación de agua
Al arrancar y cada temporada: medir pH y EC del agua de red y de la captada de lluvia
(la de lluvia debería salir con EC ≪ 0.3 mS/cm). Si la red sale dura (EC > 0.8), la
estrategia de nutrición NFT se formula sobre esa base o se prioriza lluvia/filtrada.
Una vez al año: análisis de laboratorio (coliformes y metales) del agua que toca producto
que se vende — es barato comparado con perder un cliente por inocuidad.

### V8 — Auditoría sanitaria (moho y plagas)
Semanal: % de charolas con cualquier signo de hongo, conteo de pulgón en 5 hojas marcadas de
albahaca. **Umbral: > 10 % de charolas afectadas o pulgón en 2+ plantas marcadas** dispara el
protocolo: H2O2 en desinfección, +ventilación forzada, bajar densidad de siembra 10 %, y
charola afectada a la basura sin negociar (el costo de una charola es ruido; el de una
entrega rechazada, no).

### V9 — Timesheet honesto
4 semanas cronometrando TODO (siembra, lavado, cosecha, empaque, reparto, ventas, cobranza,
mantenimiento). El plan promete 6–9 h/semana en régimen; **si la medición da > 12 h, la
automatización tiene un hueco o el proceso tiene un desperdicio** — se ataca el rubro más
caro en tiempo antes de escalar volumen. (Es la validación que casi nadie hace y la razón
#1 de burnout en microgranjas.)

### V10 — Simulacro de retiro (mock recall)
Una vez al año: elegir un lote al azar y demostrar en **< 2 horas** a qué clientes llegó y
de qué costal de semilla salió, con los registros de la bitácora. Documentarlo. Es la
pregunta estándar de auditoría de hoteles y la prueba de que la trazabilidad funciona de
verdad (formato de lote y campos por charola en
[research/inocuidad-operativa.md](../research/inocuidad-operativa.md)).

### V11 — Simulacro mensual de apagón
Botar el breaker del patio 10 minutos, una vez al mes: la bomba NFT debe seguir corriendo
desde batería, deben llegar las alertas de "corte de CFE" y, al restaurar, no debe haber
falso "sin flujo". Un respaldo que no se prueba mensualmente es un respaldo que falla el
día del corte real. (Arquitectura DC-first: [03 §2.3](03-instalacion.md).)

---

## Esquema de datos (la bitácora es el sensor de L2–L4)

Un CSV (o Google Sheet exportada) versionado en este repo, una fila por evento:

```csv
# bitacora/produccion.csv
siembra_id,fecha_siembra,variedad,lote_semilla,densidad_g,dias_oscuridad,fecha_cosecha,rendimiento_g,merma_pct,destino,precio_mxn,observaciones
GIR-260915-S001-R1N2,2026-09-15,girasol,S001,135,3,2026-09-24,420,5,RestA,105,primer lote proveedor nuevo; sanitizado H2O2 3%
```

Formato de `siembra_id` (legible por humanos, rastreable en minutos hacia atrás y hacia
adelante): `VAR-AAMMDD-Slote-posición` — p. ej. `GIR-260915-S001-R1N2` = girasol, sembrado
15-sep-2026, costal de semilla S001 (ligado en un registro aparte al proveedor, su lote y su
COA), rack 1 nivel 2. El mismo código va en masking tape sobre la charola y se copia a la
etiqueta al empacar.

```csv
# bitacora/ventas.csv
fecha,cliente,producto,cantidad,precio_unit_mxn,entregado_a_tiempo,feedback
```

Reglas: se llena el mismo día (30 s por evento), nunca de memoria al final de la semana; los
IDs de siembra van también en una etiqueta física en la charola (masking tape + marcador es
suficiente; QR después si dan ganas).

---

## Resumen operativo

- **Diario:** 10 min — excepciones del dashboard, inspección visual, bitácora.
- **Semanal:** KPIs L2 + informe del agente L3 + máximo un experimento V6 activo.
- **Quincenal:** calibración de sondas pH/EC con buffers 4.0/6.86 y solución patrón EC
  1.413 mS/cm (en el calendario, con alarma de HA; una sonda sin calibrar es un generador
  de números aleatorios). Presupuesto honesto: ~$1,050/año incluyendo sonda de repuesto
  anual, no los $400 del plan original.
- **Por fase:** gate L4 con sus números, commiteado antes de gastar un peso en la siguiente.
