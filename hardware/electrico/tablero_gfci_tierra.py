#!/usr/bin/env python3
"""Esquema eléctrico: tablero, GFCI y tierra física del circuito del patio.

Centro de carga → breaker QO120GFI → circuito del patio → contacto intemperie "in-use"
→ gabinete IP65 de CA → gabinete IP65 de CC; varilla copperweld 5/8" × 3 m → conductor
cal. 8 → barra de tierra (≤ 25 Ω medidos).

Genera docs/assets/diagramas/electrico/tablero-gfci-tierra.svg con schemdraw 0.23.
Ejecutar:  python3 hardware/electrico/tablero_gfci_tierra.py
Fuentes: docs/research/electrico-respaldo-seguridad.md §3.6 y §4 (NOM-001-SEDE-2012, DOF);
docs/referencia/03-instalacion.md §1.3.
"""
from __future__ import annotations

import os
import re

import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

INK = '#1f2937'
VERDE = '#2e7d32'
AMBAR = '#b45309'
GRIS = '#6b7280'
VERSION = 'v1 · 2026-09'

# Factor global de tipografia: sube el tamano de TODAS las etiquetas
# sin tocar `unit` (que ensancharia el lienzo y anularia la ganancia).
FS = 1.42

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, 'docs', 'assets', 'diagramas', 'electrico', 'tablero-gfci-tierra.svg')


# --- Ayudantes (idénticos en los 5 scripts) -----------------------------------
def texto(d, x, y, s, fs=11 * FS, halign='left', color=INK):
    d.add(elm.Label().at((x, y)).label(s, fontsize=fs, halign=halign, color=color))


def rect(d, c1, c2, color=INK, ls='-'):
    d.add(elm.Rect(corner1=c1, corner2=c2).at((0, 0)).theta(0).color(color).linestyle(ls))


def punto(d, p, color=INK):
    d.add(elm.Dot(radius=0.09).at(p).color(color))


def caja(d, x, y, w, h, titulo, izq=(), der=(), abajo=(), stub=0.6, fs=10 * FS, color=INK,
         titulo_fs=11 * FS, sub=None, titulo2=None):
    rect(d, (x, y), (x + w, y + h), color=color)
    texto(d, x + w / 2, y + h + 0.28, titulo, fs=titulo_fs, halign='center', color=color)
    if sub:
        texto(d, x + w / 2, y + h / 2, sub, fs=9 * FS, halign='center', color=GRIS)
    if titulo2:
        texto(d, x + w / 2, y + h + 0.28 + 0.34 * FS, titulo2, fs=8.5 * FS, halign='center', color=GRIS)
    anclas = {}
    for lista, lado in ((izq, 'izq'), (der, 'der')):
        n = len(lista)
        for i, (etq, nom) in enumerate(lista):
            py = y + h - h / (n + 1) * (i + 1)
            if lado == 'izq':
                d.add(elm.Line().at((x, py)).left(stub).color(color))
                texto(d, x + 0.12, py, etq, fs=fs, halign='left', color=color)
                anclas[nom] = (x - stub, py)
            else:
                d.add(elm.Line().at((x + w, py)).right(stub).color(color))
                texto(d, x + w - 0.12, py, etq, fs=fs, halign='right', color=color)
                anclas[nom] = (x + w + stub, py)
    n = len(abajo)
    for i, (etq, nom) in enumerate(abajo):
        px = x + w / (n + 1) * (i + 1)
        d.add(elm.Line().at((px, y)).down(stub).color(color))
        texto(d, px, y + 0.22, etq, fs=fs, halign='center', color=color)
        anclas[nom] = (px, y - stub)
    return anclas


def ruta(d, a, b, xm=None, color=INK, ls='-'):
    if xm is None:
        xm = (a[0] + b[0]) / 2
    d.add(elm.Line().at(a).to((xm, a[1])).color(color).linestyle(ls))
    d.add(elm.Line().at((xm, a[1])).to((xm, b[1])).color(color).linestyle(ls))
    d.add(elm.Line().at((xm, b[1])).to(b).color(color).linestyle(ls))


def postproceso(path, holgura_sup=22.0):
    """Corrige la fuente, pinta el fondo y abre sitio arriba para el título.

    schemdraw calcula el bbox de las etiquetas con un alto fijo, así que con la
    tipografía ampliada los acentos del título quedaban fuera del viewBox. Se
    estira el lienzo HACIA ARRIBA: como la columna limita el ancho, crecer de
    alto no reduce el tamaño del texto en pantalla.
    """
    with open(path, encoding='utf-8') as f:
        s = f.read()
    s = s.replace('font-family="sans"', 'font-family="sans-serif"')
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    vb[1] -= holgura_sup
    vb[3] += holgura_sup
    s = re.sub(r'viewBox="[^"]+"', 'viewBox="{} {} {} {}"'.format(*vb), s, count=1)
    s = re.sub(r'height="[\d.]+pt"', f'height="{vb[3]}pt"', s, count=1)
    rect_ = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="#ffffff"/>'
    i = s.index('>', s.index('<svg')) + 1
    s = s[:i] + rect_ + s[i:]
    # Halo blanco bajo cada rotulo, para que los trazos del esquema no lo tachen.
    # schemdraw dibuja los cables despues de las etiquetas, asi que un texto en
    # medio de un bus queda cruzado por la linea. paint-order="stroke" pinta
    # primero un contorno blanco grueso y encima la letra: la linea se "abre"
    # alrededor del texto sin mover nada de sitio. Es SVG2 y lo soportan
    # Chrome, Firefox y Safari desde 2016.
    # No se aplica al texto claro (seria invisible) ni a los <text> sin relleno.
    def _halo(m):
        etiqueta = m.group(0)
        if 'paint-order' in etiqueta:
            return etiqueta
        fill = re.search(r'fill="([^"]+)"', etiqueta)
        if fill and fill.group(1).lower() in ('#ffffff', 'white', 'none'):
            return etiqueta
        fs = re.search(r'font-size="([\d.]+)"', etiqueta)
        grosor = round(float(fs.group(1)) * 0.22, 2) if fs else 2.4
        return etiqueta[:-1] + (
            f' stroke="#ffffff" stroke-width="{grosor}" stroke-linejoin="round"'
            ' paint-order="stroke"' + etiqueta[-1:]
        )

    s = re.sub(r'<text\b[^>]*>', _halo, s)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


# --- Dibujo -------------------------------------------------------------------
with schemdraw.Drawing(file=SALIDA, show=False) as d:
    d.config(unit=2.0, fontsize=11 * FS, font='sans-serif', color=INK, lw=1.4, bgcolor='white', margin=0.3)

    texto(d, -0.5, 16.6, 'Tablero, GFCI y tierra física del circuito del patio (obligatorio antes del primer relé)', fs=16 * FS)
    texto(d, -0.5, 15.95, 'NOM-001-SEDE-2012: el patio es "lugar mojado" → GFCI en todo el circuito exterior, contactos WR con tapa "in-use", '
          'equipo en gabinete IP65 y puesta a tierra real (≤ 25 Ω).', fs=10 * FS, color=GRIS)
    texto(d, -0.5, 15.3, 'Lo instala un electricista certificado (medio día, ~$1,500–3,500 llave en mano con tierra). Tú verificas con este esquema y pides los 25 Ω medidos.',
          fs=9.5 * FS, color=GRIS)

    # ---------------- Acometida, medidor y centro de carga ----------------
    yL, yN, yT = 12.725, 12.25, 11.775  # niveles de L, N y T hacia el patio
    texto(d, -0.5, 11.0, 'Acometida CFE 127 V', fs=9.5 * FS, color=AMBAR)
    d.add(elm.Line().at((-0.5, 12.25)).right(1.0).color(AMBAR))
    md = caja(d, 0.5, 11.45, 2.2, 1.6, 'Medidor CFE', izq=[('', 'i')], der=[('', 'o')], color=AMBAR, titulo_fs=10 * FS)
    # Centro de carga: caja dibujada a mano con pines a alturas exactas
    CX, CY, CW, CH = 4.2, 8.8, 4.4, 4.9
    rect(d, (CX, CY), (CX + CW, CY + CH), color=AMBAR)
    texto(d, CX + CW / 2, CY + CH + 0.28, 'Centro de carga (casa)', fs=11 * FS, halign='center', color=AMBAR)
    texto(d, CX + CW / 2, CY + 3.9, 'interruptor principal', fs=9 * FS, halign='center', color=GRIS)
    texto(d, CX + CW / 2, CY + 2.2, 'barra de neutro', fs=9 * FS, halign='center', color=GRIS)
    texto(d, CX + CW / 2, CY + 1.6, 'barra de tierra', fs=9 * FS, halign='center', color=GRIS)
    texto(d, CX + CW / 2, CY + 1.1, 'puente de unión N–T', fs=8.5 * FS, halign='center', color=AMBAR)
    texto(d, CX + CW / 2, CY + 0.75, 'SOLO aquí, nunca en el patio', fs=8.5 * FS, halign='center', color=AMBAR)
    d.add(elm.Line().at(md['o']).to((CX, 12.25)).color(AMBAR))
    d.add(elm.Line().at((CX, 12.25)).left(0.0))
    for py, etq, col in ((yL, 'L', AMBAR), (yN, 'N', GRIS), (yT, 'T', VERDE)):
        d.add(elm.Line().at((CX + CW, py)).right(0.5).color(col))
        texto(d, CX + CW - 0.12, py, etq, fs=9.5 * FS, halign='right', color=col)
    d.add(elm.Line().at((CX + CW, 9.8)).right(0.5).linestyle('--').color(GRIS))
    texto(d, CX + CW + 0.6, 9.6, 'otros circuitos de la casa (refrigerador de cosecha, UPS del cerebro)', fs=8.5 * FS, color=GRIS)
    # Bajada a tierra desde la barra de tierra
    d.add(elm.Line().at((CX + 1.2, CY)).down(0.6).color(VERDE))
    texto(d, CX + 1.2, CY + 0.28, 'T', fs=9.5 * FS, halign='center', color=VERDE)

    # ---------------- Breaker GFCI en L y sensor diferencial ----------------
    d.add(elm.Breaker().at((CX + CW + 0.5, yL)).right().length(2.0).color(AMBAR)
          .label('QO120GFI 20 A', fontsize=9 * FS, loc='top', color=AMBAR))
    XB = CX + CW + 2.5
    d.add(elm.Line().at((XB, yL)).to((14.4, yL)).color(AMBAR))
    d.add(elm.Line().at((CX + CW + 0.5, yN)).to((14.4, yN)).color(GRIS))
    d.add(elm.Line().at((CX + CW + 0.5, yT)).to((14.4, yT)).color(VERDE))
    xs = 12.4
    d.add(elm.Dot(open=True, radius=0.42).at((xs, (yL + yN) / 2)).color(AMBAR))
    texto(d, xs, 11.05, 'sensor diferencial del GFCI: dispara si |I_L − I_N| ≥ ~5 mA', fs=8.5 * FS, halign='center', color=AMBAR)
    texto(d, xs, 10.7, '(fuga a tierra o a través de una persona) · botón TEST cada mes', fs=8.5 * FS, halign='center', color=GRIS)
    texto(d, xs + 0.6, 10.35, 'conductores L negro · N blanco · T verde/desnudo:', fs=8.5 * FS, halign='center', color=GRIS)
    texto(d, xs + 0.6, 10.0, 'cal. 12 AWG THW-LS en conduit', fs=8.5 * FS, halign='center', color=GRIS)

    # ---------------- Contacto intemperie y gabinetes ----------------
    ct = caja(d, 15.0, 11.3, 3.6, 1.9, 'Contacto dúplex WR 15/20 A', izq=[('L', 'l'), ('N', 'n'), ('T', 't')],
              der=[('', 'o')], color=AMBAR, titulo_fs=10 * FS, titulo2='tapa "in-use" (con la clavija puesta)')
    d.add(elm.Line().at(ct['o']).right(1.2).color(AMBAR))
    texto(d, ct['o'][0] + 0.6, ct['o'][1] + 0.3, 'clavija SJT uso rudo', fs=8.5 * FS, halign='center', color=GRIS)
    ga = caja(d, 20.4, 11.3, 4.0, 1.9, 'Gabinete A · IP65 · 127 V CA', izq=[('', 'i')], der=[('+12 V', 'p'), ('−', 'm')],
              abajo=[('T chasis', 'tc')], color=AMBAR, titulo_fs=10 * FS,
              titulo2='cargador / fuente 12 V 5 A')
    d.add(elm.Line().at((ct['o'][0] + 1.2, ct['o'][1])).to(ga['i']).color(AMBAR))
    gb = caja(d, 26.0, 11.3, 4.2, 1.9, 'Gabinete B · IP65 · 12 V CC', izq=[('+12 V', 'p'), ('−', 'm')],
              abajo=[('T chasis', 'tc')], color=VERDE, titulo_fs=10 * FS,
              titulo2='fusiblera, relés, buck, ESP32')
    d.add(elm.Line().at(ga['p']).to(gb['p']).color(VERDE))
    d.add(elm.Line().at(ga['m']).to(gb['m']).color(INK))
    # Tierra de equipo de gabinetes hasta la barra de tierra
    for g in (ga, gb):
        d.add(elm.Line().at(g['tc']).to((g['tc'][0], 10.0)).color(VERDE))
    d.add(elm.Line().at((ga['tc'][0], 10.0)).to((gb['tc'][0], 10.0)).color(VERDE))
    d.add(elm.Line().at((ga['tc'][0], 10.0)).to((ga['tc'][0], 9.6)).color(VERDE))
    d.add(elm.GroundChassis().at((ga['tc'][0], 9.6)).color(VERDE))
    texto(d, ga['tc'][0] - 1.5, 9.75, 'tierra de equipo → barra de tierra del tablero (vía el T)', fs=8.5 * FS, color=GRIS)
    texto(d, ga['tc'][0] - 1.5, 9.4, 'nunca a tubería de agua, ni al neutro, ni "en el aire"', fs=8.5 * FS, color=AMBAR)

    # ---------------- Electrodo de tierra ----------------
    xe = CX + 1.2
    d.add(elm.Line().at((xe, CY - 0.6)).to((xe, 6.6)).color(VERDE))
    texto(d, xe + 0.3, 7.9, 'conductor de puesta a tierra cal. 8 AWG', fs=9 * FS, color=VERDE)
    texto(d, xe + 0.3, 7.5, '(desnudo o verde), continuo, sin empalmes', fs=8.5 * FS, color=GRIS)
    rect(d, (xe - 0.9, 6.0), (xe + 0.9, 6.6), color=INK)
    texto(d, xe + 1.2, 6.45, 'conector de varilla (abrazadera de bronce)', fs=8.5 * FS, color=GRIS)
    texto(d, xe + 1.2, 6.08, 'o soldadura exotérmica', fs=8.5 * FS, color=GRIS)
    d.add(elm.Line().at((xe, 6.0)).to((xe, 1.4)).color(AMBAR).linewidth(4))
    texto(d, xe + 0.3, 5.0, 'varilla copperweld 5/8" × 3 m', fs=9 * FS)
    texto(d, xe + 0.3, 4.6, 'en registro con tapa, tierra húmeda (no bajo losa seca)', fs=8.5 * FS, color=GRIS)
    d.add(elm.Line().at((0.0, 5.5)).to((9.5, 5.5)).linestyle('--').color(GRIS))
    texto(d, 0.0, 5.75, 'nivel de piso', fs=8.5 * FS, color=GRIS)
    d.add(elm.Ground().at((xe, 1.4)))
    texto(d, xe + 0.3, 3.3, 'R ≤ 25 Ω medidos con telurómetro (pedir el valor por escrito).', fs=9 * FS, color=AMBAR)
    texto(d, xe + 0.3, 2.9, 'Si sale > 25 Ω: 2.ª varilla en paralelo (separación mínima según', fs=8.5 * FS, color=GRIS)
    texto(d, xe + 0.3, 2.55, 'NOM-001 Art. 250) o intensificador de tierra (GEM).', fs=8.5 * FS, color=GRIS)
    texto(d, xe + 0.3, 2.0, 'GFCI protege personas (5 mA); la tierra da camino de falla', fs=8.5 * FS, color=GRIS)
    texto(d, xe + 0.3, 1.65, 'y protege equipo. Se necesitan AMBOS.', fs=8.5 * FS, color=GRIS)

    # ---------------- "Nunca" ----------------
    NX, NY = 15.0, 3.0
    rect(d, (NX, NY), (NX + 15.2, NY + 5.2), color=AMBAR, ls='--')
    texto(d, NX + 0.2, NY + 4.8, 'NUNCA en el patio (cada punto es un accidente documentado):', fs=10 * FS, color=AMBAR)
    nunca = ['extensiones domésticas ni multicontactos al aire; solo circuito fijo + contacto WR con tapa',
             'empalmes fuera de caja o con cinta: todo empalme en caja IP65 con borneras',
             'fuentes, relés o el ESP32 "al aire" o en caja de cartón/plástico sin IP65',
             '127 V y 12 V en el mismo gabinete o compartiendo prensaestopa',
             'usar el neutro como tierra o "aterrizar" a la tubería de agua',
             'quitar el GFCI porque "dispara mucho": si dispara, hay una fuga real que buscar',
             'trabajar con la mano mojada o sin botar el breaker (bloquear con candado y aviso)']
    for i, t in enumerate(nunca):
        texto(d, NX + 0.4, NY + 4.25 - i * 0.55, '• ' + t, fs=9 * FS)

    # ---------------- Leyenda y pie ----------------
    LX, LY = 15.0, -0.4
    rect(d, (LX, LY), (LX + 15.2, LY + 3.2), color=GRIS)
    texto(d, LX + 0.2, LY + 2.85, 'Leyenda', fs=10.5 * FS)
    d.add(elm.Line().at((LX + 0.2, LY + 2.35)).right(0.8).color(AMBAR))
    texto(d, LX + 1.2, LY + 2.35, 'fase L 127 V CA (negro) · equipo de CA · varilla de tierra', fs=9.5 * FS)
    d.add(elm.Line().at((LX + 0.2, LY + 1.85)).right(0.8).color(GRIS))
    texto(d, LX + 1.2, LY + 1.85, 'neutro N (blanco)', fs=9.5 * FS)
    d.add(elm.Line().at((LX + 0.2, LY + 1.35)).right(0.8).color(VERDE))
    texto(d, LX + 1.2, LY + 1.35, 'tierra T (verde / desnudo) · +12 V CC en gabinete B', fs=9.5 * FS)
    texto(d, LX + 0.2, LY + 0.85, 'WR = resistente a intemperie · IP65 = hermético a polvo y chorro de agua', fs=9.5 * FS)
    texto(d, LX + 0.2, LY + 0.35, 'GFCI = interruptor por falla a tierra', fs=9.5 * FS)

    texto(d, -0.5, -1.2, 'Fuentes: research/electrico-respaldo-seguridad.md §3.6 y §4 (NOM-001-SEDE-2012 en DOF) · referencia/03-instalacion.md §1.3 · bom/fase2.csv (seguridad)', fs=9 * FS, color=GRIS)
    texto(d, -0.5, -1.7, f'{VERSION} · HomeGreen · generado con schemdraw desde hardware/electrico/tablero_gfci_tierra.py', fs=9 * FS, color=GRIS)

postproceso(SALIDA)
print('OK', SALIDA, os.path.getsize(SALIDA), 'bytes')
