#!/usr/bin/env python3
"""Plantas 2D del patio (Fases 0-3) y alzado del rack Husky, en SVG puro.

Uso:
    python3 hardware/cad/layout.py            # escribe en docs/assets/diagramas/layout/
    python3 hardware/cad/layout.py --out DIR  # otra carpeta

Solo biblioteca estandar (Python 3.11). Sin fuentes externas ni scripts en el SVG.

Escalas:
    * Plantas: 1:50 -> 1 m = 100 px (S = 100). Norte arriba. Cotas en m.
    * Alzado del rack: 1:10 -> 1 cm = 4 px.

SUPUESTO DEL PATIO (anotado en cada plano): 10 x 8 m = 80 m2, casa al SUR (pared),
acceso por el NORTE, coladera en la esquina NORESTE, piso de losa/firme de concreto.
Si tu patio es distinto, cambia las constantes de la seccion GEOMETRIA y regenera;
las reglas de distancia (seccion "reglas") estan en docs/diseno/layout-patio.md.

Fuentes de los numeros: docs/referencia/03-instalacion.md,
docs/research/estructura-invernadero.md, docs/research/instalacion-tunel-detalle.md,
docs/research/electrico-respaldo-seguridad.md, docs/referencia/07-puntos-ciegos-y-riesgos.md,
docs/research/clima-agronomia.md, bom/fase0-2.csv.
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
AMBER = "#b45309"    # electrico
BLUE = "#1d4ed8"     # agua
WHITE = "#ffffff"
VER = "HomeGreen · v1 · 2026-09"

DASH = "6 4"         # linea discontinua (drenaje / 12 V DC / ampliacion futura)
DOT = "2 3"          # punteada (senal de sensor / Wi-Fi)
DASHDOT = "10 4 2 4" # cumbrera / canaleta


def fmt(v: float) -> str:
    """Numero corto sin ceros inutiles."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


class SVG:
    """Acumulador minimo de SVG con cabecera estandar de la wiki."""

    def __init__(self, w: int, h: int, title: str, subtitle: str = ""):
        self.w, self.h = w, h
        self.parts: list[str] = []
        self.add(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        )
        self.add(f"<title>{escape(title)}</title>")
        self.add(
            "<defs>"
            f'<marker id="arrInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{INK}"/></marker>'
            f'<marker id="arrBlue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{BLUE}"/></marker>'
            f'<marker id="arrAmber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{AMBER}"/></marker>'
            f'<marker id="arrGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{GREEN}"/></marker>'
            f'<marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            f'<path d="M2,8 L8,2" stroke="{INK}" stroke-width="1.2"/></marker>'
            f'<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="8" stroke="{INK}" stroke-width="1.2"/></pattern>'
            f'<pattern id="hatchGreen" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="6" stroke="{GREEN}" stroke-width="0.8"/></pattern>'
            f'<pattern id="roof" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
            f'<line x1="0" y1="0" x2="0" y2="10" stroke="{GRAY}" stroke-width="0.6"/></pattern>'
            "</defs>"
        )
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
        a = f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if rx:
            a += f' rx="{rx}"'
        if opacity is not None:
            a += f' fill-opacity="{opacity}"'
        self.add(a + "/>")

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None, cap="round"):
        a = f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if marker:
            a += f' marker-end="url(#{marker})"'
        self.add(a + "/>")

    def polyline(self, pts, stroke=INK, sw=1.5, dash=None, marker=None, fill="none", close=False):
        p = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        a = f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
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
        a = f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{FONT}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
        if weight != "normal":
            a += f' font-weight="{weight}"'
        if italic:
            a += ' font-style="italic"'
        if rotate is not None:
            a += f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"'
        self.add(a + f">{escape(s)}</text>")

    def lines(self, x, y, rows, size=11, fill=INK, lh=None, anchor="start", weight="normal"):
        """Varias lineas de texto apiladas; devuelve la y siguiente."""
        lh = lh or size + 3
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, size=size, fill=fill, anchor=anchor, weight=weight)
        return y + len(rows) * lh

    def save(self, path: Path) -> None:
        self.add("</svg>\n")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts), encoding="utf-8")


# ----------------------------------------------------------------------------- plantas
S = 100.0  # px por metro (1:50 con 1 m = 100 px)


class Plano(SVG):
    """Planta del patio en metros: x de oeste a este, y de norte a sur (norte arriba)."""

    W, H = 1480, 1150          # lienzo
    OX, OY = 90, 150           # origen del patio (esquina noroeste) en px

    def __init__(self, fase: int, subtitle: str):
        title = f"Planta · Fase {fase} · escala 1:50 · supuesto 10×8 m"
        super().__init__(self.W, self.H, title, subtitle)
        self.fase = fase

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

    # -- cotas ----------------------------------------------------------------
    def dim_h(self, x1, x2, y, label=None, color=INK, size=11, above=True):
        """Cota horizontal entre x1 y x2 (m) a la altura y (m)."""
        px1, px2, py = self.X(x1), self.X(x2), self.Y(y)
        self.line(px1, py - 6, px1, py + 6, stroke=color, sw=1)
        self.line(px2, py - 6, px2, py + 6, stroke=color, sw=1)
        self.line(px1, py, px2, py, stroke=color, sw=1, marker=None)
        # tics inclinados estilo arquitectonico
        for px in (px1, px2):
            self.line(px - 4, py + 4, px + 4, py - 4, stroke=color, sw=1.2)
        label = label if label is not None else f"{fmt(abs(x2 - x1))} m"
        ty = py - 5 if above else py + 14
        self.text((px1 + px2) / 2, ty, label, size=size, fill=color, anchor="middle")

    def dim_v(self, y1, y2, x, label=None, color=INK, size=11, left=True):
        """Cota vertical entre y1 y y2 (m) en la abscisa x (m)."""
        py1, py2, px = self.Y(y1), self.Y(y2), self.X(x)
        self.line(px - 6, py1, px + 6, py1, stroke=color, sw=1)
        self.line(px - 6, py2, px + 6, py2, stroke=color, sw=1)
        self.line(px, py1, px, py2, stroke=color, sw=1)
        for py in (py1, py2):
            self.line(px - 4, py + 4, px + 4, py - 4, stroke=color, sw=1.2)
        label = label if label is not None else f"{fmt(abs(y2 - y1))} m"
        tx = px - 5 if left else px + 5
        self.text(tx, (py1 + py2) / 2, label, size=size, fill=color, anchor="middle", rotate=-90)

    # -- marco del patio ------------------------------------------------------
    def patio(self, acceso=(4.2, 5.2), puerta_casa=(4.4, 5.3)):
        """Bardas N/E/O, pared de la casa al sur (achurada), acceso norte, cotas generales."""
        # bardas de 0.15 m por fuera del patio
        self.mrect(-0.15, -0.15, 10.3, 0.15, fill=LIGHT, stroke=INK, sw=1)   # norte
        self.mrect(-0.15, 0, 0.15, 8.0, fill=LIGHT, stroke=INK, sw=1)        # oeste
        self.mrect(10.0, 0, 0.15, 8.0, fill=LIGHT, stroke=INK, sw=1)         # este
        # casa al sur: banda achurada de 0.45 m
        self.mrect(-0.15, 8.0, 10.3, 0.45, fill="url(#hatch)", stroke=INK, sw=1.5)
        self.mtext(0.2, 8.3, "CASA (pared sur)", size=11, fill=INK, weight="bold")
        # patio
        self.mrect(0, 0, 10, 8, fill="none", stroke=INK, sw=2)
        # acceso norte (claro en la barda)
        a0, a1 = acceso
        self.mrect(a0, -0.15, a1 - a0, 0.15, fill=WHITE, stroke="none")
        self.mline(a0, -0.15, a0, 0, sw=1.5)
        self.mline(a1, -0.15, a1, 0, sw=1.5)
        self.mpoly([(a0, 0), (a0 + 0.05, -0.6)], sw=1.2)  # hoja de puerta abatida
        self.add(f'<path d="M{fmt(self.X(a0+0.05))},{fmt(self.Y(-0.6))} A{fmt(0.7*S)},{fmt(0.7*S)} 0 0 1 {fmt(self.X(a1))},{fmt(self.Y(-0.05))}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
        self.mtext((a0 + a1) / 2, -0.28, "ACCESO (norte) · zaguán 1.0 m", size=11, anchor="middle", weight="bold")
        # puerta de la casa al patio
        p0, p1 = puerta_casa
        self.mrect(p0, 8.0, p1 - p0, 0.45, fill=WHITE, stroke="none")
        self.mline(p0, 8.0, p0, 8.45, sw=1.5)
        self.mline(p1, 8.0, p1, 8.45, sw=1.5)
        self.mpoly([(p0, 8.0), (p0 + 0.05, 7.1)], sw=1.2)
        self.add(f'<path d="M{fmt(self.X(p0+0.05))},{fmt(self.Y(7.1))} A{fmt(0.9*S)},{fmt(0.9*S)} 0 0 1 {fmt(self.X(p1))},{fmt(self.Y(7.95))}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>')
        self.mtext((p0 + p1) / 2, 7.02, "puerta casa→patio 0.9 m", size=10, anchor="middle", fill=GRAY)
        # cotas generales
        self.dim_h(0, 10, -0.5, "10.00 m (supuesto)")
        self.dim_v(0, 8, -0.55, "8.00 m (supuesto)")
        # norte
        nx, ny = self.X(10.55), self.Y(8.15)
        self.circle(nx, ny, 22, stroke=INK, sw=1.2)
        self.polyline([(nx, ny - 20), (nx - 8, ny + 10), (nx, ny + 3), (nx + 8, ny + 10)], fill=INK, stroke=INK, sw=1, close=True)
        self.text(nx, ny - 26, "N", size=13, weight="bold", anchor="middle")
        # sol
        self.mtext(10.27, 1.0, "sol de mediodía: desde el SUR, muy alto (19° N; UV 11+ mar–sep)", size=10, fill=GRAY, rotate=90)

    # -- simbolos -------------------------------------------------------------
    def coladera(self, x, y, label="coladera (existente)"):
        s = 0.3
        self.mrect(x - s / 2, y - s / 2, s, s, fill=WHITE, stroke=BLUE, sw=1.5)
        for i in range(1, 4):
            self.mline(x - s / 2 + i * s / 4, y - s / 2, x - s / 2 + i * s / 4, y + s / 2, stroke=BLUE, sw=0.8)
            self.mline(x - s / 2, y - s / 2 + i * s / 4, x + s / 2, y - s / 2 + i * s / 4, stroke=BLUE, sw=0.8)
        if label:
            self.mtext(x - 0.2, y + 0.32, label, size=10, fill=BLUE, anchor="end")

    def toma(self, x, y, label="toma de agua (llave existente)"):
        self.mcircle(x, y, 0.09, fill=WHITE, stroke=BLUE, sw=1.8)
        self.mtext(x, y + 0.04, "T", size=10, fill=BLUE, anchor="middle", weight="bold")
        if label:
            self.mtext(x - 0.12, y - 0.14, label, size=10, fill=BLUE, anchor="end")

    def contacto(self, x, y, label, gfci=True):
        self.mrect(x - 0.1, y - 0.1, 0.2, 0.2, fill=WHITE, stroke=AMBER, sw=1.8)
        self.mline(x - 0.04, y - 0.05, x - 0.04, y + 0.05, stroke=AMBER, sw=1.5)
        self.mline(x + 0.04, y - 0.05, x + 0.04, y + 0.05, stroke=AMBER, sw=1.5)
        if label:
            self.mtext(x - 0.14, y - 0.14, label, size=10, fill=AMBER, anchor="end")

    def gabinete(self, x, y, w, h, rows, anchor_side="right"):
        self.mrect(x, y, w, h, fill="#fff7ed", stroke=AMBER, sw=2)
        self.mline(x + 0.03, y + 0.03, x + w - 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        self.mline(x + w - 0.03, y + 0.03, x + 0.03, y + h - 0.03, stroke=AMBER, sw=0.8)
        if anchor_side == "right":
            self.mlines(x + w + 0.06, y + 0.12, rows, size=10, fill=AMBER)
        elif anchor_side == "left":
            self.mlines(x - 0.06, y + 0.12, rows, size=10, fill=AMBER, anchor="end")
        elif anchor_side == "below":
            self.mlines(x, y + h + 0.16, rows, size=10, fill=AMBER)
        elif anchor_side == "above":
            self.mlines(x, y - 0.08 - 0.13 * (len(rows) - 1), rows, size=10, fill=AMBER)

    def poste(self, x, y, size=0.08):
        self.mrect(x - size / 2, y - size / 2, size, size, fill=INK, stroke=INK, sw=1)

    def rack(self, x, y, w=0.914, h=0.457, label="", dashed=False, label_below=True):
        """Rack Husky 91.4 × 45.7 cm visto en planta; 3 charolas 25×50 atravesadas."""
        self.mrect(x, y, w, h, fill="#e8f5e9" if not dashed else "none", stroke=GREEN, sw=1.8, dash=DASH if dashed else None)
        if not dashed:
            gap = (w - 3 * 0.254) / 4
            for i in range(3):
                cx = x + gap + i * (0.254 + gap)
                self.mrect(cx, y - 0.025, 0.254, 0.508, fill="none", stroke=GREEN, sw=0.9)
        if label:
            ly = y + h + 0.15 if label_below else y - 0.08
            self.mtext(x + w / 2, ly, label, size=10, fill=GREEN, anchor="middle")

    def mesa(self, x, y, w, h, rows, color=INK):
        self.mrect(x, y, w, h, fill=WHITE, stroke=color, sw=1.5)
        self.mrect(x + 0.04, y + 0.04, w - 0.08, h - 0.08, fill="none", stroke=color, sw=0.7)
        self.mlines(x + w / 2, y + h / 2 - 0.05 * (len(rows) - 1) + 0.04, rows, size=9.5, fill=color, anchor="middle", lh=12)

    def tinaco(self, cx, cy, r, rows):
        self.mcircle(cx, cy, r, fill="#eff6ff", stroke=BLUE, sw=2)
        self.mcircle(cx, cy, r * 0.72, fill="none", stroke=BLUE, sw=0.9)
        self.mcircle(cx, cy, 0.05, fill=BLUE, stroke=BLUE, sw=0.5)
        self.mlines(cx, cy - 0.02 - 0.06 * (len(rows) - 1), rows, size=9.5, fill=BLUE, anchor="middle", lh=12)

    def tambo(self, cx, cy, r, rows):
        self.mcircle(cx, cy, r, fill="#eff6ff", stroke=BLUE, sw=2)
        self.mcircle(cx, cy, r * 0.6, fill="none", stroke=BLUE, sw=0.9, dash="3 2")
        self.mlines(cx, cy + r + 0.16, rows, size=9.5, fill=BLUE, anchor="middle", lh=12)

    def nft_bancada(self, x, y, length, n=4, pitch=0.28, name="A", slope_to="E"):
        """Bancada de n lineas PVC 4 pulg (0.11 m) de `length` m, eje E-O."""
        h = pitch * n
        self.mrect(x, y, length, h, fill="#e8f5e9", stroke=GREEN, sw=1.2, dash="4 2")
        for i in range(n):
            cy = y + pitch / 2 + i * pitch
            self.mrect(x, cy - 0.055, length, 0.11, fill=WHITE, stroke=GREEN, sw=1.6)
            # canastillas cada 0.20 m (albahaca)
            for k in range(1, int(length / 0.2)):
                self.mcircle(x + k * 0.2, cy, 0.03, fill="#c8e6c9", stroke=GREEN, sw=0.6)
        # flecha de pendiente
        ax0, ax1 = (x + 0.3, x + length - 0.3) if slope_to == "E" else (x + length - 0.3, x + 0.3)
        self.mline(ax0, y + h + 0.1, ax1, y + h + 0.1, stroke=GREEN, sw=1.2, marker="arrGreen")
        self.mtext((x + x + length) / 2, y + h + 0.24, f"bancada {name} · {n} líneas PVC sanitario 4\" × {fmt(length)} m · pendiente 2–3 % → {'E' if slope_to=='E' else 'O'}", size=10, fill=GREEN, anchor="middle")

    def cama(self, x, y, w, h, rows):
        self.mrect(x, y, w, h, fill="url(#hatchGreen)", stroke=GREEN, sw=2)
        self.mrect(x + 0.06, y + 0.06, w - 0.12, h - 0.12, fill="none", stroke=GREEN, sw=0.8)
        self.mlines(x + w / 2, y + h / 2 - 0.06 * (len(rows) - 1), rows, size=9.5, fill=GREEN, anchor="middle", lh=12)

    def tunel(self, x, y, w, h, fase, door=(1.9, 2.8), post_every=2.0):
        """Tunel a dos aguas, cumbrera E-O, postes cada `post_every` m, puerta en la cabecera este."""
        # sombra del techo (proyeccion) y cuerpo
        self.mrect(x, y, w, h, fill="url(#roof)", stroke="none")
        self.mrect(x, y, w, h, fill=WHITE, stroke="none", opacity=0.55)
        self.mrect(x, y, w, h, fill="none", stroke=INK, sw=2.5)
        # cumbrera
        self.mline(x, y + h / 2, x + w, y + h / 2, stroke=INK, sw=1.2, dash=DASHDOT)
        self.mtext(x + w / 2, y + h / 2 - 0.06, "cumbrera (E–O) · techo a dos aguas ≥ 25 % · plástico UV cal. 720 blanco 25 % + malla antigranizo 10–20 cm arriba", size=9.5, fill=GRAY, anchor="middle")
        # flechas de escurrimiento hacia los aleros
        for xx in (x + 1.0, x + w - 1.0):
            self.mline(xx, y + h / 2 - 0.15, xx, y + 0.25, stroke=GRAY, sw=1, marker="arrInk")
            self.mline(xx, y + h / 2 + 0.15, xx, y + h - 0.25, stroke=GRAY, sw=1, marker="arrInk")
        # postes
        n = int(round(w / post_every))
        for i in range(n + 1):
            px = x + i * w / n
            self.poste(px, y)
            self.poste(px, y + h)
        # postes intermedios de cabecera si el claro > 3 m
        if h > 3.05:
            for yy in (y + h / 2,):
                self.poste(x, yy)
                self.poste(x + w, yy)
        # puerta (cabecera este)
        d0, d1 = door
        self.mline(x + w, d0, x + w, d1, stroke=WHITE, sw=4)
        self.mline(x + w, d0, x + w + 0.75, d0 + 0.35, stroke=INK, sw=1.2)
        self.mtext(x + w + 0.08, d1 + 0.14, "puerta 0.9 m", size=9.5, fill=GRAY)
        self.mtext(x + w - 0.1, y + h - 0.1, "faldones enrollables + malla antiáfidos (laterales N y S)", size=9.5, fill=GRAY, anchor="end")
        # etiqueta
        self.mtext(x + 0.1, y - 0.3, f"TÚNEL {fmt(w)}×{fmt(h)} m = {fmt(w*h)} m² · PTR 1½\" cal. 14 · anclado (placa + 4 anclas 3/8\" × 5\" por poste)", size=10.5, weight="bold")

    # -- leyenda y notas ------------------------------------------------------
    def leyenda(self, x, y, extra=()):
        self.text(x, y, "LEYENDA", size=12, weight="bold")
        items = [
            ("line", BLUE, None, "agua a presión / línea de red (½\")"),
            ("line", BLUE, DASH, "drenaje · rebosadero · purga (a coladera)"),
            ("line", BLUE, DASHDOT, "canaleta / bajante pluvial (0.5–1 %)"),
            ("line", AMBER, None, "127 V CA (circuito GFCI del patio)"),
            ("line", AMBER, DASH, "12 V DC (bus batería / bombas)"),
            ("line", AMBER, DOT, "señal de sensor · Wi-Fi"),
            ("fill", "#e8f5e9", GREEN, "cultivo: rack · bancada NFT · cama"),
            ("fill", "#fff7ed", AMBER, "gabinete IP65 (GAB-n)"),
            ("fill", "#eff6ff", BLUE, "tinaco · tambo"),
            ("fill", "url(#hatch)", INK, "casa (pared sur)"),
            ("fill", "url(#roof)", GRAY, "techo del túnel (proyección)"),
            ("line", GRAY, DASH, "elemento de la fase siguiente (reserva)"),
        ] + list(extra)
        yy = y + 18
        for kind, c1, c2, lab in items:
            if kind == "line":
                self.line(x, yy - 4, x + 34, yy - 4, stroke=c1, sw=2, dash=c2)
            else:
                self.rect(x, yy - 12, 34, 14, fill=c1, stroke=c2, sw=1.2)
            self.text(x + 42, yy, lab, size=11)
            yy += 19
        # simbolos
        yy += 4
        self.text(x, yy, "SÍMBOLOS", size=12, weight="bold")
        yy += 18
        sx = (x - self.OX) / S
        sy = (yy - self.OY) / S
        self.coladera(sx + 0.17, sy - 0.05, label=None); self.text(x + 42, yy, "coladera del patio", size=11); yy += 19
        self.toma(sx + 0.17, (yy - self.OY) / S - 0.05, label=None); self.text(x + 42, yy, "toma de agua (red SACMEX)", size=11); yy += 19
        self.contacto(sx + 0.17, (yy - self.OY) / S - 0.05, None); self.text(x + 42, yy, "contacto intemperie tipo in-use", size=11); yy += 19
        self.poste(sx + 0.17, (yy - self.OY) / S - 0.05); self.text(x + 42, yy, "poste PTR con placa anclada", size=11); yy += 19
        self.rect(x, yy - 12, 34, 14, fill="#e8f5e9", stroke=GREEN, sw=1.2)
        for i in range(3):
            self.rect(x + 3 + i * 10.5, yy - 14, 8, 18, fill="none", stroke=GREEN, sw=0.8)
        self.text(x + 42, yy, "rack Husky 91×46 cm (3 charolas 25×50 por nivel)", size=11); yy += 19
        return yy

    def notas(self, x, y, rows, title="NOTAS Y SUPUESTOS", size=10.5, lh=14):
        self.text(x, y, title, size=12, weight="bold")
        return self.lines(x, y + 18, rows, size=size, lh=lh)


# ----------------------------------------------------------------------------- GEOMETRIA (m)
# Cambia aqui si tu patio es distinto; todo lo demas se recalcula al regenerar.
COLADERA = (9.6, 0.4)            # esquina noreste
TOMA = (9.8, 7.92)               # llave existente en la pared de la casa
CONTACTO = (7.05, 7.92)          # contacto existente bajo el cobertizo -> GFCI en F1
CDC = (5.75, 8.08, 0.6, 0.3)     # centro de carga (interior de la casa)
CEREBRO = (1.4, 8.08, 2.3, 0.3)  # mini-PC HA + router + UPS (interior)
VARILLA = (5.0, 7.72)            # varilla de tierra (el electricista fija el punto real)
COBERTIZO = (6.4, 6.3, 3.5, 1.7) # alero/cobertizo existente (supuesto) 3.5 x 1.7 m
TUNEL_F1 = (0.6, 0.8, 6.0, 3.0)
TUNEL_F2 = (0.6, 0.8, 6.0, 5.0)
DOOR = (1.9, 2.8)                # claro de puerta en la cabecera este (y)
TINACO = (8.2, 1.6, 0.55)        # TK-1 750 L (diametro aprox. 1.1 m [POR VERIFICAR])
TLALOQUE = (6.95, 0.7, 0.3, 0.4)
P1 = (7.45, 2.35, 0.4, 0.25)     # bomba diafragma riego + F-1
F2BOX = (7.45, 2.85, 0.4, 0.25)  # duplex sedimento+carbon + SV-1 (llenado NFT)
GAB1 = (6.25, 3.45, 0.3, 0.3)
GAB2 = (6.25, 4.95, 0.3, 0.3)
GABDC = (6.5, 7.5, 0.4, 0.35)
RACK_XS = (1.0, 2.25, 3.5)       # 3 racks Husky, separados 0.34 m (los T8 de 1.2 m vuelan 14 cm por lado)
RACK4_X = 4.75
RACK_Y = 1.0
RIEGO_Y = 1.72                   # linea de riego frente a los racks
BANCADA_X, BANCADA_L = 1.5, 3.0
BANCADA_A_Y, BANCADA_B_Y = 2.4, 4.42
TAMBO = (4.95, 3.97, 0.29)
PUMPS_NFT = (5.35, 3.85, 0.4, 0.25)
MESA_TRASPLANTE = (5.6, 4.45, 0.6, 1.2)
CAMA1 = (7.25, 2.35, 0.9, 3.9)
CAMA2 = (8.7, 2.35, 0.9, 3.9)
CAMA3 = (0.3, 6.5, 3.2, 1.0)
COMPOSTA = (0.5, 7.5, 0.29)
MESA_COSECHA = (7.3, 7.45, 1.2, 0.5)
REFRI = (8.85, 7.42, 0.6, 0.55)
TINA = (9.65, 7.15, 0.2)
HIELERA = (7.6, 6.65, 0.35, 0.3)


def dist(pts):
    """Longitud (m) de una polilinea."""
    return sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


# Recorridos (polilineas en m) reutilizados por las fases y por la documentacion
RUTA_127V = [(CONTACTO[0], 7.97), (9.9, 7.97), (9.9, 3.6), (GAB1[0] + GAB1[2], 3.6)]
RUTA_RED = [(TOMA[0], TOMA[1] - 0.07), (TOMA[0], 1.9), (8.66, 1.9)]
RUTA_RIEGO = [(P1[0], 2.48), (7.1, 2.48), (7.1, RIEGO_Y), (6.6, RIEGO_Y), (RACK_XS[0], RIEGO_Y)]
RUTA_DREN_RACKS = [(RACK_XS[0], 0.87), (6.5, 0.87), (6.5, 1.3), (7.45, 1.3), (7.45, 0.5), (COLADERA[0] - 0.15, 0.45)]
RUTA_DC_F1 = [(GAB1[0] + GAB1[2], 3.6), (7.1, 3.6), (7.1, 2.48), (P1[0], 2.48)]
RUTA_LLENADO_NFT = [(F2BOX[0], 2.98), (6.6, 3.1), (5.0, 3.1), (5.0, TAMBO[1] - TAMBO[2])]
RUTA_PURGA_NFT = [(TAMBO[0] + 0.2, TAMBO[1] + 0.2), (6.6, 4.3), (7.2, 4.3), (7.2, 0.5), (COLADERA[0] - 0.15, 0.45)]
RUTA_DC_F2 = [(GABDC[0] + 0.2, GABDC[1]), (6.75, 5.95), (6.75, 5.6), (6.2, 5.6), (6.2, 3.97), (PUMPS_NFT[0] + PUMPS_NFT[2], 3.97)]


def base_comun(p: Plano):
    """Lo que existe en todas las fases: patio, casa, coladera, toma, contacto, cobertizo."""
    p.patio()
    p.coladera(*COLADERA)
    p.toma(*TOMA)
    # cobertizo existente (supuesto)
    x, y, w, h = COBERTIZO
    p.mrect(x, y, w, h, fill="url(#roof)", stroke="none")
    p.mrect(x, y, w, h, fill=WHITE, stroke="none", opacity=0.6)
    p.mrect(x, y, w, h, fill="none", stroke=GRAY, sw=1.5, dash=DASH)
    p.mtext(x + 0.05, y + 0.16, f"COBERTIZO / alero existente (supuesto) {fmt(w)}×{fmt(h)} m · techo, sin sol directo ni goteo", size=9.5, fill=GRAY)
    # interior de la casa: centro de carga y cerebro
    cx, cy, cw, ch = CDC
    p.mrect(cx, cy, cw, ch, fill=WHITE, stroke=AMBER, sw=1.5)
    p.mtext(cx + cw / 2, cy + 0.13, "centro de carga", size=9, fill=AMBER, anchor="middle")
    bx, by, bw, bh = CEREBRO
    p.mrect(bx, by, bw, bh, fill=WHITE, stroke=AMBER, sw=1.2, dash=DOT)
    p.mtext(bx + bw / 2, by + 0.19, "cerebro (interior): mini-PC HA + router + UPS", size=9.5, fill=AMBER, anchor="middle")


def seguridad_electrica(p: Plano):
    """GFCI en centro de carga, contacto intemperie, varilla de tierra (desde Fase 1)."""
    cx, cy, cw, ch = CDC
    p.mtext(cx + cw / 2, cy + 0.25, "+ QO120GFI", size=9, fill=AMBER, anchor="middle", weight="bold")
    p.contacto(*CONTACTO, "contacto GFCI intemperie in-use")
    vx, vy = VARILLA
    p.mcircle(vx, vy, 0.07, fill=WHITE, stroke=AMBER, sw=1.5)
    p.mline(vx, vy + 0.07, vx, vy + 0.2, stroke=AMBER, sw=1.2)
    for i, ww in enumerate((0.12, 0.08, 0.04)):
        p.mline(vx - ww / 2, vy + 0.2 + i * 0.04, vx + ww / 2, vy + 0.2 + i * 0.04, stroke=AMBER, sw=1.2)
    p.mline(vx, vy, cx, cy + 0.02, stroke=AMBER, sw=1, dash=DOT)
    p.mlines(vx + 0.12, vy - 0.02, ["varilla tierra copperweld", "5/8\"×3 m · ≤ 25 Ω · cal. 8"], size=9, fill=AMBER, lh=12)
    # 127 V al patio
    p.mpoly(RUTA_127V, stroke=AMBER, sw=2.2, marker="arrAmber")
    p.mtext(9.68, 7.6, f"127 V uso rudo ≈ {fmt(dist(RUTA_127V))} m (barda este)", size=9.5, fill=AMBER, rotate=-90)


def agua_fase1(p: Plano, tunel):
    """Tinaco, captacion, red, riego de racks y drenajes (Fase 1 en adelante)."""
    tx, ty, tw, th = tunel
    # canaletas en ambos aleros -> bajantes al este -> tlaloque -> tinaco
    p.mline(tx, ty - 0.08, tx + tw, ty - 0.08, stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mtext(tx + 0.1, ty - 0.14, "canalón PVC $269/3.07 m · pendiente 0.5–1 % → bajante NE", size=9.5, fill=BLUE)
    p.mline(tx, ty + th + 0.08, tx + tw, ty + th + 0.08, stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    p.mtext(tx + 0.1, ty + th + 0.24, "2.ª canaleta (alero sur) → bajante SE → colector aéreo (2 m) a la bajante NE", size=9.5, fill=BLUE)
    p.mline(tx + tw + 0.12, ty + th + 0.08, tx + tw + 0.12, ty - 0.08, stroke=BLUE, sw=1.5, dash=DASHDOT)
    lx, ly, lw, lh = TLALOQUE
    p.mline(tx + tw, ty - 0.08, lx, ly + 0.2, stroke=BLUE, sw=2, dash=DASHDOT)
    p.mrect(lx, ly, lw, lh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(lx + lw / 2, ly + 0.16, ["filtro", "hojas +", "tlaloque"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    p.mline(lx + lw, ly + 0.2, TINACO[0] - TINACO[2], 1.35, stroke=BLUE, sw=2, dash=DASHDOT, marker="arrBlue")
    # tinaco
    p.tinaco(*TINACO, ["TK-1 tinaco", "750 L", "opaco · base firme", "(lleno ≈ 750 kg)"])
    p.mtext(TINACO[0], TINACO[1] - 0.38, "LT-1 JSN-SR04T (tapa) · TT-1", size=8.5, fill=AMBER, anchor="middle")
    p.mtext(8.74, 1.84, "FV-1 flotador", size=9, fill=BLUE)
    # rebosadero a coladera
    p.mpoly([(TINACO[0] + 0.4, TINACO[1] - 0.4), (9.3, 0.6), (COLADERA[0] - 0.15, COLADERA[1])], stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(8.75, 0.95, "rebosadero", size=9, fill=BLUE)
    # red -> flotador
    p.mpoly(RUTA_RED, stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(9.68, 5.2, f"red ½\" ≈ {fmt(dist(RUTA_RED))} m → FV-1 (solo rellena)", size=9.5, fill=BLUE, rotate=-90)
    # salida del tinaco -> V-1/F-1 -> P-1 -> tunel
    p.mpoly([(TINACO[0], TINACO[1] + TINACO[2]), (TINACO[0], 2.48), (P1[0] + P1[2], 2.48)], stroke=BLUE, sw=2)
    p.mtext(TINACO[0] + 0.06, 2.38, "V-1 + F-1", size=9, fill=BLUE)
    px, py, pw, ph = P1
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(px + pw / 2, py + 0.11, ["P-1 diafragma 12 V", "+ presostato (caja IP65)"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    p.mpoly(RUTA_RIEGO, stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(4.4, RIEGO_Y + 0.14, "riego: manifold + 1 válvula por rack → nebulizadores N1–N4 (2 boquillas/nivel)", size=9.5, fill=BLUE, anchor="middle")
    for rx in RACK_XS:
        p.mline(rx + 0.457, RIEGO_Y, rx + 0.457, RACK_Y + 0.457 + 0.02, stroke=BLUE, sw=1.2, marker="arrBlue")
    # drenaje de racks -> coladera
    p.mpoly(RUTA_DREN_RACKS, stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(7.55, 1.5, f"drenaje racks → coladera ≈ {fmt(dist(RUTA_DREN_RACKS))} m", size=9, fill=BLUE, rotate=-90)


def racks_tunel(p: Plano, rack4=False):
    for i, rx in enumerate(RACK_XS, 1):
        p.rack(rx, RACK_Y, label=f"rack {i}")
    if rack4:
        p.rack(RACK4_X, RACK_Y, label="rack 4 (opcional)", dashed=True)
    p.mtext(RACK4_X + 1.0, RACK_Y + 0.28, "racks Husky 183×91×46 cm · 5 niveles · nivelados y calzados", size=9, fill=GREEN)
    p.dim_h(RACK_XS[0] + 0.914, RACK_XS[1], RACK_Y + 0.23, "0.34", size=8.5)


def electrico_tunel(p: Plano, tunel, extractor_y):
    """127 V dentro del tunel: T8 por rack y extractor, todo por relés de GAB-1."""
    tx, ty, tw, th = tunel
    gx, gy, gw, gh = GAB1
    p.gabinete(gx, gy, gw, gh, ["GAB-1 IP65 (poste SE, a 1.2 m): ESP32 nodo-riego-v1", "relé 4 ch · fuente 12 V 5 A · buck 5 V"], anchor_side="below")
    ruta = [(gx + 0.15, gy), (6.4, 0.94), (0.8, 0.94), (0.8, extractor_y)]
    p.mpoly(ruta, stroke=AMBER, sw=1.8, marker="arrAmber")
    for rx in RACK_XS:
        p.mline(rx + 0.2, 0.94, rx + 0.2, RACK_Y, stroke=AMBER, sw=1.2, marker="arrAmber")
    p.mtext(0.74, min(extractor_y + 0.5, 2.8), "127 V aéreo (2 m) → T8 ×2/nivel + extractor", size=9, fill=AMBER, rotate=-90)
    # extractor
    p.mcircle(tx, extractor_y, 0.14, fill=WHITE, stroke=AMBER, sw=1.5)
    for a in (0, 120, 240):
        p.add(f'<path d="M{fmt(p.X(tx))},{fmt(p.Y(extractor_y))} l{fmt(0.11*S)},0 a{fmt(0.05*S)},{fmt(0.05*S)} 0 0 1 -{fmt(0.055*S)},{fmt(0.09*S)} z" fill="{AMBER}" fill-opacity="0.5" stroke="none" transform="rotate({a} {fmt(p.X(tx))} {fmt(p.Y(extractor_y))})"/>')
    p.mtext(tx + 0.18, extractor_y - 0.2, "extractor", size=9, fill=AMBER)
    p.mtext(tx + 0.18, extractor_y + 0.32, "HR > 70 %", size=9, fill=AMBER)
    # sensores
    p.mcircle(3.6, 2.0, 0.05, fill=AMBER, stroke=AMBER)
    p.mtext(3.72, 2.04, "SHT31 T/HR a 1.5 m (centro)", size=9, fill=AMBER)
    p.mtext(3.72, 2.18, "MT-1…4 capacitivos en charola testigo por nivel (conector arriba)", size=9, fill=AMBER)
    # 12 V a P-1 y sensores del tinaco
    p.mpoly(RUTA_DC_F1, stroke=AMBER, sw=1.6, dash=DASH, marker="arrAmber")
    p.mtext(7.16, 3.1, "12 V", size=9, fill=AMBER, rotate=-90)
    p.mline(P1[0] + P1[2], P1[1], TINACO[0] - 0.2, TINACO[1] + TINACO[2] - 0.05, stroke=AMBER, sw=1.2, dash=DOT)
    # wifi
    p.mtext(CEREBRO[0] + CEREBRO[2] + 0.08, CEREBRO[1] + 0.19, "Wi-Fi → GAB-1/GAB-2 (≈ 6 m, una pared)", size=9, fill=AMBER)


def zona_cosecha(p: Plano, refri=False, gabdc=False, hielera=True):
    x, y, w, h = MESA_COSECHA
    p.mesa(x, y, w, h, ["mesa de cosecha/empaque", "acero inox o polietileno (NOM-251)"])
    if refri:
        rx, ry, rw, rh = REFRI
        p.mrect(rx, ry, rw, rh, fill=WHITE, stroke=INK, sw=1.5)
        p.mline(rx, ry + 0.2, rx + rw, ry + 0.2, sw=0.8)
        p.mlines(rx + rw / 2, ry + 0.33, ["refri 4–5 °C", "9–11 ft³", "GFCI 2"], size=8.5, anchor="middle", lh=10)
        p.contacto(8.7, 7.92, None)
    tx_, ty_, tr = TINA
    p.mcircle(tx_, ty_, tr, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(tx_, ty_ - 0.32, ["tina lavado", "charolas + H2O2", "y lavamanos"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    if hielera:
        hx, hy, hw, hh = HIELERA
        p.mrect(hx, hy, hw, hh, fill=WHITE, stroke=INK, sw=1.2)
        p.mtext(hx + hw + 0.06, hy + 0.2, "hielera 45–50 L", size=8.5)
    cx, cy, cw, ch = COBERTIZO
    p.mline(cx, cy, cx + cw, cy, stroke=GREEN, sw=1.5, dash="2 4")
    p.mtext(cx + cw - 0.05, cy - 0.06, "cortina plástica: zona de corte separada del cultivo (NOM-251)", size=9, fill=GREEN, anchor="end")
    if gabdc:
        gx, gy, gw, gh = GABDC
        p.gabinete(gx, gy, gw, gh, ["GAB-DC IP65: LiFePO4 100 Ah + EPEVER LS2024B", "+ fusiblera · a 30 cm del piso · lejos del 127 V"], anchor_side="above")


def composta(p: Plano):
    p.tambo(*COMPOSTA, ["tambo composta", "(sustrato usado)"])


def fase0():
    p = Plano(0, "Rack bajo techo + mesa de siembra + toma de agua · sin túnel, sin automatización · validación comercial (semanas 1–6)")
    base_comun(p)
    # contacto existente (sin GFCI todavia)
    p.contacto(*CONTACTO, "contacto existente (en F1 se vuelve GFCI)")
    # rack y mesa bajo el cobertizo
    p.rack(7.0, 7.5, label="rack Husky 5 niveles 183×91×46 cm ($2,019) · nivelado y calzado", label_below=False)
    p.mesa(8.1, 7.3, 1.2, 0.6, ["mesa de siembra 1.2×0.6", "báscula · atomizador · H2O2"])
    p.mcircle(*TINA[:2], TINA[2], fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(TINA[0], TINA[1] - 0.3, ["cubeta remojo /", "tina lavado"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    p.mcircle(0.5, 7.5, 0.2, fill=WHITE, stroke=INK, sw=1.2)
    p.mtext(0.5, 7.2, "cubeta sustrato usado", size=8.5, anchor="middle")
    # pasillo de trabajo frente al rack
    p.dim_v(6.5, 7.5, 7.45, "≥ 0.9 pasillo", size=9)
    p.dim_h(7.914, TOMA[0], 7.1, "1.9 m a la toma (< 10 m ✓)", size=9)
    # manguera de la toma a la cubeta
    p.mline(TOMA[0], TOMA[1] - 0.09, TINA[0], TINA[1] + 0.2, stroke=BLUE, sw=1.5)
    # reserva del tunel de fase 1
    tx, ty, tw, th = TUNEL_F1
    p.mrect(tx, ty, tw, th, fill="none", stroke=GRAY, sw=1.5, dash=DASH)
    p.mtext(tx + tw / 2, ty + th / 2, "RESERVA: túnel 3×6 m de Fase 1 — trazar con hilo y escuadra 3-4-5 desde ahora; no estorbar con nada pesado", size=10.5, fill=GRAY, anchor="middle")
    p.mtext(tx + tw / 2, ty + th / 2 + 0.25, "medir aquí 3 días T mín/máx (ideal 16–24 °C) y luz con la app Photone (100–200 µmol/m²s)", size=10, fill=GRAY, anchor="middle")
    p.mrect(TUNEL_F2[0], TUNEL_F1[1] + TUNEL_F1[3], TUNEL_F2[2], 2.0, fill="none", stroke=GRAY, sw=1, dash="2 4")
    p.mtext(tx + tw / 2, 5.0, "ampliación Fase 2 (+2 m al sur)", size=9.5, fill=GRAY, anchor="middle")
    p.mtext(8.2, 1.6, "reserva tinaco F1", size=9.5, fill=GRAY, anchor="middle")
    p.mcircle(*TINACO, fill="none", stroke=GRAY, sw=1, dash=DASH)
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_h(0, tx, 0.45, "0.60", size=9)
    # leyenda y notas
    yy = p.leyenda(1130, 92)
    p.lines(1130, yy + 14, [
        "QUÉ HAY EN FASE 0",
        "· 1 rack Husky (5 niveles) bajo el cobertizo, pegado a la",
        "  pared sur: luz indirecta, sin sol de mediodía ni goteo.",
        "· Mesa de siembra + cubeta de remojo junto a la toma.",
        "· Contacto existente (T8 opcionales con timer; no en BOM).",
        "· 20 charolas 10×20; 6 de prueba (2 variedades) primero.",
        "· Nada más: la Fase 0 valida que los chefs PAGAN.",
        "",
        "QUÉ MEDIR ANTES DE FASE 1",
        "· T mín/máx 3 días en el punto del rack y en la reserva.",
        "· Luz (Photone) mañana/mediodía/tarde en el rack.",
        "· Diagonales de la reserva 3×6 (iguales ± 1 cm).",
        "· Piso: nivel de manguera; grietas; bordes < 15 cm.",
        "· Coladera funcionando (echar 10 L y ver que traga).",
        "· ¿Condominio? Art. 21/23 antes de perforar (07 §9).",
    ], size=10.5, lh=15)
    p.notas(90, 1027, [
        "SUPUESTO: patio 10 × 8 m (80 m²), casa al SUR, acceso por el NORTE, coladera en la esquina NE, piso de losa/firme. Si tu patio difiere, cambia las constantes de GEOMETRIA en hardware/cad/layout.py y regenera.",
        "Reglas que mandan (mantenerlas aunque cambie la forma): rack bajo techo con toma a < 10 m y contacto cerca; pasillo ≥ 0.9 m frente al rack; nada tapa la coladera; la reserva del túnel queda ≥ 0.6 m de bardas y ≥ 0.8 m de la barda norte.",
        "Fuentes: referencia/03-instalacion §0.1–0.2 · research/estructura-invernadero §d · bom/fase0.csv · referencia/07 §9. Escala 1:50 (1 m = 100 px en el SVG). Norte arriba.",
    ], size=10.5, lh=15)
    return p


def fase1():
    p = Plano(1, "Túnel 3×6 m con 3 racks + tinaco 750 L + gabinete IP65 + canaleta→tinaco + línea eléctrica GFCI desde la casa · meses 2–4")
    base_comun(p)
    tx, ty, tw, th = TUNEL_F1
    p.tunel(tx, ty, tw, th, 1, door=DOOR)
    racks_tunel(p)
    p.mesa(1.0, 2.9, 1.2, 0.6, ["mesa de siembra 1.2×0.6", "+ tapete térmico (dic–feb)"])
    p.mtext(2.4, 3.6, "zona libre: carrito de charolas / lavado en seco", size=9, fill=GRAY)
    agua_fase1(p, TUNEL_F1)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F1, extractor_y=ty + th / 2)
    zona_cosecha(p, refri=False, gabdc=False)
    composta(p)
    # ampliacion futura
    p.mrect(TUNEL_F2[0], ty + th, tw, 2.0, fill="none", stroke=GRAY, sw=1.2, dash=DASH)
    p.mtext(tx + tw / 2, 5.0, "ampliación Fase 2 (+2 crujías = +2 m al sur): dejar los empalmes de la fachada sur atornillados, no soldados", size=10, fill=GRAY, anchor="middle")
    # cotas
    p.dim_h(tx, tx + tw, ty - 0.5, "6.00")
    p.dim_v(ty, ty + th, tx - 0.35, "3.00")
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_h(0, tx, 0.45, "0.60", size=9)
    p.dim_v(ty + th, 8.0, 3.3, "4.20 libre hasta la casa", size=9)
    p.dim_v(RACK_Y + 0.457, 2.4, 4.7, "0.94 pasillo", size=9)
    p.dim_h(tx + tw, TINACO[0] - TINACO[2], 1.5, "1.05", size=9)
    p.dim_h(TINACO[0] + TINACO[2], COLADERA[0], 1.2, "0.85", size=9)
    # leyenda y notas
    yy = p.leyenda(1130, 92)
    p.lines(1130, yy + 14, [
        "QUÉ CAMBIA VS. FASE 0",
        "· Túnel 3×6 (18 m²) PTR anclado a la losa; cumbrera E–O,",
        "  puerta al este (de frente al acceso y al tinaco).",
        "· 3 racks en fila al norte + rack de F0 mudado adentro.",
        "· Tinaco 750 L en la esquina NE: canaleta→tlaloque→tinaco,",
        "  rebosadero a la coladera (0.85 m), red solo por flotador.",
        "· GAB-1 (ESP32 + relés + fuente) en el poste SE, a 1.2 m.",
        "· Circuito del patio: QO120GFI en centro de carga →",
        "  contacto in-use bajo el cobertizo → ≈ 11 m de cable",
        "  uso rudo por la barda este → GAB-1. Varilla de tierra.",
        "· Cobertizo = cosecha/empaque/lavado (mesa + tina).",
        "· Composta en tambo (SO): sustrato usado 100–150 kg/mes.",
        "",
        "RECORRIDOS (m, sobre este supuesto)",
        f"· 127 V contacto→GAB-1 ≈ {fmt(dist(RUTA_127V))} · 12 V GAB-1→P-1 ≈ {fmt(dist(RUTA_DC_F1))}",
        f"· Red→flotador ≈ {fmt(dist(RUTA_RED))} · riego P-1→rack 1 ≈ {fmt(dist(RUTA_RIEGO))}",
        f"· Drenaje racks→coladera ≈ {fmt(dist(RUTA_DREN_RACKS))} · canaleta 6 + 6 + bajantes",
    ], size=10.5, lh=15)
    p.notas(90, 1027, [
        "SUPUESTO: patio 10 × 8 m, casa al SUR, acceso NORTE, coladera NE, losa de concreto sana (≥ 10 cm; anclas a ≥ 15 cm del borde). Postes cada 2 m (8) o cada 3 m (6): lo define el herrero; 4 anclas de cuña 3/8\"×5\" por placa, sellador PU.",
        "Distancias mínimas: túnel ≥ 0.6 m de bardas (tensar plástico, drenaje perimetral) y ≥ 0.8 m de la barda norte (canaleta + paso); pasillo interior ≥ 0.9 m; puerta 0.9 m; tinaco sobre piso firme (750 kg) sin tapar la coladera; GAB-1 a ≥ 1.2 m del piso y del lado opuesto al riego.",
        "Nada eléctrico de 127 V en el patio sin GFCI + tierra + gabinete IP65 (NOM-001-SEDE, lugar mojado). Fuentes: referencia/03 §1 · research/instalacion-tunel-detalle §1–4 · research/estructura-invernadero · research/electrico-respaldo-seguridad §3.6 · bom/fase1.csv.",
    ], size=10.5, lh=15)
    return p


def nft_fase2(p: Plano):
    """Dos bancadas de 4 lineas, tambo 200 L, bombas 12 V, manifold, retorno, llenado y purga."""
    pitch = 0.28
    p.nft_bancada(BANCADA_X, BANCADA_A_Y, BANCADA_L, 4, pitch, "A", "E")
    p.nft_bancada(BANCADA_X, BANCADA_B_Y, BANCADA_L, 4, pitch, "B", "E")
    # manifold de alimentacion (extremo alto, oeste) con 8 valvulas
    mx = BANCADA_X - 0.08
    p.mline(mx, BANCADA_A_Y, mx, BANCADA_B_Y + 4 * pitch, stroke=BLUE, sw=2.2)
    for by in (BANCADA_A_Y, BANCADA_B_Y):
        for i in range(4):
            cy = by + pitch / 2 + i * pitch
            p.mline(mx, cy, BANCADA_X, cy, stroke=BLUE, sw=1.2, marker="arrBlue")
            p.mcircle(mx, cy, 0.03, fill=WHITE, stroke=BLUE, sw=1)
    p.mtext(mx - 0.08, 3.97, "manifold ¾\" · 8 válvulas de compuerta · 1–2 L/min por línea", size=9, fill=BLUE, anchor="middle", rotate=-90)
    # suministro desde bombas por la pared sur
    px, py, pw, ph = PUMPS_NFT
    p.mrect(px, py, pw, ph, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(px + pw / 2, py + 0.11, ["P-1/P-2 diafragma 12 V", "+ F-1 malla 120 + FT-1"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    p.mpoly([(px + 0.1, py + ph), (5.45, 5.72), (mx, 5.72), (mx, BANCADA_B_Y + 4 * pitch)], stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(3.4, 5.66, "subida ¾\" al manifold (por la pared sur, a 30 cm del piso)", size=9, fill=BLUE, anchor="middle")
    # retornos (extremo bajo, este) -> tambo
    rx = BANCADA_X + BANCADA_L + 0.06
    tcx, tcy, tr = TAMBO
    p.mline(rx, BANCADA_A_Y, rx, tcy - tr - 0.02, stroke=BLUE, sw=2, dash=None)
    p.mline(rx, BANCADA_B_Y + 4 * pitch, rx, tcy + tr + 0.02, stroke=BLUE, sw=2)
    p.mline(rx, tcy - tr - 0.02, tcx - 0.1, tcy - tr - 0.02, stroke=BLUE, sw=2, marker="arrBlue")
    p.mline(rx, tcy + tr + 0.02, tcx - 0.1, tcy + tr + 0.02, stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(rx + 0.04, 2.55, "retorno 2\" por gravedad", size=9, fill=BLUE, rotate=-90)
    p.mcircle(rx, 3.62, 0.04, fill=AMBER, stroke=AMBER)
    p.mtext(rx + 0.08, 3.5, "AT-1 pH · AT-2 EC · TT-2", size=8.5, fill=AMBER)
    p.mtext(rx + 0.08, 3.62, "(en el retorno, mezcla)", size=8.5, fill=AMBER)
    # tambo
    p.tambo(tcx, tcy, tr, ["TK-2 tambo 200 L", "tapado · a la sombra · 18–22 °C"])
    p.mtext(tcx, tcy - tr - 0.12, "DP-1/2/3 peristálticas A/B/pH− → al tambo, junto a la succión", size=8.5, fill=AMBER, anchor="middle")
    p.mline(tcx + tr, tcy, px, tcy, stroke=BLUE, sw=2, marker="arrBlue")
    # llenado desde tinaco via duplex + SV-1
    fx, fy, fw, fh = F2BOX
    p.mpoly([(TINACO[0], 2.48), (TINACO[0], 2.98), (fx + fw, 2.98)], stroke=BLUE, sw=2)
    p.mrect(fx, fy, fw, fh, fill=WHITE, stroke=BLUE, sw=1.5)
    p.mlines(fx + fw / 2, fy + 0.11, ["F-2 dúplex sed.+carbón", "+ SV-1 solenoide NC"], size=8.5, fill=BLUE, anchor="middle", lh=10)
    p.mpoly(RUTA_LLENADO_NFT, stroke=BLUE, sw=2, marker="arrBlue")
    p.mtext(5.9, 3.02, "llenado (quita cloro)", size=8.5, fill=BLUE, anchor="middle")
    # purga SV-2 -> coladera
    p.mpoly(RUTA_PURGA_NFT, stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(7.14, 2.1, f"SV-2 purga (cambio cada 2–3 sem) ≈ {fmt(dist(RUTA_PURGA_NFT))} m → coladera", size=9, fill=BLUE, rotate=-90)
    # mesa de trasplante
    mx_, my_, mw_, mh_ = MESA_TRASPLANTE
    p.mesa(mx_, my_, mw_, mh_, ["mesa", "germinación", "(foami) y", "trasplante"])
    # pasillos
    p.dim_v(BANCADA_A_Y + 4 * pitch, BANCADA_B_Y, 2.9, "0.90 pasillo", size=9)
    p.dim_h(TUNEL_F2[0], BANCADA_X, 4.0, "0.90", size=9)
    p.dim_h(BANCADA_X, BANCADA_X + BANCADA_L, 2.25, "3.00", size=9)
    p.dim_v(BANCADA_A_Y, BANCADA_A_Y + 4 * pitch, 1.3, "1.12", size=9)


def dc_first_fase2(p: Plano):
    """GAB-2 nodo NFT, bus 12 V desde GAB-DC (cobertizo), ESP32-CAM, panel opcional."""
    gx, gy, gw, gh = GAB2
    p.gabinete(gx, gy, gw, gh, ["GAB-2 IP65: ESP32 nodo-nft-v2", "pH/EC · MOSFET peristálticas", "solenoides · detector CFE"], anchor_side="below")
    p.mpoly(RUTA_DC_F2, stroke=AMBER, sw=1.8, dash=DASH, marker="arrAmber")
    p.mtext(6.85, 6.9, f"bus 12 V ≈ {fmt(dist(RUTA_DC_F2))} m (cal. [POR VERIFICAR] por caída ≤ 3 %)", size=9, fill=AMBER, rotate=-90)
    p.mline(6.2, 5.1, gx, 5.1, stroke=AMBER, sw=1.4, dash=DASH, marker="arrAmber")
    # detector CFE / cargador desde el contacto GFCI
    p.mline(CONTACTO[0], CONTACTO[1] - 0.1, GABDC[0] + 0.2, GABDC[1] + GABDC[3], stroke=AMBER, sw=1.8, marker="arrAmber")
    # panel opcional
    p.mrect(7.15, 8.1, 0.45, 0.25, fill=WHITE, stroke=AMBER, sw=1.2, dash=DASH)
    p.mtext(7.375, 8.27, "PV 100 W opc.", size=8.5, fill=AMBER, anchor="middle")
    p.mtext(7.65, 8.27, "→ en azotea de la casa (nunca sobre el plástico)", size=8.5, fill=AMBER)
    p.mline(7.15, 8.2, GABDC[0] + GABDC[2], GABDC[1] + 0.2, stroke=AMBER, sw=1.2, dash=DASH)
    # ESP32-CAM en el poste NE
    cx, cy = TUNEL_F2[0] + TUNEL_F2[2], TUNEL_F2[1]
    p.mpoly([(cx, cy), (cx + 0.9, cy + 0.9), (cx + 0.2, cy + 1.6)], stroke=AMBER, sw=0.8, dash=DOT, fill="#fff7ed", close=True)
    p.mcircle(cx, cy, 0.07, fill=AMBER, stroke=AMBER)
    p.mtext(cx + 0.22, cy + 0.42, "ESP32-CAM: puerta + tinaco (movimiento nocturno)", size=8.5, fill=AMBER, rotate=45)
    # bomba sumergible 127 V solo trasiego
    p.mlines(TINACO[0], TINACO[1] + 0.36, ["sumergible 127 V", "solo trasiego"], size=8, fill=GRAY, anchor="middle", lh=9)


def fase2():
    p = Plano(2, "Túnel ampliado a 5×6 m · 8 líneas NFT de 3 m (2 bancadas de 4) · tambo 200 L · GAB-DC con batería · refrigerador y zona de cosecha junto a la casa · meses 5–9")
    base_comun(p)
    tx, ty, tw, th = TUNEL_F2
    p.tunel(tx, ty, tw, th, 2, door=DOOR)
    racks_tunel(p, rack4=True)
    agua_fase1(p, TUNEL_F2)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F2, extractor_y=ty + th / 2)
    nft_fase2(p)
    zona_cosecha(p, refri=True, gabdc=True)
    dc_first_fase2(p)
    composta(p)
    # reserva camas F3
    for (x, y, w, h) in (CAMA1, CAMA2, CAMA3):
        p.mrect(x, y, w, h, fill="none", stroke=GRAY, sw=1.2, dash=DASH)
    p.mtext(CAMA1[0] + CAMA1[2] / 2, CAMA1[1] + 2.0, "reserva camas F3", size=9, fill=GRAY, anchor="middle", rotate=-90)
    p.mtext(CAMA3[0] + CAMA3[2] / 2, CAMA3[1] + 0.55, "reserva cama F3 + gantry", size=9, fill=GRAY, anchor="middle")
    # cotas
    p.dim_h(tx, tx + tw, ty - 0.5, "6.00")
    p.dim_v(ty, ty + th, tx - 0.35, "5.00")
    p.dim_v(0, ty, 0.3, "0.80", size=9)
    p.dim_h(0, tx, 0.45, "0.60", size=9)
    p.dim_v(ty + th, 8.0, 3.3, "2.20 hasta la casa", size=9)
    p.dim_v(RACK_Y + 0.457, BANCADA_A_Y, 4.7, "0.94", size=9)
    # leyenda y notas
    yy = p.leyenda(1130, 92)
    p.lines(1130, yy + 14, [
        "QUÉ CAMBIA VS. FASE 1",
        "· Fachada sur del túnel se mueve 2 m: 5×6 = 30 m² (+6–8",
        "  tramos PTR, mismas bases). Cumbrera queda al centro.",
        "· 2 bancadas NFT de 4 líneas × 3 m (alto al oeste, 2–3 %),",
        "  pasillo de 0.9 m entre ellas; tambo 200 L al este.",
        "· Manifold al oeste; retornos al este con pH/EC/T.",
        "· Llenado tinaco→dúplex→SV-1→tambo; purga SV-2→coladera.",
        "· DC-first: GAB-DC (batería 100 Ah + EPEVER) en el",
        "  cobertizo, bus 12 V ≈ 4 m a bombas P-1/P-2 y GAB-2.",
        "· Cobertizo = cuarto de cosecha: mesa inox, refri 4–5 °C",
        "  (contacto GFCI 2), tina/lavamanos, hielera, cortina.",
        "· ESP32-CAM al poste NE; rack 4 opcional; mesa de",
        "  germinación/trasplante al este de las bancadas.",
        "",
        "RECORRIDOS (m, sobre este supuesto)",
        f"· Bus 12 V GAB-DC→bombas ≈ {fmt(dist(RUTA_DC_F2))} · llenado ≈ {fmt(dist(RUTA_LLENADO_NFT))}",
        f"· Purga→coladera ≈ {fmt(dist(RUTA_PURGA_NFT))} · manifold 3.2 + subida ≈ 6",
    ], size=10.5, lh=15)
    p.notas(90, 1027, [
        "SUPUESTO: patio 10 × 8 m, casa al SUR, acceso NORTE, coladera NE. Separación entre líneas NFT 28 cm eje a eje (bancada 1.12 m) [POR VERIFICAR con el porte de la albahaca a 20 cm entre canastillas; con 30–35 cm la bancada sube a 1.2–1.4 m y el pasillo baja a 0.7 m].",
        "Distancias mínimas: pasillos ≥ 0.9 m (bancadas se atienden por un solo lado si miden ≤ 1.2 m); tambo tapado y a la sombra (18–22 °C); sondas en el RETORNO; peristálticas al tambo cerca de la succión; GAB-DC elevado 30 cm y separado del 127 V; refri bajo techo con contacto GFCI propio.",
        "Fuentes: referencia/03 §2 · research/hidroponia-nft · research/electrico-respaldo-seguridad §2.4 y §3.6 · research/inocuidad-operativa §4 (NOM-251) · referencia/07 §1–3 y §10 · bom/fase2.csv.",
    ], size=10.5, lh=15)
    return p


def fase3():
    p = Plano(3, "Fase 2 + camas elevadas personales con goteo desde HA + gantry XY tipo FarmBot + cámara fija de visión · mes 10+ · cero presión comercial")
    base_comun(p)
    tx, ty, tw, th = TUNEL_F2
    p.tunel(tx, ty, tw, th, 3, door=DOOR)
    racks_tunel(p, rack4=True)
    agua_fase1(p, TUNEL_F2)
    seguridad_electrica(p)
    electrico_tunel(p, TUNEL_F2, extractor_y=ty + th / 2)
    nft_fase2(p)
    zona_cosecha(p, refri=True, gabdc=True)
    dc_first_fase2(p)
    composta(p)
    # camas elevadas
    areas = []
    for i, (x, y, w, h) in enumerate((CAMA1, CAMA2, CAMA3), 1):
        areas.append(w * h)
        rows = [f"cama {i}", f"{fmt(w)}×{fmt(h)} m = {fmt(w*h)} m²", "alt. 0.7–0.9 m [POR VERIFICAR]"]
        p.cama(x, y, w, h, rows)
    # goteo desde tinaco via SV-3 (HA)
    ruta_goteo_e = [(TINACO[0] + 0.3, TINACO[1] + 0.45), (8.5, 2.25), (8.5, CAMA1[1] + CAMA1[3])]
    p.mpoly(ruta_goteo_e, stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(8.56, 3.4, "SV-3 goteo camas 1–2 (HA, 12 V NC)", size=8.5, fill=BLUE, rotate=-90)
    ruta_goteo_s = [(TOMA[0], 6.22), (CAMA3[0] + CAMA3[2] + 0.15, 6.22), (CAMA3[0] + CAMA3[2] + 0.15, CAMA3[1] + 0.4), (CAMA3[0] + CAMA3[2], CAMA3[1] + 0.4)]
    p.mpoly(ruta_goteo_s, stroke=BLUE, sw=1.5, dash=DASH, marker="arrBlue")
    p.mtext(5.0, 6.16, f"goteo cama 3 ≈ {fmt(dist(ruta_goteo_s))} m: aéreo por el borde del cobertizo; el cruce del paso puerta→túnel va en canaleta con tapa", size=8.5, fill=BLUE, anchor="middle")
    # gantry sobre cama 3
    x, y, w, h = CAMA3
    for yy_ in (y - 0.06, y + h + 0.06):
        p.mline(x, yy_, x + w, yy_, stroke=INK, sw=2.5)
    gxp = x + 1.9
    p.mrect(gxp - 0.05, y - 0.12, 0.1, h + 0.24, fill=INK, stroke=INK, sw=1)
    p.mcircle(gxp, y + h / 2 + 0.15, 0.08, fill=WHITE, stroke=INK, sw=1.5)
    p.mline(x + 0.3, y - 0.2, x + w - 0.3, y - 0.2, stroke=INK, sw=1, marker="arrInk")
    p.mline(x + w - 0.3, y - 0.2, x + 0.3, y - 0.2, stroke=INK, sw=1, marker="arrInk")
    p.mtext(x + w / 2, y - 0.26, "gantry XY tipo FarmBot: rieles V-slot en los bordes largos · puente Y · NEMA17 · GRBL/Klipper · carrera ≈ 3.3 × 0.8 m", size=9)
    p.mtext(x + w / 2, y - 0.26, "", size=9)
    # controlador del gantry
    p.gabinete(4.05, 6.55, 0.25, 0.25, ["GAB-3: driver gantry", "+ cámara (IP65)"], anchor_side="below")
    p.mline(GABDC[0], GABDC[1] + 0.15, 4.3, 6.68, stroke=AMBER, sw=1.4, dash=DASH, marker="arrAmber")
    # camara fija de vision sobre poste
    p.mcircle(4.15, 6.25, 0.07, fill=AMBER, stroke=AMBER)
    p.mpoly([(4.15, 6.25), (2.2, 6.55), (2.2, 7.5)], stroke=AMBER, sw=0.8, dash=DOT, fill="#fff7ed", close=True)
    p.mtext(4.3, 6.22, "cámara fija (poste 2 m): cobertura foliar + plagas", size=8.5, fill=AMBER)
    # composta -> camas
    p.mline(COMPOSTA[0] + 0.3, COMPOSTA[1] - 0.2, CAMA3[0] + 0.3, CAMA3[1] + CAMA3[3], stroke=GREEN, sw=1.2, dash=DOT, marker="arrGreen")
    # cotas
    p.dim_h(tx + tw, CAMA1[0], 6.0, "0.65", size=9)
    p.dim_h(CAMA1[0] + CAMA1[2], CAMA2[0], 6.0, "0.55", size=9)
    p.dim_v(ty + th, CAMA3[1], 0.25, "0.70", size=9)
    p.dim_v(CAMA1[1], CAMA1[1] + CAMA1[3], 7.05, "3.90", size=9)
    total = sum(areas)
    yy = p.leyenda(1130, 92)
    p.lines(1130, yy + 14, [
        "QUÉ CAMBIA VS. FASE 2",
        f"· 3 camas elevadas: {fmt(areas[0])} + {fmt(areas[1])} + {fmt(areas[2])} = {fmt(total)} m²",
        "  (es lo que cabe sin perder pasillos ≥ 0.55 m).",
        "  Meta 15–20 m²: ver cómo llegar en layout-patio.md §5.",
        "· Goteo de camas colgado de HA: SV-3 desde el tinaco",
        "  (12 V NC), una derivación por cama, timer + humedad.",
        "· Gantry XY tipo FarmBot sobre la cama 3 (la más larga",
        "  y la más cerca del cobertizo/GAB-DC): rieles V-slot,",
        "  puente Y, NEMA17, GRBL/Klipper; GAB-3 con driver.",
        "· Cámara fija en poste de 2 m: cobertura foliar, plagas.",
        "· La composta del tambo alimenta las camas (07 §12).",
        "· Nada de esto es el negocio: sólo si F1–F2 se pagan.",
        "",
        "REGLA DE ORO F3",
        "· Ningún cable ni manguera nueva cruza pasillos al piso:",
        "  todo aéreo (2 m) o pegado a barda/cama.",
    ], size=10.5, lh=15)
    p.notas(90, 1027, [
        "SUPUESTO: patio 10 × 8 m, casa al SUR, acceso NORTE, coladera NE. Las camas van pegadas a la barda este (0.15 m) y se atienden por un solo lado: por eso miden ≤ 1.0 m de ancho. Cama 3 deja libre la puerta casa→patio y 0.7 m de paso frente al túnel.",
        "[POR VERIFICAR] altura y material de cama (0.7–0.9 m: madera tratada/PTR + geomembrana), perfil V-slot y carrera del gantry, caudal de goteo por cama: no están en la fuente de verdad; el plan maestro sólo fija 'camas elevadas con goteo colgado de HA' y 'gantry XY V-slot + NEMA17 + GRBL/Klipper'.",
        "Fuentes: referencia/00-plan-maestro §Fase 3 · referencia/07 §12 y §14 · research/hidroponia-nft (periférica sólo para riego presurizado de camas) · layout de Fases 1–2.",
    ], size=10.5, lh=15)
    return p


# ----------------------------------------------------------------------------- alzado del rack
K = 4.0  # px por cm (1:10)

RACK_H, RACK_W, RACK_D = 183.0, 91.4, 45.7   # cm (Husky 5 niveles, Home Depot $2,019)
SHELF_T = 2.5                                # espesor del entrepaño (MDF laminado) [POR VERIFICAR]
SHELF_TOPS = (10.0, 53.0, 96.0, 139.0, 182.0)  # cara superior de N1..N5 desde el piso (ajustables)
TRAY_W, TRAY_L, TRAY_H = 25.4, 50.8, 6.0     # charola 1020 (doble: perforada dentro de lisa)
TUBE_L, TUBE_D = 120.0, 2.6                  # T8 18 W 120 cm
CANOPY = {1: 8.0, 2: 8.0, 3: 5.0, 4: 2.0}    # altura del dosel dibujada por nivel (cm)


def rack_alzado():
    W, H = 1500, 1030
    s = SVG(W, H, "Alzado · Rack Husky 183×91×46 cm · 5 niveles · escala 1:10",
            "charolas 10×20 (25.4×50.8 cm) · 3 por nivel · T8 18 W ×2 por nivel · nebulizadores N1–N4 · zona blackout arriba (N5) · v1")
    floor = 930.0

    def yc(cm):  # cm sobre el piso -> px
        return floor - cm * K

    # ---------------- vista frontal
    x0 = 130.0
    wpx = RACK_W * K
    s.text(x0, 86, "VISTA FRONTAL (desde el pasillo)", size=12, weight="bold")
    s.line(x0 - 80, floor, x0 + wpx + 120, floor, sw=2)
    s.text(x0 - 80, floor + 16, "piso nivelado (calzar patas: charola desnivelada = encharcamiento = moho)", size=10, fill=GRAY)
    # charola colectora en el piso
    s.rect(x0 - 6, floor - 4 * K, wpx + 12, 4 * K, fill="#eff6ff", stroke=BLUE, sw=1.2)
    s.text(x0 + wpx + 16, floor - 4, "charola colectora → manguera → coladera", size=10, fill=BLUE)
    # postes
    for px in (x0, x0 + wpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    # entrepaños y niveles
    gap = (RACK_W - 3 * TRAY_W) / 4
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x0, yc(top), wpx, SHELF_T * K, fill="#d1d5db", stroke=INK, sw=1.5)
        s.text(x0 - 12, yc(top) + 4, f"N{i}", size=12, weight="bold", anchor="end")
        if i <= 4:
            # 3 charolas dobles + dosel
            for k in range(3):
                tx = x0 + (gap + k * (TRAY_W + gap)) * K
                s.rect(tx, yc(top + TRAY_H), TRAY_W * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.4)
                s.rect(tx + 1.0 * K, yc(top + TRAY_H - 0.6), (TRAY_W - 2.0) * K, (TRAY_H - 1.6) * K, fill="#f1f8e9", stroke=GREEN, sw=0.8)
                c = CANOPY[i]
                s.rect(tx + 0.8 * K, yc(top + TRAY_H + c), (TRAY_W - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
            # sensor capacitivo en la charola izquierda
            tx = x0 + gap * K
            s.line(tx + 4 * K, yc(top + TRAY_H + 6), tx + 4 * K, yc(top + 1), stroke=AMBER, sw=2.5)
            s.text(tx + 5 * K, yc(top + TRAY_H + 5), f"MT-{i}", size=8.5, fill=AMBER)
            # tubos T8 bajo el entrepaño superior (uno tras otro: se ve uno)
            nxt = SHELF_TOPS[i] - SHELF_T
            ty = yc(nxt - 3.0)
            tl = x0 + wpx / 2 - TUBE_L * K / 2
            s.rect(tl, ty, TUBE_L * K, TUBE_D * K, fill="#fef3c7", stroke=AMBER, sw=1.4, rx=5)
            # nebulizadores: linea bajo los tubos, 2 boquillas
            ny = ty + TUBE_D * K + 2.0 * K
            s.line(x0, ny, x0 + wpx, ny, stroke=BLUE, sw=1.6)
            for q in (0.25, 0.75):
                bx = x0 + wpx * q
                s.polyline([(bx - 4, ny), (bx + 4, ny), (bx, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
                for dx in (-10, 0, 10):
                    s.line(bx, ny + 10, bx + dx, ny + 22, stroke=BLUE, sw=0.7, dash="2 2")
        else:
            # N5 blackout: charolas apiladas con peso bajo cubierta opaca
            free = RACK_H - top
            for k in range(3):
                tx = x0 + (gap + k * (TRAY_W + gap)) * K
                for st in range(2):
                    s.rect(tx, yc(top + TRAY_H * (st + 1)), TRAY_W * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
                s.rect(tx + 6 * K, yc(top + 2 * TRAY_H + 5), 13 * K, 5 * K, fill="#9ca3af", stroke=INK, sw=1)
                s.text(tx + 12.5 * K, yc(top + 2 * TRAY_H + 1.5), "peso 2–4 kg", size=8, anchor="middle", fill=WHITE)
    # cubierta opaca N5 (sobre el rack; el entrepaño N5 esta a 182 cm)
    s.rect(x0 - 6, yc(SHELF_TOPS[4] + 22), wpx + 12, 22 * K, fill="#374151", stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    s.text(x0 + wpx / 2, yc(SHELF_TOPS[4] + 24), "N5 = ZONA BLACKOUT: cubierta opaca (tela/plástico negro), charolas apiladas con peso, 2–4 d, atomizar a mano 1–2×/día", size=10, anchor="middle", weight="bold")
    # sensor ambiente
    s.circle(x0 + wpx + 6, yc(95), 5, fill=AMBER, stroke=AMBER)
    s.text(x0 + wpx + 14, yc(95) + 4, "SHT31 T/HR (poste, 1.0 m)", size=9, fill=AMBER)
    # cotas frontales
    dx = x0 - 60
    s.line(dx, yc(0), dx, yc(RACK_H), sw=1)
    for cm in (0, RACK_H):
        s.line(dx - 5, yc(cm), dx + 5, yc(cm), sw=1)
    s.text(dx - 8, yc(RACK_H / 2), "183 cm", size=11, anchor="middle", rotate=-90)
    dx2 = x0 - 36
    s.line(dx2, yc(SHELF_TOPS[1]), dx2, yc(SHELF_TOPS[2]), sw=1)
    s.line(dx2 - 5, yc(SHELF_TOPS[1]), dx2 + 5, yc(SHELF_TOPS[1]), sw=1)
    s.line(dx2 - 5, yc(SHELF_TOPS[2]), dx2 + 5, yc(SHELF_TOPS[2]), sw=1)
    s.text(dx2 - 6, yc((SHELF_TOPS[1] + SHELF_TOPS[2]) / 2), "43 (≥ 30 ✓)", size=9.5, anchor="middle", rotate=-90)
    by = floor + 34
    s.line(x0, by, x0 + wpx, by, sw=1)
    s.line(x0, by - 5, x0, by + 5, sw=1); s.line(x0 + wpx, by - 5, x0 + wpx, by + 5, sw=1)
    s.text(x0 + wpx / 2, by - 4, "91.4 cm", size=11, anchor="middle")
    tl = x0 + wpx / 2 - TUBE_L * K / 2
    by2 = floor + 56
    s.line(tl, by2, tl + TUBE_L * K, by2, stroke=AMBER, sw=1)
    s.line(tl, by2 - 5, tl, by2 + 5, stroke=AMBER, sw=1); s.line(tl + TUBE_L * K, by2 - 5, tl + TUBE_L * K, by2 + 5, stroke=AMBER, sw=1)
    s.text(x0 + wpx / 2, by2 - 4, "T8 120 cm (vuela 14.3 cm por lado → racks separados ≥ 0.3 m)", size=10, fill=AMBER, anchor="middle")
    # distancia luz-dosel (nivel N3)
    top3 = SHELF_TOPS[2]
    tube_bottom = SHELF_TOPS[3] - SHELF_T - 3.0 - TUBE_D
    canopy_top = top3 + TRAY_H + CANOPY[3]
    xr = x0 - 36
    s.line(xr, yc(tube_bottom), xr, yc(canopy_top), stroke=AMBER, sw=1)
    s.line(xr - 5, yc(tube_bottom), xr + 5, yc(tube_bottom), stroke=AMBER, sw=1)
    s.line(xr - 5, yc(canopy_top), xr + 5, yc(canopy_top), stroke=AMBER, sw=1)
    s.text(xr - 6, yc((tube_bottom + canopy_top) / 2), f"luz→dosel {fmt(tube_bottom - canopy_top)} (meta 15–20)", size=9, fill=AMBER, anchor="middle", rotate=-90)
    # flujo de charolas (derecha de la vista frontal)
    fx = x0 + wpx + 70
    flow = {5: ["SIEMBRA → N5 oscuridad: apiladas", "con peso 2–4 kg, 2–4 d (arriba = cálido)"],
            4: ["DESTAPE día 3–5 → N4: luz indirecta", "+ T8 12–14 h; riego SOLO por abajo"],
            3: ["N3 desarrollo (día 5–8)"],
            2: ["N2 acabado (día 8–10)"],
            1: ["N1 pre-cosecha (más fresco: frena el", "estiramiento) → COSECHA día 8–12"]}
    for i, top in enumerate(SHELF_TOPS, 1):
        s.lines(fx, yc(top + 20), flow[i], size=9.5, fill=GREEN, lh=12)
        if i > 1:
            s.line(fx + 6, yc(top + 16), fx + 6, yc(SHELF_TOPS[i - 2] + 26), stroke=GREEN, sw=1.2, marker="arrGreen", dash="3 3")

    # ---------------- vista lateral
    x1 = 830.0
    dpx = RACK_D * K
    s.text(x1, 86, "VISTA LATERAL", size=12, weight="bold")
    s.line(x1 - 30, floor, x1 + dpx + 60, floor, sw=2)
    for px in (x1, x1 + dpx - 3.5 * K):
        s.rect(px, yc(RACK_H), 3.5 * K, RACK_H * K, fill=LIGHT, stroke=INK, sw=1.5)
    # manifold vertical de nebulizadores por la parte trasera (izquierda)
    s.line(x1 - 10, yc(SHELF_TOPS[0]), x1 - 10, yc(SHELF_TOPS[4] - SHELF_T - 6), stroke=BLUE, sw=2)
    s.text(x1 - 16, yc(60), "manifold nebulizadores (½ pulg) desde P-1", size=9, fill=BLUE, anchor="middle", rotate=-90)
    for i, top in enumerate(SHELF_TOPS, 1):
        s.rect(x1, yc(top), dpx, SHELF_T * K, fill="#d1d5db", stroke=INK, sw=1.5)
        if i <= 4:
            # charola atravesada: 50.8 cm sobre 45.7 de fondo -> vuela 5.1 al frente (derecha)
            s.rect(x1, yc(top + TRAY_H), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.4)
            c = CANOPY[i]
            s.rect(x1 + 0.8 * K, yc(top + TRAY_H + c), (TRAY_L - 1.6) * K, c * K, fill="url(#hatchGreen)", stroke=GREEN, sw=0.8)
            nxt = SHELF_TOPS[i] - SHELF_T
            for q in (0.25, 0.75):
                s.circle(x1 + dpx * q, yc(nxt - 3.0 - TUBE_D / 2), TUBE_D * K / 2, fill="#fef3c7", stroke=AMBER, sw=1.4)
            ny = yc(nxt - 3.0 - TUBE_D - 2.0)
            s.line(x1 - 10, ny, x1 + dpx * 0.5, ny, stroke=BLUE, sw=1.6)
            s.polyline([(x1 + dpx * 0.5 - 4, ny), (x1 + dpx * 0.5 + 4, ny), (x1 + dpx * 0.5, ny + 9)], fill=BLUE, stroke=BLUE, sw=1, close=True)
        else:
            for st in range(2):
                s.rect(x1, yc(top + TRAY_H * (st + 1)), TRAY_L * K, TRAY_H * K, fill=WHITE, stroke=GREEN, sw=1.2)
            s.rect(x1 + 12 * K, yc(top + 2 * TRAY_H + 5), 26 * K, 5 * K, fill="#9ca3af", stroke=INK, sw=1)
    s.rect(x1 - 6, yc(SHELF_TOPS[4] + 22), dpx + 32, 22 * K, fill="#374151", stroke=INK, sw=1.2, dash=DASH, opacity=0.18)
    # cotas laterales
    by = floor + 34
    s.line(x1, by, x1 + dpx, by, sw=1); s.line(x1, by - 5, x1, by + 5, sw=1); s.line(x1 + dpx, by - 5, x1 + dpx, by + 5, sw=1)
    s.text(x1 + dpx / 2, by - 4, "45.7 cm", size=11, anchor="middle")
    by2 = floor + 56
    s.line(x1, by2, x1 + TRAY_L * K, by2, stroke=GREEN, sw=1); s.line(x1 + TRAY_L * K, by2 - 5, x1 + TRAY_L * K, by2 + 5, stroke=GREEN, sw=1); s.line(x1, by2 - 5, x1, by2 + 5, stroke=GREEN, sw=1)
    s.text(x1 + TRAY_L * K / 2, by2 - 4, "charola 50.8 cm (vuela 5.1 al frente)", size=10, fill=GREEN, anchor="middle")
    s.text(x1 + dpx / 2, floor + 78, "◄ atrás (pared, manifold)   ·   frente (pasillo) ►", size=9, fill=GRAY, anchor="middle")

    # ---------------- planta de un nivel
    x2, y2 = 1100.0, 118.0
    s.text(x2, 86, "PLANTA DE UN NIVEL (N1–N4)", size=12, weight="bold")
    s.rect(x2, y2, wpx, dpx, fill="#d1d5db", stroke=INK, sw=1.5)
    for k in range(3):
        tx = x2 + (gap + k * (TRAY_W + gap)) * K
        s.rect(tx, y2, TRAY_W * K, TRAY_L * K, fill="#f1f8e9", stroke=GREEN, sw=1.4)
        s.text(tx + TRAY_W * K / 2, y2 + TRAY_L * K / 2 + 4, f"{k+1}", size=11, fill=GREEN, anchor="middle", weight="bold")
    for q in (0.25, 0.75):
        s.line(x2 + wpx / 2 - TUBE_L * K / 2, y2 + dpx * q, x2 + wpx / 2 + TUBE_L * K / 2, y2 + dpx * q, stroke=AMBER, sw=3, dash="8 4")
    s.line(x2, y2 + 6, x2 + wpx, y2 + 6, stroke=BLUE, sw=1.6)
    for q in (0.25, 0.75):
        s.circle(x2 + wpx * q, y2 + 6, 4, fill=BLUE, stroke=BLUE)
    s.text(x2 + wpx / 2, y2 - 6, "atrás: línea de nebulizadores (2 boquillas)", size=9, fill=BLUE, anchor="middle")
    s.text(x2 + wpx / 2, y2 + TRAY_L * K + 14, "frente: volado 5.1 cm", size=9, fill=GREEN, anchor="middle")
    s.text(x2 + wpx + 8, y2 + dpx * 0.25 + 4, "T8 ×2", size=9, fill=AMBER)
    by = y2 + TRAY_L * K + 32
    s.line(x2, by, x2 + wpx, by, sw=1); s.line(x2, by - 5, x2, by + 5, sw=1); s.line(x2 + wpx, by - 5, x2 + wpx, by + 5, sw=1)
    s.text(x2 + wpx / 2, by - 4, "91.4 = 3 × 25.4 + 4 × 3.8", size=10, anchor="middle")

    # ---------------- tablas
    tx0, ty0 = 1100.0, 380.0
    rows = [
        ("CAPACIDAD (geometría, no la cifra de la investigación)", "bold"),
        ("· Entrepaño 91.4 × 45.7 cm; charola 1020 = 25.4 × 50.8 cm.", ""),
        ("· Caben 3 atravesadas por nivel (76.2 de 91.4 cm; vuelan 5.1 cm", ""),
        ("  al frente). El '8–10/nivel' de research/estructura-invernadero", ""),
        ("  NO cabe: pide ~1.0 m² por nivel. [POR VERIFICAR con el rack armado]", ""),
        ("· En luz (N1–N4): 12 posiciones/rack. N5 blackout: 3 pilas × 2–3", ""),
        ("  charolas = 6–9. Total ≈ 18–21 charolas en proceso por rack.", ""),
        ("· 3 racks (Fase 1) ≈ 36 en luz + 18–27 en oscuridad → 25–35", ""),
        ("  charolas/semana con ciclo de 8–12 d. Sí cierra la meta del plan.", ""),
        ("", ""),
        ("CARGAS", "bold"),
        ("· Charola doble con coco saturado: 2.5–4 kg → 3 × 4 = 12 kg/nivel", ""),
        ("  (+ peso 2–4 kg por pila en N5 → ≤ 30 kg). Rack: 362.9 kg/repisa.", ""),
        ("· Rack cargado ≈ 60–90 kg + peso propio [POR VERIFICAR en caja].", ""),
        ("· Forrar entrepaños de MDF con plástico o charola de drenaje.", ""),
        ("", ""),
        ("ILUMINACIÓN", "bold"),
        ("· 2 × T8 LED 18 W 6500 K 1,400 lm por nivel N1–N4 = 8 tubos/rack", ""),
        ("  ($121 c/u JWJ = $968; bom/fase1 cubre UN rack: 3 racks = 24).", ""),
        ("· 12–14 h/día por relé de GAB-1: 8 × 18 W × 13 h ≈ 1.9 kWh/día.", ""),
        ("· Tubo a 3 cm bajo el entrepaño; luz→dosel 20–27 cm con paso de", ""),
        ("  43 cm (meta 15–20 cm: bajar 1 posición el entrepaño de arriba).", ""),
        ("", ""),
        ("RIEGO", "bold"),
        ("· Nebulizadores N1–N4 (2 boquillas/nivel) desde P-1 12 V; N5 a mano.", ""),
        ("· Tras el destape: riego SOLO por abajo (perforada dentro de lisa).", ""),
        ("· MT-1…4 capacitivo en la charola testigo de cada nivel; SHT31 en poste.", ""),
    ]
    yy = ty0
    for txt, w in rows:
        if txt:
            s.text(tx0, yy, txt, size=10.5, weight=("bold" if w else "normal"))
        yy += 15
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
    jobs = {
        "patio-fase-0.svg": fase0,
        "patio-fase-1.svg": fase1,
        "patio-fase-2.svg": fase2,
        "patio-fase-3.svg": fase3,
        "rack-alzado.svg": rack_alzado,
    }
    bad = 0
    for name, fn in jobs.items():
        path = out / name
        fn().save(path)
        ok, size = validar(path)
        flag = "ok" if ok and size > 4096 else "REVISAR"
        print(f"{flag:8s} {path.relative_to(root) if path.is_relative_to(root) else path}  {size/1024:.1f} KB")
        bad += 0 if ok and size > 4096 else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
