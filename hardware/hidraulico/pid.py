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
VERSION = "v1 · 2026-09"


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

    def __init__(self, width: int, height: int, title: str, subtitle: str):
        self.w = width
        self.h = height
        self.title = title
        self.subtitle = subtitle
        self.parts: list[str] = []

    # -- primitivas ----------------------------------------------------------
    def add(self, s: str) -> None:
        self.parts.append(s)

    def text(self, x, y, s, size=12, anchor="start", weight="normal", fill=INK,
             rotate=None, italic=False) -> None:
        tr = f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"' if rotate is not None else ""
        st = ' font-style="italic"' if italic else ""
        self.add(
            f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{FONT}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{tr}>{esc(s)}</text>'
        )

    def multiline(self, x, y, lines, size=12, lh=None, anchor="start", fill=INK,
                  weight="normal") -> float:
        """Varias líneas de texto; devuelve la y siguiente."""
        lh = lh or size + 4
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
             label_dy=16) -> None:
        """Tanque: rectángulo con esquinas inferiores redondeadas y nivel de agua."""
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
        self.multiline(x + w / 2, y + h + label_dy + 16, lines, size=11, anchor="middle", fill=GRAY)

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

    def float_valve(self, cx, cy, tag, lines=(), label="below") -> None:
        """Válvula de flotador (llenado desde red): moño + brazo + bola."""
        s = 10
        self.valve(cx, cy, orient="h", size=s, butterfly=False)
        self.line(cx, cy, cx, cy + 14, width=1.6)
        self.line(cx, cy + 14, cx + 26, cy + 26, width=1.6)
        self.circle(cx + 32, cy + 29, 7, fill=LIGHT, width=1.6)
        self._label(cx, cy, s, tag, lines, label)

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

    def drain(self, cx, cy, tag="coladera", lines=()) -> None:
        """Coladera: cuadro con rejilla."""
        s = 14
        self.rect(cx - s, cy - s, 2 * s, 2 * s, fill=LIGHT, width=1.6)
        for k in (-7, 0, 7):
            self.line(cx - s + 3, cy + k, cx + s - 3, cy + k, width=1.2)
        self._label(cx, cy, s, tag, lines, "below")

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

    def _label(self, cx, cy, r, tag, lines, where) -> None:
        if where == "below":
            self.text(cx, cy + r + 14, tag, size=12, anchor="middle", weight="bold")
            self.multiline(cx, cy + r + 28, lines, size=11, anchor="middle", fill=GRAY)
        elif where == "above":
            n = len(lines)
            y0 = cy - r - 8 - n * 15
            self.text(cx, y0, tag, size=12, anchor="middle", weight="bold")
            self.multiline(cx, y0 + 15, lines, size=11, anchor="middle", fill=GRAY)
        elif where == "right":
            self.text(cx + r + 8, cy + 4, tag, size=12, anchor="start", weight="bold")
            self.multiline(cx + r + 8, cy + 18, lines, size=11, anchor="start", fill=GRAY)
        elif where == "left":
            self.text(cx - r - 8, cy + 4, tag, size=12, anchor="end", weight="bold")
            self.multiline(cx - r - 8, cy + 18, lines, size=11, anchor="end", fill=GRAY)

    # -- cajas de texto -----------------------------------------------------------
    def note(self, x, y, w, lines, kind="info", title=None, size=11) -> float:
        """Caja de notas. kind: info (gris), ok (verde), warn (ámbar). Devuelve y final."""
        col = {"info": GRAY, "ok": GREEN, "warn": AMBER}[kind]
        lh = size + 4
        n = len(lines) + (1 if title else 0)
        h = n * lh + 14
        self.rect(x, y, w, h, fill=WHITE, stroke=col, width=1.4, rx=4)
        self.rect(x, y, 5, h, fill=col, stroke=col, width=0, rx=1)
        yy = y + 16
        if title:
            self.text(x + 14, yy, title, size=size + 1, weight="bold", fill=col)
            yy += lh
        self.multiline(x + 14, yy, lines, size=size, lh=lh)
        return y + h

    def legend(self, x, y, w, items, cols=2, row_h=30) -> float:
        """Leyenda de símbolos: items = [(dibujo(sheet, cx, cy), texto)]."""
        rows = math.ceil(len(items) / cols)
        h = rows * row_h + 34
        self.rect(x, y, w, h, fill=WHITE, stroke=INK, width=1.2, rx=4)
        self.text(x + 12, y + 20, "Leyenda de símbolos", size=12, weight="bold")
        cw = (w - 24) / cols
        for i, (draw, label) in enumerate(items):
            c, r = i % cols, i // cols
            cx = x + 12 + c * cw + 22
            cy = y + 34 + r * row_h + row_h / 2
            draw(self, cx, cy)
            self.text(cx + 30, cy + 4, label, size=11)
        return y + h

    # -- salida -------------------------------------------------------------------
    def render(self) -> str:
        head = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.title)}">\n'
            f"<title>{esc(self.title)}</title>\n"
            f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{WHITE}"/>\n'
        )
        # título arriba a la izquierda, versión arriba a la derecha
        title = (
            f'<text x="24" y="34" font-family="{FONT}" font-size="18" font-weight="bold" '
            f'fill="{INK}">{esc(self.title)}</text>\n'
            f'<text x="24" y="54" font-family="{FONT}" font-size="12" fill="{GRAY}">'
            f"{esc(self.subtitle)}</text>\n"
            f'<text x="{self.w - 24}" y="34" font-family="{FONT}" font-size="12" '
            f'text-anchor="end" fill="{GRAY}">{esc("HomeGreen · " + VERSION)}</text>\n'
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
    s.sensor(cx, cy, "pH", r=10)


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
    tx, ty, tw, th = 70, 190, 170, 270
    s.tank(tx, ty, tw, th, "TK-1 · Tinaco 750 L", [
        "Rotoplas Resistec 750 L ($2,051)",
        "opaco / a la sombra: luz + agua = algas",
        "lleno ≈ 750 kg → sobre piso firme",
        "tandeo duro: Plus+ 1,100 L ($3,774)",
    ], level=0.62)

    # entradas al tinaco: captación pluvial (izq) y red SACMEX (der)
    s.water([(30, 120), (30, 175), (tx + 30, 175), (tx + 30, ty)], arrows=[1])
    s.multiline(30, 100, ["de captación pluvial", "(captacion-pluvial.svg)"], size=11, fill=GREEN)
    s.pipe([(tx + tw + 70, 120), (tx + tw + 70, 160), (tx + tw - 30, 160), (tx + tw - 30, ty)],
           arrows=[1])
    s.float_valve(tx + tw - 30, ty + 26, "FV-1", [], label="right")
    s.multiline(tx + tw + 78, 104, ["red SACMEX → válvula de flotador", "(solo rellena cuando hay presión)"],
                size=11, fill=GRAY)
    # rebosadero
    s.pipe([(tx + tw, ty + 40), (tx + tw + 40, ty + 40), (tx + tw + 40, ty + 95)], arrows=[0])
    s.text(tx + tw + 46, ty + 60, "rebosadero", size=11, fill=GRAY)
    s.text(tx + tw + 46, ty + 74, "→ coladera", size=11, fill=GRAY)

    # instrumentos del tinaco
    s.sensor(tx + 60, ty - 34, "L", "LT-1", [], r=14, label="left")
    s.line(tx + 60, ty - 20, tx + 60, ty, width=1.4, dash="3 2")
    s.multiline(tx + 80, ty - 46, [
        "JSN-SR04T ultrasónico en la tapa",
        "zona muerta ≈ 20 cm sobre nivel máx.",
        "adv. < 40 % · crítica < 20 % (interlock P-1)",
    ], size=11, fill=GRAY)
    s.sensor(tx + 110, ty + th - 60, "T", "TT-1", ["DS18B20", "sumergido"], r=14, label="right")

    # ---- Línea de succión: válvula, filtro, bomba ----
    yl = ty + th - 30  # 430
    s.pipe([(tx + tw, yl), (300, yl)], arrows=True)
    s.valve(300, yl, "V-1", ["paso · multiconector 1½\"", "salida del tinaco"])
    s.pipe([(311, yl), (370, yl)], arrows=False)
    s.filter_(395, yl, "F-1", ["filtro de sedimentos", "(accesorio del tinaco)"])
    s.pipe([(417, yl), (475, yl)], arrows=True, min_seg=30)
    s.pump(495, yl, "P-1", [
        "diafragma 12 V con presostato",
        "4–6 L/min · ~20 W · relé CH1",
        "12 V 5 A Steren ELI-1260",
    ], r=18)
    # señal de control al nodo
    s.signal([(495, yl - 18), (495, 330), (560, 330)])
    s.rect(560, 300, 150, 60, fill=LIGHT, width=1.4, rx=4)
    s.multiline(635, 322, ["nodo-riego-v1", "ESP32 · gabinete IP65", "(electrico/nodo-riego-v1.svg)"],
                size=11, anchor="middle")
    s.signal([(tx + 46, ty - 34), (tx + 46, 100), (635, 100), (635, 300)])
    s.text(400, 92, "señal LT-1 / TT-1 / MT-x → ESP32", size=11, fill=GRAY)

    # ---- Subida al manifold ----
    mx = 570  # x del manifold
    s.pipe([(513, yl), (mx, yl), (mx, 150)], arrows=[1])
    s.text(mx + 8, yl - 8, "manguera del kit de nebulizadores", size=11, fill=GRAY)
    s.text(mx + 8, 470, "[POR VERIFICAR: Ø de la manguera del kit]", size=11, fill=AMBER)

    # ---- Rack de 5 niveles con nebulizadores ----
    rx, ry, rw = 760, 130, 300
    levels = [150, 230, 310, 390, 470]  # y de cada parrilla (N5 arriba → N1 abajo)
    names = ["N5 germinación / oscuridad", "N4 desarrollo", "N3 desarrollo",
             "N2 desarrollo", "N1 recién sembradas (más fresco)"]
    # postes
    s.line(rx, ry, rx, 500, width=3)
    s.line(rx + rw, ry, rx + rw, 500, width=3)
    s.text(rx + rw / 2, ry - 10, "Rack Husky 183 × 91 × 46 cm · 5 niveles · ≥ 30 cm entre parrillas",
           size=12, anchor="middle", weight="bold")
    for i, ly in enumerate(levels):
        s.line(rx, ly, rx + rw, ly, width=2.5)
        # charolas (doble charola: perforada dentro de lisa)
        s.tray(rx + 20, ly - 10, 110)
        s.tray(rx + 170, ly - 10, 110)
        # nebulizadores (2 por nivel, encima)
        if i > 0:
            for nx in (rx + 75, rx + 225):
                s.nozzle(nx, ly - 38, size=6)
            # ramal del manifold
            s.pipe([(mx, ly - 50), (rx + 40, ly - 50), (rx + rw - 40, ly - 50)], arrows=[0])
            s.valve(mx + 60, ly - 50, size=8)
        s.text(rx + rw + 12, ly - 2, names[i], size=11, fill=GRAY)
        # sensores capacitivos de sustrato en N1–N4
        if i > 0:
            s.sensor(rx - 30, ly - 12, "M", r=10)
    # ramal superior N5: atomizado manual
    s.text(rx + 20, levels[0] - 26, "oscuridad 2–4 días: atomizar 1–2×/día a mano; tapa + peso 2–4 kg",
           size=10, fill=AMBER)
    s.multiline(mx + 10, 150 + 4, ["manifold", "1 válvula por nivel"], size=11, fill=GRAY)
    s.text(rx - 30, 520, "MT-1…4 capacitivos", size=10, anchor="middle", fill=GRAY)
    s.text(rx - 30, 533, "(ADC1, conector arriba)", size=10, anchor="middle", fill=GRAY)

    # drenaje del rack
    s.rect(rx, 505, rw, 12, fill=LIGHT, width=1.4)
    s.text(rx + rw / 2, 530, "charola colectora de drenaje bajo el rack", size=11, anchor="middle", fill=GRAY)
    s.pipe([(rx + rw, 511), (rx + rw + 60, 511), (rx + rw + 60, 590)], arrows=[1])
    s.drain(rx + rw + 60, 610, "coladera del patio", ["el drenaje NO recircula:", "agua con sustrato = moho"])

    # ---- Notas ----
    y0 = s.note(30, 560, 520, [
        "Riego por histéresis (L0): 4 capacitivos → ON si < límite inferior, OFF si > superior,",
        "máx. N ciclos/h. Consumo estimado: bomba 20 W × 15 min/día ≈ 0.2 kWh/mes.",
        "Interlock: P-1 no arranca con LT-1 < 20 % (bomba en seco) ni con nodo caído.",
        "Todo el riego sale del tinaco, NUNCA de la toma directa (tandeo).",
    ], kind="ok", title="Lógica y dimensionamiento")
    s.note(30, y0 + 10, 520, [
        "Tras el destape, riego SOLO POR ABAJO (charola lisa debajo): mojar el follaje = moho.",
        "Los nebulizadores atomizan en germinación/oscuridad y en secas; en jun–sep (HR 70–89 %)",
        "subirrigación y ventilación forzada por HR > 70 %.",
        "Rack desnivelado → riego encharcado en una esquina → moho: nivelar y calzar patas.",
    ], kind="warn", title="Errores típicos")

    # ---- Leyenda ----
    s.legend(580, 640, 630, [
        (lg_tank, "tanque con nivel"),
        (lg_pump, "bomba (triángulo = sentido)"),
        (lg_filter, "filtro"),
        (lg_valve, "válvula de mariposa (manual)"),
        (lg_float, "válvula de flotador (red)"),
        (lg_sensor, "sensor: L nivel · T temp · M sustrato"),
        (lg_pipe, "tubería con flecha de flujo"),
        (lg_water, "agua de lluvia / entrada"),
        (lg_signal, "señal al ESP32"),
        (lg_nozzle, "nebulizador / microaspersor"),
        (lg_drain, "coladera"),
    ], cols=2, row_h=28)
    s.text(30, 845, "Fuentes: referencia/03-instalacion §1.2–1.3 · research/agua-captacion · "
           "research/electronica-automatizacion · bom/fase1.csv", size=10, fill=GRAY)
    return s


# ---------------------------------------------------------------------------
# Diagrama 2 — NFT recirculante
# ---------------------------------------------------------------------------
def build_nft() -> Sheet:
    s = Sheet(
        1360, 940,
        "P&ID · NFT recirculante de hierbas (Fase 2)",
        "tambo 200 L → bomba diafragma 12 V (DC-first) → filtro malla 120 → manifold con válvulas → "
        "8 líneas PVC sanitario 4\" a 2–3 % → retorno 2\" → tambo · pH/EC en el retorno · nodo-nft-v2",
    )

    # ---- Manifold y 8 líneas ----
    hx0, hx1, hy = 520, 1250, 150
    s.pipe([(455, hy), (hx1, hy)], arrows=[0], width=3)
    s.text(hx0 - 60, hy - 14, "manifold ¾\" · 1 válvula por línea (ajuste con botella 1 L + cronómetro)",
           size=11, fill=GRAY)
    n_lines = 8
    pitch = (hx1 - hx0) / (n_lines - 1)
    ly0, ly1 = 205, 520  # tubo (entrada arriba → salida abajo, pendiente 2–3 %)
    ret_y = 560
    for i in range(n_lines):
        x = hx0 + i * pitch
        s.pipe([(x, hy), (x, ly0 - 12)], arrows=False)
        s.valve(x, hy + 26, size=8, orient="v")
        # tubo 4" en planta: tira con canastillas
        s.rect(x - 13, ly0, 26, ly1 - ly0, fill=LIGHT, width=1.8, rx=6)
        for k in range(6):
            s.circle(x, ly0 + 28 + k * 50, 6.5, fill=WHITE, width=1.2)
        s.text(x, ly1 + 14, f"L{i + 1}", size=11, anchor="middle", weight="bold")
        # bajada al retorno
        s.pipe([(x, ly1), (x, ret_y)], arrows=False)
    # anotaciones de las líneas
    s.multiline(hx0 - 20, ly0 + 40, [
        "8 líneas × 3 m",
        "PVC SANITARIO 4\"",
        "Amanco blanco",
        "$415 / 6 m (½ tramo por línea)",
        "NO hidráulico C-40 ($1,401)",
        "",
        "10 sitios / línea",
        "canastilla 3\" ($12.80)",
        "centros: 20 cm albahaca / arúgula",
        "15 cm cilantro",
        "sierra copa del CUERPO de la",
        "canastilla (medir antes; desbarbar)",
        "",
        "pendiente 2–3 % (2–3 cm / m)",
        "soportes cada ≤ 1.5 m (sin panza)",
        "entrada ALTA · salida BAJA",
    ], size=11, anchor="end", fill=GRAY)
    # flecha de pendiente
    s.line(hx0 - 210, ly0 + 250, hx0 - 30, ly0 + 250 + 5, stroke=AMBER, width=2)
    s.text(hx0 - 120, ly0 + 244, "2–3 %", size=11, anchor="middle", fill=AMBER, weight="bold")
    s.text(hx1 + 18, ly0 + 20, "caudal por línea", size=11, fill=GREEN, weight="bold")
    s.text(hx1 + 18, ly0 + 36, "1–2 L/min", size=14, fill=GREEN, weight="bold")
    s.text(hx1 + 18, ly0 + 54, "total 8–16 L/min", size=11, fill=GREEN)
    s.text(hx1 + 18, ly0 + 70, "a 1–2 m de columna", size=11, fill=GREEN)

    # ---- Retorno 2" → sondas → tambo ----
    s.pipe([(hx1, ret_y), (330, ret_y)], arrows=[0], width=3)
    s.text(900, ret_y + 18, "retorno por gravedad · PVC sanitario 2\" (codos 90° $28.80 · 45° $18.31)",
           size=11, fill=GRAY)
    s.sensor(700, ret_y, "pH", "AT-1", ["pH 5.8–6.2"], r=15, label="below", accent=True)
    s.sensor(600, ret_y, "EC", "AT-2", ["1.2–1.8 mS/cm"], r=15, label="below", accent=True)
    s.multiline(430, ret_y + 40, [
        "sondas en el RETORNO (solución mezclada),",
        "nunca junto a la dosificación",
    ], size=11, fill=GRAY)
    # tambo
    bx, by, bw, bh = 150, 600, 180, 200
    s.tank(bx, by, bw, bh, "TK-2 · Tambo 200 L", [
        "HDPE grado alimenticio ($450–900)",
        "tapado y a la sombra · 18–22 °C",
        "> 25 °C cae el O₂ disuelto",
        "cambio completo cada 2–3 semanas",
    ], level=0.6)
    s.pipe([(330, ret_y), (bx + bw - 30, ret_y), (bx + bw - 30, by)], arrows=[1])
    s.sensor(bx + 50, by + 60, "T", "TT-2", ["DS18B20"], r=14, label="right")
    s.sensor(bx + 30, by - 30, "L", "LT-2", [], r=13, label="left")
    s.line(bx + 30, by - 17, bx + 30, by, width=1.4, dash="3 2")
    s.text(bx + 50, by - 34, "nivel del tambo (interlock)", size=10, fill=GRAY)
    s.text(bx + 50, by - 21, "[POR VERIFICAR: flotador o JSN-SR04T n.º 2, no está en bom/fase2]",
           size=10, fill=AMBER)

    # ---- Succión: P-1 principal + P-2 respaldo en paralelo → F-1 → FT-1 → riser ----
    sy = by + bh - 40  # 760
    s.pipe([(bx + bw, sy), (380, sy)], arrows=True)
    s.valve(380, sy, "V-0", ["paso"], size=10)
    s.pipe([(391, sy), (420, sy), (420, sy - 40), (450, sy - 40)], arrows=False)
    s.pipe([(420, sy), (420, sy + 40), (450, sy + 40)], arrows=False)
    s.pump(468, sy - 40, "P-1", [], r=16)
    s.pump(468, sy + 40, "P-2", [], r=16)
    s.pipe([(484, sy - 40), (520, sy - 40), (520, sy)], arrows=False)
    s.pipe([(484, sy + 40), (520, sy + 40), (520, sy)], arrows=False)
    s.multiline(540, sy - 52, [
        "P-1 principal + P-2 respaldo: diafragma 12 V 40–60 W (4–6 L/min c/u)",
        "en bus de batería LiFePO4 12.8 V 100 Ah → 28–30 h sin CFE (DC-first)",
        "relevador de transferencia por ESP32 · ver electrico/bus-dc-first.svg",
        "bomba 127 V (sumergible 4500 LPH, 65 W) SOLO llenado / purga / trasiego",
    ], size=11, fill=GRAY)
    s.pipe([(520, sy), (600, sy)], arrows=True)
    s.filter_(632, sy, "F-1", ["malla 120 mesh 1\" ($230)", "lavar cada semana"])
    s.pipe([(654, sy), (720, sy)], arrows=True)
    s.sensor(748, sy, "F", "FT-1", ["YF-S201 · 450 pulsos/L", "alarma: bomba ON y < 2 L/min 60 s"],
             r=15, accent=True)
    s.pipe([(763, sy), (820, sy), (820, sy - 100)], arrows=[0])
    s.valve(820, sy - 60, size=9, orient="v")
    s.text(834, sy - 56, "V-8 purga a coladera / bypass", size=10, fill=GRAY)
    s.text(834, sy - 44, "(cambio de solución)", size=10, fill=GRAY)
    # riser: sube al manifold por la izquierda del campo de líneas
    s.pipe([(820, sy - 100), (820, sy - 130), (455, sy - 130), (455, hy)], arrows=[1, 2])
    s.text(462, sy - 138, "subida ¾\" al manifold", size=11, fill=GRAY)
    s.text(462, 240, "distribución ½\"–¾\"", size=11, fill=GRAY)

    # ---- Dosificación: 3 peristálticas al tambo cerca de la succión ----
    dx0 = 40
    for j, (nm, txt) in enumerate([("A", "sol. A"), ("B", "sol. B"), ("pH−", "AquAcid")]):
        yy = 640 + j * 50
        s.rect(dx0, yy - 12, 30, 26, fill=LIGHT, width=1.3, rx=3)
        s.text(dx0 + 15, yy + 5, nm, size=10, anchor="middle", weight="bold")
        s.circle(dx0 + 62, yy, 9, width=1.6)
        s.circle(dx0 + 62, yy, 3, fill=INK)
        s.pipe([(dx0 + 30, yy), (dx0 + 53, yy)], arrows=False, width=1.4)
        s.pipe([(dx0 + 71, yy), (bx, yy)], arrows=False, width=1.4, dash="2 2")
    s.multiline(dx0, 620, ["DP-1/2/3 peristálticas 12 V"], size=11, weight="bold")
    s.multiline(dx0, 810, [
        "dosis fija → esperar 10–15 min",
        "de mezcla → re-medir (histéresis)",
        "sin dosificación si LT-2 bajo o",
        "bomba OFF · A y B en botes",
        "separados (Ca precipita con PO₄/SO₄)",
        "calibración quincenal: pH 4.01/6.86,",
        "EC 1.413 mS/cm",
    ], size=10, fill=GRAY)

    # ---- Llenado desde tinaco: solenoide + dúplex ----
    fy = 470
    s.water([(30, fy), (110, fy)], arrows=True)
    s.multiline(30, fy - 26, ["de TK-1 tinaco 750 L", "(agua de lluvia / red)"], size=11, fill=GREEN)
    s.solenoid(140, fy, "SV-1", ["12 V ½\" NC", "(corte de luz = cerrada)"])
    s.pipe([(151, fy), (200, fy)], arrows=False)
    s.filter_(232, fy, "F-2", ["dúplex 10\": sedimento 5 µm +", "carbón activado (quita cloro)",
                               "cartuchos cada 4–6 meses"], w=50, h=32)
    s.pipe([(257, fy), (bx + 40, fy), (bx + 40, by)], arrows=[0])

    # ---- Purga del tambo ----
    s.pipe([(bx + 60, by + bh), (bx + 60, by + bh + 40)], arrows=False)
    s.solenoid(bx + 60, by + bh + 60, "SV-2", [], orient="v", label="right")
    s.pipe([(bx + 60, by + bh + 71), (bx + 60, by + bh + 90), (30, by + bh + 90)], arrows=[1])
    s.drain(30, by + bh + 118, "coladera", [])
    s.text(bx + 100, by + bh + 84, "purga NC · vaciado cada 2–3 semanas", size=10, fill=GRAY)

    # ---- Notas ----
    y0 = s.note(880, 620, 450, [
        "Sin recirculación las raíces (película 1–3 mm) se marchitan en 2–4 h",
        "con el túnel caliente: la bomba cuelga del bus de batería, no de HA.",
        "Watchdogs: FT-1 sin flujo → arranca P-2 + alarma crítica;",
        "sonda que no cambia en 24 h o salta > 1.5 en 5 min → 'no confiable'.",
        "Commissioning: 48 h con agua sola, sin fugas, caudal en rango por línea.",
    ], kind="ok", title="Continuidad y watchdogs")
    s.note(880, y0 + 10, 450, [
        "Panza a media línea (soporte > 1.5 m) = agua estancada = raíces podridas.",
        "Perforar antes de tener las canastillas → hoyo de 2\" exacto: se cae.",
        "Peat pellets / turba tapan la malla 120. Tambo al sol > 25 °C: algas y sin O₂.",
        "Periférica 0.5 HP 24/7 = 324 kWh/mes → tarifa DAC.",
    ], kind="warn", title="Errores típicos")

    # ---- Leyenda ----
    s.legend(880, 800, 450, [
        (lg_tank, "tanque con nivel"),
        (lg_pump, "bomba"),
        (lg_filter, "filtro"),
        (lg_valve, "válvula de mariposa"),
        (lg_solenoid, "válvula solenoide NC"),
        (lg_sensor, "sensor pH / EC / T / L / F"),
        (lg_line_nft, "línea NFT 4\" con canastillas"),
        (lg_signal, "señal al ESP32"),
    ], cols=2, row_h=26)
    s.text(30, 925, "Fuentes: referencia/03-instalacion §2.1–2.3 · research/hidroponia-nft · "
           "research/electrico-respaldo-seguridad §2 · referencia/06 L0 · bom/fase2.csv", size=10, fill=GRAY)
    return s


# ---------------------------------------------------------------------------
# Diagrama 3 — Captación pluvial
# ---------------------------------------------------------------------------
def build_captacion() -> Sheet:
    s = Sheet(
        1240, 860,
        "P&ID · Captación pluvial del túnel (Fase 1 → 2)",
        "techo del túnel → canalón PVC 0.5–1 % → bajante → filtro de hojas → separador de primeras "
        "lluvias (tlaloque) → tinaco 750 L (rebosadero a coladera) · flotador de red SACMEX",
    )

    # ---- Túnel (alzado, dos aguas) ----
    tx0, tx1, ty_base, ty_ridge = 60, 420, 330, 150
    tmid = (tx0 + tx1) / 2
    s.line(tx0, ty_base, tx0, 230, width=3)          # columna izq
    s.line(tx1, ty_base, tx1, 230, width=3)          # columna der
    s.line(tx0, 230, tmid, ty_ridge, width=3)        # cabio izq
    s.line(tmid, ty_ridge, tx1, 230, width=3)        # cabio der
    # malla antigranizo (doble techo)
    s.line(tx0 - 10, 216, tmid, ty_ridge - 16, width=1.2, dash="4 3")
    s.line(tmid, ty_ridge - 16, tx1 + 10, 216, width=1.2, dash="4 3")
    s.text(tmid, ty_ridge - 26, "malla antigranizo 10–20 cm SOBRE el plástico", size=11,
           anchor="middle", fill=GRAY)
    s.line(tx0 - 20, ty_base, tx1 + 20, ty_base, width=2)  # losa
    s.multiline(tmid, 262, [
        "túnel PTR · plástico UV cal. 720",
        "techo a dos aguas, pendiente ≥ 25 %",
        "3 × 6 m = 18 m² (F1) → 5 × 6 m = 30 m² (F2)",
    ], size=11, anchor="middle", fill=GRAY)
    # lluvia
    for k in range(6):
        xx = tx0 + 30 + k * 60
        s.line(xx, 96, xx - 6, 122, stroke=GREEN, width=1.4)
    s.text(tx0 + 20, 88, "lluvia: 1 mm = 1 L por m² de techo", size=11, fill=GREEN, weight="bold")

    # ---- Canaleta en el alero derecho, pendiente hacia la bajante ----
    gx0, gy0, gx1, gy1 = tx1 - 40, 232, tx1 + 60, 238
    s.gutter(gx0, gy0, gx1, gy1, depth=10)
    s.multiline(gx1 + 12, 214, [
        "canalón PVC blanco $269 / 3.07 m (Home Depot)",
        "pendiente 0.5–1 % (1 cm por 2 m) hacia la bajante",
        "soportes al larguero bajo del alero",
    ], size=11, fill=GRAY)
    # bajante
    bxx = gx1 + 4
    s.water([(bxx, gy1 + 10), (bxx, 300)], arrows=True)
    s.text(bxx + 10, 285, "bajante PVC 3\" o manguera reforzada", size=11, fill=GRAY)

    # ---- Filtro de hojas ----
    s.filter_(bxx, 330, "F-3", ["filtro de hojas (malla inox)", "sólidos > 1 mm"], w=48, h=32,
              label="left")
    s.water([(bxx, 346), (bxx, 400)], arrows=True)

    # ---- Tlaloque (separador de primeras lluvias) ----
    tlx, tly = bxx, 400
    # T: el agua entra, baja al tubo ciego; al llenarse, la bola flota y sella → sigue al tinaco
    s.water([(tlx, tly), (tlx, tly + 20)], arrows=False)
    s.rect(tlx - 22, tly + 20, 44, 150, fill=WHITE, width=2.2, rx=4)  # tubo 4" vertical
    s.add(f'<rect x="{tlx - 20}" y="{tly + 90}" width="40" height="78" fill="{GREEN}" fill-opacity="0.16"/>')
    s.circle(tlx, tly + 84, 11, fill=LIGHT, width=1.6)  # bola flotante
    s.text(tlx, tly + 88, "●", size=8, anchor="middle", fill=GRAY)
    s.valve(tlx, tly + 190, size=9, orient="v")
    s.pipe([(tlx, tly + 170), (tlx, tly + 181)], arrows=False)
    s.pipe([(tlx, tly + 199), (tlx, tly + 230)], arrows=False)
    s.text(tlx + 16, tly + 224, "V-P purga (tapón de registro)", size=10, fill=GRAY)
    s.text(tlx + 16, tly + 236, "vaciar después de cada tormenta", size=10, fill=GRAY)
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
    # salida lateral hacia tinaco (una vez lleno el tubo ciego)
    s.water([(tlx + 22, tly + 50), (700, tly + 50), (700, 300), (830, 300)], arrows=[0, 2])
    s.text(560, tly + 42, "lleno el separador → agua limpia al tinaco", size=11, fill=GREEN)

    # ---- Tinaco ----
    kx, ky, kw, kh = 800, 300, 190, 300
    s.tank(kx, ky, kw, kh, "TK-1 · Tinaco 750 L", [
        "Rotoplas Resistec 750 L ($2,051) · opaco",
        "sobre base firme al nivel del patio:",
        "lleno ≈ 750 kg · nunca sobre estructura ligera",
        "alcaldía con tandeo duro: 1,100 L ($3,774)",
    ], level=0.6)
    s.pipe([(830, 300), (830, ky)], arrows=False)
    s.text(838, ky - 8, "entrada con reductor de turbulencia (Axolote, F2)", size=10, fill=GRAY)
    # red SACMEX + flotador
    s.pipe([(1120, 160), (1120, 240), (kx + kw - 40, 240), (kx + kw - 40, ky)], arrows=[0, 1])
    s.multiline(1000, 140, ["red SACMEX (toma domiciliaria)", "solo rellena cuando hay presión"],
                size=11, fill=GRAY)
    s.float_valve(kx + kw - 40, ky + 28, "FV-1", ["flotador"], label="left")
    # rebosadero
    s.pipe([(kx + kw, ky + 45), (kx + kw + 50, ky + 45), (kx + kw + 50, 560)], arrows=[1])
    s.text(kx + kw + 56, ky + 60, "rebosadero", size=11, fill=GRAY)
    s.drain(kx + kw + 50, 585, "coladera del patio", ["no tapar coladeras con", "placas ni con el tinaco"])
    # jarro de aire
    s.line(kx + 30, ky, kx + 30, ky - 22, width=1.6)
    s.text(kx + 36, ky - 12, "jarro de aire", size=10, fill=GRAY)
    # instrumentos
    s.sensor(kx + 95, ky - 34, "L", "LT-1", [], r=14, label="left")
    s.line(kx + 95, ky - 20, kx + 95, ky, width=1.4, dash="3 2")
    s.text(kx + 115, ky - 38, "JSN-SR04T", size=10, fill=GRAY)
    s.text(kx + 115, ky - 26, "alarma tinaco bajo en HA", size=10, fill=GRAY)
    s.sensor(kx + 130, ky + kh - 70, "T", "TT-1", ["DS18B20"], r=14, label="right")
    # salida inferior → riego
    oy = ky + kh - 30
    s.pipe([(kx, oy), (740, oy)], arrows=True)
    s.valve(740, oy, "V-1", [], size=10, label="above")
    s.pipe([(729, oy), (690, oy)], arrows=False)
    s.filter_(660, oy, "F-1", [], w=40, h=28, label="above")
    s.pipe([(640, oy), (560, oy)], arrows=True)
    s.multiline(556, oy - 10, ["→ bomba de riego P-1", "(riego-microgreens.svg)", "y llenado NFT vía dúplex", "(nft-recirculacion.svg)"],
                size=11, anchor="end", fill=GREEN)
    s.text(700, oy + 34, "válvula + filtro de sedimentos", size=10, anchor="middle", fill=GRAY)

    # ---- Notas de dimensionamiento ----
    y0 = s.note(30, 660, 560, [
        "Tacubaya (SMN 1991–2020): 847 mm/año · núcleo jun–sep 132–176 mm/mes · 118 días de lluvia.",
        "Tormenta de 30 mm sobre 15–20 m² ≈ 500–600 L: no dejarla caer al patio.",
        "Anual (650 mm × coef. 0.9): 15 m² ≈ 8,800 L · 30 m² ≈ 17,500 L.",
        "Consumo del sistema ~1–3 m³/mes ⇒ en lluvias cubre 80–100 %; 750–1,100 L = 2–4 semanas.",
        "Agua de lluvia: EC 0.02–0.06 mS/cm, sin cloro (V7: medir pH/EC cada temporada).",
    ], kind="ok", title="Dimensionamiento")
    s.note(30, y0 + 10, 560, [
        "Sin separador: la primera lluvia mete hollín y polvo al tinaco. Tinaco al sol: algas.",
        "Canalón sin pendiente o con panza: se desborda en tormenta vespertina.",
        "Programa Cosecha de Lluvia (SEDEMA, ene–feb): sistema ~$20k gratis si la alcaldía califica.",
    ], kind="warn", title="Errores típicos y atajo")

    # ---- Leyenda ----
    s.legend(620, 660, 590, [
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
    s.text(30, 845, "Fuentes: research/instalacion-tunel-detalle §4 · research/agua-captacion §b · "
           "research/clima-agronomia §4–5 · referencia/03-instalacion §1.1–1.2 · bom/fase1.csv", size=10, fill=GRAY)
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
