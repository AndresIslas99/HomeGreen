# Procedimiento de instalación por fases

Cada fase termina con una **puesta en marcha (commissioning)** explícita; nada entra en
producción sin pasar su checklist. Las compras exactas y enlaces están en
[01-proveedores-cdmx.md](01-proveedores-cdmx.md); las herramientas por etapa en
[04-herramientas.md](04-herramientas.md).

---

## Fase 0 — Rack de microgreens bajo techo (1 día de montaje)

### 0.1 Selección del sitio (antes de comprar nada)
1. Buscar un punto del patio/interior con: luz natural indirecta buena (una charola de
   microgreens quiere ~100–200 µmol/m²s; medible gratis con la app Photone), piso nivelado,
   toma de agua a < 10 m y contacto eléctrico.
2. Verificar con la app de brújula/sol (Sun Surveyor o similar) que el punto no recibe sol
   directo de mediodía (a 2,240 msnm el UV quema microgreens tiernos) ni queda bajo goteo
   de lluvia.
3. Medir temperatura del punto 3 días (mín/máx): ideal 16–24 °C. Fuera de ese rango la
   germinación se vuelve lenta (< 14 °C) o desordenada (> 27 °C).

### 0.2 Montaje del rack
1. Armar rack metálico de 4–5 niveles; separación vertical ≥ 30 cm entre parrillas.
2. Nivelarlo con nivel de burbuja (charolas desniveladas = riego encharcado en una esquina
   = moho). Calzar patas si el piso no es plano.
3. Forrar cada parrilla con plástico o charola ciega debajo si el rack es de rejilla.
4. Definir zonas: nivel superior = germinación/oscuridad, niveles medios = desarrollo,
   nivel inferior = charolas recién sembradas (más fresco).

### 0.3 SOP de siembra (el proceso que se repite 2×/semana)
1. **Desinfección:** charolas lavadas con jabón y enjuague con solución de H2O2 al 3 %
   (o cloro 1:50 con triple enjuague). Charola con moho previo: doble pasada.
2. **Sanitización de semilla** (girasol y chícharo SIEMPRE — el remojo tibio es una
   incubadora de Salmonella/E. coli si la semilla venía contaminada): inmersión en H2O2 al
   3 % (idealmente a 60 °C) 5 min con agitación, enjuague con agua potable y retirar
   flotantes; para brócoli/rábano sensibles, 10 min a temperatura ambiente. Cuando un
   cliente hotelero pida el estándar duro: hipoclorito de calcio 20,000 ppm (31 g/L del
   granular al 65 %), 15 min con agitación, triple enjuague — protocolo completo, opciones y
   dónde comprar en [research/inocuidad-operativa.md](../research/inocuidad-operativa.md).
3. **Remojo** (solo girasol y chícharo): 8–12 h en agua limpia; cambiarla si pasa de 12 h;
   escurrir. Lavar y desinfectar la cubeta entre lotes.
4. **Sustrato:** hidratar la fibra de coco; llenar charola CON drenaje ~3 cm, compactar
   suave, nivelar.
5. **Densidades de arranque** (charola 10×20; tabla completa por especie con remojo,
   oscuridad, días y rendimiento en [08-recetas](08-recetas-y-economia-unitaria.md);
   calibrar con el ensayo V2 de [06-validacion](06-validacion-y-lazos-agenticos.md)):
   girasol 120–150 g secos · chícharo 250–300 g secos · rábano 25–30 g ·
   betabel 25–35 g · brócoli 13–18 g · arúgula 10–12 g (sin remojo NUNCA).
6. **Siembra:** distribuir uniforme, atomizar, tapar con segunda charola invertida CON peso
   encima (2–4 kg) — el peso fuerza raíces parejas.
7. **Oscuridad:** 2–4 días (rábano/brócoli 2–3; girasol/chícharo 3–4). Atomizar 1–2×/día.
   En diciembre–febrero la germinación se alarga 30–50 % (noches de 5–9 °C): usar tapete
   térmico o el punto más cálido de la casa; en jun–sep sembrar ~10 % menos denso (la
   humedad de 70–89 % enmohece la densidad que en marzo funciona).
8. **Destape a luz indirecta:** riego ya solo POR ABAJO (charola sin drenaje debajo, agua
   entre las dos) — mojar el follaje a partir de aquí es invitar al moho.
9. **Cosecha (día 8–12):** tijera limpia justo sobre el sustrato, de preferencia en la
   mañana del día de entrega. Pesar, registrar en bitácora, empacar.
10. **Post-cosecha:** sustrato usado a composta, charola a la pila de lavado.

### Commissioning Fase 0
- [ ] 6 charolas de prueba (2 variedades) completaron ciclo con rendimiento pesado.
- [ ] Prueba de germinación V1 hecha al lote de semilla comprado.
- [ ] Bitácora funcionando (CSV con las primeras filas reales).

---

## Fase 1 — Túnel, agua y automatización v1 (2–3 fines de semana)

### 1.1 Estructura (15–20 m²)
1. **Trazo:** marcar planta del túnel con hilo y estacas; verificar escuadra midiendo
   diagonales (deben ser iguales ±1 cm).
2. **Anclaje** (procedimiento completo y comparativa de métodos en
   [research/instalacion-tunel-detalle.md](../research/instalacion-tunel-detalle.md)): sobre
   losa de concreto, **placa base de 10–15 cm (solera 3/16") soldada al pie de cada columna
   + 4 anclas de cuña 3/8"×5" por placa** ($36 c/u en Home Depot ⇒ ~$864 el túnel). Perforar
   con rotomartillo, aspirar el polvo (el polvo reduce la carga de extracción a la mitad),
   apretar a torque firme y sellar el perímetro de cada placa con sellador PU. No anclar a
   <15 cm del borde ni en concreto agrietado. En patio rentado/condominio sin permiso de
   perforar: dados de concreto de ≥80 kg por poste + cables a 4 vientos (plan B, inferior).
   CDMX tiene rachas de 50–80 km/h pre-tormenta y el plástico es una vela de ~20 m²: la
   estructura SIN anclar es la que sale volando; el problema es la succión, no el peso.
3. **Marcos:** PTR 1½" o tubo galvanizado; postes cada ≤ 2 m; techo a dos aguas con
   pendiente ≥ 25 % para que la lluvia y el granizo escurran. Unión atornillada mejor que
   soldada si no se domina soldadura (y se puede desmontar/mover).
4. **Cubierta:** plástico UV (calibre 720) en techo, tensado con perfil zigzag o listones
   atornillados — nunca solo grapas. **Malla antigranizo por ENCIMA del plástico** con
   claro de aire, o como doble techo: el granizo de mayo–septiembre rompe plástico tensado
   sin malla.
5. **Laterales:** malla antiáfidos/sombra enrollable para ventilar de día y cerrar de noche.
6. **Drenaje perimetral:** canaleta o pendiente de piso para que el agua de tormenta no
   entre al túnel ni socave anclajes; no tapar coladeras del patio con placas ni tinaco.
7. **Reparto del trabajo y ruta crítica (4 semanas, colchón 6):** el camino crítico es el
   HERRERO — contratarlo solo para fabricar y montar el esqueleto (2–4 días, ~$2,500–4,000;
   pedir 3 cotizaciones el día 1). Tú haces trazo, barrenos/anclas, perfil zigzag, plástico
   (con 2 ayudantes, al MEDIODÍA y sin viento — el plástico se tensa con calor y queda tenso
   al enfriar), canaleta y cortinas. Materiales el día 1: PTR en Sodimac (stock en tienda),
   anclas/canalón/tinaco en Home Depot (recoger en 24 h), plástico UV + perfil Polygrap
   ($95/2 m) + zigzag ($103/kg) recogidos en Hydro Environment Tlalnepantla (evita
   paquetería). Guías de armado del propio proveedor enlazadas en el informe.
8. **Canaleta → tinaco:** canalón PVC doméstico $269/3.07 m (Home Depot), pendiente
   0.5–1 % hacia la bajante, filtro de hojas + purga de primeras lluvias antes del tinaco.
   El techo de 15–20 m² capta ~500–600 L en una tormenta de 30 mm: no dejarlo caer al patio.

### 1.2 Sistema de agua
1. Tinaco/contenedor 450–750 L sobre base firme y elevada (cada 100 L pesa 100 kg: la base
   importa). Sombreado u opaco: luz + agua = algas.
2. Captación pluvial: bajada del techo del túnel/casa → filtro de hojas → separador de
   primeras lluvias (tlaloque) → tinaco. La primera lluvia de la temporada lava el techo y
   se desvía; el resto entra casi destilada (EC ≪ 0.3).
3. Salida del tinaco con válvula, filtro de sedimentos y derivación a la bomba de riego.
   **Todo el sistema corre desde el tinaco, nunca de la toma directa** (tandeo).

### 1.3 Automatización v1 (riego + ambiente + alarmas)
1. **Banco de pruebas primero:** armar TODO en la mesa (ESP32, relés, sensores, bomba en
   una cubeta) antes de instalar en campo. Flashear ESPHome por USB la primera vez; después
   todo es OTA.
2. **Cableado de campo:** ESP32 y relés en gabinete IP65; pasacables prensaestopa; sensores
   de sustrato con el conector HACIA ARRIBA y encintado (mueren por corrosión del conector,
   no del sensor); DS18B20 sumergido en tinaco; JSN-SR04T apuntando al agua sin obstáculos.
3. **Alimentación y seguridad eléctrica (obligatorio ANTES del primer relé en el patio;
   detalle y cotizaciones en
   [research/electrico-respaldo-seguridad.md](../research/electrico-respaldo-seguridad.md)):**
   fuente 12 V 5 A para bomba/válvulas; buck a 5 V para ESP32; tierra común. El patio es
   "lugar mojado" según la NOM-001-SEDE: **GFCI en todo el circuito exterior** (breaker
   Square D QO120GFI $1,159 en el centro de carga, o mínimo contacto GFCI $389 aguas arriba
   de todo), **tapa intemperie tipo "in-use"** (~$249), **tierra física real** (varilla
   copperweld 5/8"×3 m, ≤25 Ω medidos) y toda la electrónica en gabinete IP65 con
   prensaestopas. Medio día de electricista certificado (~$1,500–3,500 llave en mano con
   tierra) es la partida que evita electrocutar a alguien con las manos mojadas.
4. **Home Assistant** en Raspberry Pi/mini-PC dentro de casa (no en el túnel: humedad),
   con UPS pequeño. Integración ESPHome nativa; dashboard con: humedades de sustrato,
   T/HR, nivel de tinaco, estado de bomba, últimas alarmas.
5. **Lógica:** riego por histéresis por nivel de rack; ventilador por T/HR; alarmas del
   catálogo L0 (ver [06-validacion](06-validacion-y-lazos-agenticos.md)). Configs YAML
   versionadas en este repo (`firmware/`).

### Commissioning Fase 1
- [ ] Estructura aguantó una tormenta real sin daño (o prueba con manguera a presión).
- [ ] Dry-run V3 de 72 h con inyección de fallas: 100 % de alarmas correctas.
- [ ] Riego automático mantuvo 4 charolas testigo sin intervención 7 días.
- [ ] Captación pluvial llenando tinaco y EC del agua captada medida.

---

## Fase 2 — NFT de hierbas + dosificación v2 (2–3 fines de semana)

### 2.1 Construcción de líneas NFT
1. Tubo PVC **sanitario** 4" blanco (Amanco, $415/tramo — NO hidráulico cédula 40 a $1,401:
   el NFT corre sin presión y el blanco refleja calor). Perforar con sierra copa del diámetro
   del CUERPO de la canastilla bajo el labio — **comprar canastillas ANTES de perforar**,
   medir y probar en un retazo (una canastilla "de 2 pulgadas" pide barreno de 1-¾"–1-⅞" /
   44–48 mm, nunca 2" exactas: se cae). Separación entre centros: 20 cm albahaca/arúgula,
   15 cm cilantro. Desbarbar cada hoyo (las rebabas atoran raíces y flujo).
2. Pendiente de cada línea: **2–3 %** (2–3 cm por metro). Soportes cada ≤ 1.5 m para evitar
   panza (agua estancada a media línea = raíces podridas).
3. Retorno por gravedad a depósito de 200–450 L, tapado y aislado del sol (la temperatura
   de solución ideal es 18–22 °C; arriba de 25 °C cae el oxígeno disuelto).
4. Bomba **sumergible 3000–4500 LPH** (65 W ≈ $45/mes de luz corriendo 24/7; la periférica
   0.5 HP del plan original consume 370 W ≈ $260/mes — dejarla solo para trasiego
   cisterna→tinaco) → filtro malla 120 → manifold con válvula de compuerta por línea:
   caudal objetivo **1–2 L/min por línea** (se ajusta con botella de 1 L y cronómetro).
5. Germinación aparte en espuma agrícola/lana de roca; trasplante a canastilla cuando la
   raíz asoma (10–14 días albahaca).

### 2.2 Dosificación automática v2
1. Sondas pH y EC en el RETORNO (lectura de solución mezclada, no junto a la salida de
   dosificación).
2. Peristálticas A/B/pH− dosificando AL DEPÓSITO, cerca de la succión de la bomba para
   mezclar rápido; nunca directo a una línea.
3. Lógica: dosis pequeña fija → esperar 10–15 min de mezcla → re-medir (histéresis con
   tiempo muerto; evita la oscilación clásica). Interlock: sin dosificación si nivel bajo
   o bomba apagada.
4. Calibración quincenal de sondas con buffers pH 4.0/6.86 y solución patrón EC 1.413
   mS/cm — evento en calendario de HA con alarma. Cambio de sonda pH anual.
5. Rutina de depósito: relleno con agua de lluvia/filtrada; **cambio completo de solución
   cada 2–3 semanas** (los micronutrientes se desbalancean aunque la EC "se vea bien") y
   ese registro va a bitácora.

### 2.3 Continuidad eléctrica del NFT — arquitectura "DC-first" (obligatoria antes de la primera línea)

En NFT las raíces cuelgan en una película de 1–3 mm: sin recirculación, marchitez
irreversible en 2–4 h con el túnel caliente. Respaldar la periférica de 120 V con inversor
exigiría ~680 Ah de batería (>$30k): descartado con números. La arquitectura correcta
(análisis y cotizaciones completas en
[research/electrico-respaldo-seguridad.md](../research/electrico-respaldo-seguridad.md)):

```
CFE 127 V ──[GFCI]──> Cargador en flotación ──┬──> Bomba NFT 12 V DC 40–60 W (24/7)
                                              │
                        LiFePO4 12.8 V 100 Ah ┤   (batería SIEMPRE en paralelo: el corte
                                              │    de CFE ni se nota, cero conmutación)
                                              ├──> Nodo ESP32 del NFT (siempre vivo)
                                              └──> [opcional] controlador solar + panel 100 W
```

1. **Bomba de operación continua: diafragma 12 V DC 40–60 W ×2** (principal + respaldo con
   relevador de transferencia manejado por el ESP32; ~$900–1,800 el par en ML). La
   periférica/sumergible de 127 V queda solo para llenado/purga.
2. **Batería LiFePO4 12.8 V 100 Ah** (Epcom, $4,459 verificado en Cyberpuerta): 28–30 h de
   recirculación continua, ~2.5 días en modo supervivencia 15 min ON/15 min OFF. Variante
   austera de arranque: batería AGM 24 Ah + cargador (~$2,500–2,900) para cortes ≤7 h,
   ampliable sin tirar nada.
3. **Opcional recomendado (+~$1,650):** panel 100 W + controlador EPEVER LS2024B — el
   controlador hace de cargador y un corte diurno se vuelve sostenible indefinidamente.
   (Un panel de 100 W NO corre el huerto completo: solo flota la batería.)
4. **UPS chico ($1,189) para router + cerebro:** sin internet no hay alarmas.
5. **Regla de oro:** el fail-safe es físico, no de software — la bomba cuelga del bus de
   batería con `restore_mode: RESTORE_DEFAULT_ON`; Home Assistant avisa y optimiza, pero la
   continuidad del agua nunca depende de que HA esté vivo. Las 5 automatizaciones (bomba sin
   flujo → respaldo, corte de CFE, escalación, modo ahorro por voltaje, nodo caído) están
   con YAML listo en el informe.

### Commissioning Fase 2
- [ ] Todas las líneas con pendiente verificada y sin encharcamiento a media línea.
- [ ] 48 h de recirculación con agua sola: sin fugas, caudal por línea en rango.
- [ ] Dry-run de dosificación en depósito con agua: pH baja/EC sube según lo esperado y
      los interlocks disparan.
- [ ] Primer ciclo de albahaca completo con pH/EC dentro de banda ≥ 90 % del tiempo
      (dato de HA, no de memoria).
- [ ] Simulacro de apagón: botar el breaker del patio 10 min → la bomba sigue (batería),
      llegan las 2 alertas (corte + estado), y al restaurar no hay falso "sin flujo".

---

## Orden de compra recomendado

No comprar la fase completa de golpe; el plan es "vender antes de construir":

1. **Hoy:** rack, charolas, semilla, coco, atomizador, báscula (Fase 0 completa, ~$5–6k).
2. **Solo si G0→1 pasa:** cotizaciones ya pedidas de PTR/malla/plástico → estructura →
   tinaco → electrónica v1 (en ese orden: la estructura protege lo demás).
3. **Solo si G1→2 pasa:** PVC + bomba + depósito → sondas y peristálticas al final
   (el NFT funciona días en manual mientras la dosificación se afina).
