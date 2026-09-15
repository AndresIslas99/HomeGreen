// ============================================================================
//  tunel_5x6.scad — Túnel a dos aguas 5 × 6 m (30 m²) en PTR 1½" cal. 14
//  (HomeGreen · Fase 2: ampliación del túnel 3 × 6 m de Fase 1).
//
//  Este archivo NO redefine la geometría: hace `use <tunel_3x6.scad>` y llama al mismo
//  módulo tunel() con otro ancho, otro número de pórticos y dos largueros de techo por
//  agua. Todo lo demás (perfiles, placas, anclas, cubierta, canalón) hereda los valores
//  por defecto de tunel_3x6.scad. Si cambias el diseño base, cámbialo allá.
//
//  Por qué 4 pórticos (8 columnas) y no 3: con 5 m de ancho el cabio mide 2.6 m y los
//  largueros de PTR 1" con 3 m de claro se pandean; con 4 pórticos los claros bajan a
//  2 m, que es el "postes cada ≤ 2 m" de docs/referencia/03-instalacion.md §1.1. El
//  informe de anclaje ya contempla "los 6 (o 8) puntos de columna"
//  (docs/research/instalacion-tunel-detalle.md §2). Si prefieres reutilizar las 6
//  columnas de Fase 1 sin agregar dos, pon n_porticos = 3 y acepta claros de 3 m.
//
//  Render (desde hardware/cad/):
//    xvfb-run -a openscad -o ../../docs/assets/diagramas/cad/tunel-5x6.png \
//      --autocenter --viewall --imgsize=1400,1000 --projection=p \
//      --colorscheme=Tomorrow --camera=0,0,0,62,0,212,0 tunel_5x6.scad
// ============================================================================
use <tunel_3x6.scad>

/* ------------------------------ Parámetros de la ampliación -------------------- */
ancho           = 5000;   // ancho exterior [mm]
largo           = 6000;   // largo [mm] (se conserva el de Fase 1)
n_porticos      = 4;      // 8 columnas → 32 anclas de cuña 3/8" × 5"
h_columna       = 2000;   // misma columna que Fase 1: se reutilizan
pendiente       = 30;     // % → peralte 750 mm, cumbrera a ~2.79 m
largueros_techo = 2;      // largueros intermedios por agua (el cabio mide 2.6 m)

/* ------------------------------ Qué dibujar ------------------------------------ */
mostrar_losa     = true;
mostrar_plastico = true;
mostrar_malla    = true;
mostrar_canalon  = true;
mostrar_titulo   = true;

/* ------------------------------ Instancia -------------------------------------- */
tunel(ancho = ancho, largo = largo, n_porticos = n_porticos, h_col = h_columna, pend = pendiente,
      largueros_techo = largueros_techo,
      losa = mostrar_losa, plastico = mostrar_plastico, malla = mostrar_malla, canalon_on = mostrar_canalon,
      titulo = mostrar_titulo,
      texto_titulo = "Túnel 5 × 6 m (30 m²) · Fase 2 · PTR 1½\" cal. 14 · 8 columnas · v1 · 2026-09");

lista_cortes(ancho = ancho, largo = largo, n_porticos = n_porticos, h_col = h_columna, pend = pendiente,
             largueros_techo = largueros_techo);

// Comparación rápida con el túnel de Fase 1 (mismos criterios) para dimensionar la ampliación
p36 = piezas_tunel(3000, 6000, 3, 2000, 30);
p56 = piezas_tunel(ancho, largo, n_porticos, h_columna, pendiente, largueros_techo = largueros_techo);
m36_15 = suma([for (q = p36) if (q[1] == "PTR 1 1/2") q[2] * q[3]]);
m56_15 = suma([for (q = p56) if (q[1] == "PTR 1 1/2") q[2] * q[3]]);
m36_1  = suma([for (q = p36) if (q[1] == "PTR 1") q[2] * q[3]]);
m56_1  = suma([for (q = p56) if (q[1] == "PTR 1") q[2] * q[3]]);
echo(str("Ampliación 3x6 -> 5x6: PTR 1 1/2 pasa de ", m36_15 / 1000, " m a ", m56_15 / 1000, " m (+", (m56_15 - m36_15) / 1000,
         " m); PTR 1 pasa de ", m36_1 / 1000, " m a ", m56_1 / 1000, " m (+", (m56_1 - m36_1) / 1000, " m)"));
echo("Se reutilizan de Fase 1: 6 columnas, cumbrera, 2 largueros de alero, jambas, dintel y placas/anclas de las 6 columnas existentes (los cabios de 1.59 m NO sirven para 5 m: quedan como escuadras o largueros cortos).");
