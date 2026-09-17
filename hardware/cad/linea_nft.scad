// ============================================================================
//  linea_nft.scad — Línea NFT en tubo PVC SANITARIO 4" (OD 114 mm) × 3000 mm con
//  10 perforaciones para canastilla de 3", pendiente 2.5 % y soportes de PTR 1"
//  (HomeGreen · Fase 2). Modelo paramétrico OpenSCAD (2021.01). Unidades: mm.
//
//  Ejes: X = a lo largo del tubo (x = 0 es el extremo ALTO / entrada; x = L es el
//  extremo BAJO / retorno), Y = transversal, Z = altura.
//
//  ADVERTENCIA (docs/referencia/03-instalacion.md §2.1 y bom/fase2.csv): el diámetro de
//  perforación NO se toma de este archivo: se mide en el CUERPO de la canastilla comprada,
//  bajo el labio, y se prueba en un retazo. Los 70 mm de `d_perf` son solo el valor de
//  dibujo para una canastilla de 3"; una canastilla "de 2 pulgadas" pide 44–48 mm.
//  Comprar las canastillas ANTES de perforar. Desbarbar cada hoyo.
//
//  Fuentes: docs/research/hidroponia-nft.md (tubo sanitario Amanco 4" blanco $415/6 m,
//  canastilla 3" $12.80, 20 cm entre centros, pendiente 2–3 %, 1–2 L/min por línea),
//  docs/referencia/03-instalacion.md §2.1 (soportes cada ≤ 1.5 m, retorno por gravedad),
//  docs/diseno/hidraulico.md (manifold ¾" con válvula por línea, retorno 2").
//
//  Render (desde hardware/cad/):
//    xvfb-run -a openscad -o ../../docs/assets/diagramas/cad/linea-nft.png \
//      --autocenter --viewall --imgsize=1400,1000 --projection=p \
//      --colorscheme=Tomorrow --camera=0,0,0,52,0,25,0 linea_nft.scad
// ============================================================================

/* ------------------------------ Tubo ------------------------------------------- */
L_tubo     = 3000;   // media tramo de 6 m [mm]
D_tubo     = 114;    // diámetro exterior del tubo sanitario 4" [mm]
pared_tubo = 3.2;    // [mm]
n_plantas  = 10;     // perforaciones por línea
sep_perf   = 200;    // entre centros: 20 cm albahaca/arúgula (15 cm cilantro) [mm]
d_perf     = 70;     // Ø de dibujo; el real se mide en la canastilla (ver advertencia)

/* ------------------------------ Canastilla 3" ---------------------------------- */
canastilla_labio  = 82;   // Ø del labio (apoya sobre el tubo) [mm]
canastilla_cuerpo = 70;   // Ø del cuerpo bajo el labio = Ø de la sierra copa [mm] → MEDIR
canastilla_alto   = 80;   // [mm]
espuma_d          = 43;   // cilindro de foami agrícola 4.3 × 5 cm
espuma_h          = 50;

/* ------------------------------ Pendiente y soportes --------------------------- */
pendiente    = 2.5;    // % (2–3 %): 75 mm de caída en 3 m
h_eje_alto   = 900;    // altura del eje del tubo en el extremo alto [mm]
x_soportes   = [150, 1500, 2850];   // posición de los 3 soportes (≤ 1.5 m entre ellos)
soporte_a    = 25;     // PTR 1" [mm]
soporte_e    = 1.9;
pies_ancho   = 320;    // separación de las patas de un soporte de línea sencilla [mm]
cuna_esp     = 8;      // media caña que recibe el tubo [mm]

/* ------------------------------ Conexiones ------------------------------------- */
tapa_esp   = 30;   // tapa (cap) 4" [mm]
d_tapa     = 124;
entrada_d  = 16;   // manguera ½" de entrada [mm]
retorno_d  = 60;   // retorno 2" [mm]
manifold_d = 25;   // manifold de alimentación ¾" [mm]

/* ------------------------------ Qué dibujar ------------------------------------ */
mostrar_plantas   = true;
mostrar_soporte   = true;
posiciones_vacias = [9];   // índices (0..n-1) sin canastilla, para ver el barreno en el render
mostrar_titulo  = true;
$fn = 32;

/* ------------------------------ Colores ---------------------------------------- */
col_pvc      = [0.95, 0.95, 0.92];
col_pvc_gris = [0.62, 0.62, 0.62];
col_canasta  = [0.20, 0.20, 0.20];
col_espuma   = [0.45, 0.60, 0.35];
col_planta   = [0.22, 0.55, 0.25];
col_ptr1     = [0.72, 0.46, 0.09];
col_valvula  = [0.85, 0.15, 0.15];
col_texto    = [0.12, 0.16, 0.22];

/* ================================ Funciones ==================================== */
function ang_pend(p = pendiente) = atan(p / 100);
function caida(L = L_tubo, p = pendiente) = L * p / 100;
// Abscisa de la perforación i (0..n-1), centradas en el tubo
function x_perf(i, L = L_tubo, n = n_plantas, s = sep_perf) = (L - (n - 1) * s) / 2 + i * s;
// Altura del eje del tubo en la abscisa x
function z_eje(x, h0 = h_eje_alto, p = pendiente) = h0 - x * p / 100;
// ¿Está v en la lista l?
function en(v, l) = len([for (q = l) if (q == v) q]) > 0;

/* ================================ Piezas ====================================== */
// Tubo con perforaciones en la generatriz superior (eje a lo largo de +X, horizontal)
module tubo_perforado(L = L_tubo, D = D_tubo, pared = pared_tubo, n = n_plantas, s = sep_perf, dp = d_perf) {
    color(col_pvc) difference() {
        rotate([0, 90, 0]) cylinder(d = D, h = L);
        rotate([0, 90, 0]) translate([0, 0, -1]) cylinder(d = D - 2 * pared, h = L + 2);
        for (i = [0 : n - 1]) translate([x_perf(i, L, n, s), 0, 0]) cylinder(d = dp, h = D);
    }
}

// Canastilla 3" con cilindro de foami y planta (tamaño según edad 0..1)
module canastilla(edad = 1, planta = true) {
    color(col_canasta) difference() {
        union() {
            cylinder(d = canastilla_cuerpo, h = canastilla_alto);
            translate([0, 0, canastilla_alto - 3]) cylinder(d = canastilla_labio, h = 3);
        }
        translate([0, 0, 2]) cylinder(d = canastilla_cuerpo - 4, h = canastilla_alto);
        for (k = [0 : 7]) rotate([0, 0, k * 45]) translate([canastilla_cuerpo / 2 - 4, -2, 6]) cube([8, 4, canastilla_alto - 16]);
    }
    color(col_espuma) translate([0, 0, 8]) cylinder(d = espuma_d, h = espuma_h);
    if (planta) color(col_planta) translate([0, 0, canastilla_alto + 20 * edad]) scale([1, 1, 0.8])
        for (k = [0 : 4]) rotate([0, 0, k * 72]) translate([28 * edad, 0, 15 * edad]) sphere(r = 22 + 48 * edad, $fn = 16);
}

// Media caña de apoyo del tubo sobre la viga del soporte
module cuna(D = D_tubo, esp = cuna_esp, ancho = 40) {
    color(col_pvc_gris) rotate([0, 90, 0]) translate([0, 0, -ancho / 2]) difference() {
        cylinder(d = D + 2 * esp, h = ancho);
        translate([0, 0, -1]) cylinder(d = D + 2, h = ancho + 2);
        translate([-D, -D, -1]) cube([D, 2 * D, ancho + 2]);   // deja solo la mitad inferior
    }
}

// Soporte transversal: 2 patas + viga (a lo largo de Y) de PTR 1", altura de viga h
module soporte_transversal(ancho_viga = pies_ancho, h = 800, a = soporte_a, e = soporte_e) {
    color(col_ptr1) {
        for (s = [-1, 1]) translate([-a / 2, s * ancho_viga / 2 - a / 2, 0]) difference() {
            cube([a, a, h]);
            translate([e, e, -1]) cube([a - 2 * e, a - 2 * e, h + 2]);
        }
        translate([-a / 2, -ancho_viga / 2 - a / 2 - a, h - a]) cube([a, ancho_viga + 3 * a, a]);   // viga
    }
}

/* ================================ Línea completa =============================== */
// Línea NFT con pendiente, tapas, entrada, retorno y canastillas. Si con_soporte=true dibuja
// 3 soportes propios; en una bancada los soportes son compartidos (ver bancada_nft).
module linea_nft(L = L_tubo, D = D_tubo, n = n_plantas, s = sep_perf, dp = d_perf, p = pendiente, h0 = h_eje_alto,
                 con_soporte = mostrar_soporte, plantas = mostrar_plantas, con_retorno = true, titulo = mostrar_titulo,
                 vacias = posiciones_vacias) {
    th = ang_pend(p);
    // todo lo que va "sobre" el tubo se dibuja con la pendiente
    translate([0, 0, h0]) rotate([0, th, 0]) {
        tubo_perforado(L, D, pared_tubo, n, s, dp);
        color(col_pvc_gris) {
            translate([-tapa_esp + 8, 0, 0]) rotate([0, 90, 0]) cylinder(d = d_tapa, h = tapa_esp);   // tapa extremo alto
            translate([L - 8, 0, 0]) rotate([0, 90, 0]) cylinder(d = d_tapa, h = tapa_esp);           // tapa extremo bajo
        }
        // entrada: manguera ½" que entra por la tapa alta, arriba de la lámina de agua
        color(col_pvc_gris) translate([-tapa_esp - 60, 0, D / 2 - 25]) rotate([0, 90, 0]) cylinder(d = entrada_d, h = 90);
        color(col_valvula) translate([-tapa_esp - 60, 0, D / 2 - 25]) rotate([0, 0, 0]) cylinder(d = 24, h = 26);    // válvula de compuerta
        // retorno: adaptador de drenaje 2" en el fondo del extremo bajo
        color(col_pvc_gris) translate([L - 90, 0, -D / 2 - 60]) cylinder(d = retorno_d, h = 70);
        // canastillas con plantas (más grandes hacia el extremo bajo = más viejas)
        for (i = [0 : n - 1]) if (!en(i, vacias)) translate([x_perf(i, L, n, s), 0, D / 2 - canastilla_alto + 4])
            canastilla(edad = 0.45 + 0.55 * i / (n - 1), planta = plantas);
    }
    if (con_retorno) color(col_pvc_gris) {
        zr = z_eje(L - 90, h0, p) - D / 2 - 60;
        translate([L - 90, 0, zr - 200]) cylinder(d = retorno_d, h = 200);
        translate([L - 90, 0, zr - 200]) rotate([90, 0, 0]) cylinder(d = retorno_d, h = 350);   // hacia el retorno común
    }
    if (con_soporte) for (x = x_soportes) translate([x, 0, 0]) {
        soporte_transversal(pies_ancho, z_eje(x, h0, p) - D / 2 - cuna_esp);
        translate([0, 0, z_eje(x, h0, p)]) cuna();
    }
    if (titulo) color(col_texto) translate([-150, -pies_ancho / 2 - 260, 0]) linear_extrude(1)
        text(str("Línea NFT · PVC sanitario 4\" (OD ", D, ") × ", L / 1000, " m · ", n, " canastillas 3\" a ", s, " mm · pendiente ", p, " % · v1 · 2026-09"), size = 42, font = "DejaVu Sans");
}

/* ================================ Bancada ===================================== */
// n líneas paralelas (separadas sep_lineas en Y) sobre 3 soportes compartidos, con manifold
// de alimentación ¾" en el extremo alto y retorno común 2" en el extremo bajo.
module bancada_nft(n_lineas = 4, sep_lineas = 350, L = L_tubo, D = D_tubo, p = pendiente, h0 = h_eje_alto, plantas = mostrar_plantas) {
    ancho = (n_lineas - 1) * sep_lineas;
    for (i = [0 : n_lineas - 1]) translate([0, (i - (n_lineas - 1) / 2) * sep_lineas, 0])
        linea_nft(L = L, D = D, p = p, h0 = h0, con_soporte = false, plantas = plantas, con_retorno = false, titulo = false, vacias = []);
    for (x = x_soportes) translate([x, 0, 0]) {
        soporte_transversal(ancho + 200, z_eje(x, h0, p) - D / 2 - cuna_esp);
        for (i = [0 : n_lineas - 1]) translate([0, (i - (n_lineas - 1) / 2) * sep_lineas, z_eje(x, h0, p)]) cuna(D);
    }
    // largueros de piso que unen los 3 soportes (rigidez)
    color(col_ptr1) for (s = [-1, 1]) translate([x_soportes[0], s * (ancho + 200) / 2 - soporte_a / 2, 0])
        cube([x_soportes[len(x_soportes) - 1] - x_soportes[0], soporte_a, soporte_a]);
    // manifold ¾" de alimentación con válvula por línea (extremo alto)
    color(col_pvc_gris) translate([-tapa_esp - 60, -ancho / 2 - 150, h0 + D / 2 - 25]) rotate([-90, 0, 0]) cylinder(d = manifold_d, h = ancho + 300);
    // retorno común 2" bajo el extremo bajo
    zr = z_eje(L - 90, h0, p) - D / 2 - 60 - 200;
    color(col_pvc_gris) {
        for (i = [0 : n_lineas - 1]) translate([L - 90, (i - (n_lineas - 1) / 2) * sep_lineas, zr]) cylinder(d = retorno_d, h = 200);
        translate([L - 90, -ancho / 2 - 200, zr]) rotate([-90, 0, 0]) cylinder(d = retorno_d, h = ancho + 400);
    }
}

/* ================================ Resumen en consola =========================== */
module resumen_linea() {
    echo(str("=== LÍNEA NFT ", L_tubo, " mm · OD ", D_tubo, " · ", n_plantas, " perforaciones Ø", d_perf, " (MEDIR en la canastilla) a ", sep_perf, " mm ==="));
    echo(str("Perforaciones (mm desde el extremo alto): ", [for (i = [0 : n_plantas - 1]) x_perf(i)]));
    echo(str("Caída total con ", pendiente, " %: ", caida(), " mm en ", L_tubo, " mm"));
    for (x = x_soportes) echo(str("Soporte en x = ", x, " mm: viga a ", z_eje(x) - D_tubo / 2 - cuna_esp, " mm del piso"));
}

/* ================================ Instancia =================================== */
linea_nft();
resumen_linea();
