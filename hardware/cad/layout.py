#!/usr/bin/env python3
"""Plantas 2D del patio (Fases 0-3) y alzado del rack Husky, en SVG puro (stdlib).

Uso:
    python3 hardware/cad/layout.py            # escribe en docs/assets/diagramas/layout/
    python3 hardware/cad/layout.py --out DIR  # otra carpeta

Escalas:
    * Plantas: 1:50 -> 1 m = 100 px (S = 100). Norte arriba. Cotas en m.
    * Alzado del rack: 1:10 -> 1 cm = 4 px. Cotas en cm.

SUPUESTO DEL PATIO (anotado en cada plano): 10 x 8 m = 80 m2, casa al SUR (pared),
acceso (zaguan) por el NORTE, coladera en la esquina NORESTE, losa/firme de concreto,
cobertizo existente de 3.5 x 1.7 m en la esquina sureste (junto a la casa).
Si tu patio es distinto: cambia las constantes de la seccion GEOMETRIA y regenera.
Las reglas de distancia que deben sobrevivir al cambio estan en docs/diseno/layout-patio.md.

Convencion de dibujo: dentro del SVG solo van cotas y etiquetas cortas + NOTAS CLAVE numeradas
(circulos). El texto de esas notas, la leyenda y las tablas se escriben al lado en
<nombre>.notas.md y las paginas de la wiki lo incrustan con pymdownx.snippets: dentro del
dibujo se leia a 6 px, en la pagina se lee a 16. Los recorridos de agua (azul), electrico
(ambar) y cultivo (verde) se etiquetan con su longitud calculada sobre este supuesto.

Fuentes de los numeros: docs/referencia/03-instalacion.md, docs/research/estructura-invernadero.md,
docs/research/instalacion-tunel-detalle.md, docs/referencia/07-puntos-ciegos-y-riesgos.md,
docs/diseno/{electrico,hidraulico,estructura-tunel}.md, bom/fase0-2.csv.
El SVG no usa fuentes externas ni scripts: abre solo.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

# ----------------------------------------------------------------------------- estilo
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"
INK = "#1f2937"      # trazos
GRAY = "#6b7280"     # texto secundario
LIGHT = "#e5e7eb"    # rellenos suaves
GREEN = "#2e7d32"    # cultivo
GREEN_BG = "#e8f5e9"
AMBER = "#b45309"    # electrico
AMBER_BG = "#fff7ed"
BLUE = "#1d4ed8"     # agua
BLUE_BG = "#eff6ff"
WHITE = "#ffffff"
VER = "HomeGreen · v1 · 2026-09"

DASH = "6 4"          # discontinua: drenaje / 12 V CC / reserva de fase siguiente
DOT = "2 3"           # punteada: senal de sensor / Wi-Fi
DASHDOT = "10 4 2 4"  # canaleta / bajante pluvial / cumbrera


def fmt(v: float) -> str:
    """Numero corto sin ceros inutiles."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


# --- tipografia ---------------------------------------------------------------
# MEDIDO en el sitio construido (Chrome, ventana de 1512 px): docs/assets/css/extra.css sube
# .md-grid a 88rem, con lo que la columna de contenido queda en 980 px, PERO la imagen recibe
# 910 px de caja de contenido, no 980: la regla 2 de extra.css limita `.md-typeset > p` a 46rem
# (920 px) y el diagrama va dentro de un <p>. La escala real es entonces 910/1220 = 0.746.
# Una letra de "size" unidades se ve a size * FS * 0.746 px. Con FS = 1.50 el cuerpo (9-9.5 u)
# queda en 10.1-10.6 px y las cotas de 10.5 u en 11.8 px; antes, con lienzo de 1600 u y sin
# factor, el cuerpo era de 5.1-5.4 px. El texto corrido de la wiki es de 16 px.
# TODO texto largo (leyenda, notas clave, tablas) salio del dibujo a <nombre>.notas.md: dentro
# del SVG solo quedan cotas y rotulos cortos, que son los que de verdad necesitan estar ahi.
FS = 1.50

# Halo blanco bajo cada rotulo, en fraccion del tamano de letra. Al subir FS la letra crecio
# sobre una geometria que NO crecio, asi que muchas cotas y etiquetas quedaron atravesadas por
# su propia linea de extension o por un recorrido. El halo (un contorno blanco pintado ANTES
# del relleno, con paint-order="stroke") interrumpe el trazo justo alrededor de las letras sin
# mover nada: 0.22 em -> ~1.5 u de blanco por lado con el cuerpo de 13.5 u, suficiente para
# despegar la letra de un trazo de 1-2.5 u. OJO: solo borra lo que se dibujo ANTES; contra un
# relleno opaco posterior no puede nada (eso se arregla moviendo, no con halo).
HALO = 0.22

# Anchos de Helvetica en milesimas de em, para estimar el ancho de una cadena y partir el
# subtitulo en lineas que quepan en el lienzo. No hace falta precision de tipografo: el margen
# de seguridad de wrap() absorbe el error.
_W = {" ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191, "(": 333,
      ")": 333, "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278,
      "<": 584, "=": 584, ">": 584, "?": 556, "@": 1015, "[": 278, "]": 278, "^": 469, "_": 556,
      "{": 334, "|": 260, "}": 334, "~": 584, "·": 278, "→": 1000, "≈": 584, "≥": 584, "≤": 584,
      "²": 333, "°": 400, "µ": 556, "Ø": 778, "½": 834, "¾": 834, "¼": 834, "–": 556, "—": 1000,
      "×": 584, "±": 584, "…": 1000, "▼": 1000, "◄": 1000, "►": 1000, "§": 556, "¿": 556,
      "①": 1000, "②": 1000, "③": 1000, "④": 1000, "⑤": 1000, "✓": 700}
_W.update({c: 556 for c in "0123456789"})
_W.update(dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                   (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
                    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update(dict(zip("abcdefghijklmnopqrstuvwxyz",
                   (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                    556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500))))
_ACC = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N"}


def twidth(s: str, size: float) -> float:
    """Ancho aproximado de `s` en unidades de viewBox, ya con el factor FS aplicado."""
    return sum(_W.get(_ACC.get(c, c), 556) for c in s) * size * FS / 1000.0


def wrap(s: str, size: float, maxw: float) -> list[str]:
    """Parte `s` en lineas que no pasen de `maxw` unidades (margen del 3 %)."""
    if not s:
        return []
    out, cur = [], ""
    for word in s.split(" "):
        probe = f"{cur} {word}".strip()
        if cur and twidth(probe, size) > maxw * 0.97:
            out.append(cur)
            cur = word
        else:
            cur = probe
    if cur:
        out.append(cur)
    return out


SUB_SIZE = 12          # tamano del subtitulo (antes de FS)
SUB_LH = 20            # interlineado del subtitulo, en unidades de viewBox


def head_rule_y(subtitle: str, w: int) -> float:
    """Y de la linea horizontal de la cabecera: depende de cuantas lineas ocupa el subtitulo."""
    n = max(1, len(wrap(subtitle, SUB_SIZE, w - 48))) if subtitle else 0
    return 58 + SUB_LH * max(0, n - 1) + 14 if n else 50


class SVG:
    """Acumulador minimo de SVG con cabecera estandar de la wiki (titulo, version, linea)."""

    def __init__(self, w: int, h: int, title: str, subtitle: str = ""):
        self.w, self.h = w, h
        self.parts: list[str] = []
        # Contenido que NO se dibuja: se emite como Markdown junto al SVG (<nombre>.notas.md).
        self.md_leyenda: list[str] = []
        self.md_keys: list[str] = []
        self.md_bloques: list[tuple[str, list[str]]] = []
        self.md_notas: list[str] = []
        self.add('<?xml version="1.0" encoding="UTF-8"?>\n'
                 f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                 f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">')
        self.add(f"<title>{escape(title)}</title>")
        defs = ["<defs>"]
        for name, col in (("arrInk", INK), ("arrBlue", BLUE), ("arrAmber", AMBER), ("arrGreen", GREEN)):
            defs.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                        f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="{col}"/></marker>')
        defs.append(f'<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                    f'<line x1="0" y1="0" x2="0" y2="8" stroke="{INK}" stroke-width="1.2"/></pattern>')
        defs.append(f'<pattern id="hatchGreen" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                    f'<line x1="0" y1="0" x2="0" y2="6" stroke="{GREEN}" stroke-width="0.8"/></pattern>')
        defs.append(f'<pattern id="roof" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
                    f'<line x1="0" y1="0" x2="0" y2="10" stroke="{GRAY}" stroke-width="0.6"/></pattern>')
        defs.append("</defs>")
        self.add("".join(defs))
        self.rect(0, 0, w, h, fill=WHITE, stroke="none")
        self.text(24, 34, title, size=18, weight="bold")
        for i, row in enumerate(wrap(subtitle, SUB_SIZE, w - 48)):
            self.text(24, 58 + i * SUB_LH, row, size=SUB_SIZE, fill=GRAY)
        self.text(w - 24, 34, VER, size=12, fill=GRAY, anchor="end")
        self.head_y = head_rule_y(subtitle, w)
        self.line(24, self.head_y, w - 24, self.head_y, sw=1)

    # -- primitivas -----------------------------------------------------------
    def add(self, s: str) -> None:
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.5, dash=None, rx=0, opacity=None):
        a = (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}" '
             f'stroke="{stroke}" stroke-width="{sw}"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if rx:
            a += f' rx="{rx}"'
        if opacity is not None:
            a += f' fill-opacity="{opacity}"'
        self.add(a + "/>")

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None, cap="round"):
        a = (f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="{stroke}" '
             f'stroke-width="{sw}" stroke-linecap="{cap}"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if marker:
            a += f' marker-end="url(#{marker})"'
        self.add(a + "/>")

    def polyline(self, pts, stroke=INK, sw=1.5, dash=None, marker=None, fill="none", close=False):
        p = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        a = (f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
             f'stroke-linejoin="round" stroke-linecap="round"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if marker:
            a += f' marker-end="url(#{marker})"'
        self.add(a + "/>")

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.5, dash=None):
        a = f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.add(a + "/>")

    def text(self, x, y, s, size=12, fill=INK, anchor="start", weight="normal", rotate=None, italic=False,
             halo=None):
        # `size` se escribe en la escala historica del dibujo; FS la sube a la escala legible.
        # halo=None -> automatico: lo lleva todo rotulo salvo los que van en blanco sobre un
        # relleno oscuro (ahi el halo blanco borraria la letra en vez de despejarla).
        if halo is None:
            halo = fill != WHITE
        a = (f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{FONT}" font-size="{fmt(size * FS)}" fill="{fill}" '
             f'text-anchor="{anchor}"')
        if halo:
            a += (f' stroke="{WHITE}" stroke-width="{fmt(size * FS * HALO)}" stroke-linejoin="round"'
                  f' paint-order="stroke"')
        if weight != "normal":
            a += f' font-weight="{weight}"'
        if italic:
            a += ' font-style="italic"'
        if rotate is not None:
            a += f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"'
        self.add(a + f">{escape(s)}</text>")

    def lines(self, x, y, rows, size=11, fill=INK, lh=None, anchor="start", weight="normal", halo=None):
        """Varias lineas de texto apiladas; devuelve la y siguiente. Una fila que empieza con '#' va en negritas."""
        lh = (lh or size + 3) * FS   # el interlineado sube con la letra o las lineas se encimarian
        for i, r in enumerate(rows):
            w = weight
            if r.startswith("#"):
                r, w = r[1:], "bold"
            if r:
                self.text(x, y + i * lh, r, size=size, fill=fill, anchor=anchor, weight=w, halo=halo)
        return y + len(rows) * lh

    def save(self, path: Path) -> None:
        self.add("</svg>\n")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts), encoding="utf-8")

    # -- texto que sale del dibujo -------------------------------------------
    def leyenda(self, items) -> None:
        """Guarda la leyenda (texto autoexplicativo: dice el trazo, no lo dibuja)."""
        self.md_leyenda.extend(items)

    def bloques(self, bloques) -> None:
        """Guarda bloques (titulo, [parrafos]) que antes iban en el panel derecho."""
        self.md_bloques.extend(bloques)

    def notas(self, rows, titulo="Supuestos y reglas") -> None:
        """Guarda las notas de pie (supuestos, reglas, fuentes)."""
        self.md_notas.extend(rows)
        self.md_notas_titulo = titulo

    def markdown(self) -> str:
        """Leyenda + notas clave + notas, en Markdown, para incrustar bajo la imagen.

        Los tres encabezados llevan `data-toc-label` porque el fragmento se repite en varias
        paginas (y hasta cuatro veces en diseno/layout-patio.md): sin eso la tabla de
        contenidos acabaria con cuatro entradas identicas llamadas "Leyenda".
        """
        etq = getattr(self, "md_toc", "")
        suf = (lambda s: " { data-toc-label=\"%s · %s\" }" % (s, etq)) if etq else (lambda s: "")
        out = ["<!-- Generado por hardware/cad/layout.py. No editar a mano: se regenera con",
               "     python3 hardware/cad/layout.py y se incrusta con pymdownx.snippets. -->", ""]
        if self.md_leyenda:
            out += ["### Leyenda" + suf("Leyenda"), ""] + [f"- {t}" for t in self.md_leyenda] + [""]
        if self.md_keys:
            out += ["### Notas clave" + suf("Notas clave"), ""]
            # en el dibujo el texto va partido a mano; en Markdown el navegador lo parte solo
            out += [f"{i}. {t.replace(chr(10), ' ')}" for i, t in enumerate(self.md_keys, 1)] + [""]
        if self.md_bloques or self.md_notas:
            out += ["### Notas" + suf("Notas"), ""]
            for titulo, filas in self.md_bloques:
                out += [f"**{titulo}**", ""] + [f"- {f}" for f in filas] + [""]
            if self.md_notas:
                out += [f"**{getattr(self, 'md_notas_titulo', 'Supuestos y reglas')}**", ""]
                out += [f"- {n}" for n in self.md_notas] + [""]
        return "\n".join(out).rstrip() + "\n"


# ----------------------------------------------------------------------------- plantas
S = 100.0  # px por metro (1:50 con 1 m = 100 px)

# Leyenda de las cuatro plantas. Ya no se dibuja (ocupaba el panel derecho), asi que cada
# entrada empieza nombrando el trazo: sin la muestra de color al lado, el texto tiene que
# describirse solo.
LEYENDA_PLANO = [
    "**Línea azul continua** — agua a presión: red ½\" · llenado.",
    "**Línea azul discontinua** — drenaje · rebosadero · purga → coladera.",
    "**Línea azul de raya y punto** — canalón / bajante pluvial (pendiente 0.5–1 %).",
    "**Línea ámbar continua** — 127 V CA (circuito GFCI del patio).",
    "**Línea ámbar discontinua** — 12 V CC (fuente / bus de batería).",
    "**Línea ámbar punteada** — señal de sensor · Wi-Fi.",
    "**Relleno verde claro con borde verde** — cultivo: rack · bancada NFT · cama.",
    "**Relleno crema con borde ámbar y aspa** — gabinete IP65 (GAB-x).",
    "**Relleno azul claro con borde azul** — tinaco TK-1 · tambo TK-2.",
    "**Rayado gris fino** — techo (túnel / cobertizo).",
    "**Línea gris discontinua** — reserva de una fase posterior.",
    "**Cuadro azul con retícula** — coladera.",
    "**Círculo azul con una T** — toma de agua.",
    "**Cuadro ámbar con dos barras** — contacto GFCI in-use.",
    "**Cuadro negro sólido** — columna PTR anclada.",
    "**Círculo numerado** — nota clave: su texto es la lista numerada de abajo.",
]


class Plano(SVG):
    """Planta del patio en metros: x de oeste a este, y de norte a sur (norte arriba).

    El lienzo cubre SOLO el dibujo. El elemento mas al este es la rosa de los vientos, en
    X(10.6) = 1170 con radio 22 -> 1192; con 24 u de margen queda W = 1220. Antes eran 1600 u
    porque 450 (28 % del ancho) los ocupaba un panel de texto: ese texto vive ahora en
    docs/assets/diagramas/layout/<nombre>.notas.md y se incrusta bajo la imagen.
    """

    W = 1220                   # ancho del lienzo (medido: dibujo hasta 1192 + margen)
    OX = 110                   # origen del patio (esquina noroeste) en px; OY se fija por fase
    MARGEN_SUR = 28            # aire bajo el rotulo mas bajo del dibujo, en Y(8.62)

    def __init__(self, fase: int, subtitle: str):
        title = f"Planta · Fase {fase} · escala 1:50 · supuesto 10×8 m"
        # El alto depende de cuantas lineas ocupa el subtitulo: la cabecera empuja el patio.
        oy = head_rule_y(subtitle, self.W) + 78
        h = int(oy + 8.62 * S + self.MARGEN_SUR)
        super().__init__(self.W, h, title, subtitle)
        self.OY = oy
        self.fase = fase
        self.md_toc = f"Fase {fase}"   # desempata las entradas del TOC cuando el fragmento se repite
        self.keys: list[str] = self.md_keys   # notas clave (texto), en orden de numero

    # -- conversion -----------------------------------------------------------
    def X(self, m):
        return self.OX + m * S

    def Y(self, m):
        return self.OY + m * S

    def mrect(self, x, y, w, h, **kw):
        self.rect(self.X(x), self.Y(y), w * S, h * S, **kw)

    def mline(self, x1, y1, x2, y2, **kw):
        self.line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), **kw)

    def mpoly(self, pts, **kw):
        self.polyline([(self.X(x), self.Y(y)) for x, y in pts], **kw)

    def mcircle(self, cx, cy, r, **kw):
        self.circle(self.X(cx), self.Y(cy), r * S, **kw)

    def mtext(self, x, y, s, **kw):
        self.text(self.X(x), self.Y(y), s, **kw)

    def mlines(self, x, y, rows, **kw):
        return self.lines(self.X(x), self.Y(y), rows, **kw)

    # -- notas clave ------------------------------------------------------------
    def key(self, x, y, text, color=INK, dx=0.0, dy=0.0):
        """Circulo numerado en (x, y) m; el texto va al Markdown de al lado. Devuelve el numero."""
        n = len(self.keys) + 1
        self.keys.append(text)
        cx, cy = self.X(x + dx), self.Y(y + dy)
        if dx or dy:
            self.line(self.X(x), self.Y(y), cx, cy, stroke=color, sw=0.8)
        self.circle(cx, cy, 9, fill=WHITE, stroke=color, sw=1.4)
        self.text(cx, cy + 3.5, str(n), size=9.5, fill=color, anchor="middle", weight="bold")
        return n

    # -- cotas ----------------------------------------------------------------
    def dim_h(self, x1, x2, y, label=None, color=INK, size=10, above=True):
        px1, px2, py = self.X(x1), self.X(x2), self.Y(y)
        for px in (px1, px2):
            self.line(px, py - 6, px, py + 6, stroke=color, sw=1)
            self.line(px - 4, py + 4, px + 4, py - 4, stroke=color, sw=1.2)
        self.line(px1, py, px2, py, stroke=color, sw=1)
        label = label if label is not None else f"{fmt(abs(x2 - x1))}"
        self.text((px1 + px2) / 2, py - 4 if above else py + 13, label, size=size, fill=color, anchor="middle")

    def dim_v(self, y1, y2, x, label=None, color=INK, size=10, left=True):
        py1, py2, px = self.Y(y1), self.Y(y2), self.X(x)
        for py in (py1, py2):
            self.line(px - 6, py, px + 6, py, stroke=color, sw=1)
            self.line(px - 4, py + 4, px + 4, py - 4, stroke=color, sw=1.2)
        self.line(px, py1, px, py2, stroke=color, sw=1)
        label = label if label is not None else f"{fmt(abs(y2 - y1))}"
        self.text(px - 4 if left else px + 12, (py1 + py2) / 2, label, size=size, fill=color, anchor="middle", rotate=-90)

    # -- marco del patio ------------------------------------------------------
    def patio(self):
        """Bardas N/E/O, pared de la casa al sur (achurada), zaguan norte, puerta de la casa, cotas y norte."""
        a0, a1 = ACCESO
        p0, p1 = PUERTA_CASA
        self.mrect(-0.15, -0.15, 10.3, 0.15, fill=LIGHT, stroke=INK, sw=1)   # barda norte
        self.mrect(-0.15, 0, 0.15, 8.0, fill=LIGHT, stroke=INK, sw=1)        # oeste
        self.mrect(10.0, 0, 0.15, 8.0, fill=LIGHT, stroke=INK, sw=1)         # este
        self.mrect(-0.15, 8.0, 10.3, 0.45, fill="url(#hatch)", stroke=INK, sw=1.5)  # casa
        self.mtext(0.15, 8.3, "CASA (pared sur)", size=11, weight="bold")
        self.mrect(0, 0, 10, 8, fill="none", stroke=INK, sw=2)
        # zaguan (acceso) en la barda norte
        self.mrect(a0, -0.15, a1 - a0, 0.15, fill=WHITE, stroke="none")
        self.mline(a0, -0.15, a0, 0, sw=1.5)
        self.mline(a1, -0.15, a1, 0, sw=1.5)
        self.mline(a0, 0, a0 + 0.05, -0.75, sw=1.2)
        self.add(f'<path d="M{fmt(self.X(a0 + 0.05))},{fmt(self.Y(-0.75))} A{fmt(0.8 * S)},{fmt(0.8 * S)} 0 0 1 '
                 f'{fmt(self.X(a1))},{fmt(self.Y(-0.05))}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
        self.mtext((a0 + a1) / 2, -0.3, "ACCESO · zaguán 1.0 m (abre hacia afuera)", size=10.5, anchor="middle", weight="bold")
        # puerta casa -> patio
        self.mrect(p0, 8.0, p1 - p0, 0.45, fill=WHITE, stroke="none")
        self.mline(p0, 8.0, p0, 8.45, sw=1.5)
        self.mline(p1, 8.0, p1, 8.45, sw=1.5)
        self.mline(p0, 8.0, p0 + 0.05, 7.1, sw=1.2)
        self.add(f'<path d="M{fmt(self.X(p0 + 0.05))},{fmt(self.Y(7.1))} A{fmt(0.9 * S)},{fmt(0.9 * S)} 0 0 1 '
                 f'{fmt(self.X(p1))},{fmt(self.Y(7.95))}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
        self.mtext((p0 + p1) / 2, 7.02, "puerta casa→patio 0.9 m", size=9.5, anchor="middle", fill=GRAY)
        # cotas generales, norte y sol
        self.dim_h(0, 10, -0.55, "10.00 m (supuesto)", size=11)
        self.dim_v(0, 8, -0.6, "8.00 m (supuesto)", size=11)
        nx, ny = self.X(10.6), self.Y(7.8)
        self.circle(nx, ny, 22, stroke=INK, sw=1.2)
        self.polyline([(nx, ny - 20), (nx - 8, ny + 10), (nx, ny + 3), (nx + 8, ny + 10)], fill=INK, stroke=INK, sw=1, close=True)
        self.text(nx, ny - 27, "N", size=13, weight="bold", anchor="middle")
        self.mtext(10.15, 8.62, "sol de mediodía: desde el SUR, casi vertical (19° N) · UV 11+ de marzo a septiembre", size=9.5, fill=GRAY, anchor="end")

    # -- simbolos -------------------------------------------------------------
    def coladera(self, x, y, s=0.3):
        self.mrect(x - s / 2, y - s / 2, s, s, fill=WHITE, stroke=BLUE, sw=1.5)
        for i in range(1, 4):
            self.mline(x - s / 2 + i * s / 4, y - s / 2, x - s / 2 + i * s / 4, y + s / 2, stroke=BLUE, sw=0.8)
            self.mline(x - s / 2, y - s / 2 + i * s / 4, x + s / 2, y - s / 2 + i * s / 4, stroke=BLUE, sw=0.8)

    def toma(self, x, y):
        self.mcircle(x, y, 0.09, fill=WHITE, stroke=BLUE, sw=1.8)
        self.mtext(x, y + 0.04, "T", size=10, fill=BLUE, anchor="middle", weight="bold")

    def contacto(self, x, y):
        self.mrect(x - 0.1, y - 0.1, 0.2, 0.2, fill=WHITE, stroke=AMBER, sw=1.8)
        self.mline(x - 0.04, y - 0.05, x - 0.04, y + 0.05, stroke=AMBER, sw=1.5)
        self.mline(x + 0.04, y - 0.05, x + 0.04, y + 0.05, stroke=AMBER, sw=1.5)

    def gabinete(self, x, y, w, h, tag, above=False, side=False, dx=0.0, anchor="middle"):
        """`side` saca el rotulo al OESTE: la troncal aerea sube por el eje del gabinete y le
        pasaba por encima al rotulo puesto arriba o abajo."""
        self.mrect(x, y, w, h, fill=AMBER_BG, stroke=AMBER, sw=2)
        self.mline(x + 0.03, y + 0.03, x + w - 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        self.mline(x + w - 0.03, y + 0.03, x + 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        if side:
            self.mtext(x - 0.16, y + h / 2 + 0.04, tag, size=9, fill=AMBER, anchor="end", weight="bold")
        else:
            self.mtext(x + w / 2 + dx, y - 0.07 if above else y + h + 0.13, tag, size=9, fill=AMBER,
                       anchor=anchor, weight="bold")

    def poste(self, x, y, size=0.09):
        self.mrect(x - size / 2, y - size / 2, size, size, fill=INK, stroke=INK, sw=1)

    def rack(self, x, y, w=0.914, h=0.457, label="", dashed=False):
        """Rack Husky 91.4 x 45.7 cm en planta con 3 charolas 25x50 atravesadas (vuelan 2.5 cm)."""
        self.mrect(x, y, w, h, fill=WHITE if dashed else GREEN_BG, stroke=GREEN, sw=1.8, dash=DASH if dashed else None)
        if not dashed:
            gap = (w - 3 * 0.254) / 4
            for i in range(3):
                self.mrect(x + gap + i * (0.254 + gap), y - 0.025, 0.254, 0.508, fill="none", stroke=GREEN, sw=0.9)
        if label:
            self.mtext(x + w / 2, y + h + 0.15, label, size=9.5, fill=GREEN, anchor="middle")

    def mesa(self, x, y, w, h, rows, color=INK, vertical=False):
        """Mesa a escala. `vertical` gira el rotulo -90 para las mesas mas altas que anchas."""
        self.mrect(x, y, w, h, fill=WHITE, stroke=color, sw=1.5)
        self.mrect(x + 0.04, y + 0.04, w - 0.08, h - 0.08, fill="none", stroke=color, sw=0.7)
        if vertical:
            # Las lineas se apilan de oeste a este; cada una corre de sur a norte. El bloque de
            # tinta se centra descontando que, girado -90, la tinta cae al oeste de la linea base.
            step = 0.11 * FS
            x0 = x + w / 2 - step * (len(rows) - 1) / 2 + 0.517 * 9 * FS / 200
            for i, r in enumerate(rows):
                self.mtext(x0 + i * step, y + h / 2, r, size=9, fill=color, anchor="middle", rotate=-90)
            return
        self.mlines(x + w / 2, y + h / 2 + (0.04 - 0.055 * (len(rows) - 1)) * FS, rows, size=9, fill=color, anchor="middle", lh=11)

    def tinaco(self, cx, cy, r, rows):
        bx, by, bw, bh = TINACO_BASE
        self.mrect(bx, by, bw, bh, fill="none", stroke=BLUE, sw=0.8, dash="3 2")
        self.mcircle(cx, cy, r, fill=BLUE_BG, stroke=BLUE, sw=2)
        self.mcircle(cx, cy, r * 0.72, fill="none", stroke=BLUE, sw=0.9)
        self.mlines(cx, cy + (0.02 - 0.06 * (len(rows) - 1)) * FS, rows, size=9, fill=BLUE, anchor="middle", lh=11)

    def tambo(self, cx, cy, r, rows, color=BLUE):
        self.mcircle(cx, cy, r, fill=BLUE_BG if color == BLUE else GREEN_BG, stroke=color, sw=2)
        self.mcircle(cx, cy, r * 0.6, fill="none", stroke=color, sw=0.9, dash="3 2")
        if rows:
            self.mlines(cx, cy + r + 0.15, rows, size=9, fill=color, anchor="middle", lh=11)

    def cama(self, x, y, w, h, rows, cxm=None):
        """Cama elevada. `cxm` corre el rotulo cuando algo opaco (la columna del gantry) cae en el centro."""
        self.mrect(x, y, w, h, fill="url(#hatchGreen)", stroke=GREEN, sw=2)
        self.mrect(x + 0.06, y + 0.06, w - 0.12, h - 0.12, fill="none", stroke=GREEN, sw=0.8)
        self.mlines(cxm if cxm is not None else x + w / 2,
                    y + h / 2 + (0.03 - 0.06 * (len(rows) - 1)) * FS, rows, size=9, fill=GREEN, anchor="middle", lh=11)

    def nft_bancada(self, x, y, length, n, pitch, name):
        """Bancada de n lineas PVC 4 pulg (0.11 m) de `length` m, eje E-O, alto al oeste."""
        h = pitch * n
        self.mrect(x, y, length, h, fill=GREEN_BG, stroke=GREEN, sw=1.2, dash="4 2")
        for i in range(n):
            cy = y + pitch / 2 + i * pitch
            self.mrect(x, cy - 0.055, length, 0.11, fill=WHITE, stroke=GREEN, sw=1.6)
            for k in range(1, int(length / 0.2)):
                self.mcircle(x + k * 0.2, cy, 0.03, fill="#c8e6c9", stroke=GREEN, sw=0.6)
        self.mtext(x + 0.05, y - 0.06, f"bancada {name} · 4 × PVC 4\" × {fmt(length)} m · alto O → bajo E (2–3 %)", size=9, fill=GREEN)

    def tunel(self, x, y, w, h, porticos, door=(1.9, 2.8)):
        """Tunel a dos aguas, cumbrera E-O, `porticos` porticos (2 columnas c/u), puerta en la cabecera este."""
        self.mrect(x, y, w, h, fill="url(#roof)", stroke="none")
        self.mrect(x, y, w, h, fill=WHITE, stroke="none", opacity=0.6)
        self.mrect(x, y, w, h, fill="none", stroke=INK, sw=2.5)
        self.mline(x, y + h / 2, x + w, y + h / 2, stroke=INK, sw=1.2, dash=DASHDOT)
        # En dos lineas y arrimado a la cabecera este: en el centro del tunel lo tapaba el relleno
        # verde opaco de la bancada A de NFT (Fases 2-3), que se dibuja despues. El tope de 0.62
        # lo fija la flecha de pendiente del portico este (x + w - 0.5).
        xr = x + w - 0.62
        self.mtext(xr, y + h / 2 - 0.30, "cumbrera E–O", size=9, fill=GRAY, anchor="end")
        self.mtext(xr, y + h / 2 - 0.08, "dos aguas ≥ 25 %", size=9, fill=GRAY, anchor="end")
        for xx in (x + 0.5, x + w - 0.5):
            self.mline(xx, y + h / 2 - 0.12, xx, y + 0.22, stroke=GRAY, sw=1, marker="arrInk")
            self.mline(xx, y + h / 2 + 0.12, xx, y + h - 0.22, stroke=GRAY, sw=1, marker="arrInk")
        n = porticos - 1
        for i in range(porticos):
            px = x + i * w / n
            self.poste(px, y)
            self.poste(px, y + h)
        # poste central de cabecera (puerta / claro > 3 m)
        for xx in (x, x + w):
            self.poste(xx, y + h / 2, size=0.07)
        d0, d1 = door
        self.mline(x + w, d0, x + w, d1, stroke=WHITE, sw=5)
        self.mline(x + w, d0, x + w + 0.8, d0 + 0.4, stroke=INK, sw=1.2)
        self.add(f'<path d="M{fmt(self.X(x + w + 0.8))},{fmt(self.Y(d0 + 0.4))} A{fmt(0.9 * S)},{fmt(0.9 * S)} 0 0 1 '
                 f'{fmt(self.X(x + w + 0.02))},{fmt(self.Y(d1))}" fill="none" stroke="{INK}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        self.mtext(x + 0.1, y - 0.28, f"TÚNEL {fmt(w)}×{fmt(h)} m = {fmt(w * h)} m² · PTR 1½\" cal. 14 · {porticos} pórticos",
                   size=10.5, weight="bold")

    # -- leyenda (ya no se dibuja: se emite en Markdown) ----------------------
    def leyenda_plano(self, extra=()):
        """Leyenda del plano en texto. Sin recuadro de muestra hay que NOMBRAR el trazo."""
        self.leyenda(LEYENDA_PLANO + list(extra))


# ----------------------------------------------------------------------------- GEOMETRIA (m)
# Cambia aqui si tu patio es distinto; todo lo demas (rutas, longitudes, cotas) se recalcula.
# x: oeste -> este (0..10). y: norte -> sur (0..8). Rectangulos: (x, y, ancho, alto). Circulos: (cx, cy, r).
ACCESO = (6.7, 7.7)               # zaguan de 1.0 m en la barda norte (supuesto)
PUERTA_CASA = (4.4, 5.3)          # puerta de la casa al patio (supuesto)
COLADERA = (9.6, 0.4)             # esquina noreste (supuesto de la wiki)
TOMA = (9.75, 7.92)               # llave existente en la pared de la casa
CONTACTO = (7.05, 7.97)           # contacto existente bajo el cobertizo -> WR GFCI in-use en F1
CONTACTO2 = (9.0, 7.97)           # 2.o contacto GFCI (refrigerador) en F2
# Franja interior de la casa (y 8.03-8.43). El orden de oeste a este es: rotulo "CASA (pared
# sur)" (termina en x = 1.45 con el cuerpo actual), CEREBRO, puerta casa->patio (4.4-5.3), CDC.
# El recuadro del cerebro arranca en 1.58 A PROPOSITO: su relleno blanco se dibuja DESPUES del
# rotulo de la casa y antes lo mordia ("CASA (pared su"). No lo muevas al oeste.
CDC = (5.40, 8.03, 1.25, 0.40)    # centro de carga (interior de la casa)
CEREBRO = (1.58, 8.03, 2.3, 0.40)  # mini-PC HA + router + UPS (interior)
VARILLA = (5.5, 7.7)              # varilla de tierra (el electricista fija el punto real)
COBERTIZO = (6.4, 6.3, 3.5, 1.7)  # alero existente (supuesto) 3.5 x 1.7 m
TUNEL_F1 = (0.6, 0.8, 6.0, 3.0)   # 18 m2, 3 porticos (6 columnas a 3 m)
TUNEL_F2 = (0.6, 0.8, 6.0, 5.0)   # 30 m2, 4 porticos (8 columnas a 2 m); crece 2 m al SUR
DOOR = (1.9, 2.8)                 # claro de puerta 0.9 m en la cabecera este (y)
RACK_XS = (2.4, 3.65, 4.9)        # 3 racks Husky pegados a la pared norte, separados 0.34 m
RACK_Y = 1.0
MESA_SIEMBRA = (1.0, 1.08, 1.2, 0.6)
TINACO = (8.15, 1.6, 0.55)        # TK-1 750 L; diametro ~1.1 m [POR VERIFICAR ficha Rotoplas]
TINACO_BASE = (7.5, 0.95, 1.3, 1.3)
# Los tres recuadros de equipo hidraulico son ESQUEMATICOS, no estan a escala: se dimensionan
# para que su rotulo quepa dentro con el cuerpo actual (antes el texto sobresalia 2-3 veces).
TLALOQUE = (7.68, 0.42, 0.48, 0.46)  # SP-1 + filtro de hojas, colgado del tramo 3" a 2 m
P1 = (7.36, 2.40, 0.72, 0.30)     # P-1 diafragma 12 V + F-1 (caja IP65)
F2BOX = (8.32, 2.40, 0.72, 0.30)  # F-2 duplex + SV-1 (llenado NFT) [+ SV-3 goteo en F3]
GAB1 = (6.3, 0.85, 0.28, 0.28)    # GAB-1 nodo riego v1 (CC), columna NE interior, a 2.0 m
GABA = (6.5, 7.55, 0.4, 0.35)     # GAB-A (CA): fuente 12 V, contactor T8, cargador (F2)
GABDC = (6.5, 6.95, 0.4, 0.35)     # GAB-DC (CC, F2): LiFePO4 100 Ah + EPEVER + fusiblera
GAB2 = (4.5, 5.52, 0.28, 0.28)    # GAB-2 nodo NFT v2 (CC), columna sur x=4.6, F2
MASTIL = (6.7, 6.3)               # poste NO del cobertizo: bajada de la troncal aerea
BANCADA_X, BANCADA_L, PITCH = 1.2, 3.0, 0.28
BANCADA_A_Y, BANCADA_B_Y = 2.4, 4.42
MANIFOLD_X = 1.05
RETORNO_X = 4.28
TAMBO = (4.75, 3.97, 0.29)        # TK-2 200 L
PUMPS_NFT = (5.12, 3.80, 0.72, 0.30)   # esquematico: dimensionado por su rotulo, como P1/F2BOX
MESA_GERM = (5.5, 4.65, 0.6, 1.1)
MESA_COSECHA = (7.3, 7.35, 1.2, 0.6)
REFRI = (8.85, 7.3, 0.6, 0.65)
TINA = (9.7, 7.0, 0.22)
HIELERA = (7.6, 6.6, 0.35, 0.3)
COMPOSTA = (0.45, 7.55, 0.29)
CAMA1 = (6.9, 3.4, 1.0, 2.8)
CAMA2 = (8.85, 3.4, 1.0, 2.8)
CAMA3 = (1.0, 6.5, 3.1, 1.0)
GAB3 = (3.9, 7.62, 0.28, 0.28)    # driver del gantry + camara (F3)
CAM_POSTE = (4.3, 6.3)
RACK_F0 = (7.2, 7.5)
MESA_F0 = (8.4, 7.35, 1.2, 0.6)
EXT_X = 0.6                        # extractor en la cabecera oeste


def dist(pts):
    """Longitud (m) de una polilinea ortogonal (suma de tramos)."""
    return sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


def rutas(tunel):
    """Recorridos (polilineas en m) que dependen del tamano del tunel. Los usan los planos y la doc."""
    tx, ty, tw, th = tunel
    ys = ty + th                      # cara sur del tunel
    xe = tx + tw                      # cara este
    r = {}
    # troncal aerea (2.2 m): GAB-A -> mastil del cobertizo -> columna SE -> cabecera este -> GAB-1
    r["troncal"] = [(GABA[0] + 0.2, GABA[1]), (MASTIL[0], MASTIL[1]), (MASTIL[0], ys), (xe + 0.08, ys), (xe + 0.08, GAB1[1] + 0.14)]
    # 127 V a T8/extractor: larguero norte (2.0 m) desde la columna NE hasta el extractor
    r["t8"] = [(xe - 0.1, ty + 0.13), (tx + 0.25, ty + 0.13), (tx + 0.25, ty + th / 2 - 0.15)]
    # 12 V GAB-1 -> P-1 (cabecera este a 2 m, sobre el dintel de la puerta)
    r["dc_p1"] = [(xe - 0.1, GAB1[1] + 0.28), (xe - 0.1, P1[1] + 0.12), (P1[0], P1[1] + 0.12)]
    # riego: P-1 -> cabecera este -> larguero norte -> risers por rack
    r["riego"] = [(P1[0], P1[1] + 0.06), (xe - 0.18, P1[1] + 0.06), (xe - 0.18, ty + 0.22), (RACK_XS[0], ty + 0.22)]
    # drenaje: colectoras -> pared norte (piso) -> cabecera este -> sale a y=3.1 -> barda este -> coladera
    r["dren"] = [(RACK_XS[0], ty + 0.1), (xe - 0.28, ty + 0.1), (xe - 0.28, 3.1), (9.85, 3.1), (9.85, 0.6), (COLADERA[0] + 0.1, COLADERA[1] + 0.1)]
    # red SACMEX: toma -> barda este -> flotador FV-1 (aereo 1.5 m sobre la base)
    r["red"] = [(TOMA[0], TOMA[1] - 0.09), (9.9, TOMA[1] - 0.09), (9.9, TINACO[1]), (TINACO[0] + TINACO[2], TINACO[1])]
    # canalones y bajantes
    r["canal_n"] = [(tx, ty - 0.08), (xe, ty - 0.08)]
    r["canal_s"] = [(tx, ys + 0.08), (xe, ys + 0.08)]
    r["colector_se"] = [(xe + 0.16, ys + 0.08), (xe + 0.16, ty - 0.08)]
    r["tramo_3"] = [(xe, ty - 0.08), (TLALOQUE[0] + 0.15, ty - 0.08), (TLALOQUE[0] + 0.15, TLALOQUE[1])]
    r["rebosadero"] = [(TINACO[0] + 0.45, TINACO[1] - 0.4), (COLADERA[0] - 0.05, COLADERA[1] + 0.15)]
    # Fase 2
    r["llenado"] = [(F2BOX[0] + 0.2, F2BOX[1] + F2BOX[3]), (F2BOX[0] + 0.2, 2.95), (xe - 0.4, 2.95), (xe - 0.4, 3.6), (TAMBO[0] + 0.3, 3.6), (TAMBO[0] + 0.3, TAMBO[1] - TAMBO[2])]
    r["purga"] = [(TAMBO[0] + 0.15, TAMBO[1] + TAMBO[2]), (TAMBO[0] + 0.15, 4.36), (xe - 0.28, 4.36), (xe - 0.28, 3.1)]
    r["subida"] = [(PUMPS_NFT[0] + 0.1, PUMPS_NFT[1]), (PUMPS_NFT[0] + 0.1, 3.64), (MANIFOLD_X, 3.64)]
    r["bus12"] = [(GABDC[0] + 0.2, GABDC[1]), (MASTIL[0], MASTIL[1]), (MASTIL[0], ys), (xe - 0.15, ys - 0.06), (5.35, ys - 0.06), (5.35, PUMPS_NFT[1] + PUMPS_NFT[3])]
    r["bus_gab2"] = [(5.35, ys - 0.06), (GAB2[0] + GAB2[2], ys - 0.06)]
    # Fase 3
    r["goteo_e"] = [(F2BOX[0] + 0.3, F2BOX[1] + F2BOX[3]), (F2BOX[0] + 0.3, 2.85), (CAMA1[0] + 0.5, 2.85), (CAMA1[0] + 0.5, CAMA1[1] + 0.3)]
    r["goteo_e2"] = [(F2BOX[0] + 0.3, 2.85), (CAMA2[0] + 0.5, 2.85), (CAMA2[0] + 0.5, CAMA2[1] + 0.3)]
    r["goteo_s"] = [(xe + 0.08, 2.85), (xe + 0.08, ys + 0.18), (CAMA3[0] + CAMA3[2], ys + 0.18), (CAMA3[0] + CAMA3[2], CAMA3[1] + 0.3)]
    r["gantry_12v"] = [(GABDC[0], GABDC[1] + 0.15), (GAB3[0] + GAB3[2], GABDC[1] + 0.15)]
    return r


def base_comun(p: Plano):
    """Lo que existe en todas las fases: patio, casa, coladera, toma, contacto, cobertizo, cerebro."""
    p.patio()
    p.coladera(*COLADERA)
    p.mtext(COLADERA[0] - 0.22, COLADERA[1] + 0.06, "coladera", size=9.5, fill=BLUE, anchor="end")
    x, y, w, h = COBERTIZO
    p.mrect(x, y, w, h, fill="url(#roof)", stroke="none")
    p.mrect(x, y, w, h, fill=WHITE, stroke="none", opacity=0.65)
    p.mrect(x, y, w, h, fill="none", stroke=GRAY, sw=1.5, dash=DASH)
    # La toma de agua cae DENTRO del cobertizo, asi que se dibuja despues de el:
    # antes iba antes y el rayado del techo mas el velo blanco al 65 % se comian
    # el circulo y la "T" por completo. Se veia como una mancha azul lavada.
    p.toma(*TOMA)
    p.mtext(x + w - 0.05, y + 0.16, f"COBERTIZO existente (supuesto) {fmt(w)}×{fmt(h)} m", size=9.5, fill=GRAY, anchor="end")
    cx, cy, cw, ch = CDC
    p.mrect(cx, cy, cw, ch, fill=WHITE, stroke=AMBER, sw=1.5)
    p.mtext(cx + cw / 2, cy + 0.13, "centro de carga", size=9, fill=AMBER, anchor="middle")
    bx, by, bw, bh = CEREBRO
    p.mrect(bx, by, bw, bh, fill=WHITE, stroke=AMBER, sw=1.2, dash=DOT)
    # Dos lineas DENTRO del recuadro: en una sola el rotulo medía 287 u en una caja de 230 y
    # ademas su relleno blanco se comia el final de "CASA (pared sur)".
    p.mlines(bx + bw / 2, by + 0.155, ["cerebro (interior):", "mini-PC HA + router + UPS"],
             size=9, fill=AMBER, anchor="middle", lh=10.5)


def seguridad_electrica(p: Plano):
    """QO120GFI, contacto WR in-use, varilla de tierra y GAB-A (desde Fase 1)."""
    cx, cy, cw, ch = CDC
    p.mtext(cx + cw / 2, cy + 0.32, "+ QO120GFI 20 A", size=9, fill=AMBER, anchor="middle", weight="bold")
    p.contacto(*CONTACTO)
    vx, vy = VARILLA
    p.mcircle(vx, vy, 0.07, fill=WHITE, stroke=AMBER, sw=1.5)
    for i, ww in enumerate((0.14, 0.09, 0.04)):
        p.mline(vx - ww / 2, vy + 0.1 + i * 0.045, vx + ww / 2, vy + 0.1 + i * 0.045, stroke=AMBER, sw=1.2)
    p.mline(vx, vy, cx + 0.05, cy, stroke=AMBER, sw=1, dash=DOT)
    p.gabinete(*GABA, "GAB-A (CA)", side=True)
    p.mline(CONTACTO[0], CONTACTO[1] - 0.1, GABA[0] + GABA[2], GABA[1] + 0.2, stroke=AMBER, sw=1.6)


def agua_base(p: Plano, tunel, R):
    """Tinaco, captacion, red, riego y drenaje (Fase 1 en adelante)."""
    tx, ty, tw, th = tunel
    p.mpoly(R["canal_n"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["canal_s"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["colector_se"], stroke=BLUE, sw=1.5, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["tramo_3"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mtext(tx + 0.1, ty - 0.14, f"canalón PVC · {fmt(tw)} m · pendiente 0.5–1 % → bajante NE", size=9, fill=BLUE)
    p.mtext(tx + 0.1, ty + th + 0.3, f"canalón sur · {fmt(tw)} m → bajante SE → colector 2\" (cabecera este, 2 m)", size=9, fill=BLUE)
    lx, ly, lw, lh = TLALOQUE
    p.mrect(lx, ly, lw, lh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(lx + lw / 2, ly + 0.14, ["SP-1", "tlaloque", "+ filtro"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.tinaco(*TINACO, ["TK-1 tinaco", "750 L · opaco", "base firme", "LT-1 · TT-1", "en la tapa"])
    p.mpoly(R["rebosadero"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mpoly(R["red"], stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(9.98, 4.6, f"red ½\" ≈ {fmt(dist(R['red']))} m → FV-1 flotador (solo rellena, tandeo)", size=9, fill=BLUE, anchor="middle", rotate=-90)
    # salida inferior -> V-1/F-1 -> tee -> P-1 (riego) | F-2 (F2)
    p.mline(TINACO[0], TINACO[1] + TINACO[2], TINACO[0], P1[1] + 0.06, stroke=BLUE, sw=2)
    p.mline(P1[0] + P1[2], P1[1] + 0.06, F2BOX[0], F2BOX[1] + 0.06, stroke=BLUE, sw=2)
    p.mtext(TINACO[0] + 0.07, P1[1] - 0.08, "V-1 + F-1", size=8.5, fill=BLUE)
    px, py, pw, ph = P1
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    # Rotulo corto: "diafragma" y "presostato (IP65)" viven en la nota clave de abajo.
    p.mlines(px + pw / 2, py + 0.105, ["P-1 12 V", "+ F-1"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mpoly(R["riego"], stroke=BLUE, sw=2, marker="arrBlue")
    for rx in RACK_XS:
        p.mline(rx + 0.457, ty + 0.22, rx + 0.457, RACK_Y + 0.3, stroke=BLUE, sw=1.2, marker="arrBlue")
    p.mpoly(R["dren"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(6.75, 3.27, f"drenaje 2\" ≈ {fmt(dist(R['dren']))} m → coladera (≥ 1 %)", size=8.5, fill=BLUE)


def racks_tunel(p: Plano, rack4=False):
    for i, rx in enumerate(RACK_XS, 1):
        p.rack(rx, RACK_Y, label=f"rack {i}" + (" (testigo MT-1…4)" if i == 3 else ""))
    p.dim_h(RACK_XS[0] + 0.914, RACK_XS[1], RACK_Y + 0.23, "0.34", size=8.5)
    x, y, w, h = MESA_SIEMBRA
    if rack4:
        p.rack(x + 0.1, RACK_Y, label="rack 4 (opc.)", dashed=True)
    else:
        p.mesa(x, y, w, h, ["mesa de siembra", "1.2×0.6 m", "+ tapete dic–feb"])


def electrico_tunel(p: Plano, tunel, R):
    """Troncal aerea, GAB-1, T8/extractor, 12 V a P-1, sensores."""
    tx, ty, tw, th = tunel
    p.mpoly(R["troncal"], stroke=AMBER, sw=2.4, marker="arrAmber")
    p.poste(*MASTIL, size=0.1)
    # Alineado por la derecha, no centrado: centrado se lo partia en dos el bus 12 V que baja
    # a P-1 (x = 6.5) y, puesto arriba, caia sobre el canalon y el punto de la ESP32-CAM.
    p.gabinete(*GAB1, "GAB-1 (CC)", dx=0.01, anchor="end")
    p.mpoly(R["t8"], stroke=AMBER, sw=1.6, marker="arrAmber")
    for rx in RACK_XS:
        p.mline(rx + 0.2, ty + 0.13, rx + 0.2, RACK_Y - 0.02, stroke=AMBER, sw=1.1, marker="arrAmber")
    ex, ey = EXT_X, ty + th / 2
    p.mcircle(ex, ey, 0.14, fill=WHITE, stroke=AMBER, sw=1.5)
    for a in (0, 120, 240):
        p.add(f'<path d="M{fmt(p.X(ex))},{fmt(p.Y(ey))} l{fmt(0.11 * S)},0 a{fmt(0.05 * S)},{fmt(0.05 * S)} 0 0 1 '
              f'-{fmt(0.055 * S)},{fmt(0.09 * S)} z" fill="{AMBER}" fill-opacity="0.5" stroke="none" '
              f'transform="rotate({a} {fmt(p.X(ex))} {fmt(p.Y(ey))})"/>')
    p.mtext(ex - 0.15, ey, "extractor", size=9, fill=AMBER, anchor="middle", rotate=-90)
    p.mpoly(R["dc_p1"], stroke=AMBER, sw=1.5, dash=DASH, marker="arrAmber")
    sx_, sy_ = (3.05, 3.97) if th > 4 else (tx + tw / 2, ty + th / 2 + 0.35)
    p.mcircle(sx_, sy_, 0.05, fill=AMBER, stroke=AMBER)
    p.mtext(sx_ + 0.1, sy_ + 0.04, "SHT31 T/HR a 1.5 m", size=9, fill=AMBER)
    p.mline(TINACO[0] - 0.3, TINACO[1] - 0.2, GAB1[0] + 0.28, GAB1[1] + 0.2, stroke=AMBER, sw=1, dash=DOT)


def zona_cosecha(p: Plano, refri=False, gabdc=False):
    x, y, w, h = MESA_COSECHA
    p.mesa(x, y, w, h, ["mesa cosecha", "y empaque", "inox/polietileno"])
    if refri:
        rx, ry, rw, rh = REFRI
        p.mrect(rx, ry, rw, rh, fill=WHITE, stroke=INK, sw=1.5)
        p.mline(rx, ry + 0.2, rx + rw, ry + 0.2, sw=0.8)
        p.mlines(rx + rw / 2, ry + 0.34, ["refri", "4–5 °C"], size=8.5, anchor="middle", lh=10)
        p.contacto(*CONTACTO2)
    tx_, ty_, tr = TINA
    p.mcircle(tx_, ty_, tr, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mline(TOMA[0], TOMA[1] - 0.09, tx_, ty_ + tr, stroke=BLUE, sw=1.2)
    p.mtext(tx_ - 0.3, ty_ - tr - 0.12, "tina + lavamanos", size=8.5, fill=BLUE, anchor="end")
    hx, hy, hw, hh = HIELERA
    p.mrect(hx, hy, hw, hh, fill=WHITE, stroke=INK, sw=1.2)
    p.mtext(hx + hw / 2, hy + hh + 0.13, "hielera 45–50 L", size=8.5, anchor="middle")
    cx, cy, cw, ch = COBERTIZO
    p.mline(cx, cy, cx + cw, cy, stroke=GREEN, sw=1.5, dash="2 4")
    p.mline(cx, cy, cx, cy + ch, stroke=GREEN, sw=1.5, dash="2 4")
    if gabdc:
        p.gabinete(*GABDC, "GAB-DC", above=True)


def composta(p: Plano):
    p.tambo(*COMPOSTA, ["composta"], color=GREEN)


# ----------------------------------------------------------------------------- fases
NOTA_SUPUESTO = ("SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, zaguán al NORTE, coladera en la esquina NE, losa de concreto, cobertizo de 3.5 × 1.7 m en la esquina SE. "
                 "Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera; las reglas de abajo deben sobrevivir al cambio.")


def fase0():
    p = Plano(0, "Rack Husky bajo el cobertizo + mesa de siembra + toma de agua · sin túnel ni automatización · validación comercial (semanas 1–6)")
    base_comun(p)
    p.contacto(*CONTACTO)
    rx, ry = RACK_F0
    p.rack(rx, ry, label="")
    p.mtext(rx + 0.457, ry - 0.1, "rack Husky 183×91×46", size=9.5, fill=GREEN, anchor="middle")
    p.mesa(*MESA_F0, ["mesa de siembra", "1.2×0.6 m", "báscula · H2O2"])
    tx_, ty_, tr = TINA
    p.mcircle(tx_, ty_, tr, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mline(TOMA[0], TOMA[1] - 0.09, tx_, ty_ + tr, stroke=BLUE, sw=1.2)
    p.mtext(9.95, 6.6, "tina + cubeta de remojo", size=8.5, fill=BLUE, anchor="end")
    p.mcircle(0.5, 7.5, 0.2, fill=WHITE, stroke=INK, sw=1.2)
    p.mtext(0.5, 7.2, "cubeta sustrato usado", size=8.5, anchor="middle")
    p.dim_v(6.55, 7.5, 6.85, "≥ 0.9 pasillo", size=9)
    p.dim_h(rx + 0.914, TOMA[0], 6.85, "1.6 m a la toma (< 10 m)", size=9)
    # reservas
    tx, ty, tw, th = TUNEL_F1
    p.mrect(tx, ty, tw, th, fill="none", stroke=GRAY, sw=1.5, dash=DASH)
    p.mtext(tx + tw / 2, ty + th / 2 - 0.1, "RESERVA · túnel 3×6 m de Fase 1", size=11, fill=GRAY, anchor="middle", weight="bold")
    p.mtext(tx + tw / 2, ty + th / 2 + 0.15, "trazar con hilo y escuadra 3-4-5 desde ahora; no estorbar con nada pesado", size=10, fill=GRAY, anchor="middle")
    p.mrect(tx, ty + th, tw, 2.0, fill="none", stroke=GRAY, sw=1, dash="2 4")
    p.mtext(tx + tw / 2, 4.85, "ampliación Fase 2 (+2 m al sur)", size=9.5, fill=GRAY, anchor="middle")
    p.mcircle(*TINACO, fill="none", stroke=GRAY, sw=1, dash=DASH)
    p.mtext(TINACO[0], TINACO[1] + 0.04, "reserva tinaco F1", size=9, fill=GRAY, anchor="middle")
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_h(0, tx, 6.2, "0.60", size=9)
    p.dim_h(tx, tx + tw, 0.4, "6.00", size=9)
    p.dim_v(ty, ty + th, 0.3, "3.00", size=9)
    # notas clave
    p.key(rx + 0.3, ry + 0.23, "Rack pegado a la pared sur, bajo techo: luz indirecta, sin sol de\nmediodía ni goteo. Nivelar y calzar patas; forrar entrepaños de MDF.", GREEN, dx=-0.55, dy=-0.05)
    p.key(MESA_F0[0] + 0.6, MESA_F0[1], "Mesa de siembra junto a la toma (< 10 m): remojo, pesado y\nsanitización de semilla (H2O2 3 %) con atomizador de mano. 20 charolas 10×20.", INK, dx=0.2, dy=-0.3)
    p.key(CONTACTO[0], CONTACTO[1], "Contacto existente (sin GFCI aún). T8 opcionales con timer;\nen Fase 1 se vuelve contacto GFCI in-use + tierra.", AMBER, dx=-0.6, dy=-0.35)
    p.key(tx + tw / 2, ty + 0.3, "Reserva del túnel: medir aquí 3 días T mín/máx (ideal 16–24 °C)\ny luz con Photone (100–200 µmol/m²s); diagonales iguales ± 1 cm;\nlosa sana ≥ 10 cm; bordes a ≥ 15 cm de cualquier ancla.", GRAY)
    p.key(COLADERA[0] - 0.5, COLADERA[1] + 0.35, "Coladera existente: probarla (10 L de golpe deben irse); nada\nla tapará: ni placas, ni tinaco, ni composta.", BLUE)
    p.key(ACCESO[0] + 0.6, 0.45, "Zaguán de 1.0 m: ¿pasa el tinaco de 750 L (Ø ≈ 1.1 m)? Si no,\nentra por la casa o se compra el de 450 L [POR VERIFICAR Ø].", INK)
    p.key(0.5, 6.9, "Sustrato usado: cubeta con tapa lejos del rack (fungus gnats);\nen Fase 1 se vuelve tambo de composta.", INK, dx=0.5, dy=-0.25)
    p.leyenda_plano()
    p.bloques([
        ("Qué hay en Fase 0 (y nada más)", [
            "1 rack Husky ($2,019) · 20 charolas · semilla · coco · báscula · atomizador · H2O2. "
            "Sin túnel, sin bomba, sin relés: la Fase 0 valida que los chefs PAGAN.",
        ]),
        ("Antes de Fase 1 (checklist de replanteo)", [
            "¿Condominio? Art. 21/23 antes de perforar (07 §9).",
            "Consumo base CFE 7 días (medidor de enchufe) y tarifa.",
            "EC/pH de la llave 3 días distintos (02 §agua).",
            "Foto de losa, coladera, toma, contacto y bardas.",
        ]),
    ])
    p.notas([
        NOTA_SUPUESTO,
        "Reglas: rack bajo techo con toma a < 10 m y contacto cerca · pasillo ≥ 0.9 m frente al rack · la reserva del túnel queda a ≥ 0.6 m de bardas y ≥ 0.8 m de la barda norte (canaleta + paso) · nada tapa la coladera.",
        "El «cerebro» del recuadro punteado (mini-PC con Home Assistant + router + UPS) va DENTRO de la casa, junto al centro de carga: seco, ventilado y con el Wi-Fi a ≤ 8 m del gabinete más lejano del patio.",
        "Fuentes: referencia/03-instalacion §0.1–0.2 · research/estructura-invernadero §d · bom/fase0.csv · referencia/07 §9. Escala 1:50 (1 m = 100 px en el SVG). Norte arriba.",
    ])
    return p


def fase1():
    p = Plano(1, "Túnel 3×6 m con 3 racks + tinaco 750 L + gabinetes IP65 + canaleta→tinaco + circuito GFCI desde la casa · meses 2–4")
    base_comun(p)
    R = rutas(TUNEL_F1)
    tx, ty, tw, th = TUNEL_F1
    p.tunel(tx, ty, tw, th, porticos=3, door=DOOR)
    racks_tunel(p)
    p.mtext(3.6, 2.85, "zona libre: carrito de charolas · lavado en seco · futuro NFT", size=9, fill=GRAY, anchor="middle")
    agua_base(p, TUNEL_F1, R)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F1, R)
    zona_cosecha(p)
    composta(p)
    p.mrect(tx, ty + th, tw, 2.0, fill="none", stroke=GRAY, sw=1.2, dash=DASH)
    p.mtext(tx + tw / 2, 4.85, "ampliación Fase 2 (+2 m al sur): fachada sur atornillada, no soldada", size=9.5, fill=GRAY, anchor="middle")
    # cotas
    p.dim_h(tx, tx + tw, 0.4, "6.00", size=9)
    p.dim_v(ty, ty + th, 0.3, "3.00", size=9)
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_h(0, tx, 6.2, "0.60", size=9)
    p.dim_v(ty + th, 8.0, 6.3, "4.20 a la casa", size=9)
    p.dim_h(tx + tw, TINACO_BASE[0], 1.62, "0.90 paso", size=8.5)
    p.dim_v(COLADERA[1] + 0.15, TINACO_BASE[1], 9.4, "0.40", size=8.5)
    p.mtext(tx + tw + 0.12, DOOR[0] - 0.06, "puerta 0.9", size=8.5, fill=GRAY)
    # notas clave
    p.key(tx + 1.6, ty + th - 0.35, "Túnel 18 m²: 3 pórticos (6 columnas a 3 m) con placa + 4 anclas de\ncuña 3/8\"×5\"; puerta al este, de frente al zaguán y al tinaco.", INK)
    p.key(RACK_XS[1] + 0.457, RACK_Y + 0.23, "3 racks Husky en fila contra la pared norte, separados 0.34 m\n(los T8 de 1.2 m vuelan 14 cm por lado). Rack 3 = testigo con MT-1…4.", GREEN, dx=0.35, dy=0.55)
    p.key(TINACO[0], TINACO[1] + 0.35, "TK-1 750 L sobre base firme 1.3×1.3 (lleno ≈ 750 kg), opaco, a 0.4 m\nde la coladera (rebosadero) y a 0.9 m del túnel (paso libre).", BLUE, dx=-0.9, dy=0.25)
    p.key(TLALOQUE[0] + 0.15, TLALOQUE[1] - 0.2, "Canalones N y S → bajante NE → tramo 3\" a 2 m sobre el paso →\nSP-1 tlaloque (purga 20–40 L) + filtro de hojas → tapa del tinaco.", BLUE, dx=-0.7, dy=0)
    p.key(P1[0] + 0.2, P1[1] + 0.12, "P-1 bomba de diafragma 12 V con presostato, en caja IP65, + F-1 de\nsedimentos junto a la salida del tinaco;\nriego ½\" aéreo (2 m) por la cabecera este y el larguero norte → riser\npor rack → nebulizadores N1–N4 (2 boquillas/nivel).", BLUE, dx=1.55, dy=0)
    p.key(GAB1[0] + 0.14, GAB1[1] - 0.25, "GAB-1 (CC, IP65) en la columna NE a 2.0 m: ESP32 nodo-riego-v1 +\nrelé 4 ch + buck. A ≤ 3 m del rack testigo y ≤ 2 m del tinaco (LT-1);\nWi-Fi desde el cerebro ≈ 7 m con una pared.", AMBER, dx=-0.55, dy=0)
    p.key(GABA[0] + 0.2, GABA[1] - 0.3, "GAB-A (CA, IP65) en la pared bajo el cobertizo: fuente 12 V 5 A +\ncontactor K5 de T8/extractor. Cordón uso rudo 1 m al contacto WR.", AMBER, dx=-0.6, dy=0)
    p.key(MASTIL[0], MASTIL[1] - 0.5, f"Troncal aérea a 2.2 m (mensajero de acero): 127 V a T8/extractor +\n12 V a GAB-1 + señal K5. GAB-A → GAB-1 ≈ {fmt(dist(R['troncal']))} m (12 V 5 A: 10–12 AWG).", AMBER, dx=0.55, dy=0)
    p.key(CDC[0] + 0.3, CDC[1] - 0.3, "Centro de carga: breaker QO120GFI 20 A para TODO el circuito del patio;\nconduit 12 AWG al contacto WR in-use; varilla copperweld 5/8\"×3 m ≤ 25 Ω.", AMBER, dx=-0.9, dy=-0.5)
    p.key(9.85, 2.0, f"Drenaje de charolas colectoras (racks sobre bloques de 15 cm) por la\npared norte, cabecera este y barda este → coladera ≈ {fmt(dist(R['dren']))} m, ≥ 1 %.", BLUE, dx=-0.5, dy=0.4)
    p.key(MESA_COSECHA[0] + 0.1, MESA_COSECHA[1], "Cobertizo = cuarto de cosecha (NOM-251): mesa inox, tina de lavado +\nlavamanos en la toma, hielera; cortina plástica lo separa del cultivo.", INK, dx=-0.25, dy=-0.55)
    p.key(COMPOSTA[0] + 0.3, COMPOSTA[1] - 0.45, "Tambo de composta (sustrato usado 100–150 kg/mes) en la esquina\nopuesta al cultivo y a la cosecha; charola con fusarium va a la basura.", GREEN, dx=0.4, dy=0)
    p.key(EXT_X, ty + th / 2, "Extractor en la cabecera oeste (HR > 70 %); entra aire por la puerta y los\nfaldones enrollables con malla antiáfidos (laterales N y S).", AMBER, dx=0.4, dy=0.4)
    p.key(MESA_SIEMBRA[0] + 0.6, MESA_SIEMBRA[1] + 0.9, "Mesa de siembra dentro del túnel (tapete térmico dic–feb por K4).\nEn Fase 2 su lugar lo puede tomar el rack 4.", INK, dx=0, dy=0)
    p.leyenda_plano()
    p.bloques([
        ("Recorridos (m, sobre este supuesto)", [
            f"127 V troncal GAB-A → columna SE → GAB-1 ≈ {fmt(dist(R['troncal']))} · T8 larguero ≈ {fmt(dist(R['t8']))}.",
            f"12 V GAB-1 → P-1 ≈ {fmt(dist(R['dc_p1']))} · riego P-1 → rack 1 ≈ {fmt(dist(R['riego']))} (+ 3 risers).",
            f"red → FV-1 ≈ {fmt(dist(R['red']))} · drenaje → coladera ≈ {fmt(dist(R['dren']))} · canalón 6 + 6 + colector 3.",
        ]),
    ])
    p.notas([
        NOTA_SUPUESTO,
        "Distancias mínimas: túnel ≥ 0.6 m de bardas (tensar plástico, drenaje perimetral) y ≥ 0.8 m de la barda norte · pasillo interior ≥ 0.9 m · puerta 0.9 m · paso libre túnel–tinaco 0.9 m · tinaco en piso firme sin tapar la coladera · gabinetes a ≥ 1.2 m del piso y 127 V y 12 V en cajas separadas.",
        "Nada de 127 V en el patio sin GFCI + tierra física + gabinete IP65 (NOM-001-SEDE, lugar mojado). Fuentes: referencia/03 §1 · research/instalacion-tunel-detalle §1–4 · research/estructura-invernadero · diseno/electrico §4 · diseno/hidraulico §1 y §3 · bom/fase1.csv.",
    ])
    return p


def nft_fase2(p: Plano, R):
    """Dos bancadas de 4 lineas E-O (alto al oeste), manifold, retornos, tambo, bombas, llenado y purga."""
    p.nft_bancada(BANCADA_X, BANCADA_A_Y, BANCADA_L, 4, PITCH, "A")
    p.nft_bancada(BANCADA_X, BANCADA_B_Y, BANCADA_L, 4, PITCH, "B")
    mx = MANIFOLD_X
    p.mline(mx, BANCADA_A_Y, mx, BANCADA_B_Y + 4 * PITCH, stroke=BLUE, sw=2.4)
    for by in (BANCADA_A_Y, BANCADA_B_Y):
        for i in range(4):
            cy = by + PITCH / 2 + i * PITCH
            p.mline(mx, cy, BANCADA_X, cy, stroke=BLUE, sw=1.2, marker="arrBlue")
            p.mcircle(mx, cy, 0.03, fill=WHITE, stroke=BLUE, sw=1)
    p.mtext(mx - 0.1, (BANCADA_A_Y + BANCADA_B_Y) / 2 + 0.5, "manifold ¾\" · 8 válvulas · 1–2 L/min por línea", size=9, fill=BLUE, anchor="middle", rotate=-90)
    rx = RETORNO_X
    tcx, tcy, tr = TAMBO
    p.mline(rx, BANCADA_A_Y, rx, tcy - tr, stroke=BLUE, sw=2.2)
    p.mline(rx, BANCADA_B_Y + 4 * PITCH, rx, tcy + tr, stroke=BLUE, sw=2.2)
    p.mline(rx, tcy - tr, tcx - 0.05, tcy - tr, stroke=BLUE, sw=2.2, marker="arrBlue")
    p.mline(rx, tcy + tr, tcx - 0.05, tcy + tr, stroke=BLUE, sw=2.2, marker="arrBlue")
    p.mtext(rx - 0.06, 2.72, "retorno 2\"", size=8.5, fill=BLUE, anchor="middle", rotate=-90)
    p.mcircle(rx, 3.62, 0.045, fill=AMBER, stroke=AMBER)
    p.tambo(tcx, tcy, tr, None)
    p.mtext(tcx, tcy + 0.03, "TK-2", size=9, fill=BLUE, anchor="middle", weight="bold")
    px, py, pw, ph = PUMPS_NFT
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(px + pw / 2, py + 0.105, ["P-1/P-2 12 V", "F-1 · FT-1"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mline(tcx + tr, tcy, px, tcy, stroke=BLUE, sw=2, marker="arrBlue")
    p.mpoly(R["subida"], stroke=BLUE, sw=2, marker="arrBlue")
    fx, fy, fw, fh = F2BOX
    p.mrect(fx, fy, fw, fh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(fx + fw / 2, fy + 0.105, ["F-2 dúplex", "+ SV-1 NC"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mpoly(R["llenado"], stroke=BLUE, sw=2, marker="arrBlue")
    p.mpoly(R["purga"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mesa(*MESA_GERM, ["germinación", "y trasplante"], vertical=True)
    p.dim_v(BANCADA_A_Y + 4 * PITCH, BANCADA_B_Y, 2.4, "0.90", size=9)
    p.dim_v(RACK_Y + 0.457, BANCADA_A_Y, 5.2, "0.94", size=9)
    p.dim_h(BANCADA_X, BANCADA_X + BANCADA_L, BANCADA_A_Y - 0.18, "3.00", size=9)


def dc_first_fase2(p: Plano, R):
    """GAB-2 nodo NFT, bus 12 V desde GAB-DC (cobertizo), ESP32-CAM, panel opcional."""
    p.gabinete(*GAB2, "GAB-2 (CC)")
    p.mpoly(R["bus12"], stroke=AMBER, sw=1.8, dash=DASH, marker="arrAmber")
    p.mpoly(R["bus_gab2"], stroke=AMBER, sw=1.5, dash=DASH, marker="arrAmber")
    p.mline(RETORNO_X + 0.05, 3.66, GAB2[0] + 0.14, GAB2[1], stroke=AMBER, sw=1, dash=DOT)
    p.mtext(RETORNO_X + 0.12, 3.6, "AT-1 pH · AT-2 EC · TT-2", size=8.5, fill=AMBER)
    p.mtext(TAMBO[0] + 0.15, 4.55, "DP-1/2/3 A·B·pH− al tambo", size=8.5, fill=AMBER)
    p.mline(CONTACTO[0], CONTACTO[1] - 0.1, GABA[0] + GABA[2], GABA[1] + 0.2, stroke=AMBER, sw=1.6)
    p.mrect(7.25, 8.05, 0.95, 0.34, fill=WHITE, stroke=AMBER, sw=1.2, dash=DASH)
    p.mtext(7.725, 8.27, "PV 100 W opc.", size=8.5, fill=AMBER, anchor="middle")
    p.mline(7.25, 8.22, GABDC[0] + GABDC[2], GABDC[1] + 0.3, stroke=AMBER, sw=1.2, dash=DASH)
    cx, cy = TUNEL_F2[0] + TUNEL_F2[2], TUNEL_F2[1]
    p.mpoly([(cx, cy), (cx + 0.7, cy + 0.9), (cx + 1.1, cy + 0.15)], stroke=AMBER, sw=0.8, dash=DOT, fill=AMBER_BG, close=True)
    p.mcircle(cx, cy, 0.07, fill=AMBER, stroke=AMBER)
    p.mtext(cx + 0.3, cy + 0.2, "ESP32-CAM", size=8.5, fill=AMBER)


def fase2():
    p = Plano(2, "Túnel ampliado a 5×6 m · 8 líneas NFT de 3 m (2 bancadas de 4) · tambo 200 L · GAB-DC con batería · refrigerador y cuarto de cosecha junto a la casa · meses 5–9")
    base_comun(p)
    R = rutas(TUNEL_F2)
    tx, ty, tw, th = TUNEL_F2
    p.tunel(tx, ty, tw, th, porticos=4, door=DOOR)
    racks_tunel(p, rack4=True)
    agua_base(p, TUNEL_F2, R)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F2, R)
    nft_fase2(p, R)
    zona_cosecha(p, refri=True, gabdc=True)
    dc_first_fase2(p, R)
    composta(p)
    for (x, y, w, h) in (CAMA1, CAMA2, CAMA3):
        p.mrect(x, y, w, h, fill="none", stroke=GRAY, sw=1.2, dash=DASH)
    p.mtext(CAMA1[0] + 0.5, CAMA1[1] + 1.5, "reserva camas F3", size=9, fill=GRAY, anchor="middle", rotate=-90)
    p.mtext(CAMA3[0] + CAMA3[2] / 2, CAMA3[1] + 0.55, "reserva cama F3 + gantry", size=9, fill=GRAY, anchor="middle")
    p.dim_h(tx, tx + tw, 0.4, "6.00", size=9)
    p.dim_v(ty, ty + th, 0.3, "5.00", size=9)
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_v(ty + th, 8.0, 6.3, "2.20 a la casa", size=9)
    p.dim_h(tx + tw, TINACO_BASE[0], 1.62, "0.90 paso", size=8.5)
    p.mtext(tx + tw + 0.12, DOOR[0] - 0.06, "puerta 0.9", size=8.5, fill=GRAY)
    # notas clave
    p.key(3.0, ty + th - 0.12, "Fachada sur del túnel se mueve 2 m: 5×6 = 30 m², 4 pórticos (8 columnas\na 2 m). Las 6 bases del este/oeste se reutilizan; las 2 columnas nuevas del sur\nvan con placa + 4 anclas de cuña 3/8\"×5\" cada una, como en Fase 1. El canalón\nsur se cuelga en el alero nuevo; la bajante NE y el tinaco no se mueven.", INK)
    p.key(BANCADA_X + 1.5, BANCADA_B_Y - 0.4, "2 bancadas E–O de 4 líneas PVC sanitario 4\" × 3 m (10 canastillas a\n20 cm), alto al OESTE (manifold) y bajo al ESTE (retornos), 2–3 %;\npasillo de 0.9 m entre bancadas; la A se atiende por 2 lados, la B por 1.", GREEN)
    p.key(TAMBO[0], TAMBO[1] + 0.5, "TK-2 tambo 200 L tapado, entre los retornos; P-1/P-2 diafragma 12 V\n+ F-1 malla 120 + FT-1 al lado; subida ¾\" al pie de la bancada A hasta\nel manifold. Sondas pH/EC/T en el RETORNO; peristálticas al tambo.", BLUE, dx=0.45, dy=0.25)
    p.key(F2BOX[0] + F2BOX[2], F2BOX[1] + 0.12, f"Llenado: tinaco → F-2 dúplex (sin cloro) → SV-1 NC → tambo ≈ {fmt(dist(R['llenado']))} m.\nPurga SV-2 (cambio cada 2–3 sem) se une al drenaje ≈ {fmt(dist(R['purga']) + 6.0)} m a la coladera.", BLUE, dx=0.55, dy=0.4)
    p.key(GABDC[0] + 0.2, GABDC[1] - 0.25, "GAB-DC (CC): LiFePO4 100 Ah a 30 cm del piso + EPEVER LS2024B +\nfusiblera 6 vías, separado de GAB-A (CA: cargador). Panel 100 W opcional\nEN LA AZOTEA, nunca sobre el plástico del túnel. Bus 12 V por la troncal\naérea a bombas y GAB-2.", AMBER, dx=-0.6, dy=0)
    p.key(GAB2[0] + 0.14, GAB2[1] - 0.27, f"GAB-2 (CC) en la columna sur x = 4.6: ESP32 nodo-nft-v2 (pH/EC, MOSFET\nperistálticas, solenoides, detector CFE). Bus GAB-DC→bombas ≈ {fmt(dist(R['bus12']))} m.", AMBER, dx=0, dy=0)
    p.key(REFRI[0] + 0.3, REFRI[1] - 0.25, "Cuarto de cosecha completo: refri usado 9–11 ft³ a 4–5 °C en su\npropio contacto GFCI, mesa inox, tina/lavamanos, hielera de reparto.", INK, dx=-0.9, dy=-0.4)
    p.key(tx + tw + 0.5, ty + 0.6, "ESP32-CAM en la columna NE: puerta, zaguán y tinaco (detección\nnocturna). Nada de valor visible desde la calle; candado en el túnel.", AMBER, dx=0.3, dy=0.4)
    p.key(MESA_GERM[0] + 0.85, MESA_GERM[1] + 0.4, "Mesa de germinación (foami agrícola) y trasplante a canastilla,\njunto a la puerta y al tambo. Rack 4 opcional donde iba la mesa de siembra.", INK, dx=0, dy=0)
    p.key(9.85, 2.0, "Mismo drenaje de Fase 1: recibe además la purga del tambo (200 L\ncada 2–3 sem) y el rebosadero. Sigue sin cruzar el paso al túnel.", BLUE, dx=-0.5, dy=0.4)
    p.leyenda_plano()
    p.bloques([
        ("Recorridos nuevos (m)", [
            f"bus 12 V GAB-DC → bombas ≈ {fmt(dist(R['bus12']))} · → GAB-2 ≈ {fmt(dist(R['bus12'][:-1]) + dist(R['bus_gab2']))}.",
            f"llenado ≈ {fmt(dist(R['llenado']))} · subida ¾\" ≈ {fmt(dist(R['subida']))} · manifold 3.2 · retornos 2 × 1.6.",
            f"purga → coladera ≈ {fmt(dist(R['purga']) + 6.0)} · troncal 127 V ≈ {fmt(dist(R['troncal']))} (igual que Fase 1).",
        ]),
    ])
    p.notas([
        NOTA_SUPUESTO,
        "Separación entre líneas NFT 28 cm eje a eje (bancada 1.12 m) [POR VERIFICAR con el porte de la albahaca a 20 cm entre canastillas; con 30–35 cm la bancada sube a 1.2–1.4 m y el pasillo baja a 0.7 m].",
        "Cajas de equipo (rótulo corto en el plano): P-1/P-2 son bombas de diafragma 12 V con presostato en caja IP65; F-1 es filtro de malla 120 y FT-1 el de disco; la mesa de cosecha es de inox o polietileno de grado alimenticio.",
        "Distancias mínimas: pasillos ≥ 0.9 m · bancada atendida por un solo lado ≤ 1.2 m · tambo tapado y a la sombra (18–22 °C) · sondas en el retorno · peristálticas al tambo junto a la succión · batería a 30 cm del piso y nunca en la caja de 127 V · refri bajo techo con GFCI propio.",
        "Fuentes: referencia/03 §2 · research/hidroponia-nft · research/electrico-respaldo-seguridad §2.4 y §3.6 · research/inocuidad-operativa §4 (NOM-251) · referencia/07 §1–3 y §10 · diseno/hidraulico §2 · diseno/electrico §2–3 · bom/fase2.csv.",
    ])
    return p


def fase3():
    p = Plano(3, "Fase 2 + camas elevadas con goteo desde HA + gantry XY tipo FarmBot + cámara fija · mes 10+ · cero presión comercial")
    base_comun(p)
    R = rutas(TUNEL_F2)
    tx, ty, tw, th = TUNEL_F2
    p.tunel(tx, ty, tw, th, porticos=4, door=DOOR)
    racks_tunel(p, rack4=True)
    agua_base(p, TUNEL_F2, R)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F2, R)
    nft_fase2(p, R)
    zona_cosecha(p, refri=True, gabdc=True)
    dc_first_fase2(p, R)
    composta(p)
    areas = []
    for i, (x, y, w, h) in enumerate((CAMA1, CAMA2, CAMA3), 1):
        areas.append(w * h)
        # La cama 3 lleva la columna del gantry (relleno negro) justo en su centro: el rotulo
        # se corre al oeste o la barra se come "= 3.1 m2".
        p.cama(x, y, w, h, [f"cama {i}", f"{fmt(w)}×{fmt(h)} = {fmt(w * h)} m²"],
               cxm=x + 0.85 if i == 3 else None)
    total = sum(areas)
    p.mpoly(R["goteo_e"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mpoly(R["goteo_e2"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mpoly(R["goteo_s"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    # gantry sobre la cama 3
    x, y, w, h = CAMA3
    for yy_ in (y - 0.06, y + h + 0.06):
        p.mline(x, yy_, x + w, yy_, stroke=INK, sw=2.5)
    gxp = x + 1.9
    p.mrect(gxp - 0.05, y - 0.12, 0.1, h + 0.24, fill=INK, stroke=INK, sw=1)
    p.mcircle(gxp, y + h / 2 + 0.15, 0.08, fill=WHITE, stroke=INK, sw=1.5)
    p.mline(x + 0.3, y - 0.22, x + w - 0.3, y - 0.22, stroke=INK, sw=1, marker="arrInk")
    p.mline(x + w - 0.3, y - 0.22, x + 0.3, y - 0.22, stroke=INK, sw=1, marker="arrInk")
    p.mtext(x + w / 2, y - 0.26, "gantry XY · V-slot · NEMA17", size=9, anchor="middle")
    p.gabinete(*GAB3, "GAB-3")
    p.mpoly(R["gantry_12v"], stroke=AMBER, sw=1.4, dash=DASH, marker="arrAmber")
    p.mcircle(*CAM_POSTE, 0.07, fill=AMBER, stroke=AMBER)
    p.mpoly([CAM_POSTE, (CAM_POSTE[0] - 0.9, CAM_POSTE[1] + 0.6), (CAM_POSTE[0] - 0.6, CAM_POSTE[1] + 1.3)], stroke=AMBER, sw=0.8, dash=DOT, fill=AMBER_BG, close=True)
    p.mtext(CAM_POSTE[0] + 0.1, CAM_POSTE[1] - 0.06, "cámara fija (poste 2 m)", size=8.5, fill=AMBER)
    p.mline(COMPOSTA[0] + 0.3, COMPOSTA[1] - 0.15, CAMA3[0], CAMA3[1] + 0.8, stroke=GREEN, sw=1.2, dash=DOT, marker="arrGreen")
    p.dim_h(tx + tw, CAMA1[0], 6.27, "", size=8)
    p.mtext(CAMA1[0] + 0.04, 6.3, "0.30", size=8)
    p.dim_h(CAMA1[0] + CAMA1[2], CAMA2[0], 6.27, "0.95 pasillo", size=8.5)
    p.dim_v(ty + th, CAMA3[1], 0.4, "0.70", size=8.5)
    p.dim_h(tx, tx + tw, 0.4, "6.00", size=9)
    p.dim_v(ty, ty + th, 0.3, "5.00", size=9)
    # notas clave
    p.key(CAMA1[0] + 0.5, CAMA1[1] + 0.5, f"Camas 1–2 (1.0 m: se atienden por un lado) al este, sobre la línea de\ndrenaje; cama 3 (gantry) al sur. Total {fmt(total)} m² de {fmt(total)}: es lo que cabe con\npasillos ≥ 0.7 m. Meta 15–20 m²: ver layout-patio.md §5.", GREEN, dx=0, dy=0)
    p.key(F2BOX[0] + F2BOX[2], F2BOX[1] + 0.12, f"Goteo colgado de HA: SV-3 (12 V NC) en la caja F-2 desde el tinaco;\nramal este ≈ {fmt(dist(R['goteo_e']) + dist(R['goteo_e2']))} m y ramal sur por la troncal y el alero sur ≈ {fmt(dist(R['goteo_s']))} m.", BLUE, dx=0.55, dy=0.4)
    p.key(CAMA3[0] + 1.9, CAMA3[1] + 0.5, "Gantry XY tipo FarmBot sobre la cama 3 (la más larga): carrera ≈ 3.0 × 0.9 m,\nGAB-3 con driver + cámara en la pared de la casa, 12 V desde GAB-DC.", INK, dx=0.7, dy=0)
    p.key(CAM_POSTE[0], CAM_POSTE[1], "Cámara fija en poste de 2 m: cobertura foliar, plagas y timelapse\nde la cama 3 (visión = juguete de F3, no el negocio).", AMBER, dx=0.45, dy=0.4)
    p.key(COMPOSTA[0] + 0.35, COMPOSTA[1] - 0.4, "La composta del tambo alimenta las camas (07 §12); nunca charola con\nfusarium. Ruta corta, sin cruzar el cuarto de cosecha.", GREEN, dx=0.4, dy=0)
    p.key(GAB3[0] + 0.14, GAB3[1] - 0.25, "Regla de oro F3: ningún cable ni manguera nueva cruza pasillos a nivel\nde piso; todo aéreo (2 m) o pegado a barda/cama.", AMBER, dx=0.5, dy=0)
    p.leyenda_plano()
    p.bloques([
        ("Qué cambia vs. Fase 2", [
            f"3 camas elevadas = {fmt(total)} m² (alt. 0.7–0.9 m [POR VERIFICAR]).",
            "SV-3 + goteo por cama (timer + humedad en HA).",
            "Gantry sobre la cama 3; GAB-3 driver; cámara fija.",
            "Nada de esto es el negocio: sólo si Fases 1–2 se pagan.",
        ]),
    ])
    p.notas([
        NOTA_SUPUESTO,
        "La estructura del túnel no cambia respecto a Fase 2: 4 pórticos (8 columnas a 2 m), cada columna con placa + 4 anclas de cuña 3/8\"×5\" sobre losa sana de ≥ 10 cm y a ≥ 15 cm del borde.",
        "Cajas de equipo (rótulo corto en el plano): P-1/P-2 son bombas de diafragma 12 V con presostato en caja IP65; F-1 es filtro de malla 120 y FT-1 el de disco; SV-3 es el solenoide 12 V NC del goteo, dentro de la caja F-2; la mesa de cosecha es de inox o polietileno de grado alimenticio.",
        "Las camas van pegadas a la barda este y a la casa y se atienden por un solo lado: por eso miden ≤ 1.0 m de ancho. Cama 3 deja libre la puerta casa→patio y 0.7 m de paso frente al túnel.",
        "[POR VERIFICAR] altura y material de cama (0.7–0.9 m: madera tratada/PTR + geomembrana), perfil V-slot y carrera del gantry, caudal de goteo por cama: no están en la fuente de verdad; el plan maestro sólo fija 'camas elevadas con goteo colgado de HA' y 'gantry XY V-slot + NEMA17 + GRBL/Klipper'.",
        "Fuentes: referencia/00-plan-maestro §Fase 3 · referencia/07 §12 y §14 · research/hidroponia-nft (periférica sólo para riego presurizado de camas) · plantas de Fases 1–2.",
    ])
    return p


# ----------------------------------------------------------------------------- alzado del rack
K = 4.0  # px por cm (1:10)

RACK_H, RACK_W, RACK_D = 183.0, 91.4, 45.7   # cm (Husky 5 niveles, Home Depot $2,019; 362.9 kg/repisa)
SHELF_T = 2.5                                # espesor del entrepano MDF + forro [POR VERIFICAR en caja]
SHELF_TOPS = (10.0, 53.0, 96.0, 139.0, 182.0)  # cara superior de N1..N5 desde el piso (paso 43 cm; ajustable)
TRAY_W, TRAY_L, TRAY_H = 25.4, 50.8, 6.0     # charola 1020 (doble: perforada dentro de lisa)
TUBE_L, TUBE_D = 120.0, 2.6                  # T8 LED 18 W 120 cm (JWJ, bom/fase1)
CANOPY = {1: 9.0, 2: 8.0, 3: 5.0, 4: 2.0}    # altura del dosel dibujada por nivel en luz (cm); N5 va tapado
DARK = "#374151"
SHELF = "#d1d5db"
WEIGHT = "#9ca3af"
TUBE_BG = "#fef3c7"

# Flujo de charolas por nivel (SOP 03 §0.3; zonas 03 §0.2: superior = oscuridad, medios = desarrollo).
# En el dibujo va solo el rotulo corto junto a su nivel; la explicacion completa (FLUJO_MD) sale
# a rack-alzado.notas.md, donde se lee a 16 px en vez de a 6.
FLOW = {
    5: ["① SIEMBRA · día 0", "N5 oscuridad"],
    4: ["② DESTAPE · día 2–4", "N4 brote"],
    3: ["③ DESARROLLO · día 4–8"],
    2: ["④ ACABADO · día 8–10"],
    1: ["⑤ COSECHA · día 8–12"],
}
FLUJO_MD = [
    "**① Siembra, día 0 → N5, oscuridad** (arriba es lo más cálido): 3 pilas de 2–3 charolas tapadas "
    "con peso de 2–4 kg, 2–4 días; atomizar a mano 1–2 veces al día.",
    "**② Destape, día 2–4 → N4, brote:** luz indirecta + T8 12–14 h; desde aquí el riego es SOLO por "
    "abajo (charola perforada dentro de la lisa).",
    "**③ Desarrollo, día 4–8 → N3:** tallo y cotiledón abiertos.",
    "**④ Acabado, día 8–10 → N2:** color y densidad finales.",
    "**⑤ Cosecha, día 8–12 → N1** (abajo es lo más fresco): suspender el riego 12–24 h antes; tijera "
    "sobre el sustrato la mañana de la entrega.",
    "Cada charola **baja un nivel por etapa**: se siembra a la altura de los ojos y se cosecha a la "
    "altura de la mano.",
]


def rack_alzado():
    # Lienzo estrecho y dos bandas: arriba el alzado frontal, el flujo y la vista lateral;
    # abajo la planta de un nivel. Las tablas y la leyenda, que antes ocupaban la columna de la
    # derecha, salen a rack-alzado.notas.md. MEDIDO: el dibujo mas al este es la linea de piso
    # de la vista lateral, en x1 + RACK_D*K + 60 = 1122.8; con 27 u de margen, W = 1150.
    W = 1150
    SUB = ("charolas 10×20 (25.4×50.8 cm) · 3 por nivel · T8 18 W ×2 y nebulizadores en "
           "N1–N4 · oscuridad arriba (N5) · cosecha abajo (N1) · cotas en cm")
    head = head_rule_y(SUB, W)
    # El dibujo mas alto no es el rack (183 cm) sino la banda de blackout, que sube 21 cm
    # sobre el entrepano N5 (182 cm) -> 203 cm. Colgar el piso de 205 cm deja la banda bajo
    # la linea de cabecera en vez de encimarla.
    floor = head + 50 + 205 * K
    banda2 = floor + 162                    # arranque de la segunda banda (planta de un nivel)
    H = int(banda2 + RACK_D * K + 2.5 * K + 76)
    s = SVG(W, H, "Alzado · Rack Husky 183×91×46 cm · 5 niveles · escala 1:10", SUB)
    s.md_toc = "alzado del rack"

    def yc(cm):
        return floor - cm * K

    def charola(x, top, w, fill=WHITE, sw=1.4):
        """Charola doble (perforada dentro de lisa) vista de canto: contorno + labio interior."""
        s.rect(x, yc(top + TRAY_H), w * K, TRAY_H * K, fill=fill, stroke=GREEN, sw=sw)
        s.rect(x + 1.0 * K, yc(top + TRAY_H - 0.6), (w - 2.0) * K, (TRAY_H - 1.6) * K, fill="#f1f8e9", stroke=GREEN, sw=0.8)

    def pila_tapada(x, top, w):
        """Dos charolas apiladas (la de arriba invertida) + peso de 2-4 kg (N5)."""
        for st in range(2):
            s.rect(x, yc(top + TRAY_H * (st + 1)), w * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
        s.rect(x + w * 0.25 * K, yc(top + 2 * TRAY_H + 5), w * 0.5 * K, 5 * K, fill=WEIGHT, stroke=INK, sw=1)
        s.text(x + w * 0.5 * K, yc(top + 2 * TRAY_H + 1.5), "2–4 kg", size=8, anchor="middle", fill=WHITE)

    def boquilla(bx, ny):
        s.polyline([(bx - 4, ny), (bx + 4, ny), (bx, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
        for dx in (-10, 0, 10):
            s.line(bx, ny + 10, bx + dx, ny + 22, stroke=BLUE, sw=0.7, dash="2 2")

    # ---------------- vista frontal
    x0 = 130.0
    wpx = RACK_W * K
    s.text(x0 - 80, head + 28, "VISTA FRONTAL (desde el pasillo)", size=12, weight="bold")
    s.line(x0 - 80, floor, x0 + wpx + 120, floor, sw=2)
    s.text(x0 - 80, floor + 16, "piso nivelado + bloques macizos de 15 cm bajo las patas", size=9.5, fill=GRAY)
    s.rect(x0 - 6, floor - 4 * K, wpx + 12, 4 * K, fill=BLUE_BG, stroke=BLUE, sw=1.2)
    s.text(x0 + wpx + 16, floor - 4, "colectora → coladera", size=10, fill=BLUE)
    for px in (x0, x0 + wpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    gap = (RACK_W - 3 * TRAY_W) / 4
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x0, yc(top), wpx, SHELF_T * K, fill=SHELF, stroke=INK, sw=1.5)
        s.text(x0 - 12, yc(top) + 4, f"N{i}", size=12, weight="bold", anchor="end")
        for k in range(3):
            tx = x0 + (gap + k * (TRAY_W + gap)) * K
            if i <= 4:
                charola(tx, top, TRAY_W)
                c = CANOPY[i]
                s.rect(tx + 0.8 * K, yc(top + TRAY_H + c), (TRAY_W - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
            else:
                pila_tapada(tx, top, TRAY_W)
        if i <= 4:
            # sensor capacitivo en la charola testigo (la primera) de cada nivel en luz
            tx = x0 + gap * K
            s.line(tx + 4 * K, yc(top + TRAY_H + 6), tx + 4 * K, yc(top + 1), stroke=AMBER, sw=2.5)
            s.text(tx + 5 * K, yc(top + TRAY_H + 5), f"MT-{i}", size=8.5, fill=AMBER)
            # T8 x2 bajo el entrepano de arriba + linea de nebulizadores
            nxt = SHELF_TOPS[i] - SHELF_T
            ty = yc(nxt - 3.0)
            tl = x0 + wpx / 2 - TUBE_L * K / 2
            s.rect(tl, ty, TUBE_L * K, TUBE_D * K, fill=TUBE_BG, stroke=AMBER, sw=1.4, rx=5)
            s.text(tl + TUBE_L * K + 6, ty + 9, "T8 ×2", size=8.5, fill=AMBER)
            ny = ty + TUBE_D * K + 2.0 * K
            s.line(x0, ny, x0 + wpx, ny, stroke=BLUE, sw=1.6)
            for q in (0.25, 0.75):
                boquilla(x0 + wpx * q, ny)
    # zona blackout
    s.rect(x0 - 6, yc(SHELF_TOPS[4] + 21), wpx + 12, 21 * K, fill=DARK, stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    s.text(x0 + wpx / 2, yc(SHELF_TOPS[4] + 17.5), "ZONA BLACKOUT · cubierta opaca (lona/cartón) · sin T8", size=9.5, anchor="middle", weight="bold")
    # SHT31 en el poste izquierdo a 1.0 m
    s.circle(x0 + wpx - 7, yc(110), 5, fill=AMBER, stroke=AMBER)
    s.text(x0 + wpx + 14, yc(110), "SHT31 T/HR · poste · 1.1 m", size=8.5, fill=AMBER, anchor="middle", rotate=-90)
    # cotas frontales
    dx = x0 - 60
    s.line(dx, yc(0), dx, yc(RACK_H), sw=1)
    for cm in (0, RACK_H):
        s.line(dx - 5, yc(cm), dx + 5, yc(cm), sw=1)
    s.text(dx - 8, yc(RACK_H / 2), "183", size=11, anchor="middle", rotate=-90)
    dx2 = x0 - 36
    s.line(dx2, yc(SHELF_TOPS[1]), dx2, yc(SHELF_TOPS[2]), sw=1)
    for cm in (SHELF_TOPS[1], SHELF_TOPS[2]):
        s.line(dx2 - 5, yc(cm), dx2 + 5, yc(cm), sw=1)
    s.text(dx2 - 6, yc((SHELF_TOPS[1] + SHELF_TOPS[2]) / 2), "43 (≥ 30 ✓)", size=9.5, anchor="middle", rotate=-90)
    by = floor + 44   # bajo el rotulo del piso, que es largo
    s.line(x0, by, x0 + wpx, by, sw=1)
    s.line(x0, by - 5, x0, by + 5, sw=1); s.line(x0 + wpx, by - 5, x0 + wpx, by + 5, sw=1)
    s.text(x0 + wpx / 2, by - 4, "91.4", size=11, anchor="middle")
    tl = x0 + wpx / 2 - TUBE_L * K / 2
    by2 = floor + 66
    s.line(tl, by2, tl + TUBE_L * K, by2, stroke=AMBER, sw=1)
    s.line(tl, by2 - 5, tl, by2 + 5, stroke=AMBER, sw=1); s.line(tl + TUBE_L * K, by2 - 5, tl + TUBE_L * K, by2 + 5, stroke=AMBER, sw=1)
    s.text(x0 + wpx / 2, by2 - 4, "T8 120 (vuela 14.3 por lado → racks en fila separados ≥ 30 cm)", size=10, fill=AMBER, anchor="middle")
    top3 = SHELF_TOPS[2]
    tube_bottom = SHELF_TOPS[3] - SHELF_T - 3.0 - TUBE_D
    canopy_top = top3 + TRAY_H + CANOPY[3]
    xr = x0 - 36
    s.line(xr, yc(tube_bottom), xr, yc(canopy_top), stroke=AMBER, sw=1)
    for cm in (tube_bottom, canopy_top):
        s.line(xr - 5, yc(cm), xr + 5, yc(cm), stroke=AMBER, sw=1)
    s.text(xr - 6, yc((tube_bottom + canopy_top) / 2), f"luz→dosel {fmt(tube_bottom - canopy_top)}", size=9, fill=AMBER, anchor="middle", rotate=-90)
    # flujo de charolas (columna a la derecha del rack): de N5 hacia N1
    fx = x0 + wpx + 100   # a la derecha de los rotulos 'T8 x2', que vuelan con el tubo
    for i, top in enumerate(SHELF_TOPS, 1):
        s.lines(fx, yc(top + 16), FLOW[i], size=9.5, fill=GREEN, lh=12)
        if i > 1:
            y_from = yc(top + 16) + 12 * FS * len(FLOW[i]) - 4
            y_to = yc(SHELF_TOPS[i - 2] + 16) - 14
            s.line(fx + 6, y_from, fx + 6, y_to, stroke=GREEN, sw=1.2, marker="arrGreen", dash="3 3")

    # ---------------- vista lateral
    x1 = 880.0
    dpx = RACK_D * K
    s.text(x1, head + 28, "VISTA LATERAL", size=12, weight="bold")
    s.line(x1 - 30, floor, x1 + dpx + 60, floor, sw=2)
    for px in (x1, x1 + dpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    s.line(x1 - 10, yc(SHELF_TOPS[0]), x1 - 10, yc(SHELF_TOPS[4] - SHELF_T - 6), stroke=BLUE, sw=2)
    s.text(x1 - 16, yc(60), "riser ½\" nebulizadores desde P-1", size=9, fill=BLUE, anchor="middle", rotate=-90)
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x1, yc(top), dpx, SHELF_T * K, fill=SHELF, stroke=INK, sw=1.5)
        if i <= 4:
            s.rect(x1 - 2.5 * K, yc(top + TRAY_H), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.4)
            c = CANOPY[i]
            s.rect(x1 - 1.7 * K, yc(top + TRAY_H + c), (TRAY_L - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
            nxt = SHELF_TOPS[i] - SHELF_T
            for q in (0.25, 0.75):
                s.circle(x1 + dpx * q, yc(nxt - 3.0 - TUBE_D / 2), TUBE_D * K / 2, fill=TUBE_BG, stroke=AMBER, sw=1.4)
            ny = yc(nxt - 3.0 - TUBE_D - 2.0)
            s.line(x1 - 10, ny, x1 + dpx * 0.5, ny, stroke=BLUE, sw=1.6)
            s.polyline([(x1 + dpx * 0.5 - 4, ny), (x1 + dpx * 0.5 + 4, ny), (x1 + dpx * 0.5, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
        else:
            for st in range(2):
                s.rect(x1 - 2.5 * K, yc(top + TRAY_H * (st + 1)), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
            s.rect(x1 + 12 * K, yc(top + 2 * TRAY_H + 5), 26 * K, 5 * K, fill=WEIGHT, stroke=INK, sw=1)
    s.rect(x1 - 12, yc(SHELF_TOPS[4] + 22), dpx + 24, 22 * K, fill=DARK, stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    by = floor + 44
    s.line(x1, by, x1 + dpx, by, sw=1); s.line(x1, by - 5, x1, by + 5, sw=1); s.line(x1 + dpx, by - 5, x1 + dpx, by + 5, sw=1)
    s.text(x1 + dpx / 2, by - 4, "45.7", size=11, anchor="middle")
    by2 = floor + 66
    s.line(x1 - 2.5 * K, by2, x1 - 2.5 * K + TRAY_L * K, by2, stroke=GREEN, sw=1)
    for px in (x1 - 2.5 * K, x1 - 2.5 * K + TRAY_L * K):
        s.line(px, by2 - 5, px, by2 + 5, stroke=GREEN, sw=1)
    s.text(x1 + dpx / 2, by2 - 4, "charola 50.8 (vuela 5.1: 2.5 por lado)", size=10, fill=GREEN, anchor="middle")
    s.text(x1 + dpx / 2, floor + 90, "◄ atrás (pared, riser)   ·   frente (pasillo) ►", size=9, fill=GRAY, anchor="middle")

    # ---------------- planta de un nivel (segunda banda, bajo el alzado)
    x2, y2 = (W - RACK_W * K) / 2, banda2
    s.text(x2, banda2 - 32, "PLANTA DE UN NIVEL (N1–N4)", size=12, weight="bold")
    s.rect(x2, y2, wpx, dpx, fill=SHELF, stroke=INK, sw=1.5)
    for k in range(3):
        tx = x2 + (gap + k * (TRAY_W + gap)) * K
        s.rect(tx, y2 - 2.5 * K, TRAY_W * K, TRAY_L * K, fill="#f1f8e9", stroke=GREEN, sw=1.4)
        s.text(tx + TRAY_W * K / 2, y2 + dpx / 2 + 4, f"{k + 1}", size=11, fill=GREEN, anchor="middle", weight="bold")
    for q in (0.25, 0.75):
        s.line(x2 + wpx / 2 - TUBE_L * K / 2, y2 + dpx * q, x2 + wpx / 2 + TUBE_L * K / 2, y2 + dpx * q, stroke=AMBER, sw=3, dash="8 4")
    s.line(x2, y2 + 6, x2 + wpx, y2 + 6, stroke=BLUE, sw=1.6)
    for q in (0.25, 0.75):
        s.circle(x2 + wpx * q, y2 + 6, 4, fill=BLUE, stroke=BLUE)
    s.text(x2 + wpx / 2, y2 - 16, "atrás: línea de nebulizadores (2 boquillas)", size=9, fill=BLUE, anchor="middle")
    s.text(x2 + wpx / 2, y2 + dpx + 2.5 * K + 14, "frente: volado 2.5", size=9, fill=GREEN, anchor="middle")
    s.text(x2 + 6, y2 + dpx * 0.25 - 5, "T8 ×2 (120 cm)", size=9, fill=AMBER)
    by = y2 + dpx + 2.5 * K + 42
    s.line(x2, by, x2 + wpx, by, sw=1); s.line(x2, by - 5, x2, by + 5, sw=1); s.line(x2 + wpx, by - 5, x2 + wpx, by + 5, sw=1)
    s.text(x2 + wpx / 2, by - 4, "91.4 = 3 × 25.4 + 4 × 3.8", size=10, anchor="middle")

    # ---------------- leyenda, flujo y tablas: fuera del dibujo, a rack-alzado.notas.md
    s.leyenda([
        "**Rectángulo blanco con borde verde** — charola 1020 doble (perforada dentro de lisa).",
        "**Achurado verde sobre la charola** — dosel: brote (2 cm) → cosecha (8–9 cm).",
        "**Barra crema con borde ámbar** — tubo LED T8 18 W 120 cm (127 V vía K5, GAB-A).",
        "**Línea ámbar vertical corta** — sensor MT-x capacitivo · SHT31.",
        "**Línea azul con ▼** — línea ½\" de nebulizadores (P-1 12 V) y su boquilla.",
        "**Banda azul claro bajo el rack** — charola colectora → manguera → coladera.",
        "**Banda gris oscura translúcida** — zona blackout N5 (cubierta opaca).",
        "**Bloque gris sobre la charola** — peso 2–4 kg sobre charola invertida.",
        "**Banda gris horizontal** — entrepaño MDF forrado (paso 43 cm, ≥ 30).",
    ])
    s.md_keys.extend(FLUJO_MD)
    s.bloques([
        ("Capacidad (geometría del entrepaño, no la cifra de la investigación)", [
            "Entrepaño 91.4 × 45.7 cm; charola 1020 = 25.4 × 50.8 cm.",
            "Caben 3 atravesadas por nivel (3 × 25.4 = 76.2 de 91.4 cm; vuelan 5.1 cm). El "
            "«8–10 por nivel» de research/estructura-invernadero §d NO cabe: pediría ~1.0 m² "
            "por nivel [POR VERIFICAR con el rack armado].",
            "En luz (N1–N4): 12 posiciones por rack. N5 oscuridad: 3 pilas × 2–3 = 6–9. "
            "Total 18–21 charolas en proceso por rack.",
            "3 racks (Fase 1) = 36 en luz; con ~7 días en luz por charola (día 3 → 10) el techo "
            "es ~36 por semana: la meta de 25–35 pide ≥ 70–85 % de ocupación. Husky de 122 cm: "
            "4 por nivel (16 en luz).",
        ]),
        ("Cargas", [
            "Charola doble con coco saturado 2.5–4 kg → nivel en luz 3 × 4 = 12 kg; N5 tapado "
            "3 × (2 × 4 + 4) = 36 kg. Total ≈ 84 kg + rack [POR VERIFICAR peso en caja].",
            "Repisa: 362.9 kg → margen > 10×; lo que manda es la rigidez y la humedad: forrar el "
            "MDF con plástico o charola de drenaje.",
        ]),
        ("Iluminación", [
            "2 × T8 LED 18 W 6500 K 1,400 lm por nivel N1–N4 = 8 tubos por rack ($121 c/u JWJ = "
            "$968); bom/fase1 cubre UN rack: 3 racks = 24 tubos.",
            "12–14 h/día por K5 (GAB-A): 8 × 18 W × 13 h ≈ 1.9 kWh/día por rack.",
            "Tubo a 3 cm bajo el entrepaño; luz → dosel 20–27 cm con paso de 43 cm. Meta "
            "100–200 µmol/m²s en la charola (app Photone); si falta, baja una posición el "
            "entrepaño de arriba [POR VERIFICAR con luxómetro].",
        ]),
        ("Riego", [
            "Nebulizadores N1–N4 (2 boquillas por nivel) desde P-1 12 V; N5 a mano.",
            "Tras el destape: riego SOLO por abajo (perforada dentro de lisa).",
            "MT-1…4 capacitivo en la charola testigo de cada nivel (rack 3 en Fase 1); SHT31 en "
            "el poste a 1.0 m; trampa amarilla 1 por rack.",
        ]),
    ])
    s.notas([
        "**N5 = oscuridad** (arriba, más cálido): cubierta opaca y pilas tapadas con peso. "
        "**N1–N4 en luz** (T8 + nebulizadores).",
        "**Verano (> 27 °C en N5): invierte** — tapadas en N1 (el más fresco) y cosecha en N2 "
        "(03 §0.2).",
        "El rack va sobre **piso nivelado** (nivel de burbuja, calzar patas) y sobre **bloques "
        "macizos de 15 cm**: son los que dan pendiente a la manguera de drenaje. Charola "
        "desnivelada = encharcamiento = moho.",
        "Fuentes: referencia/03-instalacion §0.1–0.3 · research/estructura-invernadero §d · "
        "research/clima-agronomia §8 · research/semillas-sustrato-charolas §c · "
        "diseno/hidraulico §1 · diseno/electrico §1 · bom/fase0-1.csv. Charola 1020 = 10×20 "
        "pulgadas. Escala 1:10 (1 cm = 4 px).",
    ], titulo="Cómo se opera el rack")
    return s


# ----------------------------------------------------------------------------- main
def validar(path: Path) -> tuple[bool, int]:
    from xml.dom import minidom
    try:
        minidom.parse(str(path))
        ok = True
    except Exception as e:  # noqa: BLE001
        print(f"  XML INVÁLIDO {path}: {e}")
        ok = False
    return ok, path.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None, help="carpeta de salida (default: docs/assets/diagramas/layout junto al repo)")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out = Path(args.out) if args.out else root / "docs" / "assets" / "diagramas" / "layout"
    jobs = {"patio-fase-0.svg": fase0, "patio-fase-1.svg": fase1, "patio-fase-2.svg": fase2,
            "patio-fase-3.svg": fase3, "rack-alzado.svg": rack_alzado}
    bad = 0
    for name, fn in jobs.items():
        path = out / name
        dib = fn()
        dib.save(path)
        # El texto largo del plano (leyenda, notas clave, tablas, notas) ya no cabe legible
        # dentro del SVG: se escribe al lado en Markdown y las paginas lo incrustan con
        # pymdownx.snippets, asi que se lee a 16 px, se busca y se copia.
        notas = out / f"{path.stem}.notas.md"
        notas.write_text(dib.markdown(), encoding="utf-8")
        ok, size = validar(path)
        flag = "ok" if ok and size > 4096 else "REVISAR"
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        print(f"{flag:8s} {rel}  {size / 1024:.1f} KB  +  {notas.name}  {notas.stat().st_size / 1024:.1f} KB")
        bad += 0 if ok and size > 4096 else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
