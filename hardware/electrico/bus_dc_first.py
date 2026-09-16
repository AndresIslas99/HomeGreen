#!/usr/bin/env python3
"""Esquema eléctrico: bus "DC-first" de continuidad del NFT (Fase 2).

CFE 127 V → breaker GFCI → cargador LiFePO4 (o controlador EPEVER con panel 100 W)
→ batería LiFePO4 12.8 V 100 Ah SIEMPRE en paralelo → fusible principal + seccionador
→ fusiblera → bomba principal (K1 NC) + bomba respaldo (K2 NO) → nodo NFT ESP32.

Genera docs/assets/diagramas/electrico/bus-dc-first.svg con schemdraw 0.23.
Ejecutar:  python3 hardware/electrico/bus_dc_first.py
Fuentes: docs/research/electrico-respaldo-seguridad.md §2–3, §6; docs/referencia/03-instalacion.md §2.3.
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
SALIDA = os.path.join(RAIZ, 'docs', 'assets', 'diagramas', 'electrico', 'bus-dc-first.svg')


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

    texto(d, -0.5, 17.6, 'Bus DC-first — continuidad de la bomba NFT ante cortes de CFE (Fase 2)', fs=16)
    texto(d, -0.5, 16.95, 'Topología de DC-UPS: la batería está SIEMPRE en paralelo con el cargador; el corte de CFE no se conmuta, no se nota. '
          'El fail-safe es físico, no de software.', fs=10, color=GRIS)
    texto(d, -0.5, 16.2, 'Autonomía (fuente): bomba 12 V de 40 W = 3.3 A → 12 h = 480 Wh ≈ 38–40 Ah. LiFePO4 100 Ah al 90 % DoD ≈ 28–30 h continuas; '
          'modo 15 min ON / 15 min OFF ≈ 2.5 días.', fs=9.5, color=GRIS)
    texto(d, -0.5, 15.75, 'Panel 100 W ≈ 450–500 Wh/día (CDMX 5.0–5.5 h solares pico) < 960 Wh/día de la bomba 24/7: el panel FLOTA la batería, no sostiene la operación.',
          fs=9.5, color=GRIS)
    texto(d, -0.5, 14.9, 'En casa (otro circuito): UPS DataShield DS-600 → router + cerebro HA. Sin internet no hay alarmas; el agua NO depende de HA.',
          fs=9.5, color=AMBAR)

    # ---------------- Lado CA (ámbar) ----------------
    yca = 12.6
    texto(d, -0.5, yca + 0.45, 'CFE 127 V CA', fs=10, color=AMBAR)
    d.add(elm.Line().at((-0.5, yca)).right(2.1).color(AMBAR))
    d.add(elm.Breaker().at((1.6, yca)).right().length(2.0).color(AMBAR)
          .label('QO120GFI 20 A (GFCI) · centro de carga', fontsize=8.5, loc='bottom', color=AMBAR))
    d.add(elm.Line().at((3.6, yca)).right(1.0).color(AMBAR))
    ct = caja(d, 4.6, yca - 0.8, 3.2, 1.6, 'Contacto WR + tapa "in-use"', izq=[('', 'i')], der=[('', 'o')],
              color=AMBAR, titulo_fs=10, sub='patio · intemperie')
    d.add(elm.Line().at(ct['o']).right(0.6).color(AMBAR))
    cg = caja(d, 9.0, yca - 0.8, 3.6, 1.6, 'Cargador LiFePO4 14.6 V · 10–20 A',
              izq=[('CA', 'ca')], der=[('B+', 'bp'), ('B−', 'bm')], color=INK, titulo_fs=10,
              titulo2='absorción 14.4–14.6 V · flotación ≤ 13.6 V')
    d.add(elm.Line().at((ct['o'][0] + 0.6, yca)).to(cg['ca']).color(AMBAR))
    d.add(elm.Ground().at(cg['bm']))

    # ---------------- Nodo +BUS y fusiblera ----------------
    NB = (13.2, 8.0)
    FX, FY, FW, FH = 14.4, 2.0, 2.6, 11.4
    rect(d, (FX, FY), (FX + FW, FY + FH))
    texto(d, FX + FW / 2, FY + FH + 0.28, 'Fusiblera 6 vías 12 V', fs=11, halign='center')
    texto(d, FX + FW / 2, FY + FH + 0.62, '(gabinete IP65 de CC)', fs=8.5, halign='center', color=GRIS)
    d.add(elm.Line().at((FX, 8.0)).left(0.6).color(VERDE))
    texto(d, FX + 0.12, 8.0, '+BUS', fs=9.5)
    d.add(elm.Line().at(NB).to((FX - 0.6, 8.0)).color(VERDE))
    punto(d, NB, color=VERDE)
    d.add(elm.Line().at((FX + FW / 2, FY)).down(0.6))
    d.add(elm.Ground().at((FX + FW / 2, FY - 0.6)))
    texto(d, FX + FW / 2, FY + 0.22, '−BUS', fs=9.5, halign='center')
    texto(d, FX + FW / 2 + 0.5, FY - 0.9, 'barra negativa común (batería, cargador, controlador, cargas)', fs=8.5, color=GRIS)

    # Cargador -> +BUS
    ruta(d, cg['bp'], NB, xm=NB[0], color=VERDE)

    # ---------------- Solar opcional ----------------
    ysol = 9.6
    rect(d, (-0.5, 8.0), (12.4, 11.0), color=GRIS, ls='--')
    texto(d, -0.3, 8.25, 'OPCIONAL (Fase 2.5, +$1,650 aprox.): el controlador hace de cargador; un corte diurno se vuelve sostenible', fs=8.5, color=GRIS)
    d.add(elm.Solar().at((0.4, ysol)).right().length(2.0).label('Panel 100 W Ugreen 15113 (19 V)', fontsize=9, loc='bottom'))
    ls = caja(d, 4.0, ysol - 0.8, 3.8, 1.6, 'EPEVER LS2024B PWM 20 A',
              izq=[('PV+', 'pvp'), ('PV−', 'pvm')], der=[('BAT+', 'bp'), ('BAT−', 'bm')], titulo_fs=10,
              sub='perfil LiFePO4')
    d.add(elm.Line().at((2.4, ysol)).to(ls['pvp']).color(VERDE))
    ruta(d, (0.4, ysol), ls['pvm'], xm=0.4 - 0.0, color=INK)
    d.add(elm.Ground().at(ls['bm']))
    ruta(d, ls['bp'], NB, xm=12.6, color=VERDE)
    punto(d, (12.6, 8.0), color=VERDE)

    # ---------------- Batería ----------------
    bx, by = 3.8, 3.4
    d.add(elm.Battery().at((bx, by + 2.2)).down().length(2.2).color(INK))  # placa larga (+) arriba
    texto(d, bx - 0.45, by + 2.2, '+', fs=12)
    texto(d, bx - 0.45, by + 0.05, '−', fs=12)
    texto(d, bx + 0.5, by + 1.55, 'LiFePO4 12.8 V 100 Ah', fs=10)
    texto(d, bx + 0.5, by + 1.15, 'Epcom LI100A12PRO ($4,459)', fs=9, color=GRIS)
    texto(d, bx + 0.5, by + 0.8, 'BMS interno (corte por bajo V)', fs=8.5, color=GRIS)
    d.add(elm.Ground().at((bx, by)))
    d.add(elm.Line().at((bx, by + 2.2)).up(0.8).color(VERDE))
    d.add(elm.Fuse().at((bx, by + 3.0)).right().length(2.0).color(VERDE)
          .label('F0 30 A (ANL/MIDI)', fontsize=9, loc='top').label('≤ 30 cm del borne +', fontsize=8.5, loc='bottom', color=GRIS))
    d.add(elm.Switch().at((bx + 2.0, by + 3.0)).right().length(2.0).color(VERDE)
          .label('S1 seccionador (mantenimiento)', fontsize=9, loc='top'))
    ruta(d, (bx + 4.0, by + 3.0), NB, xm=12.0, color=VERDE)
    punto(d, (12.0, 8.0), color=VERDE)
    texto(d, 6.2, 5.6, 'SIEMPRE en paralelo: cero conmutación', fs=9.5, color=VERDE)
    texto(d, 6.2, 5.2, 'HA cicla la bomba 15/15 min si V_bat < 12.9 V en corte', fs=8.5, color=GRIS)

    # ---------------- Salidas de la fusiblera ----------------
    salidas = [('F1 10 A', 'bomba1'), ('F2 10 A', 'bomba2'), ('F3 2 A', 'nodo'),
               ('F4 5 A', 'actuadores'), ('F5 2 A', 'reserva'), ('F6', 'libre')]
    ysal = {}
    for i, (etq, nom) in enumerate(salidas):
        py = FY + FH - FH / 7 * (i + 1)
        ysal[nom] = py
        d.add(elm.Line().at((FX + FW, py)).right(0.5).color(VERDE))
        texto(d, FX + FW - 0.12, py, etq.split()[0], fs=9.5, halign='right')
        d.add(elm.Fuse().at((FX + FW + 0.5, py)).right().length(1.6).color(VERDE).label(etq, fontsize=9, loc='top'))
    XO = FX + FW + 2.1  # fin de cada fusible

    # Bombas con relevadores de transferencia K1 (NC) y K2 (NO)
    y1 = ysal['bomba1']
    d.add(elm.Switch(nc=True).at((XO, y1)).right().length(1.8).label('K1 (NC)', fontsize=9, loc='bottom'))
    d.add(elm.Motor().at((XO + 1.8, y1)).right().length(1.8).label('Bomba principal 12 V 40–60 W · 24/7', fontsize=9, loc='top'))
    d.add(elm.Ground().at((XO + 3.6, y1)))
    texto(d, XO + 4.1, y1 - 0.05, 'sin ESP32 o GPIO32 = 0 → bomba ON', fs=8.5, color=GRIS)
    texto(d, XO + 4.1, y1 - 0.45, 'bobinas K1/K2 ← relé 2 ch del nodo NFT; contactos ≥ 10 A', fs=8.5, color=GRIS)
    y2 = ysal['bomba2']
    d.add(elm.Switch().at((XO, y2)).right().length(1.8).label('K2 (NO)', fontsize=9, loc='bottom'))
    d.add(elm.Motor().at((XO + 1.8, y2)).right().length(1.8).label('Bomba respaldo 12 V (idéntica)', fontsize=9, loc='top'))
    d.add(elm.Ground().at((XO + 3.6, y2)))
    texto(d, XO + 4.1, y2 - 0.05, 'GPIO14 = 1 → respaldo ON (sin flujo en YF-S201)', fs=8.5, color=GRIS)

    # Nodo NFT
    y3 = ysal['nodo']
    rect(d, (XO + 0.6, y3 - 0.6), (XO + 5.0, y3 + 0.6))
    texto(d, XO + 2.8, y3 - 0.92, 'Nodo NFT ESP32 + buck 5 V (nodo-nft-v2.svg)', fs=10, halign='center')
    d.add(elm.Line().at((XO + 0.6, y3)).left(0.6).color(VERDE))
    texto(d, XO + 0.72, y3, '+12.8 V', fs=9.5)
    d.add(elm.Line().at((XO + 5.0, y3)).right(0.6))
    texto(d, XO + 4.88, y3, 'GND', fs=9.5, halign='right')
    d.add(elm.Ground().at((XO + 5.6, y3)))
    texto(d, XO + 6.2, y3 + 0.2, 'siempre vivo: mide V_bat, flujo y red CFE;', fs=8.5, color=GRIS)
    texto(d, XO + 6.2, y3 - 0.2, 'manda K1/K2 y avisa a HA', fs=8.5, color=GRIS)

    # Actuadores 12 V
    y4 = ysal['actuadores']
    d.add(elm.Line().at((XO, y4)).right(0.8).color(VERDE))
    texto(d, XO + 1.0, y4 - 0.1, '→ actuadores 12 V del nodo NFT (driver MOSFET):', fs=9)
    texto(d, XO + 1.0, y4 - 0.5, '3 peristálticas A/B/pH− + 2 solenoides ½" NC', fs=9)

    # Reserva y libre
    y5 = ysal['reserva']
    d.add(elm.Line().at((XO, y5)).right(0.8).linestyle('--').color(GRIS))
    texto(d, XO + 1.0, y5, '→ reserva: nodo de riego v1 si se migra al bus, o luz de servicio 12 V', fs=9, color=GRIS)
    y6 = ysal['libre']
    d.add(elm.Line().at((XO, y6)).right(0.8).linestyle('--').color(GRIS))
    texto(d, XO + 1.0, y6, '→ libre', fs=9, color=GRIS)

    # ---------------- Notas de instalación ----------------
    texto(d, -0.5, 0.1, 'Instalación: todo el 12 V en gabinete IP65 separado del de 127 V · cables de bomba cal. 14 AWG, nodo cal. 18 AWG · '
          'F0 protege el cable de batería; F1–F6 protegen cada rama.', fs=9.5, color=GRIS)
    texto(d, -0.5, -0.35, 'Variante austera de arranque (fuente): Steren BR-1224 24 Ah + cargador BR-700 + 1 bomba + contacto GFCI ≈ $2,500–2,900 → cortes ≤ 7 h; '
          'se amplía a 100 Ah sin tirar nada.', fs=9.5, color=GRIS)
    texto(d, -0.5, -0.8, 'Prueba mensual (V11 apagón): botar el breaker del patio 10 min → la bomba sigue, llegan las 2 alertas, y al restaurar no hay falso "sin flujo".',
          fs=9.5, color=GRIS)

    # ---------------- Leyenda y pie ----------------
    LX, LY = 20.0, -4.4
    rect(d, (LX, LY), (LX + 11.4, LY + 2.7), color=GRIS)
    texto(d, LX + 0.2, LY + 2.35, 'Leyenda', fs=10.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.85)).right(0.8).color(VERDE))
    texto(d, LX + 1.2, LY + 1.85, 'bus 12.8 V CC (batería flotada)', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 1.35)).right(0.8).color(AMBAR))
    texto(d, LX + 1.2, LY + 1.35, '127 V CA aguas abajo del GFCI', fs=9.5)
    d.add(elm.Line().at((LX + 0.2, LY + 0.85)).right(0.8).linestyle('--').color(GRIS))
    texto(d, LX + 1.2, LY + 0.85, 'opcional / reserva', fs=9.5)
    texto(d, LX + 0.2, LY + 0.35, 'F = fusible · K = relé · NC/NO = reposo cerrado/abierto · S = seccionador', fs=9.5)

    texto(d, -0.5, -3.7, 'Fuentes: research/electrico-respaldo-seguridad.md §2–3, §6 · referencia/03-instalacion.md §2.3 · bom/fase2.csv (respaldo)', fs=9, color=GRIS)
    texto(d, -0.5, -4.2, f'{VERSION} · HomeGreen · generado con schemdraw desde hardware/electrico/bus_dc_first.py', fs=9, color=GRIS)

postproceso(SALIDA)
print('OK', SALIDA, os.path.getsize(SALIDA), 'bytes')
