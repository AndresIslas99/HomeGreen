# Cómo usar esta guía

**En una línea:** cómo está organizado el sitio, qué significa cada bloque de una página, cómo registras tu avance, cómo funcionan los gates y cómo corriges un precio o corres la wiki en tu máquina.

!!! info "Antes de empezar"
    - **Tiempo:** 15 min de lectura · **Costo:** $0 · **Personas:** 1
    - **Necesitas:** una cuenta de GitHub si vas a marcar avance con issues o proponer correcciones; Python 3.11+ si quieres el sitio en local
    - **Prerequisitos:** ninguno

## La estructura del sitio

Todo cuelga de siete pestañas. La regla de navegación: **si vas a hacer algo, entra por Fases; si vas a entender algo, entra por Diseño o Referencia.**

| Pestaña | Qué contiene | Cuándo la usas |
|---|---|---|
| **Empieza aquí** | [Antes de gastar un peso](antes-de-gastar-un-peso.md), esta página y la [línea de tiempo](linea-de-tiempo.md) | La primera semana, y cada vez que necesites ubicarte en el calendario |
| **Fases** | Una carpeta por fase (0, 1, 2, 3) con las páginas en el orden en que se ejecutan: compras → montaje → operación → ventas → gate | Mientras construyes; es el camino crítico |
| **Guías** | Una tarea = una página (sembrar una charola, anclar el túnel, calibrar sondas, facturar CFDI…) | Cuando estás con las manos en la tarea; las fases enlazan a ellas |
| **Diseño** | Por qué el sistema es así: eléctrico, hidráulico, control, datos, layout, estructura, rack | Antes de comprar electrónica o modificar algo; cuando algo falla |
| **Validación** | Lazos L0–L4, métodos V1–V11 con checklist, KPIs y gates | Antes de cada compra grande y al cerrar cada fase |
| **Software** | Firmware ESPHome, Home Assistant, herramientas CLI | Fase 1 en adelante |
| **Aprendizaje** y **Referencia** | Videos, libros, cursos; BOM, normativa, clima, glosario, FAQ, los 9 documentos base (00–08) y los 17 informes de investigación | Para tener criterio y para verificar de dónde salió un número |

Los índices de fase (`fases/fase-N/index.md`) traen siempre: objetivo, inversión, meta, duración, "cómo se verá" (planta 2D + render 3D), la tabla de páginas en orden y el gate.

## Anatomía de una página accionable

Todas las páginas de Fases y Guías tienen la misma forma para que sepas dónde mirar sin leer todo:

```markdown
# Título en imperativo                      ← lo que vas a lograr
**En una línea:** qué se logra y por qué importa.
!!! info "Antes de empezar"                 ← tiempo, costo (con fuente), personas,
    Tiempo · Costo · Personas · Necesitas · Prerequisitos     materiales y guías previas
## Pasos                                    ← numerados, con números y unidades
1. **Verbo + objeto.** Detalle. *Criterio de listo:* qué observas cuando está bien.
!!! warning "Error típico"                  ← qué sale mal y cómo evitarlo
## Al terminar                              ← checklist, qué registrar en bitácora,
- [ ] …                                        siguiente paso
## Fuentes                                  ← de dónde salió cada dato
```

El **criterio de listo** es la parte importante: no dice "haz X", dice "sabes que X quedó bien cuando ves Y". Si no puedes observar Y, el paso no está terminado.

### Admoniciones

| Bloque | Significa | Qué haces con él |
|---|---|---|
| `!!! info` | Contexto o requisitos previos | Léelo antes de empezar |
| `!!! tip` | Atajo o truco que ahorra tiempo o dinero | Opcional, recomendado |
| `!!! warning "Error típico"` | Lo que sale mal con más frecuencia | Revísalo antes del paso que lo sigue |
| `!!! danger` | Riesgo para personas, para el cultivo completo o para el dinero | No sigas sin resolverlo |
| `!!! example` | Un caso resuelto con números | Cópialo y cambia tus valores |

!!! danger "Ejemplo de danger"
    El patio es "lugar mojado" según la NOM-001-SEDE: ningún relé se energiza sin GFCI y tierra física medida (≤25 Ω).

### Otros bloques que vas a encontrar

- **Pestañas** (`=== "Opción A"`): alternativas excluyentes, por ejemplo herrero vs kit prefabricado. Elige una.
- **Listas de tareas** (`- [ ]`): checklists que puedes copiar a un issue (ver abajo).
- **Diagramas Mermaid**: flujos de decisión, estados y el Gantt; se dibujan en el navegador.
- **Imágenes con lupa**: cualquier esquema o planta se abre a pantalla completa al hacer clic.
- **Videos incrustados**: solo los verificados en [Aprendizaje → Videos](../aprendizaje/videos.md).

### Convenciones de datos

- Todos los precios son **MXN al 12-sep-2026**, con IVA. **"verificado"** = leído en la ficha del proveedor; **"aprox."** = visto en resultados de búsqueda sin abrir la ficha. Antes de pagar, abre el enlace.
- Cada número lleva unidad (L, kWh/mes, mS/cm, g/charola). Si ves un número sin unidad, es un error: repórtalo.
- **`[POR VERIFICAR: cómo]`** marca un dato que no pudimos confirmar y dice cómo confirmarlo. No es relleno: es una tarea pendiente que puedes tomar.
- Enlaces externos: solo los que aparecen en los documentos base y en los informes de investigación. Un enlace que no está ahí no entra sin verificarlo.

## Cómo marcar tu avance

La wiki no guarda estado: el avance vive en GitHub o en la bitácora. Tres opciones, combinables.

=== "Opción A: issues de GitHub"

    1. Abre un issue en [github.com/AndresIslas99/HomeGreen/issues](https://github.com/AndresIslas99/HomeGreen/issues) por cada página de fase o guía que vayas a ejecutar; título = título de la página.
    2. Copia al cuerpo del issue el bloque **Al terminar** (las líneas `- [ ]`). GitHub las vuelve casillas interactivas.
    3. Etiquetas sugeridas: `fase-0`, `fase-1`, `fase-2`, `gate`, `compra`, `validacion`. Créalas la primera vez.
    4. Cierra el issue solo cuando todas las casillas estén marcadas y la bitácora tenga la fila correspondiente.
    5. Los gates se abren como issue con la tabla del gate pegada y se cierran con los números reales (ver abajo).

=== "Opción B: bitácora CSV"

    Es el sensor de los lazos L2–L4 ([06 · Esquema de datos](../referencia/06-validacion-y-lazos-agenticos.md)). Una fila por evento, el mismo día, nunca de memoria al final de la semana.

    `bitacora/produccion.csv`:

    ```csv
    siembra_id,fecha_siembra,variedad,lote_semilla,densidad_g,dias_oscuridad,fecha_cosecha,rendimiento_g,merma_pct,destino,precio_mxn,observaciones
    GIR-260915-S001-R1N2,2026-09-15,girasol,S001,135,3,2026-09-24,420,5,RestA,105,primer lote proveedor nuevo; sanitizado H2O2 3%
    ```

    `bitacora/ventas.csv`:

    ```csv
    fecha,cliente,producto,cantidad,precio_unit_mxn,entregado_a_tiempo,feedback
    ```

    El `siembra_id` es `VAR-AAMMDD-Slote-posición`: `GIR-260915-S001-R1N2` = girasol, sembrado el 15-sep-2026, costal S001, rack 1 nivel 2. El mismo código va en masking tape sobre la charola y se copia a la etiqueta al empacar. Las herramientas de [Software → CLI](../software/herramientas-cli.md) (`tools/kpis.py`, `tools/gate_audit.py`) leen estos dos archivos.

=== "Opción C: tu propio fork"

    1. Haz fork del repositorio y clónalo.
    2. Marca las casillas directamente en los `.md` (`- [x]`) conforme avances y haz commit: el historial de Git es tu bitácora de construcción.
    3. Si además corriges un dato, mándalo como pull request al repositorio original (ver abajo).

## Cómo funcionan los gates

Un gate es la condición medible para liberar el dinero de la siguiente fase. Se evalúa en el lazo L4 con datos de la bitácora y de Home Assistant, no con impresiones.

| Gate | Umbral | De dónde sale el dato | Si no se alcanza |
|---|---|---|---|
| **G0→1** | ≥2 clientes con ≥3 compras semanales consecutivas **y** margen variable ≥55 % en ventas reales | `bitacora/ventas.csv` + precios | Iterar 2 semanas más (precio, zona, producto) o abortar con pérdida acotada de $6,700–9,500 |
| **G1→2** | 4–5 clientes fijos, pedidos rechazados 2 semanas seguidas, **y** 30 días con <2 alarmas críticas/semana y cero pérdidas por fallo de riego | ventas + histórico de Home Assistant | No agregar NFT sobre una base inestable |
| **G2→3** | Neto ≥$12k/mes durante 3 meses **y** ≤9 h/semana medidas con el timesheet V9 | contabilidad + `V9` | Subir precios, contratar ayudante o recortar clientes antes de escalar m² |

Tres reglas:

1. **Un gate no alcanzado no se renegocia a la baja.** Se itera o se detiene. Las condiciones están escritas en Git antes de empezar la fase; los commits son la prueba de que no se movieron los postes.
2. **El gate se audita, no se recuerda.** `python3 tools/gate_audit.py --gate G0-1` lee la bitácora y te dice si pasaste, con los números ([Software → CLI](../software/herramientas-cli.md)).
3. **El neto que cuenta es el realista** ($6,500–11,000/mes en régimen), no el optimista del plan original ([07 · El número corregido](../referencia/07-puntos-ciegos-y-riesgos.md)).

Cada fase tiene su página de gate con checklist: [G0→1](../fases/fase-0/gate.md) · [G1→2](../fases/fase-1/gate.md) · [G2→3](../fases/fase-2/gate.md). La tabla completa vive en [Validación → Gates](../validacion/gates.md).

## Cómo contribuir o corregir un precio

Los precios caducan. Si abres un enlace y el precio cambió, corrígelo así:

1. **Verifica en la ficha del proveedor** (no en un resultado de búsqueda) y anota la fecha.
2. **Edita el BOM** correspondiente (`bom/fase0.csv`, `fase1.csv` o `fase2.csv`). Columnas: `categoria,item,cantidad,precio_unit_mxn,subtotal_mxn,estado_precio,proveedor,enlace,notas`. Cambia `precio_unit_mxn` y `subtotal_mxn`, pon `estado_precio` en `verificado` y añade en `notas` "verificado AAAA-MM-DD".
3. **Edita la página que lo cita.** Cada página tiene un lápiz arriba a la derecha que abre el archivo en GitHub para editarlo; el buscador del sitio te dice qué páginas mencionan el ítem.
4. **Manda el pull request** con título `bom: <ítem> $viejo → $nuevo (<proveedor>, <fecha>)`. Si agregas un enlace nuevo, corre antes `python3 tools/check_links.py` (marca 200, redirección, bloqueado-403 o muerto). El flujo `.github/workflows/links.yml` lo repite cada semana.
5. **Regla de oro:** no inventes. Si no pudiste verificar, escribe `[POR VERIFICAR: cómo]` y explica cómo se verifica. Un `[POR VERIFICAR]` honesto vale más que un número bonito.

!!! warning "Enlaces conocidos como muertos o incorrectos"
    No los reintroduzcas: hanlob.com.mx como proveedor de malla antigranizo (no la vende), tusmicrogreens.com, yema.mx/p/microgreens-de-girasol, sistemadehuertosurbanoscdmx.com, el PDF de COFEPRIS-05-018 en gob.mx y el video de YouTube `b-j0V90kU_k` (es de Curtis Stone, no de Donny Greens; el correcto es `MoSDSE8j7k8`).

Lo mismo aplica a densidades, rendimientos y cualquier dato de la bitácora: si tu charola de girasol rindió 480 g con 135 g de semilla, ese dato mejora la [tabla de recetas](../referencia/08-recetas-y-economia-unitaria.md) más que cualquier fuente extranjera. Mándalo.

## Cómo correr el sitio en tu máquina

El sitio se publica solo desde `main` con GitHub Actions (`.github/workflows/docs.yml`) en https://andresislas99.github.io/HomeGreen/. Para verlo en local con recarga automática:

```bash
git clone https://github.com/AndresIslas99/HomeGreen.git
cd HomeGreen
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-docs.txt                 # mkdocs-material y mkdocs-glightbox
mkdocs serve
```

Abre http://127.0.0.1:8000. Cada vez que guardes un `.md` la página se recarga. Antes de un pull request corre `mkdocs build --strict`: falla si hay un enlace interno roto o una imagen que no existe.

Si es la primera vez que publicas tu fork: *Settings → Pages → Source: GitHub Actions*.

## Al terminar

- [ ] Sabes por qué pestaña entrar según lo que vas a hacer
- [ ] Identificas "criterio de listo", "error típico" y los cinco tipos de admonición
- [ ] Elegiste cómo vas a marcar avance (issues, bitácora o fork) y creaste el primer issue o la primera fila
- [ ] Sabes qué mide cada gate y dónde está su checklist
- [ ] Tienes el sitio corriendo en local o el enlace público a la mano
- Siguiente paso: [Línea de tiempo](linea-de-tiempo.md) para ubicar tu semana 1, y luego [Fase 0](../fases/fase-0/index.md).

## Fuentes

- [06 · Validación y lazos agénticos](../referencia/06-validacion-y-lazos-agenticos.md): gates L4, esquema de datos de la bitácora, formato de `siembra_id`.
- [07 · Puntos ciegos y riesgos](../referencia/07-puntos-ciegos-y-riesgos.md): el neto corregido contra el que se evalúan los gates.
- [00 · Plan maestro](../referencia/00-plan-maestro.md): filosofía "vender antes de construir".
- `mkdocs.yml` y `requirements-docs.txt` del repositorio: configuración del sitio.
