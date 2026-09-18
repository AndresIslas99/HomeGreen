<!-- Generado por hardware/cad/layout.py. No editar a mano: se regenera con
     python3 hardware/cad/layout.py y se incrusta con pymdownx.snippets. -->

### Leyenda { data-toc-label="Leyenda · Fase 3" }

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

### Notas clave { data-toc-label="Notas clave · Fase 3" }

1. Camas 1–2 (1.0 m: se atienden por un lado) al este, sobre la línea de drenaje; cama 3 (gantry) al sur. Total 8.7 m² de 8.7: es lo que cabe con pasillos ≥ 0.7 m. Meta 15–20 m²: ver layout-patio.md §5.
2. Goteo colgado de HA: SV-3 (12 V NC) en la caja F-2 desde el tinaco; ramal este ≈ 3.8 m y ramal sur por la troncal y el alero sur ≈ 6.53 m.
3. Gantry XY tipo FarmBot sobre la cama 3 (la más larga): carrera ≈ 3.0 × 0.9 m, GAB-3 con driver + cámara en la pared de la casa, 12 V desde GAB-DC.
4. Cámara fija en poste de 2 m: cobertura foliar, plagas y timelapse de la cama 3 (visión = juguete de F3, no el negocio).
5. La composta del tambo alimenta las camas (07 §12); nunca charola con fusarium. Ruta corta, sin cruzar el cuarto de cosecha.
6. Regla de oro F3: ningún cable ni manguera nueva cruza pasillos a nivel de piso; todo aéreo (2 m) o pegado a barda/cama.

### Notas { data-toc-label="Notas · Fase 3" }

**Qué cambia vs. Fase 2**

- 3 camas elevadas = 8.7 m² (alt. 0.7–0.9 m [POR VERIFICAR]).
- SV-3 + goteo por cama (timer + humedad en HA).
- Gantry sobre la cama 3; GAB-3 driver; cámara fija.
- Nada de esto es el negocio: sólo si Fases 1–2 se pagan.

**Supuestos y reglas**

- SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, zaguán al NORTE, coladera en la esquina NE, losa de concreto, cobertizo de 3.5 × 1.7 m en la esquina SE. Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera; las reglas de abajo deben sobrevivir al cambio.
- La estructura del túnel no cambia respecto a Fase 2: 4 pórticos (8 columnas a 2 m), cada columna con placa + 4 anclas de cuña 3/8"×5" sobre losa sana de ≥ 10 cm y a ≥ 15 cm del borde.
- Cajas de equipo (rótulo corto en el plano): P-1/P-2 son bombas de diafragma 12 V con presostato en caja IP65; F-1 es filtro de malla 120 y FT-1 el de disco; SV-3 es el solenoide 12 V NC del goteo, dentro de la caja F-2; la mesa de cosecha es de inox o polietileno de grado alimenticio.
- Las camas van pegadas a la barda este y a la casa y se atienden por un solo lado: por eso miden ≤ 1.0 m de ancho. Cama 3 deja libre la puerta casa→patio y 0.7 m de paso frente al túnel.
- [POR VERIFICAR] altura y material de cama (0.7–0.9 m: madera tratada/PTR + geomembrana), perfil V-slot y carrera del gantry, caudal de goteo por cama: no están en la fuente de verdad; el plan maestro sólo fija 'camas elevadas con goteo colgado de HA' y 'gantry XY V-slot + NEMA17 + GRBL/Klipper'.
- Fuentes: referencia/00-plan-maestro §Fase 3 · referencia/07 §12 y §14 · research/hidroponia-nft (periférica sólo para riego presurizado de camas) · plantas de Fases 1–2.
