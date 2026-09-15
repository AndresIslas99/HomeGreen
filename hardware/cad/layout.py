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

Convencion de dibujo: cada plano lleva etiquetas cortas + NOTAS CLAVE numeradas (circulos)
explicadas en el panel derecho; los recorridos de agua (azul), electrico (ambar) y cultivo
(verde) se etiquetan con su longitud calculada sobre este supuesto.

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


class SVG:
    """Acumulador minimo de SVG con cabecera estandar de la wiki (titulo, version, linea)."""

    def __init__(self, w: int, h: int, title: str, subtitle: str = ""):
        self.w, self.h = w, h
        self.parts: list[str] = []
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
        if subtitle:
            self.text(24, 54, subtitle, size=12, fill=GRAY)
        self.text(w - 24, 34, VER, size=12, fill=GRAY, anchor="end")
        self.line(24, 64, w - 24, 64, sw=1)

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

    def text(self, x, y, s, size=12, fill=INK, anchor="start", weight="normal", rotate=None, italic=False):
        a = (f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
             f'text-anchor="{anchor}"')
        if weight != "normal":
            a += f' font-weight="{weight}"'
        if italic:
            a += ' font-style="italic"'
        if rotate is not None:
            a += f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"'
        self.add(a + f">{escape(s)}</text>")

    def lines(self, x, y, rows, size=11, fill=INK, lh=None, anchor="start", weight="normal"):
        """Varias lineas de texto apiladas; devuelve la y siguiente. Una fila que empieza con '#' va en negritas."""
        lh = lh or size + 3
        for i, r in enumerate(rows):
            w = weight
            if r.startswith("#"):
                r, w = r[1:], "bold"
            if r:
                self.text(x, y + i * lh, r, size=size, fill=fill, anchor=anchor, weight=w)
        return y + len(rows) * lh

    def save(self, path: Path) -> None:
        self.add("</svg>\n")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts), encoding="utf-8")


# ----------------------------------------------------------------------------- plantas
S = 100.0  # px por metro (1:50 con 1 m = 100 px)


class Plano(SVG):
    """Planta del patio en metros: x de oeste a este, y de norte a sur (norte arriba)."""

    W, H = 1600, 1210          # lienzo
    OX, OY = 110, 140          # origen del patio (esquina noroeste) en px
    PANEL_X = 1150             # panel derecho (leyenda + notas clave)

    def __init__(self, fase: int, subtitle: str):
        title = f"Planta · Fase {fase} · escala 1:50 · supuesto 10×8 m"
        super().__init__(self.W, self.H, title, subtitle)
        self.fase = fase
        self.keys: list[str] = []   # notas clave (texto), en orden de numero

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
        """Circulo numerado en (x, y) m; el texto va al panel derecho. Devuelve el numero."""
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

    def gabinete(self, x, y, w, h, tag, above=False):
        self.mrect(x, y, w, h, fill=AMBER_BG, stroke=AMBER, sw=2)
        self.mline(x + 0.03, y + 0.03, x + w - 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        self.mline(x + w - 0.03, y + 0.03, x + 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        self.mtext(x + w / 2, y - 0.07 if above else y + h + 0.13, tag, size=9, fill=AMBER, anchor="middle", weight="bold")

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

    def mesa(self, x, y, w, h, rows, color=INK):
        self.mrect(x, y, w, h, fill=WHITE, stroke=color, sw=1.5)
        self.mrect(x + 0.04, y + 0.04, w - 0.08, h - 0.08, fill="none", stroke=color, sw=0.7)
        self.mlines(x + w / 2, y + h / 2 + 0.04 - 0.055 * (len(rows) - 1), rows, size=9, fill=color, anchor="middle", lh=11)

    def tinaco(self, cx, cy, r, rows):
        bx, by, bw, bh = TINACO_BASE
        self.mrect(bx, by, bw, bh, fill="none", stroke=BLUE, sw=0.8, dash="3 2")
        self.mcircle(cx, cy, r, fill=BLUE_BG, stroke=BLUE, sw=2)
        self.mcircle(cx, cy, r * 0.72, fill="none", stroke=BLUE, sw=0.9)
        self.mlines(cx, cy + 0.02 - 0.06 * (len(rows) - 1), rows, size=9, fill=BLUE, anchor="middle", lh=11)

    def tambo(self, cx, cy, r, rows, color=BLUE):
        self.mcircle(cx, cy, r, fill=BLUE_BG if color == BLUE else GREEN_BG, stroke=color, sw=2)
        self.mcircle(cx, cy, r * 0.6, fill="none", stroke=color, sw=0.9, dash="3 2")
        if rows:
            self.mlines(cx, cy + r + 0.15, rows, size=9, fill=color, anchor="middle", lh=11)

    def cama(self, x, y, w, h, rows):
        self.mrect(x, y, w, h, fill="url(#hatchGreen)", stroke=GREEN, sw=2)
        self.mrect(x + 0.06, y + 0.06, w - 0.12, h - 0.12, fill="none", stroke=GREEN, sw=0.8)
        self.mlines(x + w / 2, y + h / 2 + 0.03 - 0.06 * (len(rows) - 1), rows, size=9, fill=GREEN, anchor="middle", lh=11)

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
        self.mtext(x + w / 2, y + h / 2 - 0.05, "cumbrera E–O · dos aguas ≥ 25 %", size=9, fill=GRAY, anchor="middle")
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
        self.mtext(x + 0.1, y - 0.28, f"TÚNEL {fmt(w)}×{fmt(h)} m = {fmt(w * h)} m² · PTR 1½\" cal. 14 · {porticos} pórticos · placa + 4 anclas 3/8\"×5\" por columna",
                   size=10.5, weight="bold")

    # -- panel derecho ------------------------------------------------------
    def leyenda(self, extra=()):
        x, y = self.PANEL_X, 88
        self.text(x, y, "LEYENDA", size=12, weight="bold")
        items = [
            ("line", BLUE, None, "agua a presión · red ½\" · llenado"),
            ("line", BLUE, DASH, "drenaje · rebosadero · purga → coladera"),
            ("line", BLUE, DASHDOT, "canalón / bajante pluvial (0.5–1 %)"),
            ("line", AMBER, None, "127 V CA (circuito GFCI del patio)"),
            ("line", AMBER, DASH, "12 V CC (fuente / bus de batería)"),
            ("line", AMBER, DOT, "señal de sensor · Wi-Fi"),
            ("fill", GREEN_BG, GREEN, "cultivo: rack · bancada NFT · cama"),
            ("fill", AMBER_BG, AMBER, "gabinete IP65 (GAB-x)"),
            ("fill", BLUE_BG, BLUE, "tinaco TK-1 · tambo TK-2"),
            ("fill", "url(#roof)", GRAY, "techo (túnel / cobertizo)"),
            ("line", GRAY, DASH, "reserva de una fase posterior"),
        ] + list(extra)
        yy = y + 17
        for kind, c1, c2, lab in items:
            if kind == "line":
                self.line(x, yy - 4, x + 30, yy - 4, stroke=c1, sw=2, dash=c2)
            else:
                self.rect(x, yy - 11, 30, 13, fill=c1, stroke=c2, sw=1.2)
            self.text(x + 38, yy, lab, size=10.5)
            yy += 16.5
        # simbolos en una fila
        sx = (x - self.OX) / S
        sy = (yy - self.OY) / S
        self.coladera(sx + 0.15, sy - 0.05, s=0.2); self.text(x + 38, yy, "coladera", size=10.5)
        self.toma(sx + 1.2, sy - 0.05); self.text(x + 135, yy, "toma de agua", size=10.5)
        self.contacto(sx + 2.4, sy - 0.05); self.text(x + 255, yy, "contacto GFCI in-use", size=10.5)
        yy += 17
        self.poste(sx + 0.15, (yy - self.OY) / S - 0.05); self.text(x + 38, yy, "columna PTR anclada", size=10.5)
        self.circle(x + 185, yy - 5, 8, fill=WHITE, stroke=INK, sw=1.2); self.text(x + 185, yy - 1.5, "n", size=9, anchor="middle", weight="bold")
        self.text(x + 200, yy, "nota clave (abajo)", size=10.5)
        return yy + 22

    def panel_keys(self, y, title="NOTAS CLAVE", size=10.5, lh=14.5):
        x = self.PANEL_X
        self.text(x, y, title, size=12, weight="bold")
        yy = y + 18
        for i, t in enumerate(self.keys, 1):
            rows = t.split("\n")
            self.circle(x + 8, yy - 4, 8, fill=WHITE, stroke=INK, sw=1.1)
            self.text(x + 8, yy - 0.5, str(i), size=9, anchor="middle", weight="bold")
            for j, r in enumerate(rows):
                self.text(x + 22, yy + j * (lh - 1.5), r, size=size)
            yy += lh * len(rows) + 2
        return yy

    def panel_text(self, y, rows, size=10.5, lh=14.5):
        return self.lines(self.PANEL_X, y, rows, size=size, lh=lh)

    def notas(self, rows, y=None, size=10.5, lh=14.5):
        y = y or self.Y(8.75) + 20
        self.text(self.OX - 20, y, "SUPUESTOS Y REGLAS", size=12, weight="bold")
        return self.lines(self.OX - 20, y + 18, rows, size=size, lh=lh)


# ----------------------------------------------------------------------------- GEOMETRIA (m)
# Cambia aqui si tu patio es distinto; todo lo demas (rutas, longitudes, cotas) se recalcula.
# x: oeste -> este (0..10). y: norte -> sur (0..8). Rectangulos: (x, y, ancho, alto). Circulos: (cx, cy, r).
ACCESO = (6.7, 7.7)               # zaguan de 1.0 m en la barda norte (supuesto)
PUERTA_CASA = (4.4, 5.3)          # puerta de la casa al patio (supuesto)
COLADERA = (9.6, 0.4)             # esquina noreste (supuesto de la wiki)
TOMA = (9.75, 7.92)               # llave existente en la pared de la casa
CONTACTO = (7.05, 7.97)           # contacto existente bajo el cobertizo -> WR GFCI in-use en F1
CONTACTO2 = (9.0, 7.97)           # 2.o contacto GFCI (refrigerador) en F2
CDC = (5.6, 8.08, 0.6, 0.3)       # centro de carga (interior de la casa)
CEREBRO = (1.4, 8.08, 2.3, 0.3)   # mini-PC HA + router + UPS (interior)
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
TLALOQUE = (7.75, 0.5, 0.3, 0.4)  # SP-1 + filtro de hojas, colgado del tramo 3" a 2 m
P1 = (7.55, 2.45, 0.4, 0.25)      # P-1 diafragma 12 V + F-1 (caja IP65)
F2BOX = (8.35, 2.45, 0.4, 0.25)   # F-2 duplex + SV-1 (llenado NFT) [+ SV-3 goteo en F3]
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
PUMPS_NFT = (5.15, 3.85, 0.4, 0.25)
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
    p.toma(*TOMA)
    x, y, w, h = COBERTIZO
    p.mrect(x, y, w, h, fill="url(#roof)", stroke="none")
    p.mrect(x, y, w, h, fill=WHITE, stroke="none", opacity=0.65)
    p.mrect(x, y, w, h, fill="none", stroke=GRAY, sw=1.5, dash=DASH)
    p.mtext(x + w - 0.05, y + 0.16, f"COBERTIZO existente (supuesto) {fmt(w)}×{fmt(h)} m", size=9.5, fill=GRAY, anchor="end")
    cx, cy, cw, ch = CDC
    p.mrect(cx, cy, cw, ch, fill=WHITE, stroke=AMBER, sw=1.5)
    p.mtext(cx + cw / 2, cy + 0.2, "centro de carga", size=9, fill=AMBER, anchor="middle")
    bx, by, bw, bh = CEREBRO
    p.mrect(bx, by, bw, bh, fill=WHITE, stroke=AMBER, sw=1.2, dash=DOT)
    p.mtext(bx + bw / 2, by + 0.2, "cerebro (interior): mini-PC HA + router + UPS", size=9.5, fill=AMBER, anchor="middle")


def seguridad_electrica(p: Plano):
    """QO120GFI, contacto WR in-use, varilla de tierra y GAB-A (desde Fase 1)."""
    cx, cy, cw, ch = CDC
    p.mtext(cx + cw / 2, cy - 0.06, "+ QO120GFI 20 A", size=9, fill=AMBER, anchor="middle", weight="bold")
    p.contacto(*CONTACTO)
    vx, vy = VARILLA
    p.mcircle(vx, vy, 0.07, fill=WHITE, stroke=AMBER, sw=1.5)
    for i, ww in enumerate((0.14, 0.09, 0.04)):
        p.mline(vx - ww / 2, vy + 0.1 + i * 0.045, vx + ww / 2, vy + 0.1 + i * 0.045, stroke=AMBER, sw=1.2)
    p.mline(vx, vy, cx + 0.05, cy, stroke=AMBER, sw=1, dash=DOT)
    p.gabinete(*GABA, "GAB-A (CA)", above=True)
    p.mline(CONTACTO[0], CONTACTO[1] - 0.1, GABA[0] + GABA[2], GABA[1] + 0.2, stroke=AMBER, sw=1.6)


def agua_base(p: Plano, tunel, R):
    """Tinaco, captacion, red, riego y drenaje (Fase 1 en adelante)."""
    tx, ty, tw, th = tunel
    p.mpoly(R["canal_n"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["canal_s"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["colector_se"], stroke=BLUE, sw=1.5, dash=DASHDOT, marker="arrBlue")
    p.mpoly(R["tramo_3"], stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mtext(tx + 0.1, ty - 0.14, f"canalón PVC · {fmt(tw)} m · pendiente 0.5–1 % → bajante NE", size=9, fill=BLUE)
    p.mtext(tx + 0.1, ty + th + 0.3, f"canalón sur · {fmt(tw)} m → bajante SE → colector 2\" por la cabecera este (2 m)", size=9, fill=BLUE)
    lx, ly, lw, lh = TLALOQUE
    p.mrect(lx, ly, lw, lh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(lx + lw / 2, ly + 0.15, ["SP-1", "tlaloque", "+ filtro"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.tinaco(*TINACO, ["TK-1 tinaco", "750 L · opaco", "base firme", "LT-1 · TT-1", "en la tapa"])
    p.mpoly(R["rebosadero"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mpoly(R["red"], stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(9.98, 4.6, f"red ½\" ≈ {fmt(dist(R['red']))} m → FV-1 flotador (solo rellena, tandeo)", size=9, fill=BLUE, anchor="middle", rotate=-90)
    # salida inferior -> V-1/F-1 -> tee -> P-1 (riego) | F-2 (F2)
    p.mline(TINACO[0], TINACO[1] + TINACO[2], TINACO[0], P1[1] + 0.06, stroke=BLUE, sw=2)
    p.mline(P1[0] + P1[2], P1[1] + 0.06, F2BOX[0], F2BOX[1] + 0.06, stroke=BLUE, sw=2)
    p.mtext(TINACO[0] + 0.07, P1[1] - 0.02, "V-1 + F-1", size=8.5, fill=BLUE)
    px, py, pw, ph = P1
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(px + pw / 2, py + 0.11, ["P-1 diafragma 12 V", "+ presostato (IP65)"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mpoly(R["riego"], stroke=BLUE, sw=2, marker="arrBlue")
    for rx in RACK_XS:
        p.mline(rx + 0.457, ty + 0.22, rx + 0.457, RACK_Y + 0.3, stroke=BLUE, sw=1.2, marker="arrBlue")
    p.mpoly(R["dren"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(6.75, 3.27, f"drenaje 2\" a piso ≈ {fmt(dist(R['dren']))} m → coladera (pendiente ≥ 1 %)", size=8.5, fill=BLUE)


def racks_tunel(p: Plano, rack4=False):
    for i, rx in enumerate(RACK_XS, 1):
        p.rack(rx, RACK_Y, label=f"rack {i}" + (" (testigo MT-1…4)" if i == 3 else ""))
    p.dim_h(RACK_XS[0] + 0.914, RACK_XS[1], RACK_Y + 0.23, "0.34", size=8.5)
    x, y, w, h = MESA_SIEMBRA
    if rack4:
        p.rack(x + 0.1, RACK_Y, label="rack 4 (opc.)", dashed=True)
    else:
        p.mesa(x, y, w, h, ["mesa de siembra 1.2×0.6", "+ tapete térmico dic–feb"])


def electrico_tunel(p: Plano, tunel, R):
    """Troncal aerea, GAB-1, T8/extractor, 12 V a P-1, sensores."""
    tx, ty, tw, th = tunel
    p.mpoly(R["troncal"], stroke=AMBER, sw=2.4, marker="arrAmber")
    p.poste(*MASTIL, size=0.1)
    p.gabinete(*GAB1, "GAB-1 (CC)")
    p.mpoly(R["t8"], stroke=AMBER, sw=1.6, marker="arrAmber")
    for rx in RACK_XS:
        p.mline(rx + 0.2, ty + 0.13, rx + 0.2, RACK_Y - 0.02, stroke=AMBER, sw=1.1, marker="arrAmber")
    ex, ey = EXT_X, ty + th / 2
    p.mcircle(ex, ey, 0.14, fill=WHITE, stroke=AMBER, sw=1.5)
    for a in (0, 120, 240):
        p.add(f'<path d="M{fmt(p.X(ex))},{fmt(p.Y(ey))} l{fmt(0.11 * S)},0 a{fmt(0.05 * S)},{fmt(0.05 * S)} 0 0 1 '
              f'-{fmt(0.055 * S)},{fmt(0.09 * S)} z" fill="{AMBER}" fill-opacity="0.5" stroke="none" '
              f'transform="rotate({a} {fmt(p.X(ex))} {fmt(p.Y(ey))})"/>')
    p.mtext(ex + 0.2, ey + 0.05, "extractor", size=9, fill=AMBER)
    p.mpoly(R["dc_p1"], stroke=AMBER, sw=1.5, dash=DASH, marker="arrAmber")
    sx_, sy_ = (3.05, 3.97) if th > 4 else (tx + tw / 2, ty + th / 2 + 0.35)
    p.mcircle(sx_, sy_, 0.05, fill=AMBER, stroke=AMBER)
    p.mtext(sx_ + 0.1, sy_ + 0.04, "SHT31 T/HR a 1.5 m", size=9, fill=AMBER)
    p.mline(TINACO[0] - 0.3, TINACO[1] - 0.2, GAB1[0] + 0.28, GAB1[1] + 0.2, stroke=AMBER, sw=1, dash=DOT)


def zona_cosecha(p: Plano, refri=False, gabdc=False):
    x, y, w, h = MESA_COSECHA
    p.mesa(x, y, w, h, ["mesa cosecha/empaque", "inox o polietileno"])
    if refri:
        rx, ry, rw, rh = REFRI
        p.mrect(rx, ry, rw, rh, fill=WHITE, stroke=INK, sw=1.5)
        p.mline(rx, ry + 0.2, rx + rw, ry + 0.2, sw=0.8)
        p.mlines(rx + rw / 2, ry + 0.38, ["refri", "4–5 °C"], size=8.5, anchor="middle", lh=10)
        p.contacto(*CONTACTO2)
    tx_, ty_, tr = TINA
    p.mcircle(tx_, ty_, tr, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mline(TOMA[0], TOMA[1] - 0.09, tx_, ty_ + tr, stroke=BLUE, sw=1.2)
    p.mtext(tx_ - 0.3, ty_ + 0.04, "tina + lavamanos", size=8.5, fill=BLUE, anchor="end")
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
    p.mesa(*MESA_F0, ["mesa de siembra 1.2×0.6", "báscula · atomizador · H2O2"])
    tx_, ty_, tr = TINA
    p.mcircle(tx_, ty_, tr, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mline(TOMA[0], TOMA[1] - 0.09, tx_, ty_ + tr, stroke=BLUE, sw=1.2)
    p.mtext(9.95, 6.7, "tina + cubeta de remojo", size=8.5, fill=BLUE, anchor="end")
    p.mcircle(0.5, 7.5, 0.2, fill=WHITE, stroke=INK, sw=1.2)
    p.mtext(0.5, 7.2, "cubeta sustrato usado", size=8.5, anchor="middle")
    p.dim_v(6.55, 7.5, 7.1, "≥ 0.9 pasillo", size=9)
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
    p.key(MESA_F0[0] + 0.6, MESA_F0[1] + 0.3, "Mesa de siembra junto a la toma (< 10 m): remojo, pesado y\nsanitización de semilla (H2O2 3 %). 20 charolas 10×20.", INK, dx=-0.2, dy=-0.5)
    p.key(CONTACTO[0], CONTACTO[1], "Contacto existente (sin GFCI aún). T8 opcionales con timer;\nen Fase 1 se vuelve contacto GFCI in-use + tierra.", AMBER, dx=-0.6, dy=-0.35)
    p.key(tx + tw / 2, ty + 0.3, "Reserva del túnel: medir aquí 3 días T mín/máx (ideal 16–24 °C)\ny luz con Photone (100–200 µmol/m²s); diagonales iguales ± 1 cm;\nlosa sana ≥ 10 cm; bordes a ≥ 15 cm de cualquier ancla.", GRAY)
    p.key(COLADERA[0] - 0.5, COLADERA[1] + 0.35, "Coladera existente: probarla (10 L de golpe deben irse); nada\nla tapará: ni placas, ni tinaco, ni composta.", BLUE)
    p.key(ACCESO[0] + 0.6, 0.45, "Zaguán de 1.0 m: ¿pasa el tinaco de 750 L (Ø ≈ 1.1 m)? Si no,\nentra por la casa o se compra el de 450 L [POR VERIFICAR Ø].", INK)
    p.key(0.5, 6.9, "Sustrato usado: cubeta con tapa lejos del rack (fungus gnats);\nen Fase 1 se vuelve tambo de composta.", INK, dx=0.5, dy=-0.25)
    yy = p.leyenda()
    yy = p.panel_keys(yy + 6)
    p.panel_text(yy + 10, [
        "#QUÉ HAY EN FASE 0 (y nada más)",
        "1 rack Husky ($2,019) · 20 charolas · semilla · coco ·",
        "báscula · atomizador · H2O2. Sin túnel, sin bomba, sin",
        "relés: la Fase 0 valida que los chefs PAGAN.",
        "",
        "#ANTES DE FASE 1 (checklist de replanteo)",
        "· ¿Condominio? Art. 21/23 antes de perforar (07 §9).",
        "· Consumo base CFE 7 días (medidor de enchufe) y tarifa.",
        "· EC/pH de la llave 3 días distintos (02 §agua).",
        "· Foto de losa, coladera, toma, contacto y bardas.",
    ])
    p.notas([
        NOTA_SUPUESTO,
        "Reglas: rack bajo techo con toma a < 10 m y contacto cerca · pasillo ≥ 0.9 m frente al rack · la reserva del túnel queda a ≥ 0.6 m de bardas y ≥ 0.8 m de la barda norte (canaleta + paso) · nada tapa la coladera.",
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
    p.dim_h(tx + tw, TINACO_BASE[0], 1.3, "0.90 paso", size=8.5)
    p.dim_v(COLADERA[1] + 0.15, TINACO_BASE[1], 9.4, "0.40", size=8.5)
    p.mtext(tx + tw + 0.12, DOOR[0] - 0.06, "puerta 0.9", size=8.5, fill=GRAY)
    # notas clave
    p.key(tx + 1.6, ty + th - 0.35, "Túnel 18 m²: 3 pórticos (6 columnas a 3 m) con placa + 4 anclas de\ncuña 3/8\"×5\"; puerta al este, de frente al zaguán y al tinaco.", INK)
    p.key(RACK_XS[1] + 0.457, RACK_Y + 0.23, "3 racks Husky en fila contra la pared norte, separados 0.34 m\n(los T8 de 1.2 m vuelan 14 cm por lado). Rack 3 = testigo con MT-1…4.", GREEN, dx=0.35, dy=0.55)
    p.key(TINACO[0], TINACO[1] + 0.35, "TK-1 750 L sobre base firme 1.3×1.3 (lleno ≈ 750 kg), opaco, a 0.4 m\nde la coladera (rebosadero) y a 0.9 m del túnel (paso libre).", BLUE, dx=-0.9, dy=0.25)
    p.key(TLALOQUE[0] + 0.15, TLALOQUE[1] - 0.2, "Canalones N y S → bajante NE → tramo 3\" a 2 m sobre el paso →\nSP-1 tlaloque (purga 20–40 L) + filtro de hojas → tapa del tinaco.", BLUE, dx=-0.7, dy=0)
    p.key(P1[0] + 0.2, P1[1] + 0.12, "P-1 diafragma 12 V + F-1 sedimentos junto a la salida del tinaco;\nriego ½\" aéreo (2 m) por la cabecera este y el larguero norte → riser\npor rack → nebulizadores N1–N4 (2 boquillas/nivel).", BLUE, dx=1.55, dy=0)
    p.key(GAB1[0] + 0.14, GAB1[1] - 0.25, "GAB-1 (CC, IP65) en la columna NE a 2.0 m: ESP32 nodo-riego-v1 +\nrelé 4 ch + buck. A ≤ 3 m del rack testigo y ≤ 2 m del tinaco (LT-1);\nWi-Fi desde el cerebro ≈ 7 m con una pared.", AMBER, dx=-0.55, dy=0)
    p.key(GABA[0] + 0.2, GABA[1] - 0.3, "GAB-A (CA, IP65) en la pared bajo el cobertizo: fuente 12 V 5 A +\ncontactor K5 de T8/extractor. Cordón uso rudo 1 m al contacto WR.", AMBER, dx=-0.6, dy=0)
    p.key(MASTIL[0], MASTIL[1] - 0.5, f"Troncal aérea a 2.2 m (mensajero de acero): 127 V a T8/extractor +\n12 V a GAB-1 + señal K5. GAB-A → GAB-1 ≈ {fmt(dist(R['troncal']))} m (12 V 5 A: 10–12 AWG).", AMBER, dx=0.55, dy=0)
    p.key(CDC[0] + 0.3, CDC[1] - 0.3, "Centro de carga: breaker QO120GFI 20 A para TODO el circuito del patio;\nconduit 12 AWG al contacto WR in-use; varilla copperweld 5/8\"×3 m ≤ 25 Ω.", AMBER, dx=-0.9, dy=-0.5)
    p.key(9.85, 2.0, f"Drenaje de charolas colectoras (racks sobre bloques de 15 cm) por la\npared norte, cabecera este y barda este → coladera ≈ {fmt(dist(R['dren']))} m, ≥ 1 %.", BLUE, dx=-0.5, dy=0.4)
    p.key(MESA_COSECHA[0] + 0.6, MESA_COSECHA[1] - 0.3, "Cobertizo = cuarto de cosecha (NOM-251): mesa inox, tina de lavado +\nlavamanos en la toma, hielera; cortina plástica lo separa del cultivo.", INK, dx=-0.5, dy=-0.55)
    p.key(COMPOSTA[0] + 0.3, COMPOSTA[1] - 0.45, "Tambo de composta (sustrato usado 100–150 kg/mes) en la esquina\nopuesta al cultivo y a la cosecha; charola con fusarium va a la basura.", GREEN, dx=0.4, dy=0)
    p.key(EXT_X, ty + th / 2, "Extractor en la cabecera oeste (HR > 70 %); entra aire por la puerta y los\nfaldones enrollables con malla antiáfidos (laterales N y S).", AMBER, dx=0.4, dy=0.4)
    p.key(MESA_SIEMBRA[0] + 0.6, MESA_SIEMBRA[1] + 0.9, "Mesa de siembra dentro del túnel (tapete térmico dic–feb por K4).\nEn Fase 2 su lugar lo puede tomar el rack 4.", INK, dx=0, dy=0)
    yy = p.leyenda()
    yy = p.panel_keys(yy + 6)
    p.panel_text(yy + 8, [
        "#RECORRIDOS (m, sobre este supuesto)",
        f"127 V troncal GAB-A→columna SE→GAB-1 ≈ {fmt(dist(R['troncal']))} · T8 larguero ≈ {fmt(dist(R['t8']))}",
        f"12 V GAB-1→P-1 ≈ {fmt(dist(R['dc_p1']))} · riego P-1→rack 1 ≈ {fmt(dist(R['riego']))} (+ 3 risers)",
        f"red→FV-1 ≈ {fmt(dist(R['red']))} · drenaje→coladera ≈ {fmt(dist(R['dren']))} · canalón 6 + 6 + colector 3",
    ], size=10, lh=14)
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
    p.mtext(rx - 0.06, 3.0, "retorno 2\"", size=8.5, fill=BLUE, anchor="middle", rotate=-90)
    p.mcircle(rx, 3.62, 0.045, fill=AMBER, stroke=AMBER)
    p.tambo(tcx, tcy, tr, None)
    p.mtext(tcx, tcy + 0.03, "TK-2", size=9, fill=BLUE, anchor="middle", weight="bold")
    px, py, pw, ph = PUMPS_NFT
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(px + pw / 2, py + 0.11, ["P-1/P-2 12 V", "F-1 malla · FT-1"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mline(tcx + tr, tcy, px, tcy, stroke=BLUE, sw=2, marker="arrBlue")
    p.mpoly(R["subida"], stroke=BLUE, sw=2, marker="arrBlue")
    fx, fy, fw, fh = F2BOX
    p.mrect(fx, fy, fw, fh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(fx + fw / 2, fy + 0.11, ["F-2 dúplex", "+ SV-1 NC"], size=8, fill=BLUE, anchor="middle", lh=9.5)
    p.mpoly(R["llenado"], stroke=BLUE, sw=2, marker="arrBlue")
    p.mpoly(R["purga"], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mesa(*MESA_GERM, ["mesa", "germinación", "(foami) y", "trasplante"])
    p.dim_v(BANCADA_A_Y + 4 * PITCH, BANCADA_B_Y, 2.4, "0.90 pasillo", size=9)
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
    p.mrect(7.3, 8.08, 0.5, 0.28, fill=WHITE, stroke=AMBER, sw=1.2, dash=DASH)
    p.mtext(7.55, 8.27, "PV 100 W opc.", size=8.5, fill=AMBER, anchor="middle")
    p.mtext(7.9, 8.27, "en la azotea, nunca sobre el plástico", size=8.5, fill=AMBER)
    p.mline(7.3, 8.2, GABDC[0] + GABDC[2], GABDC[1] + 0.3, stroke=AMBER, sw=1.2, dash=DASH)
    cx, cy = TUNEL_F2[0] + TUNEL_F2[2], TUNEL_F2[1]
    p.mpoly([(cx, cy), (cx + 0.7, cy + 0.9), (cx + 1.1, cy + 0.15)], stroke=AMBER, sw=0.8, dash=DOT, fill=AMBER_BG, close=True)
    p.mcircle(cx, cy, 0.07, fill=AMBER, stroke=AMBER)
    p.mtext(cx + 0.55, cy + 0.2, "ESP32-CAM", size=8.5, fill=AMBER)


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
    p.dim_h(tx + tw, TINACO_BASE[0], 1.3, "0.90 paso", size=8.5)
    p.mtext(tx + tw + 0.12, DOOR[0] - 0.06, "puerta 0.9", size=8.5, fill=GRAY)
    # notas clave
    p.key(3.0, ty + th - 0.12, "Fachada sur del túnel se mueve 2 m: 5×6 = 30 m², 4 pórticos (8 columnas\na 2 m). Las 6 bases del este/oeste se reutilizan; el canalón sur se cuelga\nen el alero nuevo; la bajante NE y el tinaco no se mueven.", INK)
    p.key(BANCADA_X + 1.5, BANCADA_B_Y - 0.4, "2 bancadas E–O de 4 líneas PVC sanitario 4\" × 3 m (10 canastillas a\n20 cm), alto al OESTE (manifold) y bajo al ESTE (retornos), 2–3 %;\npasillo de 0.9 m entre bancadas; la A se atiende por 2 lados, la B por 1.", GREEN)
    p.key(TAMBO[0], TAMBO[1] + 0.5, "TK-2 tambo 200 L tapado, entre los retornos; P-1/P-2 diafragma 12 V\n+ F-1 malla 120 + FT-1 al lado; subida ¾\" al pie de la bancada A hasta\nel manifold. Sondas pH/EC/T en el RETORNO; peristálticas al tambo.", BLUE, dx=0.45, dy=0.25)
    p.key(F2BOX[0] + 0.2, F2BOX[1] + 0.12, f"Llenado: tinaco → F-2 dúplex (sin cloro) → SV-1 NC → tambo ≈ {fmt(dist(R['llenado']))} m.\nPurga SV-2 (cambio cada 2–3 sem) se une al drenaje ≈ {fmt(dist(R['purga']) + 6.0)} m a la coladera.", BLUE, dx=0.75, dy=0.4)
    p.key(GABDC[0] + 0.2, GABDC[1] - 0.25, "GAB-DC (CC): LiFePO4 100 Ah a 30 cm del piso + EPEVER LS2024B +\nfusiblera 6 vías, separado de GAB-A (CA: cargador). Panel 100 W opc.\nen la azotea. Bus 12 V por la troncal aérea a bombas y GAB-2.", AMBER, dx=-0.6, dy=0)
    p.key(GAB2[0] + 0.14, GAB2[1] + 0.5, f"GAB-2 (CC) en la columna sur x = 4.6: ESP32 nodo-nft-v2 (pH/EC, MOSFET\nperistálticas, solenoides, detector CFE). Bus GAB-DC→bombas ≈ {fmt(dist(R['bus12']))} m.", AMBER, dx=0, dy=0)
    p.key(REFRI[0] + 0.3, REFRI[1] - 0.25, "Cuarto de cosecha completo: refri usado 9–11 ft³ a 4–5 °C en su\npropio contacto GFCI, mesa inox, tina/lavamanos, hielera de reparto.", INK, dx=-0.9, dy=-0.4)
    p.key(tx + tw + 0.5, ty + 0.6, "ESP32-CAM en la columna NE: puerta, zaguán y tinaco (detección\nnocturna). Nada de valor visible desde la calle; candado en el túnel.", AMBER, dx=0.3, dy=0.4)
    p.key(MESA_GERM[0] + 0.85, MESA_GERM[1] + 0.4, "Mesa de germinación (foami agrícola) y trasplante a canastilla,\njunto a la puerta y al tambo. Rack 4 opcional donde iba la mesa de siembra.", INK, dx=0, dy=0)
    p.key(9.85, 2.0, "Mismo drenaje de Fase 1: recibe además la purga del tambo (200 L\ncada 2–3 sem) y el rebosadero. Sigue sin cruzar el paso al túnel.", BLUE, dx=-0.5, dy=0.4)
    yy = p.leyenda()
    yy = p.panel_keys(yy + 6)
    p.panel_text(yy + 8, [
        "#RECORRIDOS NUEVOS (m)",
        f"bus 12 V GAB-DC→bombas ≈ {fmt(dist(R['bus12']))} · →GAB-2 ≈ {fmt(dist(R['bus12'][:-1]) + dist(R['bus_gab2']))}",
        f"llenado ≈ {fmt(dist(R['llenado']))} · subida ¾\" ≈ {fmt(dist(R['subida']))} · manifold 3.2 · retornos 2 × 1.6",
        f"purga→coladera ≈ {fmt(dist(R['purga']) + 6.0)} · troncal 127 V ≈ {fmt(dist(R['troncal']))} (igual que F1)",
    ], size=10, lh=14)
    p.notas([
        NOTA_SUPUESTO,
        "Separación entre líneas NFT 28 cm eje a eje (bancada 1.12 m) [POR VERIFICAR con el porte de la albahaca a 20 cm entre canastillas; con 30–35 cm la bancada sube a 1.2–1.4 m y el pasillo baja a 0.7 m].",
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
        p.cama(x, y, w, h, [f"cama {i}", f"{fmt(w)}×{fmt(h)} = {fmt(w * h)} m²"])
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
    p.mtext(x + w / 2, y - 0.26, "gantry XY: rieles V-slot en los bordes largos · puente Y · NEMA17 · GRBL/Klipper", size=9, anchor="middle")
    p.gabinete(*GAB3, "GAB-3")
    p.mpoly(R["gantry_12v"], stroke=AMBER, sw=1.4, dash=DASH, marker="arrAmber")
    p.mcircle(*CAM_POSTE, 0.07, fill=AMBER, stroke=AMBER)
    p.mpoly([CAM_POSTE, (CAM_POSTE[0] - 0.9, CAM_POSTE[1] + 0.6), (CAM_POSTE[0] - 0.6, CAM_POSTE[1] + 1.3)], stroke=AMBER, sw=0.8, dash=DOT, fill=AMBER_BG, close=True)
    p.mtext(CAM_POSTE[0] + 0.1, CAM_POSTE[1] - 0.06, "cámara fija (poste 2 m)", size=8.5, fill=AMBER)
    p.mline(COMPOSTA[0] + 0.3, COMPOSTA[1] - 0.15, CAMA3[0], CAMA3[1] + 0.8, stroke=GREEN, sw=1.2, dash=DOT, marker="arrGreen")
    p.dim_h(tx + tw, CAMA1[0], 6.27, "0.30", size=8)
    p.dim_h(CAMA1[0] + CAMA1[2], CAMA2[0], 6.27, "0.95 pasillo", size=8.5)
    p.dim_v(ty + th, CAMA3[1], 0.8, "0.70", size=8.5)
    p.dim_h(tx, tx + tw, 0.4, "6.00", size=9)
    p.dim_v(ty, ty + th, 0.3, "5.00", size=9)
    # notas clave
    p.key(CAMA1[0] + 0.5, CAMA1[1] + 0.5, f"Camas 1–2 (1.0 m: se atienden por un lado) al este, sobre la línea de\ndrenaje; cama 3 (gantry) al sur. Total {fmt(total)} m² de {fmt(total)}: es lo que cabe con\npasillos ≥ 0.7 m. Meta 15–20 m²: ver layout-patio.md §5.", GREEN, dx=0, dy=0)
    p.key(F2BOX[0] + 0.2, F2BOX[1] + 0.12, f"Goteo colgado de HA: SV-3 (12 V NC) en la caja F-2 desde el tinaco;\nramal este ≈ {fmt(dist(R['goteo_e']) + dist(R['goteo_e2']))} m y ramal sur por la troncal y el alero sur ≈ {fmt(dist(R['goteo_s']))} m.", BLUE, dx=0.75, dy=0.4)
    p.key(CAMA3[0] + 1.9, CAMA3[1] + 0.5, "Gantry XY tipo FarmBot sobre la cama 3 (la más larga): carrera ≈ 3.0 × 0.9 m,\nGAB-3 con driver + cámara en la pared de la casa, 12 V desde GAB-DC.", INK, dx=0.7, dy=0)
    p.key(CAM_POSTE[0], CAM_POSTE[1], "Cámara fija en poste de 2 m: cobertura foliar, plagas y timelapse\nde la cama 3 (visión = juguete de F3, no el negocio).", AMBER, dx=0.45, dy=0.4)
    p.key(COMPOSTA[0] + 0.35, COMPOSTA[1] - 0.4, "La composta del tambo alimenta las camas (07 §12); nunca charola con\nfusarium. Ruta corta, sin cruzar el cuarto de cosecha.", GREEN, dx=0.4, dy=0)
    p.key(GAB3[0] + 0.14, GAB3[1] - 0.25, "Regla de oro F3: ningún cable ni manguera nueva cruza pasillos a nivel\nde piso; todo aéreo (2 m) o pegado a barda/cama.", AMBER, dx=0.5, dy=0)
    yy = p.leyenda()
    yy = p.panel_keys(yy + 6)
    p.panel_text(yy + 8, [
        "#QUÉ CAMBIA VS. FASE 2",
        f"· 3 camas elevadas = {fmt(total)} m² (alt. 0.7–0.9 m [POR VERIFICAR]).",
        "· SV-3 + goteo por cama (timer + humedad en HA).",
        "· Gantry sobre la cama 3; GAB-3 driver; cámara fija.",
        "· Nada de esto es el negocio: sólo si F1–F2 se pagan.",
    ], size=10, lh=14)
    p.notas([
        NOTA_SUPUESTO,
        "Las camas van pegadas a la barda este y a la casa y se atienden por un solo lado: por eso miden ≤ 1.0 m de ancho. Cama 3 deja libre la puerta casa→patio y 0.7 m de paso frente al túnel.",
        "[POR VERIFICAR] altura y material de cama (0.7–0.9 m: madera tratada/PTR + geomembrana), perfil V-slot y carrera del gantry, caudal de goteo por cama: no están en la fuente de verdad; el plan maestro sólo fija 'camas elevadas con goteo colgado de HA' y 'gantry XY V-slot + NEMA17 + GRBL/Klipper'.",
        "Fuentes: referencia/00-plan-maestro §Fase 3 · referencia/07 §12 y §14 · research/hidroponia-nft (periférica sólo para riego presurizado de camas) · plantas de Fases 1–2.",
    ])
    return p


# ----------------------------------------------------------------------------- alzado del rack
K = 4.0  # px por cm (1:10)

RACK_H, RACK_W, RACK_D = 183.0, 91.4, 45.7   # cm (Husky 5 niveles, Home Depot $2,019)
SHELF_T = 2.5                                # espesor del entrepano MDF + forro [POR VERIFICAR en caja]
SHELF_TOPS = (10.0, 53.0, 96.0, 139.0, 182.0)  # cara superior de N1..N5 desde el piso (ajustables)
TRAY_W, TRAY_L, TRAY_H = 25.4, 50.8, 6.0     # charola 1020 (doble: perforada dentro de lisa)
TUBE_L, TUBE_D = 120.0, 2.6                  # T8 LED 18 W 120 cm
CANOPY = {2: 8.0, 3: 5.0, 4: 2.0}            # altura del dosel dibujada por nivel en luz (cm); N1 y N5 van tapados


def rack_alzado():
    W, H = 1600, 1040
    s = SVG(W, H, "Alzado · Rack Husky 183×91×46 cm · 5 niveles · escala 1:10",
            "charolas 10×20 (25.4×50.8 cm) · 3 por nivel · T8 18 W ×2 por nivel N1–N4 · nebulizadores N1–N4 · oscuridad arriba (N5) · recién sembradas abajo (N1) · cotas en cm")
    floor = 930.0

    def yc(cm):
        return floor - cm * K

    # ---------------- vista frontal
    x0 = 130.0
    wpx = RACK_W * K
    s.text(x0, 86, "VISTA FRONTAL (desde el pasillo)", size=12, weight="bold")
    s.line(x0 - 80, floor, x0 + wpx + 120, floor, sw=2)
    s.text(x0 - 80, floor + 16, "piso nivelado + bloques de 15 cm bajo las patas (charola desnivelada = encharcamiento = moho; los bloques dan pendiente al drenaje)", size=9.5, fill=GRAY)
    s.rect(x0 - 6, floor - 4 * K, wpx + 12, 4 * K, fill=BLUE_BG, stroke=BLUE, sw=1.2)
    s.text(x0 + wpx + 16, floor - 4, "charola colectora → manguera → coladera", size=10, fill=BLUE)
    for px in (x0, x0 + wpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    gap = (RACK_W - 3 * TRAY_W) / 4
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x0, yc(top), wpx, SHELF_T * K, fill="#d1d5db", stroke=INK, sw=1.5)
        s.text(x0 - 12, yc(top) + 4, f"N{i}", size=12, weight="bold", anchor="end")
        if 2 <= i <= 4:
            for k in range(3):
                tx = x0 + (gap + k * (TRAY_W + gap)) * K
                s.rect(tx, yc(top + TRAY_H), TRAY_W * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.4)
                s.rect(tx + 1.0 * K, yc(top + TRAY_H - 0.6), (TRAY_W - 2.0) * K, (TRAY_H - 1.6) * K, fill="#f1f8e9", stroke=GREEN, sw=0.8)
                c = CANOPY[i]
                s.rect(tx + 0.8 * K, yc(top + TRAY_H + c), (TRAY_W - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
        else:
            for k in range(3):
                tx = x0 + (gap + k * (TRAY_W + gap)) * K
                for st in range(2):
                    s.rect(tx, yc(top + TRAY_H * (st + 1)), TRAY_W * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
                s.rect(tx + 6 * K, yc(top + 2 * TRAY_H + 5), 13 * K, 5 * K, fill="#9ca3af", stroke=INK, sw=1)
                s.text(tx + 12.5 * K, yc(top + 2 * TRAY_H + 1.5), "peso 2–4 kg", size=8, anchor="middle", fill=WHITE)
        if i <= 4:
            tx = x0 + gap * K
            s.line(tx + 4 * K, yc(top + TRAY_H + 6), tx + 4 * K, yc(top + 1), stroke=AMBER, sw=2.5)
            s.text(tx + 5 * K, yc(top + TRAY_H + 5), f"MT-{i}", size=8.5, fill=AMBER)
            nxt = SHELF_TOPS[i] - SHELF_T
            ty = yc(nxt - 3.0)
            tl = x0 + wpx / 2 - TUBE_L * K / 2
            s.rect(tl, ty, TUBE_L * K, TUBE_D * K, fill="#fef3c7", stroke=AMBER, sw=1.4, rx=5)
            ny = ty + TUBE_D * K + 2.0 * K
            s.line(x0, ny, x0 + wpx, ny, stroke=BLUE, sw=1.6)
            for q in (0.25, 0.75):
                bx = x0 + wpx * q
                s.polyline([(bx - 4, ny), (bx + 4, ny), (bx, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
                for dx in (-10, 0, 10):
                    s.line(bx, ny + 10, bx + dx, ny + 22, stroke=BLUE, sw=0.7, dash="2 2")
            if i == 1:
                s.text(tl + TUBE_L * K + 6, ty + 9, "T8 de N1 apagados mientras haya charolas tapadas", size=8.5, fill=AMBER)
    s.rect(x0 - 6, yc(SHELF_TOPS[4] + 22), wpx + 12, 22 * K, fill="#374151", stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    s.text(x0 - 80, yc(SHELF_TOPS[4] + 25), "N5 = OSCURIDAD (arriba = más cálido): cubierta opaca, charolas apiladas con peso 2–4 kg, 2–4 días, atomizar a mano 1–2×/día · N1 = recién sembradas (abajo = más fresco)", size=10, weight="bold")
    s.circle(x0 + wpx + 6, yc(95), 5, fill=AMBER, stroke=AMBER)
    s.text(x0 + wpx + 14, yc(95) + 4, "SHT31 T/HR (poste, 1.0 m)", size=9, fill=AMBER)
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
    by = floor + 34
    s.line(x0, by, x0 + wpx, by, sw=1)
    s.line(x0, by - 5, x0, by + 5, sw=1); s.line(x0 + wpx, by - 5, x0 + wpx, by + 5, sw=1)
    s.text(x0 + wpx / 2, by - 4, "91.4", size=11, anchor="middle")
    tl = x0 + wpx / 2 - TUBE_L * K / 2
    by2 = floor + 56
    s.line(tl, by2, tl + TUBE_L * K, by2, stroke=AMBER, sw=1)
    s.line(tl, by2 - 5, tl, by2 + 5, stroke=AMBER, sw=1); s.line(tl + TUBE_L * K, by2 - 5, tl + TUBE_L * K, by2 + 5, stroke=AMBER, sw=1)
    s.text(x0 + wpx / 2, by2 - 4, "T8 120 (vuela 14.3 por lado → racks separados ≥ 30 cm)", size=10, fill=AMBER, anchor="middle")
    top3 = SHELF_TOPS[2]
    tube_bottom = SHELF_TOPS[3] - SHELF_T - 3.0 - TUBE_D
    canopy_top = top3 + TRAY_H + CANOPY[3]
    xr = x0 - 36
    s.line(xr, yc(tube_bottom), xr, yc(canopy_top), stroke=AMBER, sw=1)
    for cm in (tube_bottom, canopy_top):
        s.line(xr - 5, yc(cm), xr + 5, yc(cm), stroke=AMBER, sw=1)
    s.text(xr - 6, yc((tube_bottom + canopy_top) / 2), f"luz→dosel {fmt(tube_bottom - canopy_top)}", size=9, fill=AMBER, anchor="middle", rotate=-90)
    # flujo de charolas
    fx = x0 + wpx + 70
    flow = {5: ["② OSCURIDAD día 1–4 → N5 (arriba, más cálido):", "apiladas con peso 2–4 kg; atomizar 1–2×/día"],
            4: ["③ DESTAPE día 3–5 → N4: luz indirecta +", "T8 12–14 h; riego SOLO por abajo"],
            3: ["④ N3 desarrollo (día 5–8)"],
            2: ["⑤ N2 acabado → COSECHA día 8–12", "(tijera sobre el sustrato, la mañana de entrega)"],
            1: ["① SIEMBRA día 0 → N1 (abajo, más fresco):", "tapada con peso; sube a N5 al día siguiente"]}
    for i, top in enumerate(SHELF_TOPS, 1):
        s.lines(fx, yc(top + 20), flow[i], size=9.5, fill=GREEN, lh=12)
        if i > 2:
            s.line(fx + 6, yc(top + 16), fx + 6, yc(SHELF_TOPS[i - 2] + 26), stroke=GREEN, sw=1.2, marker="arrGreen", dash="3 3")
    s.line(fx - 14, yc(SHELF_TOPS[0] + 24), fx - 14, yc(SHELF_TOPS[4] + 6), stroke=GREEN, sw=1.4, marker="arrGreen", dash="6 3")
    s.text(fx - 18, yc(95), "día 1: de N1 a N5", size=9, fill=GREEN, anchor="middle", rotate=-90)

    # ---------------- vista lateral
    x1 = 860.0
    dpx = RACK_D * K
    s.text(x1, 86, "VISTA LATERAL", size=12, weight="bold")
    s.line(x1 - 30, floor, x1 + dpx + 60, floor, sw=2)
    for px in (x1, x1 + dpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    s.line(x1 - 10, yc(SHELF_TOPS[0]), x1 - 10, yc(SHELF_TOPS[4] - SHELF_T - 6), stroke=BLUE, sw=2)
    s.text(x1 - 16, yc(60), "riser ½\" nebulizadores desde P-1", size=9, fill=BLUE, anchor="middle", rotate=-90)
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x1, yc(top), dpx, SHELF_T * K, fill="#d1d5db", stroke=INK, sw=1.5)
        if 2 <= i <= 4:
            s.rect(x1 - 2.5 * K, yc(top + TRAY_H), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.4)
            c = CANOPY[i]
            s.rect(x1 - 1.7 * K, yc(top + TRAY_H + c), (TRAY_L - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
        else:
            for st in range(2):
                s.rect(x1 - 2.5 * K, yc(top + TRAY_H * (st + 1)), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
            s.rect(x1 + 12 * K, yc(top + 2 * TRAY_H + 5), 26 * K, 5 * K, fill="#9ca3af", stroke=INK, sw=1)
        if i <= 4:
            nxt = SHELF_TOPS[i] - SHELF_T
            for q in (0.25, 0.75):
                s.circle(x1 + dpx * q, yc(nxt - 3.0 - TUBE_D / 2), TUBE_D * K / 2, fill="#fef3c7", stroke=AMBER, sw=1.4)
            ny = yc(nxt - 3.0 - TUBE_D - 2.0)
            s.line(x1 - 10, ny, x1 + dpx * 0.5, ny, stroke=BLUE, sw=1.6)
            s.polyline([(x1 + dpx * 0.5 - 4, ny), (x1 + dpx * 0.5 + 4, ny), (x1 + dpx * 0.5, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
    s.rect(x1 - 12, yc(SHELF_TOPS[4] + 22), dpx + 24, 22 * K, fill="#374151", stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    by = floor + 34
    s.line(x1, by, x1 + dpx, by, sw=1); s.line(x1, by - 5, x1, by + 5, sw=1); s.line(x1 + dpx, by - 5, x1 + dpx, by + 5, sw=1)
    s.text(x1 + dpx / 2, by - 4, "45.7", size=11, anchor="middle")
    by2 = floor + 56
    s.line(x1 - 2.5 * K, by2, x1 - 2.5 * K + TRAY_L * K, by2, stroke=GREEN, sw=1)
    for px in (x1 - 2.5 * K, x1 - 2.5 * K + TRAY_L * K):
        s.line(px, by2 - 5, px, by2 + 5, stroke=GREEN, sw=1)
    s.text(x1 + dpx / 2, by2 - 4, "charola 50.8 (vuela 2.5 por lado)", size=10, fill=GREEN, anchor="middle")
    s.text(x1 + dpx / 2, floor + 78, "◄ atrás (pared, riser)   ·   frente (pasillo) ►", size=9, fill=GRAY, anchor="middle")

    # ---------------- planta de un nivel
    x2, y2 = 1150.0, 118.0
    s.text(x2, 86, "PLANTA DE UN NIVEL (N1–N4)", size=12, weight="bold")
    s.rect(x2, y2, wpx, dpx, fill="#d1d5db", stroke=INK, sw=1.5)
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
    by = y2 + dpx + 2.5 * K + 32
    s.line(x2, by, x2 + wpx, by, sw=1); s.line(x2, by - 5, x2, by + 5, sw=1); s.line(x2 + wpx, by - 5, x2 + wpx, by + 5, sw=1)
    s.text(x2 + wpx / 2, by - 4, "91.4 = 3 × 25.4 + 4 × 3.8", size=10, anchor="middle")

    # ---------------- tablas
    rows = [
        "#CAPACIDAD (geometría, no la cifra de la investigación)",
        "· Entrepaño 91.4 × 45.7 cm; charola 1020 = 25.4 × 50.8 cm.",
        "· Caben 3 atravesadas por nivel (76.2 de 91.4 cm; vuelan 2.5 cm",
        "  por lado). El '8–10/nivel' de research/estructura-invernadero",
        "  NO cabe: pide ~1.0 m² por nivel. [POR VERIFICAR con el rack armado]",
        "· En luz (N2–N4): 9 posiciones/rack. N5 oscuridad: 3 pilas × 2–3 =",
        "  6–9. N1 recién sembradas: 3 pilas × 2 = 6. Total ≈ 21–24 por rack.",
        "· 3 racks (Fase 1) ≈ 27 en luz (≈ 7 d cada una) → ~27 charolas/semana",
        "  con ciclo de 8–12 d: cierra la meta de 25–35 del plan.",
        "",
        "#CARGAS",
        "· Charola doble con coco saturado: 2.5–4 kg → nivel en luz 3 × 4 =",
        "  12 kg; nivel tapado (N1, N5) 3 × (2 × 4 + 4) = 36 kg. Rack: 362.9 kg/repisa.",
        "· Carga viva total ≈ 110 kg + peso propio [POR VERIFICAR en caja]:",
        "  margen > 10× por repisa; lo que importa es rigidez y humedad.",
        "· Forrar entrepaños de MDF con plástico o charola de drenaje.",
        "",
        "#ILUMINACIÓN",
        "· 2 × T8 LED 18 W 6500 K 1,400 lm por nivel N1–N4 = 8 tubos/rack",
        "  ($121 c/u JWJ = $968; bom/fase1 cubre UN rack: 3 racks = 24).",
        "· 12–14 h/día por K5 (GAB-A): 8 × 18 W × 13 h ≈ 1.9 kWh/día/rack.",
        "· Tubo a 3 cm bajo el entrepaño; luz→dosel 20–27 cm con paso de 43 cm.",
        "  Meta: 100–200 µmol/m²s en la charola (app Photone); si falta, baja",
        "  una posición el entrepaño de arriba [POR VERIFICAR con luxómetro].",
        "",
        "#RIEGO",
        "· Nebulizadores N1–N4 (2 boquillas/nivel) desde P-1 12 V; N5 a mano.",
        "· Tras el destape: riego SOLO por abajo (perforada dentro de lisa).",
        "· MT-1…4 capacitivo en la charola testigo de cada nivel; SHT31 en poste.",
    ]
    s.lines(1150.0, 400.0, rows, size=10.5, lh=15)
    s.text(24, H - 10, "Fuentes: referencia/03-instalacion §0.2–0.3 · research/estructura-invernadero §d · research/clima-agronomia §8 · research/semillas-sustrato-charolas §c · diseno/hidraulico §1 · bom/fase0-1.csv. Charola 1020 = 10×20 pulgadas.", size=9.5, fill=GRAY)
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
        fn().save(path)
        ok, size = validar(path)
        flag = "ok" if ok and size > 4096 else "REVISAR"
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        print(f"{flag:8s} {rel}  {size / 1024:.1f} KB")
        bad += 0 if ok and size > 4096 else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
