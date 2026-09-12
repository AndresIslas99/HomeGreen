# Inocuidad alimentaria operativa: sanitización de semilla, laboratorios y trazabilidad por lote
**Proyecto:** Huerto comercial automatizado (microgreens + hierbas NFT), patio 80 m², CDMX
**Fecha de investigación:** 12 de septiembre de 2026
**Nota metodológica:** el presupuesto de búsquedas web de la sesión estaba agotado (200/200), por lo que toda la investigación se hizo abriendo directamente URLs canónicas (WebFetch/curl) y verificando su contenido. Cada afirmación indica si la fuente fue **verificada** (página abierta y leída hoy) o es **conocimiento de referencia por verificar**. Los precios sin verificación en página están marcados "aprox."

---

### 1. Por qué esto importa (contexto de riesgo)

- Los microgreens de **girasol y chícharo** son los que comparten más riesgo con los germinados/brotes: semilla grande, **remojo de 8–24 h** en agua tibia = incubadora perfecta de *Salmonella* y *E. coli* O157:H7 si la semilla venía contaminada. Los brotes causan brotes epidémicos recurrentes documentados por FDA; por eso EE. UU. regula a los sprouters con un subparte completo (21 CFR 112, Subparte M) que exige **tratamiento científicamente válido de la semilla antes de germinar** y análisis del agua de riego gastada.
- Los microgreens cortados **por encima del sustrato, sin tocar la semilla**, tienen un perfil de riesgo menor que los brotes (no se come raíz ni semilla), pero el remojo inicial y la venta de **"charola viva"** (el cliente corta sobre el cepellón) acercan el riesgo al de un germinado.
- Fuentes verificadas hoy:
  - FDA — *Guidance for Industry: Reducing Microbial Food Safety Hazards in the Production of Seed for Sprouting* (mayo 2022): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-reducing-microbial-food-safety-hazards-production-seed-sprouting (página abierta y confirmada; aplica a toda la cadena de semilla para germinar, motivada por "continuing outbreaks of foodborne illness associated with... raw and lightly-cooked sprouts").
  - Sprout Safety Alliance (Illinois Tech/IFSH + FDA): https://www.iit.edu/ssa (página abierta; ofrece video de tratamiento de semilla, manual gratuito *Safer Sprout Production* 2ª ed. y red de asistencia técnica).
  - Produce Safety Alliance (Cornell CALS): https://producesafetyalliance.cornell.edu/ (dominio verificado hoy; es la referencia de capacitación FSMA para productores de frescos).

---

### 2. Protocolo de sanitización de semilla (adaptado a insumos comprables en CDMX)

**Regla de decisión por variedad:**

| Variedad | Remojo | Riesgo relativo | Tratamiento |
|---|---|---|---|
| Girasol | 8–12 h | Alto | SIEMPRE tratar (Opción A o B) |
| Chícharo | 8–24 h | Alto | SIEMPRE tratar (Opción A o B) |
| Betabel/acelga | 2–8 h opcional | Medio | Tratar si hay remojo |
| Rábano, brócoli, col | Sin remojo | Bajo–medio | Opción B o semilla con COA del proveedor |

**Opción A — Hipoclorito de calcio 20,000 ppm (estándar histórico de la industria de brotes, FDA 1999/2017)**
> Fundamento: la guía FDA de 1999 *Reducing Microbial Food Safety Hazards for Sprouted Seeds* y la guía de operaciones de brotes de 2017 citan 20,000 ppm de cloro libre con Ca(OCl)₂ como el tratamiento de referencia (la página FDA de 1999 respondió 401 al fetch de hoy; verificar URL en la sección de gaps — el marco regulatorio vigente, 21 CFR 112.142(e), exige "tratamiento científicamente válido" sin fijar un químico único).

1. Preparar solución al momento: **31 g de hipoclorito de calcio al 65% por litro de agua potable** (= ~20,000 ppm cloro libre; si tu producto es 70%, usa 28.6 g/L). Volumen mínimo: **5 L de solución por kg de semilla** (relación ≥5:1).
2. Sumergir la semilla **15 minutos con agitación continua** (la agitación es parte del tratamiento validado; sin ella quedan bolsas de aire).
3. Escurrir y hacer **triple enjuague** con agua potable hasta eliminar olor a cloro.
4. Pasar directo al remojo/siembra; no almacenar semilla húmeda.
5. Seguridad: solución cáustica y oxidante — guantes de nitrilo, gafas, exterior o zona ventilada; nunca mezclar con ácidos ni con peróxido. Desechar diluida.
6. Antes de tratar un lote completo: **prueba de germinación con 200 semillas tratadas vs 200 sin tratar** (el hipoclorito puede bajar germinación en lotes viejos).

**Opción B — Peróxido de hidrógeno 3% (escala casera/microgreens; protocolo tipo UC ANR Pub. 8151 "Growing Seed Sprouts at Home")**
> UC Davis/ANR recomendó para brotes caseros: H₂O₂ al 3% **precalentado a 60 °C, 5 minutos de inmersión** con agitación, enjuague con agua potable y retiro de semillas flotantes/basura. El catálogo ANR migró de sitio y el PDF 8151 no pudo abrirse hoy (ver gaps); el protocolo es el difundido por extensión UC.
- Variante fría para semilla sensible (brócoli, rábano): H₂O₂ 3% a temperatura ambiente, **10 minutos**, enjuague.
- Es la opción realista de Fase 0: el insumo es el "agua oxigenada" de cualquier farmacia CDMX (~$20–40 aprox. el frasco de 480 mL) o H₂O₂ 35% grado alimenticio diluido 1:11.
- Menos letalidad que 20,000 ppm de cloro, pero razonable para microgreens cortados en aéreo + higiene de proceso.

**Opción C — Ácido peracético comercial (cuando haya flujo de caja)**
- Productos tipo SaniDate 5.0 / Tsunami 100 (BioSafe/Ecolab) se usan en brotes según etiqueta. En México se consiguen vía distribuidores de químicos sanitarios; en Mercado Libre: https://listado.mercadolibre.com.mx/acido-peracetico (precio aprox. $400–900 por 1 L al 15%, no verificado). Dosis según etiqueta del fabricante para semilla.

**Complementos obligatorios del protocolo (todas las opciones):**
- **Agua del remojo posterior**: solo agua potable/desinfectada; cambiarla si el remojo pasa de 12 h; lavar y desinfectar la cubeta entre lotes.
- **Charolas y tijeras**: lavar con jabón, desinfectar con H₂O₂ 3% o solución de cloro 200 ppm (5 mL de cloro doméstico al 6% por litro), secar al aire. Ya está en tu plan (H₂O₂ para charolas) — formalízalo en bitácora.
- **Comprar semilla con Certificado de Análisis (COA)** del proveedor cuando exista (negativo a *Salmonella*/E. coli en 375 g compuestos) y **guardar el número de lote de cada costal**: es la mitad de tu trazabilidad.
- **Charola viva**: véndela con etiqueta "cortar y enjuagar antes de consumir" — desplaza el paso de lavado al cliente y te protege.

**Insumos y dónde comprarlos (CDMX):**

| Insumo | Presentación | Precio MXN | Dónde |
|---|---|---|---|
| Hipoclorito de calcio 65–70% | Bote 1 kg (cloro granular para alberca) | aprox. $150–350 | https://listado.mercadolibre.com.mx/hipoclorito-de-calcio (búsqueda; ML bloqueó verificación directa hoy); también tiendas de albercas/ferreterías grandes |
| Agua oxigenada 3% (10 vol) | Frasco 480 mL–1 L | aprox. $20–60 | Cualquier farmacia (Guadalajara, Del Ahorro, etc.) |
| H₂O₂ 35% grado alimenticio | 1 L | aprox. $180–400 | https://listado.mercadolibre.com.mx/peroxido-de-hidrogeno-grado-alimenticio (búsqueda) |
| Ácido peracético 15% | 1 L | aprox. $400–900 | https://listado.mercadolibre.com.mx/acido-peracetico (búsqueda) |
| Charolas germinación con/sin drenaje | pieza | $117–129 (verificado hoy) | Hydro Environment, CDMX — https://www.hydroenv.com.mx/ (tel. 55-5565-1153; su buscador no arrojó peróxido/sanitizantes, solo equipo de cultivo) |
| Reactivos/quimicos de laboratorio | varios | cotizar | Reactivos Meyer (fabricante CDMX) — https://www.reactivosmeyer.com.mx/ |

---

### 3. Laboratorios de análisis microbiológico en CDMX / zona metropolitana

**Verificados hoy (sitio abierto y leído):**

| Laboratorio | Qué hace | Ubicación / contacto | Acreditación | Precio y tiempo | Enlace |
|---|---|---|---|---|---|
| **Laboratorio QUIBIMEX, S.A. de C.V.** | Microbiología de alimentos crudos y cocidos, fisicoquímicos, superficies; auditorías técnico-sanitarias; cursos | Alfonso Toro 1207, Col. Sector Popular, Iztapalapa, CDMX, CP 09060 · Tel. 55 5445 5494 al 96 · WhatsApp 56 1002 6942 · ventas@quibimex.com.mx | **EMA A-012-001/12 (NMX-EC-17025)**; autorización COFEPRIS **TA-28-19** (el sitio la reporta "en proceso de renovación" — confirmar al cotizar) | No publica precios; cotización directa. L–V 9–19 h | https://laboratorioquibimex.com/ y https://quibimex.com.mx/ |
| **LANISAF — Laboratorio Nacional de Investigación y Servicio Agroalimentario y Forestal (U. A. Chapingo)** | **Detección de E. coli en agua**: por citometría (presencia/ausencia + cuantificación) **$607/muestra**; por plaqueo en medio selectivo **$542/muestra** (catálogo vigente 1-mar-2026, verificado en PDF). Muestra: 200 mL en frasco de vidrio desinfectado, en frío; recepción L–J (V antes de 12 h); resultados ≤12 días hábiles | Edif. Efraím Hernández X., Km 38.5 Carr. México–Texcoco (≈45 min del oriente de CDMX) · Tel. (595) 952 1500 ext. 6450 · lanisaf.servicios@chapingo.mx | ISO 9001:2015 (RSGC-1087, vigente a 2027). No es EMA para este ensayo — útil como monitoreo económico, no como evidencia regulatoria | $542–607 MXN/muestra (VERIFICADO 2026) | https://lanisaf.chapingo.mx/ · catálogo: https://lanisaf.chapingo.mx/wp-content/uploads/2026/02/12-Catalogo-de-servicios-LANISAF-Mar01.pdf |
| **Agrolab México (FS Lab / WTR Lab)** | Uno de los laboratorios de inocuidad más grandes de LatAm: microbiología de alimentos, agua potable/riego, superficies vivas e inertes, paquetes para sector restaurantero y hotelero; +20 oficinas de recolección en el país | Matriz en Gómez Palacio, Dgo.; opera nacionalmente por mensajería/recolección — confirmar oficina CDMX · info@agrolab.com.mx (aviso en sitio: líneas telefónicas con fallas, sep-2026) | Múltiples acreditaciones/aprobaciones (detalle a confirmar al cotizar) | No publica precios | https://agrolab.com.mx/ |
| **Eurofins México (división Agroalimentaria)** | Patógenos: *Salmonella*, *Listeria monocytogenes*, *E. coli* O157, *Campylobacter*, *C. perfringens*; indicadores: coliformes, enterobacterias, estafilococos | Sitio MX no publica dirección; contacto por formulario | Red global; acreditaciones MX a confirmar | No publica precios | https://www.eurofins.com.mx/agro-alimentario/microbiolog%C3%ADa/ |
| **Opciones económicas de directorio (solo teléfono, sin web verificable)** | LAE – Laboratorio Analítico Especializado (Av. 523 #101, San Juan de Aragón, GAM, CDMX · 55 5771 5439) · Laboratorios Bioquality (Cuautitlán Izcalli · 55 5871 1227, giro "análisis de alimentos") | — | Verificar EMA/COFEPRIS por teléfono | — | Listado fuente: https://www.seccionamarilla.com.mx/resultados/laboratorios-de-analisis-de-alimentos/distrito-federal/1 |

**Cómo validar cualquier laboratorio antes de pagar:**
- Padrón de acreditados EMA: https://www.ema.org.mx/portal_v3/ → menú "Catálogo de Acreditados" (el buscador es una app JS; no expone URL directa — verificado hoy).
- Pedir al lab su **número de acreditación EMA** y su **oficio de Tercero Autorizado COFEPRIS** (clave "TA-XX-XX", como el TA-28-19 de Quibimex) y comprobar vigencia.

**Precios de mercado de referencia para presupuestar (NO verificados hoy; contrastar al cotizar):**

| Análisis | Precio típico CDMX 2026 (aprox.) |
|---|---|
| Mesófilos aerobios (producto) | $200–400/muestra |
| Coliformes totales/fecales o E. coli (producto) | $250–500/muestra |
| *Salmonella* spp. en 25 g (producto) | $350–700/muestra |
| Paquete microbiológico agua (NOM-127: coliformes totales + E. coli) | $600–1,200 |
| Superficie viva/inerte (esponjado) | $200–400 |

**Plan de muestreo sugerido (costo anual realista $6,000–10,000 aprox.):**
- **Al arrancar Fase 1:** 1 análisis de agua (tinaco + captación pluvial) y 1 análisis de producto (mezcla girasol+chícharo: mesófilos, E. coli, *Salmonella*) → ese informe es tu carta de presentación B2B.
- **Rutina:** agua cada 6 meses (y siempre que cambies de fuente o arranque la temporada de lluvia si usas pluvial); producto 2–4 veces/año rotando variedades; superficie (mesa de corte) 1–2 veces/año.
- **Monitoreo barato intermedio:** LANISAF ($542) para agua; placas Petrifilm E. coli/coliformes (3M) para autocontrol: https://listado.mercadolibre.com.mx/petrifilm (aprox. $40–70/placa, no verificado).

---

### 4. NOM-251-SSA1-2009 aplicada a un cuarto de cosecha casero

Fuente verificada: texto oficial en SIDOF/DOF (publicada 1-mar-2010, Secretaría de Salud): https://sidof.segob.gob.mx/notas/5133449 — la norma cubre instalaciones, equipo/utensilios, servicios (agua/drenaje), almacenamiento, control de plagas, higiene de personal, transporte y capacitación. Es **obligatoria** para cualquiera que procese/venda alimentos (tu empaque y corte cuentan como "proceso"); COFEPRIS la verifica con el Aviso de Funcionamiento.

**Traducción práctica a tu patio (lo mínimo defendible ante un chef o un verificador):**

| Rubro NOM-251 | Qué hacer en un cuarto de cosecha de 6–10 m² |
|---|---|
| Instalaciones y áreas | Zona de corte/empaque separada del cultivo (aunque sea por cortina plástica); piso y paredes lavables en la zona de empaque; no cosechar sobre tierra descubierta |
| Superficies y utensilios | Mesa de acero inoxidable o tabla de polietileno (NO madera); tijeras/cuchillos de acero; lavar + desinfectar (H₂O₂ 3% o cloro 200 ppm) antes y después de cada cosecha; bitácora de limpieza firmada |
| Agua | Riego final (últimas 48 h) y enjuague de utensilios con agua potable o desinfectada; si usas captación pluvial: filtro de sedimentos + desinfección (cloro a 0.2–1.5 ppm libre o UV) antes de que toque producto; análisis semestral (sección 3) |
| Lavado de manos | Estación con jabón líquido, agua corriente y toallas desechables ANTES de entrar a cosechar; gel alcohol 70% como refuerzo, nunca como sustituto |
| Higiene personal | Cofia/gorra, sin anillos ni pulseras, uñas cortas; no cosechar con heridas descubiertas, diarrea o gripe (esto elimina el vector #1: el humano) |
| Control de fauna | Mallas en ventanas/túnel, **cero mascotas** en zona de cultivo y empaque, trampas mecánicas numeradas en perímetro con registro quincenal; nunca rodenticida dentro del área de producto |
| Químicos y residuos | Sanitizantes/nutrientes en anaquel separado, etiquetados; bote de basura con tapa y pedal; charolas contaminadas (fusarium) fuera el mismo día |
| Almacenamiento y transporte | Producto terminado 1–4 °C; entregas en hielera limpia y exclusiva para producto; no transportar junto a químicos/gasolina |
| Capacitación y registros | Curso "Manejo Higiénico de Alimentos" (en línea, varios proveedores; el estándar del sector es el que exige el Distintivo H) para ti y cualquier ayudante; conservar TODAS las bitácoras ≥12 meses |
| Trámite | **Aviso de Funcionamiento COFEPRIS** (gratuito, se presenta una vez): te vuelve proveedor formal y es lo primero que pide el área de compras de un hotel |

---

### 5. Sistema de trazabilidad por lote (diseño listo para implementar)

**Codificación de lote (una línea, legible por humanos):**

```
[VARIEDAD 3 letras]-[AAMMDD siembra]-[lote semilla]-[posición]
Ejemplo:  GIR-260914-S047-R2N3
          girasol · sembrado 14-sep-2026 · costal semilla S047 · rack 2, nivel 3
```

- `S047` = tu consecutivo interno de costal, ligado en el "registro de semilla" al proveedor, su número de lote y su COA. Así un problema se rastrea **hacia atrás** (qué costal) y **hacia adelante** (qué clientes) en minutos.
- El lote va escrito en cinta masking sobre la charola el día de siembra y se copia a la etiqueta al empacar.

**Qué registrar por charola (una fila en Google Sheets o, mejor, en tu Home Assistant — ya tienes la infraestructura):**

| Campo | Ejemplo |
|---|---|
| Código de lote | GIR-260914-S047-R2N3 |
| Variedad y proveedor de semilla + lote del proveedor | Girasol negro, [proveedor], lote 2026-08-B12 |
| Sanitización de semilla | H₂O₂ 3%, 60 °C, 5 min, operador AI |
| Remojo | 10 h, agua de garrafón |
| Sustrato (lote de paca de coco) | C-2026-07 |
| Fuente de agua de riego | Tinaco / pluvial filtrada |
| Fechas: siembra / destape / cosecha | 14-sep / 18-sep / 24-sep |
| Rendimiento (g) y merma | 410 g, merma 0 |
| Incidencias | ninguna / mancha fusarium → charola desechada |
| Destino (cliente + factura/remisión) | Restaurante X, remisión 0231 |
| Temperatura a la entrega | 3.8 °C (sensor de la hielera) |

Automatización barata: un QR por charola impreso el día de siembra que apunta al formulario; el ESP32 ya te da temperaturas históricas para anexar al lote (los chefs valoran el dashboard — el plan ya lo contempla como material de venta).

**Machote de etiqueta B2B (clamshell/bolsa, 7×5 cm):**

```
MICROGREEN DE GIRASOL — [MARCA]
Lote: GIR-260914-S047-R2N3
Cosechado: 24-sep-2026   Consumir antes de: 01-oct-2026
Peso neto: 100 g   Conservar de 1 a 4 °C
Producto cultivado sin agroquímicos. Se recomienda
enjuagar y desinfectar antes de consumir.
Productor: [Nombre/razón social] · CDMX
Tel/WhatsApp: [__] · [correo]
```

- La leyenda de enjuague te protege legalmente sin arruinar el argumento de venta.
- Conserva **contramuestra fotográfica** de cada entrega (foto de charolas + etiqueta) y registros 12 meses.
- **Simulacro de retiro (mock recall) 1 vez al año:** elige un lote al azar y demuestra en <2 h a qué clientes llegó y de qué costal salió; documéntalo — es una pregunta estándar de auditoría de hoteles.
- Referencia internacional: en EE. UU. la regla de trazabilidad FSMA 204 pone a los germinados y hojas frescas en la lista de alta prioridad con requisitos de lote muy similares a este diseño; adoptarlo te deja listo si algún cliente exportador/corporativo lo pide.

---

### 6. Qué documentación piden hoteles, grupos restauranteros y distribuidores

Los portales de proveedores de Grupo Presidente, City Express (hoy operado con Marriott) y La Europea **no publican requisitos abiertos** (verificado hoy: sus sitios no exponen la documentación; el flujo real es vía el área de compras). Lo que sí está documentado y es el estándar del mercado:

1. **Distintivo H (SECTUR/Salud, norma NMX-F-605-NORMEX vigente 2018):** es la certificación de manejo higiénico que portan los restaurantes de hotel y cadenas. Su lista de verificación obliga al establecimiento a demostrar **control de proveedores**: en la práctica el chef/gerente de compras te pedirá evidencia de que eres "proveedor confiable" = análisis microbiológicos recientes, bitácoras y visita a tus instalaciones. NORMEX es el organismo que la respalda (verificado hoy: https://www.normex.com.mx/ · tel. 55 5598 3036; su área de inocuidad certifica además **NOM-251/BPM, HACCP, GLOBALG.A.P. y PrimusGFS**: https://www.normex.com.mx/inocuidad.php). La página informativa de SECTUR en gob.mx respondió 404 hoy — verificar URL vigente.
2. **Paquete documental estándar que te pedirá un hotel o grupo (prepáralo como PDF único de 8–10 páginas):**
   - Constancia de Situación Fiscal + facturación CFDI 4.0 (tus empresas ya lo cubren).
   - **Aviso de Funcionamiento COFEPRIS** de tu unidad de producción.
   - **Resultados de laboratorio** de producto (mesófilos, E. coli, *Salmonella*) y de agua, con antigüedad <6 meses, idealmente de lab con EMA/Tercero Autorizado (Quibimex encaja perfecto).
   - Ficha técnica por producto (variedad, presentación, vida de anaquel, condiciones de conservación, foto).
   - Carta de garantía de inocuidad + descripción de tu sistema de lotes y política de retiro (sección 5).
   - Evidencia de capacitación en Manejo Higiénico de Alimentos.
   - Algunos corporativos: póliza de responsabilidad civil de producto (aprox. $3,000–6,000/año con aseguradoras mexicanas; cotizar) y alta como proveedor con días de crédito 30–60.
3. **Retail/distribuidores (Chedraui, La Europea):** además de lo anterior piden alta en su portal de proveedores, **código de barras GS1 México**, y para frescos suelen exigir certificación de campo tipo **PrimusGFS o GLOBALG.A.P.** — no lo necesitas para restaurantes; considéralo solo si en Fase 3 buscas retail. CANIRAC (https://canirac.org.mx/, verificado activo) publica guías del sector restaurantero útiles para hablar el idioma del cliente.
4. **Ventaja competitiva real detectada:** casi ningún microproductor de microgreens en CDMX llega con carpeta de inocuidad + dashboard de monitoreo 24/7. Con $1,500–2,500 de análisis iniciales + el Aviso COFEPRIS gratuito te diferencias de inmediato y justificas precio premium.

---

### 7. Tabla consolidada de proveedores/recursos

| Nombre | Qué | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Laboratorio Quibimex (Iztapalapa) | Análisis micro de alimentos/superficies, auditorías | Cotizar (WhatsApp 56 1002 6942) | https://laboratorioquibimex.com/ | EMA A-012-001/12; COFEPRIS TA-28-19 en renovación; el mejor balance cercanía/acreditación |
| LANISAF – UACh (Texcoco) | E. coli en agua | $542–607/muestra (verificado, catálogo mar-2026) | https://lanisaf.chapingo.mx/ | Económico para monitoreo; no EMA; resultados ≤12 días hábiles |
| Agrolab (FS Lab/WTR Lab) | Paquetes micro alimentos/agua/superficies, sector hotelero | Cotizar: info@agrolab.com.mx | https://agrolab.com.mx/ | +20 oficinas de recolección; confirmar punto CDMX |
| Eurofins México | Patógenos e indicadores en alimentos | Cotizar | https://www.eurofins.com.mx/agro-alimentario/microbiolog%C3%ADa/ | Red global; dirección MX por confirmar |
| LAE Lab. Analítico Especializado (GAM) / Bioquality (Cuautitlán Izcalli) | Análisis de alimentos (económicos) | Cotizar: 55 5771 5439 / 55 5871 1227 | https://www.seccionamarilla.com.mx/resultados/laboratorios-de-analisis-de-alimentos/distrito-federal/1 | Sin web propia verificada; validar acreditación por teléfono |
| EMA | Padrón de laboratorios acreditados | — | https://www.ema.org.mx/portal_v3/ | Verificar acreditación de cualquier lab |
| NORMEX | Distintivo H / NOM-251 / HACCP / PrimusGFS | Cotizar: 55 5598 3036 | https://www.normex.com.mx/inocuidad.php | Para cuando un corporativo exija certificación |
| FDA – guía semilla para germinar (2022) | Protocolo/marco de sanitización de semilla | — | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-reducing-microbial-food-safety-hazards-production-seed-sprouting | Fuente técnica primaria |
| Sprout Safety Alliance (Illinois Tech) | Manual gratuito *Safer Sprout Production*, video de tratamiento de semilla | Gratis | https://www.iit.edu/ssa | Capacitación autodidacta |
| NOM-251-SSA1-2009 (texto oficial) | Prácticas de higiene obligatorias | — | https://sidof.segob.gob.mx/notas/5133449 | Base del cuarto de cosecha |
| Mercado Libre (búsquedas) | Hipoclorito de calcio 65% / H₂O₂ 35% / peracético / Petrifilm | aprox. $150–350/kg · $180–400/L · $400–900/L · $40–70/placa | https://listado.mercadolibre.com.mx/hipoclorito-de-calcio · https://listado.mercadolibre.com.mx/peroxido-de-hidrogeno-grado-alimenticio · https://listado.mercadolibre.com.mx/acido-peracetico · https://listado.mercadolibre.com.mx/petrifilm | ML bloqueó el fetch hoy: precios aprox. de mercado |
| Hydro Environment (CDMX) | Charolas, equipo de cultivo | Charola $117–129 (verificado) | https://www.hydroenv.com.mx/ | Tel. 55-5565-1153; no vende sanitizantes |
| Reactivos Meyer (CDMX) | Reactivos químicos (H₂O₂ grados técnicos) | Cotizar | https://www.reactivosmeyer.com.mx/ | Fabricante nacional |

---

### Recomendación concreta

**Compra esta semana (~$700 MXN):**
1. 2 frascos de agua oxigenada 3% de farmacia (~$60) → protocolo Opción B para las primeras siembras de girasol/chícharo + desinfección de charolas y tijeras.
2. 1 kg de hipoclorito de calcio 65% "cloro granular para alberca" (~$250 aprox., Mercado Libre o tienda de albercas) + báscula de 0.1 g que ya tienes → deja montada la Opción A (31 g/L, 15 min, triple enjuague) para cuando un cliente hotelero pida el estándar duro.
3. Termómetro de cocina (~$150) para el precalentado a 60 °C y para registrar temperatura de entregas.
4. Rollo de masking + plumón indeleble: arranca HOY la codificación `VAR-AAMMDD-Slote-pos` y la hoja de registro por charola (sección 5). Costo cero y es lo que más valor B2B genera.

**En Fase 1 (cuando haya 2 clientes fijos, ~$2,500):**
5. Llama a **Quibimex** (55 5445 5496 / WA 56 1002 6942): cotiza paquete "producto: mesófilos + E. coli + Salmonella" y "agua: coliformes + E. coli"; pide confirmar vigencia de su EMA y TA COFEPRIS. Un solo informe con membrete acreditado te abre puertas de hotel.
6. Manda en paralelo una muestra de agua a **LANISAF ($542)** como monitoreo económico recurrente.
7. Presenta el **Aviso de Funcionamiento COFEPRIS** (gratuito) y toma un curso en línea de Manejo Higiénico de Alimentos.
8. Arma la **carpeta de inocuidad PDF** (sección 6) y súbela al mismo dashboard que enseñas a los chefs.

**Por qué así:** el riesgo real del negocio está concentrado en girasol/chícharo remojados; H₂O₂ 3% + higiene NOM-251 + lotes trazables cubren el 90% del riesgo por menos de $1,000, y el análisis acreditado de Quibimex convierte la inocuidad de un costo en tu principal argumento de venta frente a hoteles con Distintivo H.

---

### Gaps / pendientes de verificación humana
- FDA bloqueó el fetch de la guía de 1999 (*...sprouted seeds*, HTTP 401) y eCFR 21 CFR 112 Subparte M (redirect anti-bot): confirmar en navegador la cifra de 20,000 ppm y §112.142(e). URLs en la lista de verificación.
- Publicación UC ANR 8151 (*Growing Seed Sprouts at Home*): el catálogo migró a anrpublications.org; confirmar el protocolo de H₂O₂ 3% a 60 °C/5 min y conseguir el PDF.
- Mercado Libre bloqueó el scraping: todos los precios de químicos son aproximados de mercado.
- Precios por muestra de Quibimex, Agrolab y Eurofins: solo por cotización directa (los rangos de la sección 3 son estimaciones de mercado, no verificadas).
- Estado real (vigente/renovación) del Tercero Autorizado TA-28-19 de Quibimex.
- Dirección física y acreditación EMA del laboratorio de Eurofins en México; oficina de recolección de Agrolab en CDMX.
- Requisitos formales de proveedores de Grupo Presidente/City Express/La Europea/Chedraui: no públicos; la sección 6 refleja la práctica estándar del sector — validar con el primer comprador real.
- Página oficial de Distintivo H en gob.mx respondió 404; verificar URL vigente y el texto de la NMX-F-605-NORMEX-2018 (de pago en NORMEX).
- OMAFRA retiró su factsheet de microgreens (404 verificado); Cornell/PSU no exponen una página específica de sanitización de semilla para microgreens que haya podido abrir hoy — el marco FDA/SSA la sustituye bien.
