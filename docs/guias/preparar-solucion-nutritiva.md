# Preparar la solución nutritiva del NFT

**En una línea:** en el tambo de 200 L, con agua de lluvia o de red sin cloro, disuelves 300 g de la fórmula genérica (o A y B por separado, **nunca en la misma cubeta**), esperas 10–15 min de mezcla entre cada adición, bajas el pH a 5.8–6.2 y dejas la EC en 1.2–1.8 mS/cm — y anotas gramos, agua base y lecturas, porque una EC "que se ve bien" no dice qué sales hay en el agua.

!!! info "Antes de empezar"
    - **Tiempo:** ~45 min activos + 30–45 min de esperas de mezcla (estimado) · **Costo por tanque de 200 L:** fórmula genérica 1.5 kg / $349 → 300 g ≈ **$70**; costal 25 kg / $3,359 → ≈ $40; sales A/B (~$90–150/m³) → ≈ $18–30 ([research/hidroponia-nft §e](../research/hidroponia-nft.md)) · **Personas:** 1
    - **Necesitas:** [Solución nutritiva para hortalizas 1.5 kg (rinde 1,000 L) $349](https://hydroenv.com.mx/producto/solucion-nutritiva-para-hortalizas-de-1-5-kg-rinde-para-1000-litros/) (o [costal 25 kg $3,359](https://hydroenv.com.mx/producto/solucion-nutritiva-para-hidroponia-hortalizas-en-costal-de-25-kg/) al escalar), báscula de precisión 0.1 g (o de cocina de 1 g), 2 cubetas de 19 L limpias marcadas **A** y **B**, jarra graduada, cucharón o agitador limpio, medidor pH/TDS-EC de mano **calibrado** ([calibrar sondas](calibrar-sondas-ph-ec.md)), [AquAcid pH− $516](https://hydroenv.com.mx/producto/aquacid-buffer-para-bajar-ph-regulador-de-ph-para-hidroponia/) (o ácido fosfórico/cítrico grado alimenticio), guantes de nitrilo y lentes, agua base (lluvia del tinaco o red por el dúplex sedimento + carbón), etiquetas
    - **Prerequisitos:** NFT con 48 h de agua sola sin fugas ([Fase 2 · NFT, paso 14](../fases/fase-2/nft.md)); EC y pH del agua de red y de lluvia medidos ([V7](../validacion/v07-agua.md)); sondas calibradas; secuencia de llenado en [Hidráulico §5.3](../diseno/hidraulico.md); lógica del lazo en [Dosificación v2](../fases/fase-2/dosificacion-v2.md)

## Los números que gobiernan la mezcla

![P&ID NFT recirculante: tambo 200 L con dosificación A/B/pH− junto a la succión, sondas pH y EC en el retorno, llenado desde el tinaco vía dúplex sedimento + carbón](../assets/diagramas/hidraulico/nft-recirculacion.svg)

| Magnitud | Objetivo | Fuente |
|---|---|---|
| pH | **5.8–6.2** | [06-validación L0](../referencia/06-validacion-y-lazos-agenticos.md) |
| EC total (agua + nutriente) | **1.2–1.8 mS/cm** según cultivo; arranca abajo de la banda y sube con datos de tus plantas | [06 L0](../referencia/06-validacion-y-lazos-agenticos.md), [Dosificación v2 §C](../fases/fase-2/dosificacion-v2.md) |
| Temperatura de solución | 18–22 °C; > 25 °C cae el oxígeno disuelto | [03 §2.1](../referencia/03-instalacion.md) |
| Fórmula genérica a dosis completa | 1.5 g/L → pH 6.2–6.3, CE 1.0–1.5 (ficha) | [research/hidroponia-nft §e](../research/hidroponia-nft.md) |
| Agua de lluvia | EC 0.02–0.06 mS/cm, sin cloro: la base ideal | [research/agua-captacion §e](../research/agua-captacion.md) |
| Agua de red < 0.4 mS/cm | Directo, solo carbón activado para el cloro | ídem |
| Agua de red 0.4–0.8 | Mezclar 50/50 con lluvia; restar el Ca/Mg del agua a la fórmula | ídem |
| Agua de red > 0.8 | **No** para NFT: lluvia como fuente principal o RO | ídem |
| Mezcla | 10–15 min entre adiciones; nunca dosificación continua | [03 §2.2](../referencia/03-instalacion.md) |
| Orden en tanque nuevo | **A → mezcla → B → mezcla → pH− → medir** | [Control · Lazo 2](../diseno/control.md) |

## Pasos

1. **Elige y anota el agua base.** Lluvia del tinaco (tras purgar el tlaloque) o red pasada por el dúplex sedimento 5 µm + carbón activado (el cloro libre de la red, 0.2–1.5 mg/L, daña raíces). Mide EC y pH del agua **antes** de agregar nada; con la tabla de arriba decides si va directo, 50/50 o solo lluvia.
   *Criterio de listo:* EC base anotada; EC base + ~1.0–1.5 de nutriente cabe en 1.2–1.8.
2. **Llena el tambo a la marca de 200 L** (SV-1 desde el tinaco vía dúplex, con LT-1 > 20 %; o lluvia) y **arranca la recirculación**: la bomba P-1 es la que mezcla. Verifica la temperatura en HA (`sensor.temperatura_solucion`): 18–22 °C; si la solución viene del tinaco al sol y pasa de 25 °C, espera a la tarde.
3. **Pesa el nutriente en seco, sobre papel o vaso tarado**, y anota los gramos y el lote del empaque:

    === "Fórmula genérica (arranque de Fase 2)"

        - **1.5 g/L → 300 g para 200 L** (aritmética: 1.5 kg rinde 1,000 L). Es un solo polvo balanceado para hortalizas de hoja: la opción de menor riesgo mientras aprendes el sistema.
        - Cuándo migrar: al pasar de ~2 m³/mes de consumo, al costal de 25 kg ($202/m³) o a sales A/B ($90–150/m³) cuando ya exista rutina de pesado.
        - Para la dosificación automática con peristálticas se necesita un concentrado en bote: [POR VERIFICAR: si la fórmula genérica completa admite concentrarse sin precipitar (pregunta a Hydro Environment o prueba 1 L en un frasco y observa 24 h); si precipita, el lazo automático usa A/B por separado y la fórmula genérica solo para el tanque inicial].

    === "Sales A/B (cuando ya hay rutina de pesado)"

        - **A:** Hakaphos de perfil **vegetativo** (Base/Verde) a **1 g/L → 200 g** para 200 L. **No** el Violeta 13-40-13 de los listados: es fórmula de floración (alto fósforo) [POR VERIFICAR: precio y ficha del Hakaphos vegetativo; el listado de [Mercado Libre](https://listado.mercadolibre.com.mx/fertilizante-hakaphos-violeta) y [Aldase](https://aldase.com.mx/producto/hakaphos-violeta-13-40-13-25-kg/) es del Violeta].
        - **B:** nitrato de calcio soluble a **0.8 g/L → 160 g** ([1 kg $56.50 en Hydro Environment](https://hydroenv.com.mx/producto/nitrato-de-calcio-para-plantas-1-kg/) para probar; [25 kg en ML](https://listado.mercadolibre.com.mx/nitrato-calcio-25-kg) al escalar).
        - **Cubetas separadas, siempre.** El nitrato de calcio precipita con fosfatos y sulfatos: A y B solo se encuentran ya diluidos en los 200 L del tambo.
        - [Nitrato de potasio 1 kg $119.90](https://hydroenv.com.mx/producto/nitrato-de-potasio-para-plantas-1-kg/) está disponible para afinar potasio [POR VERIFICAR: receta A/B completa para hoja con los gramos de cada sal; el porqué de las bandas y las fórmulas están en Resh, *Cultivos hidropónicos*, en `bom/fase2.csv`].

4. **Disuelve aparte, nunca polvo directo al tambo.** Cubeta con 5–10 L de la misma agua del tambo, agita hasta que no queden grumos ni cristales en el fondo. Con A/B: A en la cubeta A, B en la cubeta B; enjuaga el cucharón entre una y otra.
   *Criterio de listo:* la cubeta se ve transparente (puede tener color), sin sedimento.
5. **Vierte A (o la genérica) cerca de la succión de la bomba**, con P-1 corriendo, y **espera 10–15 min** sin agregar nada más. Mide EC con el medidor de mano y compárala con `sensor.ec_nft`.
6. **Con A/B: vierte B** de la misma forma y espera otros 10–15 min. Mide.
7. **Ajusta la EC si quedó abajo de 1.2 mS/cm:** agrega en porciones chicas (regla práctica de esta guía: ~10 % del peso inicial, ya disuelto, con 10–15 min entre cada una). No rebases 1.8; si te pasaste, agrega agua base, no la tires.
   *Criterio de listo:* EC en 1.2–1.8 (arranque 1.2–1.4) estable en dos lecturas separadas 10 min; sonda y medidor de mano ≤ 0.1 mS/cm de diferencia.
8. **Ajusta el pH.** El agua de red suele venir > 7 y la fórmula genérica deja 6.2–6.3: casi siempre hay que bajar. Guantes y lentes; **ácido al agua, nunca agua al ácido**: diluye unos mL de pH− en 1 L de agua del tambo y viértelos a la succión; espera 10–15 min; vuelve a medir. Repite en dosis pequeñas hasta 5.8–6.2. Una dosis grande "para llegar de una" se pasa al otro lado y arranca la oscilación que el lazo automático está diseñado para evitar.
   *Criterio de listo:* pH 5.8–6.2 estable en dos lecturas; sonda y medidor de mano ≤ 0.1.
9. **Verifica la temperatura** (18–22 °C) y que las 8 líneas siguen en 1–2 L/min.
10. **Botes para las peristálticas:** A, B y pH− en **tres botes separados y etiquetados**, cada uno con su manguera; pH− en anaquel aparte de los sanitizantes (H2O2, hipoclorito). La concentración de los botes se fija en el dry-run de dosificación [POR VERIFICAR: junto con el tamaño de la "dosis fija" — la que mueve la EC ≤ 0.1 mS/cm o el pH ≤ 0.1 en 200 L ([Dosificación v2 §C](../fases/fase-2/dosificacion-v2.md))]. Las mangueras internas de las peristálticas son consumibles: revísalas cada semana.
11. **Rearma la dosificación automática** en HA solo cuando el tanque está en banda y las sondas coinciden con el medidor de mano ([Control · Lazo 2](../diseno/control.md): el rearme es manual).

!!! danger "A y B en la misma cubeta"
    El calcio de B precipita con los fosfatos y sulfatos de A: la cubeta se vuelve lodo blanco, el calcio ya no está disponible y la EC "sube" con sales que la planta no puede tomar. Dos cubetas, dos botes, dos peristálticas.

!!! warning "Error típico: comprar Flora Series 'porque es lo que usan en YouTube'"
    GHE Flora Series cuesta $1,300–8,000 por m³ de solución contra $349 (genérica), $202 (costal) o $90–150 (sales). Es producto de autocultivo boutique; en producción se descarta ([research/hidroponia-nft §e](../research/hidroponia-nft.md)).

!!! warning "Error típico: fiarse solo de la EC"
    La EC suma sales, no dice cuáles. Con agua de red dura (Na, Cl) una EC de 1.4 puede llevar 0.9 de sales inútiles. Por eso se mide el agua base primero y por eso la solución se cambia completa cada 2–3 semanas aunque la EC "se vea bien" ([Cambiar la solución](cambiar-solucion-nft.md)).

## Al terminar

- [ ] Agua base identificada y medida (EC/pH) antes de agregar nutriente
- [ ] Gramos pesados y lote anotado; disuelto aparte; A y B en cubetas separadas
- [ ] 10–15 min de mezcla entre cada adición; EC 1.2–1.8 y pH 5.8–6.2 estables; sonda vs medidor de mano ≤ 0.1
- [ ] Temperatura 18–22 °C; 8 líneas en 1–2 L/min
- [ ] Botes A/B/pH− etiquetados y separados; dosificación automática rearmada
- Registrar en `bitacora/nft.csv`: `evento=solucion_nueva`, `nivel_tambo_pct`, `temp_solucion_C` y en `observaciones`: agua base y su EC, producto y lote, gramos (A/B por separado), EC y pH inicial y final, mL de pH−
- Siguiente paso: [Dosificación v2 · dry-run](../fases/fase-2/dosificacion-v2.md) (primera vez) o [Cambiar la solución del NFT](cambiar-solucion-nft.md) (cada 2–3 semanas)

## Fuentes

- [research/hidroponia-nft §e (nutrientes, costo por m³, Hakaphos vegetativo vs Violeta, nitrato de calcio siempre separado) y §g (pH−)](../research/hidroponia-nft.md)
- [research/agua-captacion §e](../research/agua-captacion.md) — calidad del agua de red y de lluvia, cloro, tabla de EC
- [referencia/03-instalacion §2.1–2.2](../referencia/03-instalacion.md) — temperatura, sondas en retorno, peristálticas a la succión, tiempo muerto
- [referencia/06-validacion L0](../referencia/06-validacion-y-lazos-agenticos.md) — bandas pH/EC · [diseno/control Lazo 2](../diseno/control.md) — orden A → B → pH−, rearme manual · [diseno/hidraulico §5.3](../diseno/hidraulico.md)
- [fases/fase-2/dosificacion-v2](../fases/fase-2/dosificacion-v2.md) — dosis fija, botes, rutina
- [`bom/fase2.csv`](../referencia/bom.md) — nutriente, AquAcid, Resh
