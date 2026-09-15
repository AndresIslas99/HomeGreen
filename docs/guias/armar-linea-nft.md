# Armar una línea NFT

**En una línea:** conviertes medio tramo de PVC **sanitario** de 4" en una línea de 3 m con 10 sitios a 20 cm, con la entrada por el extremo alto, el retorno de 2" por el bajo y 2–3 % de pendiente, y la pruebas con 1 L de agua antes de que la toque una raíz — perforando con la sierra copa del diámetro que **mediste** en la canastilla, no del que dice la etiqueta.

!!! info "Antes de empezar"
    - **Tiempo:** ~2 h por línea después de la primera (estimado); las 8 líneas de Fase 2 caben en un fin de semana ([Fase 2 · NFT](../fases/fase-2/nft.md)) · **Costo por línea:** ½ tramo de tubo $208 + 2 tapas ~$60 + adaptador de drenaje ~$40 ≈ **$310–380** en PVC + 10 canastillas de 3" × $12.80 = $128; una sola vez: sierra copa Truper COBI ~$300 con mandril, cemento PVC 240 mL + limpiador ~$220, lima ~$60 ([research/hidroponia-nft §a](../research/hidroponia-nft.md), [04-herramientas](../referencia/04-herramientas.md)) · **Personas:** 2 para cortar y mover el tubo de 6 m; 1 para lo demás
    - **Necesitas:** [tubo sanitario Amanco 4" × 6 m blanco, $415](https://www.homedepot.com.mx/p/amanco-wavin-tubo-sanitario-11-x-600-cm-blanco-amanco-942842-451963) (½ por línea), tapas 4", adaptador de drenaje 4" → 2", niple o pasamuros para manguera de ½"–¾", [codo 45° $18.31 / 90° $28.80](https://www.homedepot.com.mx/p/amanco-wavin-codo-pvc-4-513695-513695) para el colector, [canastillas 3" $12.80](https://hydroenv.com.mx/producto/canastilla-hidroponica-de-3-pulgadas/) **ya en mano**, [sierra copa Truper COBI](https://listado.mercadolibre.com.mx/truper-sierra-corta-circulos-bimetalica) del diámetro medido + mandril, taladro, dos caballetes, vernier, flexómetro, hilo de gis o regla larga, segueta, lima o cuchilla, [cemento PVC + limpiador](https://www.homedepot.com.mx/p/cemento-para-pvc-240-ml-transparente-contact-104028-104028), nivel de 24" con cuña, 3 soportes de PTR 1" con media caña, botella de 1 L y cronómetro, lentes
    - **Prerequisitos:** canastillas compradas **antes** de perforar; plan de bancadas y tambo en [Fase 2 · NFT](../fases/fase-2/nft.md); porqués y tags en [Hidráulico §2](../diseno/hidraulico.md); modelo paramétrico en [`hardware/cad/linea_nft.scad`](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/linea_nft.scad)

## Cómo queda

![Render CAD de una línea NFT: tubo sanitario 4" × 3 m con 10 perforaciones a 20 cm entre centros para canastilla de 3", pendiente 2.5 %, 3 soportes de PTR 1", tapa con entrada de ½" en el extremo alto y retorno de 2" en el bajo](../assets/diagramas/cad/linea-nft.png)

![Animación del flujo en el NFT recirculante: la solución entra por el extremo alto, corre como película bajo las canastillas y regresa por el retorno al tambo](../assets/diagramas/animaciones/nft-flujo.svg)

La línea es el eslabón entre el manifold y el retorno del P&ID: entra ½"–¾" por el extremo **alto**, corre como película de 1–3 mm bajo las canastillas y sale por el extremo **bajo** a un colector de 2" que cae por gravedad al tambo ([P&ID completo](../assets/diagramas/hidraulico/nft-recirculacion.svg)).

| Parámetro | Valor | Por qué |
|---|---|---|
| Tubo | PVC **sanitario** 4" blanco (OD 114 mm), $415/6 m | El NFT corre sin presión; el hidráulico cédula 40 cuesta $1,401 sin beneficio; el blanco refleja calor (el naranja lo absorbe) |
| Largo | 3.0 m (½ tramo) | Sin desperdicio; cabe en el túnel de 5 × 6 m |
| Sitios | 10 a **20 cm** entre centros (albahaca, arúgula); 14 a 15 cm (cilantro) | [03-instalación §2.1](../referencia/03-instalacion.md); 9 × 20 cm = 1.8 m centrados dejan 60 cm libres en cada extremo para tapas y conexiones |
| Perforación | Ø del **cuerpo** de la canastilla bajo el labio, medido | Una "de 2 pulgadas" pide 44–48 mm, nunca 2" exactas; el modelo dibuja 70 mm para la de 3" solo como valor de render |
| Pendiente | **2–3 %** = 6–9 cm entre extremos (el modelo usa 2.5 % = 7.5 cm) | Menos: charco a media línea y raíces podridas; más: la película no moja el bloque |
| Soportes | 3, a 0.15 / 1.50 / 2.85 m (≤ 1.5 m entre ellos) | Sin panza |
| Caudal | **1–2 L/min** (1 L en 30–60 s con botella y cronómetro) | Película continua sin brincar las canastillas |

## Pasos

### A. Medir y probar (una sola vez, con la primera línea)

1. **Mide la canastilla, no la etiqueta.** Con vernier, mide el diámetro del cuerpo justo **debajo del labio**, en mm. Ese número es tu sierra copa; compra **una** de ese diámetro (no el kit de 9 piezas). Anótalo también en `d_perf` y `canastilla_cuerpo` del `.scad` si quieres el render con tu canastilla ([README CAD](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/README.md)).
2. **Perfora un retazo de 20 cm**, desbarba y prueba la canastilla.
   *Criterio de listo:* entra con el labio apoyado sobre el tubo, no baila (holgura ≤ 1 mm) y no cae al fondo. Si cae, la sierra es grande: la única salida es un anillo por sitio o repetir el tramo (½ tramo, $208). Si no entra, lima un poco el hoyo; nunca fuerces la canastilla.

### B. Cortar y marcar

3. **Corta el tramo de 6 m a la mitad** con segueta, a escuadra (marca el corte con una tira de papel envuelta al tubo), y desbarba los dos cortes. Salen dos líneas.
4. **Marca la generatriz** (la línea recta de perforación) a lo largo del tubo con hilo de gis o regla larga, con el tubo sobre los caballetes y la marca de fábrica hacia abajo. Si los hoyos se tuercen, las canastillas quedan inclinadas y las raíces tocan la película desigual.
5. **Marca los 10 centros a 20 cm** (15 cm para cilantro, 14 sitios) sobre la generatriz, dejando ~60 cm libres en cada extremo.
   *Criterio de listo:* la distancia entre el primer y el último centro es 1.80 m (2.10 m con cilantro) y quedan iguales los márgenes de los extremos.

### C. Perforar y desbarbar

6. **Perfora con la sierra copa a velocidad baja**, taladro perpendicular, broca piloto en la marca, tubo bien apoyado en los dos caballetes. No fuerces: el PVC se calienta y la rebaba se funde. Lentes puestos.
7. **Desbarba cada hoyo por fuera y por dentro** con lima o cuchilla y sacude o enjuaga las virutas que cayeron dentro del tubo: las rebabas atoran raíces y flujo, y las virutas tapan la malla 120 en el primer arranque.
   *Criterio de listo:* pasas el dedo por el borde de cada hoyo y no engancha; el interior del tubo está limpio.

### D. Tapas y conexiones

8. **Extremo alto (entrada):** tapa de 4" con niple o pasamuros para la manguera de ½"–¾" que viene del manifold, colocado en la mitad superior de la tapa para que el chorro caiga al piso del tubo y forme la película sin salpicar la primera canastilla.
9. **Extremo bajo (salida):** tapa de 4" con el adaptador de drenaje 4" → 2" en la **parte inferior** de la tapa, al ras del piso del tubo: si queda alto, deja charco permanente al final de la línea.
10. **Cementa** con limpiador + cemento regular (sin presión, basta) y deja curar lo que diga el envase antes de mojar.
    *Criterio de listo:* con la línea en el suelo y ambas tapas puestas, vertida 1 L de agua por la entrada sale por el drenaje sin gotear por las tapas.

### E. Soportes y pendiente

11. **Coloca la línea sobre 3 soportes** con media caña (0.15, 1.50 y 2.85 m desde el extremo alto), en la bancada que corresponde ([Fase 2 · NFT, paso 6](../fases/fase-2/nft.md)).
12. **Da la pendiente: 2–3 % = 6–9 cm entre entrada y salida.** Mide con el nivel de 24" y una cuña calibrada, o con las dos alturas marcadas en los soportes. Extremo alto hacia el manifold, bajo hacia el colector.
    *Criterio de listo:* 1 L vertido por la entrada cruza los 3 m sin detenerse ni dejar charco bajo ningún sitio; la burbuja del nivel confirma la caída en los tres tramos (sin panza entre soportes).

### F. Conectar y ajustar el caudal

13. **Entrada:** manguera desde la válvula de compuerta de esta línea en el manifold de ¾". **Salida:** al colector de 2" con codo de 45° (menos turbulencia que 90°); el colector lleva ≥ 1 % hacia el tambo y entra por la tapa **sin quedar sumergido** (sifonea y burbujea sobre las sondas).
14. **Ajusta el caudal con botella de 1 L y cronómetro:** bomba en marcha, válvula de la línea abierta; objetivo **30–60 s por litro (1–2 L/min)**. Cierra un poco si es la línea más cercana al manifold. Anota segundos y posición de la válvula.
    *Criterio de listo:* la película cubre el piso del tubo de punta a punta sin brincar por las canastillas ni "trepar" por los lados.
15. **Corre con agua sola** dentro de las 48 h de commissioning del sistema ([Fase 2 · NFT, paso 14](../fases/fase-2/nft.md)): revisa tapas, codos y niple a la 1, 6, 24 y 48 h.

### G. Canastillas y plantas

16. **Un bloque de foami por canastilla** (semillero de 144 bloques, $45.50; o cilindro de foami 4.3 × 5 cm, $2.90 para la de 3"). La base del bloque debe **tocar** la película, no quedar sumergida. Trasplanta cuando la raíz asoma por el bloque (10–14 días en albahaca).
17. **Etiqueta la línea** con fecha y lote en masking tape: `ALB-AAMMDD-Sxxx-L1`, el mismo formato que las charolas ([datos §1](../diseno/datos.md)).

!!! warning "Error típico: hoyo del diámetro nominal"
    "Canastilla de 3 pulgadas" no significa sierra copa de 3". El nominal es el labio; el cuerpo es menor. Perforar sin la canastilla en la mano es la forma más rápida de tirar $208.

!!! warning "Error típico: salida arriba de la tapa"
    Si el adaptador de drenaje no queda al ras del piso del tubo, el último tramo se convierte en charco: raíces sin oxígeno en el sitio 10 y sedimento acumulado. Lo mismo pasa con una panza entre soportes a más de 1.5 m.

!!! warning "Error típico: tubo hidráulico o naranja"
    El cédula 40 cuesta 3.4× y no aporta nada sin presión; el sanitario naranja absorbe calor y la solución sube de los 25 °C que matan el oxígeno disuelto. Sanitario blanco.

## Video de apoyo

Construcción con nomenclatura de tlapalería mexicana (usa PVC hidráulico; tú usas sanitario):

<iframe width="560" height="315" src="https://www.youtube.com/embed/PbnziwkUfus" title="Cómo hacer un sistema hidropónico NFT (México Verde)" frameborder="0" allowfullscreen></iframe>

Dimensionamiento (bomba, pendiente 2 %, espaciamiento) en la guía escrita de Hydro Environment ["NFT y su instalación"](https://hydroenv.com.mx/id102/) ([research/tutoriales-videos §b](../research/tutoriales-videos.md)).

## Al terminar

- [ ] Diámetro de sierra copa = cuerpo de la canastilla medido; la canastilla no baila ni cae en el retazo de prueba
- [ ] 10 hoyos (14 en cilantro) sobre una generatriz recta, desbarbados por dentro y por fuera; interior sin virutas
- [ ] Tapas cementadas: entrada arriba en el extremo alto, drenaje al ras del piso en el extremo bajo; sin goteo con 1 L de prueba
- [ ] Pendiente 2–3 % verificada con nivel y con 1 L de agua; soportes a ≤ 1.5 m sin panza
- [ ] Caudal 1–2 L/min anotado (segundos por litro y posición de válvula); colector de 2" no sumergido
- Registrar en `bitacora/nft.csv` (campos de [Fase 2 · NFT](../fases/fase-2/nft.md)): `fecha,evento,linea,caudal_L_min,nivel_tambo_pct,temp_solucion_C,observaciones` con `evento=linea_armada`, `linea=L1…L8`, `caudal_L_min` medido y en `observaciones` el Ø de sierra copa y la caída en cm
- Siguiente paso: [Fase 2 · NFT, bancadas y commissioning de 48 h](../fases/fase-2/nft.md) → [Preparar la solución nutritiva](preparar-solucion-nutritiva.md)

## Fuentes

- [referencia/03-instalacion §2.1](../referencia/03-instalacion.md) — tubo sanitario, perforación tras medir la canastilla, separación 20/15 cm, desbarbar, pendiente 2–3 %, soportes ≤ 1.5 m, caudal 1–2 L/min
- [research/hidroponia-nft §a, §b, §f](../research/hidroponia-nft.md) — precios de tubo y conexiones, costo por línea, canastillas, foami, blanco vs naranja
- [diseno/hidraulico §2](../diseno/hidraulico.md) — tags, manifold ¾", retorno 2", colector no sumergido · [fases/fase-2/nft](../fases/fase-2/nft.md) — bancadas, commissioning, germinación
- [`hardware/cad/linea_nft.scad`](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/linea_nft.scad) y [README](https://github.com/AndresIslas99/HomeGreen/blob/main/hardware/cad/README.md) — posiciones de soportes, 2.5 %, advertencia sobre `d_perf`
- [referencia/04-herramientas](../referencia/04-herramientas.md) y [research/herramientas](../research/herramientas.md) — sierra copa, cemento PVC, lima, nivel de 24"
- [research/tutoriales-videos §b](../research/tutoriales-videos.md) — México Verde (verificado), guía de Hydro Environment
