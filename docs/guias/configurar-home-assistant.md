# Configurar Home Assistant para el huerto

**En una línea:** en una tarde instalas Home Assistant OS en el cerebro (mini PC o Pi 5) dentro de
casa, lo dejas con IP fija y UPS, integras los nodos ESPHome, cargas el paquete, las 28
automatizaciones y el dashboard del repo, haces sonar una crítica de prueba con el teléfono en
silencio y dejas programada la copia de seguridad, para que desde esa noche cada alarma del
catálogo L0 llegue a tu teléfono con la severidad correcta.

!!! info "Antes de empezar"
    - **Tiempo:** 2–3 h (instalación 45 min, nodos 20 min, YAML 30 min, notificaciones y pruebas 45 min) · **Costo:** software $0; mini PC ThinkCentre usado i5/8 GB/SSD **~$3,000 aprox.** ([ML](https://listado.mercadolibre.com.mx/mini-pc-lenovo-thinkcentre)) o Pi 5 4 GB **$3,069** verificado + fuente 27 W ~$404 aprox. ([Cyberpuerta](https://www.cyberpuerta.mx/Placas-de-Desarrollo-Raspberry/)); UPS chico **~$900 aprox.** ([ML](https://listado.mercadolibre.com.mx/no-break-500va)) o DataShield DS-600 **$1,189** / KS800PRO **$1,859** con puerto para NUT ([Cyberpuerta](https://www.cyberpuerta.mx/index.php?cl=search&searchparam=DataShield+UPS)); medidor de enchufe Steren HER-432 **$336–399** ([Steren](https://www.steren.com.mx/catalogsearch/result/?q=medidor+de+consumo)) · **Personas:** 1
    - **Necesitas:** el cerebro con su fuente, una USB de 8 GB para el instalador, cable de red, monitor y teclado solo para el primer arranque del mini PC, teléfono con la app de Home Assistant, laptop con el repo clonado, y los tres YAML de [`firmware/homeassistant/`](https://github.com/AndresIslas99/HomeGreen/tree/main/firmware/homeassistant).
    - **Prerequisitos:** al menos un nodo flasheado ([Flashear ESPHome](flashear-esphome.md)); leído [Home Assistant](../software/home-assistant.md) (qué hace cada archivo y la tabla de automatizaciones) y [Software](../software/index.md) (red y versiones).

## Pasos

### A. Instalar Home Assistant OS (45 min)

1. **Elige y prepara el cerebro.** Mini PC: entra al BIOS, arranque UEFI, desactiva *Secure Boot*; Pi 5: microSD de calidad (o NVMe) y la fuente oficial. Va **dentro de casa**, con cable de red al router y en el UPS junto con el router ([03 §1.3](../referencia/03-instalacion.md), [07 §10](../referencia/07-puntos-ciegos-y-riesgos.md)).
2. **Escribe la imagen de HA OS.** Descarga la imagen oficial para tu equipo ("generic x86-64" para el mini PC; la de Raspberry Pi 5) y grábala en el SSD (desde un USB en vivo) o en la microSD con la herramienta de imágenes de Raspberry Pi o similar `[POR VERIFICAR: sigue la página de instalación oficial de Home Assistant para tu hardware; los pasos cambian con cada versión]`. Enciende con cable de red.
3. **Onboarding:** desde la laptop abre `http://homeassistant.local:8123` (espera 5–10 min al primer arranque). Crea el usuario dueño, nombre "Huerto", ubicación en tu colonia de CDMX, zona horaria `America/Mexico_City`, unidades métricas. *Criterio de listo:* ves el panel "Resumen" y Ajustes → Sistema → Red muestra la IP por cable.
4. **IP fija:** reserva DHCP en el router para la MAC del cerebro (o IP estática en Ajustes → Sistema → Red). Reserva también las de los nodos ([Flashear ESPHome §D](flashear-esphome.md)). *Criterio de listo:* `http://<ip-fija>:8123` abre y `homeassistant.local` resuelve a esa IP.

### B. Complementos y nodos (20 min)

5. **Instala los add-ons** (Ajustes → Complementos → Tienda): **ESPHome** (compila y flashea por OTA), **File editor** o **Studio Code Server** (editar YAML desde el navegador), **Samba share** (copiar archivos desde la laptop) o **Terminal & SSH**, y **Network UPS Tools** solo si tu UPS tiene puerto de datos (KS800PRO). Inicia cada uno y activa *Mostrar en la barra lateral*.
6. **Pega tus secretos en ESPHome:** ESPHome → ⋮ → *Secrets* → el contenido de tu `secrets.yaml` ([Flashear ESPHome §A](flashear-esphome.md)).
7. **Adopta los nodos:** Ajustes → Dispositivos e integraciones → los ESP32 aparecen "descubiertos" → *Configurar* → clave API del nodo. *Criterio de listo:* `nodo-riego-v1` (y `nodo-nft-v2` en Fase 2) con `Nodo … estado` ON y sus entidades con los nombres de [datos.md §2](../diseno/datos.md). Anota cualquier `entity_id` distinto: lo corregirás en los YAML del paso C.

### C. Cargar el paquete, las automatizaciones y el dashboard (30 min)

8. **Paquete.** Con Samba o el editor: crea `/config/packages/` y copia `configuration-snippets.yaml` como `/config/packages/huerto.yaml`. En `/config/configuration.yaml` agrega (una sola vez):
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
   Sustituye `mobile_app_TU_CELULAR` (dos veces) por tu servicio real: Herramientas para desarrolladores → Acciones → escribe `notify.mobile_app` y copia el nombre (la app debe estar instalada, paso 12; puedes volver a este punto).
9. **Comprueba y reinicia:** Herramientas para desarrolladores → YAML → *Comprobar configuración* → "Configuración válida" → *Reiniciar*. *Criterio de listo:* Ajustes → Dispositivos → Ayudantes lista "Mantenimiento NFT", "Energía · alarma mensual", "Última calibración de sondas"…, y Ajustes → Entidades muestra `sensor.excepciones_activas` y `alert.nft_emergencia`.
10. **Automatizaciones:** pega el contenido de `automations.yaml` en `/config/automations.yaml` (si ya tenías automatizaciones creadas desde la interfaz, agrega las nuevas al final conservando la lista) → Ajustes → Automatizaciones → ⋮ → *Recargar automatizaciones*. *Criterio de listo:* 28 automatizaciones con prefijos `NFT ·`, `RIEGO ·`, `AMBIENTE ·`, `ENERGÍA ·`, `MANTENIMIENTO ·`, `RESUMEN ·`, `DATOS ·`, `BITÁCORA ·`, `CEREBRO ·`, ninguna con el icono de error.
11. **Dashboard:** Ajustes → Paneles → *Agregar panel* → "Nuevo panel desde cero" → título "Huerto", icono `mdi:sprout`, *Mostrar en la barra lateral* → ábrelo → ⋮ → *Editar panel* → ⋮ → *Editor de configuración sin formato* → borra lo que haya, pega `dashboard-huerto.yaml` completo → *Guardar*. *Criterio de listo:* cinco pestañas (Excepciones, Microgreens, NFT, Energía, Bitácora) y ninguna tarjeta en rojo con los nodos que ya tienes (las del NFT saldrán en rojo hasta la Fase 2: es normal).

!!! warning "Error típico: pegar el paquete dentro de configuration.yaml"
    El paquete es un archivo aparte en `packages/`; si lo pegas en `configuration.yaml` chocará
    con las claves que HA ya escribió ahí (`automation: !include …`). Y si HA marca
    "Configuración inválida", lee la línea exacta: casi siempre es sangría (dos espacios) o
    un `!secret` cuya clave no existe en `secrets.yaml`.

### D. Notificaciones que suenan en silencio (30 min)

12. **App de Home Assistant** en tu teléfono: inicia sesión contra la IP fija (y, si quieres acceso desde fuera, Home Assistant Cloud o tu propio túnel `[POR VERIFICAR: costo de HA Cloud vs. configurar acceso remoto por tu cuenta]`), acepta notificaciones y, en iOS, el permiso de **notificaciones críticas**. Vuelve al paso 8 si el nombre `mobile_app_…` no existía aún.
13. **Prueba la crítica:** Herramientas para desarrolladores → Acciones → `notify.huerto_critica`, mensaje "prueba", y en *data*: `push: {interruption-level: critical, sound: {name: default, critical: 1, volume: 1.0}}`, `channel: Huerto critica`, `importance: high`. Pon el teléfono en silencio antes. *Criterio de listo:* suena en < 10 s. En Android, abre los ajustes de notificación de la app y confirma que el canal "Huerto critica" tiene sonido y salta el modo "No molestar".
14. **Prueba un aviso normal:** `notify.huerto_aviso`. *Criterio de listo:* llega sin sonido crítico (es la diferencia entre advertencia y crítica de [06 §Escalamiento](../referencia/06-validacion-y-lazos-agenticos.md)).
15. **Telegram (opcional):** bot con @BotFather, token en `secrets.yaml`, tu `chat_id`, bloque comentado del paquete y `telegram_huerto` en el grupo `huerto_critica` `[POR VERIFICAR: en versiones recientes de HA el bot se configura desde la interfaz y el envío es telegram_bot.send_message]`.

### E. Helpers del primer día (15 min)

16. **Fechas de mantenimiento:** en la vista Bitácora pulsa "Hoy calibré las sondas", "Hoy cambié la solución" y "Hoy hice el simulacro V11" (o escribe la fecha real en cada `input_datetime`). Sin fecha, los recordatorios de las 08:00 no cuentan días.
17. **Energía:** mide 7 días el consumo base de tu casa con el HER-432 (o lee el promedio anual en el recibo de CFE), extrapola a un mes y escríbelo en "Energía · consumo base del hogar"; ajusta las potencias si mediste otras. Alarma en 220 kWh/mes ([07 §1](../referencia/07-puntos-ciegos-y-riesgos.md), [antes de gastar un peso](../empieza-aqui/antes-de-gastar-un-peso.md)).
18. **Bitácora a archivo:** Ajustes → Integraciones → *Agregar* → **File** → *Notificación* → ruta `/config/bitacora/ha-eventos.csv`, sin marca de tiempo → renombra la entidad a `notify.bitacora_ha`. Crea la carpeta `/config/bitacora/` con Samba. Prueba el formulario de la vista Bitácora. *Criterio de listo:* el archivo tiene la fila con fecha, evento, pH, EC, T, HR y tinaco.
19. **Calendario:** Ajustes → Integraciones → *Agregar* → **Local Calendar** → nombre `huerto` (entidad `calendar.huerto`). Agrega los eventos fijos: calibración cada 15 días, cambio de solución cada 2–3 semanas, V11 el primer domingo de mes, visitas y entregas. Cada evento avisa 1 h antes.
20. **UPS con NUT (solo KS800PRO):** add-on NUT → dispositivo `ups`, driver `usbhid-ups`, puerto `auto` `[POR VERIFICAR: driver y usuario/contraseña del add-on en su documentación]` → integración NUT → confirma que existe una entidad de estado con `OL`; si se llama distinto a `sensor.ups_status_data`, cámbialo en la automatización `CEREBRO · ADVERTENCIA · UPS de la casa en batería`. Con DS-600 no hay puerto: sáltate este paso.

### F. Copias de seguridad y actualizaciones (10 min)

21. **Programa la copia:** Ajustes → Sistema → Copias de seguridad → automática semanal (con copia a red o nube si tu versión lo ofrece). Haz una manual ahora y **descárgala** a la laptop. *Criterio de listo:* tienes un archivo de copia fuera del cerebro.
22. **Regla de actualización:** HA y ESPHome se actualizan juntos, un domingo después del informe semanal, con copia previa; nunca la víspera de una entrega ni durante un corte ([Software](../software/index.md)).

### G. Probar las alarmas en la mesa (30 min)

23. Corre la tabla "Probar antes de plantar" de [Home Assistant](../software/home-assistant.md): desconectar el YF-S201, desenchufar el detector de red, apagar un nodo, cortar el Wi-Fi, bajar el umbral del tinaco, mover la sonda de pH entre buffers, encender "Mantenimiento NFT", reiniciar HA. *Criterio de listo:* cada fila produce la alarma prevista en el canal previsto y ninguna alarma falsa. Es el ensayo del [dry-run V3](../validacion/v03-dry-run.md).

!!! warning "Error típico: cerebro sin UPS o UPS sin router"
    Un corte que apaga el router deja al cerebro sin internet y a ti sin alarmas justo cuando
    más importan. Router y cerebro en el mismo UPS; el DS-600 aguanta 45–90 min con 25–35 W
    ([research/eléctrico §3.4](../research/electrico-respaldo-seguridad.md)).

!!! warning "Error típico: confiar en HA para que corra el agua"
    Todo lo de esta guía avisa y optimiza. La bomba NFT corre por K1 NC y batería en
    paralelo, y el riego lo decide el nodo; si HA se cae, el cultivo no se entera
    ([control.md](../diseno/control.md)).

## Al terminar

- [ ] HA OS con IP fija, cable de red, dentro de casa y en el UPS con el router
- [ ] Nodos adoptados; entidades con los nombres de [datos.md §2](../diseno/datos.md) (o los YAML de HA corregidos)
- [ ] Paquete + 28 automatizaciones + dashboard sin errores; `mobile_app_TU_CELULAR` sustituido
- [ ] Crítica de prueba sonó con el teléfono en silencio; aviso normal recibido
- [ ] Fechas de mantenimiento, consumo base del hogar, `notify.bitacora_ha` y `calendar.huerto` listos
- [ ] Copia de seguridad descargada; tabla de pruebas al 100 %
- Registrar en `bitacora/electrico.csv` (`fecha,evento,gabinete,rama,valor_medido,unidad,quien,observaciones`): `evento = instalacion_ha` con la versión de HA OS, de ESPHome y el modelo del cerebro en `observaciones`; una fila `evento = prueba_alarma` por cada fila de la tabla probada.
- Siguiente paso: [Dry-run V3](../validacion/v03-dry-run.md) (72 h con fallas inyectadas) → [Fase 1 · Automatización v1](../fases/fase-1/automatizacion-v1.md) → en Fase 2, [Armar el respaldo DC](armar-respaldo-dc.md) y [Simulacro de apagón](simulacro-de-apagon.md).

## Fuentes

- [software/home-assistant.md](../software/home-assistant.md) — los tres archivos, tabla de automatizaciones, notificaciones, NUT, copias, pruebas.
- [referencia/06-validacion-y-lazos-agenticos.md](../referencia/06-validacion-y-lazos-agenticos.md) — escalamiento (canales, tiempos), L1, calibración quincenal, V3, V11.
- [referencia/03-instalacion.md §1.3](../referencia/03-instalacion.md) — HA en casa con UPS, dashboard mínimo; [referencia/07-puntos-ciegos-y-riesgos.md](../referencia/07-puntos-ciegos-y-riesgos.md) §1 (220 kWh, HER-432) y §10 (equipo dentro de casa).
- [research/electrico-respaldo-seguridad.md](../research/electrico-respaldo-seguridad.md) §3.4 (DS-600, KS800PRO con NUT) y §5.2 (notificación crítica, `alert`).
- [research/electronica-automatizacion.md §2](../research/electronica-automatizacion.md) y [research/puntos-ciegos.md §(a)](../research/puntos-ciegos.md) — cerebro, UPS, medidor de enchufe.
- [diseno/datos.md §2](../diseno/datos.md) — entidades; [diseno/control.md](../diseno/control.md) — qué corre en ESPHome y qué en HA.
- [`bom/fase1.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase1.csv), [`bom/fase2.csv`](https://github.com/AndresIslas99/HomeGreen/blob/main/bom/fase2.csv).
