// ============================================================================
//  tunel_3x6.scad — Túnel a dos aguas 3 × 6 m en PTR 1½" cal. 14 (HomeGreen · Fase 1)
//  Modelo paramétrico OpenSCAD (probado con OpenSCAD 2021.01).
//
//  Unidades: mm.  Ejes: X = ancho (oeste → este), Y = largo (sur → norte), Z = altura.
//  La cumbrera corre a lo largo de Y. La puerta va en la cabecera norte (y = largo),
//  porque el acceso al patio se supone al norte (ver docs/diseno/layout-patio.md).
//
//  Criterios de diseño (fuente: docs/research/instalacion-tunel-detalle.md y
//  docs/research/estructura-invernadero.md; resumen en docs/diseno/estructura-tunel.md):
//   - PTR 1½" × 1½" cal. 14 (38 mm, pared 1.9 mm) en columnas, cabios, cumbrera,
//     largueros de alero y cabeceras. PTR 1" (25 mm) en cabios intermedios, largueros
//     de techo, contravientos y postes de la malla antigranizo.
//   - 6 columnas (3 pórticos) con placa base 100 × 100 mm y 4 anclas de cuña 3/8" × 5"
//     por placa (24 anclas), sobre losa de concreto.
//   - Techo a dos aguas con pendiente ≥ 25 % (aquí 30 %) para que escurra el granizo.
//   - Plástico UV cal. 720 como superficie translúcida; malla antigranizo 150 mm por
//     encima del plástico, sobre postes cortos.
//   - Contravientos: una cruz de San Andrés por fachada larga + escuadras a 45° en las
//     4 esquinas de las cabeceras.
//   - Canalón de PVC en cada alero (pendiente 0.75 %) con bajante hacia el tinaco.
//
//  Render (desde hardware/cad/):
//    xvfb-run -a openscad -o ../../docs/assets/diagramas/cad/tunel-3x6.png \
//      --autocenter --viewall --imgsize=1400,1000 --projection=p \
//      --colorscheme=Tomorrow --camera=0,0,0,62,0,212,0 tunel_3x6.scad
//  La lista de cortes se imprime en consola (ECHO) cada vez que se abre o renderiza.
//
//  Para el túnel de 5 × 6 m NO copies este archivo: tunel_5x6.scad hace
//  `use <tunel_3x6.scad>` y llama a tunel(ancho=5000, ...). Cambia parámetros aquí
//  solo si cambia el diseño del túnel de Fase 1.
// ============================================================================

/* ------------------------------ Geometría general ------------------------------ */
ancho       = 3000;   // ancho exterior (cara a cara de columnas) [mm]
largo       = 6000;   // largo entre ejes de los pórticos extremos [mm]
n_porticos  = 3;      // pórticos de 2 columnas: 3 → 6 columnas, separación 3 m
h_columna   = 2000;   // altura de columna hasta el alero [mm]
pendiente   = 30;     // pendiente del techo [%]; mínimo 25 % (granizo y lluvia)

/* ------------------------------ Perfiles PTR ----------------------------------- */
ptr_a  = 38;    // PTR 1½" × 1½" (38.1 mm) — estructura principal
ptr_e  = 1.9;   // pared cal. 14 [mm]
ptr_b  = 25;    // PTR 1" × 1" (25.4 mm) — elementos ligeros
ptr_be = 1.9;

/* ------------------------------ Cabeceras y puerta ----------------------------- */
puerta_ancho    = 900;    // vano libre de la puerta [mm]
puerta_alto     = 1900;   // altura del dintel [mm]
h_rodapie       = 500;    // altura del travesaño bajo de cabecera [mm]
largueros_techo = 1;      // largueros intermedios de techo por agua (2 para 5 m de ancho)
escuadra        = 600;    // cateto de las escuadras de esquina a 45° [mm]

/* ------------------------------ Placa base y anclas ---------------------------- */
placa_lado     = 100;   // placa cuadrada [mm]
placa_esp      = 6;     // solera ¼" ≈ 6.35 mm (el informe admite 3/16"–¼")
ancla_n        = 4;     // anclas de cuña por placa
ancla_d        = 9.5;   // 3/8" = 9.5 mm
ancla_L        = 127;   // 5" = 127 mm
ancla_sep      = 70;    // separación entre centros de anclas [mm] (15 mm al borde)
ancla_saliente = 22;    // lo que sobresale sobre la placa (rondana + tuerca + rosca) [mm]

/* ------------------------------ Cubierta --------------------------------------- */
sep_malla      = 150;   // separación malla antigranizo – plástico [mm] (informe: 10–20 cm)
esp_lamina     = 1.5;   // grosor de dibujo de plástico y malla [mm]
alpha_plastico = 0.35;  // transparencia del plástico blanco lechoso 25 % sombra
alpha_malla    = 0.22;  // transparencia de la malla antigranizo
voladizo       = 60;    // cuánto sobresale el plástico del alero y de las cabeceras [mm]

/* ------------------------------ Canalón ---------------------------------------- */
canalon_d      = 110;   // canalón PVC doméstico ~11 cm [mm]
canalon_pend   = 0.75;  // pendiente del canalón [%] (informe: 0.5–1 %)
bajante_d      = 75;    // bajante 3" [mm]
lado_bajante   = 1;     // +1 = bajante en el alero este, -1 = oeste, 0 = sin bajante

/* ------------------------------ Qué dibujar ------------------------------------ */
mostrar_losa          = true;
mostrar_plastico      = true;
mostrar_malla         = true;
mostrar_canalon       = true;
mostrar_contravientos = true;
mostrar_placas        = true;
mostrar_titulo        = true;   // rótulo sobre la losa: "Túnel 3 × 6 m · v1 · 2026-09"
titulo_norte          = true;   // true: rótulo junto a la cabecera norte (para cámara desde el noreste)
$fn = 24;

/* ------------------------------ Colores ---------------------------------------- */
col_ptr15   = [0.19, 0.25, 0.30];   // PTR 1½" (gris azulado oscuro)
col_ptr1    = [0.72, 0.46, 0.09];   // PTR 1" (ámbar): se distingue en el render
col_placa   = [0.35, 0.35, 0.35];
col_ancla   = [0.80, 0.80, 0.82];
col_plast   = [1.00, 1.00, 1.00];
col_malla   = [0.25, 0.25, 0.28];
col_canalon = [0.93, 0.93, 0.90];
col_losa    = [0.78, 0.77, 0.74];
col_texto   = [0.12, 0.16, 0.22];

/* ================================ Funciones ==================================== */
// Peralte del techo (subida desde el alero hasta la cumbrera)
function rise(ancho, pend) = (ancho / 2) * pend / 100;
// Ángulo del agua respecto a la horizontal [°]
function ang_techo(ancho, pend) = atan(pend / 100);
// Longitud de corte del cabio (eje alero → eje cumbrera) + un perfil de traslape
function L_cabio(ancho, pend, a) = sqrt(pow(ancho / 2 - a / 2, 2) + pow(rise(ancho, pend), 2)) + a;
// Separación entre pórticos
function sep_porticos(largo, n) = largo / (n - 1);
// Suma de un vector numérico
function suma(v, i = 0) = i >= len(v) ? 0 : v[i] + suma(v, i + 1);
// Altura del eje del cabio en una abscisa x (medida desde el eje de la columna)
function z_cabio(x, ancho, h_col, pend, a) = h_col + a + (ancho / 2 - abs(x)) * pend / 100;

/* ================================ Primitivas =================================== */
// Barra de PTR hueca a lo largo de +Z, centrada en XY
module ptr(L, a = 38, e = 1.9) {
    translate([-a / 2, -a / 2, 0]) difference() {
        cube([a, a, L]);
        translate([e, e, -1]) cube([a - 2 * e, a - 2 * e, L + 2]);
    }
}

// Barra de PTR entre dos puntos 3D (para diagonales y cabios)
module barra(p1, p2, a = 38, e = 1.9) {
    v = p2 - p1;
    L = norm(v);
    b = acos(v[2] / L);
    c = atan2(v[1], v[0]);
    translate(p1) rotate([0, b, c]) ptr(L, a, e);
}

// Lámina delgada en el plano XZ entre p1=[x,z] y p2=[x,z], extruida de y0 a y1
module lamina(p1, p2, y0, y1, esp = 1.5) {
    v = [p2[0] - p1[0], p2[1] - p1[1]];
    L = norm(v);
    b = atan2(v[0], v[1]);
    translate([p1[0], y0, p1[1]]) rotate([0, b, 0]) translate([-esp / 2, 0, 0]) cube([esp, y1 - y0, L]);
}

// Placa base 100 × 100 con 4 anclas de cuña 3/8" × 5" (la parte embebida queda en la losa)
module placa_base(lado = placa_lado, esp = placa_esp, n = ancla_n, sep = ancla_sep,
                  d = ancla_d, L = ancla_L, saliente = ancla_saliente) {
    color(col_placa) translate([-lado / 2, -lado / 2, 0]) cube([lado, lado, esp]);
    pos = (n == 4) ? [[-1, -1], [1, -1], [-1, 1], [1, 1]] : [[-1, 0], [1, 0]];
    for (p = pos) translate([p[0] * sep / 2, p[1] * sep / 2, 0]) color(col_ancla) {
        translate([0, 0, -(L - esp - saliente)]) cylinder(d = d, h = L);          // ancla
        translate([0, 0, esp]) cylinder(d = 22, h = 2);                           // rondana
        translate([0, 0, esp + 2]) cylinder(d = 16 / cos(30), h = 8, $fn = 6);    // tuerca 9/16"
    }
}

// Canalón de PVC (media caña) a lo largo de +Y, con pendiente hacia y = L (norte)
module canalon(L, d = canalon_d, pend = canalon_pend) {
    rotate([-atan(pend / 100), 0, 0]) rotate([-90, 0, 0]) difference() {
        cylinder(d = d, h = L);
        translate([0, 0, -1]) cylinder(d = d - 6, h = L + 2);
        translate([-d, -d, -1]) cube([2 * d, d, L + 2]);   // quita la mitad superior
    }
}

/* ================================ Estructura =================================== */
// Pórtico: dos columnas (opcionales) + dos cabios en el plano y = y0
module portico(y0, ancho, h_col, pend, a, e, con_columnas = true, a_cabio = 38, e_cabio = 1.9, col = col_ptr15) {
    r  = rise(ancho, pend);
    xc = ancho / 2 - a / 2;      // eje de columna
    z0 = h_col + a;              // arranque del eje del cabio (sobre el larguero de alero)
    zc = z0 + r;                 // eje del cabio en la cumbrera
    if (con_columnas) color(col_ptr15) for (s = [-1, 1]) translate([s * xc, y0, 0]) ptr(h_col, a, e);
    color(col) {
        barra([-xc, y0, z0], [0, y0, zc], a_cabio, e_cabio);
        barra([ xc, y0, z0], [0, y0, zc], a_cabio, e_cabio);
    }
}

// Túnel completo
module tunel(ancho = ancho, largo = largo, n_porticos = n_porticos, h_col = h_columna, pend = pendiente,
             a = ptr_a, e = ptr_e, b = ptr_b, eb = ptr_be,
             puerta_ancho = puerta_ancho, puerta_alto = puerta_alto, h_rodapie = h_rodapie,
             largueros_techo = largueros_techo, escuadra = escuadra, sep_malla = sep_malla,
             losa = mostrar_losa, plastico = mostrar_plastico, malla = mostrar_malla,
             canalon_on = mostrar_canalon, contravientos = mostrar_contravientos, placas = mostrar_placas,
             lado_bajante = lado_bajante, titulo = mostrar_titulo, titulo_norte = titulo_norte,
             alpha_p = alpha_plastico, alpha_m = alpha_malla, esp = esp_lamina, voladizo = voladizo,
             texto_titulo = "") {

    r    = rise(ancho, pend);
    th   = ang_techo(ancho, pend);
    xc   = ancho / 2 - a / 2;            // eje de columna
    z0   = h_col + a;                    // eje del cabio en el alero
    zc   = z0 + r;                       // eje del cabio en la cumbrera
    sep  = sep_porticos(largo, n_porticos);
    xj   = puerta_ancho / 2 + a / 2;     // eje de las jambas

    /* --- Losa de concreto (solo contexto visual) --- */
    if (losa) color(col_losa)
        translate([-ancho / 2 - 600, -600, -120]) cube([ancho + 1200, largo + 1200, 120]);

    /* --- Pórticos principales (PTR 1½") --- */
    for (i = [0 : n_porticos - 1]) {
        y0 = i * sep;
        portico(y0, ancho, h_col, pend, a, e, true, a, e, col_ptr15);
        if (placas) for (s = [-1, 1]) translate([s * xc, y0, 0]) placa_base();
    }

    /* --- Cabios intermedios (PTR 1") a media crujía, apoyados en alero y cumbrera --- */
    color(col_ptr1) for (i = [0 : n_porticos - 2])
        portico((i + 0.5) * sep, ancho, h_col, pend, a, e, false, b, eb, col_ptr1);

    /* --- Cumbrera y largueros de alero (PTR 1½") --- */
    color(col_ptr15) {
        translate([0, 0, zc - a]) rotate([-90, 0, 0]) ptr(largo, a, e);                       // cumbrera
        for (s = [-1, 1]) translate([s * xc, 0, h_col + a / 2]) rotate([-90, 0, 0]) ptr(largo, a, e); // aleros
    }

    /* --- Largueros intermedios de techo (PTR 1"), por la cara interior del cabio --- */
    color(col_ptr1) for (s = [-1, 1]) for (k = [1 : largueros_techo]) {
        t  = k / (largueros_techo + 1);
        px = s * xc * (1 - t);
        pz = z0 + t * r - (a / 2 + b / 2) / cos(th);      // debajo del cabio
        translate([px, 0, pz]) rotate([0, -s * th, 0]) rotate([-90, 0, 0]) ptr(largo, b, eb);
    }

    /* --- Cabeceras (PTR 1½") --- */
    color(col_ptr15) for (y0 = [0, largo]) {
        norte = (y0 == largo);
        // travesaño alto (a la altura del alero) y bajo (rodapié)
        translate([-(xc - a / 2), y0, h_col + a / 2]) rotate([0, 90, 0]) ptr(ancho - 2 * a, a, e);
        if (!norte) {
            translate([-(xc - a / 2), y0, h_rodapie]) rotate([0, 90, 0]) ptr(ancho - 2 * a, a, e);
            translate([0, y0, 0]) ptr(zc - a, a, e);                                        // poste central sur
        } else {
            Lb = xc - a / 2 - xj - a / 2;                                                   // rodapié partido
            translate([-(xc - a / 2), y0, h_rodapie]) rotate([0, 90, 0]) ptr(Lb, a, e);
            translate([xj + a / 2, y0, h_rodapie]) rotate([0, 90, 0]) ptr(Lb, a, e);
            for (s = [-1, 1]) translate([s * xj, y0, 0]) ptr(h_col, a, e);                   // jambas
            translate([-puerta_ancho / 2, y0, puerta_alto + a / 2]) rotate([0, 90, 0]) ptr(puerta_ancho, a, e); // dintel
            translate([0, y0, h_col + a]) ptr(r - a, a, e);                                  // pendolón
        }
    }

    /* --- Contravientos (PTR 1") --- */
    if (contravientos) color(col_ptr1) {
        // cruz de San Andrés en la primera crujía de cada fachada larga
        for (s = [-1, 1]) {
            barra([s * xc, a, a], [s * xc, sep - a, h_col - a], b, eb);
            barra([s * xc, a, h_col - a], [s * xc, sep - a, a], b, eb);
        }
        // escuadras a 45° en las 4 esquinas (plano de cabecera)
        for (s = [-1, 1]) for (y0 = [0, largo])
            barra([s * xc, y0, h_col - escuadra], [s * (xc - escuadra), y0, h_col], b, eb);
    }

    /* --- Plástico UV (superficie translúcida) --- */
    zp0 = z0 + (a / 2 + 2) / cos(th);                       // cara exterior del plástico en el alero
    xe  = ancho / 2 + voladizo;                             // borde del plástico (voladizo)
    zpe = zp0 - voladizo * pend / 100;                      // altura del borde del voladizo
    zpc = zc + (a / 2 + 2) / cos(th);                       // cara exterior en la cumbrera
    if (plastico) color(col_plast, alpha_p) {
        for (s = [-1, 1])
            lamina([s * xe, zpe], [0, zpc], -voladizo, largo + voladizo, esp);              // dos aguas
        for (s = [-1, 1])
            translate([s * (ancho / 2 + 3) - esp / 2, 0, 0]) cube([esp, largo, h_col + a]);  // cortinas laterales
        // cabeceras (pentágono); la norte lleva el hueco de la puerta
        for (y0 = [0, largo]) translate([0, (y0 == 0) ? -3 : largo + 3 + esp, 0]) rotate([90, 0, 0])
            linear_extrude(esp) difference() {
                polygon([[-ancho / 2, 0], [ancho / 2, 0], [ancho / 2, h_col + a], [0, zc + a / 2], [-ancho / 2, h_col + a]]);
                if (y0 == largo) translate([-puerta_ancho / 2, -1]) square([puerta_ancho, puerta_alto + 1]);
            }
    }

    /* --- Malla antigranizo 150 mm sobre el plástico, sobre postes cortos de PTR 1" --- */
    if (malla) {
        color(col_malla, alpha_m) for (s = [-1, 1])
            lamina([s * xe, zpe + sep_malla], [0, zpc + sep_malla], -voladizo, largo + voladizo, esp);
        color(col_ptr1) for (i = [0 : n_porticos - 1]) for (t = [0, 0.5, 1]) for (s = [-1, 1])
            if (!(t == 1 && s == 1)) {   // la cumbrera se comparte
                px = s * xc * (1 - t);
                translate([px, i * sep, z0 + t * r]) ptr(sep_malla + 20, b, eb);
            }
        // alambre galvanizado longitudinal sobre los postes (soporte de la malla)
        color(col_ancla) for (t = [0, 0.5, 1]) for (s = [-1, 1]) if (!(t == 1 && s == 1))
            translate([s * xc * (1 - t), 0, z0 + t * r + sep_malla + 17]) rotate([-90, 0, 0]) cylinder(d = 3, h = largo);
    }

    /* --- Canalón en cada alero + bajante --- */
    if (canalon_on) color(col_canalon) {
        for (s = [-1, 1]) translate([s * (xe + canalon_d / 2 - 20), 0, zpe - 8]) canalon(largo);
        if (lado_bajante != 0) {
            xb = lado_bajante * (xe + canalon_d / 2 - 20);
            zb = zpe - 8 - largo * canalon_pend / 100 - canalon_d / 2;
            translate([xb, largo + 40, 250]) cylinder(d = bajante_d, h = zb - 250);                 // bajante
            translate([xb, largo + 40, 250]) rotate([0, lado_bajante * 90, 0]) cylinder(d = bajante_d, h = 400); // hacia el tinaco
        }
    }

    /* --- Rótulo --- */
    if (titulo) color(col_texto)
        translate(titulo_norte ? [ancho / 2 + 450, largo + 520, 0.5] : [-ancho / 2 - 450, -520, 0.5])
        rotate([0, 0, titulo_norte ? 180 : 0]) linear_extrude(1)
        text(texto_titulo == "" ? str("Túnel ", ancho / 1000, " × ", largo / 1000, " m · PTR 1½\" cal. 14 · v1 · 2026-09")
                                : texto_titulo, size = 110, font = "DejaVu Sans");
}

/* ================================ Lista de cortes ============================== */
// Devuelve [[pieza, perfil, cantidad, longitud_mm], ...]
function piezas_tunel(ancho = ancho, largo = largo, n_porticos = n_porticos, h_col = h_columna, pend = pendiente,
                      a = ptr_a, b = ptr_b, puerta_ancho = puerta_ancho, puerta_alto = puerta_alto,
                      largueros_techo = largueros_techo, escuadra = escuadra, sep_malla = sep_malla) =
    let (r = rise(ancho, pend), xc = ancho / 2 - a / 2, zc = h_col + a + r,
         sep = sep_porticos(largo, n_porticos), Lc = round(L_cabio(ancho, pend, a)),
         xj = puerta_ancho / 2 + a / 2)
    [
        ["Columna",                                   "PTR 1 1/2", 2 * n_porticos,       h_col],
        ["Cabio a dos aguas",                         "PTR 1 1/2", 2 * n_porticos,       Lc],
        ["Cumbrera",                                  "PTR 1 1/2", 1,                    largo],
        ["Larguero de alero",                         "PTR 1 1/2", 2,                    largo],
        ["Travesaño alto de cabecera",                "PTR 1 1/2", 2,                    ancho - 2 * a],
        ["Travesaño bajo cabecera sur",               "PTR 1 1/2", 1,                    ancho - 2 * a],
        ["Travesaño bajo cabecera norte (partido)",   "PTR 1 1/2", 2,                    round(xc - a / 2 - xj - a / 2)],
        ["Poste central cabecera sur",                "PTR 1 1/2", 1,                    round(zc - a)],
        ["Jamba de puerta",                           "PTR 1 1/2", 2,                    h_col],
        ["Dintel de puerta",                          "PTR 1 1/2", 1,                    puerta_ancho],
        ["Pendolón cabecera norte",                   "PTR 1 1/2", 1,                    round(r - a)],
        ["Cabio intermedio (arco sin columna)",       "PTR 1",     2 * (n_porticos - 1), Lc],
        ["Larguero intermedio de techo",              "PTR 1",     2 * largueros_techo,  largo],
        ["Tirante cruz de San Andrés (fachada larga)","PTR 1",     4,                    round(sqrt(pow(sep - 2 * a, 2) + pow(h_col - 2 * a, 2)))],
        ["Escuadra de esquina 45° (cabeceras)",       "PTR 1",     4,                    round(sqrt(2) * escuadra)],
        ["Poste de malla antigranizo",                "PTR 1",     5 * n_porticos,       sep_malla + 20]
    ];

module lista_cortes(ancho = ancho, largo = largo, n_porticos = n_porticos, h_col = h_columna, pend = pendiente,
                    a = ptr_a, b = ptr_b, puerta_ancho = puerta_ancho, puerta_alto = puerta_alto,
                    largueros_techo = largueros_techo, escuadra = escuadra, sep_malla = sep_malla) {
    p = piezas_tunel(ancho, largo, n_porticos, h_col, pend, a, b, puerta_ancho, puerta_alto, largueros_techo, escuadra, sep_malla);
    echo(str("=== LISTA DE CORTES túnel ", ancho / 1000, " x ", largo / 1000, " m · ", n_porticos, " pórticos · pendiente ", pend, " % ==="));
    for (q = p) echo(str(q[1], " | ", q[0], " | ", q[2], " pza x ", q[3], " mm"));
    m15 = suma([for (q = p) if (q[1] == "PTR 1 1/2") q[2] * q[3]]);
    m1  = suma([for (q = p) if (q[1] == "PTR 1") q[2] * q[3]]);
    echo(str("PTR 1 1/2 cal. 14: ", m15 / 1000, " m lineales -> mínimo teórico ", ceil(m15 / 6000), " tramos de 6 m (sin desperdicio)"));
    echo(str("PTR 1: ", m1 / 1000, " m lineales -> mínimo teórico ", ceil(m1 / 6000), " tramos de 6 m (sin desperdicio)"));
    echo(str("Placas base ", placa_lado, "x", placa_lado, " mm: ", 2 * n_porticos, " | Anclas de cuña 3/8\" x 5\": ", 2 * n_porticos * ancla_n));
    echo(str("Altura de cumbrera (eje): ", h_col + a + rise(ancho, pend), " mm | ángulo del agua: ", ang_techo(ancho, pend), " °"));
}

/* ================================ Instancia =================================== */
tunel();
lista_cortes();
