# Hacer la prueba de germinación (V1) de un lote de semilla

**En una línea:** 50 semillas, una toalla húmeda y 3–5 días te dicen si un costal se siembra, se reclama o se descarta antes de arriesgar una charola o comprar 5 kg; es el método V1 y la primera fila de tu trazabilidad.

!!! info "Antes de empezar"
    - **Tiempo:** 10 min de montaje + 3–5 días de espera + 10 min de conteo · **Costo:** $0 (toalla de papel, bolsa con cierre, plumón) · **Personas:** 1
    - **Necesitas:** 50 semillas por lote (200 + 200 si vas a validar la Opción A de [sanitización](sanitizar-semilla.md)) · toalla de papel · bolsa con cierre o recipiente con tapa · atomizador con agua potable · plumón indeleble · termómetro o termohigrómetro ($150–199, [Steren](https://www.steren.com.mx/casa-y-oficina/termometros-digitales)) · `bitacora/semilla.csv`
    - **Prerequisitos:** ninguno. Se hace **antes** de [Sembrar una charola](sembrar-una-charola.md), antes de comprar más de 1 kg a un proveedor nuevo y con **cada costal nuevo**: el girasol de CEDA es grado botanero y no trae certificado de germinación ([research/semillas](../research/semillas-sustrato-charolas.md)).

## Cuándo se hace y qué se acepta

| Situación | Muestra | Umbral de aceptación |
|---|---|---|
| Lote nuevo de cualquier proveedor, antes de la primera siembra | 50 semillas | **≥85 %** germinadas |
| Girasol y chícharo (semilla grande, grado alimento) | 50 semillas | **≥80 %** |
| Antes de comprar >1 kg, el costal de 5 kg o el bulto de CEDA | 50 semillas del kilo de prueba | mismo umbral; si pasa, compra |
| Validar la Opción A de sanitización (hipoclorito 20,000 ppm) en un lote | 200 tratadas vs 200 sin tratar | la tratada mantiene el umbral; si cae, ese lote va con Opción B |
| Cada costal nuevo, aunque sea el mismo proveedor | 50 semillas | mismo umbral (el lote cambia aunque el proveedor no) |

Un lote que no pasa **se reclama o se descarta; nunca se siembra "a ver qué pasa"** ([06 · V1](../referencia/06-validacion-y-lazos-agenticos.md)).

## Pasos

1. **Asigna el código de lote interno al costal.** Consecutivo `S001`, `S002`… escrito con plumón en el empaque el día que llega; en `bitacora/semilla.csv` anota proveedor, número de lote del proveedor, fecha de compra y si trae COA. *Criterio de listo:* el costal tiene código visible y su fila existe antes de abrirlo.
2. **Cuenta 50 semillas al azar.** Toma de distintos puntos del costal (arriba, en medio, al fondo), no solo de la superficie. *Criterio de listo:* 50 exactas sobre la mesa; anotaste la fecha.
3. **Humedece la toalla.** Atomiza con agua potable hasta que esté húmeda sin escurrir; extiende las semillas separadas, sin tocarse; dobla la toalla encima. *Criterio de listo:* al levantar la toalla no gotea y ninguna semilla queda seca.
4. **Mete en la bolsa o recipiente y etiqueta.** Sin cerrar hermético (deja aire); escribe `Sxxx`, especie y fecha. *Criterio de listo:* etiqueta legible; la bolsa no queda inflada ni sellada.
5. **Deja 3–5 días a temperatura ambiente, 18–24 °C, fuera del sol directo.** En diciembre–febrero usa el punto más cálido de la casa o el tapete térmico ([Germinar en invierno](germinar-en-invierno.md)): una prueba hecha a 12 °C reprueba lotes buenos. *Criterio de listo:* el termómetro junto a la bolsa marca entre 18 y 24 °C.
6. **Revisa cada día.** Mantén la toalla húmeda (atomiza si se seca) y retira cualquier semilla con pelusa. *Criterio de listo:* toalla húmeda todos los días; sin olor.
7. **Cuenta entre el día 3 y el 5** (las brassicas suelen estar listas al día 3; girasol, chícharo y betabel al día 5). Germinada = raíz blanca visible saliendo de la semilla. `% = germinadas ÷ 50 × 100`. *Criterio de listo:* tienes las dos cifras (probadas y germinadas) escritas antes de tirar la toalla.
8. **Decide y registra.** Pasa → siembra o compra; no pasa → reclama al proveedor o descarta. Girasol de CEDA: si ≥80 %, recompra costal de 5 kg ($140) o bulto ($24/kg); si no, quédate con Al Natural ($185/kg). *Criterio de listo:* la fila de `bitacora/semilla.csv` tiene `%` y `decision`.

!!! example "Dos resultados reales de ejemplo"
    - Rábano Champion `S003`: 43 de 50 germinadas → **86 % → pasa** (umbral 85 %).
    - Girasol CEDA `S001`: 39 de 50 → **78 % → no pasa** (umbral 80 %): reclamar o descartar y sembrar la semana con Al Natural (`S002`); repetir V1 con el siguiente kilo antes de decidir el costal de 5 kg.
    - Girasol CEDA `S004` (segundo kilo): 42 de 50 → **84 % → pasa**; se autoriza la recompra de 5 kg y arranca el A/B de [Fase 0 · Siembra](../fases/fase-0/siembra.md).

!!! tip "Muestreo en charola (el V1 continúa en producción)"
    En el lazo diario L1 cuenta la germinación de **1 charola marcada por lote**: pinta con plumón un cuadro de 10 × 10 cm en la orilla de la charola y cuenta cuántas semillas de ese cuadro emergieron al destape. Si en charola germina mucho menos que en la toalla, el problema está en tu proceso (riego, peso, temperatura), no en la semilla ([06 · L1 y V2](../referencia/06-validacion-y-lazos-agenticos.md)).

!!! warning "Errores típicos"
    - **Tomar las 50 semillas de la superficie del costal.** La semilla vieja o dañada se asienta; muestrea a distintas profundidades.
    - **Dejar secar la toalla un día** o **sellar la bolsa hermética** (pelusa y resultado inválido).
    - **Probar en un cuarto frío en enero** y descartar un lote bueno; mide la temperatura.
    - **Sembrar "porque urge" sin esperar el resultado.** Tres días de espera cuestan menos que 10 charolas que no germinan.
    - **Confiar en el porcentaje del costal anterior.** Cada costal es un lote; cada lote, su V1.

## Al terminar

- [ ] Costal con código `Sxxx` y fila en `bitacora/semilla.csv` (proveedor, lote del proveedor, fecha de compra, COA)
- [ ] 50 semillas contadas de distintos puntos del costal
- [ ] Temperatura de la prueba entre 18 y 24 °C, registrada
- [ ] Conteo hecho al día 3–5 con `%` calculado
- [ ] Decisión escrita: siembra, compra, reclamo o descarte
- **Registrar en `bitacora/semilla.csv`** (si no existe, créalo con este encabezado; es el "registro de semilla" de [research/inocuidad §5](../research/inocuidad-operativa.md) y el dato de entrada de V1):
  `lote_semilla,especie,proveedor,lote_proveedor,fecha_compra,coa,fecha_prueba,semillas_probadas,germinadas,pct_germinacion,decision,observaciones`
  Ejemplo: `S001,girasol,Mayoreo Online (CEDA),2026-08-B12,2026-09-14,no,2026-09-18,50,43,86,acepta,grado botanero; pedir sin tratamiento`
- **Siguiente paso:** [Sanitizar semilla](sanitizar-semilla.md) y [Sembrar una charola](sembrar-una-charola.md). Ficha completa del método en [Validación · V1](../validacion/v01-germinacion.md).

## Fuentes

- [06 · Validación y lazos agénticos](../referencia/06-validacion-y-lazos-agenticos.md): método V1 (50 semillas, 3–5 días, ≥85 % / ≥80 %), muestreo L1, esquema de datos.
- [research/inocuidad-operativa §2 y §5](../research/inocuidad-operativa.md): prueba 200 vs 200 para la Opción A, registro de semilla, COA y lote del proveedor.
- [research/semillas-sustrato-charolas](../research/semillas-sustrato-charolas.md) y [08 · Recetas](../referencia/08-recetas-y-economia-unitaria.md): girasol de CEDA (grado botanero, prueba obligatoria, recompra 5 kg / bulto), precios de semilla.
- [Fase 0 · Siembra](../fases/fase-0/siembra.md): semana 0 de V1 en el calendario de arranque.
