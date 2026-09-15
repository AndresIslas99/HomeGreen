# Modelos CAD paramétricos (OpenSCAD)

Modelos 3D del huerto en [OpenSCAD](https://openscad.org) (probados con la versión 2021.01).
Cada archivo es un modelo paramétrico: cambias un número al principio del archivo, vuelves a
renderizar y el PNG de la wiki se actualiza. Los renders viven en
`docs/assets/diagramas/cad/` y los usan las páginas de diseño
(`docs/diseno/estructura-tunel.md`, `rack-y-charolas.md`, `layout-patio.md`) y los índices
de fase.

| Archivo | Qué modela | Render (docs/assets/diagramas/cad/) | Fase |
|---|---|---|---|
| `tunel_3x6.scad` | Túnel a dos aguas 3 × 6 m: PTR 1½" cal. 14, 6 columnas, placas base 100 × 100 mm con 4 anclas 3/8" × 5", pendiente 30 %, largueros, contravientos, plástico translúcido, malla antigranizo a 150 mm, canalón + bajante. Imprime la **lista de cortes** en consola. | `tunel-3x6.png` | 1 |
| `tunel_5x6.scad` | El mismo módulo `tunel()` con `ancho = 5000`, 4 pórticos (8 columnas) y 2 largueros de techo por agua. No copia geometría: hace `use <tunel_3x6.scad>`. | `tunel-5x6.png` | 2 |
| `rack_charolas.scad` | Rack Husky 1830 × 914 × 457 mm, 5 niveles, 3 charolas 1020 (254 × 508 × 60 mm) por nivel, 2 tubos T8 de 1200 mm por nivel iluminado, riser de riego. Los niveles muestran los estados del SOP (tapada / brote / desarrollo / cosecha). | `rack-charolas.png` | 0–1 |
| `linea_nft.scad` | Línea NFT: PVC sanitario 4" (OD 114 mm) × 3000 mm, 10 perforaciones a 200 mm entre centros, canastillas 3", pendiente 2.5 %, 3 soportes de PTR 1", tapas, entrada ½" y retorno 2". Incluye el módulo `bancada_nft()` (n líneas sobre soportes compartidos). | `linea-nft.png` | 2 |
| `patio_fase2.scad` | Composición del patio de 10 × 8 m (supuesto): túnel 5 × 6, 8 líneas NFT en 2 bancadas, tambo 200 L, tinaco 750 L, 3 racks, gabinetes IP65, zona de cosecha. Usa los tres archivos anteriores con `use <...>`. | `patio-fase-2-3d.png` | 2 |

Unidades: **milímetros**. Ejes: X = oeste → este, Y = sur → norte, Z = altura. En el túnel la
cumbrera corre a lo largo de Y y la puerta va en la cabecera norte (`y = largo`), porque la
wiki supone el acceso del patio al norte.

## Requisitos

- OpenSCAD 2021.01 o posterior (`sudo apt install openscad` en Debian/Ubuntu; en macOS `brew
  install --cask openscad`; en Windows el instalador oficial).
- Para renderizar sin pantalla (servidor, CI): `xvfb-run` (`sudo apt install xvfb`).
- Fuente DejaVu Sans para los rótulos (viene en casi todas las distribuciones; si falta, el
  rótulo sale con la fuente por defecto y no pasa nada).

## Cómo modificar parámetros

1. Abre el `.scad` en el editor de OpenSCAD (o cualquier editor de texto).
2. Todos los parámetros están **al principio del archivo**, agrupados y comentados en español
   (geometría, perfiles, placa y anclas, cubierta, canalón, "qué dibujar", colores).
3. Cambia el valor, guarda y pulsa F5 (preview). La consola imprime la lista de cortes / el
   resumen con los nuevos valores.

Ejemplos útiles:

| Quiero… | Cambia… |
|---|---|
| Un túnel de 4 × 7 m | En `tunel_3x6.scad`: `ancho = 4000; largo = 7000;` (o crea un `tunel_4x7.scad` con `use <tunel_3x6.scad>` como hace `tunel_5x6.scad`). |
| Postes cada 2 m en vez de 3 m | `n_porticos = 4` (8 columnas, 32 anclas). |
| Alero a 2.2 m | `h_columna = 2200`. |
| Pendiente de 25 % (mínimo) | `pendiente = 25`. No bajes de 25 %: el granizo acumulado es la causa #1 de colapso del plástico. |
| Malla antigranizo a 100 mm del plástico | `sep_malla = 100` (el informe admite 10–20 cm). |
| Ver solo el esqueleto (sin plástico ni malla) | `mostrar_plastico = false; mostrar_malla = false;` |
| Bajante del canalón en el alero oeste | `lado_bajante = -1`. |
| Cortinas laterales dibujadas abiertas | Hoy se dibujan cerradas; pon `mostrar_plastico = false` o edita la altura del `cube` de "cortinas laterales" en `tunel()`. |
| Rack de 1.22 m de ancho (Husky ancho) | En `rack_charolas.scad`: `rack_ancho = 1219; rack_fondo = 610; charolas_por_nivel = 4;` |
| Charolas 1020 sin sobresalir del fondo | Solo con el rack de 610 mm de fondo (arriba); con 457 mm la charola de 508 sobresale 25 mm por lado, es normal. |
| Cilantro a 15 cm en el NFT | En `linea_nft.scad`: `sep_perf = 150; n_plantas = 14;` (14 × 150 = 2.1 m centrados en 3 m). |
| Perforación para la canastilla que compré | `d_perf = <lo que mediste en el cuerpo bajo el labio>` y `canastilla_cuerpo` igual. **El diámetro real se mide en la canastilla, nunca se toma de aquí.** |
| Pendiente NFT de 3 % | `pendiente = 3` (en `linea_nft.scad`). |
| Bancada de 3 líneas | En `patio_fase2.scad`: `nft_lineas_por_bancada = 3`. |
| Patio de 12 × 7 m | En `patio_fase2.scad`: `patio_x = 12000; patio_y = 7000;` y reacomoda `tunel_cx`, `tunel_y0`, `tinaco_pos`, `racks`. |

Las funciones y módulos se reutilizan entre archivos con `use <archivo.scad>`; `use` importa
módulos y funciones (con sus valores por defecto) pero **no** las variables de nivel superior:
por eso `tunel_5x6.scad` vuelve a declarar `ancho`, `largo`, etc. y los pasa como argumentos.

## Cómo re-renderizar los PNG de la wiki

Desde `hardware/cad/` (las rutas de salida son relativas a esa carpeta). Con pantalla, quita
`xvfb-run -a`.

```bash
cd hardware/cad
OUT=../../docs/assets/diagramas/cad
OPTS="--autocenter --viewall --imgsize=1400,1000 --projection=p --colorscheme=Tomorrow"

xvfb-run -a openscad -o $OUT/tunel-3x6.png       $OPTS --camera=0,0,0,62,0,212,0 tunel_3x6.scad
xvfb-run -a openscad -o $OUT/tunel-5x6.png       $OPTS --camera=0,0,0,62,0,212,0 tunel_5x6.scad
xvfb-run -a openscad -o $OUT/rack-charolas.png   $OPTS --camera=0,0,0,72,0,22,0  rack_charolas.scad
xvfb-run -a openscad -o $OUT/linea-nft.png       $OPTS --camera=0,0,0,52,0,25,0  linea_nft.scad
xvfb-run -a openscad -o $OUT/patio-fase-2-3d.png $OPTS --camera=0,0,0,42,0,200,0 patio_fase2.scad
```

- `--camera=tx,ty,tz,rx,ry,rz,dist` es la cámara "gimbal": con `--viewall` la distancia se
  ajusta sola y solo importan `rx` (elevación: 90 = de frente, 0 = desde arriba) y `rz`
  (azimut: 0 = desde el sur, 180–215 = desde el norte/noreste, donde está la puerta).
- Si un render sale vacío o cortado, cambia `rz`/`rx` o sube `dist` quitando `--viewall`.
- Cada PNG de la wiki pesa entre 48 y 230 KB; si uno sale de menos de 20 KB, el modelo no se
  dibujó (revisa errores de sintaxis en la consola: `openscad -o x.png archivo.scad 2>&1`).
- Los `ECHO` (lista de cortes, resumen de rack/línea) salen por **stdout**: para guardarlos,
  `openscad -o /tmp/x.png tunel_3x6.scad > cortes.txt 2>&1`.

## Cómo leer la lista de cortes del túnel

`tunel_3x6.scad` y `tunel_5x6.scad` imprimen `PERFIL | pieza | cantidad × longitud`, los metros
lineales por perfil y el mínimo teórico de tramos de 6 m. Ese mínimo **no** incluye el
desperdicio de corte; el empaquetado real por tramo (con 3 mm de kerf por corte) está en la
tabla de `docs/diseno/estructura-tunel.md`. Truco práctico: tres columnas de 2.00 m no caben
en un tramo de 6.00 m exactos (6,000 + kerf); si tu proveedor entrega 6.10 m sí caben, y si
no, corta las columnas a 1.99 m.

## Exportar a STL / DXF (opcional)

```bash
openscad -o tunel_3x6.stl tunel_3x6.scad   # malla 3D (los .stl están en .gitignore)
openscad -o placa.dxf placa_2d.scad         # plano 2D: solo si creas un archivo con projection()
```

Para planos 2D de las placas base o de las perforaciones del NFT, lo más simple es un archivo
nuevo con `projection()` sobre el módulo que quieras y exportar a DXF/SVG.

## Limitaciones honestas

- Es un modelo **geométrico** para dimensionar, cortar y explicar; **no es un cálculo
  estructural**. Las cargas de viento y el margen de las anclas se discuten con cifras del
  informe en `docs/diseno/estructura-tunel.md`; para una estructura mayor de 30 m² o en azotea,
  consulta a un ingeniero.
- Las uniones se dibujan a tope (sin cartabones ni cordones de soldadura); el herrero decide
  el detalle de unión y puede pedir 1–2 cm extra por pieza para escuadrar.
- En el preview (F5/OpenCSG) lo que se dibuja después de una superficie translúcida queda
  oculto tras ella: por eso en `patio_fase2.scad` el túnel y las bardas van al final. Si
  agregas objetos dentro del túnel, agrégalos **antes** del bloque "Superficies translúcidas".
- Las dimensiones del tinaco de 750 L y del tambo de 200 L son típicas, no de ficha técnica:
  mide el que compres antes de trazar bases.
