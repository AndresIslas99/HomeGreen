# Hueco 2 — Continuidad eléctrica del NFT e instalación eléctrica exterior segura

**Proyecto:** Huerto comercial automatizado, patio 80 m², CDMX (microgreens + hierbas NFT, ESP32/ESPHome/Home Assistant)
**Fecha de investigación:** 12 de septiembre de 2026
**Nota metodológica:** El presupuesto de WebSearch de esta sesión estaba agotado, así que toda la evidencia proviene de ~20 páginas abiertas directamente con WebFetch (Steren, Cyberpuerta, Home Depot MX, DOF, Cronoshare, Programa Casa Segura). Mercado Libre y Amazon MX bloquearon el acceso desde este entorno (403/503): los precios que dependen de ellos van marcados **"aprox."** y con URL de búsqueda para que un verificador los confirme. Los precios de Home Depot MX se muestran en su HTML como enteros con centavos pegados (p. ej. `24900` = $249.00); donde apliqué esa interpretación lo señalo.

---

### 1. El problema: por qué esto es la falla de diseño más peligrosa del plan

- En **NFT no hay sustrato ni columna de agua**: las raíces cuelgan en una película de 1–3 mm. Si la recirculación se detiene, la película se drena en minutos y las raíces quedan al aire. Con el túnel a 25–35 °C, el punto de marchitez irreversible llega en **2–4 horas** (regla estándar del gremio hidropónico; en días nublados y frescos puede estirarse a 6–8 h, pero no se diseña para el mejor caso). Un corte de CFE de una tarde = perder 6–8 líneas de albahaca que representan $6,000–10,000/mes de ingreso.
- El plan además coloca **relés, fuentes 12 V y una bomba 120 V en un patio que se moja** (lluvia mayo–octubre, riego, tinacos) **sin GFCI, sin tierra física y sin gabinetes IP65**. Agua + 127 VCA + manos húmedas es el escenario clásico de electrocución doméstica; y una fuente barata goteada es el escenario clásico de incendio.
- Ninguna fase del plan presupuesta esto. Este informe lo dimensiona y lo cotiza: el paquete completo (respaldo + seguridad) cuesta **~$9,500–13,500 MXN**, es decir, menos que perder un solo mes de ventas de hierbas.

---

### 2. Dimensionamiento del respaldo: ¿cuánta batería se necesita?

#### 2.1 Carga a respaldar

Para 6–8 líneas NFT se necesitan ~1–2 L/min por canal → **8–16 L/min a 1–2 m de columna**. Eso lo entrega una bomba chica; el 0.5 HP del plan está sobrado para recircular (se justifica solo para llenado/purga/retorno largo).

#### 2.2 Escenario A — Bomba periférica 0.5 HP 120 VCA + inversor (la del plan)

| Parámetro | Valor |
|---|---|
| Consumo eléctrico real 0.5 HP | ~500–600 W (tomo 550 W) |
| Pico de arranque (inrush) | 3–6× nominal → 1,650–3,300 VA |
| Eficiencia inversor | ~85% → **~650 W desde batería** |
| Energía 8 h | ~5.2 kWh |
| Energía 12 h | ~7.8 kWh |
| Banco 12 V necesario (12 h, LiFePO4 90% DoD) | **~680 Ah nominales** (7 baterías de 100 Ah) |
| Costo solo baterías (Epcom 100 Ah × 7) | ~$31,000 MXN |
| Inversor requerido | ≥1,500 W onda senoidal pura (los de onda modificada maltratan motores de inducción); el Steren INV-1500 ($2,842) es onda modificada |

**Veredicto: inviable.** Incluso con ciclo 50% ON/OFF necesitarías ~340 Ah (~$14,000 solo en baterías). Y un UPS comercial de 800 VA ni siquiera arranca el motor (inrush > capacidad) y con 480 W de carga su batería interna de 9 Ah daría **5–8 minutos**.

#### 2.3 Escenario B — Bomba 12 V DC de 30–60 W directa a batería (recomendado)

| Parámetro | Valor |
|---|---|
| Bomba 12 V (diafragma o centrífuga) | 40 W típico → 3.3 A @ 12 V |
| Energía 12 h continuas | 480 Wh → **~38–40 Ah** |
| LiFePO4 50 Ah (90% DoD útil) | ~13–14 h continuas |
| **LiFePO4 100 Ah** (90% DoD útil) | **~28–30 h continuas** |
| AGM 100 Ah (50% DoD sano) | ~15 h continuas |
| Con "modo supervivencia" 15 min ON / 15 min OFF (NFT lo tolera: la película y la esponja retienen humedad entre ciclos) | consumo a la mitad → LiFePO4 100 Ah ≈ **2.5 días** |

**Veredicto: ganador absoluto.** Sin inversor, sin pérdidas de conversión, sin problema de arranque, y la batería necesaria cuesta 7 veces menos.

#### 2.4 Arquitectura recomendada: "DC-first" (topología de sistema de alarma / DC-UPS)

```
CFE 127V ──[GFCI]──> Cargador/fuente en flotación ──┬──> Bomba NFT 12V (24/7)
                                                    │
                               LiFePO4 12.8V 100Ah ─┤    (la batería está SIEMPRE en paralelo:
                                                    │     el corte de CFE ni se nota, cero conmutación)
                                                    ├──> Nodo ESP32 del patio (siempre vivo)
                                                    └──> [opcional] Controlador solar <── Panel 100 W
```

- La bomba NFT **normal** pasa a ser la de 12 V; corre 24/7 desde el bus de batería flotada. La periférica 0.5 HP 120 V se conserva solo para llenado/purga/transferencia de tinaco (tarea no crítica que puede esperar al regreso de la luz).
- Redundancia barata: **dos bombas 12 V** (una instalada, una de repuesto en el estante o en paralelo con válvula check). Dos bombas DC cuestan menos que un solo inversor senoidal puro.
- El ESP32 del NFT se alimenta del mismo bus → sigue reportando a Home Assistant durante el corte (el router y la Raspberry se respaldan con un mini UPS, sección 4).

---

### 3. Cotizaciones CDMX (septiembre 2026)

#### 3.1 Baterías

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Cyberpuerta | **Epcom LI100A12PRO — LiFePO4 12.8 V 100 Ah** | **$4,459** | https://www.cyberpuerta.mx/index.php?cl=search&searchparam=bateria+LiFePO4 | Verificado 12-sep-2026. Entrega a CDMX 3–7 días. **La pieza central recomendada.** |
| Cyberpuerta | EPEVER LFP100EP128V2 — LiFePO4 12.8 V 100 Ah | $5,499 | (misma búsqueda) | Verificado. Alternativa de marca. |
| Mercado Libre | LiFePO4 12 V 50–60 Ah genéricas | aprox. $2,300–3,200 | https://listado.mercadolibre.com.mx/bateria-lifepo4-12v-100ah | ML bloqueó el acceso desde este entorno (403); precio de referencia de mercado, **verificar**. |
| Mercado Libre | AGM/ciclo profundo 12 V 100 Ah (LTH, Época, etc.) | aprox. $3,000–4,500 | https://listado.mercadolibre.com.mx/bateria-agm-ciclo-profundo-12v-100ah | No verificado (403). AGM = 40% más barata pero mitad de ciclo de vida y 50% DoD. |
| Steren | BR-1224 sellada plomo-ácido 12 V 24 Ah | $1,290 | https://www.steren.com.mx/catalogsearch/result/?q=bateria+sellada | Verificado. Solo alcanza para "modo supervivencia" ~7 h; útil como respaldo mínimo de arranque del proyecto. |
| Steren | BR-1212 12 V 12 Ah / BR-1207 12 V 7 Ah | $695 / $495 | (misma búsqueda) | Verificado. Para el nodo ESP32, no para la bomba. |

#### 3.2 Cargadores / mantenedores

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Steren | **BR-700** cargador inteligente 12 V (plomo-ácido sellada) | $406–495 | https://www.steren.com.mx/catalogsearch/result/?q=cargador+de+bateria+12v | Verificado (el rango refleja precio con/sin descuento visto en dos páginas). Ideal si eliges AGM. |
| Steren | BR-510 cargador 6/12 V | $359.60–449 | (misma búsqueda) | Verificado. |
| Mercado Libre | Cargador específico LiFePO4 14.6 V 10–20 A | aprox. $700–1,400 | https://listado.mercadolibre.com.mx/cargador-lifepo4-14.6v-10a | No verificado (403). Para LiFePO4 conviene cargador con perfil correcto (14.4–14.6 V absorción, flotación ≤13.6 V); muchos usan el controlador solar (3.4) como cargador dual. |

#### 3.3 Inversores (solo si se insistiera en respaldar cargas 120 V)

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Steren | INV-400 (400 W, 12→110 V) | $870 | https://www.steren.com.mx/catalogsearch/result/?q=inversor+12v | Verificado. Onda modificada. |
| Steren | **INV-600** (600 W) | $1,218 | (misma búsqueda) | Verificado. Suficiente para cargas resistivas/electrónica, **no** para arrancar la periférica 0.5 HP. |
| Steren | INV-1000 / INV-1500 | $2,030 / $2,842 | (misma búsqueda) | Verificado. Aun el INV-1500 es onda modificada: mala pareja para motor de inducción; se descarta la vía inversor para la bomba. |

#### 3.4 UPS comerciales (para el "cerebro", no para la bomba)

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Cyberpuerta | DataShield DS-600 (600 VA / 360 W) | $1,189 | https://www.cyberpuerta.mx/index.php?cl=search&searchparam=DataShield+UPS | Verificado. Con Raspberry Pi + módem (~25–35 W) da ~45–90 min: suficiente para avisar y apagar limpio. |
| Cyberpuerta | **DataShield KS800PRO** (800 VA / 480 W) | $1,859 | (misma búsqueda) | Verificado. Trae puerto de comunicación → integrable a HA vía NUT para detectar el corte. |
| Cyberpuerta | DataShield KS-1000PRO (1,000 VA / 600 W) | $2,489 | (misma búsqueda) | Verificado. |
| Steren | NB-605 (600 VA) / NB-900 (900 VA) / NB-1500 (1,500 VA) | $1,160 / $1,970 / $2,436 | https://www.steren.com.mx/catalogsearch/result/?q=no+break | Verificado. Alternativa con tienda física en CDMX. |

**Conclusión UPS:** un UPS comercial NUNCA sustituye al banco de batería de la bomba (5–8 min de autonomía con 480 W y no arranca motores), pero uno de $1,189–1,859 es la forma más barata y limpia de mantener vivo router + Raspberry (Home Assistant) para que las alertas salgan durante el corte.

#### 3.5 Solar como respaldo (evaluación)

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Cyberpuerta | **Ugreen 15113 panel plegable 100 W** (19 V, mono) | $1,049 + $158 envío | https://www.cyberpuerta.mx/index.php?cl=search&searchparam=panel+solar+100W | Verificado, 142 pzas en stock. Un panel rígido 100–150 W de instalación fija en ML anda en aprox. $1,200–2,000 (no verificado, 403). |
| Cyberpuerta | **Epsolar (EPEVER) LS2024B** controlador PWM 20 A | $599 | https://www.cyberpuerta.mx/index.php?cl=search&searchparam=controlador+de+carga+solar | Verificado. Con perfil LiFePO4 configurable. |
| Cyberpuerta | Victron BlueSolar MPPT 100/20 | $1,249 (según listado; **verificar**, precio inusualmente bajo para Victron) | (misma búsqueda) | Aparece en el listado; los MPPT Victron suelen costar $2,000–3,000. Marcar aprox. |
| Cyberpuerta | Morningstar SHS-10 (10 A) | $909 | (misma búsqueda) | Verificado. |

**Números:** CDMX tiene ~5.0–5.5 horas solares pico. Un panel de 100 W produce ~450–500 Wh/día reales; la bomba de 40 W corriendo 24/7 consume ~960 Wh/día → **un panel de 100 W NO sostiene la operación continua** (se necesitarían 250–300 W), pero **como cargador de respaldo es excelente**: mantiene la batería flotada sin depender de CFE, y en un corte diurno alimenta la bomba directamente, estirando la autonomía de 30 h a varios días.

**Veredicto:** por +$1,650–2,000 (panel 100 W + LS2024B + cable/soporte) frente a +$400–500 de un cargador AC, el solar es **competitivo como upgrade de resiliencia** (cortes multi-día, apagones de zona) y elimina un cargador de la lista si el controlador hace ambas funciones. Recomendado como "Fase 2.5", no indispensable el día 1.

#### 3.6 Protección eléctrica: GFCI, tierra física, intemperie

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Home Depot MX | **Contacto dúplex GFCI Square D 15 A** (blanco/negro/aluminio) | **$389** | https://www.homedepot.com.mx/s/gfci | Verificado (aparece 3 veces al mismo precio). La opción calidad/precio. |
| Home Depot MX | Contactos dúplex GFCI Estevez (Unno/Gamma/Omega) | $239–489 | (misma búsqueda) | Verificado. Marca económica mexicana. |
| Home Depot MX | Contacto GFCI Leviton 15 A | $640 aprox.; un listado mostró $1,935 (oferta desde $2,575) que parece kit/producto premium | https://www.homedepot.com.mx/s/leviton%20gfci | Ambiguo en el HTML; **verificar en tienda**. Placas Leviton para GFCI: $61–71 (interpretación de precios en centavos). |
| Home Depot MX | **Breaker GFCI Square D QO115GFI / QO120GFI** (15/20 A) | $1,179 / $1,159 | https://www.homedepot.com.mx/s/interruptor%20falla%20a%20tierra | Verificado. Protege TODO el circuito del patio desde el centro de carga (mejor que contacto por contacto). |
| Home Depot MX | Breaker GFCI Bticino SBTP1C15R6 / C20R6 | $1,059 | (misma búsqueda) | Verificado. |
| Home Depot MX | **Tapa de exteriores VETO con contacto doble 2P+T** (tipo intemperie) | $249 (interpretación de `24900`) | https://www.homedepot.com.mx/s/tapa%20intemperie | Verificado el producto; precio interpretado del formato en centavos — marcar aprox. Placas intemperie Vimexpro $49–69; placa Leviton intemperie $165; Decora metal $155 (misma interpretación). |
| Home Depot MX | Varilla de tierra CMP 72.5 cm | $69 aprox. (listado muestra `6900`; interpretación en centavos) | https://www.homedepot.com.mx/s/varilla%20de%20tierra | El buscador de HD casi no indexa varillas. La estándar para NOM es 5/8" × 3 m. |
| Mercado Libre | Varilla copperweld 5/8" × 3 m + conector | aprox. $250–450 | https://listado.mercadolibre.com.mx/varilla-copperweld-5-8-3-metros | No verificado (403). También en cualquier tlapalería/CFE-materiales de CDMX. Kit con intensificador de tierra (GEM) aprox. +$250–400. |

#### 3.7 Bomba 12 V DC (la pieza que falta en todas las tiendas grandes)

| Proveedor | Producto | Precio MXN | Enlace | Notas |
|---|---|---|---|---|
| Mercado Libre | **Bomba de diafragma 12 V 40–80 W** (4–6 L/min, presurizada, tipo SEAFLO/genérica) | aprox. $350–900 | https://listado.mercadolibre.com.mx/bomba-diafragma-12v | No verificado (403). Es el estándar de facto en México para autolavados/campers; entrega el caudal/altura que el NFT necesita. Comprar 2. |
| Mercado Libre | Bomba sumergible 12 V tipo "bilge" 1100 GPH | aprox. $250–500 | https://listado.mercadolibre.com.mx/bomba-sumergible-12v-1100gph | No verificado (403). Mucho caudal, poca altura (≤2 m): sirve si el depósito está al pie de las líneas. |
| Steren | Micro bomba MOT-300 (80–120 L/h) | $35.96–49 | https://www.steren.com.mx/catalogsearch/result/?q=bomba+de+agua | Verificado. **Insuficiente** para el NFT (solo demo/dosificación); se lista para descartarla explícitamente. |
| Home Depot MX | Bomba presurizadora SUPER 70 W | $597 | https://www.homedepot.com.mx/s/bomba%2012v | Verificado, pero es 127 V; HD no tiene bombas 12 V útiles. |

#### 3.8 Mano de obra: electricista certificado en CDMX

| Concepto | Precio MXN | Fuente | Notas |
|---|---|---|---|
| Instalación eléctrica completa (referencia mayor) | $200–270 por m² (rango nacional $150–350) | https://www.cronoshare.com.mx/cuanto-cuesta/instalacion-electrica (verificado) | Solo como referencia de escala; no aplica directo al patio. |
| Visita + medio día de electricista certificado (CDMX) | **aprox. $800–1,500** | Rango de mercado; Cronoshare no publica tarifa por jornada en la página verificada | **Verificación humana recomendada**: pedir 2–3 cotizaciones (apps: Cronoshare, jobs locales). |
| Instalación de tierra física completa (varilla + soldadura/conector + cable desnudo cal. 8 + puente al centro de carga) | aprox. $1,500–3,500 llave en mano | mercado | Incluye material menor. Si el electricista mide con telurómetro, mejor. |
| Instalar breaker GFCI en centro de carga + contacto intemperie en patio | aprox. $500–900 de mano de obra | mercado | Trabajo de 2–3 h. |

---

### 4. Qué exige la NOM-001-SEDE-2012 (nivel divulgativo, no es asesoría legal)

Fuente primaria verificada: texto de la norma en el DOF — https://dof.gob.mx/nota_detalle.php?codigo=5280607&fecha=29/11/2012 (confirmado que es la NOM-001-SEDE-2012, "Instalaciones Eléctricas (utilización)", 29-nov-2012). La norma sigue la estructura del NEC estadounidense. Recurso divulgativo adicional: Programa Casa Segura (https://programacasasegura.org), programa mexicano de educación en seguridad eléctrica.

Lo relevante para un patio-huerto (los números de artículo se citan de memoria sobre la estructura tipo NEC de la norma; el texto DOF verificado confirma las definiciones y principios — un verificador puede confirmar numeración exacta):

1. **GFCI obligatorio en exteriores (Art. 210-8):** los contactos de 15/20 A y 127 V instalados en exteriores, azoteas, y en general donde hay agua, deben tener protección de falla a tierra (ICFT/GFCI) que corta en ~5 mA de fuga. La propia norma define el "interruptor de circuito por falla a tierra" como dispositivo que desenergiza el circuito cuando la corriente a tierra excede un valor predeterminado (definición confirmada en el texto DOF).
2. **Lugares mojados (Art. 406, definición confirmada en DOF):** un patio expuesto a lluvia/riego es "lugar mojado" (instalaciones "sometidas a saturación con agua"). Los contactos ahí requieren **cubierta a prueba de intemperie que mantenga la protección con la clavija conectada** (tapa tipo "in-use"/burbuja, como la VETO cotizada) y contactos resistentes a intemperie (marcado WR).
3. **Equipo apto para el ambiente (Art. 110-11, confirmado en DOF):** equipo no identificado para ambientes húmedos/corrosivos necesita protección adicional → las fuentes 12 V, relés y ESP32 van dentro de **gabinete IP65/NEMA 3R-4X** con prensaestopas, nunca "al aire".
4. **Puesta a tierra (Art. 250):** la norma la llama "principio fundamental de seguridad" (texto DOF). En la práctica: electrodo de tierra (varilla copperweld típica de 3 m), conductor de puesta a tierra hasta el centro de carga, y **resistencia ≤25 Ω para electrodo único** (si no se logra, segunda varilla). Todos los contactos del patio con terminal de tierra conectada de verdad.
5. **Implicación práctica para el proyecto:** breaker GFCI QO en el centro de carga para el circuito del patio ($1,159–1,179) **o** contacto GFCI aguas arriba de todo lo del patio ($389); tierra física real; extensión/cableado tipo uso rudo SJT/ST; todo empalme dentro de caja; bus 12 V y 127 V en gabinetes separados.

> Nota honesta: la NOM aplica formalmente vía UVIE (Unidades de Verificación) a instalaciones nuevas/comerciales; en una casa nadie te va a inspeccionar el patio. Se cumple porque **es lo que evita electrocutar a alguien con las manos mojadas**, no por el trámite. Como negocio de alimentos que recibirá visitas de chefs/clientes, el estándar además protege la responsabilidad civil.

---

### 5. Lógica de alerta en Home Assistant: "corte de luz + bomba parada"

Hardware que ya está en el plan: sensor de flujo **YF-S201** ($120, Fase 2) y ESP32. Se agregan dos cosas casi gratis: (a) el nodo ESP32 del NFT se alimenta del **bus de batería** (siempre vivo), (b) un **detector de presencia de red**: una fuente USB de 5 V conectada a la red del patio alimenta, a través de un optoacoplador o divisor, un GPIO del ESP32 — si hay 127 V, el pin está en alto. (Alternativa sin soldar: integrar el UPS DataShield/Steren por USB con la integración **NUT** de Home Assistant y usar su estado "OnBattery".)

#### 5.1 ESPHome (nodo NFT alimentado por batería)

```yaml
sensor:
  - platform: pulse_counter
    pin: GPIO27
    id: flujo_nft
    name: "Flujo NFT"
    unit_of_measurement: "L/min"
    update_interval: 10s
    filters:
      - lambda: return x / 450.0;   # YF-S201 ≈ 450 pulsos/litro
  - platform: adc
    pin: GPIO34
    id: v_bateria
    name: "Voltaje bateria NFT"
    attenuation: 12db
    update_interval: 30s
    filters:
      - multiply: 5.7               # divisor 47k/10k para leer hasta ~18 V

binary_sensor:
  - platform: gpio
    pin: { number: GPIO26, mode: INPUT_PULLDOWN }
    id: red_cfe
    name: "Red CFE presente"
    device_class: power
    filters: [ delayed_off: 5s, delayed_on: 5s ]

switch:
  - platform: gpio
    pin: GPIO25
    id: bomba_nft
    name: "Bomba NFT"
    restore_mode: RESTORE_DEFAULT_ON   # tras reinicio, la bomba SIEMPRE enciende
  - platform: gpio
    pin: GPIO33
    id: bomba_respaldo
    name: "Bomba NFT respaldo"
```

#### 5.2 Automatizaciones en Home Assistant

```yaml
# 1) CRÍTICA: bomba comandada ON pero sin flujo (bomba muerta, tapada o línea rota)
- alias: "NFT - bomba sin flujo"
  trigger:
    - platform: numeric_state
      entity_id: sensor.flujo_nft
      below: 2            # L/min, umbral según tus líneas
      for: "00:02:00"
  condition:
    - condition: state
      entity_id: switch.bomba_nft
      state: "on"
  action:
    - service: switch.turn_on
      target: { entity_id: switch.bomba_respaldo }
    - service: notify.mobile_app_tu_cel
      data:
        title: "🚨 NFT SIN FLUJO"
        message: "Bomba ON pero flujo {{ states('sensor.flujo_nft') }} L/min. Respaldo activado. Raíces mueren en 2-4 h."
        data: { push: { interruption-level: critical } }   # iOS; en Android usar channel + importance high

# 2) Corte de CFE (aviso temprano, aunque la bomba siga en batería)
- alias: "NFT - corte de luz"
  trigger:
    - platform: state
      entity_id: binary_sensor.red_cfe_presente
      to: "off"
      for: "00:00:30"
  action:
    - service: notify.mobile_app_tu_cel
      data:
        title: "⚡ Corte de luz en el patio"
        message: "NFT corriendo en batería ({{ states('sensor.voltaje_bateria_nft') }} V). Autonomía estimada 24-30 h."

# 3) Escalación: corte + sin flujo = emergencia real (repite cada 10 min con 'alert')
alert:
  nft_emergencia:
    name: "NFT parado durante apagón"
    entity_id: binary_sensor.nft_emergencia   # template: red_cfe off AND flujo < 2
    state: "on"
    repeat: 10
    notifiers: [ mobile_app_tu_cel ]
    # opcional: acción adicional con llamada vía CallMeBot/Twilio

# 4) Modo supervivencia: batería baja durante corte -> ciclar bomba 15/15 min
- alias: "NFT - modo ahorro en corte"
  trigger:
    - platform: numeric_state
      entity_id: sensor.voltaje_bateria_nft
      below: 12.9          # LiFePO4 ~30-40% restante
      for: "00:05:00"
  condition:
    - condition: state
      entity_id: binary_sensor.red_cfe_presente
      state: "off"
  action:
    - service: script.turn_on
      target: { entity_id: script.ciclo_bomba_15_15 }

# 5) Watchdog: el nodo dejó de reportar (se cayó WiFi/ESP32) -> también es alarma
- alias: "NFT - nodo caído"
  trigger:
    - platform: state
      entity_id: sensor.flujo_nft
      to: "unavailable"
      for: "00:05:00"
  action:
    - service: notify.mobile_app_tu_cel
      data: { title: "⚠️ Nodo NFT sin señal", message: "Sin datos 5 min. Verifica en sitio." }
```

Puntos de diseño: (a) el **fail-safe es físico, no de software** — la bomba 12 V está cableada al bus de batería y `restore_mode: RESTORE_DEFAULT_ON` garantiza que un reinicio del ESP32 la deje encendida; Home Assistant solo *avisa* y *optimiza*, no es requisito para que el agua circule; (b) el router + Raspberry van al UPS DataShield para que las notificaciones salgan durante el corte; (c) prueba mensual: botar el breaker del patio 10 min y verificar que llegan las 2 alertas.

---

### 6. BOM consolidado del hueco (respaldo + seguridad)

| # | Partida | Opción recomendada | Precio MXN | Estado |
|---|---|---|---|---|
| 1 | Batería | Epcom LiFePO4 12.8 V 100 Ah (Cyberpuerta) | $4,459 | Verificado |
| 2 | Bomba NFT 12 V 40–60 W ×2 (principal + respaldo) | Diafragma tipo SEAFLO (ML) | aprox. $900–1,800 | Aprox. (ML 403) |
| 3 | Cargador flotador | Controlador solar EPEVER LS2024B como cargador DC (con panel) **o** cargador LiFePO4 ML | $599 / aprox. $700–1,400 | Verif. / aprox. |
| 4 | Panel solar 100 W (opcional recomendado) | Ugreen 15113 (Cyberpuerta) | $1,049 + envío | Verificado |
| 5 | UPS para Raspberry + router | DataShield DS-600 | $1,189 | Verificado |
| 6 | Protección GFCI | Breaker Square D QO120GFI (todo el circuito del patio) o contacto Square D | $1,159 / $389 | Verificado |
| 7 | Contacto + tapa intemperie | VETO tapa exterior con contacto | aprox. $249 | Verif. producto, precio interpretado |
| 8 | Tierra física | Varilla copperweld 5/8"×3 m + conector + cable cal. 8 | aprox. $400–800 material | Aprox. |
| 9 | Gabinete IP65 + prensaestopas + fusiblera 12 V + cable | Genérico ML/tlapalería | aprox. $500–900 | Aprox. |
| 10 | Electricista certificado (GFCI + tierra + contacto exterior, medio día–día) | Local, 2–3 cotizaciones | aprox. $1,500–3,500 llave en mano | Aprox. |
| | **Total con solar** | | **~$11,000–14,500** | |
| | **Total mínimo (sin solar, cargador AC, contacto GFCI en vez de breaker)** | | **~$8,500–11,000** | |

Variante ultra-austera de arranque (solo sobrevivir cortes de ≤7 h mientras llegan ventas): Steren BR-1224 (24 Ah, $1,290) + BR-700 ($406–495) + 1 bomba diafragma (aprox. $500) + contacto GFCI Estevez ($239) ≈ **$2,500–2,900**, ampliable después a la batería de 100 Ah sin tirar nada.

---

### Recomendación concreta

1. **Cambia la arquitectura de la bomba de recirculación: de 120 VCA a 12 VDC ("DC-first").** La bomba NFT de operación continua debe ser una de diafragma 12 V de 40–60 W colgada de un bus batería-flotada (compra 2: aprox. $900–1,800 por el par). La periférica 0.5 HP queda solo para llenado/purga. Respaldarla con inversor exigiría ~680 Ah y >$30,000: descartado con números.
2. **Compra la Epcom LiFePO4 12.8 V 100 Ah de Cyberpuerta ($4,459, verificado):** da 28–30 h de recirculación continua o ~2.5 días en modo 15/15, cubre cualquier corte realista de CFE en CDMX y dura 8–10 años. Si el flujo de caja no da, arranca con la Steren BR-1224 de 24 Ah ($1,290) y migra después.
3. **Agrega el panel Ugreen 100 W ($1,049) + EPEVER LS2024B ($599):** por ~$1,650 el controlador hace de cargador (elimina esa partida), la batería queda flotada sin depender de CFE y un corte diurno se vuelve indefinidamente sostenible en modo supervivencia. Es la única variante de "solar" que tiene sentido a esta escala; no intentes correr todo el huerto con solar.
4. **Seguridad antes que el primer relé en el patio:** breaker Square D QO120GFI ($1,159) para todo el circuito exterior (o mínimo el contacto GFCI Square D de $389 aguas arriba de todo), tapa intemperie tipo "in-use" (~$249), varilla copperweld 3 m con conector (~$400–800 en material) y electrónica en gabinete IP65. Contrata medio día de electricista certificado (aprox. $1,500–3,500 llave en mano con tierra física) — pide que deje ≤25 Ω medidos. Esto es lo que la NOM-001-SEDE-2012 exige para lugares mojados (DOF verificado) y lo que evita un accidente.
5. **UPS DataShield DS-600 ($1,189) para Raspberry + router**, y las 5 automatizaciones de la sección 5 (flujo YF-S201 + detector de red + watchdog + modo ahorro + escalación). Regla de oro: el software avisa, pero la continuidad del agua nunca depende de que Home Assistant esté vivo.
6. **Presupuesto total del hueco: ~$8,500–14,500 MXN.** Insértalo como partida obligatoria de la Fase 2 (antes de sembrar la primera línea NFT): es ~1 mes de ingreso esperado de las hierbas y elimina el único modo de falla que puede matar el 100% del cultivo en una tarde.
