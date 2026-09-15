# V7 · Validación de agua

**En una línea:** mides pH y EC del agua de la llave (3 días distintos) y de la lluvia captada al arrancar y cada temporada, clasificas tu red en una de tres rutas para el NFT, y una vez al año mandas al laboratorio el agua que toca producto que se vende —$542–607 la muestra es barato comparado con perder un cliente por inocuidad.

!!! info "Antes de empezar"
    - **Cuándo:** al arrancar (Semana 0 o S12 con el tinaco), al inicio y al final de la temporada de lluvias, **antes de llenar el tambo NFT** (S19–20) y siempre que cambies de fuente; laboratorio al arrancar la Fase 1 y después cada 6–12 meses · **Tiempo:** 5 min por lectura × 4 lecturas; 1 h para tomar y llevar la muestra al laboratorio · **Costo:** medidor pH + TDS/EC de mano ~$450 aprox. ([ML](https://listado.mercadolibre.com.mx/medidor-ph-tds-ec), `bom/fase2.csv`, adelántalo a Fase 1); laboratorio: E. coli en agua $542–607/muestra (LANISAF, verificado); paquete NOM-127 coliformes + E. coli $600–1,200 aprox.; plan anual completo (agua + producto + superficie) $6,000–10,000 aprox. · **Personas:** 1
    - **Necesitas:** medidor de mano **calibrado** con buffers 4.01/6.86 y patrón 1.413 mS/cm, 3 vasos limpios, agua destilada, frasco de vidrio desinfectado de 200 mL y hielera para la muestra de laboratorio, `bitacora/agua.csv`, `bitacora/inocuidad/laboratorio.csv`
    - **Guías relacionadas:** [Fase 1 · Agua §Medir el agua](../fases/fase-1/agua.md) · [Instalar canaleta y captación](../guias/instalar-canaleta-y-captacion.md) · [Preparar solución nutritiva](../guias/preparar-solucion-nutritiva.md) · [Calibrar sondas](../guias/calibrar-sondas-ph-ec.md) · **Desbloquea:** la ruta del agua del NFT (compras de Fase 2); la carpeta de inocuidad

## Propósito

La banda objetivo del NFT es **EC 1.2–1.8 mS/cm incluyendo nutrientes**: si el agua base ya trae 1.0 de sales inútiles (sodio, cloruros de pozos del oriente), no queda margen para la fórmula ([research/agua-captacion §e](../research/agua-captacion.md)). El agua de lluvia de CDMX sale con **EC 0.02–0.06 mS/cm**, sin cloro: es la fuente premium y un argumento de venta con los chefs. Y como el producto se come crudo, el agua que lo toca en las últimas 48 h debe ser potable o desinfectada (NOM-251, [research/inocuidad §4](../research/inocuidad-operativa.md)); el informe de laboratorio acreditado es además lo primero que pide compras de un hotel.

## Rutas según la EC de la red

| EC del agua de red | Diagnóstico | Ruta para el NFT | Para microgreens |
|---|---|---|---|
| **< 0.4 mS/cm** (típico poniente/centro, Cutzamala) | Excelente | Directo; solo carbón activado para el cloro (dúplex sedimento 5 µm + carbón) | Sin cambio |
| **0.4–0.8 mS/cm** | Usable | Mezclar 50/50 con lluvia y restar el aporte de Ca/Mg del agua a la fórmula | OK (riegan sustrato) |
| **> 0.8–1.0 mS/cm** (oriente/sur, pozos: hasta 2.5 mS/cm medidos) | Mala para NFT | Lluvia como fuente principal, o RO (~$2,500–5,000 aprox. un equipo doméstico 100 GPD) | Usable, vigilar sales en el sustrato |

Lluvia: **≪ 0.3 mS/cm** (típico 0.02–0.06). Si sale más alta, el separador de primeras lluvias no está purgando o el tinaco está sucio.

## Procedimiento

### A. Medición de campo (al arrancar y cada temporada)

1. **Calibra el medidor de mano** con los mismos buffers (4.01 / 6.86) y el patrón 1.413 mS/cm, según su manual; anota la fecha de calibración. Sin esto, todo lo que sigue es ruido. *Criterio de listo:* lee 6.86 ± 0.1 y 1.413 ± 0.1 en los patrones.
2. **Agua de red, 3 días distintos**, de la llave del patio, después de dejar correr 30 s: pH, EC y temperatura del vaso (el patrón vale a 25 °C; fuera de eso, usa la tabla de la etiqueta). Con tandeo, mide en días con y sin presión. *Criterio de listo:* 3 filas `fuente=red` con fecha.
3. **Agua captada**, después de la primera tormenta útil (con el tlaloque purgado): del tinaco, por la salida inferior. *Criterio de listo:* 1 fila `fuente=lluvia`; en temporada, repetir a mitad y al final.
4. **Tinaco y tambo** (Fase 2): EC del tinaco mezclado (red + lluvia) y del tambo **antes** de agregar nutriente en cada cambio de solución. *Criterio de listo:* la fila `fuente=tambo_base` de cada cambio ([Cambiar la solución](../guias/cambiar-solucion-nft.md)).
5. **Clasifica la red** con la tabla y escribe la ruta en `observaciones` y en tu copia de [Fase 2 · Compras](../fases/fase-2/compras.md): eso decide si compras dúplex, mezclas o RO. *Criterio de listo:* ruta escrita antes de comprar nada de tratamiento.
6. **Enjuaga la sonda con destilada** entre muestras y guárdala húmeda. *Criterio de listo:* la sonda de pH nunca se guarda seca.

### B. Laboratorio (al arrancar Fase 1; luego cada 6–12 meses)

7. **Elige el laboratorio** y verifica su acreditación (padrón EMA: [ema.org.mx](https://www.ema.org.mx/portal_v3/) → Catálogo de Acreditados; pide el número EMA y, si aplica, su oficio de Tercero Autorizado COFEPRIS). Opciones verificadas: **LANISAF (UACh, Texcoco)** para E. coli en agua, $607 citometría / $542 plaqueo, ISO 9001, no EMA para ese ensayo: monitoreo económico; **Quibimex (Iztapalapa)**, EMA A-012-001/12, cotización directa: evidencia para hoteles ([research/inocuidad §3](../research/inocuidad-operativa.md)). *Criterio de listo:* cotización con folio y lista de análisis.
8. **Toma la muestra como pide el laboratorio**: LANISAF, 200 mL en frasco de vidrio desinfectado, en frío, recepción lunes a jueves (viernes antes de las 12 h); resultados ≤ 12 días hábiles. Muestra del punto que toca producto: tinaco (o tambo NFT) y, si captas lluvia, tinaco tras tormenta. *Criterio de listo:* frasco etiquetado con fecha, hora y punto; en hielera.
9. **Pide coliformes totales + E. coli** (paquete tipo NOM-127) y, una vez al año, **metales** ([06 §V7](../referencia/06-validacion-y-lazos-agenticos.md)); al arrancar la Fase 1 agrega 1 análisis de **producto** (mesófilos, E. coli, *Salmonella* en girasol o chícharo): ese informe es tu carta de presentación B2B. *Criterio de listo:* orden de servicio con los tres rubros.
10. **Archiva el informe** en la carpeta de inocuidad (PDF de 8–10 páginas para hoteles) y registra el resultado en `bitacora/inocuidad/laboratorio.csv`. Vigencia útil para el paquete B2B: < 6 meses. *Criterio de listo:* PDF guardado y fila con `aprobado`.

## Criterio de aceptación

!!! example "Aceptar el agua si"
    - **Lluvia:** EC **≪ 0.3 mS/cm** (esperable 0.02–0.06) en cada lectura de temporada.
    - **Red:** clasificada con **3 lecturas** en la tabla; si EC > 0.8 mS/cm, el NFT **no** se formula sobre esa base sin mezcla, lluvia o RO.
    - **Laboratorio (anual, mínimo):** coliformes y metales del agua que toca producto que se vende **dentro de norma** en el informe del laboratorio; informe con menos de 6 meses cuando lo pida un cliente.
    - Todo en `bitacora/agua.csv` y `bitacora/inocuidad/laboratorio.csv`.

## Plantilla de registro

`bitacora/agua.csv` (columnas base `fecha,fuente,ec_ms_cm,ph` como proponen [Fase 1 · Agua](../fases/fase-1/agua.md) y la [guía de canaleta](../guias/instalar-canaleta-y-captacion.md), más dos):

```csv
fecha,fuente,ec_ms_cm,ph,temp_c,observaciones
2026-09-15,red,0.52,7.4,22,"llave del patio; con presion; medidor calibrado 2026-09-15"
2026-09-17,red,0.49,7.3,21,"dia de tandeo: solo tinaco de casa"
2026-09-19,red,0.55,7.5,23,"promedio 0.52 -> ruta: mezclar 50/50 con lluvia para NFT"
2026-06-08,lluvia,0.04,6.6,19,"tinaco tras tormenta 30 mm; tlaloque purgado antes"
2027-02-02,tambo_base,0.28,7.1,18,"mezcla 50/50 antes de nutriente; cambio de solucion #4"
```

- `fuente`: `red` · `lluvia` · `tinaco` (mezcla) · `tambo_base` (antes de nutriente) · `ro`.
- Si `tools/kpis.py` lee este archivo, las cuatro primeras columnas no cambian `[POR VERIFICAR: en software/herramientas-cli.md cuando el script esté en el repositorio]`.

`bitacora/inocuidad/laboratorio.csv` (una fila por análisis):

```csv
fecha_muestra,laboratorio,acreditacion,fuente,analisis,resultado,unidad,limite_referencia,aprobado,folio,costo_mxn,vigente_hasta,observaciones
2027-01-20,LANISAF UACh,ISO 9001 RSGC-1087,tinaco,E. coli (plaqueo),ausente,UFC/100 mL,ausente,si,LAN-27-0142,542,2027-07-20,"200 mL vidrio; entregado lunes 9 h; resultado en 9 dias habiles"
2027-01-20,Quibimex,EMA A-012-001/12,tinaco,coliformes totales,<1.1,NMP/100 mL,ausente (NOM-127),si,QB-27-0388,[POR VERIFICAR: cotizacion],2027-07-20,"paquete agua; incluye metales anual"
2027-01-20,Quibimex,EMA A-012-001/12,producto girasol,Salmonella spp. 25 g,ausente,en 25 g,ausente,si,QB-27-0389,[POR VERIFICAR: cotizacion],2027-07-20,"carta de presentacion B2B"
```

- `limite_referencia`: el que el laboratorio reporta según la norma aplicable `[POR VERIFICAR: límites exactos de NOM-127 y de producto en el informe del laboratorio; esta wiki no los fija]`.

## Si falla

| Resultado | Qué hacer |
|---|---|
| Red > 0.8 mS/cm | NFT con lluvia como fuente principal (captación de Fase 1 + tinaco 1,100 L) o RO; microgreens siguen con red. Escríbelo en compras de Fase 2 antes de comprar el dúplex |
| Red 0.4–0.8 | Mezcla 50/50; resta Ca/Mg del agua a la fórmula ([Preparar solución nutritiva](../guias/preparar-solucion-nutritiva.md)) |
| Lluvia > 0.3 mS/cm | Separador de primeras lluvias sin purgar o tinaco con sedimento: purga tras cada tormenta, lava el tinaco, repite la lectura tras la siguiente lluvia ([Instalar canaleta](../guias/instalar-canaleta-y-captacion.md)) |
| pH de red > 8 o < 6 | Anótalo: la peristáltica de pH− trabajará más (deriva de dosificación, [Control](../diseno/control.md)); no es motivo de rechazo |
| Laboratorio: coliformes o E. coli presentes | Esa agua **no** toca producto: riego de las últimas 48 h con agua potable; cloro 0.2–1.5 ppm libre o UV antes de que toque producto si es pluvial; lavar tinaco; **repetir el análisis** antes de vender producto regado con esa fuente ([research/inocuidad §4](../research/inocuidad-operativa.md)) |
| Laboratorio: metal fuera de norma | Cambiar de fuente (lluvia/RO) para todo lo que se vende; segundo análisis para confirmar |
| Lecturas de red muy distintas entre días | Tandeo con mezcla de fuentes: usa el promedio para clasificar y mide otra vez en la otra temporada |

!!! warning "Errores típicos"
    - Medir con el medidor sin calibrar, o con la sonda de pH guardada seca.
    - Medir la lluvia sin haber purgado el tlaloque: mides el techo, no la lluvia.
    - Comprar RO o dúplex antes de tener las 3 lecturas.
    - Mandar la muestra un viernes por la tarde (llega el lunes, caliente).
    - Usar el informe de laboratorio de hace un año en la carpeta para un hotel: vigencia < 6 meses.

## Al terminar

- [ ] Medidor calibrado; 3 lecturas de red + 1 de lluvia con fecha en `bitacora/agua.csv`
- [ ] Ruta del NFT decidida y escrita (directo / mezcla / lluvia-RO)
- [ ] Muestra al laboratorio al arrancar Fase 1; informe archivado y fila en `laboratorio.csv`
- [ ] Siguiente lectura de temporada y siguiente laboratorio en el calendario
- Registrar: filas de arriba; en `bitacora/produccion.csv`, `observaciones` con "riego desde tinaco" en la primera siembra que use esa agua
- Siguiente paso: [Fase 2 · Compras](../fases/fase-2/compras.md) (dúplex, RO o solo lluvia) · [Preparar solución nutritiva](../guias/preparar-solucion-nutritiva.md) · carpeta de inocuidad con [V10](v10-mock-recall.md)

## Fuentes

- [06 · Validación §V7 y §resumen operativo](../referencia/06-validacion-y-lazos-agenticos.md): pH y EC de red y lluvia al arrancar y por temporada; lluvia ≪ 0.3; red > 0.8; laboratorio anual (coliformes y metales).
- [research/agua-captacion §e](../research/agua-captacion.md): tabla de EC (< 0.4 / 0.4–0.8 / > 0.8), lluvia 0.02–0.06, pozos del oriente, RO ~$2,500–5,000, "medir 3 días distintos".
- [research/inocuidad-operativa §3 y §4](../research/inocuidad-operativa.md): laboratorios (LANISAF $542–607, Quibimex EMA, Agrolab, Eurofins), padrón EMA, plan de muestreo, precios de referencia, NOM-251 (agua de las últimas 48 h, cloro 0.2–1.5 ppm o UV), vigencia < 6 meses.
- [Fase 1 · Agua](../fases/fase-1/agua.md) y [Fase 2 · NFT](../fases/fase-2/nft.md): dónde cae la medición en el calendario; dúplex sedimento + carbón; cloro de red 0.2–1.5 mg/L.
- [Diseño · Hidráulico](../diseno/hidraulico.md): puntos de medición y frecuencia.
