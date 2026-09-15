# V1 · Prueba de germinación por lote de semilla

**En una línea:** 50 semillas entre toalla húmeda, 3–5 días, y sabes si el costal se siembra, se reclama o se descarta antes de arriesgar una charola o comprar 5 kg; es el método más barato de toda la sección y la primera fila de tu trazabilidad.

!!! info "Antes de empezar"
    - **Cuándo:** antes de sembrar cualquier lote nuevo; antes de comprar > 1 kg a un proveedor nuevo; con **cada costal**, aunque sea del mismo proveedor · **Tiempo:** 10 min de montaje + 3–5 días de espera + 10 min de conteo · **Costo:** $0 · **Personas:** 1
    - **Necesitas:** 50 semillas por lote (200 + 200 si validas la Opción A de sanitización), toalla de papel, bolsa con cierre o recipiente con tapa, atomizador con agua potable, plumón indeleble, termómetro (el de cocina de $150 del `bom/fase0.csv` sirve), `bitacora/semilla.csv`
    - **Guía paso a paso:** [Hacer la prueba de germinación](../guias/prueba-de-germinacion.md) · **Desbloquea:** sembrar el lote; la recompra del costal de 5 kg o del bulto de CEDA

## Propósito

El girasol de CEDA es grado botanero y no trae certificado de germinación; el chícharo "barato" depende de validar arvejón grado alimento; y cualquier costal puede venir viejo o mal almacenado ([08 · Reglas económicas](../referencia/08-recetas-y-economia-unitaria.md)). Un lote malo sembrado "a ver qué pasa" cuesta 10 charolas, una semana de rack y una entrega; la prueba cuesta tres días de espera. Además, el número de lote del costal y su resultado V1 son la mitad de la trazabilidad que pide un hotel ([research/inocuidad §5](../research/inocuidad-operativa.md)).

## Cuándo y con qué muestra

| Situación | Muestra | Umbral |
|---|---|---|
| Lote nuevo de cualquier proveedor, antes de la primera siembra | 50 semillas | **≥ 85 %** |
| Girasol y chícharo (semilla grande, grado alimento) | 50 semillas | **≥ 80 %** |
| Antes de comprar > 1 kg (costal de 5 kg, bulto de CEDA) | 50 semillas del kilo de prueba | Mismo umbral; si pasa, compra |
| Validar la Opción A de sanitización (hipoclorito de calcio 20,000 ppm) en un lote | 200 tratadas vs 200 sin tratar | La tratada mantiene el umbral; si cae, ese lote va con Opción B (H2O2 3 %) |
| Cada costal nuevo del mismo proveedor | 50 semillas | Mismo umbral: el lote cambia aunque el proveedor no |

## Procedimiento

1. **Asigna el código de lote interno al costal** el día que llega: consecutivo `S001`, `S002`… con plumón en el empaque, y su fila en `bitacora/semilla.csv` (proveedor, lote del proveedor, fecha de compra, si trae COA). *Criterio de listo:* el costal tiene código visible y su fila existe antes de abrirlo.
2. **Cuenta 50 semillas al azar** de distintas profundidades del costal (arriba, en medio, al fondo). *Criterio de listo:* 50 exactas y la fecha anotada.
3. **Humedece la toalla** con el atomizador hasta que esté húmeda sin escurrir; extiende las semillas sin que se toquen; dobla la toalla encima. *Criterio de listo:* la toalla no gotea al levantarla y ninguna semilla queda seca.
4. **Mete en la bolsa sin sellar hermético** y etiqueta `Sxxx`, especie y fecha. *Criterio de listo:* etiqueta legible; la bolsa deja aire.
5. **Deja 3–5 días a temperatura ambiente, 18–24 °C**, fuera del sol directo. De diciembre a febrero usa el punto más cálido de la casa o el tapete térmico ([Germinar en invierno](../guias/germinar-en-invierno.md)): una prueba a 12 °C reprueba lotes buenos. *Criterio de listo:* el termómetro junto a la bolsa marca 18–24 °C.
6. **Revisa cada día**: atomiza si la toalla se seca; retira cualquier semilla con pelusa. *Criterio de listo:* toalla húmeda todos los días; sin olor.
7. **Cuenta entre el día 3 y el 5** (brassicas al día 3; girasol, chícharo y betabel al día 5). Germinada = raíz blanca visible. `pct = germinadas ÷ 50 × 100`. *Criterio de listo:* las dos cifras escritas antes de tirar la toalla.
8. **Decide y registra.** Pasa → siembra o compra. No pasa → reclama al proveedor o descarta. *Criterio de listo:* la fila tiene `pct_germinacion` y `decision`.

## Criterio de aceptación

!!! example "Aceptar el lote si"
    - **≥ 85 %** de las 50 semillas germinaron (**≥ 80 %** en girasol y chícharo), contadas entre el día 3 y el 5 a 18–24 °C.
    - En la validación de la Opción A: el lote **tratado** mantiene el umbral.
    - El resultado está en `bitacora/semilla.csv` **antes** de la primera siembra del lote.

    Un lote que no pasa se reclama o se descarta; **nunca se siembra "a ver qué pasa"** ([06 §V1](../referencia/06-validacion-y-lazos-agenticos.md)).

## Plantilla de registro

`bitacora/semilla.csv` (el "registro de semilla" que liga `S001` con proveedor, lote y COA; mismo encabezado que la [guía](../guias/prueba-de-germinacion.md)):

```csv
lote_semilla,especie,proveedor,lote_proveedor,fecha_compra,coa,fecha_prueba,semillas_probadas,germinadas,pct_germinacion,decision,observaciones
S001,girasol,Mayoreo Online (CEDA),2026-08-B12,2026-09-14,no,2026-09-18,50,43,86,acepta,grado botanero; pedir sin tratamiento
S002,girasol,Al Natural,AN-2609-07,2026-09-14,no,2026-09-18,50,47,94,acepta,semilla especifica; brazo B del A/B
S004,girasol,Mayoreo Online (CEDA),2026-09-C03,2026-10-02,no,2026-10-06,50,39,78,rechaza,segundo kilo; reclamar; seguir con S002
```

- `decision`: `acepta` · `rechaza` · `reclama` · `acepta_opcion_B` (pasó sin tratar pero cayó con hipoclorito).
- Guarda el COA, si existe, en `bitacora/coa/Sxxx.pdf`.
- El `lote_semilla` es el que después aparece en cada `siembra_id` (`GIR-260921-S001-R1N5`): sin esta fila, el mock recall [V10](v10-mock-recall.md) no llega al proveedor.

## Si falla

| Resultado | Qué hacer |
|---|---|
| 70–84 % en girasol o chícharo | Reclamar al proveedor con la foto del conteo; **no** sembrar. Segundo kilo de otro costal y repetir V1. Con girasol: mientras tanto sembrar con Al Natural ($185/kg, sigue dejando 67–75 % de margen bruto, [Fase 0 · Siembra](../fases/fase-0/siembra.md)) |
| < 70 % | Descartar el lote; cambiar de proveedor para esa especie |
| Pasa la muestra sin tratar pero cae con hipoclorito (Opción A) | Ese lote se sanitiza con Opción B (H2O2 3 %) y se anota `acepta_opcion_B` ([Sanitizar semilla](../guias/sanitizar-semilla.md)) |
| Pasa V1 pero en charola germina mucho menos | El problema es tu proceso (riego, peso, temperatura), no la semilla: revisa densidad y riego con [V2](v02-rendimiento.md) antes de culpar al costal |
| Prueba hecha < 18 °C | Resultado inválido: repetir con tapete o cuarto cálido |

!!! warning "Errores típicos"
    - Tomar las 50 semillas de la superficie del costal (la semilla dañada se asienta).
    - Sellar la bolsa hermética o dejar secar la toalla un día.
    - Confiar en el porcentaje del costal anterior: cada costal es un lote.
    - Sembrar "porque urge" sin esperar el resultado.

## Al terminar

- [ ] Costal con código `Sxxx` y fila en `bitacora/semilla.csv` con proveedor, lote del proveedor, fecha, COA
- [ ] 50 semillas de distintas profundidades; temperatura 18–24 °C registrada
- [ ] Conteo al día 3–5 y `pct_germinacion` calculado
- [ ] `decision` escrita; si no pasó, reclamo o descarte hecho
- Registrar: la fila de `bitacora/semilla.csv` (plantilla arriba)
- Siguiente paso: [Sanitizar semilla](../guias/sanitizar-semilla.md) → [Sembrar una charola](../guias/sembrar-una-charola.md) → [V2 · Rendimiento](v02-rendimiento.md)

## Fuentes

- [06 · Validación §V1 y §L1](../referencia/06-validacion-y-lazos-agenticos.md): 50 semillas, 3–5 días, ≥ 85 % / ≥ 80 %, muestreo diario de 1 charola por lote.
- [08 · Recetas y economía unitaria](../referencia/08-recetas-y-economia-unitaria.md): girasol CEDA con prueba V1, chícharo solo con arvejón validado.
- [research/inocuidad-operativa §2 y §5](../research/inocuidad-operativa.md): prueba 200 vs 200 para hipoclorito, COA y lote del proveedor, registro de semilla.
- [Guía · Prueba de germinación](../guias/prueba-de-germinacion.md) y [Fase 0 · Siembra](../fases/fase-0/siembra.md): temperatura de la prueba, encabezado del CSV, calendario de S0.
