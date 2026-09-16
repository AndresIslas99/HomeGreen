# Verificación de enlaces

**En una línea:** el estado de los 679 enlaces externos de esta wiki la última vez que se
revisaron, para que sepas cuáles puedes abrir sin pensarlo y cuáles hay que confirmar a mano.

!!! info "Cómo se genera esta página"
    `python3 tools/check_links.py --salida docs/referencia/enlaces.md` y el workflow
    [`links.yml`](https://github.com/AndresIslas99/HomeGreen/blob/main/.github/workflows/links.yml)
    cada lunes. Las opciones están en [Herramientas CLI](../software/herramientas-cli.md#check_linkspy).

## Qué significa cada estado

| Estado | Qué probó | Qué haces |
|---|---|---|
| `ok` | El servidor contestó 2xx. Un video de YouTube se confirma con la API oEmbed, que además devuelve el canal | Nada. **460 enlaces** están así y no aparecen en la tabla de abajo |
| `redirect` | Contestó 2xx después de redirigir; la URL final está en la nota | Si el destino ya es otro producto, corrige el enlace y el precio |
| `blocked` | 403/429, timeout o conexión cortada. **No prueba que la página no exista:** Mercado Libre, Cloudflare y varios portales de gobierno de CDMX cortan la conexión a cualquier script o a IP fuera de México | Ábrelo en el navegador antes de darlo por muerto |
| `dead` | 404/410, dominio que no resuelve, video que oEmbed reporta retirado, o una ruta de este repositorio que no existe | Busca el equivalente y corrige la fila del BOM con el precio **y la fecha** |
| `dead (conocido)` | Muerto, ya anotado en la página que lo cita y listado en [`tools/enlaces-muertos-conocidos.txt`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/enlaces-muertos-conocidos.txt) | Nada: el workflow solo falla con un muerto **nuevo** |

!!! warning "Un enlace muerto es una partida del BOM que ya no puedes comprar"
    Los ocho muertos de hoy están todos en los informes de `docs/research/`, que son documentos
    históricos: registran qué se consultó el 12-sep-2026. Por eso no se borran, se anotan. Ninguna
    página de compras, de fase o de guía tiene un enlace roto.

## Los enlaces que no son `ok`

Los 460 verificados correctamente no se listan (la tabla sería ilegible). Aquí están los
`redirect`, los `blocked` y los `dead`:

| Estado | HTTP | URL | Dónde | Nota |
| dead (conocido) | 404 | http://www.cultivarte.com.mx/producto/cubo-lana-de-roca-3x3x25 | docs/research/hidroponia-nft.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://hydrocultura.com/collections/plasticos-para-invernadero-y-acolchados/rollos-de-plastico-invernadero-mexico | docs/research/estructura-invernadero.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://hydroenv.com.mx/catalogo/index.php?main_page=product_info&products_id=140 | docs/research/hidroponia-nft.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://magnefix.com.mx/impresion-de-etiquetas-adhesivas-cdmx/ | docs/research/semillas-sustrato-charolas.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://www.gob.mx/cms/uploads/attachment/file/996969/COFEPRIS-05-018.pdf | docs/research/normativa-fiscal.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://www.hanlob.com.mx/producto/malla-antigranizo-cristal-3-7-mt-ancho-x-100-mt-largo/ | docs/research/estructura-invernadero.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://www.homedepot.com.mx/bombas/bomba-periferica-de-05-hp-137488 | docs/research/agua-captacion.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| dead (conocido) | 404 | https://yema.mx/p/microgreens-de-girasol | docs/research/mercado-precios.md | HTTP 404 (GET); ya anotado en la página que lo cita |
| blocked |  | https://alocasiamx.com/microgreens/ | docs/research/mercado-precios.md | dominio dinámico: no verificado |
| blocked | propio | https://andresislas99.github.io/HomeGreen/ | docs/empieza-aqui/como-usar-esta-guia.md, README.md | sitio del proyecto: 404 hasta habilitar Settings → Pages → Source: GitHub Actions |
| blocked | TLS | https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/Tarifa1.aspx | docs/referencia/normativa.md, docs/research/puntos-ciegos.md | TLS: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local  |
| blocked | TLS | https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/TarifaDAC.aspx | docs/referencia/normativa.md, docs/research/puntos-ciegos.md | TLS: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local  |
| blocked |  | https://bascomex.com/products/filtro-de-1-pulgada-malla-palaplast-120-mesh | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked | conn | https://bpack.mx/blog/aviso-funcionamiento-cofepris-alimentos | docs/guias/aviso-cofepris.md, docs/referencia/normativa.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | 403 | https://community.home-assistant.io/t/atlas-scientific-wi-fi-hydroponics-kit-example-yaml/538083 | docs/aprendizaje/videos.md, docs/referencia/05-aprendizaje.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | 403 | https://community.home-assistant.io/t/implementing-analog-ph-sensor-of-dfrobot/714202 | docs/aprendizaje/videos.md, docs/guias/calibrar-sondas-ph-ec.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | conn | https://cosechalluvia.sedema.cdmx.gob.mx/ | docs/fases/fase-1/agua.md, docs/guias/aplicar-cosecha-de-lluvia.md, docs/referencia/normativa.md (+1) | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | 403 | https://cursos.aprende.gob.mx/courses/course-v1:COFEPRIS+CSDF26041X+2026_04/about | docs/aprendizaje/cursos.md, docs/empieza-aqui/antes-de-gastar-un-peso.md, docs/guias/aviso-cofepris.md (+3) | HTTP 403 (GET) |
| blocked | 499 | https://en.climate-data.org/north-america/mexico/federal-district/mexico-city-1093/ | docs/referencia/clima.md, docs/research/clima-agronomia.md | HTTP 499 (GET) |
| blocked | propio | https://github.com/AndresIslas99/HomeGreen.git | docs/empieza-aqui/como-usar-esta-guia.md | repositorio del proyecto: GitHub contesta 404 mientras sea privado |
| blocked | propio | https://github.com/AndresIslas99/HomeGreen/issues | docs/empieza-aqui/como-usar-esta-guia.md | repositorio del proyecto: GitHub contesta 404 mientras sea privado |
| blocked | 403 | https://github.com/greenponik/DFRobot_ESP_PH_BY_GREENPONIK | docs/aprendizaje/videos.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | 403 | https://github.com/makstech/esphome-irrigation-system | docs/aprendizaje/videos.md, docs/referencia/05-aprendizaje.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | 403 | https://github.com/r0bb10/ESPHome-DFRobot-pH-Meter | docs/aprendizaje/videos.md, docs/guias/calibrar-sondas-ph-ec.md, docs/referencia/05-aprendizaje.md (+2) | HTTP 403 (GET) |
| blocked | conn | https://gobierno.cdmx.gob.mx/noticias/sumate-al-programa-de-cosecha-de-lluvia/ | docs/guias/aplicar-cosecha-de-lluvia.md, docs/research/agua-captacion.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | 403 | https://greengrow.com.mx/categoria/lamparas-para-crecimiento-de-plantas/led/ | docs/research/clima-agronomia.md | HTTP 403 (GET) |
| blocked | TLS | https://inverfarms.com/product/espuma-hidroponica-oasis-aero-max/ | docs/research/hidroponia-nft.md | TLS: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl. |
| blocked |  | https://laboratorioquibimex.com/ | docs/guias/mock-recall.md, docs/referencia/01-proveedores-cdmx.md, docs/referencia/normativa.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx | docs/referencia/bom.md, docs/research/herramientas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/acido-peracetico | docs/guias/sanitizar-semilla.md, docs/research/inocuidad-operativa.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/anaquel-estante-metalico-5-niveles | docs/research/estructura-invernadero.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bascula-de-precision-0.1g | docs/fases/fase-0/compras.md, docs/guias/sembrar-una-charola.md, docs/referencia/04-herramientas.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bascula-digital-cocina | docs/fases/fase-0/compras.md, docs/guias/cosechar-y-empacar.md, docs/referencia/04-herramientas.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bateria-agm-ciclo-profundo-12v-100ah | docs/research/electrico-respaldo-seguridad.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bateria-lifepo4-12v-100ah | docs/research/electrico-respaldo-seguridad.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-agua-12v | docs/research/puntos-ciegos.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-de-agua-diafragma-12v | docs/diseno/hidraulico.md, docs/fases/fase-1/compras.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-diafragma-12v | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/guias/armar-respaldo-dc.md (+3) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-periferica-truper | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-peristaltica-12v | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/referencia/01-proveedores-cdmx.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bomba-sumergible-12v-1100gph | docs/research/electrico-respaldo-seguridad.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bombas-presurizadoras-rotoplas | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bombas-sumergible-para-estanque | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/bti-larvicida | docs/research/clima-agronomia.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/captador-de-agua-pluvial | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/careta-esmerilar-truper | docs/research/herramientas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/cargador-lifepo4-14.6v-10a | docs/fases/fase-2/compras.md, docs/guias/armar-respaldo-dc.md, docs/research/electrico-respaldo-seguridad.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/charolas-microgreens | docs/research/mercado-precios.md, docs/research/semillas-sustrato-charolas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/charolas-para-microgreens | docs/fases/fase-0/compras.md, docs/guias/sembrar-una-charola.md, docs/referencia/01-proveedores-cdmx.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/clamshell | docs/fases/fase-0/compras.md, docs/guias/cosechar-y-empacar.md, docs/referencia/01-proveedores-cdmx.md (+3) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/computacion/pc-escritorio/mini-pc/lenovo/usado/ | docs/research/electronica-automatizacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/cubos-lana-de-roca-hidroponia | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/esp32-cam | docs/research/electronica-automatizacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/fertilizante-hakaphos-violeta | docs/guias/preparar-solucion-nutritiva.md, docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/fibra-de-coco | docs/research/semillas-sustrato-charolas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/filtro-para-agua-120-mesh-1-pulgada | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/filtro-sedimentos-y-carbon | docs/diseno/hidraulico.md, docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/filtros-de-carbon-activado-para-agua | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/gabinete-plastico-exterior-ip65 | docs/fases/fase-1/compras.md, docs/guias/montar-gabinete-ip65.md, docs/referencia/04-herramientas.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/general-hydroponics-flora-series | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/hielera-45-litros | docs/fases/fase-2/compras.md, docs/guias/ruta-de-reparto.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/hipoclorito-de-calcio | docs/fases/fase-0/compras.md, docs/guias/sanitizar-semilla.md, docs/referencia/01-proveedores-cdmx.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/invernadero-prefabricado | docs/research/estructura-invernadero.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/jabon-potasico-insecticida | docs/guias/control-de-plagas.md, docs/research/clima-agronomia.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/lampara-led-full-spectrum | docs/research/clima-agronomia.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/libro-hidroponia-basica-gloria-samperio | docs/aprendizaje/libros.md, docs/research/libros-cursos.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/libros-microgreens | docs/research/libros-cursos.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/malla-antigranizo | docs/research/instalacion-tunel-detalle.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/medidor-ph-tds-ec | docs/empieza-aqui/antes-de-gastar-un-peso.md, docs/fases/fase-1/agua.md, docs/fases/fase-2/compras.md (+5) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/microgreens | docs/research/mercado-precios.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/mini-pc-lenovo-thinkcentre | docs/fases/fase-1/compras.md, docs/guias/configurar-home-assistant.md, docs/referencia/01-proveedores-cdmx.md (+3) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/nebulizadores-de-riego | docs/diseno/hidraulico.md, docs/fases/fase-1/compras.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/nitrato-calcio-25-kg | docs/guias/preparar-solucion-nutritiva.md, docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/no-break-500va | docs/fases/fase-1/compras.md, docs/guias/configurar-home-assistant.md, docs/referencia/bom.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/peroxido-de-hidrogeno-35%25-grado-alimenticio-oxigeno-liquido | docs/fases/fase-0/compras.md, docs/guias/control-de-plagas.md, docs/guias/lavar-y-desinfectar-charolas.md (+4) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/peroxido-de-hidrogeno-grado-alimenticio | docs/research/inocuidad-operativa.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/petrifilm | docs/research/inocuidad-operativa.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/poste-galvanizado | docs/research/estructura-invernadero.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/refrigerador-usado | docs/fases/fase-2/compras.md, docs/referencia/bom.md, docs/research/puntos-ciegos.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/semilla-de-girasol-para-germinar | docs/research/semillas-sustrato-charolas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/semilla-de-girasol-por-kilo-y-por-bulto | docs/research/semillas-sustrato-charolas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/semillas-de-albahaca-genovesa | docs/research/clima-agronomia.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/semillas-para-microgreens | docs/research/semillas-sustrato-charolas.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/sensor-de-flujo-de-agua-yf-s201 | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/sensor-de-temperatura-y-humedad-dht22 | docs/research/electronica-automatizacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/separador-de-primeras-lluvias | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/sistema-captacion-agua-de-lluvia | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/solucion-buffer-para-calibrar-ph | docs/fases/fase-2/compras.md, docs/guias/calibrar-sondas-ph-ec.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tambos-de-200-litros | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/referencia/01-proveedores-cdmx.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tapete-termico-germinacion | docs/fases/fase-0/compras.md, docs/fases/fase-1/compras.md, docs/guias/germinar-en-invierno.md (+4) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tinaco-750-litros | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tinaco-rotoplas-750-litros | docs/research/agua-captacion.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/trampas-amarillas-pegajosas | docs/fases/fase-1/compras.md, docs/guias/control-de-plagas.md, docs/referencia/01-proveedores-cdmx.md (+3) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/truper-sierra-corta-circulos-bimetalica | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/guias/armar-linea-nft.md (+3) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tubo-galvanizado-cedula-30 | docs/research/estructura-invernadero.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tubo-led-t8-120-cm | docs/research/clima-agronomia.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/tubo-pvc-4-pulgadas-6-metros | docs/research/hidroponia-nft.md | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/valvula-solenoide-12v-1-2 | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/referencia/bom.md (+1) | dominio dinámico: no verificado |
| blocked |  | https://listado.mercadolibre.com.mx/varilla-copperweld-5-8-3-metros | docs/guias/instalar-gfci-y-tierra.md, docs/research/electrico-respaldo-seguridad.md | dominio dinámico: no verificado |
| blocked | 403 | https://medium.com/@pedrohora/building-a-smart-garden-irrigation-system-with-esp32-esphome-home-assistant-and-node-red-c3c4fb78b457 | docs/aprendizaje/videos.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | 403 | https://mexico.justia.com/estados/df/leyes/ley-de-propiedad-en-condominio-de-inmuebles-para-el-distrito-federal/ | docs/referencia/normativa.md, docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | 403 | https://microgreenswebclass.com/tuf | docs/research/cobranza-b2b.md | HTTP 403 (GET) |
| blocked | 403 | https://plast-tel.mx/producto/malla-antigranizo-por-metro/ | docs/research/clima-agronomia.md | HTTP 403 (GET) |
| blocked | 403 | https://pubmed.ncbi.nlm.nih.gov/32144769/ | docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | 403 | https://pubmed.ncbi.nlm.nih.gov/36836750/ | docs/guias/cosechar-y-empacar.md, docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | conn | https://sca.sacmex.cdmx.gob.mx:8447/ | docs/research/agua-captacion.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://sedema.cdmx.gob.mx/programas/programa/altepetl | docs/referencia/normativa.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://siapem.cdmx.gob.mx/ | docs/referencia/normativa.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked |  | https://sistemadehuertosurbanoscdmx.com/ | docs/research/normativa-fiscal.md | dominio dinámico: no verificado |
| blocked | conn | https://tusmicrogreens.com/products/curso-completo-microgreens | docs/research/tutoriales-videos.md | conexión rechazada (Tunnel connection failed: 502 Bad Gateway); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | 403 | https://ucanr.edu/statewide-program/uc-anr-small-farms-network/selling-restaurants | docs/research/cobranza-b2b.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com | docs/referencia/01-proveedores-cdmx.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/categoria-producto/modulos/relevadores-modulos/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/categoria-producto/tarjetas-desarrollo/esp32/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/ds18b20-sensor-de-temperatura-digital-de-acero-inoxidable-sumergible/ | docs/diseno/hidraulico.md, docs/fases/fase-1/compras.md, docs/referencia/bom.md (+1) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/electrovalvula-solenoide-1-2-pulgada-nc/ | docs/diseno/hidraulico.md, docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/esp32-cam-ov2640-con-ch340-wifi-bluetooth/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/esp32-cam-ov2640-v3-con-interfaz-tipo-c/ | docs/fases/fase-2/compras.md, docs/referencia/bom.md, docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/esp32-devkit-v1-30-pines-usb-c-microusb/ | docs/fases/fase-1/compras.md, docs/guias/flashear-esphome.md, docs/referencia/01-proveedores-cdmx.md (+2) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/esp32-devkitc-v4-esp32-wroom-32d-32u/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/fuente-conmutada-12v-5a/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/kit-sensor-de-ph-analogico-con-soluciones-de-calibracion-sen0161-v2/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/relevador-5v-de-1-a-8-canales/ | docs/fases/fase-1/compras.md, docs/guias/armar-respaldo-dc.md, docs/referencia/bom.md (+1) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/relevadores-12v-de-124-y-8-canales/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-de-humedad-suelo-capacitivo-anticorrosivo/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-de-ph-liquido/ | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/referencia/01-proveedores-cdmx.md (+2) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-de-temperatura-dht22-am2302/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-de-temperatura-y-humedad-dht22-con-cables/ | docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-tds-meter-v1-0-analogico-sen0244/ | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/guias/calibrar-sondas-ph-ec.md (+3) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/sensor-ultrasonico-jns-sr04t/ | docs/diseno/hidraulico.md, docs/fases/fase-1/compras.md, docs/referencia/bom.md (+1) | HTTP 403 (GET) |
| blocked | 403 | https://uelectronics.com/producto/xlg-75-12-a-fuente-conmutada-12v-5a-ip67-mean-well/ | docs/fases/fase-1/compras.md, docs/referencia/01-proveedores-cdmx.md, docs/research/electronica-automatizacion.md | HTTP 403 (GET) |
| blocked |  | https://www.abolawlex.com/post/qu%C3%A9-tipo-de-socios-o-accionistas-no-pueden-pertenecer-al-resico | docs/research/normativa-fiscal.md | dominio dinámico: no verificado |
| blocked | conn | https://www.alnatural.com.mx/tienda/charolas-de-germinacion-venta-mayoreo | docs/fases/fase-0/compras.md, docs/guias/sembrar-una-charola.md, docs/referencia/01-proveedores-cdmx.md (+2) | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/fibra-de-coco-sustrato-venta | docs/research/semillas-sustrato-charolas.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/semilla-de-brocoli | docs/research/semillas-sustrato-charolas.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/semilla-de-chicharo-sin-tratamiento | docs/research/semillas-sustrato-charolas.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/semilla-de-girasol-para-microgreens | docs/fases/fase-0/compras.md, docs/guias/sembrar-una-charola.md, docs/referencia/01-proveedores-cdmx.md (+3) | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/semilla-de-rabano | docs/research/semillas-sustrato-charolas.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.alnatural.com.mx/tienda/venta-rollo-plastico-para-invernadero | docs/research/estructura-invernadero.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | TLS | https://www.bsai.com.mx/products/gabinete-plastico-para-exterior-ip65-de-300-x-300-x-90-mm-cierre-por-tornillos | docs/guias/montar-gabinete-ip65.md, docs/research/herramientas.md | TLS: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1016) |
| blocked | 403 | https://www.capitalmexico.com.mx/tema-dia/7-alcaldias-de-la-cdmx-distribuyen-agua-de-mala-calidad/ | docs/research/agua-captacion.md | HTTP 403 (GET) |
| blocked | timeout | https://www.coppel.com/blog/finanzas/como-abrir-un-restaurante-pasos-clave-para-emprender-ppc/ | docs/research/cobranza-b2b.md | timeout 20 s: no responde desde aquí; ábrelo en el navegador antes de darlo por muerto |
| blocked | 403 | https://www.debate.com.mx/consejos/el-peligro-del-recibo-de-luz-el-limite-de-consumo-para-no-perder-el-subsidio-de-la-cfe-en-mexico-20260702-0112.html | docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | conn | https://www.edicionesatalanta.com/catalogo/el-jardinero-horticultor/ | docs/aprendizaje/libros.md, docs/research/libros-cursos.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | 403 | https://www.elmanana.com/opinion/columnas/mexicanos-gastan-menos-en-restaurantes-canirac-propone-esto-6179619.html | docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | 403 | https://www.engineeringforchange.org/wp-content/uploads/2020/07/MANUAL-INSTALACI%C3%93N-KIT-TL%C3%81LOC-12-JUNIO-2019CH.pdf | docs/aprendizaje/libros.md, docs/aprendizaje/videos.md, docs/diseno/hidraulico.md (+9) | HTTP 403 (GET) |
| blocked |  | https://www.facebook.com/CdeAbastoCDMX | docs/research/mercado-precios.md | dominio dinámico: no verificado |
| blocked | 401 | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-reducing-microbial-food-safety-hazards-production-seed-sprouting | docs/guias/sanitizar-semilla.md, docs/referencia/normativa.md, docs/research/inocuidad-operativa.md | HTTP 401 (GET) |
| blocked |  | https://www.imprentacdmx.com/servicios-de-impresion/impresion-de-etiquetas-adhesivas/ | docs/fases/fase-0/compras.md, docs/guias/cosechar-y-empacar.md, docs/referencia/01-proveedores-cdmx.md (+2) | dominio dinámico: no verificado |
| blocked |  | https://www.instagram.com/microverdesdelaciudad/ | docs/research/mercado-precios.md | dominio dinámico: no verificado |
| blocked |  | https://www.invernaderosmx.com/collections/plastico-5-transparente | docs/fases/fase-1/compras.md, docs/referencia/01-proveedores-cdmx.md, docs/research/estructura-invernadero.md | dominio dinámico: no verificado |
| blocked | 403 | https://www.jornada.com.mx/noticia/2026/02/23/capital/alerta-por-frio-y-heladas-en-cdmx-cinco-alcaldias-con-temperaturas-bajo-cero | docs/referencia/clima.md, docs/research/clima-agronomia.md | HTTP 403 (GET) |
| blocked | 403 | https://www.jornada.com.mx/noticia/2026/05/25/capital/lluvias-y-granizo-causan-estragos-en-la-cdmx | docs/research/clima-agronomia.md | HTTP 403 (GET) |
| blocked | 403 | https://www.mibolsillo.com/tips/cfe-2026-la-razon-por-la-que-perderias-el-subsidio-de-energia-20260829-0025.html | docs/research/puntos-ciegos.md | HTTP 403 (GET) |
| blocked | 403 | https://www.proveedores.com/proveedores/costean-microgreens/ | docs/research/mercado-precios.md | HTTP 403 (GET) |
| blocked | 403 | https://www.quiminet.com/productos/malla-antigranizo-14246351640/precios.htm | docs/research/estructura-invernadero.md | HTTP 403 (GET) |
| blocked | 403 | https://www.quiminet.com/proveedores/clamshell-80337230523.htm | docs/research/semillas-sustrato-charolas.md | HTTP 403 (GET) |
| blocked | 403 | https://www.quiminet.com/proveedores/empaque-tipo-clamshell-43471604278.htm | docs/research/semillas-sustrato-charolas.md | HTTP 403 (GET) |
| blocked | 403 | https://www.reef2reef.com/threads/diy-my-dose-%E2%80%94-open-source-dosing-controller-built-on-esp32-home-assistant.1151856/ | docs/aprendizaje/videos.md, docs/referencia/05-aprendizaje.md, docs/research/tutoriales-videos.md | HTTP 403 (GET) |
| blocked | conn | https://www.sacmex.cdmx.gob.mx/calidad-agua/analisis-calidad-del-agua | docs/research/agua-captacion.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedeco.cdmx.gob.mx/tramites/sistema-electronico-de-avisos-y-permisos-de-establecimientos-mercantiles-siapem | docs/referencia/normativa.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/comunicacion/nota/avanza-instalacion-de-huertos-urbanos-en-unidades-habitacionales-de-la-ciudad-de-mexico | docs/referencia/normativa.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/comunicacion/nota/busca-sedema-instalar-10-mil-sistemas-de-cosecha-de-lluvia-bajo-subsidio-parcial | docs/guias/aplicar-cosecha-de-lluvia.md, docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/comunicacion/nota/instala-gobierno-capitalino-20-mil-145-sistemas-de-cosecha-de-lluvia-en-cinco-alcaldias | docs/research/normativa-fiscal.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/comunicacion/nota/sedema-lanza-convocatoria-para-el-seminario-taller-escuela-de-huertos-urbanos | docs/aprendizaje/cursos.md, docs/empieza-aqui/antes-de-gastar-un-peso.md, docs/guias/aviso-cofepris.md (+4) | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/programas/programa/cosecha-de-lluvia | docs/empieza-aqui/antes-de-gastar-un-peso.md, docs/fases/fase-1/agua.md, docs/guias/aplicar-cosecha-de-lluvia.md (+4) | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | conn | https://www.sedema.cdmx.gob.mx/storage/app/media/DGCPCA/gacetareglas-de-operacion-del-programacosecha-de-lluvia.pdf | docs/guias/aplicar-cosecha-de-lluvia.md, docs/referencia/normativa.md, docs/research/agua-captacion.md | conexión rechazada ([Errno 104] Connection reset by peer); suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano |
| blocked | err | https://www.uplaw.com.mx/post/qué-puede-hacer-una-pyme-cuando-sus-clientes-no-le-pagan | docs/guias/cobrar-y-suspender.md, docs/referencia/normativa.md, docs/research/cobranza-b2b.md | error: UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 13:  |
| blocked | TLS | https://wwwmat.sat.gob.mx/consultas/53693/catalogo-de-productos-y-servicios | docs/guias/facturar-cfdi.md, docs/referencia/normativa.md, docs/research/normativa-fiscal.md | TLS: [SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1016) |
| blocked | TLS | https://wwwmatnp.sat.gob.mx/articulo/06071/articulo-2-a | docs/referencia/normativa.md, docs/research/normativa-fiscal.md | TLS: [SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1016) |
| redirect | 200 | http://boletinsgm.igeolcu.unam.mx/bsgm/index.php/component/content/article/273-sitio/articulos/cuarta-epoca/6702/1318-6702-12-dominguez | docs/research/agua-captacion.md | → https://boletinsgm.igeolcu.unam.mx/bsgm/index.php/component/content/article/273-sitio/articulos/cuarta-epoca/6702/1318-6702-12-dominguez |
| redirect | 200 | http://sistemas.senasica.gob.mx/hortalizas/ | docs/research/normativa-fiscal.md | → http://sistemas.senasica.gob.mx/maintenance.html |
| redirect | 200 | http://www.valent.mx/productos/insecticidas/gnatrol | docs/fases/fase-1/compras.md, docs/guias/control-de-plagas.md, docs/referencia/01-proveedores-cdmx.md (+3) | → https://www.valent.mx/productos/insecticidas/gnatrol |
| redirect | 200 | https://agrolab.com.mx/ | docs/research/inocuidad-operativa.md | → https://www.agrolab.com.mx/v003/ |
| redirect | 200 | https://aldase.com.mx/producto/hakaphos-violeta-13-40-13-25-kg/ | docs/guias/preparar-solucion-nutritiva.md, docs/research/hidroponia-nft.md | → https://aldase.com.mx/cgi-sys/suspendedpage.cgi |
| redirect | 200 | https://articulo.mercadolibre.com.mx/MLM-1406745221-estante-whalen-de-5-repisas-ajustables-capacidad-para-2200kg-_JM | docs/research/estructura-invernadero.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Farticulo.mercadolibre.com.mx%2FMLM-1406745221-estante-whalen-de-5-repisas-ajustables-capacidad-para-2200kg-_JM&tid=9459f5a7-7d52-4c5c-97c5-776e6715fa2f |
| redirect | 200 | https://articulo.mercadolibre.com.mx/MLM-1923449949-semillas-varias-para-germinados-brotes-o-microgreens-700-g-_JM | docs/research/semillas-sustrato-charolas.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Farticulo.mercadolibre.com.mx%2FMLM-1923449949-semillas-varias-para-germinados-brotes-o-microgreens-700-g-_JM&tid=a6feb734-6d8d-405b-b6e1-159025b65f25 |
| redirect | 200 | https://articulo.mercadolibre.com.mx/MLM-2050379399-modulo-de-sensor-de-humedad-sht31-temperatura-sht31-d-microc-_JM | docs/fases/fase-1/compras.md, docs/referencia/bom.md, docs/research/electronica-automatizacion.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Farticulo.mercadolibre.com.mx%2FMLM-2050379399-modulo-de-sensor-de-humedad-sht31-temperatura-sht31-d-microc-_JM&tid=837ad592-13bc-479b-aafc-847b1dfb9695 |
| redirect | 200 | https://articulo.mercadolibre.com.mx/MLM-625789531-microgreens-brotes-minivegetales-cdmx-_JM | docs/research/mercado-precios.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Farticulo.mercadolibre.com.mx%2FMLM-625789531-microgreens-brotes-minivegetales-cdmx-_JM&tid=7bde7989-f20a-4f02-a659-8268e7693326 |
| redirect | 200 | https://articulo.mercadolibre.com.mx/MLM-778305835-clamshell-contenedor-bisagra-plastico-frutas-berries-1-lbs-_JM | docs/research/semillas-sustrato-charolas.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Farticulo.mercadolibre.com.mx%2FMLM-778305835-clamshell-contenedor-bisagra-plastico-frutas-berries-1-lbs-_JM&tid=10f96fcc-d2dd-4c3e-80e1-09caba75ca84 |
| redirect | 200 | https://bricomark.mx/producto/tubo-pvc-hidraulico-cedula-40-x-6-metros-de-4-15-40-kg-cm2-futura/ | docs/research/hidroponia-nft.md | → https://bricomark.mx/producto/tubo-pvc-hidraulico-cedula-40-de-102mm-de-4-x-6-metros-15-40-kg-cm2-cresco/ |
| redirect | 200 | https://canirac.org.mx/ | docs/research/inocuidad-operativa.md | → https://portal.canirac.org.mx/ |
| redirect | 200 | https://formencia.com/course/cultivo-hidroponico-desde-cero/ | docs/aprendizaje/cursos.md, docs/research/libros-cursos.md | → https://formencia.com/course/hidroponia-2 |
| redirect | 200 | https://hogar.mercadolibre.com.mx/jardin-exterior-invernaderos/tunel-invernadero | docs/research/estructura-invernadero.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Fhogar.mercadolibre.com.mx%2Fjardin-exterior-invernaderos%2Ftunel-invernadero&tid=dcf6c94e-6c12-4c4f-a3ff-f27fea10dc0a |
| redirect | 200 | https://hydroenv.com.mx/categoria-de-productos/57/ | docs/research/semillas-sustrato-charolas.md | → https://hydroenv.com.mx/charolas-de-germinacion/ |
| redirect | 200 | https://hydroenv.com.mx/id102/ | docs/aprendizaje/videos.md, docs/fases/fase-2/nft.md, docs/guias/armar-linea-nft.md (+2) | → https://hydroenv.com.mx/guia-nft-y-su-instalacion/ |
| redirect | 200 | https://hydroenv.com.mx/id535/ | docs/aprendizaje/videos.md, docs/referencia/05-aprendizaje.md, docs/research/tutoriales-videos.md | → https://hydroenv.com.mx/como-armar-un-invernadero-casero-para-patio-hydro-crop-guia-en-13-pasos/ |
| redirect | 200 | https://hydroenv.com.mx/producto/1106-invernadero-mini-green-de-6-x-5-metros-a-un-tunel-de-superficie-de-30-m2-estructura-y-cubierta/ | docs/research/estructura-invernadero.md | → https://hydroenv.com.mx/producto/invernadero-mini-green-6x6-m-36m2-tunel-agricola/ |
| redirect | 200 | https://hydroenv.com.mx/producto/1623-invernadero-hidroponico-tipo-tunel-de-5-x-6-metros/ | docs/research/estructura-invernadero.md | → https://hydroenv.com.mx/producto/invernadero-hidroponico-5x6-m-para-fvh-y-hortalizas/ |
| redirect | 200 | https://hydroenv.com.mx/producto/1811-gramo-de-semilla-albahaca-var-italian-large-leaf/ | docs/referencia/01-proveedores-cdmx.md, docs/research/clima-agronomia.md | → https://hydroenv.com.mx/producto/gramo-de-semilla-de-albahaca-variedad-italian-large-leaf/ |
| redirect | 200 | https://hydroenv.com.mx/producto/363-rollo-de-plastico-para-invernadero-25-sombra-de-6-2-x-85-m-cal-720-100-kg/ | docs/research/estructura-invernadero.md | → https://hydroenv.com.mx/producto/plastico-para-invernadero-25-sombra-rollo-6-2-x-85-m-cal-720-100-kg/ |
| redirect | 200 | https://hydroenv.com.mx/producto/406-rollo-de-malla-sombra-para-invernadero-al-35-de-3-7-m-de-ancho/ | docs/research/clima-agronomia.md | → https://hydroenv.com.mx/producto/rollo-de-malla-sombra-para-invernadero-al-35-de-3-7-m-de-ancho/ |
| redirect | 200 | https://insumoscerveceros.mx/inicio/1305-solucion-para-calibracion-de-ph-buffer-401-120-ml.html | docs/diseno/hidraulico.md, docs/fases/fase-2/compras.md, docs/guias/calibrar-sondas-ph-ec.md (+3) | → https://insumoscerveceros.mx/products/solucion-para-calibracion-de-ph-buffer-401-120-ml |
| redirect | 200 | https://netacero.com/filtro-pluvial/ | docs/research/agua-captacion.md | → https://netacero.com/wp-content/uploads/2025/11/Filtro-Pluvial.webp |
| redirect | 200 | https://producesafetyalliance.cornell.edu/ | docs/research/inocuidad-operativa.md | → https://cals.cornell.edu/produce-safety-alliance |
| redirect | 200 | https://programacasasegura.org | docs/guias/instalar-gfci-y-tierra.md, docs/referencia/normativa.md, docs/research/electrico-respaldo-seguridad.md | → https://www.programacasasegura.org/ |
| redirect | 200 | https://sodimac.com.mx/sodimac-mx/content/tipos-de-entrega/ | docs/research/instalacion-tunel-detalle.md | → https://www.sodimac.com.mx/sodimac-mx/content/tipos-de-entrega |
| redirect | 200 | https://surtiaceros.com/producto/tubo-galvanizado-para-cerco-1-5-8-c-18-x-6-00-mts/ | docs/research/estructura-invernadero.md | → https://surtiaceros.com/?s=tubo%20galvanizado%20para%20cerco%201%205%208%20c%2018%20x%206%2000%20mts |
| redirect | 200 | https://www.donnygreens.com/ | docs/aprendizaje/cursos.md, docs/aprendizaje/videos.md, docs/research/tutoriales-videos.md | → https://www.donnygreens.com/dg-home |
| redirect | 200 | https://www.eurofins.com.mx/agro-alimentario/microbiolog%C3%ADa/ | docs/research/inocuidad-operativa.md | → https://www.eurofins.com/es-mx/analisis-alimentos-mexico/ |
| redirect | 200 | https://www.fao.org/3/i3846s/i3846s.pdf | docs/aprendizaje/libros.md, docs/empieza-aqui/antes-de-gastar-un-peso.md, docs/referencia/05-aprendizaje.md (+1) | → https://openknowledge.fao.org/server/api/core/bitstreams/a7b544d0-a107-4616-a05e-f88a2de6a7ce/content |
| redirect | 200 | https://www.homedepot.com.mx/p/cemento-para-pvc-240-ml-transparente-contact-104028-104028 | docs/guias/armar-linea-nft.md, docs/referencia/04-herramientas.md, docs/research/herramientas.md | → https://www.homedepot.com.mx/p/cemento-solvente-para-tuberia-pvc-240ml-sellado-resistente-transparente-104028-104028 |
| redirect | 200 | https://www.homedepot.com.mx/p/husky-estante-de-5-niveles-de-acero-183-x-12192-x-61-cm-negro-zrop482472-5llb-150283 | docs/diseno/rack-y-charolas.md, docs/research/estructura-invernadero.md | → https://www.homedepot.com.mx/p/husky-estante-acero-5-niveles-181439-kg-de-carga-183-x-12192-x-61-cm-multiusos-zrop482472-5llb-150283 |
| redirect | 200 | https://www.homedepot.com.mx/p/husky-estante-de-5-niveles-de-acero-183-x-914-x-457-cm-negro-zrop361872-5llb-150281 | docs/diseno/hidraulico.md, docs/diseno/rack-y-charolas.md, docs/fases/fase-0/compras.md (+4) | → https://www.homedepot.com.mx/p/husky-estante-acero-5-niveles-181439-kg-de-carga-183-x-914-x-457-cm-alta-resistencia-zrop361872-5llb-150281 |
| redirect | 200 | https://www.homedepot.com.mx/p/truper-rotomartillo-1-2-650w-truper-pro-roto-1-2a7-231999 | docs/guias/anclar-el-tunel.md, docs/guias/montar-gabinete-ip65.md, docs/referencia/04-herramientas.md (+1) | → https://www.homedepot.com.mx/p/truper-rotomartillo-profesional-1-2-650-w-truper-roto-1-2a7-231999 |
| redirect | 200 | https://www.homedepot.com.mx/s/taquete%20expansivo | docs/research/instalacion-tunel-detalle.md | → https://www.homedepot.com.mx/p/taquete-anclaje-expansivo-de-3-8-de-pulgada-plata-372087-979510 |
| redirect | 200 | https://www.hydroenv.com.mx/ | docs/research/inocuidad-operativa.md | → https://hydroenv.com.mx/ |
| redirect | 200 | https://www.johnnyseeds.com/growers-library/vegetables/microgreens-key-growing-information.html | docs/research/recetas-produccion-economia.md | → https://www.johnnyseeds.com/growers-library/vegetables/microgreens/microgreens-key-growing-information.html |
| redirect | 200 | https://www.mercadolibre.com.mx/bomba-electrica-periferica-para-agua-truper-12-hp-periferica-127-v-60-hz-boap-12a2-color-negro/p/MLM16110430 | docs/research/hidroponia-nft.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Fwww.mercadolibre.com.mx%2Fbomba-electrica-periferica-para-agua-truper-12-hp-periferica-127-v-60-hz-boap-12a2-color-negro%2Fp%2FMLM16110430&tid=efc2071f-5fb0-46fc-b011-02ac295b60c0 |
| redirect | 200 | https://www.mercadolibre.com.mx/bomba-peristaltica-dosificadora-de-agua-de-doble-cabezal-mi/p/MLM2017622966 | docs/research/electronica-automatizacion.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Fwww.mercadolibre.com.mx%2Fbomba-peristaltica-dosificadora-de-agua-de-doble-cabezal-mi%2Fp%2FMLM2017622966&tid=57cc5b01-f77e-4cb9-a058-6dc22aa55836 |
| redirect | 200 | https://www.mercadolibre.com.mx/estante-anaquel-rack-repisas-5-niveles-metalico-180x40x90-cm/p/MLM28717444 | docs/diseno/rack-y-charolas.md, docs/research/estructura-invernadero.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Fwww.mercadolibre.com.mx%2Festante-anaquel-rack-repisas-5-niveles-metalico-180x40x90-cm%2Fp%2FMLM28717444&tid=6c8066ab-1d9e-4062-9f35-e70686356c00 |
| redirect | 200 | https://www.mercadolibre.com.mx/gnatrol-larvicida-biologico-500-gr/up/MLMU716202200 | docs/research/clima-agronomia.md | → https://www.mercadolibre.com.mx/gz/account-verification?go=https%3A%2F%2Fwww.mercadolibre.com.mx%2Fgnatrol-larvicida-biologico-500-gr%2Fup%2FMLMU716202200&tid=146d3f43-e3a5-4240-8bf0-78b1b9bfedf5 |
| redirect | 200 | https://www.sodimac.com.mx/sodimac-mx/search?Ntt=ptr | docs/research/instalacion-tunel-detalle.md | → https://www.sodimac.com.mx/sodimac-mx/category/cat11448/PTR?sTerm=ptr&sScenario=BRD_ptr |
| redirect | 200 | https://www.steren.com.mx/catalogsearch/result/?q=inversor+12v | docs/research/electrico-respaldo-seguridad.md | → https://www.steren.com.mx/catalogsearch/result/index/?_q=inversor+12v&f=inversor+12v&q=inversor+ |
| redirect | 200 | https://www.trueleafmarket.com/products/amaranth-sprouting-red-garnet-seeds-conventional | docs/research/recetas-produccion-economia.md | → https://trueleafmarket.com/products/amaranth-sprouting-red-garnet-seeds-conventional |
| redirect | 200 | https://www.trueleafmarket.com/products/beet-seeds-microgreens | docs/research/recetas-produccion-economia.md | → https://trueleafmarket.com/products/beet-seeds-microgreens |
| redirect | 200 | https://www.trueleafmarket.com/products/pea-microgreens-seeds | docs/research/recetas-produccion-economia.md | → https://trueleafmarket.com/products/pea-microgreens-seeds |
| redirect | 200 | https://www.trueleafmarket.com/products/sunflower-black-oil-microgreens-seeds | docs/research/recetas-produccion-economia.md | → https://trueleafmarket.com/products/sunflower-black-oil-microgreens-seeds |
| redirect | 200 | https://www.truper.com/ficha_tecnica/controllers/index.php?codigo=27019 | docs/research/agua-captacion.md | → https://www.truper.com/ficha_tecnica/Bomba-electrica-periferica-para-agua-1-2-HP.html?code=27019 |

**Resumen:** 679 URL únicas en 114 archivos · ok 460 · redirect 49 · blocked 162 · **dead 8** (8 ya conocidos y anotados, **0 nuevos**) · 196 s.

*Última verificación: 2026-09-16 · regenera con `python3 tools/check_links.py --salida docs/referencia/enlaces.md`.*
