# Arranque real: el orden, y lo que hay que decidir antes de gastar

Esta página existe porque una auditoría de la wiki encontró que **no se puede ejecutar la
Fase 0 siguiendo el orden en que están escritas sus páginas**. No es que falte contenido —
sobra— sino que hay dependencias circulares, números que no coinciden entre páginas y
decisiones que el texto deja abiertas justo donde hay que actuar.

Aquí está el orden que sí funciona, las decisiones pendientes y las contradicciones
detectadas, cada una con la cita de las dos páginas que se contradicen para que puedas
resolverlas tú y cerrar el tema.

!!! danger "Lo primero: la página 1 no se puede ejecutar"
    [`fases/fase-0/compras.md`](../fases/fase-0/compras.md) pide como prerrequisito el
    *«sitio elegido y medido 3 días (montaje §1) — el rack se compra cuando ya sabes dónde va»*.

    [`fases/fase-0/montaje.md`](../fases/fase-0/montaje.md) pide como prerrequisito
    *«Comprar el equipo (compras.md)»*.

    **Cada página es prerrequisito de la otra.** La salida es separar la medición del sitio
    (§1 de montaje) del resto: medir es gratis, no necesita nada comprado y es justo lo que
    decide dónde va el rack. El orden real está abajo.

---

## 1. El orden que sí funciona

La Semana 1 **no** es la semana en que compras el rack. Es la semana de la primera siembra.
Antes hay una Semana 0 de mediciones que no cuesta nada y que condiciona todo lo demás.

| Cuándo | Qué | Depende de | Cuesta |
|---|---|---|---|
| **S0 · lunes** | **Llamar al contador**: ¿aparezco como socio o accionista de alguna persona moral? | Nada | $0 |
| **S0 · lun–mié** | **Medir el sitio 3 días**: luz a las 9, 13 y 17 h (meta 100–200 µmol/m²s), temperatura mín/máx (16–24 °C), agua a menos de 10 m, coladera que trague 10 L, piso plano | Nada. Teléfono con Photone y un termómetro mín/máx | $0 |
| **S0 · lun** | Llamar a Hydro Environment (55 5565-1153): tiempo de entrega a CDMX y existencia de rábano Champion en 500 g | Nada | $0 |
| **S0 · jue–vie** | **Comprar, en orden de tiempo de entrega**: primero lo de Hydro Environment (rábano + polvillo de coco, único proveedor fuera de CDMX), después CEDA, Al Natural, Home Depot y la ferretería | Sitio ya elegido | ~$8,800 |
| **S0 · el día que llega cada lote** | **Arrancar V1 de cada lote el mismo día que llega**: 50 semillas entre toalla, 3–5 días a 18–24 °C | Que llegue la semilla | $0 |
| **S0 · un día completo** | **Armar el rack** (1.5–2 h) y la estación de siembra y lavado (1 h) | Rack comprado, sitio medido, plástico para forrar | — |
| **S1 · lunes** | **Sembrar las 6 charolas del A/B de girasol** (3 CEDA + 3 Al Natural), 135 g secos cada una, posiciones alternadas. Es V2 y V6 al mismo tiempo | **V1 aprobada de los dos lotes** | — |
| **S1 · jueves** | Sembrar 3 charolas de rábano + 1 de amaranto | V1 del rábano aprobada | — |
| **S1–S2 · 2 h** | Mapear los 15 restaurantes, abrir `bitacora/prospectos.csv` | Nada | $0 |
| **S2 · jueves** | **Cosechar y pesar una por una** las 6 charolas del A/B. Decidir la semilla ganadora | Ciclo de 10 días cumplido | — |
| **S3 · mar–jue** | Ronda 1 de visitas, 8 restaurantes | **Producto cortado esa mañana** ⚠️ ver decisión 4 | — |
| **S4** | Ronda 2 y **primera entrega cobrada**. Es la semana 1 de recurrencia | Un pedido cerrado | — |
| **S4–S5** | En paralelo y gratis: pedir 3 cotizaciones de herrero y precios de PTR, malla, plástico y tinaco | Nada | $0 |
| **S5–S6** | Sostener entregas de martes y viernes; cerrar acuerdo de suministro con quien llegue a 3 semanas | Clientes de S4 repitiendo | — |
| **S6 · viernes** | Correr el gate y escribir la decisión | Bitácora conciliada | $0 |

!!! warning "La Semana 0 no cabe en una semana si haces las 6 acciones de «Antes de gastar un peso»"
    La acción 3 de esa página mide el consumo eléctrico durante **7 días corridos** y la 4 pide
    **3 mediciones de EC/pH en días distintos**. Ninguna de las dos bloquea la Fase 0: sirven
    para dimensionar la Fase 2. Córrelas en paralelo y no dejes que detengan la compra del rack.

    La única de las seis que **sí** puede frenar la primera venta cobrada de S4 es la pregunta
    al contador. Por eso está sola en el día 1.

---

## 2. Las decisiones que hay que tomar antes de gastar

Cada una está hoy abierta en la wiki. Ninguna se resuelve sola.

### Decisión 1 · Falta semilla de girasol: el calendario pide 2.8 kg y el BOM compra 2 kg

El calendario de 6 semanas siembra 21 charolas de girasol a 135 g = **2,835 g**. El BOM compra
1 kg de CEDA + 1 kg de Al Natural = **2,000 g**. Y es peor en la práctica: después del A/B solo
se siembra la ganadora, así que quedan ~595 g de esa bolsa para 15 charolas.

**Las dos salidas:**

- **(a)** Comprar el costal de 5 kg de CEDA ($140) desde el día 1 y asumir que si V1 reprueba se tira.
- **(b)** Recortar el calendario a las 14 charolas que alcanzan con 2 kg, y aceptar menos muestras.

**Recomendación:** (a). Son $140 contra el riesgo de quedarte sin producto ancla en la semana
que más importa. El girasol es 21 de las ~33 charolas del calendario.

### Decisión 2 · El gate no tiene una sola semana de holgura

El gate pide **2 clientes con 3 compras semanales consecutivas**, medido al cierre de S6. Los
primeros pedidos reales caen en S4. Quedan S4, S5 y S6: **tres semanas para un umbral de tres
semanas.** Cualquier cosa normal —un chef de vacaciones, un puente, una entrega rechazada, una
semana de moho— lo rompe.

**Decide ahora, por escrito, antes de la primera venta:** si la primera entrega cobrada cae en
S5, la fecha del gate se mueve a S7. Mover la *fecha* no es renegociar el *umbral*, y es
coherente con la regla de escribir los gates antes de gastar. Cuesta cero decidirlo hoy y es
imposible decidirlo sin hacer trampa cuando ya estés en S6.

### Decisión 3 · Las mismas 6 charolas no pueden ser medición y muestra

V2 exige cosechar las 3 charolas el mismo día y pesar **cada una completa**, sin sustrato ni
cáscaras. Las mismas 6 charolas del A/B son, según `ventas.md`, la fuente de las ~4 charolas de
muestra para los 15 restaurantes. No se puede pesar una charola completa y además repartirla.

**Hay que sembrar de más:** 3–4 charolas adicionales de girasol (~500 g), que se suman al
déficit de la decisión 1. Decide cuáles son de medición y cuáles de muestra **antes** de sembrar.

### Decisión 4 · La ronda 1 de visitas no tiene nada que cosechar esa mañana

El calendario cosecha **viernes y sábado** de S3. La ronda 1 de visitas es **martes a jueves** de
S3, y `ventas.md` exige muestra cortada esa mañana.

**Las dos salidas:**

- **(a)** Recorrer las siembras de S1 para que haya cosecha martes y jueves de S3.
- **(b)** Cambiar la regla a **«lleva la charola viva y corta delante del chef»**.

**Recomendación:** (b), y no solo porque sea más fácil: cortar delante del chef es mejor
argumento de venta que llegar con un clamshell. Pero hay que decirlo en `ventas.md`, que hoy
dice lo contrario.

### Decisión 5 · La decisión fiscal bloquea la primera venta cobrada

`ventas.md` dice: *«No emitas ninguna factura hasta resolver con contador desde qué RFC»*. La
primera venta cobrada tiene que caer en S4. Si la respuesta del contador tarda, no hay regla
escrita de qué hacer.

**Escribe la regla ahora:** en Fase 0 se vende con **remisión firmada y cobro por SPEI**, sin
factura, hasta que el contador responda. Si un cliente exige factura para pagar, ese cliente
espera. Un restaurante chico casi nunca la exige; un hotel siempre.

### Decisión 6 · Confirmar si Al Natural e Hydrocultura tienen mostrador

`compras.md` promete *«una sola mañana de recorrido en CDMX»*. No es una mañana: los proveedores
están en Tlalnepantla (norte), Central de Abasto (oriente) y Miguel Hidalgo (poniente).

Esto ya está resuelto en la página nueva de
[**Proveedores presenciales**](../referencia/proveedores-presenciales.md), con direcciones
verificadas y rutas en auto desde Coyoacán. El hallazgo más útil: **UNIT Electronics tiene
mostrador en Av. Copilco 357, Coyoacán** — el resto de la wiki lo trataba como proveedor solo
en línea.

---

## 3. Los números que no cuadran entre páginas

Todos estos son reales y están citados. Hasta que se resuelvan, **no uses ninguno para
comprometerte con un cliente ni para presupuestar.**

| Qué | Una página dice | Otra dice | Cuál usar |
|---|---|---|---|
| Inversión de Fase 0 | Plan maestro: $4,000–6,000 | BOM: ~$9,500 · `compras.md`: $9,100 | **$8,814**, ya corregido en el [BOM](../referencia/bom.md) |
| Ingreso bruto con 30 charolas/semana | Plan maestro: $8,000–11,000 | Doc 08: ~$16,900/mes | Ninguno: con 90 % de sell-through y 15 % de merma aterriza en **$13–14k**. Sin resolver |
| GFCI + tierra + electricista ($4,559) | Fase 1 lo exige en la S13 | Estaba presupuestado en el BOM de Fase 2 | **Corregido**: ahora vive una sola vez, en Fase 1 |
| PTR 1½" | BOM compraba 15 tramos | El modelo paramétrico calcula 11 | Sin resolver: correr el `.scad` y cerrar una cifra |
| PTR 1" | BOM compra 4 tramos | El modelo calcula 7 | Sin resolver: pueden faltar ~$825 |
| Escenario austero de Fase 0 | BOM: *«rábano/betabel 250 g»* | `compras.md`: *«250 g cuesta $1,000; 500 g cuestan $800»* | **500 g siempre.** Comprar menos sale más caro |
| Reloj de 30 días del gate G1→2 | El Gantt lo dibuja como 28 d | Termina **un día después** del hito del gate | Sin resolver |
| Ampliación del túnel 3×6 → 5×6 | Fase 2 dice que se cotiza aparte | No está costeada en ninguna parte | Sin resolver: el total del proyecto está subestimado ~10–15 % |

---

## 4. Los supuestos que hay que probar barato, antes de que sean caros

| Supuesto | Por qué es frágil | Cómo probarlo |
|---|---|---|
| **El girasol rinde 300–500 g por charola** | Ninguna fuente pública lo pesó: es estimado. Es el ancla de volumen de toda la fase | Ya está en el plan y es gratis: pesar una por una las 6 charolas del A/B. **No comprometas precio ni volumen con ningún chef hasta tener ese número** |
| **La conversión visitado → recurrente es 10–20 %** | 15 × 13 % = 2 clientes: el plan pasa el gate justo en el límite inferior de su propia expectativa | Ir a 3 restaurantes en S2 **sin muestra y sin hoja de precios**, y hacer solo una pregunta: *«¿qué usan hoy y cuánto les cuesta?»* |
| **El girasol de CEDA a $34/kg germina ≥ 80 %** | Es semilla grado botanero sin certificado. Si reprueba, el costo por charola salta de $9.10 a $29.50 | Es el propósito de V1. Lo que falta es no depender del resultado: comprar el kilo de CEDA en el primer viaje |
| **La charola viva «dura una semana en la cocina»** | **No verificado.** De esa frase cuelgan tres decisiones: que no hace falta cadena de frío, que los clamshells son solo para muestras, y que el rechazo es casi cero | Deja una charola viva en tu cocina desde la primera cosecha y fotografíala cada día una semana. Cuesta una charola |
| **10 charolas dobles alcanzan para muestrear 15 restaurantes y surtir 2 clientes** | S6 es la semana de menor cosecha (4 charolas) y es justo cuando dos clientes recurrentes necesitan 4–6 | Simula el calendario en una hoja **antes** de sembrar: las 33 charolas con su fecha de siembra y su ventana de cosecha. 30 minutos |

---

## 5. Lo que falta en el BOM y hay que comprar de todos modos

Estas cosas las piden las guías de montaje y ventas, y hasta ahora no estaban presupuestadas.
Casi todas son presenciales, lo cual conviene: se consiguen en la tlapalería del barrio, Home
Depot o el súper.

- Nivel de burbuja tipo torpedo (~$200) y flexómetro de 5 m
- Plástico grueso para forrar los 5 entrepaños de MDF (el MDF laminado se hincha)
- Calzas, masking y marcador indeleble
- Termómetro con mín/máx para la medición del sitio
- Cubetas de remojo y tina de lavado
- Hielera y gel packs para la ronda de visitas

A ojo son **$1,500–2,500** que hoy no están en ningún total.

---

## 6. Detalle menor pero que confunde

`gate.md` dice que el script de auditoría del gate *«se documenta cuando esté en el
repositorio»*. **Ya está**: es [`tools/gate_audit.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gate_audit.py),
funciona, y corrido contra `bitacora/ejemplo/` da GO con 2 clientes recurrentes y 61.8 % de margen.

Dos detalles al usarlo:

- El comando documentado **no lleva `--guardar`**, así que no escribe el informe que la propia
  página promete. Añádelo.
- El costo por defecto del girasol en el script es **$29.50** (Al Natural). Si el A/B lo gana
  CEDA, hay que pasar `--costo girasol=9.10` o el margen sale subestimado.
