#!/usr/bin/env python3
"""Esquema eléctrico: nodo NFT v2 (Fase 2) — dosificación pH/EC y continuidad.

ESP32 DevKit V1 + placa pH (BNC, ADC1) + TDS/EC (ADC1) + DS18B20 (1-Wire) + YF-S201
(pulsos) + 3 peristálticas 12 V vía MOSFET + 2 solenoides 12 V NC + detector de red CFE
(optoacoplador desde cargador USB) + divisor 47k/10k para el voltaje de batería
+ relé 2 ch para las bombas principal (NC) / respaldo (NO) del bus DC.

Genera docs/assets/diagramas/electrico/nodo-nft-v2.svg con schemdraw 0.23.
Ejecutar:  python3 hardware/electrico/nodo_nft_v2.py
Fuentes: docs/research/electrico-respaldo-seguridad.md §5, docs/research/electronica-automatizacion.md §3,
docs/referencia/03-instalacion.md §2.2–2.3.
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
SALIDA = os.path.join(RAIZ, 'docs', 'assets', 'diagramas', 'electrico', 'nodo-nft-v2.svg')


# --- Ayudantes (idénticos en los 5 scripts) -----------------------------------
def texto(d, x, y, s, fs=11, halign='left', color=INK):
    d.add(elm.Label().at((x, y)).label(s, fontsize=fs, halign=halign, color=color))


def rect(d, c1, c2, color=INK, ls='-'):
    d.add(elm.Rect(corner1=c1, corner2=c2).at((0, 0)).theta(0).color(color).linestyle(ls))


def punto(d, p, color=INK):
    d.add(elm.Dot(radius=0.09).at(p).color(color))


def caja(d, x, y, w, h, titulo, izq=(), der=(), abajo=(), stub=0.6, fs=10, color=INK,
         titulo_fs=11, sub=None, titulo2=None):
    """Caja de módulo con pines (izq/der de arriba a abajo; abajo de izquierda a derecha).
    Devuelve dict nombre -> (x, y) del extremo libre del stub."""
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

    texto(d, -0.5, 17.6, 'Nodo NFT v2 — pH/EC, dosificación y continuidad (Fase 2)', fs=16)
    texto(d, -0.5, 16.95,
          'Alimentado desde el bus de batería (bus-dc-first.svg): sigue midiendo y avisando durante un corte de CFE. '
          'Firmware: firmware/esphome/nodo-nft-v2.yaml', fs=10, color=GRIS)
    texto(d, -0.5, 16.2, 'GPIO34/35/36 son solo entrada (sin pull-up interno). GPIO12 es pin de arranque (strapping): '
          'pull-down 10 kΩ a GND obligatorio o el ESP32 no arranca.', fs=9.5, color=GRIS)
    texto(d, -0.5, 15.75, 'Sondas pH y TDS en el RETORNO del NFT; peristálticas dosifican al depósito junto a la succión de la bomba. '
          'Filtro RC 1 kΩ / 100 nF en cada entrada ADC.', fs=9.5, color=GRIS)

    # ---------------- ESP32 ----------------
    X0, Y0, W, H = 10.2, 1.0, 6.2, 13.0
    paso = H / 10
    ys = [Y0 + H - paso * (i + 1) for i in range(9)]
    rect(d, (X0, Y0), (X0 + W, Y0 + H))
    texto(d, X0 + W / 2, Y0 + H + 0.28, 'ESP32 DevKit V1 (30 pines) · ESPHome', fs=12, halign='center')
    izq = [('3V3', 'v33'), ('GND', 'gnd'), ('GPIO34 · ADC1_6 pH', 'g34'), ('GPIO35 · ADC1_7 TDS', 'g35'),
           ('GPIO36 · ADC1_0 V_bat', 'g36'), ('GPIO4 · 1-Wire', 'g4'), ('GPIO27 · pulsos', 'g27'),
           ('GPIO23 · red CFE', 'g23')]
    der = [('VIN (5 V)', 'vin'), ('GND', 'gndr'), ('GPIO25 · A', 'g25'), ('GPIO26 · B', 'g26'),
           ('GPIO33 · pH−', 'g33'), ('GPIO12 · sol. llenado', 'g12'), ('GPIO13 · sol. purga', 'g13'),
           ('GPIO32 · K1 principal', 'g32'), ('GPIO14 · K2 respaldo', 'g14')]
    esp = {}
    for (etq, nom), py in zip(izq, ys):
        d.add(elm.Line().at((X0, py)).left(0.6))
        texto(d, X0 + 0.12, py, etq, fs=9.5)
        esp[nom] = (X0 - 0.6, py)
    for (etq, nom), py in zip(der, ys):
        d.add(elm.Line().at((X0 + W, py)).right(0.6))
        texto(d, X0 + W - 0.12, py, etq, fs=9.5, halign='right')
        esp[nom] = (X0 + W + 0.6, py)
    d.add(elm.Line().at((X0 + W / 2, Y0)).down(0.5))
    texto(d, X0 + W / 2, Y0 - 0.8, 'USB: solo flasheo inicial (después OTA). No conectar USB y VIN a la vez.',
          fs=8.5, halign='center', color=AMBAR)
    d.add(elm.Vdd().at(esp['v33']).color(VERDE).label('3V3 (≤ 600 mA)', fontsize=9, color=VERDE))
    d.add(elm.Ground().at(esp['gnd']))

    # ---------------- Entradas (columna izquierda) ----------------
    SX, SW, SH = 2.0, 3.6, 1.4

    def sensor(cy, titulo, salidas, vcc='3V3', titulo2=None, abajo=()):
        a = caja(d, SX, cy - SH / 2, SW, SH, titulo, izq=[(vcc, 'vcc'), ('GND', 'gnd')], der=salidas,
                 abajo=abajo, fs=9.5, titulo_fs=10, titulo2=titulo2)
        d.add(elm.Vdd().at(a['vcc']).color(VERDE).label(vcc, fontsize=9, color=VERDE))
        d.add(elm.Ground().at(a['gnd']))
        return a

    def filtro_rc(a, b, xm):
        """Serie 1 kΩ + 100 nF a GND antes del ADC."""
        d.add(elm.Resistor().at(a).right().length(1.4).label('1 kΩ', fontsize=9))
        n = (a[0] + 1.4, a[1])
        punto(d, n)
        d.add(elm.Capacitor().at(n).down().length(1.0).label('100 nF', fontsize=9, loc='bottom'))
        d.add(elm.Ground().at((n[0], n[1] - 1.0)))
        ruta(d, n, b, xm=xm)

    # pH
    ph = sensor(13.6, 'Placa pH PH-4502C (o DFRobot Gravity)', [('Po', 'po')], vcc='5V',
                abajo=[('BNC', 'bnc')])
    d.add(elm.Dot(open=True, radius=0.16).at(ph['bnc']))
    texto(d, ph['bnc'][0] + 0.35, ph['bnc'][1], 'BNC ← electrodo E201 (retorno)', fs=8.5, color=GRIS)
    filtro_rc(ph['po'], esp['g34'], xm=8.6)
    texto(d, 5.9, 14.62, 'Po ≤ 3.1 V: ajustar offset con buffer 4.01', fs=8, color=GRIS)

    # TDS / EC
    tds = sensor(10.8, 'TDS SEN0244 (DFRobot, 0–2.3 V)', [('AOUT', 'ao')], vcc='3V3', abajo=[('sonda', 'sd')])
    d.add(elm.Dot(open=True, radius=0.16).at(tds['sd']))
    texto(d, tds['sd'][0] + 0.35, tds['sd'][1], 'sonda TDS (retorno)', fs=8.5, color=GRIS)
    texto(d, tds['sd'][0] + 0.35, tds['sd'][1] - 0.35, 'calibrar en mS/cm', fs=8.5, color=GRIS)
    filtro_rc(tds['ao'], esp['g35'], xm=8.1)

    # Divisor de voltaje de batería 47k/10k -> GPIO36 (x5.7 en firmware)
    xv, yv = 0.8, 8.0
    d.add(elm.Vdd().at((xv, yv + 1.2)).color(VERDE).label('BUS 12.8 V (F3)', fontsize=9, color=VERDE))
    d.add(elm.Resistor().at((xv, yv + 1.2)).down().length(1.2).label('47 kΩ', fontsize=9, loc='left'))
    punto(d, (xv, yv))
    d.add(elm.Resistor().at((xv, yv)).down().length(1.2).label('10 kΩ', fontsize=9, loc='left'))
    d.add(elm.Ground().at((xv, yv - 1.2)))
    d.add(elm.Line().at((xv, yv)).to((6.1, yv)))
    punto(d, (6.1, yv))
    d.add(elm.Capacitor().at((6.1, yv)).down().length(1.0).label('100 nF', fontsize=9, loc='bottom'))
    d.add(elm.Ground().at((6.1, yv - 1.0)))
    ruta(d, (6.1, yv), esp['g36'], xm=7.6)
    texto(d, 1.6, yv + 0.75, 'Divisor V_bat: 14.6 V → 2.56 V', fs=8.5, color=GRIS)
    texto(d, 1.6, yv + 0.4, '(×5.7 en firmware; atenuación 12 dB)', fs=8.5, color=GRIS)

    # DS18B20
    ds = sensor(5.2, 'DS18B20 · T solución (depósito)', [('DQ', 'dq')])
    ruta(d, ds['dq'], esp['g4'], xm=7.0)
    punto(d, (6.5, 5.2))
    d.add(elm.Resistor().at((6.5, 5.2)).up().length(1.1).label('4.7 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Vdd().at((6.5, 6.3)).color(VERDE).label('3V3', fontsize=9, color=VERDE))

    # YF-S201 (salida Hall a 5 V -> divisor 10k/20k)
    yf = sensor(2.4, 'YF-S201 · flujo NFT (≈450 pulsos/L)', [('SIG', 'sig')], vcc='5V')
    d.add(elm.Resistor().at(yf['sig']).right().length(1.4).label('10 kΩ', fontsize=9))
    n = (yf['sig'][0] + 1.4, yf['sig'][1])
    punto(d, n)
    d.add(elm.Resistor().at(n).down().length(1.2).label('20 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Ground().at((n[0], n[1] - 1.2)))
    ruta(d, n, esp['g27'], xm=7.5)
    texto(d, 7.7, 2.65, 'SIG 5 V → 3.3 V', fs=8.5, color=GRIS)

    # Detector de red CFE: cargador USB del patio -> optoacoplador -> GPIO23 (INPUT_PULLDOWN)
    usb = caja(d, 0.6, -1.3, 3.2, 1.4, 'Cargador USB 5 V al contacto GFCI',
               der=[('+5 V', 'p'), ('GND_USB', 'g')], fs=9.5, titulo_fs=10,
               titulo2='detector de red CFE: NO unir GND_USB al nodo')
    d.add(elm.Resistor().at(usb['p']).right().length(1.3).label('470 Ω', fontsize=9))
    opto = d.add(elm.Optocoupler().at((6.7, -0.6)).color(INK))
    ruta(d, (usb['p'][0] + 1.3, usb['p'][1]), (opto.anode[0], opto.anode[1]), xm=opto.anode[0] - 0.3)
    ruta(d, usb['g'], (opto.cathode[0], opto.cathode[1]), xm=opto.cathode[0] - 0.3)
    oc = ((opto.anode[0] + opto.collector[0]) / 2, min(opto.cathode[1], opto.emitter[1]) - 0.45)
    texto(d, oc[0], oc[1], 'PC817', fs=9, halign='center', color=GRIS)
    d.add(elm.Line().at(opto.collector).up(0.4))
    d.add(elm.Vdd().at((opto.collector[0], opto.collector[1] + 0.4)).color(VERDE).label('3V3', fontsize=9, color=VERDE))
    ne = (opto.emitter[0] + 0.6, opto.emitter[1])
    d.add(elm.Line().at(opto.emitter).to(ne))
    punto(d, ne)
    d.add(elm.Resistor().at(ne).down().length(1.2).label('10 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Ground().at((ne[0], ne[1] - 1.2)))
    ruta(d, ne, esp['g23'], xm=8.0)
    texto(d, 8.2, opto.emitter[1] + 0.35, 'con 127 V presente → GPIO23 = 1', fs=8.5, color=GRIS)

    # ---------------- Salidas (derecha) ----------------
    # Driver MOSFET x5 (canal típico detallado abajo)
    DX, DY, DW, DH = 18.0, 4.4, 3.4, 6.2
    rect(d, (DX, DY), (DX + DW, DY + DH))
    texto(d, DX + DW / 2, DY + DH + 0.28, 'Driver MOSFET ×5 (canal típico abajo)', fs=11, halign='center')
    texto(d, DX + DW / 2, DY + 0.18, 'GND → barra común', fs=8, halign='center', color=GRIS)
    canales = [('g25', 'IN_A', 'OUT_A', 'motor', 'Peristáltica A (12 V)'),
               ('g26', 'IN_B', 'OUT_B', 'motor', 'Peristáltica B (12 V)'),
               ('g33', 'IN_pH', 'OUT_pH', 'motor', 'Peristáltica pH− (12 V)'),
               ('g12', 'IN_S1', 'OUT_S1', 'sol', 'Solenoide llenado ½" NC 12 V'),
               ('g13', 'IN_S2', 'OUT_S2', 'sol', 'Solenoide purga ½" NC 12 V')]
    XR = 24.6  # riel +12 V de actuadores
    for nom, ein, eout, tipo, etq in canales:
        py = esp[nom][1]
        d.add(elm.Line().at((DX, py)).left(0.6))
        texto(d, DX + 0.12, py, ein, fs=9.5)
        d.add(elm.Line().at(esp[nom]).to((DX - 0.6, py)))
        d.add(elm.Line().at((DX + DW, py)).right(0.6))
        texto(d, DX + DW - 0.12, py, eout, fs=9.5, halign='right')
        o = (DX + DW + 0.6, py)
        if tipo == 'motor':
            d.add(elm.Motor().at(o).right().length(1.8))
        else:
            d.add(elm.Inductor2().at(o).right().length(1.8))
        texto(d, o[0] + 0.9, py + 0.52, etq, fs=8.5, halign='center')
        d.add(elm.Line().at((o[0] + 1.8, py)).to((XR, py)).color(VERDE))
        punto(d, (XR, py), color=VERDE)
    # pull-down obligatorio en GPIO12 (strapping)
    g12 = esp['g12']
    punto(d, (g12[0] + 0.6, g12[1]))
    d.add(elm.Resistor().at((g12[0] + 0.6, g12[1])).down().length(1.0).label('10 kΩ', fontsize=8.5, loc='bottom').color(AMBAR))
    d.add(elm.Ground().at((g12[0] + 0.6, g12[1] - 1.0)))
    d.add(elm.Line().at((XR, esp['g13'][1])).to((XR, esp['g25'][1] + 0.5)).color(VERDE))
    d.add(elm.Vdd().at((XR, esp['g25'][1] + 0.5)).color(VERDE).label('+12 V · F4 5 A (fusiblera)', fontsize=9, color=VERDE))
    texto(d, XR + 0.4, esp['g25'][1], 'A y B: sales; pH−: AquAcid', fs=8.5, color=GRIS)
    texto(d, XR + 0.4, esp['g12'][1], 'NC: sin energía = cerrada', fs=8.5, color=GRIS)
    texto(d, XR + 0.4, esp['g13'][1], '(un corte no vacía el tinaco)', fs=8.5, color=GRIS)

    # Relé 2 ch para K1 (principal, NC) y K2 (respaldo, NO) del bus DC
    RX, RY, RW, RH = 18.0, 1.7, 3.4, 2.2
    rect(d, (RX, RY), (RX + RW, RY + RH))
    texto(d, RX + RW / 2, RY + RH + 0.28, 'Módulo relé 2 ch 5 V (bombas NFT)', fs=10.5, halign='center')
    for nom, ein, eout, etq1, etq2 in [
            ('g32', 'IN1', 'K1 NC', '→ bomba principal 12 V por contacto NC:', 'sin ESP32 o GPIO32 = 0 → bomba ON (fail-safe)'),
            ('g14', 'IN2', 'K2 NO', '→ bomba respaldo 12 V por contacto NO:', 'GPIO14 = 1 → respaldo ON')]:
        py = esp[nom][1]
        d.add(elm.Line().at((RX, py)).left(0.6))
        texto(d, RX + 0.12, py, ein, fs=9.5)
        d.add(elm.Line().at(esp[nom]).to((RX - 0.6, py)))
        d.add(elm.Line().at((RX + RW, py)).right(0.6))
        texto(d, RX + RW - 0.12, py, eout, fs=9.5, halign='right')
        d.add(elm.Line().at((RX + RW + 0.6, py)).right(1.0).linestyle('--').color(GRIS))
        texto(d, RX + RW + 1.8, py + 0.2, etq1, fs=8.5, color=GRIS)
        texto(d, RX + RW + 1.8, py - 0.2, etq2, fs=8.5, color=GRIS)
    texto(d, RX + RW + 1.8, RY - 0.1, 'contactos y fusibles de bomba: ver bus-dc-first.svg', fs=8.5, color=GRIS)
    d.add(elm.Line().at((RX + 1.0, RY)).down(0.5))
    d.add(elm.Vdd().at((RX + 1.0, RY - 0.5)).color(VERDE).label('5V', fontsize=9, color=VERDE).flip())
    texto(d, RX + 1.0, RY + 0.22, 'VCC', fs=9, halign='center')
    d.add(elm.Line().at((RX + 2.4, RY)).down(0.5))
    d.add(elm.Ground().at((RX + 2.4, RY - 0.5)))
    texto(d, RX + 2.4, RY + 0.22, 'GND', fs=9, halign='center')

    # ---------------- Alimentación (arriba a la derecha) ----------------
    PX, PY = 18.0, 14.2
    d.add(elm.Vdd().at((PX, PY)).color(VERDE).label('BUS 12.8 V', fontsize=9, color=VERDE))
    texto(d, PX - 0.2, PY + 1.1, 'desde la fusiblera del bus DC, F3 (bus-dc-first.svg)', fs=8.5, halign='right', color=GRIS)
    d.add(elm.Fuse().at((PX, PY)).right().length(1.6).label('F3 2 A', fontsize=9, loc='bottom').color(VERDE))
    n12 = (PX + 1.6, PY)
    bk = caja(d, n12[0] + 0.8, PY - 0.9, 2.8, 1.6, 'Buck LM2596 12→5 V',
              izq=[('IN+', 'ip'), ('IN−', 'im')], der=[('OUT+', 'op'), ('OUT−', 'om')], fs=9, titulo_fs=10)
    texto(d, n12[0] + 2.2, PY - 0.1, 'ajustar 5.0 V', fs=8.5, halign='center', color=GRIS)
    ruta(d, n12, bk['ip'], xm=n12[0] + 0.1, color=VERDE)
    d.add(elm.Ground().at(bk['im']))
    d.add(elm.Ground().at(bk['om']))
    n5 = (bk['op'][0] + 0.9, bk['op'][1])
    d.add(elm.Line().at(bk['op']).to(n5).color(VERDE))
    punto(d, n5, color=VERDE)
    d.add(elm.Capacitor().at(n5).down().length(1.2).label('470 µF', fontsize=9, loc='bottom').color(VERDE))
    d.add(elm.Ground().at((n5[0], n5[1] - 1.2)))
    d.add(elm.Line().at(n5).right(0.6).color(VERDE))
    d.add(elm.Line().at((n5[0] + 0.6, n5[1])).to((n5[0] + 0.6, esp['vin'][1])).color(VERDE))
    d.add(elm.Line().at((n5[0] + 0.6, esp['vin'][1])).to(esp['vin']).color(VERDE))
    texto(d, 17.2, esp['vin'][1] + 0.3, '+5 V → VIN ESP32, VCC relé 2 ch, placa pH, YF-S201', fs=9, color=VERDE)
    d.add(elm.Ground().at(esp['gndr']))

    # ---------------- Canal típico del driver ----------------
    CX, CY = 12.0, -4.4
    texto(d, CX, CY - 2.2, 'Canal típico del driver (×5): MOSFET de nivel lógico IRLZ44N o módulo D4184', fs=10)
    texto(d, CX, CY + 0.15, 'IN (GPIO)', fs=9)
    d.add(elm.Resistor().at((CX + 1.3, CY)).right().length(1.4).label('220 Ω', fontsize=9))
    g = (CX + 2.7, CY)
    punto(d, g)
    d.add(elm.Resistor().at(g).down().length(1.2).label('10 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Ground().at((g[0], g[1] - 1.2)))
    q = d.add(elm.NFet().anchor('gate').at(g).color(INK))
    d.add(elm.Ground().at(q.source))
    d.add(elm.Motor().at(q.drain).up().length(1.6))
    texto(d, q.drain[0] - 0.7, q.drain[1] + 0.8, 'carga 12 V', fs=9, halign='right')
    top = (q.drain[0], q.drain[1] + 1.6)
    d.add(elm.Line().at(top).right(1.2).color(VERDE))
    d.add(elm.Line().at(q.drain).right(1.2))
    d.add(elm.Diode().at((q.drain[0] + 1.2, q.drain[1])).up().length(1.6))
    texto(d, q.drain[0] + 1.6, q.drain[1] + 0.8, 'D 1N5819 (flyback)', fs=9)
    d.add(elm.Line().at(top).up(0.3).color(VERDE))
    d.add(elm.Vdd().at((top[0], top[1] + 0.3)).color(VERDE).label('+12 V (F4)', fontsize=9, color=VERDE))

    # ---------------- Leyenda y pie ----------------
    LX, LY = -0.5, -6.6
    rect(d, (LX, LY), (LX + 10.6, LY + 3.2), color=GRIS)
    texto(d, LX + 0.2, LY + 2.85, 'Leyenda', fs=10.5)
    d.add(elm.Line().at((LX + 0.2, LY + 2.3)).right(0.8).color(VERDE))
    texto(d, LX + 1.2, LY + 2.3, 'alimentación CC desde el bus de batería (12.8 V · 5 V · 3V3)', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.8)).right(0.8))
    texto(d, LX + 1.2, LY + 1.8, 'señal / control 3.3 V', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.3)).right(0.8).linestyle('--').color(GRIS))
    texto(d, LX + 1.2, LY + 1.3, 'contacto de relé / referencia a otro esquema', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 0.8)).right(0.8).color(AMBAR))
    texto(d, LX + 1.2, LY + 0.8, 'componente obligatorio de seguridad (pull-down GPIO12)', fs=9.5)
    texto(d, LX + 0.2, LY + 0.3, 'F = fusible (fusiblera del bus) · K = relé · NC/NO = reposo cerrado/abierto', fs=9.5)

    texto(d, -0.5, -7.5, 'Fuentes: research/electrico-respaldo-seguridad.md §5 · research/electronica-automatizacion.md §3 · referencia/03-instalacion.md §2.2–2.3', fs=9, color=GRIS)
    texto(d, -0.5, -8.0, f'{VERSION} · HomeGreen · generado con schemdraw desde hardware/electrico/nodo_nft_v2.py', fs=9, color=GRIS)

postproceso(SALIDA)
print('OK', SALIDA, os.path.getsize(SALIDA), 'bytes')
