# Aprendizaje — tutoriales, libros y cursos para tener criterio

Ruta de estudio alineada a las fases. Regla general que salió de la investigación: **los
recursos canónicos de producción y electrónica están en inglés** (On The Grow, Donny Greens,
SmartHomeScene, GitHub); **los recursos donde el contexto local importa** (materiales de
tlapalería, NFT con PVC nacional, captación pluvial, normativa) **están en español y de
fuentes mexicanas**. Detalle completo: [research/tutoriales-videos.md](../research/tutoriales-videos.md)
y [research/libros-cursos.md](../research/libros-cursos.md).

---

## Qué hacer HOY (todo gratis)

1. **Inscribirse al curso Intagri "Producción de Hortalizas de Hoja en Hidroponía o NFT"**
   (Dr. Rodríguez Delfín, UNALM) — normalmente $742, **en promoción a $0** al 12-sep-2026:
   [programa](https://www.intagri.com/memorias/hortalizas/Produccion-hortalizas-hoja-hidroponia/programa-detallado).
   Es exactamente la Fase 2; el acceso se toma ahora aunque la fase llegue en meses.
2. **Descargar el manual de instalación del Kit Tláloc** (Isla Urbana, PDF oficial ilustrado):
   [PDF](https://www.engineeringforchange.org/wp-content/uploads/2020/07/MANUAL-INSTALACI%C3%93N-KIT-TL%C3%81LOC-12-JUNIO-2019CH.pdf).
3. **Descargar los manuales FAO**: [La Huerta Hidropónica Popular](https://www.fao.org/4/ah501s/ah501s.pdf) ·
   [Una huerta para todos](https://www.fao.org/3/i3846s/i3846s.pdf) ·
   [Manual del productor urbano](https://www.fao.org/4/a1177s/a1177s.pdf) ·
   [manual de espuma agrícola Oasis](https://www.guao.org/sites/default/files/biblioteca/Manual%20de%20hidropon%C3%ADa.pdf) ·
   [15 manuales de hidroponía (índice, incluye el manual NFT del TEC)](https://infolibros.org/libros-pdf-gratis/temas-varios/hidroponia/).
4. Apuntar en el calendario: **convocatoria ~febrero de la Escuela de Huertos Urbanos de
   SEDEMA** (48 h, gratuita, certificado oficial, cupo 40 — y networking con la escena
   huertera CDMX): [nota](https://www.sedema.cdmx.gob.mx/comunicacion/nota/sedema-lanza-convocatoria-para-el-seminario-taller-escuela-de-huertos-urbanos).

## Fase 0 — Producir y VENDER microgreens

| Recurso | Para qué | Enlace |
|---|---|---|
| **On The Grow** — playlist de tutoriales por variedad (girasol, chícharo, rábano, brócoli) | LA escuela de producción; experimentos comparativos de densidad/peso/blackout | [playlist](https://www.youtube.com/playlist?list=PLkEXI0BumyG5OBbqj_wXM6gnPB6gJ4alW) |
| On The Grow — guía escrita de charolas 10×20 + guías PDF gratuitas | Tasas de siembra por charola (el dato operativo más valioso), consulta rápida | [guía](https://onthegrow.net/blogs/microgreens/how-to-grow-microgreens-10x20-trays-complete-guide) · [índice](https://onthegrow.net/blogs/microgreens/best-microgreen-growing-advice-resources-on-the-grow) |
| **Donny Greens** — playlist de negocio + video de venta a restaurantes | On The Grow enseña a cultivar; **Donny enseña a VENDER** (entrega semanal a chefs, 7 años viviendo de ello). Ver ANTES de la primera ronda de visitas | [playlist](https://www.youtube.com/playlist?list=PLA09_1g6En1FVnk3eu93LeIVCFNjqSTu0) · [video](https://www.youtube.com/watch?v=MoSDSE8j7k8) |
| Curtis Stone — "My 3 Most Profitable Microgreens" | Decidir el mix de variedades por margen | [video](https://www.youtube.com/watch?v=KO-OuqbR3EE) |
| En español (complemento) | TvAgro: [Cultivo y Comercialización de Microvegetales](https://www.youtube.com/watch?v=sO2FXdSysrY) | |

**Libros de esta fase (~$885):** *Microgreens: The Insiders Secrets* de Donny Greens
($396.60, [Amazon MX](https://www.amazon.com.mx/Microgreens-Insiders-Building-Successful-Microgreen/dp/191366600X))
— precios por charola, venta a chefs, suscripciones; y *El jardinero horticultor* de
Jean-Martin Fortier **en español** ($488, [El Péndulo](https://pendulo.com/libro/jardinero-horticultor-el_393665),
en stock en 8 sucursales CDMX) — siembras escalonadas y canal directo con 10+ años de datos.
(*The Urban Farmer* de Curtis Stone no tiene traducción; $583 importado vía
[Buscalibre](https://www.buscalibre.com.mx/libros/search?q=the+urban+farmer+curtis+stone),
segunda ronda: se traslapa ~60 % con Fortier.)

## Fase 1 — Túnel, agua y automatización v1

| Recurso | Para qué | Enlace |
|---|---|---|
| **SmartHomeScene** — sensor capacitivo v1.2 con ESPHome | La guía exacta del sensor del BOM: cableado, YAML con filtros `median` + `calibrate_linear`, calibración seco/húmedo, hasta 8 sondas por ESP32 | [guía](https://smarthomescene.com/diy/diy-capacitive-soil-moisture-sensor-v1-2-with-esphome/) |
| **makstech/esphome-irrigation-system** (GitHub) | Esqueleto del controlador de riego: 8 zonas, control de bomba, funciona aun sin HA; dos YAML listos | [repo](https://github.com/makstech/esphome-irrigation-system) |
| Aguacatec (español) — automatizar el riego con HA | La LÓGICA de automatización ya en español (riego + condición de humedad + corte de seguridad) | [guía](https://aguacatec.es/automatizar-el-riego-con-home-assistant/) |
| La Huertina de Toni — serie de invernadero casero | Secuencia constructiva del túnel (traducir a PTR) | [parte 1](https://www.youtube.com/watch?v=9g0WfUQC2Qo) |
| Hydro Environment — guía de invernadero de patio en 13 pasos | Dimensionamiento con materiales mexicanos | [guía](https://hydroenv.com.mx/id535/) |
| EyouAgro — instalación de malla antigranizo paso a paso (español) | El riesgo #2 del plan, bien instalado | [guía](https://eyouagro.com/faqs/hail-netting-installation/) |

## Fase 2 — NFT y dosificación pH/EC

| Recurso | Para qué | Enlace |
|---|---|---|
| Hydro Environment — "NFT y su instalación" + video | Dimensiona bomba, pendiente 2 %, espaciamiento, con materiales que ellos venden | [guía](https://hydroenv.com.mx/id102/) · [video](https://www.youtube.com/watch?v=yY7fvK-wjHg) |
| México Verde — NFT con PVC (video, español MX) | Ejecución física con nomenclatura de tlapalería mexicana | [video](https://www.youtube.com/watch?v=PbnziwkUfus) |
| **r0bb10/ESPHome-DFRobot-pH-Meter** (GitHub) | Componente ESPHome para la sonda pH DFRobot: calibración 2/3 puntos desde HA, compensación de temperatura, EEPROM | [repo](https://github.com/r0bb10/ESPHome-DFRobot-pH-Meter) |
| Electronic Clinic — sistema hidropónico ESP32 (pH+EC+DS18B20+nivel) | El tutorial integrado más parecido al plan completo | [tutorial](https://www.electroniclinic.com/hydroponic-system-using-esp32-ph-sensor-ec-ds18b20-a02yyuw-sensor/) |
| "DIY my Dose" (Reef2Reef) | Dosificadora de 4 peristálticas open-source con calibración mL/s — idéntica a dosificar A/B/pH− | [hilo](https://www.reef2reef.com/threads/diy-my-dose-%E2%80%94-open-source-dosing-controller-built-on-esp32-home-assistant.1151856/) |
| Atlas Scientific EZO + ESPHome (YAML) | La ruta "cara pero sin dolor" si las sondas baratas dan lata (soporte nativo `ph_ezo`/`ec_ezo`) | [hilo](https://community.home-assistant.io/t/atlas-scientific-wi-fi-hydroponics-kit-example-yaml/538083) |

**Libros de esta fase:** *Cultivos hidropónicos* de Howard Resh, 5ª ed. **en español** ($899,
[Casa del Libro](https://latam.casadellibro.com/libro-cultivos-hidroponicos-5-ed-suelo-para-tecnicos-y-agricultores-profesionales-asi-como-para-los/9788484760054/796153),
"últimas unidades"; plan B [Buscalibre $1,088](https://www.buscalibre.com.mx/libro-cultivos-hidroponicos/9788484760054/p/979920))
— el **por qué** de las bandas de control (pH 5.8–6.2, EC por cultivo, síntoma → deficiencia);
comprarlo con ingresos de Fase 1. Escalón accesible mientras tanto: *Hidroponia* de Longar
(Trillas, $275, [El Sótano](https://www.elsotano.com/buscar?SotK=hidroponia)).

## Sanidad vegetal (permanente)

*Manejo Integrado de Plagas* (Toledo/Infante, Trillas, México — $429,
[Amazon MX](https://www.amazon.com.mx/Manejo-Integrado-Plagas-Toledo-Arreola/dp/9682483247)):
criterio de **umbrales** (cuándo intervenir vs cuándo basta ventilar) — directo contra
pulgón/fusarium, y es la base intelectual del método de validación V8. Complemento gratuito:
manuales BPA de [SENASICA](https://www.gob.mx/senasica/documentos/manuales-buenas-practicas-agricolas)
(la plantilla de la bitácora de inocuidad) y el curso gratuito de COFEPRIS
[Control sanitario de frutas y hortalizas frescas](https://cursos.aprende.gob.mx/courses/course-v1:COFEPRIS+CSDF26041X+2026_04/about).

## Qué NO comprar

El diplomado de Intagri (~$20–25k: sobredimensionado para 30 m²), *The Winter Market
Gardener* (CDMX casi no tiene invierno limitante), el curso de pago de Curtis Stone (el
material gratuito de los 3 canales basta), y el libro de $197 USD de On The Grow (sus guías
PDF gratuitas cubren lo operativo).

## Lagunas conocidas

No existe tutorial canónico **en español** de dosificación pH/EC con ESPHome (se trabaja con
los repos en inglés), ni video específico de invernadero en PTR (los herreros mexicanos no
hacen tutoriales — se adapta la secuencia de PVC/madera), ni libro serio de microgreens
comerciales en español. Si alguno aparece, PR bienvenido a este doc.
