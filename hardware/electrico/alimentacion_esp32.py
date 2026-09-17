#!/usr/bin/env python3
"""Esquema eléctrico: alimentación y protección del ESP32 (común a ambos nodos).

12 V → fusible → diodo de polaridad → buck LM2596 → 5 V → ESP32 (LDO 3V3 interno);
capacitores de desacoplo; tierra común en estrella; presupuesto de corriente.

Genera docs/assets/diagramas/electrico/alimentacion-esp32.svg con schemdraw 0.23.
Ejecutar:  python3 hardware/electrico/alimentacion_esp32.py
Fuentes: docs/referencia/03-instalacion.md §1.3 (fuente 12 V 5 A, buck a 5 V, tierra común);
docs/research/electronica-automatizacion.md §2.
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

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, 'docs', 'assets', 'diagramas', 'electrico', 'alimentacion-esp32.svg')


# --- Ayudantes (idénticos en los 5 scripts) -----------------------------------
def texto(d, x, y, s, fs=11, halign='left', color=INK):
    d.add(elm.Label().at((x, y)).label(s, fontsize=fs, halign=halign, color=color))


def rect(d, c1, c2, color=INK, ls='-'):
    d.add(elm.Rect(corner1=c1, corner2=c2).at((0, 0)).theta(0).color(color).linestyle(ls))


def punto(d, p, color=INK):
    d.add(elm.Dot(radius=0.09).at(p).color(color))


def caja(d, x, y, w, h, titulo, izq=(), der=(), abajo=(), stub=0.6, fs=10, color=INK,
         titulo_fs=11, sub=None, titulo2=None):
    rect(d, (x, y), (x + w, y + h), color=color)
    texto(d, x + w / 2, y + h + 0.28, titulo, fs=titulo_fs, halign='center', color=color)
    if sub:
        texto(d, x + w / 2, y + h / 2, sub, fs=9, halign='center', color=GRIS)
    if titulo2:
        texto(d, x + w / 2, y + h + 0.62, titulo2, fs=8.5, halign='center', color=GRIS)
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


def postproceso(path):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    s = s.replace('font-family="sans"', 'font-family="sans-serif"')
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    rect_ = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="#ffffff"/>'
    i = s.index('>', s.index('<svg')) + 1
    s = s[:i] + rect_ + s[i:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


# --- Dibujo -------------------------------------------------------------------
with schemdraw.Drawing(file=SALIDA, show=False) as d:
    d.config(unit=2.0, fontsize=11, font='sans-serif', color=INK, lw=1.4, bgcolor='white', margin=0.8)

    texto(d, -0.5, 14.4, 'Alimentación y protección del ESP32 (común a los nodos de riego y NFT)', fs=16)
    texto(d, -0.5, 13.75, '12 V → buck → 5 V → ESP32 (3V3 interno) · capacitores de desacoplo · tierra común en estrella · presupuesto de corriente. '
          'Detalle del bloque "alimentación" de nodo-riego-v1.svg y nodo-nft-v2.svg.', fs=10, color=GRIS)

    # ---------------- Cadena 12 V -> 5 V ----------------
    y = 10.0
    d.add(elm.Vdd().at((0.0, y)).color(VERDE))
    texto(d, -0.3, y + 0.55, '+12 V', fs=9, halign='right', color=VERDE)
    texto(d, -0.5, y + 2.4, 'Entrada: +12 V desde la fusiblera del bus DC (F3) o desde la fuente 12 V 5 A (F0).', fs=9.5, color=GRIS)
    d.add(elm.Fuse().at((0.0, y)).right().length(1.8).color(VERDE).label('F 2 A', fontsize=9, loc='bottom'))
    d.add(elm.Diode().at((1.8, y)).right().length(1.8).color(VERDE)
          .label('D1 1N5822 Schottky (polaridad inversa)', fontsize=9, loc='top'))
    na = (3.6, y)
    punto(d, na, color=VERDE)
    d.add(elm.Capacitor(polar=True).at(na).down().length(1.6))
    texto(d, na[0] - 0.35, na[1] - 1.1, 'C1 100 µF / 25 V', fs=9, halign='right')
    d.add(elm.Ground().at((na[0], na[1] - 1.6)))
    d.add(elm.Line().at(na).right(1.2).color(VERDE))
    nt = (4.8, y)
    punto(d, nt, color=VERDE)
    d.add(elm.DiodeTVS().at(nt).down().length(1.6).linestyle('--').color(GRIS))
    d.add(elm.Ground().at((nt[0], nt[1] - 1.6)).linestyle('--').color(GRIS))
    texto(d, nt[0] + 0.35, nt[1] - 1.9, 'TVS SMBJ15A (opcional:', fs=8.5, color=GRIS)
    texto(d, nt[0] + 0.35, nt[1] - 2.25, 'picos al arrancar la bomba)', fs=8.5, color=GRIS)
    bk = caja(d, 6.2, y - 0.8, 3.2, 1.6, 'Buck LM2596 (módulo 3 A)', izq=[('IN+', 'ip'), ('IN−', 'im')],
              der=[('OUT+', 'op'), ('OUT−', 'om')], titulo_fs=10, fs=9,
              titulo2='ajustar a 5.0 V con multímetro ANTES de conectar el ESP32')
    ruta(d, nt, bk['ip'], xm=nt[0] + 0.5, color=VERDE)
    d.add(elm.Ground().at(bk['im']))
    d.add(elm.Ground().at(bk['om']))
    y5 = bk['op'][1]
    d.add(elm.Line().at(bk['op']).right(1.0).color(VERDE))
    nc = (bk['op'][0] + 1.0, y5)
    punto(d, nc, color=VERDE)
    d.add(elm.Capacitor(polar=True).at(nc).down().length(1.6))
    texto(d, nc[0] + 0.35, nc[1] - 0.8, 'C2 470 µF / 10 V', fs=9)
    d.add(elm.Ground().at((nc[0], nc[1] - 1.6)))
    d.add(elm.Line().at(nc).right(2.8).color(VERDE))
    ndd = (nc[0] + 2.8, y5)
    punto(d, ndd, color=VERDE)
    d.add(elm.Capacitor().at(ndd).down().length(1.6))
    texto(d, ndd[0] + 0.35, ndd[1] - 0.8, 'C3 100 nF', fs=9)
    d.add(elm.Ground().at((ndd[0], ndd[1] - 1.6)))
    d.add(elm.Line().at(ndd).right(1.6).color(VERDE))
    # Rama +5 V a módulos
    d.add(elm.Line().at(ndd).up(1.5).color(VERDE))
    d.add(elm.Vdd().at((ndd[0], ndd[1] + 1.5)).color(VERDE).label('+5 V', fontsize=9, color=VERDE))
    texto(d, ndd[0] + 0.8, ndd[1] + 2.1, '→ módulo relé (VCC y JD-VCC), JSN-SR04T, placa pH, YF-S201', fs=9, color=VERDE)
    texto(d, ndd[0] + 0.8, ndd[1] + 1.75, 'cable cal. 18 AWG, < 30 cm del buck al ESP32 (evita brownout por caída)', fs=8.5, color=GRIS)

    # ---------------- ESP32 ----------------
    EX, EY, EW, EH = ndd[0] + 1.6, y5 - 3.7, 4.6, 4.7
    rect(d, (EX, EY), (EX + EW, EY + EH))
    texto(d, EX + EW / 2, EY + EH + 0.28, 'ESP32 DevKit V1', fs=12, halign='center')
    texto(d, EX + EW / 2, y5 - 0.6, 'AMS1117-3.3 (LDO interno)', fs=9, halign='center', color=GRIS)
    texto(d, EX + EW / 2, y5 - 0.95, '≤ 600 mA; disipa (5−3.3 V)·I', fs=8.5, halign='center', color=GRIS)
    texto(d, EX + EW / 2, EY + 0.4, 'USB: solo flasheo inicial;', fs=8.5, halign='center', color=AMBAR)
    texto(d, EX + EW / 2, EY + 0.08, 'nunca USB y VIN a la vez', fs=8.5, halign='center', color=AMBAR)
    pins_izq = [('VIN (5 V)', y5), ('GND', y5 - 1.5), ('EN', y5 - 2.9)]
    pins_der = [('3V3', y5), ('GND', y5 - 1.5), ('GPIOs (3.3 V)', y5 - 2.9)]
    esp = {}
    for etq, py in pins_izq:
        d.add(elm.Line().at((EX, py)).left(0.6))
        texto(d, EX + 0.12, py, etq, fs=9.5)
        esp['i_' + etq.split()[0]] = (EX - 0.6, py)
    for etq, py in pins_der:
        d.add(elm.Line().at((EX + EW, py)).right(0.6))
        texto(d, EX + EW - 0.12, py, etq, fs=9.5, halign='right')
        esp['d_' + etq.split()[0]] = (EX + EW + 0.6, py)
    d.add(elm.Ground().at(esp['i_GND']))
    d.add(elm.Ground().at(esp['d_GND']))
    # EN: pull-up interno de la placa + 100 nF para arranque limpio
    d.add(elm.Capacitor().at(esp['i_EN']).down().length(1.0))
    texto(d, esp['i_EN'][0] - 0.3, esp['i_EN'][1] - 0.5, 'C4 100 nF', fs=9, halign='right')
    d.add(elm.Ground().at((esp['i_EN'][0], esp['i_EN'][1] - 1.0)))
    texto(d, esp['i_EN'][0] + 0.2, esp['i_EN'][1] - 1.75, 'C4 en EN: reset limpio tras huecos', fs=8.5, halign='right', color=GRIS)
    texto(d, esp['i_EN'][0] + 0.2, esp['i_EN'][1] - 2.1, 'de la fuente (arranques fallidos)', fs=8.5, halign='right', color=GRIS)
    # 3V3 a sensores
    d.add(elm.Line().at(esp['d_3V3']).right(0.8).color(VERDE))
    ne = (esp['d_3V3'][0] + 0.8, y5)
    punto(d, ne, color=VERDE)
    d.add(elm.Capacitor(polar=True).at(ne).down().length(1.6))
    texto(d, ne[0] + 0.35, ne[1] - 0.8, 'C5 10 µF', fs=9)
    d.add(elm.Ground().at((ne[0], ne[1] - 1.6)))
    d.add(elm.Line().at(ne).right(2.0).color(VERDE))
    nf = (ne[0] + 2.0, y5)
    punto(d, nf, color=VERDE)
    d.add(elm.Capacitor().at(nf).down().length(1.6))
    texto(d, nf[0] + 0.35, nf[1] - 0.8, 'C6 100 nF', fs=9)
    d.add(elm.Ground().at((nf[0], nf[1] - 1.6)))
    d.add(elm.Line().at(nf).right(1.8).color(VERDE))
    d.add(elm.Vdd().at((nf[0] + 1.8, y5)).color(VERDE).label('3V3', fontsize=9, color=VERDE))
    texto(d, nf[0] + 2.3, y5 + 0.25, '→ SHT31, DS18B20, capacitivos ×4, TDS, pull-ups', fs=9, color=VERDE)
    texto(d, nf[0] + 2.3, y5 - 0.15, 'solo sensores (decenas de mA); nunca relés/bombas', fs=8.5, color=GRIS)
    texto(d, nf[0] + 2.3, y5 - 0.55, '100 nF junto a cada sensor; conector hacia arriba', fs=8.5, color=GRIS)
    d.add(elm.Dot(radius=0.01).at((nf[0] + 9.6, y5)).color('#ffffff'))  # extiende el lienzo para el texto
    texto(d, EX, EY - 0.4, 'GPIOs: 3.3 V máx., ≤ 12 mA por pin → siempre a través de módulo relé / MOSFET', fs=8.5, color=GRIS)

    # ---------------- Tierra común ----------------
    texto(d, -0.5, 4.6, 'Tierra común en ESTRELLA', fs=11)
    texto(d, -0.5, 4.15, 'Todos los GND (fuente/fusiblera −BUS, buck, ESP32, módulo relé, drivers, sensores) llegan a UNA barra dentro del gabinete de CC.', fs=9.5, color=GRIS)
    texto(d, -0.5, 3.75, 'Retornos de potencia (bomba, peristálticas) por su propio cable a la barra: nunca por el cable de señal de un sensor.', fs=9.5, color=GRIS)
    texto(d, -0.5, 3.35, 'El GND_USB del detector de red CFE queda aislado (optoacoplador). La tierra física (T, 127 V) va al chasis de los gabinetes, no a esta barra.', fs=9.5, color=GRIS)

    # ---------------- Presupuesto de corriente ----------------
    PX, PY = -0.5, -1.2
    rect(d, (PX, PY), (PX + 13.6, PY + 3.7), color=GRIS)
    texto(d, PX + 0.2, PY + 3.35, 'Presupuesto de corriente en 5 V (típicos de hoja de datos; medir en banco, V3)', fs=10)
    filas = ['ESP32 con Wi-Fi activo: 0.08–0.24 A (picos de transmisión)',
             'módulo relé 4 ch: ~0.07–0.09 A por bobina activada → ~0.3–0.36 A con las 4',
             'JSN-SR04T ~0.03 A · placa pH y TDS < 0.01 A c/u · YF-S201 ~0.015 A',
             'total ≈ 0.5–0.7 A → LM2596 (≈ 2 A útiles) con margen; nunca alimentar bombas del 5 V',
             'en 12 V: bomba diafragma 40 W = 3.3 A por F1 (fusiblera), ventilador por F2, NO por el buck']
    for i, t in enumerate(filas):
        texto(d, PX + 0.4, PY + 2.85 - i * 0.55, '• ' + t, fs=9)

    # ---------------- Protecciones ----------------
    QX, QY = 14.0, -1.2
    rect(d, (QX, QY), (QX + 15.0, QY + 3.7), color=AMBAR, ls='--')
    texto(d, QX + 0.2, QY + 3.35, 'Protecciones de este bloque (checklist antes de energizar)', fs=10, color=AMBAR)
    prot = ['F 2 A en la rama del nodo (protege el cable cal. 18) · D1 contra polaridad invertida',
            'C1/C2 absorben el arranque del buck y los huecos cuando arranca la bomba',
            'buck ajustado a 5.0 V en vacío, luego con carga; si baja de 4.75 V, cable más corto/grueso',
            'ESP32 nunca por 3V3 desde fuera; nunca USB + VIN simultáneos; GPIO12 con pull-down 10 kΩ',
            'gabinete IP65 con prensaestopas; cableado de 12 V y de 127 V por gabinetes separados']
    for i, t in enumerate(prot):
        texto(d, QX + 0.4, QY + 2.85 - i * 0.55, '• ' + t, fs=9)

    # ---------------- Leyenda y pie ----------------
    LX, LY = 20.0, 3.3
    rect(d, (LX, LY), (LX + 9.0, LY + 2.2), color=GRIS)
    texto(d, LX + 0.2, LY + 1.85, 'Leyenda', fs=10.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.35)).right(0.8).color(VERDE))
    texto(d, LX + 1.2, LY + 1.35, 'alimentación CC (12 V · 5 V · 3V3)', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 0.85)).right(0.8).linestyle('--').color(GRIS))
    texto(d, LX + 1.2, LY + 0.85, 'opcional', fs=9.5)
    texto(d, LX + 0.2, LY + 0.35, 'C polarizados: + al lado del riel positivo', fs=9.5)

    texto(d, -0.5, -2.1, 'Fuentes: referencia/03-instalacion.md §1.3 · research/electronica-automatizacion.md §2 · research/electrico-respaldo-seguridad.md §5', fs=9, color=GRIS)
    texto(d, -0.5, -2.6, f'{VERSION} · HomeGreen · generado con schemdraw desde hardware/electrico/alimentacion_esp32.py', fs=9, color=GRIS)

postproceso(SALIDA)
print('OK', SALIDA, os.path.getsize(SALIDA), 'bytes')
