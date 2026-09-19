#!/usr/bin/env python3
"""pid.py — genera los P&ID hidráulicos de HomeGreen como SVG escrito a mano.

Solo biblioteca estándar (Python 3.11). Sin fuentes externas ni scripts en el SVG.

Uso:
    python3 hardware/hidraulico/pid.py           # escribe los 3 SVG en docs/assets/diagramas/hidraulico/
    python3 hardware/hidraulico/pid.py --check   # además valida XML (minidom) y tamaño > 4 KB
    python3 hardware/hidraulico/pid.py --out DIR # otra carpeta de salida

Diagramas (manifiesto CONVENCIONES §3):
    riego-microgreens.svg   tinaco 750 L → válvula → filtro sedimentos → bomba diafragma 12 V →
                            manifold → nebulizadores por nivel; JSN-SR04T; DS18B20; retorno a coladera
    nft-recirculacion.svg   tambo 200 L → bomba 12 V → filtro malla 120 → manifold con válvulas →
                            8 líneas PVC 4" pendiente 2–3 % → retorno 2" → tambo; pH/EC en retorno;
                            peristálticas A/B/pH−; solenoide de llenado vía dúplex; YF-S201
    captacion-pluvial.svg   techo túnel → canalón 0.5–1 % → filtro de hojas → tlaloque → tinaco
                            (rebosadero a coladera); flotador de red SACMEX

Símbolos ISA simplificados: tanque, bomba (círculo con triángulo), filtro, válvula de mariposa,
válvula solenoide, válvula de flotador, sensor (círculo con etiqueta pH/EC/T/L/F/M), tubería con
flechas de dirección, canaleta, nebulizador, coladera.

Estilo: fondo blanco, trazos #1f2937, acento #2e7d32 (verde), #b45309 (ámbar) para alertas,
texto sans 12–14 px, título arriba a la izquierda, leyenda, "v1 · 2026-09".

Todo número anotado sale de docs/referencia/03-instalacion.md, docs/research/hidroponia-nft.md,
docs/research/agua-captacion.md, docs/research/instalacion-tunel-detalle.md §4,
docs/research/electrico-respaldo-seguridad.md y bom/*.csv.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from xml.dom import minidom

# ---------------------------------------------------------------------------
# Paleta y tipografía (manifiesto §3)
# ---------------------------------------------------------------------------
INK = "#1f2937"
GREEN = "#2e7d32"
AMBER = "#b45309"
GRAY = "#6b7280"
LIGHT = "#f3f4f6"
WHITE = "#ffffff"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"
# Factor global de tipografía: escala TODO el texto y los interlineados/altos de
# fila que dependen de él. El ANCHO del lienzo es fijo (es lo que fija el tamaño
# real en pantalla: px = size * FS * 980 / ancho_viewBox); el ALTO lo calcula
# cada diagrama al final, así la letra puede crecer sin que nada se salga.
FS = 1.38
VERSION = "v1 · 2026-09"

# Anchos de Helvetica (AFM, unidades/1000) para poder MEDIR el texto antes de
# dibujarlo: sin esto las cajas de notas y de leyenda se desbordan al subir FS.
_HW = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191,
    "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278,
    "0": 556, "1": 556, "2": 556, "3": 556, "4": 556, "5": 556, "6": 556, "7": 556,
    "8": 556, "9": 556, ":": 278, ";": 278, "<": 584, "=": 584, ">": 584, "?": 556,
    "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333,
    "{": 334, "|": 260, "}": 334, "~": 584,
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722,
    "I": 278, "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944, "X": 667,
    "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556,
    "i": 222, "j": 222, "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556,
    "q": 556, "r": 333, "s": 500, "t": 278, "u": 556, "v": 500, "w": 722, "x": 500,
    "y": 500, "z": 500,
    "¡": 333, "¿": 611, "°": 400, "·": 278, "±": 584,
    "×": 584, "÷": 584, "«": 556, "»": 556, "º": 365,
    "–": 556, "—": 1000, "‘": 222, "’": 222, "“": 333,
    "”": 333, "•": 350, "…": 1000, "→": 1000, "←": 1000,
    "⇒": 1000, "≈": 549, "≠": 549, "≤": 549, "≥": 549,
    "µ": 556, "Ω": 768, "²": 333, "³": 333, "₂": 400,
    "₄": 400, "á": 556, "é": 556, "í": 278, "ó": 556,
    "ú": 556, "ü": 556, "ñ": 556, "Á": 667, "É": 667,
    "Í": 278, "Ó": 778, "Ú": 722, "Ñ": 722, " ": 278,
}


def text_w(s: str, size: float) -> float:
    """Ancho en unidades SVG del texto `s` compuesto en Helvetica a `size`."""
    return sum(_HW.get(c, 556) for c in str(s)) * size / 1000.0


def esc(s: str) -> str:
    """Escapa texto para XML."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt(v: float) -> str:
    """Números compactos para atributos SVG."""
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


# ---------------------------------------------------------------------------
# Hoja SVG con símbolos
# ---------------------------------------------------------------------------
class Sheet:
    """Acumula fragmentos SVG y ofrece símbolos P&ID simplificados."""

    def __init__(self, width: int, height: int, title: str, subtitle: str, fs: float = FS):
        self.w = width
        self.h = height
        self.fs = fs   # factor tipográfico de ESTA hoja
        self.title = title
        self.subtitle = subtitle
        self.parts: list[str] = []

    # -- medición ------------------------------------------------------------
    def tw(self, s: str, size: float) -> float:
        """Ancho real que ocupará `s` dibujado a `size` con el FS de esta hoja."""
        return text_w(s, size * self.fs)

    def wrap(self, lines, width: float, size: float) -> list[str]:
        """Parte en varias las líneas que no caben en `width` unidades SVG."""
        out: list[str] = []
        for ln in lines:
            if self.tw(ln, size) <= width:
                out.append(ln)
                continue
            cur = ""
            for word in str(ln).split(" "):
                cand = f"{cur} {word}".strip()
                if cur and self.tw(cand, size) > width:
                    out.append(cur)
                    cur = word
                else:
                    cur = cand
            if cur:
                out.append(cur)
        return out

    # -- primitivas ----------------------------------------------------------
    def add(self, s: str) -> None:
        self.parts.append(s)

    def text(self, x, y, s, size=12, anchor="start", weight="normal", fill=INK,
             rotate=None, italic=False) -> None:
        tr = f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"' if rotate is not None else ""
        st = ' font-style="italic"' if italic else ""
        self.add(
            f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{FONT}" font-size="{fmt(size * self.fs)}" '
            f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{tr}>{esc(s)}</text>'
        )

    def multiline(self, x, y, lines, size=12, lh=None, anchor="start", fill=INK,
                  weight="normal") -> float:
        """Varias líneas de texto; devuelve la y siguiente."""
        lh = (lh or size + 4) * self.fs
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size=size, anchor=anchor, fill=fill, weight=weight)
        return y + len(lines) * lh

    def line(self, x1, y1, x2, y2, stroke=INK, width=1.5, dash=None, cap="round") -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="{cap}"{d}/>'
        )

    def rect(self, x, y, w, h, fill=WHITE, stroke=INK, width=1.5, rx=0, dash=None,
             opacity=None) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' fill-opacity="{opacity}"' if opacity is not None else ""
        self.add(
            f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}{op}/>'
        )

    def circle(self, cx, cy, r, fill=WHITE, stroke=INK, width=1.5) -> None:
        self.add(
            f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{width}"/>'
        )

    def polygon(self, pts, fill=WHITE, stroke=INK, width=1.5) -> None:
        p = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
        self.add(
            f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linejoin="round"/>'
        )

    def path(self, d, fill="none", stroke=INK, width=1.5, dash=None) -> None:
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}/>'
        )

    # -- tuberías y señales -------------------------------------------------
    def _arrow(self, x1, y1, x2, y2, color=INK, size=6) -> None:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        pts = [
            (mx + ux * size, my + uy * size),
            (mx - ux * size + px * size * 0.75, my - uy * size + py * size * 0.75),
            (mx - ux * size - px * size * 0.75, my - uy * size - py * size * 0.75),
        ]
        self.polygon(pts, fill=color, stroke=color, width=1)

    def pipe(self, pts, width=2.5, stroke=INK, arrows=True, dash=None, min_seg=36) -> None:
        """Polilínea de tubería con flecha a la mitad de cada tramo largo.

        arrows: True → todos los tramos ≥ min_seg; int → solo ese índice de tramo;
        lista → esos índices; False → sin flechas.
        """
        p = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d}/>'
        )
        if arrows is False:
            return
        idx = range(len(pts) - 1)
        if isinstance(arrows, int) and not isinstance(arrows, bool):
            idx = [arrows]
        elif isinstance(arrows, (list, tuple)):
            idx = arrows
        for i in idx:
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            if math.hypot(x2 - x1, y2 - y1) >= min_seg:
                self._arrow(x1, y1, x2, y2, color=stroke)

    def signal(self, pts, stroke=GRAY) -> None:
        """Señal eléctrica/instrumento: línea punteada fina."""
        self.pipe(pts, width=1.2, stroke=stroke, arrows=False, dash="4 3")

    def water(self, pts, arrows=True) -> None:
        """Flujo de agua (acento verde)."""
        self.pipe(pts, width=2.5, stroke=GREEN, arrows=arrows)

    # -- símbolos ISA simplificados ---------------------------------------------
    def tank(self, x, y, w, h, tag, lines=(), level=0.65, open_top=False,
             label_dy=16) -> float:
        """Tanque: rectángulo con nivel de agua. Devuelve la y bajo su rótulo."""
        r = min(18, w / 4)
        # nivel de agua
        lv = y + h - level * (h - 6)
        self.add(
            f'<path d="M{fmt(x)},{fmt(lv)} L{fmt(x)},{fmt(y + h - r)} '
            f'Q{fmt(x)},{fmt(y + h)} {fmt(x + r)},{fmt(y + h)} L{fmt(x + w - r)},{fmt(y + h)} '
            f'Q{fmt(x + w)},{fmt(y + h)} {fmt(x + w)},{fmt(y + h - r)} L{fmt(x + w)},{fmt(lv)} Z" '
            f'fill="{GREEN}" fill-opacity="0.16" stroke="none"/>'
        )
        self.line(x, lv, x + w, lv, stroke=GREEN, width=1.2, dash="5 3")
        top = "" if open_top else f"L{fmt(x + w)},{fmt(y)} L{fmt(x)},{fmt(y)} Z"
        d = (
            f"M{fmt(x)},{fmt(y)} L{fmt(x)},{fmt(y + h - r)} Q{fmt(x)},{fmt(y + h)} {fmt(x + r)},{fmt(y + h)} "
            f"L{fmt(x + w - r)},{fmt(y + h)} Q{fmt(x + w)},{fmt(y + h)} {fmt(x + w)},{fmt(y + h - r)} "
            f"L{fmt(x + w)},{fmt(y)} {top}"
        )
        self.path(d, width=2)
        self.text(x + w / 2, y + h + label_dy, tag, size=13, anchor="middle", weight="bold")
        return self.multiline(x + w / 2, y + h + label_dy + 16, lines, size=11, anchor="middle",
                              fill=GRAY)

    def pump(self, cx, cy, tag, lines=(), r=17, direction="right", label="below") -> None:
        """Bomba: círculo con triángulo apuntando en la dirección del flujo."""
        self.circle(cx, cy, r, width=2)
        ang = {"right": 0, "left": 180, "up": -90, "down": 90}[direction]
        a = math.radians(ang)
        tri = []
        for k in (0, 130, 230):
            b = a + math.radians(k)
            rr = r * 0.78 if k == 0 else r * 0.62
            tri.append((cx + rr * math.cos(b), cy + rr * math.sin(b)))
        self.polygon(tri, fill=INK, stroke=INK, width=1)
        self._label(cx, cy, r, tag, lines, label)

    def filter_(self, cx, cy, tag, lines=(), w=44, h=30, label="below") -> None:
        """Filtro: rectángulo con malla (zigzag) interior."""
        self.rect(cx - w / 2, cy - h / 2, w, h, width=2)
        step = 6
        d = f"M{fmt(cx - w / 2 + 4)},{fmt(cy + h / 4)} "
        up = True
        xx = cx - w / 2 + 4
        while xx + step <= cx + w / 2 - 4:
            xx += step
            d += f"L{fmt(xx)},{fmt(cy - h / 4 if up else cy + h / 4)} "
            up = not up
        self.path(d, width=1.3)
        self._label(cx, cy, h / 2, tag, lines, label)

    def valve(self, cx, cy, tag=None, lines=(), orient="h", size=11, label="below",
              butterfly=True) -> None:
        """Válvula de mariposa: moño (dos triángulos) + disco perpendicular."""
        s = size
        if orient == "h":
            self.polygon([(cx - s, cy - s * 0.7), (cx, cy), (cx - s, cy + s * 0.7)], width=1.6)
            self.polygon([(cx + s, cy - s * 0.7), (cx, cy), (cx + s, cy + s * 0.7)], width=1.6)
            if butterfly:
                self.line(cx, cy - s * 0.9, cx, cy + s * 0.9, width=2.2)
                self.circle(cx, cy, 2.2, fill=INK)
        else:
            self.polygon([(cx - s * 0.7, cy - s), (cx, cy), (cx + s * 0.7, cy - s)], width=1.6)
            self.polygon([(cx - s * 0.7, cy + s), (cx, cy), (cx + s * 0.7, cy + s)], width=1.6)
            if butterfly:
                self.line(cx - s * 0.9, cy, cx + s * 0.9, cy, width=2.2)
                self.circle(cx, cy, 2.2, fill=INK)
        if tag:
            self._label(cx, cy, s, tag, lines, label)

    def solenoid(self, cx, cy, tag, lines=(), orient="h", label="below") -> None:
        """Válvula solenoide NC: moño + vástago + caja con 'S'."""
        s = 11
        self.valve(cx, cy, orient=orient, size=s, butterfly=False)
        if orient == "h":
            self.line(cx, cy, cx, cy - s - 8, width=1.6)
            self.rect(cx - 9, cy - s - 24, 18, 16, width=1.6)
            self.text(cx, cy - s - 12, "S", size=11, anchor="middle", weight="bold")
        else:
            self.line(cx, cy, cx + s + 8, cy, width=1.6)
            self.rect(cx + s + 8, cy - 8, 18, 16, width=1.6)
            self.text(cx + s + 17, cy + 4, "S", size=11, anchor="middle", weight="bold")
        self._label(cx, cy, s + (0 if orient == "v" else 0), tag, lines, label)

    def float_valve(self, cx, cy, tag, lines=(), label="below", mirror=False) -> None:
        """Válvula de flotador (llenado desde red): moño + brazo + bola.

        mirror=True dibuja el brazo hacia la izquierda (válvula en la pared derecha del tanque).
        """
        s = 10
        d = -1 if mirror else 1
        self.valve(cx, cy, orient="h", size=s, butterfly=False)
        self.line(cx, cy, cx, cy + 14, width=1.6)
        self.line(cx, cy + 14, cx + d * 26, cy + 26, width=1.6)
        self.circle(cx + d * 32, cy + 29, 7, fill=LIGHT, width=1.6)
        if tag:
            self._label(cx, cy, s, tag, lines, label)

    def jump(self, x, y, r=6, width=2.5) -> None:
        """Salto de tubería vertical sobre una horizontal (cruce sin conexión)."""
        self.path(f"M{fmt(x)},{fmt(y + r)} A{r},{r} 0 0 1 {fmt(x)},{fmt(y - r)}", width=width)

    def sensor(self, cx, cy, symbol, tag=None, lines=(), r=14, label="below",
               accent=False) -> None:
        """Instrumento: círculo con etiqueta (pH / EC / T / L / F / M)."""
        col = GREEN if accent else INK
        self.circle(cx, cy, r, width=2, stroke=col)
        size = 11 if len(symbol) <= 1 else 10
        self.text(cx, cy + size * 0.36, symbol, size=size, anchor="middle", weight="bold", fill=col)
        if tag:
            self._label(cx, cy, r, tag, lines, label)

    def nozzle(self, cx, cy, size=6, color=GREEN) -> None:
        """Nebulizador: boquilla que rocía hacia abajo."""
        self.polygon([(cx - size * 0.6, cy - size), (cx + size * 0.6, cy - size), (cx, cy)],
                     fill=color, stroke=color, width=1)
        for k in (-1, 0, 1):
            self.line(cx, cy, cx + k * size * 1.1, cy + size * 1.8, stroke=color, width=1, dash="2 2")

    def drain(self, cx, cy, tag="coladera", lines=()) -> float:
        """Coladera: cuadro con rejilla. Devuelve la y bajo su rótulo."""
        s = 14
        self.rect(cx - s, cy - s, 2 * s, 2 * s, fill=LIGHT, width=1.6)
        for k in (-7, 0, 7):
            self.line(cx - s + 3, cy + k, cx + s - 3, cy + k, width=1.2)
        return self._label(cx, cy, s, tag, lines, "below")

    def gutter(self, x1, y1, x2, y2, depth=9, color=INK) -> None:
        """Canaleta abierta (perfil U) en alzado, de (x1,y1) a (x2,y2)."""
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        ux, uy = dx / n, dy / n
        px, py = -uy, ux  # normal (hacia abajo si la canaleta va a la derecha)
        d = (
            f"M{fmt(x1)},{fmt(y1)} L{fmt(x1 + px * depth)},{fmt(y1 + py * depth)} "
            f"L{fmt(x2 + px * depth)},{fmt(y2 + py * depth)} L{fmt(x2)},{fmt(y2)}"
        )
        self.path(d, width=2.2, stroke=color)
        # agua dentro
        self.line(x1 + px * depth * 0.55 + ux * 4, y1 + py * depth * 0.55 + uy * 4,
                  x2 + px * depth * 0.55 - ux * 4, y2 + py * depth * 0.55 - uy * 4,
                  stroke=GREEN, width=2, dash="6 3")

    def tray(self, x, y, w, h=8) -> None:
        """Charola 10×20 en alzado."""
        self.rect(x, y, w, h, fill=LIGHT, width=1.2)

    def _label(self, cx, cy, r, tag, lines, where) -> float:
        """Dibuja el rótulo del símbolo y devuelve la y por debajo de su última línea."""
        if where == "below":
            self.text(cx, cy + r + 14 * self.fs, tag, size=12, anchor="middle", weight="bold")
            return self.multiline(cx, cy + r + 28 * self.fs, lines, size=11, anchor="middle",
                                  fill=GRAY)
        if where == "above":
            n = len(lines)
            y0 = cy - r - 8 * self.fs - n * 15 * self.fs
            self.text(cx, y0, tag, size=12, anchor="middle", weight="bold")
            return self.multiline(cx, y0 + 15 * self.fs, lines, size=11, anchor="middle", fill=GRAY)
        if where == "right":
            self.text(cx + r + 8, cy + 4 * self.fs, tag, size=12, anchor="start", weight="bold")
            return self.multiline(cx + r + 8, cy + 18 * self.fs, lines, size=11, anchor="start",
                                  fill=GRAY)
        if where == "left":
            self.text(cx - r - 8, cy + 4 * self.fs, tag, size=12, anchor="end", weight="bold")
            return self.multiline(cx - r - 8, cy + 18 * self.fs, lines, size=11, anchor="end",
                                  fill=GRAY)
        return cy + r

    # -- cajas de texto -----------------------------------------------------------
    def note_h(self, w, lines, title=None, size=11) -> float:
        """Alto que ocupará la caja de notas ya con el texto ajustado al ancho."""
        lh = (size + 4) * self.fs
        n = len(self.wrap(lines, w - 28, size)) + (1 if title else 0)
        return n * lh + 14 * self.fs

    def note(self, x, y, w, lines, kind="info", title=None, size=11) -> float:
        """Caja de notas. kind: info (gris), ok (verde), warn (ámbar). Devuelve y final.

        El texto se ajusta al ancho de la caja y el alto sale de las líneas ya
        ajustadas: al subir FS la caja crece, no se desborda el texto.
        """
        col = {"info": GRAY, "ok": GREEN, "warn": AMBER}[kind]
        lh = (size + 4) * self.fs
        lines = self.wrap(lines, w - 28, size)
        n = len(lines) + (1 if title else 0)
        h = n * lh + 14 * self.fs
        self.rect(x, y, w, h, fill=WHITE, stroke=col, width=1.4, rx=4)
        self.rect(x, y, 5, h, fill=col, stroke=col, width=0, rx=1)
        yy = y + 16 * self.fs
        if title:
            self.text(x + 14, yy, title, size=size + 1, weight="bold", fill=col)
            yy += lh
        # multiline() ya multiplica por self.fs: hay que pasarle el interlineado
        # SIN escalar o el texto se sale por abajo de la caja (lo hacía).
        self.multiline(x + 14, yy, lines, size=size, lh=size + 4)
        return y + h

    LEGEND_LABEL = 11          # tamaño base del rótulo de cada símbolo
    LEGEND_GAP = 52            # del borde de la columna al inicio del rótulo

    def legend_geom(self, w, items, cols=2, row_h=30):
        """(alto, alto_de_fila, ancho_de_columna, rótulos ajustados).

        El rótulo se parte si no cabe en su columna y la fila crece para
        alojarlo: así el recuadro nunca corta una línea de texto.
        """
        cw = (w - 24) / cols
        avail = cw - self.LEGEND_GAP - 8
        labels = [self.wrap([lab], avail, self.LEGEND_LABEL) for _d, lab in items]
        lh = (self.LEGEND_LABEL + 3) * self.fs
        rows = math.ceil(len(items) / cols)
        row_h = max(row_h * self.fs, max(len(l) for l in labels) * lh + 10 * self.fs)
        return rows * row_h + 34 * self.fs, row_h, cw, labels

    def legend(self, x, y, w, items, cols=2, row_h=30) -> float:
        """Leyenda de símbolos: items = [(dibujo(sheet, cx, cy), texto)]."""
        h, row_h, cw, labels = self.legend_geom(w, items, cols, row_h)
        self.rect(x, y, w, h, fill=WHITE, stroke=INK, width=1.2, rx=4)
        self.text(x + 12, y + 20 * self.fs, "Leyenda de símbolos", size=12, weight="bold")
        lh = (self.LEGEND_LABEL + 3) * self.fs
        for i, (draw, _label) in enumerate(items):
            c, r = i % cols, i // cols
            cx = x + 12 + c * cw + 22
            cy = y + 34 * self.fs + r * row_h + row_h / 2
            draw(self, cx, cy)
            ls = labels[i]
            y0 = cy + 4 * self.fs - (len(ls) - 1) * lh / 2
            for k, ln in enumerate(ls):
                self.text(cx + 30, y0 + k * lh, ln, size=self.LEGEND_LABEL)
        return y + h

    def legend_h(self, w, items, cols=2, row_h=30) -> float:
        return self.legend_geom(w, items, cols, row_h)[0]

    # -- salida -------------------------------------------------------------------
    def render(self) -> str:
        head = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.title)}">\n'
            f"<title>{esc(self.title)}</title>\n"
            f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{WHITE}"/>\n'
        )
        # título arriba a la izquierda, versión arriba a la derecha.
        # Ambos se ajustan al ancho disponible: el cintillo es lo único que NO
        # puede crecer hacia abajo sin mover todo el dibujo.
        ver = "HomeGreen · " + VERSION
        ver_w = self.tw(ver, 12)
        t_size = 18.0
        t_room = self.w - 48 - ver_w - 20
        if self.tw(self.title, t_size) > t_room:
            t_size = max(13.0, t_size * t_room / self.tw(self.title, t_size))
        s_size = 12.0
        s_room = self.w - 48
        if self.tw(self.subtitle, s_size) > s_room:
            s_size = max(9.5, s_size * s_room / self.tw(self.subtitle, s_size))
        title = (
            f'<text x="24" y="34" font-family="{FONT}" font-size="{fmt(t_size * self.fs)}" font-weight="bold" '
            f'fill="{INK}">{esc(self.title)}</text>\n'
            f'<text x="24" y="56" font-family="{FONT}" font-size="{fmt(s_size * self.fs)}" fill="{GRAY}">'
            f"{esc(self.subtitle)}</text>\n"
            f'<text x="{self.w - 24}" y="34" font-family="{FONT}" font-size="{fmt(12 * self.fs)}" '
            f'text-anchor="end" fill="{GRAY}">{esc(ver)}</text>\n'
            f'<line x1="24" y1="64" x2="{self.w - 24}" y2="64" stroke="{INK}" stroke-width="1"/>\n'
        )
        return head + title + "\n".join(self.parts) + "\n</svg>\n"


# ---------------------------------------------------------------------------
# Mini-símbolos para leyendas
# ---------------------------------------------------------------------------
def lg_tank(s, cx, cy):
    s.rect(cx - 10, cy - 10, 20, 20, rx=3, width=1.6)
    s.line(cx - 10, cy + 2, cx + 10, cy + 2, stroke=GREEN, width=1.2, dash="3 2")


def lg_pump(s, cx, cy):
    s.pump(cx, cy, "", r=10)


def lg_filter(s, cx, cy):
    s.filter_(cx, cy, "", w=26, h=18)


def lg_valve(s, cx, cy):
    s.valve(cx, cy, size=8)


def lg_solenoid(s, cx, cy):
    s.valve(cx, cy + 4, size=7, butterfly=False)
    s.line(cx, cy + 4, cx, cy - 6, width=1.4)
    s.rect(cx - 6, cy - 16, 12, 10, width=1.4)


def lg_float(s, cx, cy):
    s.valve(cx - 6, cy - 4, size=7, butterfly=False)
    s.line(cx - 6, cy - 4, cx - 6, cy + 4, width=1.4)
    s.line(cx - 6, cy + 4, cx + 8, cy + 9, width=1.4)
    s.circle(cx + 12, cy + 10, 4, fill=LIGHT, width=1.4)


def lg_sensor(s, cx, cy):
    s.sensor(cx, cy, "pH", r=12)


def lg_pipe(s, cx, cy):
    s.pipe([(cx - 18, cy), (cx + 18, cy)], min_seg=10)


def lg_water(s, cx, cy):
    s.water([(cx - 18, cy), (cx + 18, cy)])


def lg_signal(s, cx, cy):
    s.signal([(cx - 18, cy), (cx + 18, cy)])


def lg_nozzle(s, cx, cy):
    s.nozzle(cx, cy - 4, size=5)


def lg_drain(s, cx, cy):
    s.rect(cx - 9, cy - 9, 18, 18, fill=LIGHT, width=1.3)
    for k in (-4, 0, 4):
        s.line(cx - 6, cy + k, cx + 6, cy + k, width=1)


def lg_gutter(s, cx, cy):
    s.gutter(cx - 16, cy - 3, cx + 16, cy - 1, depth=7)


def lg_line_nft(s, cx, cy):
    s.rect(cx - 18, cy - 5, 36, 10, fill=LIGHT, width=1.4, rx=3)
    for k in (-10, 0, 10):
        s.circle(cx + k, cy, 2.6, fill=WHITE, width=1)


# ---------------------------------------------------------------------------
# Diagrama 1 — Riego de microgreens
# ---------------------------------------------------------------------------
def build_riego() -> Sheet:
    s = Sheet(
        1240, 860,
        "P&ID · Riego de microgreens (Fase 1)",
        "tinaco 750 L → válvula → filtro de sedimentos → bomba diafragma 12 V → manifold → "
        "nebulizadores por nivel · nodo-riego-v1 · drenaje a coladera",
    )

    # ---- Tinaco TK-1 ----
    tx, ty, tw, th = 70, 230, 170, 230
    s.tank(tx, ty, tw, th, "TK-1 · Tinaco 750 L", [
        "Rotoplas Resistec 750 L ($2,051)",
        "opaco / a la sombra: luz + agua = algas",
        "lleno ≈ 750 kg → sobre piso firme",
        "tandeo duro: Plus+ 1,100 L ($3,774)",
    ], level=0.62)

    # entrada de captación pluvial (izquierda, por la tapa)
    s.multiline(30, 84, ["de captación pluvial", "(captacion-pluvial.svg)"], size=11, fill=GREEN)
    s.water([(30, 116), (30, 212), (tx + 30, 212), (tx + 30, ty)], arrows=[1])

    # nivel LT-1 en la tapa
    s.sensor(tx + 80, ty - 34, "L", "LT-1", [], r=14, label="left")
    s.line(tx + 80, ty - 20, tx + 80, ty, width=1.4, dash="3 2")
    s.multiline(tx + 102, ty - 52, [
        "JSN-SR04T en la tapa → nodo-riego-v1",
        "zona muerta ≈ 20 cm sobre nivel máx.",
        "adv. < 40 % · crítica < 20 % (interlock P-1)",
    ], size=11, fill=GRAY)

    # red SACMEX por la pared derecha con válvula de flotador.
    # El rótulo va a la IZQUIERDA de la bajante: a la derecha empieza el carril
    # del manifold y del rack, que con FS alto ya no deja hueco.
    s.pipe([(460, 104), (460, 250), (tx + tw, 250)], arrows=[0, 1])
    s.multiline(452, 100, ["red SACMEX → flotador FV-1",
                           "(solo rellena con presión)"], size=11, anchor="end", fill=GRAY)
    s.float_valve(tx + tw - 26, 250, "FV-1", [], label="left", mirror=True)

    # rebosadero
    s.pipe([(tx + tw, 285), (290, 285), (290, 345)], arrows=[1])
    s.text(296, 305, "rebosadero", size=11, fill=GRAY)
    s.text(296, 319, "→ coladera", size=11, fill=GRAY)

    # temperatura del agua
    # dentro del tinaco: a tx+90 el rótulo DS18B20 salía por la pared derecha
    s.sensor(tx + 50, ty + th - 65, "T", "TT-1", ["DS18B20"], r=14, label="right")

    # ---- Línea de succión: válvula, filtro, bomba ----
    yl = ty + th - 30  # 430
    s.pipe([(tx + tw, yl), (290, yl)], arrows=True)
    s.valve(290, yl, "V-1", ["paso 1½\""], label="above")
    s.pipe([(301, yl), (358, yl)], arrows=False)
    s.filter_(380, yl, "F-1", ["sedimentos"], label="above")
    s.pipe([(402, yl), (462, yl)], arrows=True, min_seg=30)
    s.pump(480, yl, "P-1", [
        "diafragma 12 V con presostato",
        "4–6 L/min · ~20 W · relé CH1",
        "fuente 12 V 5 A Steren ELI-1260",
    ], r=18)
    # control desde el nodo: la caja se dimensiona con el texto ya medido,
    # así el rótulo nunca sobresale del recuadro al subir FS.
    nb = ["nodo-riego-v1", "ESP32 · gabinete IP65", "electrico/nodo-riego-v1.svg"]
    nb_w = max(s.tw(t, 10) for t in nb) + 26
    nb_h = len(nb) * 15 * s.fs + 16 * s.fs
    nb_x, nb_y = 475 - nb_w / 2, 276
    s.signal([(480, yl - 18), (480, nb_y + nb_h)])
    s.rect(nb_x, nb_y, nb_w, nb_h, fill=LIGHT, width=1.4, rx=4)
    s.multiline(475, nb_y + 21 * s.fs, nb, size=10, anchor="middle")

    # ---- Subida al manifold ----
    mx = 580
    s.pipe([(498, yl), (mx, yl), (mx, 150)], arrows=[1])
    # Rótulo del manifold en el cintillo libre bajo el título: dentro del carril
    # del rack lo cruzarían el riel izquierdo y las bajadas por nivel.
    s.multiline(mx + 10, 86, ["manifold · 1 válvula por nivel", "manguera flexible del kit"],
                size=11, fill=GRAY)

    # ---- Rack de 5 niveles con nebulizadores ----
    rx, ry, rw = 700, 130, 290
    levels = [150, 230, 310, 390, 470]  # parrillas N5 (arriba) … N1 (abajo)
    names = [
        [("N5 germinación / oscuridad", GRAY), ("atomizar 1–2×/día a mano;", AMBER),
         ("tapa invertida + peso 2–4 kg", AMBER)],
        [("N4 desarrollo", GRAY)],
        [("N3 desarrollo", GRAY)],
        [("N2 desarrollo", GRAY)],
        [("N1 recién sembradas", GRAY), ("(más fresco)", GRAY)],
    ]
    s.line(rx, ry, rx, 500, width=3)
    s.line(rx + rw, ry, rx + rw, 500, width=3)
    s.text(rx + rw, ry - 30, "Rack Husky 183 × 91 × 46 cm", size=11, anchor="end", weight="bold")
    s.text(rx + rw, ry - 10, "5 niveles · ≥ 30 cm entre parrillas", size=11, anchor="end",
           weight="bold")
    for i, ly in enumerate(levels):
        s.line(rx, ly, rx + rw, ly, width=2.5)
        s.tray(rx + 20, ly - 10, 110)    # doble charola: perforada dentro de lisa
        s.tray(rx + 170, ly - 10, 110)
        if i > 0:
            for nx in (rx + 75, rx + 225):
                s.nozzle(nx, ly - 38, size=6)
            s.pipe([(mx, ly - 50), (rx + 40, ly - 50), (rx + rw - 40, ly - 50)], arrows=[0])
            s.valve(mx + 60, ly - 50, size=8)
            s.sensor(rx - 30, ly - 12, "M", r=10)
        for k, (txt, col) in enumerate(names[i]):
            s.text(rx + rw + 12, ly - 2 + k * 13 * s.fs, txt, size=11, fill=col)
    s.multiline(rx - 30, 548, ["MT-1…4 capacitivos", "(ADC1, conector arriba)"], size=10,
                lh=16, anchor="middle", fill=GRAY)

    # drenaje del rack → coladera (no recircula)
    s.rect(rx, 505, rw, 12, fill=LIGHT, width=1.4)
    s.text(rx + rw / 2, 530, "charola colectora de drenaje bajo el rack", size=11, anchor="middle", fill=GRAY)
    s.pipe([(rx + rw, 511), (rx + rw + 60, 511), (rx + rw + 60, 590)], arrows=[1])
    # el rótulo de la coladera baja con FS: la leyenda se coloca DEBAJO de él
    # (antes la leyenda estaba fija en y=672 y su recuadro blanco, dibujado
    # después, partía por la mitad el renglón "agua con sustrato = moho").
    drain_y = s.drain(rx + rw + 60, 610, "coladera del patio",
                      ["el drenaje NO recircula:", "agua con sustrato = moho"])

    # ---- Notas ----
    y0 = s.note(30, 578, 660, [
        "Riego por histéresis (L0): 4 capacitivos → ON si < límite inferior, OFF si > superior,",
        "máx. N ciclos/h. Consumo estimado: bomba 20 W × 15 min/día ≈ 0.2 kWh/mes.",
        "Interlock: P-1 no arranca con LT-1 < 20 % (bomba en seco) ni con nodo caído.",
        "Todo el riego sale del tinaco, NUNCA de la toma directa (tandeo).",
        "[POR VERIFICAR: Ø de la manguera flexible del manifold].",
    ], kind="ok", title="Lógica y dimensionamiento")
    y1 = s.note(30, y0 + 10, 660, [
        "Tras el destape, riego SOLO POR ABAJO (charola lisa debajo): mojar el follaje = moho.",
        "Los nebulizadores atomizan en germinación/oscuridad y en secas; en jun–sep (HR 70–89 %)",
        "subirrigación y ventilación forzada por HR > 70 %.",
        "Rack desnivelado → riego encharcado en una esquina → moho: nivelar y calzar patas.",
    ], kind="warn", title="Errores típicos")

    # ---- Leyenda ----
    leg_y = max(drain_y + 14, y1 + 14)
    leg_b = s.legend(30, leg_y, 1186, [
        (lg_tank, "tanque con nivel"),
        (lg_pump, "bomba (triángulo = sentido)"),
        (lg_filter, "filtro"),
        (lg_valve, "válvula de mariposa (manual)"),
        (lg_float, "válvula de flotador (red)"),
        (lg_sensor, "sensor (L, T, M, pH, EC, F)"),
        (lg_pipe, "tubería con flecha de flujo"),
        (lg_water, "agua de lluvia / entrada"),
        (lg_signal, "señal al ESP32"),
        (lg_nozzle, "nebulizador / microaspersor"),
        (lg_drain, "coladera"),
    ], cols=4, row_h=26)
    foot = leg_b + 24 * s.fs
    s.text(30, foot, "Fuentes: referencia/03-instalacion §1.2–1.3 · research/agua-captacion · "
           "research/electronica-automatizacion · bom/fase1.csv", size=10, fill=GRAY)
    s.h = int(math.ceil(foot + 16 * s.fs))
    return s


# ---------------------------------------------------------------------------
# Diagrama 2 — NFT recirculante
# ---------------------------------------------------------------------------
def build_nft() -> Sheet:
    s = Sheet(
        1240, 1080,
        "P&ID · NFT recirculante de hierbas (Fase 2)",
        "tambo 200 L → bomba diafragma 12 V (DC-first) → filtro malla 120 → manifold con válvulas → "
        "8 líneas PVC sanitario 4\" a 2–3 % → retorno 2\" → tambo · pH/EC en el retorno · nodo-nft-v2",
    )

    # ---- Manifold y 8 líneas (vista en planta) ----
    # hx1 se recortó de 1250 a 1108: MEDIDO, la columna "caudal" necesita 85 u
    # a su derecha (cxr = hx1 + 22) y el margen derecho está en 1216, así que
    # el lienzo baja de 1360 a 1240 u y cada letra gana 9.7 % en pantalla.
    hx0, hx1, hy = 520, 1108, 150
    s.pipe([(455, hy), (hx1, hy)], arrows=[0], width=3)
    s.text(460, 136, "manifold ¾\" · 1 válvula por línea (ajuste con botella de 1 L + cronómetro)",
           size=11, fill=GRAY)
    n_lines = 8
    pitch = (hx1 - hx0) / (n_lines - 1)
    ly0, ly1 = 205, 520
    ret_y = 560
    for i in range(n_lines):
        x = hx0 + i * pitch
        s.pipe([(x, hy), (x, ly0 - 12)], arrows=False)
        s.valve(x, hy + 26, size=8, orient="v")
        s.rect(x - 13, ly0, 26, ly1 - ly0, fill=LIGHT, width=1.8, rx=6)
        for k in range(6):
            s.circle(x, ly0 + 28 + k * 50, 6.5, fill=WHITE, width=1.2)
        s.text(x + 16, ly0 - 5, f"L{i + 1}", size=11, weight="bold")
        s.pipe([(x, ly1), (x, ret_y)], arrows=False)
    # pendiente de las líneas (flecha ámbar junto a L1)
    sx = hx0 - 24
    s.line(sx, ly0 + 10, sx, ly1 - 12, stroke=AMBER, width=2)
    s.polygon([(sx, ly1 - 2), (sx - 5, ly1 - 12), (sx + 5, ly1 - 12)], fill=AMBER, stroke=AMBER, width=1)
    s.text(sx - 6, (ly0 + ly1) / 2, "pendiente 2–3 %", size=11, anchor="middle", fill=AMBER,
           weight="bold", rotate=-90)
    # anotaciones de las líneas (suben para dejar libre el rótulo de F-2, que
    # crece hacia arriba desde el filtro dúplex)
    s.multiline(440, 190, [
        "8 líneas × 3 m · PVC SANITARIO 4\" Amanco blanco",
        "$415 / 6 m (½ tramo por línea) · NO C-40 ($1,401)",
        "10 sitios / línea · canastilla 3\" ($12.80)",
        "centros 20 cm albahaca / arúgula · 15 cm cilantro",
        "sierra copa del CUERPO de la canastilla",
        "(comprar canastillas ANTES de perforar; desbarbar)",
        "pendiente 2–3 % (2–3 cm por metro)",
        "soportes cada ≤ 1.5 m (sin panza)",
        "entrada ALTA · salida BAJA",
    ], size=11, anchor="end", fill=GRAY)
    # caudal objetivo (columna derecha)
    cxr = hx1 + 22
    s.text(cxr, 230, "caudal", size=11, fill=GREEN, weight="bold")
    s.text(cxr, 244, "por línea", size=11, fill=GREEN, weight="bold")
    s.text(cxr, 264, "1–2 L/min", size=14, fill=GREEN, weight="bold")
    s.text(cxr, 284, "total", size=11, fill=GREEN)
    s.text(cxr, 300, "8–16 L/min", size=12, fill=GREEN, weight="bold")
    s.text(cxr, 316, "a 1–2 m de", size=11, fill=GREEN)
    s.text(cxr, 330, "columna", size=11, fill=GREEN)

    # ---- Retorno 2" con sondas → tambo (por la pared derecha) ----
    bx, by, bw, bh = 170, 600, 160, 200
    s.pipe([(hx1, ret_y), (350, ret_y), (350, 640), (bx + bw, 640)], arrows=[0, 1], width=3)
    # Bloque único anclado al margen derecho, en el hueco que dejó la columna de
    # notas. Suelto a media hoja lo cruzaban la subida al manifold (y=630) y el
    # rótulo del retorno.
    s.multiline(1216, ret_y + 18, ["retorno por gravedad · PVC sanitario 2\"",
                                   "(codos 90° $28.80 · 45° $18.31)",
                                   "sondas en el RETORNO (solución mezclada),",
                                   "nunca junto a la dosificación"], size=11, anchor="end",
                fill=GRAY)
    s.sensor(700, ret_y, "pH", "AT-1", ["pH 5.8–6.2"], r=15, accent=True)
    s.sensor(600, ret_y, "EC", "AT-2", ["1.2–1.8 mS/cm"], r=15, accent=True)

    # ---- Tambo TK-2 ----
    tk_y = s.tank(bx, by, bw, bh, "TK-2 · Tambo 200 L", [
        "HDPE alimenticio $450–900",
        "tapado y a la sombra",
        "18–22 °C · > 25 °C cae el O₂",
        "cambio total cada 2–3 sem.",
    ], level=0.6)
    # TT-2 baja 30 u: a by+60 el rótulo DS18B20 quedaba justo sobre la línea
    # de nivel del tambo. LT-2 se corre a bx+100 para dejar libre la columna
    # de rótulos de la dosificación (x 40-220).
    s.sensor(bx + 50, by + 110, "T", "TT-2", ["DS18B20"], r=14, label="right")
    # LT-2 se corre a bx+110 y su texto se ancla a la derecha en x=250: en la
    # tapa izquierda el círculo y el rótulo caían sobre la columna de la
    # dosificación (x 40-220), que se ensanchó con la letra.
    s.sensor(bx + 110, by - 28, "L", "LT-2", [], r=13, label="left")
    s.line(bx + 110, by - 15, bx + 110, by, width=1.4, dash="3 2")
    s.text(250, 540, "nivel del tambo (interlock)", size=10, anchor="end", fill=GRAY)
    s.text(250, 556, "[POR VERIFICAR: no en BOM]", size=10, anchor="end", fill=AMBER)

    # ---- Succión: P-1 principal + P-2 respaldo → F-1 → FT-1 → subida ----
    sy = by + bh - 60  # 740
    s.pipe([(bx + bw, sy), (369, sy)], arrows=True)
    # rótulo arriba: abajo lo cruza la bajada de purga del tambo
    s.valve(380, sy, "V-0", ["paso"], size=10, label="above")
    s.pipe([(391, sy), (420, sy), (420, sy - 40), (452, sy - 40)], arrows=False)
    s.pipe([(420, sy), (420, sy + 40), (452, sy + 40)], arrows=False)
    s.pump(468, sy - 40, "P-1", [], r=16, label="above")
    s.pump(468, sy + 40, "P-2", [], r=16)
    s.pipe([(484, sy - 40), (520, sy - 40), (520, sy)], arrows=False)
    s.pipe([(484, sy + 40), (520, sy + 40), (520, sy)], arrows=False)
    s.pipe([(520, sy), (610, sy)], arrows=True)
    s.filter_(632, sy, "F-1", ["malla 120 mesh 1\" ($230)", "lavar cada semana"])
    # FT-1 se corre de 790 a 860: sus dos renglones y los de F-1 (centrados
    # bajo cada símbolo) se tocaban y se leían pegados ("($230)YF-S201").
    s.pipe([(654, sy), (845, sy)], arrows=True)
    s.sensor(860, sy, "F", "FT-1", ["YF-S201 · 450 pulsos/L", "alarma: ON y < 2 L/min 60 s"],
             r=15, accent=True)
    s.pipe([(875, sy), (900, sy), (900, sy - 80)], arrows=False)
    s.valve(900, sy - 40, size=9, orient="v")
    s.text(886, sy - 39, "V-8 purga a coladera / bypass", size=10, anchor="end", fill=GRAY)
    s.text(886, sy - 24, "(cambio de solución)", size=10, anchor="end", fill=GRAY)
    # subida al manifold: cruza el retorno con salto
    s.pipe([(900, sy - 80), (900, 630), (455, 630), (455, ret_y + 6)], arrows=[1])
    s.jump(455, ret_y)
    s.pipe([(455, ret_y - 6), (455, hy)], arrows=[0])
    # bajo el tramo horizontal de la subida (y=630): arriba lo alcanzaban los
    # rótulos de AT-1/AT-2, que crecen hacia abajo con FS
    s.text(462, 652, "subida ¾\" al manifold · distribución ½\"–¾\"", size=11, fill=GRAY)
    s.multiline(490, 836, [
        "P-1 principal + P-2 respaldo: diafragma 12 V 40–60 W (4–6 L/min c/u)",
        "en bus de batería LiFePO4 12.8 V 100 Ah → 28–30 h sin CFE (DC-first).",
        "Relevador de transferencia por ESP32: FT-1 sin flujo → arranca P-2.",
        "Bomba 127 V (sumergible 4500 LPH, 65 W) SOLO llenado / purga / trasiego.",
        "Detalle eléctrico: electrico/bus-dc-first.svg",
    ], size=11, fill=GRAY)

    # ---- Dosificación: 3 peristálticas al tambo, cerca de la succión ----
    # El encabezado va ARRIBA del tambo (x 170–330): a la altura de las bombas
    # el rótulo, ya más ancho, entraba en la pared del tambo.
    dx0 = 40
    s.text(dx0, 588, "DP-1/2/3 peristálticas 12 V", size=10, weight="bold")
    for j, nm in enumerate(["A", "B", "pH−"]):
        yy = 640 + j * 50
        s.rect(dx0, yy - 12, 30, 26, fill=LIGHT, width=1.3, rx=3)
        s.text(dx0 + 15, yy + 5, nm, size=10, anchor="middle", weight="bold")
        s.circle(dx0 + 62, yy, 9, width=1.6)
        s.circle(dx0 + 62, yy, 3, fill=INK)
        s.pipe([(dx0 + 30, yy), (dx0 + 53, yy)], arrows=False, width=1.4)
        s.pipe([(dx0 + 71, yy), (bx, yy)], arrows=False, width=1.4, dash="2 2")
    # bajo el rótulo del tambo (a la altura de la pared del tambo lo cruzaban)
    s.multiline(dx0, 915, ["A y B en botes separados", "(Ca precipita con PO₄ / SO₄)",
                           "pH−: AquAcid ($516)"], size=10, lh=14, fill=GRAY)

    # ---- Llenado desde tinaco: solenoide + dúplex ----
    fy = 470
    s.water([(30, fy), (139, fy)], arrows=True)
    # el segundo renglón llegaba a la cajita "S" de SV-1 (x 141-159)
    s.multiline(30, fy - 46, ["de TK-1 tinaco 750 L", "(lluvia / red)"], size=11, fill=GREEN)
    s.solenoid(150, fy, "SV-1", ["½\" NC 12 V"])
    s.pipe([(161, fy), (235, fy)], arrows=False)
    # F-2 se corre a la derecha y se queda con UN renglón: sus tres líneas
    # llegaban a la caja "S" del solenoide SV-1 y al bloque de las 8 líneas.
    # El detalle (cartuchos y periodicidad) pasó a la nota de errores típicos.
    s.filter_(260, fy, "F-2", ["dúplex 10\" (2 cartuchos)"], w=50, h=32, label="above")
    s.pipe([(285, fy), (300, fy), (300, by)], arrows=[1])
    # a la derecha de la bajada al tambo (x=300): encima la partía en dos
    s.multiline(310, fy + 22, ["SV-1 cerrada sin luz:", "no vacía el tinaco"], size=10,
                lh=16, fill=GRAY)

    # ---- Purga del tambo → coladera ----
    # La columna de purga se corrió de x=370 a x=410: con la letra más grande,
    # el rótulo SV-2 quedaba encima del rótulo del tambo.
    px = 410
    s.pipe([(bx + bw, by + bh - 15), (px, by + bh - 15), (px, 830)], arrows=False)
    s.solenoid(px, 845, "SV-2", [], orient="v", label="left")
    s.pipe([(px, 856), (px, 876)], arrows=False)
    dr_y = s.drain(px, 890, "coladera", ["purga NC · vaciado", "cada 2–3 semanas"])

    # ---- Banda inferior de texto ----
    # Todas las cajas van DEBAJO del dibujo, en dos columnas de 640 u. Antes la
    # columna derecha empezaba en x=880 y y=620, en medio del área de bombas y
    # del caudalímetro FT-1: al crecer la letra los rótulos de esos equipos se
    # metían bajo los recuadros blancos de las notas.
    band = max(dr_y, tk_y, 960, 836 + 5 * 15 * s.fs) + 16
    cw, cxa, cxb = 576, 30, 636
    y0 = s.note(cxa, band, cw, [
        "Sin recirculación las raíces (película 1–3 mm) se marchitan en 2–4 h",
        "con el túnel caliente: la bomba cuelga del bus de batería, no de HA.",
        "Watchdogs: FT-1 sin flujo → arranca P-2 + alarma crítica;",
        "sonda que no cambia en 24 h o salta > 1.5 en 5 min → 'no confiable'.",
        "Commissioning: 48 h con agua sola, sin fugas, caudal en rango por línea.",
    ], kind="ok", title="Continuidad y watchdogs")
    y1 = s.note(cxb, band, cw, [
        "Panza a media línea (soporte > 1.5 m) = agua estancada = raíces podridas.",
        "Perforar antes de tener las canastillas → hoyo de 2\" exacto: se cae.",
        "Peat pellets / turba tapan la malla 120. Tambo al sol > 25 °C: algas y sin O₂.",
        "Periférica 0.5 HP 24/7 = 324 kWh/mes → tarifa DAC.",
        "F-2 dúplex 10\": sedimento 5 µm + carbón activado (quita el cloro);",
        "cambiar cartuchos cada 4–6 meses.",
    ], kind="warn", title="Errores típicos")

    band2 = max(y0, y1) + 12
    d_b = s.note(cxa, band2, cw, [
        "dosis fija pequeña → esperar 10–15 min de mezcla → re-medir (histéresis).",
        "Interlock: sin dosis con LT-2 bajo o bomba OFF; dosificar AL TAMBO, no a una línea.",
        "Calibrar cada 15 días: pH 4.01 / 6.86 y EC 1.413 mS/cm (evento en HA).",
    ], kind="ok", title="Dosificación (L0)")

    # ---- Leyenda ----
    leg_b = s.legend(cxb, band2, cw, [
        (lg_tank, "tanque con nivel"),
        (lg_pump, "bomba"),
        (lg_filter, "filtro"),
        (lg_valve, "válvula de mariposa"),
        (lg_solenoid, "válvula solenoide NC"),
        (lg_sensor, "sensor pH / EC / T / L / F"),
        (lg_line_nft, "línea NFT 4\" con canastillas"),
        (lg_signal, "señal al ESP32"),
    ], cols=2, row_h=26)
    foot = max(d_b, leg_b) + 24 * s.fs
    s.text(30, foot, "Fuentes: referencia/03-instalacion §2.1–2.3 · research/hidroponia-nft · "
           "research/electrico-respaldo-seguridad §2 · referencia/06 L0 · bom/fase2.csv", size=10, fill=GRAY)
    s.h = int(math.ceil(foot + 16 * s.fs))
    return s


# ---------------------------------------------------------------------------
# Diagrama 3 — Captación pluvial
# ---------------------------------------------------------------------------
def build_captacion() -> Sheet:
    s = Sheet(
        1240, 922,
        "P&ID · Captación pluvial del túnel (Fase 1 → 2)",
        "techo del túnel → canalón PVC 0.5–1 % → bajante → filtro de hojas → separador de primeras "
        "lluvias (tlaloque) → tinaco 750 L (rebosadero a coladera) · flotador de red SACMEX",
    )

    # ---- Túnel (alzado, dos aguas) ----
    tx0, tx1, ty_base, ty_ridge = 60, 420, 330, 150
    tmid = (tx0 + tx1) / 2
    s.line(tx0, ty_base, tx0, 230, width=3)
    s.line(tx1, ty_base, tx1, 230, width=3)
    s.line(tx0, 230, tmid, ty_ridge, width=3)
    s.line(tmid, ty_ridge, tx1, 230, width=3)
    s.line(tx0 - 10, 216, tmid, ty_ridge - 16, width=1.2, dash="4 3")
    s.line(tmid, ty_ridge - 16, tx1 + 10, 216, width=1.2, dash="4 3")
    s.text(330, 150, "malla antigranizo 10–20 cm SOBRE el plástico", size=11, fill=GRAY)
    s.line(tx0 - 20, ty_base, tx1 + 20, ty_base, width=2)
    s.multiline(tmid, 262, [
        "túnel PTR · plástico UV cal. 720",
        "techo a dos aguas, pendiente ≥ 25 %",
        "3 × 6 m = 18 m² (F1) → 5 × 6 m = 30 m² (F2)",
    ], size=11, anchor="middle", fill=GRAY)
    for k in range(6):
        xx = 90 + k * 60
        s.line(xx, 96, xx - 6, 122, stroke=GREEN, width=1.4)
    s.text(80, 88, "lluvia: 1 mm = 1 L por m² de techo", size=11, fill=GREEN, weight="bold")

    # ---- Canaleta en el alero derecho, pendiente hacia la bajante ----
    s.gutter(414, 232, 486, 238, depth=10)
    s.multiline(500, 214, [
        "canalón PVC blanco $269 / 3.07 m (Home Depot)",
        "pendiente 0.5–1 % (1 cm por 2 m) hacia la bajante",
        "soportes al larguero bajo del alero",
    ], size=11, fill=GRAY)
    bxx = 490
    s.water([(bxx, 248), (bxx, 300)], arrows=True)
    s.text(500, 276, "bajante PVC 3\"", size=11, fill=GRAY)
    s.text(500, 294, "(o manguera reforzada)", size=11, fill=GRAY)

    # ---- Filtro de hojas ----
    s.filter_(bxx, 330, "F-3", ["filtro de hojas (malla inox)", "sólidos > 1 mm"], w=48, h=32,
              label="left")
    s.water([(bxx, 346), (bxx, 400)], arrows=True)

    # ---- Tlaloque (separador de primeras lluvias) ----
    tlx, tly = bxx, 400
    s.water([(tlx, tly), (tlx, tly + 20)], arrows=False)
    s.rect(tlx - 22, tly + 20, 44, 150, fill=WHITE, width=2.2, rx=4)
    s.add(f'<rect x="{tlx - 20}" y="{tly + 90}" width="40" height="78" fill="{GREEN}" fill-opacity="0.16"/>')
    s.circle(tlx, tly + 84, 11, fill=LIGHT, width=1.6)
    s.pipe([(tlx, tly + 170), (tlx, tly + 181)], arrows=False)
    s.valve(tlx, tly + 190, size=9, orient="v")
    s.pipe([(tlx, tly + 199), (tlx, tly + 230)], arrows=False)
    s.text(tlx + 16, tly + 238, "V-P purga (tapón de registro)", size=10, fill=GRAY)
    s.text(tlx + 16, tly + 253, "vaciar después de cada tormenta", size=10, fill=GRAY)
    s.text(tlx - 28, tly + 40, "SP-1", size=12, anchor="end", weight="bold")
    s.multiline(tlx - 28, tly + 56, [
        "separador de primeras lluvias",
        "F1: casero, tubo PVC 4\" vertical +",
        "tapón de purga (~$400–800 material)",
        "desvía los primeros 20–40 L que",
        "lavan polvo y hollín del techo",
        "F2: Tlaloque IU200 $4,500 (techos",
        "≤ 120 m²) · Paquete Básico Tláloc",
        "$5,300 = tlaloque + filtro + Axolote",
    ], size=11, anchor="end", fill=GRAY)
    # salida lateral hacia el tinaco (una vez lleno el tubo ciego)
    kx, ky, kw, kh = 800, 300, 190, 300
    s.water([(tlx + 22, tly + 50), (700, tly + 50), (700, 260), (kx + 60, 260), (kx + 60, ky)],
            arrows=[0, 1, 2])
    # anclado a la derecha justo antes de la pared del tinaco (x = kx = 800):
    # de izquierda a derecha el rótulo la cruzaba.
    s.text(790, tly + 68, "separador lleno → agua limpia al tinaco", size=11, anchor="end",
           fill=GREEN)

    # ---- Tinaco ----
    tk_y = s.tank(kx, ky, kw, kh, "TK-1 · Tinaco 750 L", [
        "Rotoplas Resistec 750 L ($2,051) · opaco",
        "sobre base firme al nivel del patio:",
        "lleno ≈ 750 kg · nunca sobre estructura ligera",
        "alcaldía con tandeo duro: 1,100 L ($3,774)",
    ], level=0.6)
    # en dos renglones: a una línea no cabe dentro del tinaco (190 u) y la
    # pared derecha del tanque le pasaba por encima.
    s.multiline(kx + kw / 2, ky + 92, ["reductor de turbulencia", "(Axolote, F2)"], size=10,
                lh=15, anchor="middle", fill=GRAY)
    s.line(kx + 25, ky, kx + 25, ky - 22, width=1.6)
    s.text(kx + 19, ky - 12, "jarro de aire", size=10, anchor="end", fill=GRAY)
    # nivel y temperatura
    s.sensor(kx + 120, ky - 34, "L", "LT-1", [], r=14, label="left")
    s.line(kx + 120, ky - 20, kx + 120, ky, width=1.4, dash="3 2")
    s.text(kx + 140, ky - 38, "JSN-SR04T", size=10, fill=GRAY)
    s.text(kx + 140, ky - 24, "alarma tinaco bajo en HA", size=10, fill=GRAY)
    # dentro del tinaco: a kx+105 el rótulo DS18B20 salía por la pared derecha
    s.sensor(kx + 60, ky + kh - 70, "T", "TT-1", ["DS18B20"], r=14, label="right")
    # red SACMEX por la pared derecha + flotador
    s.pipe([(1120, 160), (1120, 330), (kx + kw, 330)], arrows=[0, 1])
    s.multiline(1108, 140, ["red SACMEX (toma domiciliaria)", "solo rellena cuando hay presión"],
                size=11, anchor="end", fill=GRAY)
    s.float_valve(kx + kw - 26, 330, "FV-1", [], label="left", mirror=True)
    # rebosadero
    # la coladera sube 25 u: su rótulo tocaba el del tinaco, que baja con FS
    s.pipe([(kx + kw, 370), (1060, 370), (1060, 535)], arrows=[1])
    s.text(1066, 392, "rebosadero", size=11, fill=GRAY)
    dr_y = s.drain(1060, 560, "coladera del patio", [])
    # salida inferior → riego / NFT
    oy = ky + kh - 30
    s.pipe([(kx, oy), (751, oy)], arrows=True)
    s.valve(740, oy, "V-1", [], size=10)
    s.pipe([(729, oy), (682, oy)], arrows=False)
    s.filter_(660, oy, "F-1", ["sedimentos"], w=44, h=28)
    s.pipe([(638, oy), (580, oy)], arrows=True)
    # anclados antes de la pared del tinaco (x = kx = 800), que los cruzaba
    s.multiline(790, oy - 48, ["→ P-1 riego (riego-microgreens.svg)",
                               "→ llenado NFT (nft-recirculacion.svg)"], size=11, lh=15,
                anchor="end", fill=GREEN)

    # ---- Notas de dimensionamiento ----
    y0 = s.note(30, 672, 700, [
        "Tacubaya (SMN 1991–2020): 847 mm/año · núcleo jun–sep 132–176 mm/mes · 118 días de lluvia.",
        "Tormenta de 30 mm sobre 15–20 m² ≈ 500–600 L: no dejarla caer al patio.",
        "Anual (650 mm × coef. 0.9): 15 m² ≈ 8,800 L · 30 m² ≈ 17,500 L.",
        "Consumo del sistema ~1–3 m³/mes ⇒ en lluvias cubre 80–100 %; 750–1,100 L = 2–4 semanas.",
        "Agua de lluvia: EC 0.02–0.06 mS/cm, sin cloro (V7: medir pH/EC cada temporada).",
    ], kind="ok", title="Dimensionamiento")
    y1 = s.note(30, y0 + 10, 700, [
        "Sin separador: la primera lluvia mete hollín y polvo al tinaco. Tinaco al sol: algas.",
        "Canalón sin pendiente o con panza: se desborda en la tormenta vespertina.",
        "No tapar coladeras del patio con placas ni con el tinaco; rebosadero SIEMPRE a coladera.",
        "Programa Cosecha de Lluvia (SEDEMA, ene–feb): sistema ~$20k gratis si la alcaldía califica.",
    ], kind="warn", title="Errores típicos y atajo")

    # ---- Leyenda ----
    # Debajo del rótulo del tinaco y de la coladera: los dos bajan con FS y
    # antes el recuadro blanco de la leyenda les pasaba por encima.
    leg_b = s.legend(750, max(tk_y + 14, dr_y + 14, 672), 466, [
        (lg_gutter, "canaleta / canalón"),
        (lg_filter, "filtro (hojas / sedimentos)"),
        (lg_tank, "tanque / separador con nivel"),
        (lg_valve, "válvula manual"),
        (lg_float, "válvula de flotador (red)"),
        (lg_sensor, "sensor L nivel · T temperatura"),
        (lg_water, "agua de lluvia (acento)"),
        (lg_pipe, "tubería con flecha de flujo"),
        (lg_drain, "coladera"),
    ], cols=2, row_h=26)
    foot = max(y1, leg_b) + 24 * s.fs
    s.text(30, foot, "Fuentes: research/instalacion-tunel-detalle §4 · research/agua-captacion §b · "
           "research/clima-agronomia §4–5 · referencia/03-instalacion §1.1–1.2 · bom/fase1.csv", size=10, fill=GRAY)
    s.h = int(math.ceil(foot + 16 * s.fs))
    return s


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
DIAGRAMS = {
    "riego-microgreens.svg": build_riego,
    "nft-recirculacion.svg": build_nft,
    "captacion-pluvial.svg": build_captacion,
}


def default_out() -> Path:
    return Path(__file__).resolve().parents[2] / "docs" / "assets" / "diagramas" / "hidraulico"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=default_out(), help="carpeta de salida")
    ap.add_argument("--check", action="store_true", help="valida XML y tamaño > 4 KB")
    args = ap.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    ok = True
    for name, build in DIAGRAMS.items():
        svg = build().render()
        path = args.out / name
        path.write_text(svg, encoding="utf-8")
        size = path.stat().st_size
        status = "ok"
        if args.check:
            try:
                minidom.parseString(svg.encode("utf-8"))
            except Exception as e:  # noqa: BLE001
                status = f"XML INVÁLIDO: {e}"
                ok = False
            if size <= 4096:
                status = f"{status} · PESO INSUFICIENTE"
                ok = False
        print(f"{path}  {size / 1024:.1f} KB  {status}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
