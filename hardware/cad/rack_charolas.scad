// ============================================================================
//  rack_charolas.scad — Rack Husky 5 niveles 1830 × 914 × 457 mm con charolas 1020 y
//  tubos LED T8 de 120 cm (HomeGreen · Fase 0 y Fase 1).
//  Modelo paramétrico OpenSCAD (probado con OpenSCAD 2021.01). Unidades: mm.
//
//  Ejes: X = ancho del rack (914), Y = fondo (457), Z = altura (1830).
//  Origen en la esquina inferior izquierda TRASERA: el frente del rack mira hacia -Y.
//
//  Fuentes: bom/fase0.csv y bom/fase1.csv (Husky 5 niveles 183 × 91.4 × 45.7 cm,
//  362.9 kg/repisa; entrepaños de MDF que hay que forrar; 8 tubos LED T8 18 W 120 cm =
//  2 por nivel iluminado), docs/referencia/03-instalacion.md §0.2 (nivel superior =
//  germinación/oscuridad, niveles medios = desarrollo, nivel inferior = recién sembradas;
//  separación vertical ≥ 30 cm) y docs/referencia/08-recetas-y-economia-unitaria.md
//  (charola 1020 = 25 × 50 cm).
//
//  Render (desde hardware/cad/):
//    xvfb-run -a openscad -o ../../docs/assets/diagramas/cad/rack-charolas.png \
//      --autocenter --viewall --imgsize=1400,1000 --projection=p \
//      --colorscheme=Tomorrow --camera=0,0,0,72,0,22,0 rack_charolas.scad
// ============================================================================

/* ------------------------------ Rack ------------------------------------------- */
rack_ancho = 914;     // [mm]
rack_fondo = 457;     // [mm]
rack_alto  = 1830;    // [mm]
niveles    = 5;
poste_a    = 38;      // sección del poste (perfil cuadrado equivalente) [mm]
poste_e    = 1.5;
riel_h     = 35;      // altura del bastidor de cada entrepaño [mm]
mdf_esp    = 15;      // entrepaño laminado (MDF) original del Husky [mm]
forro_esp  = 4;       // forro plástico / charola de drenaje sobre el MDF [mm]
z_primer_nivel = 150; // cara superior del entrepaño 1 (abajo) [mm]
z_ultimo_nivel = 1790;// cara superior del entrepaño 5 (arriba) [mm]

/* ------------------------------ Charolas --------------------------------------- */
charola            = [254, 508, 60];  // charola 1020: 10 × 20 in × 6 cm
charola_pared      = 2;
charolas_por_nivel = 3;               // 3 × 254 = 762 ≤ 914; la charola (508) sobresale
                                      // 25 mm por delante y por detrás del fondo de 457
sep_charolas       = 20;              // separación entre charolas [mm]
sustrato_h         = 30;              // ~3 cm de fibra de coco (03-instalacion §0.3)
// Estado de cada nivel, de abajo (1) hacia arriba (5). Opciones:
//   "tapada"     = recién sembrada, con segunda charola invertida y peso encima (2–4 kg)
//   "brote"      = 2–4 días, recién destapada
//   "desarrollo" = 5–8 días
//   "cosecha"    = 8–12 días, lista para cortar
estado_niveles = ["tapada", "brote", "desarrollo", "cosecha", "tapada"];

/* ------------------------------ Iluminación T8 --------------------------------- */
t8_L               = 1200;  // tubo LED T8 120 cm (sobresale 143 mm por lado del rack de 914)
t8_d               = 26;
t8_por_nivel       = 2;
niveles_iluminados = [1, 2, 3, 4];   // el nivel 5 (superior) es de oscuridad: sin tubos → 8 tubos

/* ------------------------------ Riego ------------------------------------------ */
mostrar_riego  = true;   // riser ½" en el poste trasero + lateral con 3 nebulizadores por nivel
riser_d        = 21;     // PVC ½" [mm]
lateral_d      = 10;
nebulizadores_por_nivel = 3;

mostrar_titulo = true;
$fn = 24;

/* ------------------------------ Colores ---------------------------------------- */
col_acero    = [0.16, 0.16, 0.17];
col_mdf      = [0.80, 0.68, 0.48];
col_forro    = [0.08, 0.08, 0.08];
col_charola  = [0.12, 0.12, 0.12];
col_sustrato = [0.36, 0.26, 0.16];
col_brote    = [0.80, 0.85, 0.45];
col_verde    = [0.36, 0.66, 0.30];
col_cosecha  = [0.18, 0.50, 0.22];
col_peso     = [0.55, 0.52, 0.50];
col_t8       = [0.98, 0.98, 0.88];
col_pvc      = [0.93, 0.93, 0.90];
col_texto    = [0.12, 0.16, 0.22];

/* ================================ Funciones ==================================== */
// Cara superior del entrepaño i (1 = abajo … niveles = arriba)
function z_nivel(i, n = niveles, z1 = z_primer_nivel, zn = z_ultimo_nivel) = z1 + (i - 1) * (zn - z1) / (n - 1);
// Claro libre entre la charola de un nivel y el tubo T8 del nivel de arriba
function claro_libre(i) = z_nivel(i + 1) - riel_h - t8_d - 8 - (z_nivel(i) + forro_esp + charola[2]);
// ¿Está el valor v en la lista l?
function en(v, l) = len([for (x = l) if (x == v) x]) > 0;

/* ================================ Piezas ====================================== */
// Charola 1020 hueca (pared 2 mm), origen en su esquina inferior
module charola_1020(c = charola, p = charola_pared) {
    color(col_charola, 0.95) difference() {
        cube(c);
        translate([p, p, p]) cube([c[0] - 2 * p, c[1] - 2 * p, c[2]]);
    }
}

// Charola con su contenido según el estado
module charola_con_cultivo(estado = "desarrollo", c = charola, p = charola_pared) {
    charola_1020(c, p);
    // sustrato
    color(col_sustrato) translate([p, p, p]) cube([c[0] - 2 * p, c[1] - 2 * p, sustrato_h]);
    if (estado == "tapada") {
        // segunda charola invertida encima + dos "pesos" (ladrillo/bolsa de 2–4 kg)
        translate([0, 0, 2 * c[2] + 2]) mirror([0, 0, 1]) charola_1020(c, p);
        color(col_peso) for (y = [c[1] * 0.25, c[1] * 0.75]) translate([c[0] / 2 - 90, y - 50, 2 * c[2] + 2]) cube([180, 100, 55]);
    } else if (estado == "brote") {
        color(col_brote) translate([p, p, p + sustrato_h]) cube([c[0] - 2 * p, c[1] - 2 * p, 15]);
    } else if (estado == "desarrollo") {
        color(col_verde) translate([p, p, p + sustrato_h]) cube([c[0] - 2 * p, c[1] - 2 * p, 45]);
    } else {  // "cosecha"
        color(col_cosecha) translate([p, p, p + sustrato_h]) cube([c[0] - 2 * p, c[1] - 2 * p, 85]);
    }
}

// Entrepaño i: bastidor + MDF + forro
module entrepano(i) {
    z = z_nivel(i);
    color(col_acero) difference() {
        translate([0, 0, z - riel_h]) cube([rack_ancho, rack_fondo, riel_h]);
        translate([poste_a, poste_a, z - riel_h - 1]) cube([rack_ancho - 2 * poste_a, rack_fondo - 2 * poste_a, riel_h + 2]);
    }
    color(col_mdf) translate([poste_a - 5, poste_a - 5, z - mdf_esp]) cube([rack_ancho - 2 * poste_a + 10, rack_fondo - 2 * poste_a + 10, mdf_esp]);
    color(col_forro) translate([4, 4, z]) cube([rack_ancho - 8, rack_fondo - 8, forro_esp]);
}

// Tubo LED T8 a lo largo de X
module tubo_t8(L = t8_L, d = t8_d) {
    color(col_t8) rotate([0, 90, 0]) cylinder(d = d, h = L);
    color([0.2, 0.6, 0.3]) for (x = [0, L - 25]) translate([x, 0, 0]) rotate([0, 90, 0]) cylinder(d = d + 1, h = 25);  // casquillos
}

/* ================================ Rack completo ================================ */
module rack_husky(estados = estado_niveles, iluminados = niveles_iluminados, riego = mostrar_riego,
                  n = niveles, ancho = rack_ancho, fondo = rack_fondo, alto = rack_alto,
                  por_nivel = charolas_por_nivel, titulo = mostrar_titulo) {
    // postes
    color(col_acero) for (x = [0, ancho - poste_a]) for (y = [0, fondo - poste_a])
        translate([x, y, 0]) difference() {
            cube([poste_a, poste_a, alto]);
            translate([poste_e, poste_e, -1]) cube([poste_a - 2 * poste_e, poste_a - 2 * poste_e, alto + 2]);
        }
    // entrepaños y charolas
    total = por_nivel * charola[0] + (por_nivel - 1) * sep_charolas;
    x0 = (ancho - total) / 2;
    y0 = (fondo - charola[1]) / 2;   // la charola de 508 sobresale (fondo 457)
    for (i = [1 : n]) {
        entrepano(i);
        for (k = [0 : por_nivel - 1])
            translate([x0 + k * (charola[0] + sep_charolas), y0, z_nivel(i) + forro_esp])
                charola_con_cultivo(estados[i - 1]);
    }
    // tubos T8 bajo el entrepaño superior de cada nivel iluminado
    for (i = iluminados) if (i < n) {
        zt = z_nivel(i + 1) - riel_h - t8_d / 2 - 6;
        for (k = [1 : t8_por_nivel]) translate([(ancho - t8_L) / 2, fondo * k / (t8_por_nivel + 1), zt]) tubo_t8();
    }
    // riego: riser ½" por el poste trasero izquierdo + lateral con nebulizadores por nivel
    if (riego) color(col_pvc) {
        translate([-riser_d / 2 - 4, fondo + riser_d / 2 + 4, 0]) cylinder(d = riser_d, h = alto - 30);
        for (i = iluminados) if (i < n) {
            zl = z_nivel(i + 1) - riel_h - 45;
            translate([-riser_d / 2 - 4, fondo + riser_d / 2 + 4, zl]) rotate([90, 0, 0]) cylinder(d = lateral_d, h = riser_d / 2 + 4 + 40);
            translate([-riser_d / 2 - 4, fondo - 40, zl]) rotate([0, 90, 0]) cylinder(d = lateral_d, h = ancho + riser_d / 2 + 4);
            for (k = [1 : nebulizadores_por_nivel])
                translate([ancho * (k - 0.5) / nebulizadores_por_nivel, fondo - 40, zl - lateral_d / 2]) rotate([180, 0, 0]) cylinder(d1 = 12, d2 = 4, h = 18);
        }
    }
    if (titulo) color(col_texto) translate([-160, -400, 0]) linear_extrude(1)
        text(str("Rack Husky 5 niveles · ", alto, " × ", ancho, " × ", fondo, " mm · v1 · 2026-09"), size = 44, font = "DejaVu Sans");
}

/* ================================ Resumen en consola =========================== */
module resumen_rack() {
    echo(str("=== RACK ", rack_alto, " x ", rack_ancho, " x ", rack_fondo, " mm · ", niveles, " niveles ==="));
    for (i = [1 : niveles]) echo(str("Nivel ", i, ": cara superior a ", z_nivel(i), " mm · estado: ", estado_niveles[i - 1],
        (i < niveles) ? str(" · claro libre sobre la charola hasta el tubo T8: ", claro_libre(i), " mm") : " · superior (sin tubo)"));
    echo(str("Charolas: ", charolas_por_nivel * niveles, " (", charolas_por_nivel, " por nivel) · Tubos T8: ", t8_por_nivel * len(niveles_iluminados)));
    echo(str("Voladizo del tubo T8 de ", t8_L, " mm sobre el rack de ", rack_ancho, " mm: ", (t8_L - rack_ancho) / 2, " mm por lado"));
}

/* ================================ Instancia =================================== */
rack_husky();
resumen_rack();
