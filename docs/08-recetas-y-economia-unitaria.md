# Recetas de producción por especie y economía unitaria

La tabla operativa que gobierna qué se siembra, con cuánta semilla y a qué precio se vende.
Síntesis de 3 fuentes cruzadas (Johnny's Yield Trial 2017 —el único dataset público con
rendimientos pesados por charola 1020—, Bootstrap Farmer y True Leaf Market) con precios de
semilla mexicanos verificados al 12-sep-2026. Fuente completa:
[research/recetas-produccion-economia.md](research/recetas-produccion-economia.md).

## Tabla operativa por especie (charola 1020, 25×50 cm)

| Especie | Semilla g/charola | Remojo | Oscuridad | Días a cosecha | Rendimiento g/charola | Merma plan* |
|---|---|---|---|---|---|---|
| Girasol | **120–150 g secos** | 8–12 h | 2–3 d con peso | 8–12 | 300–500 (estimado — pesar las primeras 6) | 5–10 % |
| Chícharo | **250–300 g secos** | 6–24 h | 3–5 d | 9–13 | 350–600 (estimado) | 3–8 % |
| Rábano | **25–30 g** | no | 2–3 d | 7–10 | **225–325 (medido)** | 2–5 % |
| Betabel | **25–35 g** | 4–8 h | 6–8 d (el más largo) | 13–18 | 180–270 | 8–12 % |
| Brócoli | **13–18 g** | no | 2–3 d | 9–13 | 250–330 | 5–10 % |
| Amaranto | **8–12 g** | no | 2–4 d | 14–18 | 120–200 | 10–15 % |
| Cilantro (entera) | **30–40 g** | 2–4 h + H2O2 | 7–9 d | 18–24 | 140–200 | 8–12 % |
| Arúgula | **10–12 g** | **NUNCA** (mucílago) | 3–4 d | 10–14 | 200–285 (28× su semilla) | 5–8 % |

\* Ninguna fuente pública tabula mermas: son supuestos de planeación (global ~8 %); la
bitácora los sustituye con datos propios desde la semana 2 — es el primer entregable del
lazo L1 de [06-validacion](06-validacion-y-lazos-agenticos.md).

## Precio de semilla verificado en México ($/kg efectivo, escalón 453+ g)

| Especie | Hydro Environment | Referencia internacional (25 lb) | Lectura |
|---|---|---|---|
| Girasol (forrajero) | $300 | ~$141 | Mejor: CEDA $24–34 (con prueba V1) o Al Natural $185 (específica) |
| Chícharo | $340 | ~$106 | ⚠️ ver regla de oro abajo |
| Rábano | $1,600 | ~$430 | Usable (solo 28 g/charola) |
| Betabel | $1,600 | — | Usable |
| Brócoli | $3,500 (¡8×!) | ~$440 | Comprar en Hydrocultura |
| Amaranto nacional | $300 | Garnet Red ~$635 | ⚠️ el nacional es de grano: probablemente VERDE — validar color antes de vender como "fino" |
| Cilantro | $450 | — | Semilla entera: subir densidad y sumar 2–3 días |
| Arúgula | $2,800 (4.7×) | ~$590 | Solo para arrancar; presionar cotización Hydrocultura |

Palanca de margen para Fase 2+: importar brassicas a precio internacional (requiere permiso
fitosanitario SENASICA) o mayoreo real con Hydrocultura.

## Economía por charola (charola viva B2B, lista corregida $90–120 / $130–180)

| Especie | Costo variable | Margen bruto/charola | **$/charola-SEMANA de rack** |
|---|---|---|---|
| **Rábano** | $49.30 | $81–131 | **$82** ← el mejor uso del rack |
| **Arúgula** | $35.30 | $95–145 | **$70** |
| Amaranto (si logra color/precio fino) | $7.50 | $123–173 | $65 |
| Brócoli | $57.00 | $73–123 | $62 |
| **Girasol (semilla CEDA)** | **$9.10** | $81–111 | **$61** |
| Chícharo (arvejón CEDA, por validar) | $15.50–21 | $69–105 | $55 |
| Betabel | $52.50 | $78–128 | $48 |
| Cilantro | $20.25 | $110–160 | $45 (solo bajo pedido) |
| **Chícharo (semilla Hydroenv $340/kg)** | **$98.00** | **−$8 a +$22** | **$4.50 ☠️** |

La métrica que decide qué sembrar es **$/charola-semana** (el rack es el recurso escaso), no
el margen por charola.

## Reglas económicas

1. **El error conceptual del plan original:** el chícharo "barato" ($340/kg) cuesta
   $93.50/charola porque lleva 275 g; el brócoli "carísimo" ($3,500/kg) solo $52.50 porque
   lleva 15 g. **La densidad manda tanto como el $/kg.**
2. **NO arrancar con chícharo** hasta validar arvejón grado alimento de CEDA (~$40–60/kg,
   preguntar en Mayoreo Online/La Molinera): con semilla Hydroenv pierde dinero a cualquier
   precio ≤$98.
3. **Mix de arranque Fase 0:** girasol (ancla de volumen, prueba A/B CEDA vs específica) +
   rábano (mejor $/charola-semana, la especie más noble para aprender) + arúgula (segunda
   fina). Amaranto solo charola de PRUEBA de color. Brócoli/betabel en segunda ola cuando
   Hydrocultura cotice. Cilantro solo bajo pedido confirmado (21 días de rack).
4. **Con la lista corregida el mix queda en ~15–30 % de costo variable** — el "25–35 %" del
   plan se salva por el lado del precio, no del costo. A los precios originales ($60–90),
   rábano dejaba 18 %, brócoli 5 % y chícharo perdía: los $60–90 destruyen el margen de todo
   menos el girasol.
5. **Ingreso Fase 1 revalidado:** 30 charolas/sem (15 girasol + 15 finas) ≈ $16,900/mes
   bruto con ~21 % de costo variable — el objetivo del plan se alcanza incluso con 20–22
   charolas vendidas: hay colchón para curva de aprendizaje y merma.
6. Descargar la guía gratuita de densidades de On The Grow (checkout $0:
   [tray-specific guide](https://onthegrow.net/products/free-tray-specific-microgreen-seeding-guide-pdf))
   como 4ª fuente, y **pesar las primeras 6 charolas de girasol/chícharo**: el multiplicador
   real es el único dato que ninguna fuente pública midió.
