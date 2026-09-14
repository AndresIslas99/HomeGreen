# Hueco 4 — Términos de pago y cobranza B2B con restaurantes + acuerdo de suministro simple

**Proyecto:** Huerto comercial automatizado (microgreens + hierbas NFT), patio 80 m², CDMX
**Fecha de investigación:** 12 de septiembre de 2026
**Por qué importa:** El plan asume vender = cobrar. En la práctica, los restaurantes mexicanos operan con crédito de proveedores (15–45 días) y la rotación/cierre de restaurantes es alta. Si las Fases 0–1 acumulan cartera vencida, no hay caja para financiar la Fase 2. Este informe define condiciones de pago por fase, la mecánica fiscal exacta (PUE/PPD/REP/RESICO-AGAPES), un machote de acuerdo de suministro de 1 página y un protocolo anti-morosos.

**Nota metodológica:** el buscador principal de la sesión se agotó; se trabajó con Brave Search vía fetch + apertura directa de fuentes. Las leyes (LISR, LIVA, CFF) se verificaron contra los PDF oficiales de la Cámara de Diputados descargados hoy. Lo no verificado de primera mano está marcado "aprox./por verificar".

---

### 1. Cómo pagan realmente los restaurantes (evidencia recopilada)

**Regla empírica del sector: nadie paga contra entrega por default.**

- **WSDA (Washington State Dept. of Agriculture), "Selling to Restaurants", Handbook for Small and Direct Marketing Farms 2019** (PDF abierto y leído completo): *"Most restaurants do not pay on delivery, and may pay monthly. It is important to keep track of deliveries and always be sure to get a signed invoice in duplicate... If an account is delinquent beyond the agreed upon terms, be cautious about continuing the relationship."* También: *"Farm may need good cash-flow management to sustain a delayed payment schedule"* y que los caterers de menú local hacen *"forward-contract agreements"* por volúmenes significativos a precio premium. URL: https://cms.agr.wa.gov/WSDAKentico/Documents/DO/RM/RM/16_SellingToRestaurants.pdf
- **UC ANR Small Farms Network, "Selling to Restaurants"** (snippet de búsqueda; la página bloqueó el acceso directo — por verificar): *"Two weeks, 30, 45 or 90 days is common"* como calendario de pago, y recomienda *"offer an incentive for early payment, such as a 3% discount for payment within 10 days."* URL: https://ucanr.edu/statewide-program/uc-anr-small-farms-network/selling-restaurants
- **PoloTab, "Finanzas para restaurantes 101: guía práctica México"** (abierta y leída): del lado del restaurante, el desfase típico que manejan es *"Apps: pago 7–15 días después vs proveedores a 7 días → desfase de caja"* — es decir, un proveedor chico de perecederos cobrando a 7 días es normal en su modelo financiero; recomiendan al restaurantero negociar *"precios fijos trimestrales o cláusula de ajuste inflacionario"* y proyectar flujo a 13 semanas. URL: https://www.polotab.com/blog/finanzas-para-restaurantes-101-guia-practica-2025-mexico
- **Blog Coppel, "Cómo abrir un restaurante en México"** (snippet, aprox.): los proveedores *"ofrecen crédito a 15 o 30 días una vez que estableces historial de pagos puntuales"* — el crédito se gana con historial, no se regala al arrancar. URL: https://www.coppel.com/blog/finanzas/como-abrir-un-restaurante-pasos-clave-para-emprender-ppc/
- **CANIRAC** (portal abierto): la cámara opera un **catálogo de proveedores** (https://portal.canirac.org.mx/catalogo-proveedores/) y programas de crédito para restauranteros (p. ej. Inbursa "Crédito Express Restaurantero", hasta 8× facturación mensual para afiliados CANIRAC: https://www.inbursa.com.mx/sites/gfi/credito-express-restaurantero). Lectura: el restaurante promedio vive apalancado; tu factura compite contra renta, nómina y banco.

**Benchmark CDMX — cómo cobran los microgreeners que ya operan:**
- **Mijardiin (CDMX zona centro, abierta hoy: https://www.mijardiin.mx/microgreens):** 18 variedades, porciones de 50–60 g a **$100–120 MXN por contenedor**, y —dato clave para este hueco— venden por **suscripción prepagada semanal/quincenal** ($260–560 por paquete, envío incluido, pedido por WhatsApp). Es decir: el jugador local establecido evita el crédito por completo cobrando por adelantado en modelo suscripción. Validación directa de la estrategia "contado primero" de la Fase 0.
- **Bidhara México** (brotes/microgreens para restaurantes y eventos: https://bidharamexico.com/tienda/brotes-microgreens — vista en resultados, no abierta) y **Moisaner** (mayoreo/menudeo CDMX desde 2021: https://moisaner.com/conocenos/ — bloqueó verificación bot): competidores CDMX activos; sus condiciones B2B exactas quedan por verificar en campo.
- En r/microgreens hay testimonios de US$700–1,000/mes por restaurante y discusiones de cobro (https://www.reddit.com/r/microgreens/comments/1ajw3md/pricing_for_restaurants/ — Reddit bloquea el fetch desde esta sesión; leer manualmente).

**Síntesis para un micro-proveedor de perecederos en CDMX:**
1. El estándar foodservice es crédito 15–45 días, pero es *negociable hacia abajo* cuando: (a) el producto es perecedero de entrega semanal, (b) el ticket es chico ($300–1,500/semana), (c) eres proveedor artesanal "con historia" que el chef quiere presumir. Los tickets chicos se pagan por caja chica o transferencia inmediata sin pasar por cuentas por pagar.
2. El peligro no es el plazo pactado sino el *plazo real*: la cuenta se paga "cuando cae el corte" y el proveedor chico es el último de la fila. De ahí la regla WSDA: remisión firmada en cada entrega + suspender a la primera factura vencida.
3. No hay datos públicos confiables específicos de morosidad foodservice MX (Atradius dejó de publicar barómetro México reciente accesible — ver brechas). Asume que 1 de cada 4–5 clientes te va a fallar un pago en el primer año y diseña el sistema para que eso duela poco.

---

### 2. Estrategia de cobro recomendada por fase

| Fase | Término de pago | Mecánica | CFDI |
|---|---|---|---|
| **Fase 0 (validación, sem. 1–6)** | **Contado estricto.** Transferencia SPEI al momento de la entrega o mismo día; efectivo aceptable con recibo | Muestra gratis la 1ª semana; desde el primer pedido real: "se entrega y se transfiere". Cero excepciones — estás validando que *pagan*, no solo que *quieren* | PUE, PagoEfectuado 03 (transferencia) o 01 (efectivo), al día |
| **Fase 1 (meses 2–4)** | **Cuenta semanal.** Corte viernes, pago lunes–martes (máx. 7 días naturales) | Una remisión firmada por entrega, una factura semanal que agrupa las entregas. Recordatorio automático lunes 9 am | PUE si pagan dentro del mismo mes; si el corte cruza de mes sin pago → PPD |
| **Fase 1 tardía / Fase 2** | **Crédito 15 días SOLO ganado**: cliente con 8+ semanas de pago puntual, y con tope | Tope de crédito = 2 semanas de pedidos (típico $2,000–4,000). Nunca 2 facturas abiertas a la vez. Opcional: 2–3 % descuento por pago a 7 días (práctica UC ANR) | PPD + complemento de pago (REP) obligatorio |
| **Cualquier fase — cadenas/hoteles/comisariatos** | 30 días solo si el ticket mensual > $8,000 y hay contrato firmado | Alta como proveedor formal, orden de compra, contrarrecibo | PPD + REP siempre |

**Reglas de oro (no negociables):**
- **Nunca crédito a un restaurante con menos de 6 meses operando.** La mortalidad de restaurantes nuevos es el escenario exacto en el que el proveedor chico pierde.
- **1 factura vencida > 7 días = la siguiente entrega es solo contado. 2 facturas vencidas = pausa total.** El producto perecedero no se puede "repossess"; el único apalancamiento real es la siguiente entrega (al chef le rompes el menú si faltas — úsalo con cortesía pero úsalo).
- **Ningún cliente > 25–30 % de tus ventas.** Con 4–5 clientes (gate de Fase 1→2), perder al peor pagador cuesta una semana de producto, no el mes.
- El descuento por pronto pago se ofrece como premio, nunca se anuncia como precio de lista con recargo por crédito.
- Todo pago por SPEI a cuenta de negocio; el efectivo solo en Fase 0 y con recibo foliado. El historial bancario ES tu score para créditos futuros y tu evidencia si hay pleito.

---

### 3. Mecánica fiscal exacta (verificada contra ley y RMF 2026)

#### 3.1 PUE vs PPD y el complemento de pago (REP)

- **PUE** ("Pago en una sola exhibición"): cuando te pagan al facturar **o dentro del mismo mes de emisión**. No requiere nada más. Fuente: SenHub (https://senhub.mx/blog/que-es-complemento-de-pago) y Grupo CerVel (https://grupocervel.com/blog/complemento-de-pago), ambos abiertos y leídos.
- **PPD** ("Pago en parcialidades o diferido"): cualquier venta a crédito cuyo pago no cae en el mes de emisión. Obliga a emitir después un **CFDI con complemento de recepción de pagos (REP)** por cada cobro (fundamento: art. 29-A CFF).
- **Plazo del REP (RMF 2026, regla 2.7.1.32, publicada en DOF el 28-dic-2025):** *"a más tardar el quinto día natural del mes inmediato siguiente"* al mes en que recibiste el pago. Días naturales, no hábiles. **No hay prórroga vigente en 2026** (verificado en Tesio: https://tesio.com.mx/blog/prorroga-complemento-pago-2026/ y Grupo CerVel). Ejemplo: te pagan el 29 de agosto → REP a más tardar el 5 de septiembre.
- **Facilidad práctica:** puedes emitir **un solo REP mensual por cliente** agrupando todos sus pagos del mes (confirmado en Grupo CerVel). Para 5 clientes = 5 REP el día 1–5 de cada mes; media hora de trabajo.
- **Multa por no emitir REP** (art. 83 fracc. VII CFF, montos actualizados dic-2025, según Grupo CerVel): **$22,300 a $127,530 MXN por comprobante**; reincidencia puede llevar a clausura preventiva de 3 a 15 días. Una multa de estas se come 2–3 meses de utilidad del huerto: el REP no es opcional.
- **Trampa clásica a evitar:** facturar PUE "por comodidad" y que el restaurante pague el mes siguiente. El SAT detecta el descalce (la factura PUE sin pago bancario correlacionado) y manda cartas invitación. Si diste crédito que cruza de mes: PPD desde el inicio.

#### 3.2 RESICO AGAPES: el ISR se causa sobre lo COBRADO (verificado en el texto de ley)

Verificado directamente en el PDF oficial de la LISR (Cámara de Diputados, última reforma DOF 01-04-2024, descargado hoy: https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf):

- **Microgreens y hierbas frescas SON actividad agrícola:** CFF art. 16 fracc. III (PDF oficial https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf): *"Las agrícolas que comprenden las actividades de siembra, cultivo, cosecha y la primera enajenación de los productos obtenidos, que no hayan sido objeto de transformación industrial."* Cortar, lavar y empacar en fresco no es transformación industrial; deshidratar, marinar o procesar sí lo sería (y rompería tanto AGAPES como la tasa 0 % de IVA).
- **Exención de 900 mil (art. 113-E, noveno párrafo LISR, citado textual):** *"Las personas físicas que se dediquen exclusivamente a las actividades agrícolas, ganaderas, silvícolas o pesqueras, cuyos ingresos en el ejercicio no excedan de novecientos mil pesos efectivamente cobrados, no pagarán el impuesto sobre la renta por los ingresos provenientes de dichas actividades."* "Exclusivamente" = 100 % de los ingresos por esas actividades (párrafo décimo).
- **Flujo de efectivo:** en RESICO el pago mensual se calcula sobre ingresos *"amparados por los comprobantes fiscales digitales por Internet **efectivamente cobrados**"* (art. 113-E, quinto párrafo). **Consecuencia directa para la cobranza: una factura PPD emitida y no cobrada NO causa ISR.** El impuesto (si lo hubiera) nace cuando entra el dinero — coherencia perfecta con vender a crédito, pero también significa que la factura emitida no es "ingreso": hasta no cobrar, no hay negocio.
- **Tasas si algún día excedes 900k:** tabla mensual 1.00 % (hasta $25,000/mes) a 2.50 % (tope $3.5 M anuales). Con los números del plan ($14–21k/mes bruto = $170–250k/año) estás holgadamente debajo de 900k: **ISR $0** en régimen AGAPES. Fuentes secundarias (ResicoCalc, abierta: https://resicocalc.com/blog/resico-para-agapes-actividades-primarias) indican que al exceder se paga **solo sobre el excedente** y que puede optarse por **no presentar declaraciones mensuales ni anual** mientras no rebases 900k (facilidad reportada también por dPoder/Firmas.mx; regla exacta por verificar con contador).
- **Retención del 1.25 % (art. 113-J LISR, citado textual):** cuando un RESICO PF vende a **personas morales** (la mayoría de restaurantes formales son S.A. de C.V. / S. de R.L.), éstas *"deberán retener... 1.25 % sobre el monto de los pagos"*. **PERO hay excepción para AGAPES exentos:** si el CFDI lleva en la descripción la leyenda *"Los ingresos que ampara este comprobante se encuentran en el supuesto de exención a que se refiere el artículo 113-E, noveno párrafo"*, la persona moral NO retiene (regla 3.13.33 RMF 2022 según IDC Online, abierta: https://idconline.mx/fiscal-contable/2022/04/26/excepcion-de-retencion-a-resicos-pf-agapes; renumerada como 3.13.26 en RMF 2026 según ResicoCalc — **verificar número de regla vigente con contador**). Práctico: configura la leyenda como texto fijo en tu plantilla de facturación.
- **IVA tasa 0 %:** LIVA art. 2o.-A fracc. I inciso a) (PDF oficial https://www.diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf, citado textual): tasa 0 % a la enajenación de *"animales y vegetales que no estén industrializados"*. Tus facturas van con IVA 0 % — el restaurante no paga IVA por tu producto (argumento de venta menor pero real vs. distribuidores de mezclas procesadas al 16 %). Nota de coyuntura: en septiembre 2026 circula una propuesta de "IVA de 7 % para RESICO" (El Contribuyente, 10-sep-2026: https://www.elcontribuyente.mx/2026/09/iva-de-7-para-resico-que-significa-realmente-la-propuesta-del-sat/) — es propuesta del Paquete 2027, no ley; vigilar.

#### 3.3 ⚠️ ADVERTENCIA CRÍTICA detectada en el texto de ley (afecta al plan)

El art. 113-E LISR **excluye de RESICO** a quienes *"sean socios, accionistas o integrantes de personas morales o cuando sean partes relacionadas en los términos del artículo 90"* (fracc. I, citado textual del PDF oficial). El plan dice *"tus empresas ya te dan la infraestructura fiscal"*: **si el dueño del huerto es socio/accionista de sus empresas, NO puede tributar como RESICO persona física** (hay excepciones puntuales vía RMF para socios de personas morales no lucrativas — no aplican al caso típico). Opciones a evaluar CON CONTADOR antes de emitir la primera factura:
1. Facturar las ventas del huerto **desde una de las empresas existentes** (persona moral): pierde la exención AGAPES de 900k y el 0 % de ISR, pero simplifica; la PM paga ISR corporativo sobre utilidad (con deducciones reales del huerto). IVA sigue al 0 % por ser vegetales no industrializados.
2. Que el huerto lo opere y facture **otra persona física del hogar** que NO sea socia de nada (cónyuge, familiar) en RESICO-AGAPES: conserva exención 900k + sin retención 1.25 % + sin declaraciones. Es la vía fiscalmente óptima si es real (la operación debe ser genuina de esa persona).
3. Persona física con actividad empresarial régimen general (sección I): sin límite de socios, ISR sobre utilidad con deducciones; sector primario tiene facilidades administrativas propias. Más carga administrativa.

Esta decisión cambia la mecánica de facturación de TODO el proyecto y debe resolverse en Fase 0.

---

### 4. Acuerdo simple de suministro semanal — machote de 1 página

**Punto de partida real:** el formato genérico gratuito de milformatos (Word descargable: https://milformatos.com/contratos/contrato-de-suministro/) sirve de esqueleto legal mexicano pero **le faltan** cláusulas de plazo de pago, rechazo de producto y terminación (verificado abriendo la página). La estructura de abajo integra las prácticas WSDA ("fresh sheet" semanal, remisión firmada, forward agreements) y UC ANR (descuento por pronto pago) adaptadas a México. No es asesoría legal; para tickets de $300–1,500/semana el objetivo es un documento de UNA página que el administrador firme sin mandarlo al abogado.

**ACUERDO DE SUMINISTRO SEMANAL — [MARCA DEL HUERTO]**

> **1. Partes.** [Nombre/razón social del productor], RFC ___ ("el Productor") y [razón social del restaurante], RFC ___, representado por [administrador/dueño] ("el Cliente"). *(Firmar con administrador o dueño, NUNCA solo con el chef — el plan ya identifica la rotación de chefs como riesgo #4.)*
> **2. Producto y pedido.** El Productor envía lista de disponibilidad ("fresh sheet") cada [domingo 18:00] por WhatsApp/correo. El Cliente confirma pedido a más tardar [lunes 12:00]. Pedido mínimo semanal: $[400] MXN. Variaciones de ±20 % sobre el pedido confirmado no requieren renegociación.
> **3. Entrega.** [Martes y/o jueves, 9:00–12:00] en [dirección]. Producto cosechado el mismo día o charola viva. Cada entrega se acompaña de remisión en duplicado firmada por quien recibe.
> **4. Aceptación y rechazo.** El Cliente inspecciona AL MOMENTO de la entrega. Producto rechazado con causa (calidad, error de pedido) se repone en máx. 24 h o se descuenta de la factura semanal, a elección del Cliente. **No se aceptan rechazos ni devoluciones posteriores a la recepción firmada** (producto vivo/perecedero).
> **5. Precio.** Según lista anexa. Revisión trimestral; ajustes con aviso de 14 días naturales. *(Alternativa: ajuste semestral por INPC.)*
> **6. Pago.** Factura semanal (corte [viernes]); pago por transferencia SPEI a más tardar [7] días naturales tras la factura, a la cuenta CLABE ___. Pago a 7 días o menos: descuento de [2] %. Factura vencida: las entregas siguientes se realizan contra pago inmediato hasta regularizar; interés moratorio pactado del [3–5] % mensual sobre saldos vencidos.
> **7. Facturación.** CFDI 4.0 con IVA 0 % (vegetales no industrializados). [Si RESICO-AGAPES: la factura incluye la leyenda de exención del art. 113-E noveno párrafo y NO procede retención de ISR del 1.25 %.]
> **8. Vigencia.** Indefinida; cualquiera de las partes puede terminar con aviso de 14 días. Sin exclusividad para ninguna de las partes.
>
> Firmas: ____________ / ____________ Fecha: ______

**Notas de uso:**
- La cláusula 4 es la que más pleitos evita: en perecederos el rechazo *solo en recepción* es estándar (práctica implícita en WSDA: la remisión firmada es la prueba de aceptación).
- La cláusula 6 encapsula toda la política de cobranza: crédito corto explícito + suspensión automática + moratorios pactados (los moratorios pactados por escrito son exigibles; sin pacto, el Código de Comercio supletorio da 6 % ANUAL — irrisorio).
- Para adeudos ya generados > $5,000, convertir a **pagaré** (formato gratuito Word/PDF: https://milformatos.com/empresas-y-negocios/el-pagare/): es título ejecutivo (Ley General de Títulos y Operaciones de Crédito) y permite juicio ejecutivo mercantil directo, sin discutir primero la existencia de la deuda. El formato sugiere moratorios de 5 % mensual como práctica común.
- El acuerdo NO garantiza volumen anual ni obliga al restaurante a comprar: su función es fijar reglas de juego (día de pedido, rechazo, plazo de pago) y darte papel firmado si hay impago. Un "forward contract" duro es contraproducente en esta escala.

---

### 5. Señales de alerta de restaurantes que no van a pagar + tácticas para cortar pérdidas

**Señales de alerta (ordenadas por gravedad):**
1. **Pide más volumen Y más plazo a la vez.** El clásico previo al quiebre: te usan de financiamiento gratis. Volumen sube solo con historial de pago intacto.
2. **Pagos parciales sin acuerdo** ("te deposito la mitad y la otra la próxima semana") o pagos en efectivo cuando siempre fueron por SPEI (señal de cuenta bancaria con problemas/embargos).
3. **Cambia la razón social a la que piden facturar** a mitad de la relación (RFC nuevo, S.A. recién constituida): patrón típico de insolvencia — dejan deudas en la sociedad vieja.
4. **Rotación del administrador o del dueño operativo** (no solo del chef): tu acuerdo lo firmó alguien que ya no está; re-valida el acuerdo en la primera semana del reemplazo.
5. **Nómina o renta atrasadas** (los meseros lo cuentan todo si preguntas con tacto en la entrega), proveedores grandes que ya solo les venden de contado, camioneta del gas que no les surte.
6. **Caída visible de operación:** menú recortado, horario reducido, reseñas recientes desplomándose, salón vacío en horas pico. Entregas semanales = inspección semanal gratuita; entrena al repartidor (tú) a mirar.
7. **Restaurante con < 6 meses de vida** que pide crédito de entrada. El contexto 2026 de contracción del sector en CDMX (documentado en el research de puntos ciegos) hace esto más letal: el crédito se gana, no se pide.
8. **"El de pagos no vino"** dos semanas seguidas. Una vez es normal; dos es política de la casa.

**Protocolo de cobranza escalonado (micro-proveedor, sin abogados hasta el final):**

| Día desde vencimiento | Acción |
|---|---|
| 0 (día de pago) | Recordatorio amable por WhatsApp con la factura adjunta y CLABE (automatizable) |
| +3 | Llamada/mensaje directo al administrador: "¿hubo algún problema con la factura X?" |
| +7 | **Suspensión automática de crédito**: próxima entrega solo contra pago inmediato (incluir el vencido). Se avisa sin drama: "política de la casa" |
| +14 | Pausa total de entregas. Ofrecer convenio: pagaré firmado con fecha cierta por el saldo (formato milformatos) |
| +30 | Carta de cobranza formal (correo con acuse) citando facturas y moratorios pactados. Para montos < $10k, el costo real de juicio no se justifica: el pagaré + presión de suspensión es el mecanismo práctico |
| +45 | Cortar pérdidas: se asume incobrable, se documenta (sirve como cancelación/nota de crédito para no cargar el CFDI en cartera eternamente). En RESICO no pagaste ISR por no haber cobrado — la pérdida es el costo variable del producto (~30 %), no el precio de venta |

**Marco legal mexicano del cobro (fuentes abiertas y leídas hoy):**
- **UPLAW (despacho MX), "¿Qué puede hacer una PYME cuando sus clientes no le pagan?"** (https://www.uplaw.com.mx/post/qué-puede-hacer-una-pyme-cuando-sus-clientes-no-le-pagan): secuencia recomendada = prevención (verificar solvencia, contrato firmado, anticipos, política de crédito) → extrajudicial (carta de requerimiento con monto y plazo; convenio de reconocimiento de adeudo; **suspensión del servicio si el contrato lo permite** — por eso la cláusula 6 del machote la pacta expresamente) → judicial. **Juicio ejecutivo mercantil** (rápido) exige título ejecutivo: *"pagaré, letra de cambio o cheque"*; sin título, queda el **juicio ordinario mercantil** probando la entrega. La prescripción mercantil general es de 10 años, pero cobrar en los primeros meses es lo que funciona.
- **Expansión, "¿Qué hacer si no me pagan una factura?" (29-nov-2024)** (https://expansion.mx/finanzas-personales/2024/11/29/que-hacer-si-no-me-pagan-una-factura): la vía ordinaria mercantil permite demandar con la **factura aceptada por el cliente** como prueba fundamental (la "firma de aceptación" — exactamente la remisión/factura firmada que exige este protocolo); requerimiento previo sin necesidad de notario si tienes esa firma; el juicio puede tardar *"desde meses hasta años"* si el deudor contesta. Conclusión práctica para tickets de $1,000–5,000: la vía judicial es disuasión, no plan de cobro — el plan de cobro es suspensión + pagaré + tope de exposición.

**Principios de diseño del sistema (para que un impago nunca duela):**
- **Exposición máxima por cliente = 2 semanas de producto.** Con tickets de $400–1,500/semana, tu peor escenario por cliente es $800–3,000: molesto, no mortal. Compara: costo variable real de ese producto ≈ $250–1,000.
- **El apalancamiento del proveedor de perecederos es la continuidad, no la amenaza legal.** Al chef le rompes el mise en place si no llegas el martes. La suspensión cortés e inmediata cobra más facturas que cualquier abogado.
- **Remisión firmada SIEMPRE** (WSDA: *"always be sure to get a signed invoice in duplicate"*). Sin firma de recepción no hay deuda demostrable.
- **La factura CFDI no es prueba de adeudo por sí sola** en juicio mercantil; remisión firmada + acuerdo firmado + estados de cuenta sí arman el caso. El pagaré lo vuelve trivial (vía ejecutiva).
- Cliente recuperado que volvió a pagar puntual 8 semanas: puede volver a crédito, con tope reducido a la mitad. Cliente que quebró debiendo: la deuda de la S.A. quebrada casi nunca se recupera — por eso el tope de exposición es la única defensa real.

---

### Tabla de proveedores / recursos

| Nombre | Qué es / para qué | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Milformatos — Contrato de suministro | Machote Word gratis, base legal MX para el acuerdo de 1 página | $0 | https://milformatos.com/contratos/contrato-de-suministro/ | Verificado hoy: descarga gratis; le faltan cláusulas de pago/rechazo — usar estructura de la sección 4 |
| Milformatos — Pagaré | Formato pagaré Word/PDF gratis (título ejecutivo, LGTOC) | $0 | https://milformatos.com/empresas-y-negocios/el-pagare/ | Verificado hoy; sugiere moratorios 5 % mensual como práctica |
| WSDA — Selling to Restaurants (fact sheet 16) | Guía gratuita farm-to-restaurant: fresh sheet, remisiones, pagos | $0 | https://cms.agr.wa.gov/WSDAKentico/Documents/DO/RM/RM/16_SellingToRestaurants.pdf | PDF abierto y leído completo hoy |
| UC ANR Small Farms — Selling to Restaurants | Guía extensión universitaria: plazos comunes, descuento pronto pago | $0 | https://ucanr.edu/statewide-program/uc-anr-small-farms-network/selling-restaurants | Bloqueó bot (403); citada por snippet — verificar manualmente |
| Curtis Stone — The Urban Farmer (libro + sitio) | Modelo de negocio urban farm → restaurantes; cursos de microgreens | Libro ~$400–600 aprox. (no verificado) | https://theurbanfarmer.co/book/ y https://microgreenswebclass.com/tuf | Sitio verificado hoy; el libro cubre "market development"; detalles de facturación no visibles en la página |
| CANIRAC — Catálogo de proveedores | Registrarse como proveedor ante la cámara restaurantera | Por verificar | https://portal.canirac.org.mx/catalogo-proveedores/ | Portal verificado hoy; costo/proceso de alta no publicado en portada |
| Grupo CerVel — guía REP | Referencia PUE/PPD/REP, plazos y multas 2026 | $0 | https://grupocervel.com/blog/complemento-de-pago | Abierta y leída hoy; fuente de multas $22,300–$127,530 |
| Tesio — prórroga complemento de pago 2026 | Confirma regla 2.7.1.32 RMF 2026 (DOF 28-dic-2025), sin prórroga | $0 | https://tesio.com.mx/blog/prorroga-complemento-pago-2026/ | Abierta y leída hoy |
| SenHub — qué es complemento de pago | Referencia PUE mismo mes vs PPD | $0 | https://senhub.mx/blog/que-es-complemento-de-pago | Abierta y leída hoy |
| IDC Online — excepción retención AGAPES | Leyenda CFDI para evitar retención 1.25 % | $0 (artículo) | https://idconline.mx/fiscal-contable/2022/04/26/excepcion-de-retencion-a-resicos-pf-agapes | Abierta hoy; regla 3.13.33 RMF 2022 — número vigente 2026 por confirmar |
| ResicoCalc — RESICO para AGAPES | Explicación 2026: exención 900k, excedente, leyenda, declaraciones | $0 | https://resicocalc.com/blog/resico-para-agapes-actividades-primarias | Abierta y leída hoy |
| LISR / LIVA / CFF (Cámara de Diputados) | Textos legales oficiales (arts. 113-E, 113-J, 2-A LIVA, 16 CFF) | $0 | https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf · /LIVA.pdf · /CFF.pdf | PDFs descargados y citados textualmente hoy |
| PoloTab — Finanzas para restaurantes 101 | Cómo ve el flujo de caja tu cliente (desfases, 13 semanas) | $0 | https://www.polotab.com/blog/finanzas-para-restaurantes-101-guia-practica-2025-mexico | Abierta y leída hoy |
| UPLAW — PYME con clientes que no pagan | Ruta legal MX: extrajudicial → ejecutivo/ordinario mercantil | $0 (artículo) | https://www.uplaw.com.mx/post/qué-puede-hacer-una-pyme-cuando-sus-clientes-no-le-pagan | Abierta y leída hoy |
| Expansión — qué hacer si no pagan una factura | Vía ordinaria mercantil, factura firmada como prueba | $0 | https://expansion.mx/finanzas-personales/2024/11/29/que-hacer-si-no-me-pagan-una-factura | Abierta y leída hoy |
| Inbursa — Crédito Express Restaurantero | Contexto: financiamiento de tus clientes (afiliados CANIRAC) | n/a | https://www.inbursa.com.mx/sites/gfi/credito-express-restaurantero | Visto en resultados de búsqueda (no abierto) |
| El Contribuyente — propuesta IVA 7 % RESICO | Vigilancia regulatoria Paquete 2027 | $0 | https://www.elcontribuyente.mx/2026/09/iva-de-7-para-resico-que-significa-realmente-la-propuesta-del-sat/ | URL vista en el propio sitio (10-sep-2026); artículo no abierto |
| Mijardiin — microgreens CDMX (benchmark) | Competidor CDMX zona centro; modelo de suscripción prepagada | $100–120/contenedor 50–60 g; paquetes $260–560 | https://www.mijardiin.mx/microgreens | Abierta y leída hoy; precios de su página |
| Bidhara México — brotes/microgreens | Competidor B2B (restaurantes/eventos) | Por verificar | https://bidharamexico.com/tienda/brotes-microgreens | Vista en resultados de búsqueda, no abierta |
| Moisaner — microgreens mayoreo CDMX | Competidor mayoreo/menudeo CDMX desde 2021 | Por verificar | https://moisaner.com/conocenos/ | Bloqueó verificación bot al abrir |

---

### Recomendación concreta (qué hacer exactamente)

1. **Antes de la primera factura (Fase 0, esta semana):** sesión de 1 hora con contador para resolver la ADVERTENCIA 3.3: si eres socio/accionista de tus empresas, RESICO-PF está vetado (art. 113-E fracc. I). Decide entre facturar vía persona moral existente o vía otra persona física del hogar en RESICO-AGAPES (óptimo fiscal: ISR $0 hasta 900k cobrados, sin retención 1.25 % con leyenda, IVA 0 %, opción sin declaraciones). No factures nada hasta decidir esto.
2. **Política de pago por fase (imprimir en la hoja de precios):** Fase 0 = SPEI contra entrega. Fase 1 = factura semanal, pago a 7 días. Crédito a 15 días solo tras 8 semanas puntuales y con tope de 2 semanas de pedidos. 30 días solo para cadenas/hoteles con contrato. La hoja de precios debe decir "Precios con IVA 0 % — producto agrícola fresco".
3. **Facturación operativa:** CFDI PUE para todo lo que se cobra dentro del mes; PPD para cualquier crédito que cruce de mes; REP mensual agrupado por cliente los días 1–5 de cada mes, sin excepción (multa mínima $22,300 vs 30 min de trabajo). Plantilla de CFDI con leyenda de exención 113-E si aplica RESICO-AGAPES.
4. **Documento de venta:** usar el machote de 1 página de la sección 4 (adaptado del formato milformatos + prácticas WSDA/UC ANR). Firmarlo con administrador/dueño en cuanto un cliente pase de 3 semanas comprando (gate de Fase 0). Remisión firmada en duplicado en CADA entrega desde el día 1 — cuesta $0 y es la diferencia entre deuda cobrable e incobrable.
5. **Sistema anti-moroso (configurar una vez):** recordatorio automático de pago (WhatsApp) al vencimiento; regla mecánica 7/14/45 (contado→pausa→incobrable); exposición máx. 2 semanas por cliente; pagaré para cualquier adeudo > $5,000; observación del local en cada entrega. Meta: que el peor impago posible cueste < $3,000 (≈ una semana de un cliente grande), que el flujo de Fase 1 nunca dependa de cartera > 15 días, y que la caja para Fase 2 se construya sobre lo COBRADO, no sobre lo facturado.

---

### Brechas / pendientes de verificación humana

- **Dato duro de morosidad B2B México:** el Barómetro de Prácticas de Pago de Atradius para México no fue localizable en atradius.com.mx ni group.atradius.com (solo reportes Asia/EAU 2026). Buscar manualmente el último reporte "USMCA/México" para anclar el % de facturas vencidas.
- **UC ANR:** la página bloqueó el fetch (403); la cita "Two weeks, 30, 45 or 90 days is common" y el descuento 3 %/10 días provienen del snippet de búsqueda.
- **Número de regla RMF 2026 de la excepción de retención 1.25 % AGAPES** (¿3.13.26?) y de la facilidad de no presentar declaraciones < 900k: confirmar con contador contra el texto de la RMF 2026 publicada en DOF 28-dic-2025.
- **Si el titular es socio/accionista:** confirmar con contador la exclusión de RESICO y la mejor alternativa (la sección 3.3 esboza opciones, no es asesoría fiscal).
- **CANIRAC catálogo de proveedores:** costo y proceso de alta como proveedor no publicados en portada; contactar a la cámara.
- **Curtis Stone:** los detalles finos de su ciclo de pedidos/facturación a chefs están en el libro (no visibles online); el precio del libro no se verificó.
- **Interés moratorio pactado:** el tope práctico/usura en la jurisprudencia mexicana (para no pactar un % anulable) merece 10 minutos de un abogado; el 3–5 % mensual del machote es práctica común según milformatos, no norma.
- **Propuesta IVA 7 % RESICO (Paquete 2027):** seguirla; si prosperara podría tocar la facturación aunque el producto agrícola hoy esté a 0 %.
- **Testimonios directos de productores MX:** Reddit (r/microgreens) es inaccesible desde esta sesión y los foros mexicanos no aparecieron en los buscadores disponibles; la mejor verificación es de campo — preguntar condiciones de pago a Moisaner/Bidhara como cliente incógnito y a 2–3 chefs de la lista de Fase 0.
- **Condiciones B2B de competidores CDMX (Moisaner, Bidhara):** no publicadas / bloqueadas al fetch; verificar por WhatsApp.
