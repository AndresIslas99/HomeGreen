<!-- Generado por hardware/cad/layout.py. No editar a mano: se regenera con
     python3 hardware/cad/layout.py y se incrusta con pymdownx.snippets. -->

### Leyenda { data-toc-label="Leyenda · Fase 0" }

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

### Notas clave { data-toc-label="Notas clave · Fase 0" }

1. Rack pegado a la pared sur, bajo techo: luz indirecta, sin sol de mediodía ni goteo. Nivelar y calzar patas; forrar entrepaños de MDF.
2. Mesa de siembra junto a la toma (< 10 m): remojo, pesado y sanitización de semilla (H2O2 3 %) con atomizador de mano. 20 charolas 10×20.
3. Contacto existente (sin GFCI aún). T8 opcionales con timer; en Fase 1 se vuelve contacto GFCI in-use + tierra.
4. Reserva del túnel: medir aquí 3 días T mín/máx (ideal 16–24 °C) y luz con Photone (100–200 µmol/m²s); diagonales iguales ± 1 cm; losa sana ≥ 10 cm; bordes a ≥ 15 cm de cualquier ancla.
5. Coladera existente: probarla (10 L de golpe deben irse); nada la tapará: ni placas, ni tinaco, ni composta.
6. Zaguán de 1.0 m: ¿pasa el tinaco de 750 L (Ø ≈ 1.1 m)? Si no, entra por la casa o se compra el de 450 L [POR VERIFICAR Ø].
7. Sustrato usado: cubeta con tapa lejos del rack (fungus gnats); en Fase 1 se vuelve tambo de composta.

### Notas { data-toc-label="Notas · Fase 0" }

**Qué hay en Fase 0 (y nada más)**

- 1 rack Husky ($2,019) · 20 charolas · semilla · coco · báscula · atomizador · H2O2. Sin túnel, sin bomba, sin relés: la Fase 0 valida que los chefs PAGAN.

**Antes de Fase 1 (checklist de replanteo)**

- ¿Condominio? Art. 21/23 antes de perforar (07 §9).
- Consumo base CFE 7 días (medidor de enchufe) y tarifa.
- EC/pH de la llave 3 días distintos (02 §agua).
- Foto de losa, coladera, toma, contacto y bardas.

**Supuestos y reglas**

- SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, zaguán al NORTE, coladera en la esquina NE, losa de concreto, cobertizo de 3.5 × 1.7 m en la esquina SE. Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera; las reglas de abajo deben sobrevivir al cambio.
- Reglas: rack bajo techo con toma a < 10 m y contacto cerca · pasillo ≥ 0.9 m frente al rack · la reserva del túnel queda a ≥ 0.6 m de bardas y ≥ 0.8 m de la barda norte (canaleta + paso) · nada tapa la coladera.
- El «cerebro» del recuadro punteado (mini-PC con Home Assistant + router + UPS) va DENTRO de la casa, junto al centro de carga: seco, ventilado y con el Wi-Fi a ≤ 8 m del gabinete más lejano del patio.
- Fuentes: referencia/03-instalacion §0.1–0.2 · research/estructura-invernadero §d · bom/fase0.csv · referencia/07 §9. Escala 1:50 (1 m = 100 px en el SVG). Norte arriba.
