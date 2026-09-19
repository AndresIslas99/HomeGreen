<!-- Generado por hardware/cad/layout.py. No editar a mano: se regenera con
     python3 hardware/cad/layout.py y se incrusta con pymdownx.snippets. -->

### Leyenda { data-toc-label="Leyenda · Fase 1" }

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

### Notas clave { data-toc-label="Notas clave · Fase 1" }

1. Túnel 18 m²: 3 pórticos (6 columnas a 3 m) con placa + 4 anclas de cuña 3/8"×5"; puerta al este, de frente al zaguán y al tinaco.
2. 3 racks Husky en fila contra la pared norte, separados 0.34 m (los T8 de 1.2 m vuelan 14 cm por lado). Rack 3 = testigo con MT-1…4.
3. TK-1 750 L sobre base firme 1.3×1.3 (lleno ≈ 750 kg), opaco, a 0.4 m de la coladera (rebosadero) y a 0.9 m del túnel (paso libre).
4. Canalones N y S → bajante NE → tramo 3" a 2 m sobre el paso → SP-1 tlaloque (purga 20–40 L) + filtro de hojas → tapa del tinaco.
5. P-1 bomba de diafragma 12 V con presostato, en caja IP65, + F-1 de sedimentos junto a la salida del tinaco; riego ½" aéreo (2 m) por la cabecera este y el larguero norte → riser por rack → nebulizadores N1–N4 (2 boquillas/nivel).
6. GAB-1 (CC, IP65) en la columna NE a 2.0 m: ESP32 nodo-riego-v1 + relé 4 ch + buck. A ≤ 3 m del rack testigo y ≤ 2 m del tinaco (LT-1); Wi-Fi desde el cerebro ≈ 7 m con una pared.
7. GAB-A (CA, IP65) en la pared bajo el cobertizo: fuente 12 V 5 A + contactor K5 de T8/extractor. Cordón uso rudo 1 m al contacto WR.
8. Troncal aérea a 2.2 m (mensajero de acero): 127 V a T8/extractor + 12 V a GAB-1 + señal K5. GAB-A → GAB-1 ≈ 6.58 m (12 V 5 A: 10–12 AWG).
9. Centro de carga: breaker QO120GFI 20 A para TODO el circuito del patio; conduit 12 AWG al contacto WR in-use; varilla copperweld 5/8"×3 m ≤ 25 Ω.
10. Drenaje de charolas colectoras (racks sobre bloques de 15 cm) por la pared norte, cabecera este y barda este → coladera ≈ 12.4 m, ≥ 1 %.
11. Cobertizo = cuarto de cosecha (NOM-251): mesa inox, tina de lavado + lavamanos en la toma, hielera; cortina plástica lo separa del cultivo.
12. Tambo de composta (sustrato usado 100–150 kg/mes) en la esquina opuesta al cultivo y a la cosecha; charola con fusarium va a la basura.
13. Extractor en la cabecera oeste (HR > 70 %); entra aire por la puerta y los faldones enrollables con malla antiáfidos (laterales N y S).
14. Mesa de siembra dentro del túnel (tapete térmico dic–feb por K4). En Fase 2 su lugar lo puede tomar el rack 4.

### Notas { data-toc-label="Notas · Fase 1" }

**Recorridos (m, sobre este supuesto)**

- 127 V troncal GAB-A → columna SE → GAB-1 ≈ 6.58 · T8 larguero ≈ 6.87.
- 12 V GAB-1 → P-1 ≈ 2.25 · riego P-1 → rack 1 ≈ 6.4 (+ 3 risers).
- red → FV-1 ≈ 7.58 · drenaje → coladera ≈ 12.4 · canalón 6 + 6 + colector 3.

**Supuestos y reglas**

- SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, zaguán al NORTE, coladera en la esquina NE, losa de concreto, cobertizo de 3.5 × 1.7 m en la esquina SE. Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera; las reglas de abajo deben sobrevivir al cambio.
- Distancias mínimas: túnel ≥ 0.6 m de bardas (tensar plástico, drenaje perimetral) y ≥ 0.8 m de la barda norte · pasillo interior ≥ 0.9 m · puerta 0.9 m · paso libre túnel–tinaco 0.9 m · tinaco en piso firme sin tapar la coladera · gabinetes a ≥ 1.2 m del piso y 127 V y 12 V en cajas separadas.
- Nada de 127 V en el patio sin GFCI + tierra física + gabinete IP65 (NOM-001-SEDE, lugar mojado). Fuentes: referencia/03 §1 · research/instalacion-tunel-detalle §1–4 · research/estructura-invernadero · diseno/electrico §4 · diseno/hidraulico §1 y §3 · bom/fase1.csv.
