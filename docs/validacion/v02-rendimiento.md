# V2 · Ensayo de rendimiento por variedad

**En una línea:** tres charolas idénticas de una variedad, pesadas con báscula el día de cosecha, te dicen dos cosas que ninguna fuente pública sabe de tu rack: si el proceso está controlado (coeficiente de variación < 15 %) y si esa variedad paga el margen meta a tu precio de lista.

!!! info "Antes de empezar"
    - **Cuándo:** con cada variedad nueva antes de venderla (Fase 0: girasol y rábano en S1–S3); repetir por temporada (invierno y lluvias mueven rendimiento y CV) y tras cualquier cambio de densidad · **Tiempo:** 3 siembras en la misma sesión + 5 min de pesado por charola + 10 min de cálculo · **Costo:** el costo variable de 3 charolas (girasol CEDA $9.10, rábano $49.30, arúgula $35.30 c/u, [08](../referencia/08-recetas-y-economia-unitaria.md)) · **Personas:** 1
    - **Necesitas:** báscula de cocina de 1 g ($120) y báscula de precisión 0.1 g ($180) de `bom/fase0.csv`, 3 charolas dobles, semilla de **un solo lote** que pasó [V1](v01-germinacion.md), `bitacora/produccion.csv`
    - **Guías relacionadas:** [Sembrar una charola](../guias/sembrar-una-charola.md) · [Cosechar y empacar](../guias/cosechar-y-empacar.md) · **Desbloquea:** vender la variedad; fijar precio y mix por $/charola-semana

## Propósito

La tabla de recetas trae rendimientos **estimados** (girasol 300–500 g, chícharo 350–600 g) porque ninguna fuente pública los pesó; solo rábano, betabel, brócoli, amaranto, cilantro y arúgula tienen dato medido (Johnny's Yield Trial 2017, a primera hoja verdadera, en Maine). Tu multiplicador real (g cosechados ÷ g de semilla seca) es el único dato que decide el margen, y cosechando 1–2 días más tarde en CDMX puede salir 10–30 % arriba ([research/recetas §gaps](../research/recetas-produccion-economia.md)). Un CV alto entre tres charolas iguales significa que algo del proceso —densidad, riego, peso en oscuridad, posición— no está bajo control, y vender así es prometer lo que no controlas.

![Animación del ciclo de microgreens: remojo, oscuridad con peso, destape, desarrollo y cosecha con pesado](../assets/diagramas/animaciones/ciclo-microgreens.svg)

## Procedimiento

1. **Fija la receta antes de sembrar** desde [08 · tabla operativa](../referencia/08-recetas-y-economia-unitaria.md): densidad en g secos, remojo, días de oscuridad, días a cosecha. Escríbela en `observaciones` de las tres filas. *Criterio de listo:* los 4 números decididos y anotados; no se cambian a media prueba.
2. **Siembra 3 charolas idénticas el mismo día**: mismo lote `Sxxx`, misma densidad pesada a 0.1 g, misma sanitización y remojo, mismo coco, mismo peso en oscuridad. Posiciones alternadas en la pila y en el rack (no las tres en el mismo nivel). *Criterio de listo:* tres `siembra_id` consecutivos con la misma `densidad_g` en `bitacora/produccion.csv`.
3. **Trátalas exactamente igual** durante el ciclo: mismo riego, mismo destape, misma luz. En el lazo L1 cuenta la germinación del cuadro de 10 × 10 cm en una de ellas (es la charola marcada del lote). *Criterio de listo:* cero intervenciones distintas entre las tres.
4. **Cosecha las tres el mismo día**, en la ventana de la receta (rábano 7–10 días; girasol 8–12), con tijera limpia justo sobre el sustrato. *Criterio de listo:* las tres cortadas en la misma sesión.
5. **Pesa cada charola por separado** en la báscula de 1 g (producto limpio, sin cáscaras ni sustrato) y escribe `rendimiento_g` en su fila. *Criterio de listo:* tres pesos, no un promedio a ojo.
6. **Calcula media, desviación estándar y CV:**

    ```text
    media = (g1 + g2 + g3) / 3
    desv  = raíz( ((g1−media)² + (g2−media)² + (g3−media)²) / 2 )     # desviación muestral, n−1
    CV %  = desv / media × 100
    multiplicador = media / densidad_g
    ```

    *Criterio de listo:* CV con un decimal en la fila de `v02-rendimiento.csv`.
7. **Calcula el margen** con el costo variable de [08](../referencia/08-recetas-y-economia-unitaria.md) y tu precio de lista ($90–120 girasol; $130–180 finas; clamshell $50–90): `margen = (precio − costo variable) ÷ precio`. Si vendes cortado, compara además `g/charola` contra los gramos que prometes por clamshell. *Criterio de listo:* margen calculado con el precio al que **de verdad** vendes, no el de lista si diste promo.
8. **Decide** con la tabla de abajo y escribe la decisión en la fila. *Criterio de listo:* `decision` = `vender`, `repetir` o `no_vender`.

!!! example "Ejemplo con números"
    Rábano `S003`, 28 g, cosecha día 9: 260 g, 285 g, 240 g → media 261.7 g, desviación 22.5 g, **CV 8.6 %** (pasa). Multiplicador 9.3×. Costo variable $49.30, precio de lista $155 → **margen 68 %** (pasa la meta L2 de 60 %). Decisión: `vender`.

    Girasol `S001`, 135 g: 420, 450, 400 g → media 423 g, desviación 25 g, **CV 5.9 %**; multiplicador 3.1×. Con CEDA ($9.10) a $105: margen 91 %; con Al Natural ($29.50): 72 %. Las dos venden; el A/B de [V6](v06-experimento-ab.md) decide cuál semilla.

## Criterio de aceptación

!!! example "Aceptar la variedad si"
    - **CV < 15 %** entre las 3 charolas (misma densidad, mismo lote, mismo día).
    - **El rendimiento medio cubre el costo con el margen meta:** margen variable ≥ 60 % (meta L2, [KPIs](kpis.md)) al precio real de venta; nunca por debajo del 55 % que exige G0→1 (b).
    - Las tres filas están en `bitacora/produccion.csv` con `rendimiento_g` pesado.

    Si CV ≥ 15 %, **el proceso no está controlado**: revisar densidad, riego o presión de peso antes de vender esa variedad ([06 §V2](../referencia/06-validacion-y-lazos-agenticos.md)).

Para decidir **qué** sembrar entre variedades que pasan, la métrica es `$/charola-semana de rack` (margen bruto ÷ semanas que ocupa el rack), no el margen por charola: rábano ~$82, arúgula ~$70, girasol CEDA ~$61, cilantro ~$45 y solo bajo pedido ([08](../referencia/08-recetas-y-economia-unitaria.md)). Con tus rendimientos medidos, recalcula esa columna.

## Plantilla de registro

Las tres charolas van como filas normales en `bitacora/produccion.csv` (`V2 charola 1 de 3` en `observaciones`). El resultado del ensayo, en `bitacora/validacion/v02-rendimiento.csv`:

```csv
ensayo_id,fecha_siembra,variedad,lote_semilla,densidad_g,temporada,siembra_id_1,siembra_id_2,siembra_id_3,g_1,g_2,g_3,media_g,desv_g,cv_pct,multiplicador,costo_variable_mxn,precio_real_mxn,margen_pct,decision,observaciones
V2-RAB-01,2026-09-24,rabano,S003,28,secas,RAB-260924-S003-R1N5,RAB-260924-S003-R1N4,RAB-260924-S003-R1N3,260,285,240,261.7,22.5,8.6,9.3,49.30,155,68,vender,cosecha dia 9; sin moho
V2-GIR-01,2026-09-21,girasol,S001,135,secas,GIR-260921-S001-R1N5,GIR-260921-S001-R1N4,GIR-260921-S001-R1N3,420,450,400,423.3,25.2,5.9,3.1,9.10,105,91,vender,brazo CEDA del A/B; cascaras pegadas 5 %
V2-AMA-01,2026-09-24,amaranto,S005,10,secas,AMA-260924-S005-R1N2,AMA-260924-S005-R1N2b,AMA-260924-S005-R1N2c,150,95,180,141.7,43.1,30.4,14.2,7.50,150,95,repetir,CV alto: dos charolas se secaron en N2; color verde no rojo
```

- `temporada`: `secas` (nov–abr), `lluvias` (may–oct) o `invierno` (dic–feb): el CV y el rendimiento cambian con el clima ([research/clima-agronomia](../research/clima-agronomia.md)).
- `precio_real_mxn`: al que vendiste o vas a vender esa semana, promo incluida.
- Tres charolas es el **mínimo**; con 6 (las de girasol de la Fase 0) la desviación es más confiable.

## Si falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| CV ≥ 15 % con una charola muy por debajo | Posición (nivel seco o con corriente), riego desigual entre niveles, peso en oscuridad distinto | Revisar boquillas o atomizado por nivel; repetir con posiciones alternadas; no vender hasta CV < 15 % |
| CV ≥ 15 % con las tres dispersas | Densidad no pesada (semilla húmeda vs seca), remojo distinto, coco no hidratado parejo | Pesar semilla seca a 0.1 g; hidratar el coco en tanda; repetir |
| Rendimiento medio bajo pero CV bien | Densidad baja para la especie, cosecha temprana, semilla vieja | Subir densidad dentro del rango de [08](../referencia/08-recetas-y-economia-unitaria.md) con un A/B ([V6](v06-experimento-ab.md)); cosechar 1–2 días más tarde |
| Margen < 60 % con rendimiento normal | Precio de promo o semilla cara (chícharo Hydroenv $98/charola pierde a cualquier precio ≤ $98) | Subir precio a lista o cambiar la fuente de semilla; si no da, `no_vender` |
| Pasa en secas, falla en lluvias | HR 70–89 %: moho y estiramiento | Bajar densidad 10 %, ventilar, riego solo por abajo; repetir V2 en la temporada nueva |

!!! warning "Errores típicos"
    - Promediar "a ojo" en vez de pesar cada charola.
    - Comparar charolas de lotes o densidades distintas y llamarle V2.
    - Copiar los 250 g de girasol de algunas guías: es semilla ya remojada; 120–150 g secos es el rango.
    - Aceptar CV ≥ 15 % "porque el promedio se ve bien".

## Al terminar

- [ ] 3 charolas del mismo lote, densidad y día, con posiciones alternadas
- [ ] Tres pesos individuales en `bitacora/produccion.csv`
- [ ] Media, desviación, CV, multiplicador y margen en `bitacora/validacion/v02-rendimiento.csv`
- [ ] Decisión escrita: `vender` / `repetir` / `no_vender`
- [ ] Columna $/charola-semana recalculada con tus datos
- Registrar: fila en `bitacora/validacion/v02-rendimiento.csv`; la decisión también en `observaciones` de las tres charolas
- Siguiente paso: [Hoja de precios](../guias/hoja-de-precios.md) con lo que puedes prometer; [V6](v06-experimento-ab.md) si quieres mover la densidad

## Fuentes

- [06 · Validación §V2](../referencia/06-validacion-y-lazos-agenticos.md): 3 charolas idénticas, CV < 15 %, rendimiento medio vs costo y margen meta.
- [08 · Recetas y economía unitaria](../referencia/08-recetas-y-economia-unitaria.md): densidades, rendimientos medidos vs estimados, costo variable, $/charola-semana, "pesar las primeras 6".
- [research/recetas-produccion-economia](../research/recetas-produccion-economia.md): Johnny's Yield Trial 2017 (metodología, gaps: girasol y chícharo sin dato pesado; +10–30 % con cosecha tardía).
- [Fase 0 · Siembra](../fases/fase-0/siembra.md): ejemplo de CV (420/450/400 g → 6 %), A/B de girasol como V2 + V6.
- [research/clima-agronomia](../research/clima-agronomia.md): efecto de lluvias e invierno en germinación y moho.
