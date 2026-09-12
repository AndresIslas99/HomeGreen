# Puntos ciegos del plan — Huerto comercial automatizado (80 m², CDMX)

**Fecha de investigación: 12 de septiembre de 2026.** Precios en MXN a esta fecha; los marcados "aprox." vienen de fuentes no verificadas al 100% o son estimaciones propias señaladas como tales.

**Veredicto en una línea:** el plan es sólido en lo técnico y lo comercial-básico, pero subestima 4 cosas que sí matan proyectos así: (1) el riesgo de caer en tarifa DAC de CFE por la bomba NFT sobredimensionada, (2) el tiempo real de operación (15 h/sem, no 6–9), (3) la fragilidad del mercado restaurantero 2026 (CANIRAC confirma contracción) y (4) la cadena de frío del producto cortado (a 20–25 °C el microgreen cortado muere en <1 día).

---

## (a) Electricidad: consumo real, tarifa CFE y riesgo DAC

### El dato que cambia el diseño: límite DAC = 250 kWh/mes

CDMX es **tarifa 1** (doméstica). Confirmado en la página oficial de CFE y en 3 medios (sep-2026): si tu **promedio móvil de 12 meses** supera **250 kWh/mes**, CFE te reclasifica automáticamente a **DAC (Doméstica de Alto Consumo)** y pierdes todo el subsidio.

Números confirmados 2026:

| Concepto | Valor | Fuente |
|---|---|---|
| Límite DAC tarifa 1 | 250 kWh/mes (promedio 12 meses) | CFE oficial + MiBolsillo + Debate |
| Tarifa 1, consumo básico | ≈ $1.125/kWh (jun-2026) | MiBolsillo |
| DAC cargo fijo | $145.04/mes (ago-2026); $142.41 (may-2026) | MiBolsillo / Infobae |
| DAC energía | $6.05–7.02/kWh; **región Central ≈ $6.63/kWh** | MiBolsillo |
| Ejemplo: 300 kWh en DAC región Central | ≈ **$2,134 + IVA y DAP** (~$2,500) | MiBolsillo |
| Mismo consumo en tarifa 1 subsidiada | ~$500–700 aprox. | estimación con bloques |

Es decir: caer en DAC multiplica el recibo **hasta 5×** (Infobae). Y como es promedio móvil anual, **un solo año de bomba mal elegida te encarcela en DAC durante meses** aunque después bajes el consumo.

### Consumo real del sistema (cálculo propio, potencias típicas)

**Fase 1 (microgreens, sin lámparas — como está el plan):**

| Equipo | Potencia | Uso | kWh/mes |
|---|---|---|---|
| Raspberry Pi + router + 2 ESP32 | ~10 W | 24/7 | 7.2 |
| Bomba 12V nebulización | 20 W | 15 min/día | 0.2 |
| Ventilador | 25 W | 8 h/día | 6 |
| **Total Fase 1** | | | **~13 kWh/mes ≈ $15–35** |

Fase 1 es eléctricamente trivial. El problema es la Fase 2.

**Fase 2 (NFT) — aquí está el error del plan.** El plan especifica "bomba periférica 0.5 HP". Una periférica de 0.5 HP consume ~370–450 W reales. NFT requiere flujo continuo o casi continuo:

| Escenario bomba NFT | kWh/mes | Consecuencia |
|---|---|---|
| Periférica 0.5 HP, 24/7 | **~324** | **DAC ella solita**, recibo ~$2,600/mes |
| Periférica 0.5 HP, 12 h/día | ~162 | + consumo del hogar (100–170 típico) → DAC casi seguro |
| **Bomba correcta: sumergible/magnética 35–60 W, 24/7** | **~32** | Sin drama |

Para 6–8 líneas NFT de 4" con <2 m de columna de agua, una bomba de fuente/acuario de 45–60 W (3,000–4,500 L/h) sobra. **La periférica de 0.5 HP está sobredimensionada ~8× y es el punto ciego más caro del plan: la diferencia son ~$1,600–2,000/mes de recibo si te manda a DAC — 15–20% del neto proyectado de $8–13.5k.**

Consumo Fase 2 bien diseñada: bomba 45 W (32) + Pi/nodos (7) + ventilación 2×25 W 12 h (18) + germinación 4 tubos LED 18 W × 14 h (30) ≈ **85–90 kWh/mes** adicionales al hogar. Con un hogar de 150+ kWh/mes ya estás rozando 250. **Acciones: medir el consumo base del hogar HOY (medidor Steren HER-432, $336–399) y monitorear kWh acumulado en Home Assistant con alarma en 220 kWh/mes.** Si el negocio crece con LEDs, la salida limpia es contratar un **servicio PDBT (negocio) separado con CFE**: sin subsidio (~$4–5.5/kWh aprox., no verificado) pero sin castigo DAC y deducible.

### ¿UPS para la bomba NFT? Sí, pero no un UPS de PC

Realidad física: en NFT las raíces cuelgan en una película de agua; sin flujo, en clima templado hay estrés en 1–2 h y daño serio en 4+ h (la reserva es solo lo que queda en canal y charola). Un corte nocturno de 6 h sin respaldo puede costarte las 6–8 líneas (~2–4 semanas de ingreso de hierbas).

Los números de respaldo:

| Opción | Costo | Autonomía real con bomba | Veredicto |
|---|---|---|---|
| UPS 1000 VA/500–600 W (Forza NT-1011 $939, APC BV1000 $1,689 en Cyberpuerta) | $939–1,689 | Con bomba 450 W: **4–8 min**. Con bomba 45 W: ~45–90 min | Insuficiente para >2 h |
| Steren NB-1500 (1,500 VA, "hasta 90 min") | $2,436 | Con 60 W (bomba chica + Pi): ~60–90 min | Marginal |
| **Bomba 12V DC 25–40 W + batería Steren BR-1224 24 Ah ($1,044) + cargador flotante BR-700** | **~$2,000–2,500 total** | 230 Wh útiles → **6–8 h**; con 2 baterías **12–15 h** | **La solución correcta** |
| Mini-UPS Steren NB-060 8,000 mAh para módem/Pi | $529 | Pi + router: 2–4 h | Complemento para no perder telemetría/alarmas |

**Recomendación:** diseñar el circuito hidráulico en 12 V DC desde el inicio (bomba principal DC de bajo consumo, o bomba AC + bomba DC de emergencia con relevador de transferencia controlado por ESP32 que detecta pérdida de AC y arranca el respaldo). Costo total ~$2,500 vs. perder un ciclo completo de hierbas. Para cortes >12 h (raros pero ya vistos): protocolo manual de riego por gravedad con checklist.

## (b) Apagones en CDMX: frecuencia real

No existe un SAIDI/SAIFI público fácil de citar por colonia (gap para verificación humana), pero los datos duros disponibles:

- El **Tren Ligero de CDMX registró 66 cortes de energía entre enero 2025 y el 26 de junio de 2026** (45 en 2025, 21 en el primer semestre 2026), algunos con suspensión de hasta 4 horas — infraestructura eléctrica dedicada, en la zona sur (Coyoacán, Tlalpan, Xochimilco). (Publimetro, 14-jul-2026, vía solicitud de transparencia al STE.)
- **Mayo 2024:** crisis nacional con 3 días de apagones que incluyeron CDMX (N+).
- **Septiembre 2026:** apagones en el sureste y en centros industriales de Nuevo León; la columna de La Razón (02-sep-2026) advierte que "durante un par de años la tónica pueden ser eventos así, e incluso agravarse por eventos climáticos extremos" por el rezago de inversión en transmisión.
- CFE publica **cortes programados por mantenimiento en CDMX con frecuencia semanal-quincenal** (headlines de ene, mar, abr, jun 2026), típicamente de 2–8 h por colonia.
- En temporada de lluvias (may–oct) las tormentas tiran el servicio por horas en alcaldías específicas (N+, adn40).

**Traducción operativa:** planear con **3–6 cortes/año de 1–8 h** en tu colonia es realista; un corte >2 h en año 1 es prácticamente seguro. El respaldo DC del punto (a) no es paranoia, es tabla de actuario. Además: tras cada corte el sistema debe *auto-recuperarse* (ESPHome/HA arrancan solos, la bomba rearranca, y la alarma de "bomba sin flujo tras restauración" (sensor YF-S201, ya está en el plan) avisa al teléfono).

## (c) Mermas de microgreens y rechazo de restaurantes

**No existe un % de merma "oficial" publicado** (gap). Lo que sí está documentado:

- La revisión académica de referencia (Comprehensive Reviews in Food Science, 2020, PubMed 32144769) dice textual: "One major limitation to the growth of the microgreen industry is the **rapid quality deterioration that occurs soon after harvest**, which keeps prices high and restricts commerce to local sales. Once harvested, microgreens easily dehydrate, wilt, decay and rapidly lose certain nutrients." Y aunque no ha habido brotes atribuidos, ya acumulaban **7 recalls** por riesgo de patógenos (comparten fisiología con germinados).
- Causas de merma en producción: germinación irregular por lote de semilla, damping-off/fusarium (el plan ya lo menciona), estrés térmico en olas de calor, charolas tiradas por contaminación.

**Estimación propia honesta (así márcala en tu Excel):** en régimen estable un productor competente tira o no vende el **10–20% de las charolas sembradas** (año 1 más cerca de 20–25% mientras aprendes; girasol y chícharo son nobles, brócoli y betabel fallan más). El plan ya descuenta "mermas" dentro de $1,000–1,500/mes junto con agua y luz — a 30 charolas/semana con costo variable de ~$25–30/charola, 15% de merma son ~$500–700/mes solo de insumos perdidos, más el ingreso no facturado (~$1,600–2,700/mes de venta perdida). **Siembra 15–20% más de lo comprometido, siempre.**

**Rechazo de restaurantes:** sin estadística publicada (gap). Mecánica real: el chef rechaza por marchitez, tamaño fuera de spec, plaga visible o simplemente porque cambió el menú. Presupuesta **5–10% de las entregas rechazadas o "recortadas" en los primeros 6 meses** y créditos/reposiciones como costo comercial. Entregar charola viva (producto aún creciendo) reduce el rechazo casi a cero — es tu mejor arma y el plan ya la tiene.

## (d) Estacionalidad de restaurantes CDMX (con números 2025–2026)

- **Enero es un cráter:** CANIRAC Durango reportó caídas de **30–40% en ventas en enero 2025** (vs. 24–30% en 2024); en Puebla se reportaron caídas de **hasta 50% en enero 2026** (MSN/El Sol de Puebla). CDMX no es distinta: la "cuesta de enero" restaurantera es estructural.
- **El 2026 es un mal año del sector:** CANIRAC nacional esperaba crecer 3% y su presidente estima que llegarán a **+1.3% nominal, es decir, venderán MENOS platillos que en 2025**; 9 de cada 10 restaurantes subieron precios solo 3–5% absorbiendo costos; **6 de cada 10 aperturas de restaurantes fracasan** (El Mañana/entrevista al presidente de CANIRAC, 30-ago-2026).
- Hasta **el Mundial 2026 decepcionó**: el mercado restaurantero se contrajo **hasta 20%** durante el torneo; 5 de cada 10 restaurantes vendieron menos que una semana regular; 45% operó con ocupación <50% (El Economista, 11-sep-2026). El consumo migró a bares o a casa.
- Reforma de jornada a 40 h en discusión: CANIRAC estima **+32% de costo de nómina** para restaurantes — presión adicional de márgenes en tus clientes 2026–2027.
- **Diciembre es el pico** (posadas/cenas) — pero muchos restaurantes de autor **cierran del 24 dic al 6 ene** y los chefs toman vacaciones en enero y Semana Santa: tu mejor mes de producción de invierno choca con dos semanas de pedidos en cero.

**Traducción a tu flujo:** modela **enero–febrero con -35% de ingreso** y Semana Santa con -20%. Tu "neto realista $8,000–13,500" es el promedio de meses buenos; el colchón de caja para enero debe salir de noviembre–diciembre. Y ojo: le estás vendiendo a un sector que en 2026 está recortando SKUs premium — el microgreen es de lo primero que un costero recorta. Diversifica desde Fase 1 con 1–2 canales no-restaurante (mercaditos orgánicos de fin de semana, box de suscripción a particulares, cafés de especialidad) para que ningún canal pese >60%.

## (e) Cadena de frío: sí es obligatoria para producto cortado

Datos duros (estudio en mostaza, Foods/Life 2023, PubMed 36836750 — almacenado en bolsa PE de 150 µm):

| Temperatura | Vida útil sensorial |
|---|---|
| **5 °C** | **14 días** |
| 10 °C | 4 días |
| 15 °C | 2 días |
| 20–25 °C | **< 1 día** (se deteriora "beyond consumption") |

Conclusiones operativas:

1. **Producto cortado = refrigeración a 4–5 °C desde la primera hora.** Un patio en CDMX a 18–25 °C mata el producto cortado el mismo día. Necesitas **refrigerador dedicado** (uno usado de 9–11 pies funciona; ~$3,000–5,000 aprox. en Mercado Libre) — no el refri de la cocina de tu casa (inocuidad + espacio + auditoría visual del cliente).
2. **La hielera SÍ basta para el reparto**, no para almacenar: pre-enfría el producto a 5 °C la noche anterior, hielera rígida de 45–50 L con 4–6 gel packs congelados mantiene <10 °C por 4–6 h — de sobra para una ruta de 2–4 h en CDMX. (Hielera 45–50 L: ~$900–1,800 aprox. en ML/Home Depot, precio no verificado.)
3. Ese refri suma ~25–40 kWh/mes al cálculo DAC del punto (a). Inclúyelo.
4. La **charola viva evita todo esto** — véndela como formato preferente; el cortado, solo bajo pedido y entregado el mismo día de corte (que además es tu pitch de venta y es verificable en tu dashboard).

## (f) Tiempo real por semana: 6–9 h es fantasía en Fase 1–2; son ~15 h

El marketing gringo (microgreensfarmer.com: "Do you have 4 hours a week to spare?") vende 4 h/semana; es la cifra de un hobby de 5 charolas, no de 30 charolas/semana + NFT + ventas. Desglose honesto en régimen Fase 1–2 (30 charolas/sem + 6–8 líneas NFT, 4–6 clientes):

| Tarea | h/semana |
|---|---|
| Siembra (2 sesiones: pesar, hidratar, sembrar, apilar) | 3.0 |
| Cosecha + empaque (10–12 min/charola cortada + hierbas) | 3.5–4.5 |
| Lavado y desinfección de charolas (H2O2/cloro) | 1.5 |
| Reparto (2 rutas/sem × 1.5–2 h en tráfico CDMX) | 3.0–4.0 |
| Ventas, WhatsApp con chefs, cobranza, facturas | 1.5–2.0 |
| Sistema: calibración de sondas, limpieza de depósito, ajustes | 1.0–1.5 |
| Compras de insumos / imprevistos | 1.0 |
| **Total** | **14.5–17.5 h/semana** |

La automatización DIY quita el riego, la ventilación y la vigilancia (que sin ella serían 5–8 h más y sustos), **pero no siembra, no corta, no lava, no reparte y no cobra**. El "6–9 h/semana" del plan solo se cumple en Fase 0–1 chica (10–15 charolas, sin NFT, 2 clientes). Presupuesta 15 h y que la sorpresa sea a favor. Implicación de fondo: a $10k netos/mes entre 65 h/mes ≈ **$150/h** — decente, pero compáralo contra tu tarifa de consultoría antes de escalar m² en lugar de precio.

## (g) Vecinos y condominio: revisa el régimen ANTES de la Fase 1

Marco legal real (Ley de Propiedad en Condominio de Inmuebles para el Distrito Federal, texto vigente, última reforma 04-ago-2023, consultada en Justia):

- **Art. 21:** queda prohibido a los condóminos "**destinarla a usos distintos al fin establecido en la Escritura Constitutiva**" (fracc. I) y "realizar acto alguno que afecte la tranquilidad de los demás condóminos" (fracc. II). Una unidad habitacional usada como micro-granja comercial con estructura de PTR, entregas y ruido es impugnable por cualquier vecino ante la PROSOC.
- **Art. 23:** **las azoteas de uso general son propiedad común** — si el "patio" fuera área común de uso exclusivo (frecuente en PH y condominios horizontales), instalar un túnel requiere acuerdo de asamblea; construido sin permiso = te lo pueden hacer quitar.
- **Si el patio es tuyo (casa propia, no condominio): el riesgo baja a molestias** (ruido, escurrimientos, aspecto) vía Ley de Cultura Cívica — manejable.

Puntos prácticos: una bomba periférica de 0.5 HP produce ~55–65 dB — audible de noche en un patio compartido; la bomba chica DC del punto (a) es casi inaudible (otra razón más para el rediseño). El túnel con plástico UV es visible desde ventanas vecinas: estética "invernadero ordenado" y comunicación temprana con vecinos (y regalar charolas) vale más que cualquier argumento legal. **Checklist previo a invertir los $18–28k de Fase 1: 1) ¿escritura dice "uso habitacional" en condominio o casa propia?; 2) ¿el patio es privativo o común de uso exclusivo?; 3) uso de suelo del predio (consulta gratuita en SEDUVI online) — la venta a restaurantes con factura desde un domicilio habitacional en CDMX suele encuadrarse como actividad de bajo impacto, pero confírmalo (gap: verificación humana con el certificado de uso de suelo de TU predio).**

## (h) Robo y seguridad del equipo en patio

Contexto duro (ENVIPE 2026 del INEGI, publicada 10-sep-2026, datos 2025):

- **CDMX es la entidad con la tasa de prevalencia delictiva MÁS ALTA del país: 34,930 víctimas por cada 100 mil habitantes** (nacional: ~24,000; Edomex 31,889).
- 33.8 millones de delitos en 2025; 28.5% de los hogares del país tuvo al menos una víctima; fraude y extorsión ya son el 44% de los delitos (ojo: **la extorsión telefónica a negocios visibles es riesgo real cuando empieces a facturar y tener presencia**).

Tu exposición concreta: ~$8–14k de equipo robable en el patio en Fase 2 (Pi/mini-PC, sondas pH/EC, bombas, cámara, herramienta) + el costo de reposición en tiempo (2–4 semanas sin automatización). Mitigación barata y suficiente a esta escala:

- No visible desde la calle; racks y depósito lejos de bardas colindantes.
- Pi/mini-PC y fuente **dentro de casa**, solo nodos ESP32 (valor $150 c/u) a la intemperie — rediseño gratis que reduce el botín 80%.
- Candados + cadena en puertas del túnel (~$400–800), y la ESP32-CAM del plan con detección de movimiento nocturno y notificación (ya lo tienes en el stack, actívalo desde Fase 1).
- Marca el equipo (grabador) y guarda serie/fotos para denuncia.

## (i) Seguros: la respuesta honesta es "casi nadie te va a asegurar esto barato"

- **Seguro de casa-habitación:** cubre contenidos contra robo con violencia e incendio, pero **el uso comercial del inmueble puede excluir o rescindir la cobertura** — hay que declararlo a la aseguradora (pregunta explícita: "actividad de agricultura urbana comercial en el domicilio"). No encontré producto empaquetado ni precio público para micro-agricultura urbana en México (gap: cotizar directo con 2–3 aseguradoras pyme — GNP/Chubb/HDI — vía agente).
- **Responsabilidad civil por producto** (alguien se intoxica con tu microgreen): a esta escala prácticamente nadie lo contrata; tu "seguro" real es inocuidad documentada: H2O2 en charolas, agua de cisterna analizada 1×/año (~$800–1,500 aprox. laboratorio), lote y fecha en cada etiqueta (trazabilidad = con qué respondes ante un chef si algo sale mal). Recuerda: el sector ya lleva 7 recalls en EUA por patógenos (PubMed 32144769); vendes un producto crudo listo-para-comer.
- Decisión racional a esta escala: **autoasegurarte** (fondo de reposición de $10k que se llena con $500/mes) + mitigación física del punto (h), y cotizar seguro formal solo si pasas de ~$25k/mes de ingreso.

## (j) Escalabilidad: qué haces cuando la demanda supere los 80 m²

Primero, el techo real de los 80 m² no son los m²: es **energía (DAC), horas-fundador y agua (tandeo)**. Con racks verticales, 80 m² dan físicamente para 100–150 charolas/sem + 12–16 líneas NFT, pero a las ~50 charolas/sem ya chocaste con las 20–25 h/sem de una sola persona y con los 250 kWh si metes LEDs.

Escalera de decisiones (en orden, cada peldaño se paga solo):

1. **Sube precios / lista de espera** (el gate de Fase 2 del plan ya la contempla): margen sin capex ni horas. Un productor local con demanda insatisfecha está subvaluado.
2. **Ayudante 4–8 h/sem** (ver punto l) antes de un solo m² más: desbloquea ~40 charolas/sem.
3. **Densificación con LED** (2º turno de luz en racks): +40–60% de producción, pero +80–150 kWh/mes → **esto solo con contrato PDBT de negocio separado** (sin riesgo DAC, deducible; requiere trámite CFE — gap: costo exacto $/kWh PDBT 2026 sin verificar, aprox. $4–5.5/kWh).
4. **Segunda ubicación** (azotea/bodega rentada cerca de la zona de clientes): duplica casi todo el capex (~$40–60k) y añade renta (~$8–20k/mes aprox. una bodega chica en CDMX, no verificado); solo tiene sentido con ~$30k/mes de demanda comprobada y ayudante ya entrenado. La alternativa capital-light: **aliarte con otro productor** (él produce con tu spec, tú vendes y repartes con tu marca) — el cuello real del negocio es la relación con chefs, no los m².
5. Lo que NO hacer: firmar contrato de renta ANTES de tener lista de espera de 8+ clientes recurrentes por 2 meses.

## (k) Costo de adquisición de cliente (CAC) real

El plan trata las visitas de Fase 0 como "gratis". Cuenta real de la campaña de adquisición (15 visitas para cerrar 2–3 clientes, la tasa implícita del propio plan, consistente con conversión fría B2B de 10–25%):

| Concepto | Costo |
|---|---|
| 15 muestras regaladas (charola/clamshell + etiqueta) | ~$750 |
| Transporte/gasolina 15 visitas | ~$900 |
| Re-visitas y degustaciones de cierre (5×) | ~$300 |
| **Out-of-pocket por cliente cerrado (÷3)** | **~$650** |
| + 22–30 h de tu tiempo (1.5–2 h/visita con traslado) | ~8–10 h/cliente |

Y no es un costo de una sola vez: **la rotación de chefs** (el plan la identifica) implica churn de clientes de ~30–50% anual en restauración — o sea que re-pagas CAC cada año por la mitad de tu cartera, en un sector donde 6 de cada 10 aperturas fracasan (CANIRAC 2026): te van a cerrar clientes. Presupuesta **$3,000–5,000/año + 30–40 h/año permanentes en labor comercial**. Mitigaciones: formalizar con administrador/dueño y no solo con el chef (ya está en el plan, bien), pedir 1 referido a cada chef contento (baja el CAC ~70%), WhatsApp Business con catálogo y lista de precios viva.

## (l) Burnout del fundador único y plan B de mano de obra

El riesgo estructural: la producción es **52 semanas/año sin pausa** (los microgreens no saben de puentes). El plan dice "el sistema aguanta 3–4 días solo" — cierto para riego/alarmas, **falso para cosechar, empacar y entregar**: si tú no estás un jueves, ese ingreso no existe y el chef prueba otro proveedor. Con 15 h/sem + trabajo principal, el punto de quiebre típico es el mes 4–6.

Números reales de mano de obra CDMX (2026):

| Concepto | Valor | Fuente |
|---|---|---|
| Salario mínimo 2026 (zona general) | **$315.04/día; $9,582.47/mes** (vigente 1-ene-2026, +13%) | CONASAMI vía Yahoo/El Economista |
| Ayudante general, mediana de mercado | **$32.31/h; ~$63,000/año** (rango hasta $147,600) | Talent.com México |
| Costo efectivo por horas, informal-digno | $50–60/h (pagando arriba de mercado por confiabilidad) | estimación propia |
| **Ayudante 6 h/sábado (siembra+lavado+empaque)** | **~$1,300–1,600/mes** | cálculo |

Plan B concreto y barato: desde el **mes 4** (no cuando ya estés quemado), un ayudante fijo de 6 h/semana con SOP escrito (checklists de siembra/cosecha/lavado con fotos — el mismo rigor que ya piensas ponerle al firmware). Eso cuesta ~15% del neto proyectado y te compra: vacaciones posibles, enfermedad cubierta, y el primer paso de la escalera de escalamiento (j). Para ausencias largas, CANIRAC tiene bolsa de trabajo del sector y el vecino/familiar con checklist del plan sirve solo para regar y avisar, no para operar. **Regla anti-burnout medible: si 3 semanas seguidas pasas de 18 h, contratas o recortas clientes — está prohibido "aguantar".**

---

## Tabla consolidada de proveedores/recursos (verificados hoy salvo indicación)

| Proveedor / recurso | Qué | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Steren — no-breaks | NB-060 mini-UPS módem/Pi 8,000 mAh; NB-605 600 VA; NB-900 900 VA; NB-1500 1,500 VA; NB-2200 2,200 VA | $529 / $1,160 / $1,970 / $2,436 / $6,090 | https://www.steren.com.mx/catalogsearch/result/?q=no+break | Precios vistos hoy en búsqueda del sitio |
| Steren — baterías 12 V AGM | BR-1207 7 Ah; BR-1212 12 Ah; BR-1224 24 Ah; cargadores BR-510/BR-700 | $406 / $568.40 / $1,044 | https://www.steren.com.mx/catalogsearch/result/?q=bateria+12v+acido | Base del respaldo DC de la bomba NFT |
| Steren — medidor de consumo | Wattímetro de enchufe HER-432; contacto Wi-Fi con medidor SHOME-135 | $399 (oferta $336.40) / $249 (oferta $208.80) | https://www.steren.com.mx/catalogsearch/result/?q=medidor+de+consumo | Para auditar kWh del hogar antes de Fase 2; el SHOME-135 se integra a HA |
| Cyberpuerta — UPS 1000 VA | Forza NT-1011 $939; CDP R-UPR1008 $1,399; Hikvision DS-UPS1000-X $1,469; APC BV1000 $1,689; CyberPower CP1000AVRLCD $3,789 | $939–3,789 | https://www.cyberpuerta.mx/index.php?cl=search&searchparam=ups%201000va | Entrega en CDMX; solo para cargas chicas (Pi/red), no para bomba 0.5 HP |
| Mercado Libre — bomba 12 V | Bombas de agua 12 V DC (respaldo/principal NFT) | ~$250–900 aprox. | https://listado.mercadolibre.com.mx/bomba-agua-12v | URL de búsqueda; precio no verificado hoy |
| Mercado Libre — hielera | Hielera rígida 45–50 L para reparto | ~$900–1,800 aprox. | https://listado.mercadolibre.com.mx/hielera-45-litros | URL de búsqueda; precio no verificado hoy |
| Mercado Libre — refrigerador usado | Refri dedicado 9–11 pies para producto cortado | ~$3,000–5,000 aprox. | https://listado.mercadolibre.com.mx/refrigerador-usado | URL de búsqueda; precio no verificado hoy |
| CFE — tarifa 1 y DAC | Página oficial de tarifas (consulta mensual) | — | https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/Tarifa1.aspx y https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/TarifaDAC.aspx | La tabla de $/kWh se carga al elegir mes (JS); límites DAC visibles |
| Talent.com México | Salario de ayudante general (mediana y rango) | $32.31/h; $63,000/año | https://mx.talent.com/salary?job=ayudante+general | Consultado hoy |
| CANIRAC | Cámara del sector: indicadores, bolsa de trabajo, capacitación, directorio CDMX | — | https://portal.canirac.org.mx/ | Útil para inteligencia de clientes y contratación |
| PubMed — mostaza 5 °C/14 días | Estudio de temperatura de almacenamiento | — | https://pubmed.ncbi.nlm.nih.gov/36836750/ | 5→14 d; 10→4 d; 15→2 d; 20–25 °C <1 d |
| PubMed — revisión shelf life/inocuidad | Review 2020: deterioro postcosecha, 7 recalls | — | https://pubmed.ncbi.nlm.nih.gov/32144769/ | Base para cadena de frío e inocuidad |
| Justia México | Ley de Propiedad en Condominio de Inmuebles para el DF (texto vigente, ref. 04-ago-2023) | — | https://mexico.justia.com/estados/df/leyes/ley-de-propiedad-en-condominio-de-inmuebles-para-el-distrito-federal/ | Arts. 21 y 23 citados en (g) |

Fuentes de prensa/datos citadas: MiBolsillo (DAC ago-2026: https://www.mibolsillo.com/tips/cfe-2026-la-razon-por-la-que-perderias-el-subsidio-de-energia-20260829-0025.html), La Verdad Noticias (límites DAC, 06-sep-2026: https://laverdadnoticias.com/dinero-inteligente/finanzas-personales/cfe-tarifa-dac-como-saber-cambio), Infobae (DAC may-2026: https://www.infobae.com/mexico/2026/05/01/recibo-de-luz-cfe-2026-como-evitar-la-tarifa-domestica-de-alto-consumo/), Debate (bloques y límites, 02-jul-2026: https://www.debate.com.mx/consejos/el-peligro-del-recibo-de-luz-el-limite-de-consumo-para-no-perder-el-subsidio-de-la-cfe-en-mexico-20260702-0112.html), Publimetro (Tren Ligero 66 apagones: https://www.publimetro.com.mx/noticias/2026/07/14/tren-ligero-sobre-rieles-pero-sin-luz-suma-66-apagones-en-cdmx/), La Razón (apagones sep-2026: https://www.razon.com.mx/opinion/2026/09/02/apagones-del-bienestar/), El Economista (Mundial -20%: https://www.eleconomista.com.mx/bistronomie/restaurantes-invirtieron-mundial-terminaron-caidas-20260911-832901.html), El Mañana/CANIRAC (+1.3% 2026, 6/10 fracasan: https://www.elmanana.com/opinion/columnas/mexicanos-gastan-menos-en-restaurantes-canirac-propone-esto-6179619.html), Yahoo Noticias (cuesta de enero Durango -30/40%: https://es-us.noticias.yahoo.com/cuesta-enero-causa-ca%C3%ADda-40-030438207.html; salario mínimo 2026: https://es-us.noticias.yahoo.com/entra-vigor-salario-m%C3%ADnimo-2026-140700644.html), El Siglo de Torreón (ENVIPE 2026 CDMX 34,930/100k: https://www.elsiglodetorreon.com.mx/noticia/2026/fraude-y-extorsion-dominan-los-delitos-en-mexico-suman-44-inegi.html), microgreensfarmer.com (la promesa de "4 h/semana": https://microgreensfarmer.com/).

---

## Recomendación concreta (qué comprar/hacer exactamente y por qué)

**Esta semana (costo total ≈ $340):**
1. Compra el **medidor Steren HER-432 ($336.40)** y mide 7 días el consumo base de tu casa. Si tu hogar ya promedia >160 kWh/mes, la Fase 2 tal como está diseñada te manda a DAC: decide desde ahora "bomba chica DC" y, si algún día metes LEDs, "contrato PDBT aparte".
2. Lee tu recibo CFE: confirma que eres tarifa 1 y anota tu promedio anual de kWh (viene graficado). Configura desde ya en Home Assistant un helper de energía con **alarma en 220 kWh/mes acumulados**.
3. Verifica el estatus legal del patio: escritura (¿condominio o propiedad plena?), y consulta el uso de suelo de tu predio en SEDUVI (gratis, online). Si es condominio: NO inviertas los $18–28k de Fase 1 sin revisar la Escritura Constitutiva (Art. 21 de la Ley de Condominio te puede parar el proyecto con una queja de un solo vecino).

**Cambios al plan (antes de Fase 2):**
4. **Sustituye la "bomba periférica 0.5 HP" por bomba sumergible/magnética de 35–60 W** (o mejor: bomba 12 V DC de ~40 W). Motivo: 324 kWh/mes vs 32 kWh/mes; es la diferencia entre quedarte en tarifa subsidiada o pagar ~$1,800/mes extra en DAC — el error más caro del documento.
5. **Respaldo eléctrico DC, no UPS de PC:** batería Steren BR-1224 (24 Ah, $1,044) + cargador flotante + relevador de transferencia manejado por ESP32 → 6–8 h de riego NFT en apagón (~$2,500 total). Añade el **mini-UPS NB-060 ($529)** para módem+Pi: sin internet no hay alarmas, y los cortes de 1–8 h en CDMX son cosa de 3–6 veces al año (el Tren Ligero acumuló 66 en 18 meses).
6. **Cadena de frío:** refri dedicado usado (~$3–5k) a 4–5 °C + hielera 45 L con gel packs para reparto. Regla: cortado a 20–25 °C dura <1 día; a 5 °C, 14 días. Prioriza venta de charola viva.
7. **Presupuesto realista:** merma 15–20% (siembra ese excedente), enero–febrero -35% de ventas, CAC ~$650 + 8–10 h por cliente y re-adquisición anual del 30–50% de la cartera, 15 h/semana de tu tiempo (no 6–9). Con esos cuatro ajustes, el neto realista de régimen baja de "$8,000–13,500" a **$6,500–11,000/mes** — sigue siendo un buen negocio secundario, pero financia las fases con ese número, no con el optimista.
8. **Mes 4: ayudante 6 h/sábado (~$1,400/mes)** con SOP escrito. Es tu seguro anti-burnout y el prerrequisito de cualquier escalamiento. Antes de rentar un solo m² adicional: lista de espera de 8+ clientes y precios ya subidos una vez.
9. **Seguridad:** cerebro (Pi) dentro de casa, solo ESP32 a la intemperie; candado y cadena; ESP32-CAM con alerta nocturna desde Fase 1. CDMX tiene la tasa de victimización más alta del país (34,930/100k, ENVIPE 2026) — el diseño "botín mínimo en el patio" es gratis.
10. **No contrates seguro todavía:** autoasegúrate con fondo de $500/mes y declara la actividad a tu aseguradora de casa si tienes póliza (evita que te la rescindan). Cotiza pyme formal solo arriba de $25k/mes de ingreso.
