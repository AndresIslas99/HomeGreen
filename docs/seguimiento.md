---
hide:
  - toc
---

# Seguimiento del proyecto

**Esta página no es documentación: es la libreta.** El resto de la wiki dice qué hacer; aquí
registras qué llevas hecho, a qué precio compraste de verdad y en qué va cada gate.

Las partidas, los umbrales y los criterios no están escritos aquí: se leen de
[`bom/partidas.csv`](referencia/bom.md) y de [Gates](validacion/gates.md) a través de
[`tools/gen_seguimiento.py`](https://github.com/AndresIslas99/HomeGreen/blob/main/tools/gen_seguimiento.py).
Si cambias el BOM, este tablero cambia solo.

!!! warning "Dónde vive lo que escribes aquí, y cómo perderlo"
    En el **almacenamiento local de este navegador**. No hay servidor detrás: nada se sube a
    ningún lado, nada se comparte, y nadie más lo ve. El precio de eso es concreto:

    - Si entras desde el teléfono, verás un tablero **vacío**: es otro navegador.
    - Si limpias datos de navegación o usas ventana privada, **se borra**.

    Por eso **Exportar respaldo** no es un extra: es la copia de seguridad. Hazla cada vez que
    termines una jornada de compras. El registro duradero del proyecto sigue siendo el repo —
    los CSV de `bitacora/` y el propio BOM— y para eso está **Compras a CSV**.

<div id="hg-seguimiento">
  <p><em>Cargando el tablero…</em> Si este mensaje no desaparece, tu navegador tiene el
  JavaScript desactivado; el resto de la wiki funciona igual sin él.</p>
</div>

## Cómo se usa cada pestaña

**Compras.** La lista de las 96 partidas, agrupadas por fase y por bloque de compra —el mismo
orden en que las piden las páginas de cada fase. Marca lo que ya compraste y anota **lo que
pagaste de verdad**, no lo que decía el plan: ahí es donde se ve si el presupuesto aguanta.
Las partidas en cursiva y con borde punteado son las que **no suman** al total (informativas,
condicionales o ya pagadas en una fase anterior) y están ahí para que sepas que existen, no
para que las compres.

**Gates.** Los tres gates con su criterio real. Tú escribes el valor medido; el veredicto lo
calcula la página. No hay botón de "pasar de todos modos", y es a propósito: la regla del
proyecto es que un gate no alcanzado se itera o se detiene, nunca se rebaja.

**Validaciones.** Los métodos V1–V11 con su estado y el número que salió. La regla dura: no se
siembra nada que no haya pasado V1.

**Parámetros.** Los umbrales y los supuestos económicos. Pide contraseña, y conviene entender
exactamente qué protege eso y qué no.

!!! danger "La contraseña de esta página es un candado en una puerta de cristal"
    La wiki es un **sitio estático**. No hay servidor que verifique nada: el candado vive en el
    JavaScript que tu navegador ya descargó. Guardé el hash y no el texto, así que la contraseña
    no se lee de un vistazo en el código fuente — pero **quien sepa editar JavaScript la salta en
    un minuto**, y eso no tiene arreglo dentro de un sitio estático.

    Para lo que sirve de verdad: que no muevas un umbral sin querer, y que puedas enseñarle el
    tablero a un socio, a un chef o a tu contador sin que lo editen. Para lo que **no** sirve:
    proteger información de alguien que quiera verla. No pongas aquí nada que te dolería que se
    leyera. Si algún día necesitas control de acceso real, eso pide un backend y es otro proyecto.

## Qué hace el tablero y qué no

| Sí | No |
|---|---|
| Registrar compras con precio real y desviación contra el plan | Comprar por ti ni cotizar en vivo |
| Calcular el veredicto de cada gate contra su umbral | Dejarte pasar un gate que no se cumple |
| Sobrevivir a que cierres la pestaña | Sobrevivir a que limpies el navegador — exporta |
| Exportar a CSV para que el dato acabe en el repo | Sincronizar entre tu computadora y tu teléfono |
| Evitar que muevas un umbral sin querer | Proteger nada de quien sepa abrir el código |
