// ============================================================================
//  patio_fase2.scad — Composición 3D del patio en Fase 2 (HomeGreen).
//  Patio de 10 × 8 m (80 m²), casa al sur, acceso al norte — SUPUESTO de la wiki
//  (docs/diseno/layout-patio.md tiene la planta 2D acotada; si difieren, manda la planta).
//
//  Contiene: túnel 5 × 6 m (tunel_3x6.scad con otros parámetros), 8 líneas NFT en dos
//  bancadas de 4 (linea_nft.scad), tambo de 200 L (depósito de solución), tinaco de 750 L
//  (agua cruda + captación pluvial), 3 racks Husky (rack_charolas.scad), gabinetes IP65,
//  zona de cosecha con refrigerador y coladera (posición supuesta).
//
//  Unidades: mm. Ejes: X = oeste → este (0..10000), Y = sur → norte (0..8000), Z = altura.
//  Los módulos vienen por `use <...>`: no copies geometría aquí; cambia los parámetros.
//
//  Render (desde hardware/cad/):
//    xvfb-run -a openscad -o ../../docs/assets/diagramas/cad/patio-fase-2-3d.png \
//      --autocenter --viewall --imgsize=1400,1000 --projection=p \
//      --colorscheme=Tomorrow --camera=0,0,0,42,0,200,0 patio_fase2.scad
// ============================================================================
use <tunel_3x6.scad>
use <rack_charolas.scad>
use <linea_nft.scad>

/* ------------------------------ Patio (supuesto) ------------------------------- */
patio_x  = 10000;   // [mm] (10 m, este–oeste)
patio_y  = 8000;    // [mm] (8 m, sur–norte)
barda_h  = 2200;    // altura de bardas laterales y norte [mm] (supuesto)
barda_e  = 150;
casa_h   = 3000;    // fachada sur de la casa [mm] (supuesto)
acceso_x = [8500, 9500];   // vano del acceso en la barda norte [mm] (supuesto)
puerta_casa_x = [7500, 8400]; // puerta de la casa al patio [mm] (supuesto)

/* ------------------------------ Túnel 5 × 6 ------------------------------------ */
tunel_ancho = 5000;
tunel_largo = 6000;
tunel_n     = 4;                 // 8 columnas
tunel_cx    = 3000;              // eje longitudinal del túnel (x) [mm]
tunel_y0    = 1000;              // cabecera sur del túnel [mm]; la puerta queda al norte (y = 7000)

/* ------------------------------ NFT ------------------------------------------- */
nft_lineas_por_bancada = 4;
nft_sep_lineas         = 350;    // entre ejes de tubo [mm]
nft_y_alto             = 4500;   // extremo ALTO (norte) de las líneas [mm]; el bajo queda en 1500
nft_bancadas_cx        = [1600, 4400];   // centro de cada bancada en x [mm]; pasillo central de 1.55 m

/* ------------------------------ Depósitos ------------------------------------- */
tambo_d  = 580;   tambo_h  = 900;    // tambo HDPE 200 L (dimensiones típicas; medir el que compres)
tambo_pos = [3000, 1300];            // dentro del túnel, entre los retornos de las bancadas
tinaco_d = 1100;  tinaco_h = 1400;   // tinaco 750 L: [POR VERIFICAR: medidas de la ficha Rotoplas Resistec 750 L]
tinaco_pos = [6600, 6800];           // fuera del túnel, junto a la bajante del canalón este
base_tinaco_h = 150;                 // base firme y elevada (03-instalacion §1.2)

/* ------------------------------ Racks ----------------------------------------- */
// [x del respaldo, y inicial, rotación]: 2 racks contra la pared oeste, 1 contra la este
racks = [[1057, 4800, 90], [1057, 5800, 90], [4943, 5700, -90]];

/* ------------------------------ Otros ----------------------------------------- */
gabinetes = [[5300, 1250, 1300], [5300, 1250, 1750], [560, 6700, 1500]];   // A (CA), B (CC), nodo riego
coladera_pos = [9000, 2000];        // supuesta
refri_pos    = [9200, 500];         // refrigerador usado 9–11 pies (zona de cosecha bajo techo, supuesto)
mesa_pos     = [7600, 500];         // mesa de cosecha/empaque

mostrar_etiquetas = true;
rot_etiquetas     = 180;            // 180 = legible con la cámara al norte (rz ≈ 200)
mostrar_titulo    = true;
$fn = 32;

/* ------------------------------ Colores ---------------------------------------- */
col_piso    = [0.80, 0.79, 0.76];
col_barda   = [0.85, 0.84, 0.80];
col_casa    = [0.90, 0.86, 0.76];
col_tambo   = [0.15, 0.25, 0.55];
col_tinaco  = [0.20, 0.20, 0.22];
col_gab     = [0.75, 0.75, 0.78];
col_refri   = [0.92, 0.92, 0.92];
col_mesa    = [0.70, 0.70, 0.72];
col_texto   = [0.12, 0.16, 0.22];
col_acento  = [0.18, 0.49, 0.20];   // #2e7d32
col_pvc_g   = [0.62, 0.62, 0.62];

/* ================================ Auxiliares ================================== */
module etiqueta(txt, pos, size = 260, col = col_texto) {
    if (mostrar_etiquetas) color(col) translate([pos[0], pos[1], 1]) rotate([0, 0, rot_etiquetas])
        linear_extrude(1) text(txt, size = size, font = "DejaVu Sans", halign = "center");
}
module flecha_norte(pos) {
    color(col_acento) translate([pos[0], pos[1], 1]) {
        linear_extrude(2) polygon([[-60, 0], [60, 0], [60, 500], [180, 500], [0, 800], [-180, 500], [-60, 500]]);
        translate([0, -320, 0]) rotate([0, 0, rot_etiquetas]) linear_extrude(2) text("N", size = 260, font = "DejaVu Sans:style=Bold", halign = "center");
    }
}

/* ================================ Patio ======================================= */
// piso
color(col_piso) translate([0, 0, -120]) cube([patio_x, patio_y, 120]);
// casa (fachada sur) con puerta al patio
color(col_casa) difference() {
    translate([0, -300, 0]) cube([patio_x, 300, casa_h]);
    translate([puerta_casa_x[0], -320, -1]) cube([puerta_casa_x[1] - puerta_casa_x[0], 340, 2100]);
}
// coladera (supuesta)
color([0.25, 0.25, 0.25]) translate([coladera_pos[0] - 100, coladera_pos[1] - 100, -2]) cube([200, 200, 2]);

/* ================================ NFT: 2 bancadas de 4 ========================= */
for (cx = nft_bancadas_cx)
    translate([cx, nft_y_alto, 0]) rotate([0, 0, -90])
        bancada_nft(n_lineas = nft_lineas_por_bancada, sep_lineas = nft_sep_lineas);

// tambo 200 L (depósito de solución, tapado y a la sombra dentro del túnel) + bombas 12 V
color(col_tambo) translate([tambo_pos[0], tambo_pos[1], 0]) cylinder(d = tambo_d, h = tambo_h);
color([0.30, 0.30, 0.32]) translate([tambo_pos[0], tambo_pos[1], tambo_h]) cylinder(d = tambo_d + 20, h = 25);   // tapa
color(col_gab) translate([tambo_pos[0] + 380, tambo_pos[1] - 200, 0]) cube([140, 90, 100]);                      // bomba diafragma 12 V principal
color(col_gab) translate([tambo_pos[0] + 380, tambo_pos[1] + 110, 0]) cube([140, 90, 100]);                      // bomba de respaldo
// retorno 2" de cada bancada hacia el tambo (a la altura del retorno común)
zr = 900 - 3000 * 2.5 / 100 - 114 / 2 - 60 - 200;
color(col_pvc_g) {
    translate([nft_bancadas_cx[0] + (3 * nft_sep_lineas) / 2 + 200, nft_y_alto - 3000 + 90, zr]) rotate([0, 90, 0])
        cylinder(d = 60, h = tambo_pos[0] - tambo_d / 2 - (nft_bancadas_cx[0] + (3 * nft_sep_lineas) / 2 + 200));
    translate([tambo_pos[0] + tambo_d / 2, nft_y_alto - 3000 + 90, zr]) rotate([0, 90, 0])
        cylinder(d = 60, h = (nft_bancadas_cx[1] - (3 * nft_sep_lineas) / 2 - 200) - (tambo_pos[0] + tambo_d / 2));
}

/* ================================ Tinaco 750 L ================================ */
color([0.55, 0.55, 0.55]) translate([tinaco_pos[0] - tinaco_d / 2 - 100, tinaco_pos[1] - tinaco_d / 2 - 100, 0])
    cube([tinaco_d + 200, tinaco_d + 200, base_tinaco_h]);                                   // base firme
color(col_tinaco) translate([tinaco_pos[0], tinaco_pos[1], base_tinaco_h]) cylinder(d = tinaco_d, h = tinaco_h);
color([0.35, 0.35, 0.37]) translate([tinaco_pos[0], tinaco_pos[1], base_tinaco_h + tinaco_h]) cylinder(d1 = tinaco_d, d2 = 400, h = 200);
// bajante del canalón este → filtro de hojas → tinaco (tramo horizontal, 3")
color([0.93, 0.93, 0.90]) translate([tunel_cx + tunel_ancho / 2 + 95 + 400, tunel_y0 + tunel_largo + 40, 250]) rotate([0, 90, 0])
    cylinder(d = 75, h = tinaco_pos[0] - tinaco_d / 2 - (tunel_cx + tunel_ancho / 2 + 95 + 400));

/* ================================ Racks ======================================= */
for (r = racks) translate([r[0], r[1], 0]) rotate([0, 0, r[2]]) rack_husky(titulo = false, riego = false);

/* ================================ Gabinetes, cosecha ========================== */
for (g = gabinetes) color(col_gab) translate([g[0] - 45, g[1] - 150, g[2]]) cube([90, 300, 300]);
color(col_refri) translate([refri_pos[0], refri_pos[1], 0]) cube([600, 650, 1500]);
color(col_mesa) translate([mesa_pos[0], mesa_pos[1], 0]) { translate([0, 0, 800]) cube([1200, 600, 40]); for (x = [20, 1140]) for (y = [20, 540]) translate([x, y, 0]) cube([40, 40, 800]); }

/* ================================ Etiquetas =================================== */
// Colocadas en piso libre (no bajo el túnel) para que no se encimen con la estructura.
etiqueta("Túnel 5 × 6 m (30 m²) · puerta al norte", [2600, tunel_y0 + tunel_largo + 420], 200);
etiqueta("Tambo 200 L + bombas 12 V", [tambo_pos[0], 520], 190);
etiqueta("Racks Husky ×3", [2400, 6150], 170);
etiqueta("Tinaco 750 L", [tinaco_pos[0], tinaco_pos[1] + tinaco_d / 2 + 180], 200);
etiqueta("Gabinetes IP65", [6900, 1250], 170);
etiqueta("Cosecha + refrigerador (supuesto)", [8300, 1750], 190);
etiqueta("Coladera (supuesta)", [coladera_pos[0], coladera_pos[1] + 420], 170);
etiqueta("Acceso (norte)", [9000, patio_y - 520], 190);
// NFT: rótulo a lo largo del pasillo central (gira 90° respecto a los demás)
if (mostrar_etiquetas) color(col_texto) translate([tunel_cx, 3000, 1]) rotate([0, 0, rot_etiquetas + 90])
    linear_extrude(1) text("NFT · 8 líneas · 2 bancadas · 2.5 % al sur", size = 150, font = "DejaVu Sans", halign = "center");
// Casa: rótulo vertical sobre la fachada, legible desde el norte
if (mostrar_etiquetas) color(col_texto) translate([4500, 2, 2450]) rotate([0, 0, 180]) rotate([90, 0, 0])
    linear_extrude(2) text("Casa · fachada sur (supuesto)", size = 240, font = "DejaVu Sans", halign = "center");
flecha_norte([9600, 6300]);
if (mostrar_titulo) color(col_texto) translate([patio_x + 400, patio_y + 900, 1]) rotate([0, 0, rot_etiquetas]) linear_extrude(1)
    text("HomeGreen · Patio Fase 2 · 10 × 8 m (supuesto) · v1 · 2026-09", size = 260, font = "DejaVu Sans", halign = "left");

echo("Composición Fase 2: túnel 5 x 6 m (8 columnas), 8 líneas NFT (2 bancadas de 4), tambo 200 L, tinaco 750 L, 3 racks Husky, 3 gabinetes IP65.");

/* ================================ Superficies translúcidas: AL FINAL =========== */
// En el preview OpenCSG de OpenSCAD lo que se dibuja DESPUÉS de una superficie translúcida
// queda oculto detrás de ella. Por eso el túnel (plástico + malla) y las bardas van al final.
translate([tunel_cx, tunel_y0, 0])
    tunel(ancho = tunel_ancho, largo = tunel_largo, n_porticos = tunel_n, largueros_techo = 2,
          losa = false, titulo = false, lado_bajante = 1, alpha_p = 0.16, alpha_m = 0.10);
// bardas oeste, este y norte (translúcidas para ver el interior); vano de acceso al norte
color(col_barda, 0.30) {
    translate([-barda_e, 0, 0]) cube([barda_e, patio_y, barda_h]);
    translate([patio_x, 0, 0]) cube([barda_e, patio_y, barda_h]);
    difference() {
        translate([-barda_e, patio_y, 0]) cube([patio_x + 2 * barda_e, barda_e, barda_h]);
        translate([acceso_x[0], patio_y - 10, -1]) cube([acceso_x[1] - acceso_x[0], barda_e + 20, barda_h + 2]);
    }
}
