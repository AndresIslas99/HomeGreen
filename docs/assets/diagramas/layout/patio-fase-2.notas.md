<!-- Generado por hardware/cad/layout.py. No editar a mano: se regenera con
     python3 hardware/cad/layout.py y se incrusta con pymdownx.snippets. -->

### Leyenda { data-toc-label="Leyenda · Fase 2" }

- **Línea azul continua** — agua a presión: red ½" · llenado.
- **Línea azul discontinua** — drenaje · rebosadero · purga → coladera.
- **Línea azul de raya y punto** — canalón / bajante pluvial (pendiente 0.5–1 %).
- **Línea ámbar continua** — 127 V CA (circuito GFCI del patio).
- **Línea ámbar discontinua** — 12 V CC (fuente / bus de batería).
- **Línea ámbar punteada** — señal de sensor · Wi-Fi.
- **Relleno verde claro con borde verde** — cultivo: rack · bancada NFT · cama.
- **Relleno crema con borde ámbar y aspa** — gabinete IP65 (GAB-x).
- **Relleno azul claro con borde azul** — tinaco TK-1 · tambo TK-2.
- **Rayado gris fino** — techo (túnel / cobertizo).
- **Línea gris discontinua** — reserva de una fase posterior.
- **Cuadro azul con retícula** — coladera.
- **Círculo azul con una T** — toma de agua.
- **Cuadro ámbar con dos barras** — contacto GFCI in-use.
- **Cuadro negro sólido** — columna PTR anclada.
- **Círculo numerado** — nota clave: su texto es la lista numerada de abajo.

### Notas clave { data-toc-label="Notas clave · Fase 2" }

1. Fachada sur del túnel se mueve 2 m: 5×6 = 30 m², 4 pórticos (8 columnas a 2 m). Las 6 bases del este/oeste se reutilizan; las 2 columnas nuevas del sur van con placa + 4 anclas de cuña 3/8"×5" cada una, como en Fase 1. El canalón sur se cuelga en el alero nuevo; la bajante NE y el tinaco no se mueven.
2. 2 bancadas E–O de 4 líneas PVC sanitario 4" × 3 m (10 canastillas a 20 cm), alto al OESTE (manifold) y bajo al ESTE (retornos), 2–3 %; pasillo de 0.9 m entre bancadas; la A se atiende por 2 lados, la B por 1.
3. TK-2 tambo 200 L tapado, entre los retornos; P-1/P-2 diafragma 12 V + F-1 malla 120 + FT-1 al lado; subida ¾" al pie de la bancada A hasta el manifold. Sondas pH/EC/T en el RETORNO; peristálticas al tambo.
4. Llenado: tinaco → F-2 dúplex (sin cloro) → SV-1 NC → tambo ≈ 4.45 m. Purga SV-2 (cambio cada 2–3 sem) se une al drenaje ≈ 8.78 m a la coladera.
5. GAB-DC (CC): LiFePO4 100 Ah a 30 cm del piso + EPEVER LS2024B + fusiblera 6 vías, separado de GAB-A (CA: cargador). Panel 100 W opcional EN LA AZOTEA, nunca sobre el plástico del túnel. Bus 12 V por la troncal aérea a bombas y GAB-2.
6. GAB-2 (CC) en la columna sur x = 4.6: ESP32 nodo-nft-v2 (pH/EC, MOSFET peristálticas, solenoides, detector CFE). Bus GAB-DC→bombas ≈ 4.2 m.
7. Cuarto de cosecha completo: refri usado 9–11 ft³ a 4–5 °C en su propio contacto GFCI, mesa inox, tina/lavamanos, hielera de reparto.
8. ESP32-CAM en la columna NE: puerta, zaguán y tinaco (detección nocturna). Nada de valor visible desde la calle; candado en el túnel.
9. Mesa de germinación (foami agrícola) y trasplante a canastilla, junto a la puerta y al tambo. Rack 4 opcional donde iba la mesa de siembra.
10. Mismo drenaje de Fase 1: recibe además la purga del tambo (200 L cada 2–3 sem) y el rebosadero. Sigue sin cruzar el paso al túnel.

### Notas { data-toc-label="Notas · Fase 2" }

**Recorridos nuevos (m)**

- bus 12 V GAB-DC → bombas ≈ 4.2 · → GAB-2 ≈ 3.13.
- llenado ≈ 4.45 · subida ¾" ≈ 4.33 · manifold 3.2 · retornos 2 × 1.6.
- purga → coladera ≈ 8.78 · troncal 127 V ≈ 6.58 (igual que Fase 1).

**Supuestos y reglas**

- SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, zaguán al NORTE, coladera en la esquina NE, losa de concreto, cobertizo de 3.5 × 1.7 m en la esquina SE. Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera; las reglas de abajo deben sobrevivir al cambio.
- Separación entre líneas NFT 28 cm eje a eje (bancada 1.12 m) [POR VERIFICAR con el porte de la albahaca a 20 cm entre canastillas; con 30–35 cm la bancada sube a 1.2–1.4 m y el pasillo baja a 0.7 m].
- Cajas de equipo (rótulo corto en el plano): P-1/P-2 son bombas de diafragma 12 V con presostato en caja IP65; F-1 es filtro de malla 120 y FT-1 el de disco; la mesa de cosecha es de inox o polietileno de grado alimenticio.
- Distancias mínimas: pasillos ≥ 0.9 m · bancada atendida por un solo lado ≤ 1.2 m · tambo tapado y a la sombra (18–22 °C) · sondas en el retorno · peristálticas al tambo junto a la succión · batería a 30 cm del piso y nunca en la caja de 127 V · refri bajo techo con GFCI propio.
- Fuentes: referencia/03 §2 · research/hidroponia-nft · research/electrico-respaldo-seguridad §2.4 y §3.6 · research/inocuidad-operativa §4 (NOM-251) · referencia/07 §1–3 y §10 · diseno/hidraulico §2 · diseno/electrico §2–3 · bom/fase2.csv.
