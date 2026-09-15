#!/usr/bin/env python3
"""Esquema eléctrico: nodo de riego v1 (Fase 1).

ESP32 DevKit V1 + 4 sensores capacitivos (ADC1) + SHT31 (I2C) + DS18B20 (1-Wire)
+ JSN-SR04T (nivel de tinaco) + módulo relé 4 ch (bomba diafragma 12 V, ventilador,
luces T8 vía relé de potencia 127 V, reserva) + fuente 12 V 5 A + buck 5 V.

Genera docs/assets/diagramas/electrico/nodo-riego-v1.svg con schemdraw 0.23.
Ejecutar:  python3 hardware/electrico/nodo_riego_v1.py
Fuentes de los datos: docs/research/electronica-automatizacion.md,
docs/research/electrico-respaldo-seguridad.md, docs/referencia/03-instalacion.md §1.3.
"""
from __future__ import annotations

import os
import re

import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

# --- Estilo de la wiki (CONVENCIONES §3) -------------------------------------
INK = '#1f2937'      # trazos y texto
VERDE = '#2e7d32'    # alimentación CC
AMBAR = '#b45309'    # 127 V CA / alertas
GRIS = '#6b7280'     # notas secundarias
VERSION = 'v1 · 2026-09'

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, 'docs', 'assets', 'diagramas', 'electrico', 'nodo-riego-v1.svg')


# --- Ayudantes de dibujo ------------------------------------------------------
def texto(d, x, y, s, fs=11, halign='left', color=INK):
    d.add(elm.Label().at((x, y)).label(s, fontsize=fs, halign=halign, color=color))


def caja(d, x, y, w, h, titulo, izq=(), der=(), stub=0.6, fs=10, color=INK,
         titulo_fs=11, titulo_loc='top', sub=None, titulo2=None):
    """Caja de módulo con pines. izq/der: lista de (etiqueta, nombre) de arriba
    a abajo. Devuelve dict nombre -> (x, y) del extremo libre de cada stub."""
    rect(d, (x, y), (x + w, y + h), color=color)
    if titulo_loc == 'top':
        texto(d, x + w / 2, y + h + 0.28, titulo, fs=titulo_fs, halign='center', color=color)
    else:
        texto(d, x + w / 2, y - 0.32, titulo, fs=titulo_fs, halign='center', color=color)
    if sub:
        texto(d, x + w / 2, y + h / 2, sub, fs=9, halign='center', color=GRIS)
    if titulo2:
        texto(d, x + w / 2, y + h + 0.62, titulo2, fs=8.5, halign='center', color=GRIS)
    anclas = {}

    def _pines(lista, lado):
        n = len(lista)
        if n == 0:
            return
        paso = h / (n + 1)
        for i, (etq, nom) in enumerate(lista):
            py = y + h - paso * (i + 1)
            if lado == 'izq':
                d.add(elm.Line().at((x, py)).left(stub).color(color))
                texto(d, x + 0.12, py, etq, fs=fs, halign='left', color=color)
                anclas[nom] = (x - stub, py)
            else:
                d.add(elm.Line().at((x + w, py)).right(stub).color(color))
                texto(d, x + w - 0.12, py, etq, fs=fs, halign='right', color=color)
                anclas[nom] = (x + w + stub, py)

    _pines(izq, 'izq')
    _pines(der, 'der')
    return anclas


def ruta(d, a, b, xm=None, color=INK, ls='-'):
    """Cable ortogonal a -> b con tramo vertical en x = xm."""
    if xm is None:
        xm = (a[0] + b[0]) / 2
    d.add(elm.Line().at(a).to((xm, a[1])).color(color).linestyle(ls))
    d.add(elm.Line().at((xm, a[1])).to((xm, b[1])).color(color).linestyle(ls))
    d.add(elm.Line().at((xm, b[1])).to(b).color(color).linestyle(ls))


def punto(d, p, color=INK):
    d.add(elm.Dot(radius=0.09).at(p).color(color))


def rect(d, c1, c2, color=INK, ls='-'):
    """Rectángulo en coordenadas absolutas (Rect se ancla a (0,0), sin rotación)."""
    d.add(elm.Rect(corner1=c1, corner2=c2).at((0, 0)).theta(0).color(color).linestyle(ls))


def postproceso(path):
    """Fondo blanco explícito y fuente genérica; el SVG abre solo (sin scripts)."""
    with open(path, encoding='utf-8') as f:
        s = f.read()
    s = s.replace('font-family="sans"', 'font-family="sans-serif"')
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    rect = (f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" '
            f'fill="#ffffff"/>')
    i = s.index('>', s.index('<svg')) + 1
    s = s[:i] + rect + s[i:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


# --- Dibujo -------------------------------------------------------------------
with schemdraw.Drawing(file=SALIDA, show=False) as d:
    d.config(unit=2.0, fontsize=11, font='sans-serif', color=INK, lw=1.4, bgcolor='white')

    # Título y subtítulo
    texto(d, -0.5, 18.4, 'Nodo de riego v1 — ESP32 + sensores + relés (Fase 1)', fs=16)
    texto(d, -0.5, 17.75,
          'Rack de microgreens: riego por histéresis, ventilación, luces T8 y nivel de tinaco. '
          'Firmware: firmware/esphome/nodo-riego-v1.yaml', fs=10, color=GRIS)

    # ---------------- ESP32 DevKit V1 (30 pines) ----------------
    X0, Y0, W, H = 11.0, 2.5, 4.6, 10.6
    izq = [('3V3', 'v33'), ('GND', 'gnd'), ('GPIO32 · ADC1_4', 'g32'), ('GPIO33 · ADC1_5', 'g33'),
           ('GPIO34 · ADC1_6', 'g34'), ('GPIO35 · ADC1_7', 'g35'), ('GPIO21 · SDA', 'g21'),
           ('GPIO22 · SCL', 'g22'), ('GPIO4 · 1-Wire', 'g4'), ('GPIO5 · TRIG', 'g5'),
           ('GPIO18 · ECHO', 'g18')]
    # Lado derecho: mismo paso que el izquierdo para que los cables al relé sean rectos
    paso = H / (len(izq) + 1)
    ys = [Y0 + H - paso * (i + 1) for i in range(len(izq))]
    rect(d, (X0, Y0), (X0 + W, Y0 + H))
    texto(d, X0 + W / 2, Y0 + H + 0.28, 'ESP32 DevKit V1 (30 pines) · ESPHome', fs=12, halign='center')
    esp = {}
    for (etq, nom), py in zip(izq, ys):
        d.add(elm.Line().at((X0, py)).left(0.6))
        texto(d, X0 + 0.12, py, etq, fs=9.5)
        esp[nom] = (X0 - 0.6, py)
    der = {'vin': ('VIN (5 V)', ys[0]), 'gndr': ('GND', ys[1]), 'g25': ('GPIO25 · IN1', ys[4]),
           'g26': ('GPIO26 · IN2', ys[5]), 'g27': ('GPIO27 · IN3', ys[6]), 'g14': ('GPIO14 · IN4', ys[7])}
    for nom, (etq, py) in der.items():
        d.add(elm.Line().at((X0 + W, py)).right(0.6))
        texto(d, X0 + W - 0.12, py, etq, fs=9.5, halign='right')
        esp[nom] = (X0 + W + 0.6, py)
    # USB solo para el primer flasheo
    d.add(elm.Line().at((X0 + W / 2, Y0)).down(0.6))
    texto(d, X0 + W / 2, Y0 - 0.85, 'USB: solo flasheo inicial (después OTA).', fs=9,
          halign='center', color=GRIS)
    texto(d, X0 + W / 2, Y0 - 1.2, 'No conectar USB y VIN a la vez.', fs=9,
          halign='center', color=AMBAR)

    # 3V3 y GND del ESP32
    d.add(elm.Vdd().at(esp['v33']).color(VERDE).label('3V3 (≤ 600 mA)', fontsize=9, color=VERDE))
    d.add(elm.Ground().at(esp['gnd']))

    # ---------------- Sensores (columna izquierda) ----------------
    SX, SW, SH = 2.0, 3.6, 1.4
    centros = {'s1': 14.0, 's2': 11.6, 's3': 9.2, 's4': 6.8, 'sht': 4.4, 'ds': 2.0, 'jsn': -0.4}

    def sensor(nombre, cy, titulo, salidas, vcc='3V3', sub=None, titulo2=None):
        a = caja(d, SX, cy - SH / 2, SW, SH, titulo,
                 izq=[(vcc, 'vcc'), ('GND', 'gnd')], der=salidas, fs=9.5, titulo_fs=10, sub=sub,
                 titulo2=titulo2)
        d.add(elm.Vdd().at(a['vcc']).color(VERDE).label(vcc, fontsize=9, color=VERDE))
        d.add(elm.Ground().at(a['gnd']))
        return a

    s1 = sensor('s1', centros['s1'], 'Capacitivo v1.2 · S1 (nivel 1)', [('AOUT', 'out')])
    s2 = sensor('s2', centros['s2'], 'Capacitivo v1.2 · S2 (nivel 2)', [('AOUT', 'out')])
    s3 = sensor('s3', centros['s3'], 'Capacitivo v1.2 · S3 (nivel 3)', [('AOUT', 'out')])
    s4 = sensor('s4', centros['s4'], 'Capacitivo v1.2 · S4 (nivel 4)', [('AOUT', 'out')])
    sht = sensor('sht', centros['sht'], 'SHT31 · T/HR ambiente (I2C 0x44)',
                 [('SDA', 'sda'), ('SCL', 'scl')],
                 titulo2='pull-ups I2C 4.7 kΩ a 3V3 si el módulo no los trae')
    ds = sensor('ds', centros['ds'], 'DS18B20 · T agua tinaco', [('DQ', 'dq')])
    jsn = sensor('jsn', centros['jsn'], 'JSN-SR04T · nivel tinaco', [('TRIG', 'trig'), ('ECHO', 'echo')],
                 vcc='5V')

    # Cables sensor -> ESP32 (tramos verticales escalonados para no cruzar)
    ruta(d, s1['out'], esp['g32'], xm=8.3)
    ruta(d, s2['out'], esp['g33'], xm=7.8)
    ruta(d, s3['out'], esp['g34'], xm=7.3)
    ruta(d, s4['out'], esp['g35'], xm=6.8)
    ruta(d, sht['sda'], esp['g21'], xm=7.0)
    ruta(d, sht['scl'], esp['g22'], xm=7.5)

    # 1-Wire con pull-up 4.7 kΩ
    ruta(d, ds['dq'], esp['g4'], xm=8.0)
    punto(d, (6.5, centros['ds']))
    d.add(elm.Resistor().at((6.5, centros['ds'])).up().length(1.1).label('4.7 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Vdd().at((6.5, centros['ds'] + 1.1)).color(VERDE).label('3V3', fontsize=9, color=VERDE))

    # JSN-SR04T: TRIG directo; ECHO es de 5 V -> divisor 10 k / 20 k a 3.3 V
    ruta(d, jsn['trig'], esp['g5'], xm=8.5)
    ye = jsn['echo'][1]
    d.add(elm.Resistor().at(jsn['echo']).right().length(1.6).label('10 kΩ', fontsize=9, loc='bottom'))
    nodo = (jsn['echo'][0] + 1.6, ye)
    punto(d, nodo)
    d.add(elm.Resistor().at(nodo).down().length(1.3).label('20 kΩ', fontsize=9, loc='bottom'))
    d.add(elm.Ground().at((nodo[0], ye - 1.3)))
    ruta(d, nodo, esp['g18'], xm=9.0)
    texto(d, 9.15, ye + 0.15, 'ECHO 5 V → 3.3 V', fs=8.5, color=GRIS)

    # ---------------- Módulo relé 4 canales ----------------
    RX, RY, RW, RH = 18.0, 4.4, 3.6, 8.5
    rect(d, (RX, RY), (RX + RW, RY + RH))
    texto(d, RX + RW / 2, RY + RH + 0.28, 'Módulo relé 4 ch 5 V optoacoplado', fs=11, halign='center')
    texto(d, RX + RW / 2, RY - 0.35, 'entradas activas en BAJO (IN = 0 → K cerrado)', fs=8.5, halign='center', color=GRIS)
    texto(d, RX + RW / 2, RY - 0.7, 'contactos 10 A / 250 V CA · JD-VCC = VCC (5 V)', fs=8.5, halign='center', color=GRIS)
    rel = {}
    for nom, etq in [('vin', 'VCC 5 V'), ('gndr', 'GND'), ('g25', 'IN1'), ('g26', 'IN2'),
                     ('g27', 'IN3'), ('g14', 'IN4')]:
        py = esp[nom][1]
        d.add(elm.Line().at((RX, py)).left(0.6))
        texto(d, RX + 0.12, py, etq, fs=9.5)
        rel[nom] = (RX - 0.6, py)
    # Contactos a la derecha
    cont = {}
    for i, nom in enumerate(['com1', 'no1', 'com2', 'no2', 'com3', 'no3', 'com4', 'no4']):
        py = 12.0 - i * 1.0
        d.add(elm.Line().at((RX + RW, py)).right(0.6))
        texto(d, RX + RW - 0.12, py, nom.upper(), fs=9.5, halign='right')
        cont[nom] = (RX + RW + 0.6, py)

    # Señales de control ESP32 -> relé (rectas) y alimentación 5 V / GND compartida
    for nom in ['g25', 'g26', 'g27', 'g14']:
        d.add(elm.Line().at(esp[nom]).to(rel[nom]))
    d.add(elm.Line().at(esp['vin']).to(rel['vin']).color(VERDE))
    punto(d, (16.8, esp['vin'][1]), color=VERDE)
    d.add(elm.Line().at(esp['gndr']).to(rel['gndr']))
    punto(d, (16.8, esp['gndr'][1]))
    d.add(elm.Ground().at((16.8, esp['gndr'][1])))

    # ---------------- Cargas de 12 V (K1, K2) ----------------
    def carga_12v(com, no, fus, etiqueta, nota):
        d.add(elm.Vdd().at(com).color(VERDE).label('+12 V', fontsize=9, color=VERDE))
        d.add(elm.Fuse().at(no).right().length(1.6).label(fus, fontsize=9).color(VERDE))
        d.add(elm.Motor().at((no[0] + 1.6, no[1])).right().length(1.6).label(etiqueta, fontsize=9, loc='top'))
        d.add(elm.Ground().at((no[0] + 3.2, no[1])))
        texto(d, no[0] + 3.7, no[1] - 0.3, nota, fs=8.5, color=GRIS)

    carga_12v(cont['com1'], cont['no1'], 'F1 5 A', 'K1 · bomba diafragma 12 V (presostato)',
              'riego por nebulizadores')
    carga_12v(cont['com2'], cont['no2'], 'F2 2 A', 'K2 · ventilador 12 V',
              'histéresis HR > 70 %')

    # ---------------- K3: luces T8 vía relé de potencia 127 V ----------------
    d.add(elm.Vdd().at(cont['com3']).color(VERDE).label('+12 V', fontsize=9, color=VERDE))
    d.add(elm.Fuse().at(cont['no3']).right().length(1.6).label('F3 1 A', fontsize=9).color(VERDE))
    bob = (cont['no3'][0] + 1.6, cont['no3'][1])
    d.add(elm.Inductor2().at(bob).right().length(1.6).label('K5 bobina 12 V', fontsize=9, loc='top'))
    d.add(elm.Ground().at((bob[0] + 1.6, bob[1])))
    texto(d, bob[0] + 2.1, bob[1] - 0.3, 'relé de potencia / contactor 127 V', fs=8.5, color=GRIS)
    # Contacto de K5 en el circuito de 127 V (gabinete separado, ámbar)
    yl = 2.4
    xl = 22.6
    texto(d, xl - 0.3, yl + 1.35, 'L 127 V CA (del contacto GFCI, gabinete de CA)', fs=9, color=AMBAR)
    d.add(elm.Line().at((xl, yl)).right(0.5).color(AMBAR))
    d.add(elm.Fuse().at((xl + 0.5, yl)).right().length(1.5).label('F5 2 A', fontsize=9, color=AMBAR).color(AMBAR))
    d.add(elm.Switch().at((xl + 2.0, yl)).right().length(1.5).label('K5', fontsize=9, loc='bottom', color=AMBAR).color(AMBAR))
    d.add(elm.Lamp().at((xl + 3.5, yl)).right().length(1.5).label('T8 LED 18 W ×8 = 144 W',
                                                                fontsize=9, loc='bottom', color=AMBAR).color(AMBAR))
    d.add(elm.Line().at((xl + 5.0, yl)).right(0.5).color(AMBAR))
    texto(d, xl + 5.6, yl, 'N', fs=9, color=AMBAR)
    d.add(elm.Line().at((bob[0] + 0.8, bob[1] - 0.45)).to((xl + 2.75, yl + 0.45)).linestyle('--').color(GRIS))
    rect(d, (xl - 0.3, yl - 1.0), (xl + 6.2, yl + 1.05), color=AMBAR, ls='--')
    texto(d, xl - 0.3, yl - 1.3, 'gabinete 127 V CA separado · tierra física al chasis metálico', fs=8.5, color=AMBAR)

    # K4 reserva
    d.add(elm.Vdd().at(cont['com4']).color(VERDE).label('+12 V', fontsize=9, color=VERDE))
    d.add(elm.Line().at(cont['no4']).right(1.2).linestyle('--').color(GRIS))
    texto(d, cont['no4'][0] + 1.4, cont['no4'][1] + 0.2, 'K4 reserva: tapete térmico 127 V (dic–feb)', fs=9, color=GRIS)
    texto(d, cont['no4'][0] + 1.4, cont['no4'][1] - 0.2, 'o luz nivel 5; mismo esquema que K3', fs=9, color=GRIS)

    # ---------------- Alimentación (arriba a la derecha) ----------------
    PX, PY = 16.2, 14.6
    gf = caja(d, PX, PY, 3.0, 1.6, 'Contacto GFCI 127 V', der=[('L', 'l'), ('N', 'n'), ('T', 't')],
              fs=9, titulo_fs=10, color=AMBAR)
    texto(d, PX + 1.5, PY + 0.8, 'tapa "in-use"', fs=8.5, halign='center', color=GRIS)
    FX = PX + 4.4
    fu = caja(d, FX, PY, 3.4, 1.6, 'Fuente Steren ELI-1260 12 V 5 A',
              izq=[('L', 'l'), ('N', 'n'), ('T', 't')], der=[('+12 V', 'p'), ('GND', 'g')], fs=9, titulo_fs=10)
    for k in ['l', 'n', 't']:
        d.add(elm.Line().at(gf[k]).to(fu[k]).color(AMBAR))
    # +12 V -> fusible general -> nodo +12 V y buck
    d.add(elm.Fuse().at(fu['p']).right().length(1.6).label('F0 5 A', fontsize=9, loc='bottom').color(VERDE))
    n12 = (fu['p'][0] + 1.6, fu['p'][1])
    punto(d, n12, color=VERDE)
    d.add(elm.Vdd().at(n12).color(VERDE).label('+12 V (a K1–K4)', fontsize=9, color=VERDE))
    d.add(elm.Ground().at(fu['g']))
    BX, BY = n12[0] + 1.0, PY - 0.2
    bk = caja(d, BX, BY, 2.8, 1.6, 'Buck LM2596 12→5 V',
              izq=[('IN+', 'ip'), ('IN−', 'im')], der=[('OUT+', 'op'), ('OUT−', 'om')], fs=9, titulo_fs=10)
    texto(d, BX + 1.4, BY + 0.8, 'ajustar 5.0 V', fs=8.5, halign='center', color=GRIS)
    d.add(elm.Line().at(n12).to(bk['ip']).color(VERDE))
    d.add(elm.Ground().at(bk['im']))
    d.add(elm.Ground().at(bk['om']))
    n5 = (bk['op'][0] + 0.9, bk['op'][1])
    d.add(elm.Line().at(bk['op']).to(n5).color(VERDE))
    punto(d, n5, color=VERDE)
    d.add(elm.Capacitor().at(n5).down().length(1.2).label('470 µF', fontsize=9, loc='bottom').color(VERDE))
    d.add(elm.Ground().at((n5[0], n5[1] - 1.2)))
    # 5 V al nodo compartido VIN / VCC relé (y al JSN-SR04T): pasa por ENCIMA del módulo relé
    y5 = 13.75
    d.add(elm.Line().at(n5).right(0.6).color(VERDE))
    d.add(elm.Line().at((n5[0] + 0.6, n5[1])).to((n5[0] + 0.6, y5)).color(VERDE))
    d.add(elm.Line().at((n5[0] + 0.6, y5)).to((16.8, y5)).color(VERDE))
    d.add(elm.Line().at((16.8, y5)).to((16.8, esp['vin'][1])).color(VERDE))
    texto(d, 19.0, y5 + 0.3, '+5 V → VIN ESP32, VCC módulo relé, JSN-SR04T', fs=9, color=VERDE)
    texto(d, -0.5, 17.1, 'Tierra común: todos los GND (fuente, buck, ESP32, relé, sensores) en UNA barra dentro del gabinete IP65.',
          fs=9.5, color=GRIS)
    texto(d, -0.5, 16.65, 'ADC1 (GPIO32–35) para los capacitivos: ADC2 no funciona con Wi-Fi activo. Sensores con el conector hacia arriba y sellado.',
          fs=9.5, color=GRIS)

    # ---------------- Leyenda y pie ----------------
    LX, LY = 18.0, -2.4
    rect(d, (LX, LY), (LX + 11.0, LY + 3.2), color=GRIS)
    texto(d, LX + 0.2, LY + 2.85, 'Leyenda', fs=10.5)
    d.add(elm.Line().at((LX + 0.2, LY + 2.3)).right(0.8).color(VERDE))
    texto(d, LX + 1.2, LY + 2.3, 'alimentación CC (12 V · 5 V · 3V3)', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.8)).right(0.8).color(AMBAR))
    texto(d, LX + 1.2, LY + 1.8, '127 V CA — solo dentro del gabinete de CA, aguas abajo del GFCI', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.3)).right(0.8))
    texto(d, LX + 1.2, LY + 1.3, 'señal / control 3.3 V', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 0.8)).right(0.8).linestyle('--').color(GRIS))
    texto(d, LX + 1.2, LY + 0.8, 'enlace mecánico / opcional', fs=9.5)
    texto(d, LX + 0.2, LY + 0.3, 'F = fusible por rama · K = relé · valores de fusible protegen el cable, no la carga', fs=9.5)

    texto(d, -0.5, -3.3, 'Fuentes: research/electronica-automatizacion.md · research/electrico-respaldo-seguridad.md · referencia/03-instalacion.md §1.3', fs=9, color=GRIS)
    texto(d, -0.5, -3.8, f'{VERSION} · HomeGreen · generado con schemdraw desde hardware/electrico/nodo_riego_v1.py', fs=9, color=GRIS)

postproceso(SALIDA)
print('OK', SALIDA, os.path.getsize(SALIDA), 'bytes')
