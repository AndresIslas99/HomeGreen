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
2. **Remojo de semilla** (solo girasol y chícharo): 8–12 h en agua limpia; escurrir.
3. **Sustrato:** hidratar el bloque de fibra de coco (un bloque de 5 kg rinde ~70 L);
   llenar charola CON drenaje ~3 cm, compactar suave, nivelar.
4. **Densidades de arranque** (charola 10×20; calibrar después con el ensayo V2 de
   [06-validacion](06-validacion-y-lazos-agenticos.md)):
   girasol 100–120 g · chícharo 200–250 g (remojado) · rábano 30–40 g ·
   betabel 40–50 g · brócoli 20–25 g.
5. **Siembra:** distribuir uniforme, atomizar, tapar con segunda charola invertida CON peso
   encima (2–4 kg) — el peso fuerza raíces parejas.
6. **Oscuridad:** 2–4 días (rábano/brócoli 2–3; girasol/chícharo 3–4). Atomizar 1–2×/día.
7. **Destape a luz indirecta:** riego ya solo POR ABAJO (charola sin drenaje debajo, agua
   entre las dos) — mojar el follaje a partir de aquí es invitar al moho.
8. **Cosecha (día 8–12):** tijera limpia justo sobre el sustrato, de preferencia en la
   mañana del día de entrega. Pesar, registrar en bitácora, empacar.
9. **Post-cosecha:** sustrato usado a composta, charola a la pila de lavado.

### Commissioning Fase 0
- [ ] 6 charolas de prueba (2 variedades) completaron ciclo con rendimiento pesado.
- [ ] Prueba de germinación V1 hecha al lote de semilla comprado.
- [ ] Bitácora funcionando (CSV con las primeras filas reales).

---

## Fase 1 — Túnel, agua y automatización v1 (2–3 fines de semana)

### 1.1 Estructura (15–20 m²)
1. **Trazo:** marcar planta del túnel con hilo y estacas; verificar escuadra midiendo
   diagonales (deben ser iguales ±1 cm).
2. **Anclaje:** en piso de concreto, placas o ángulos anclados con taquete expansivo de
   3/8"; en tierra, dados de concreto de 30×30×30 cm. CDMX tiene rachas fuertes
   pre-tormenta: la estructura ligera SIN anclar es la que sale volando.
3. **Marcos:** PTR 1½" o tubo galvanizado; postes cada ≤ 2 m; techo a dos aguas con
   pendiente ≥ 25 % para que la lluvia y el granizo escurran. Unión atornillada mejor que
   soldada si no se domina soldadura (y se puede desmontar/mover).
4. **Cubierta:** plástico UV (calibre 720) en techo, tensado con perfil zigzag o listones
   atornillados — nunca solo grapas. **Malla antigranizo por ENCIMA del plástico** con
   claro de aire, o como doble techo: el granizo de mayo–septiembre rompe plástico tensado
   sin malla.
5. **Laterales:** malla antiáfidos/sombra enrollable para ventilar de día y cerrar de noche.
6. **Drenaje perimetral:** canaleta o pendiente de piso para que el agua de tormenta no
   entre al túnel ni socave anclajes.

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
3. **Alimentación:** fuente 12 V 5 A para bomba/válvulas; buck a 5 V para ESP32. Tierra
   común. Contacto con protección (el patio es intemperie: usar contacto con tapa y GFCI
   idealmente).
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
1. Tubo PVC hidráulico 4": perforar con sierra copa del diámetro de la canastilla (para
   canastilla de 2" ≈ sierra copa de 48–51 mm; **comprar canastillas ANTES de perforar** y
   probar en un retazo). Separación entre centros: 20 cm albahaca/arúgula, 15 cm cilantro.
2. Pendiente de cada línea: **2–3 %** (2–3 cm por metro). Soportes cada ≤ 1.5 m para evitar
   panza (agua estancada a media línea = raíces podridas).
3. Retorno por gravedad a depósito de 200–450 L, tapado y aislado del sol (la temperatura
   de solución ideal es 18–22 °C; arriba de 25 °C cae el oxígeno disuelto).
4. Bomba (periférica 0.5 HP o sumergible equivalente) → filtro malla 120 → manifold con
   válvula de compuerta por línea: caudal objetivo **1–2 L/min por línea** (se ajusta a ojo
   con botella de 1 L y cronómetro).
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

### Commissioning Fase 2
- [ ] Todas las líneas con pendiente verificada y sin encharcamiento a media línea.
- [ ] 48 h de recirculación con agua sola: sin fugas, caudal por línea en rango.
- [ ] Dry-run de dosificación en depósito con agua: pH baja/EC sube según lo esperado y
      los interlocks disparan.
- [ ] Primer ciclo de albahaca completo con pH/EC dentro de banda ≥ 90 % del tiempo
      (dato de HA, no de memoria).

---

## Orden de compra recomendado

No comprar la fase completa de golpe; el plan es "vender antes de construir":

1. **Hoy:** rack, charolas, semilla, coco, atomizador, báscula (Fase 0 completa, ~$5–6k).
2. **Solo si G0→1 pasa:** cotizaciones ya pedidas de PTR/malla/plástico → estructura →
   tinaco → electrónica v1 (en ese orden: la estructura protege lo demás).
3. **Solo si G1→2 pasa:** PVC + bomba + depósito → sondas y peristálticas al final
   (el NFT funciona días en manual mientras la dosificación se afina).
