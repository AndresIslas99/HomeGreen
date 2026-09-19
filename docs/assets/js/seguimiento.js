/* HomeGreen · tablero de seguimiento del proyecto
 * ---------------------------------------------------------------------------
 * Convierte la wiki en algo que ademas registra el avance: que se compro y a
 * que precio real, en que va cada gate y cada validacion, y con que parametros
 * economicos se esta trabajando.
 *
 * Donde vive el dato: en localStorage de ESTE navegador. No hay servidor. Eso
 * significa dos cosas que la pagina dice en voz alta:
 *   - si limpias el navegador o entras desde otro dispositivo, no esta;
 *   - por eso el boton de exportar no es un extra, es la copia de seguridad.
 * El registro duradero sigue siendo el repo: los CSV de bitacora/.
 *
 * El candado de parametros es un candado de puerta de cristal: esto es un sitio
 * estatico, el codigo se descarga al navegador y cualquiera puede saltarselo
 * editando el JS. Sirve para no mover un umbral sin querer y para ensenarle el
 * tablero a alguien sin que lo edite. No es seguridad.
 */
(function () {
  'use strict';

  var DATOS_URL = 'assets/datos/seguimiento.json';
  var CLAVE = 'homegreen.seguimiento.v1';
  // SHA-256 de la contrasena. Se guarda el hash y no el texto para que no se lea
  // de un vistazo en el codigo fuente; aun asi es saltable, ver la nota de arriba.
  var HASH = 'db268aa17bd2ddcf9f510ed39ff1b8599c41e27bf605f29a59d2ab05c99dd9b4';

  var datos = null;
  var estado = cargar();
  var desbloqueado = false;
  var pestana = 'compras';
  var filtroFase = 'todas';
  var soloPendientes = false;
  // presencial | linea. Cambia que proveedor y que precio se muestra por partida,
  // y con ello el presupuesto. Lo que no viaja por paqueteria no cambia: sigue
  // siendo presencial en los dos modos, y se marca como tal.
  var modo = 'presencial';

  // -- persistencia ---------------------------------------------------------
  function vacio() {
    return { compras: {}, gates: {}, validaciones: {}, parametros: {}, umbrales: {}, actualizado: null };
  }

  function cargar() {
    try {
      var s = window.localStorage.getItem(CLAVE);
      if (!s) return vacio();
      var d = JSON.parse(s);
      var v = vacio();
      Object.keys(v).forEach(function (k) { if (d[k] === undefined) d[k] = v[k]; });
      return d;
    } catch (e) {
      // Ventana privada, almacenamiento bloqueado o JSON corrupto: se arranca en
      // limpio en vez de romper la pagina.
      return vacio();
    }
  }

  function guardar() {
    estado.actualizado = new Date().toISOString();
    try {
      window.localStorage.setItem(CLAVE, JSON.stringify(estado));
      marcarGuardado(true);
    } catch (e) {
      marcarGuardado(false);
    }
  }

  function marcarGuardado(ok) {
    var el = document.getElementById('hg-guardado');
    if (!el) return;
    if (ok) {
      var f = new Date();
      el.textContent = 'Guardado en este navegador · ' +
        f.toLocaleDateString('es-MX') + ' ' + f.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
      el.className = 'hg-guardado';
    } else {
      el.textContent = 'NO se pudo guardar: este navegador tiene el almacenamiento bloqueado. Exporta antes de cerrar.';
      el.className = 'hg-guardado hg-error';
    }
  }

  // -- utilidades -----------------------------------------------------------
  function mxn(v) {
    return '$' + (Math.round(v || 0)).toLocaleString('es-MX');
  }

  function esc(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function el(id) { return document.getElementById(id); }

  async function sha256(txt) {
    var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(txt));
    return Array.from(new Uint8Array(buf)).map(function (b) {
      return b.toString(16).padStart(2, '0');
    }).join('');
  }

  function umbral(gateId, critId, porDefecto) {
    var k = gateId + '.' + critId;
    return estado.umbrales[k] !== undefined ? estado.umbrales[k] : porDefecto;
  }

  function cumple(valor, comparador, u) {
    if (valor === '' || valor === null || valor === undefined || isNaN(valor)) return null;
    var v = Number(valor), t = Number(u);
    if (comparador === '>=') return v >= t;
    if (comparador === '<=') return v <= t;
    if (comparador === '<') return v < t;
    if (comparador === '>') return v > t;
    if (comparador === '==') return v === t;
    return null;
  }

  // Devuelve el precio y el proveedor que aplican segun el modo elegido. En modo
  // en linea, una partida que no viaja se queda con su dato presencial.
  function enLinea(c) {
    return !!(c.online && !c.solo_presencial && c.online.bloque && c.online.bloque !== 'presencial');
  }

  function vigente(c) {
    if (modo === 'linea' && enLinea(c)) {
      return { subtotal: c.online.subtotal, precio: c.online.precio,
               donde: c.online.proveedor, bloque: c.online.bloque_nombre,
               fisica: false, enlace: c.online.enlace, nota: c.online.notas };
    }
    return { subtotal: c.subtotal, precio: c.precio, donde: c.donde, bloque: null,
             fisica: c.presencial, enlace: '', nota: '' };
  }

  // Envio del escenario en linea: se paga por BLOQUE, no por partida. Es justo el
  // punto: varios productos del mismo bloque comparten un solo envio.
  function envios(filtradas) {
    var grupos = {};
    filtradas.forEach(function (c) {
      if (!c.cuenta || !enLinea(c)) return;
      var b = c.online.bloque;
      grupos[b] = (grupos[b] || 0) + c.online.subtotal;
    });
    var total = 0, detalle = [];
    Object.keys(grupos).forEach(function (b) {
      var r = (datos.envios || []).filter(function (x) { return x.id === b; })[0] || {};
      var gratis = r.umbral && grupos[b] >= r.umbral;
      var costo = gratis ? 0 : (r.envio || 0);
      total += costo;
      detalle.push({ id: b, nombre: r.nombre || b, productos: grupos[b], envio: costo, gratis: gratis });
    });
    detalle.sort(function (a, b) { return b.productos - a.productos; });
    return { total: total, detalle: detalle };
  }

  // -- render: compras ------------------------------------------------------
  function renderCompras() {
    var items = datos.compras.filter(function (c) {
      if (filtroFase !== 'todas' && String(c.fase) !== filtroFase) return false;
      if (soloPendientes && (estado.compras[c.id] || {}).comprado) return false;
      return true;
    });

    var enFase = datos.compras.filter(function (c) {
      return filtroFase === 'todas' || String(c.fase) === filtroFase;
    });

    var planTotal = 0, realTotal = 0, nComp = 0, nCuenta = 0;
    enFase.forEach(function (c) {
      if (!c.cuenta) return;
      var v = vigente(c);
      nCuenta++;
      planTotal += v.subtotal;
      var e = estado.compras[c.id] || {};
      if (e.comprado) {
        nComp++;
        realTotal += (e.real !== undefined && e.real !== '') ? Number(e.real) : v.subtotal;
      }
    });
    var env = modo === 'linea' ? envios(enFase) : { total: 0, detalle: [] };
    planTotal += env.total;

    var pct = nCuenta ? Math.round(100 * nComp / nCuenta) : 0;
    var desv = realTotal - enFase.reduce(function (a, c) {
      if (!c.cuenta) return a;
      var e = estado.compras[c.id] || {};
      return a + (e.comprado ? vigente(c).subtotal : 0);
    }, 0);

    var h = '';
    h += '<div class="hg-resumen">';
    h += tarjeta('Comprado', nComp + ' / ' + nCuenta, pct + ' % de las partidas');
    h += tarjeta('Presupuesto', mxn(planTotal), modo === 'linea'
      ? 'producto + ' + mxn(env.total) + ' de envíos' : 'comprando en persona');
    h += tarjeta('Gastado', mxn(realTotal), 'precio real de lo ya comprado');
    h += tarjeta('Contra el plan', (desv >= 0 ? '+' : '') + mxn(desv),
      desv > 0 ? 'por encima de lo presupuestado' : (desv < 0 ? 'por debajo: bien' : 'exacto'),
      desv > 0 ? 'mal' : 'bien');
    h += '</div>';

    h += '<div class="hg-barra"><div class="hg-barra-int" style="width:' + pct + '%"></div></div>';

    if (modo === 'linea') {
      var sinEnviar = enFase.filter(function (c) { return c.cuenta && !enLinea(c); });
      var montoSin = sinEnviar.reduce(function (a, c) { return a + c.subtotal; }, 0);
      h += '<div class="hg-envios"><strong>En ' + env.detalle.length + ' pedidos, ' +
           mxn(env.total) + ' de envío.</strong> El envío se paga por pedido, no por partida: ' +
           'es lo que hace que agrupar valga la pena.';
      h += '<table class="hg-tabla"><thead><tr><th>Pedido</th><th>Producto</th><th>Envío</th></tr></thead><tbody>';
      env.detalle.forEach(function (d) {
        h += '<tr><td>' + esc(d.nombre) + '</td><td class="hg-num">' + mxn(d.productos) + '</td>' +
             '<td class="hg-num">' + (d.envio === 0
               ? '<span class="hg-bien">$0' + (d.gratis ? ' · pasa el umbral' : '') + '</span>'
               : mxn(d.envio)) + '</td></tr>';
      });
      if (sinEnviar.length) {
        h += '<tr><td><strong>No viaja por paquetería</strong> · ' + sinEnviar.length +
             ' partidas</td><td class="hg-num">' + mxn(montoSin) +
             '</td><td class="hg-num">presencial</td></tr>';
      }
      h += '</tbody></table></div>';
    }

    var bloques = {};
    items.forEach(function (c) {
      var k = 'Fase ' + c.fase + ' · ' + (c.bloque || 'sin bloque');
      (bloques[k] = bloques[k] || []).push(c);
    });

    Object.keys(bloques).forEach(function (k) {
      h += '<h3 class="hg-bloque">' + esc(k) + '</h3>';
      h += '<div class="hg-lista">';
      bloques[k].forEach(function (c) {
        var e = estado.compras[c.id] || {};
        var no = !c.cuenta;
        h += '<div class="hg-item' + (e.comprado ? ' hg-ok' : '') + (no ? ' hg-nosuma' : '') + '">';
        h += '<label class="hg-check"><input type="checkbox" data-compra="' + c.id + '"' +
             (e.comprado ? ' checked' : '') + '><span></span></label>';
        h += '<div class="hg-cuerpo">';
        h += '<div class="hg-titulo">' + esc(c.nombre) +
             (no ? ' <span class="hg-tag">no suma: ' + esc(c.motivo) + '</span>' : '') +
             (c.temporada ? ' <span class="hg-tag hg-temp">' + esc(c.temporada) + '</span>' : '') + '</div>';
        var v = vigente(c);
        var forzado = modo === 'linea' && !enLinea(c);
        h += '<div class="hg-meta">' + c.cantidad + ' ' + esc(c.unidad) + ' · plan ' + mxn(v.subtotal) +
             ' · <span class="' + (v.fisica ? 'hg-fis' : 'hg-onl') + '">' + esc(v.donde) + '</span>' +
             (v.bloque ? ' <span class="hg-tag">' + esc(v.bloque) + '</span>' : '') +
             (forzado ? ' <span class="hg-tag hg-temp">no viaja: presencial</span>' : '') +
             (c.opciones.length > 1 ? ' · ' + (c.opciones.length - 1) + ' opción(es) más' : '') + '</div>';
        if (v.nota) h += '<div class="hg-nota">' + esc(v.nota) + '</div>';
        else if (c.notas) h += '<div class="hg-nota">' + esc(c.notas) + '</div>';
        h += '<div class="hg-campos">';
        h += '<label>Pagué <input type="number" step="0.01" placeholder="' + c.subtotal +
             '" data-real="' + c.id + '" value="' + esc(e.real === undefined ? '' : e.real) + '"></label>';
        h += '<label>Dónde <input type="text" placeholder="tienda o vendedor" data-donde="' + c.id +
             '" value="' + esc(e.donde || '') + '"></label>';
        h += '<label>Fecha <input type="date" data-fecha="' + c.id + '" value="' + esc(e.fecha || '') + '"></label>';
        h += '</div>';
        h += '</div></div>';
      });
      h += '</div>';
    });

    if (!items.length) h += '<p class="hg-vacio">Nada que mostrar con este filtro.</p>';
    return h;
  }

  function tarjeta(t, v, sub, clase) {
    return '<div class="hg-tarjeta' + (clase ? ' hg-' + clase : '') + '">' +
      '<div class="hg-t-lab">' + esc(t) + '</div>' +
      '<div class="hg-t-val">' + esc(v) + '</div>' +
      '<div class="hg-t-sub">' + esc(sub) + '</div></div>';
  }

  // -- render: gates --------------------------------------------------------
  function renderGates() {
    var h = '<p class="hg-intro">Los gates se escriben antes de gastar y no se renegocian: se cumplen, ' +
            'se itera o se para. Aquí solo registras el valor medido; el veredicto lo calcula la página.</p>';

    datos.gates.forEach(function (g) {
      var e = estado.gates[g.id] || {};
      var res = g.criterios.map(function (c) {
        return cumple(e[c.id], c.comparador, umbral(g.id, c.id, c.umbral));
      });
      var medidos = res.filter(function (r) { return r !== null; }).length;
      var pasan = res.filter(function (r) { return r === true; }).length;
      var veredicto = medidos === 0 ? 'sin datos'
        : (pasan === g.criterios.length ? 'PASA' : (medidos < g.criterios.length ? 'incompleto' : 'NO PASA'));
      var cls = veredicto === 'PASA' ? 'bien' : (veredicto === 'NO PASA' ? 'mal' : 'neutro');

      h += '<div class="hg-gate">';
      h += '<div class="hg-gate-cab"><h3>' + esc(g.nombre) + '</h3>' +
           '<span class="hg-veredicto hg-' + cls + '">' + veredicto + '</span></div>';
      h += '<div class="hg-gate-sub">' + esc(g.cuando) + ' · ' + esc(g.decision) + '</div>';
      if (g.aviso) h += '<div class="hg-aviso">' + esc(g.aviso) + '</div>';
      h += '<table class="hg-tabla"><thead><tr><th>Métrica</th><th>Umbral</th><th>Medido</th><th></th></tr></thead><tbody>';
      g.criterios.forEach(function (c, i) {
        var u = umbral(g.id, c.id, c.umbral);
        var r = res[i];
        h += '<tr>';
        h += '<td>' + esc(c.metrica) + '<div class="hg-fuente">' + esc(c.fuente) + '</div></td>';
        h += '<td class="hg-num">' + esc(c.comparador) + ' ' + esc(u) + ' ' + esc(c.unidad) +
             (u !== c.umbral ? ' <span class="hg-tag">editado, original ' + esc(c.umbral) + '</span>' : '') + '</td>';
        h += '<td><input type="number" step="any" data-gate="' + g.id + '" data-crit="' + c.id +
             '" value="' + esc(e[c.id] === undefined ? '' : e[c.id]) + '"></td>';
        h += '<td class="hg-num">' + (r === null ? '—' :
             (r ? '<span class="hg-bien">cumple</span>' : '<span class="hg-mal">no cumple</span>')) + '</td>';
        h += '</tr>';
      });
      h += '</tbody></table>';
      h += '<label class="hg-larga">Nota <textarea rows="2" data-gatenota="' + g.id + '">' +
           esc(e.nota || '') + '</textarea></label>';
      h += '</div>';
    });
    return h;
  }

  // -- render: validaciones -------------------------------------------------
  var ESTADOS = ['pendiente', 'en curso', 'pasó', 'falló'];

  function renderValidaciones() {
    var h = '<p class="hg-intro">Los métodos V1–V11 de la wiki. La regla dura del proyecto: ' +
            'no se siembra nada que no haya pasado V1, y no se agrega NFT sobre una base inestable.</p>';
    h += '<div class="hg-lista">';
    datos.validaciones.forEach(function (v) {
      var e = estado.validaciones[v.id] || {};
      var est = e.estado || 'pendiente';
      h += '<div class="hg-item hg-v-' + est.replace(/\s|ó/g, '') + '">';
      h += '<div class="hg-cuerpo">';
      h += '<div class="hg-titulo">' + esc(v.id) + ' · ' + esc(v.nombre) +
           ' <span class="hg-tag">Fase ' + v.fase + '</span></div>';
      h += '<div class="hg-nota">' + esc(v.nota) + '</div>';
      h += '<div class="hg-campos">';
      h += '<label>Estado <select data-val="' + v.id + '">' + ESTADOS.map(function (o) {
        return '<option' + (o === est ? ' selected' : '') + '>' + o + '</option>';
      }).join('') + '</select></label>';
      h += '<label>Fecha <input type="date" data-valfecha="' + v.id + '" value="' + esc(e.fecha || '') + '"></label>';
      h += '<label class="hg-ancha">Resultado <input type="text" data-valnota="' + v.id +
           '" placeholder="el número medido" value="' + esc(e.nota || '') + '"></label>';
      h += '</div></div></div>';
    });
    h += '</div>';
    return h;
  }

  // -- render: parametros (con candado) -------------------------------------
  function renderParametros() {
    var h = '';
    h += '<div class="hg-candado">';
    h += '<strong>Este apartado cambia los umbrales con los que se juzga el proyecto.</strong> ';
    h += 'Por eso pide contraseña. Conviene saber qué protege y qué no: la wiki es un sitio estático, ' +
         'así que el candado vive en el JavaScript que tu navegador ya descargó. Evita que muevas un ' +
         'umbral sin querer, o que lo mueva alguien a quien le enseñes el tablero. ' +
         '<strong>No es seguridad</strong>: quien sepa editar el código lo abre. Si algún día necesitas ' +
         'protección de verdad, eso pide un servidor.';
    h += '</div>';

    if (!desbloqueado) {
      h += '<form class="hg-login" id="hg-login">';
      h += '<label>Contraseña <input type="password" id="hg-pass" autocomplete="current-password"></label>';
      h += '<button type="submit" class="hg-btn">Desbloquear</button>';
      h += '<span id="hg-passmsg"></span>';
      h += '</form>';
      h += '<p class="hg-intro">Mientras tanto, así están los parámetros:</p>';
    }

    h += '<h3 class="hg-bloque">Parámetros económicos</h3>';
    h += '<table class="hg-tabla"><thead><tr><th>Parámetro</th><th>Valor</th><th>De dónde sale</th></tr></thead><tbody>';
    datos.parametros.forEach(function (p) {
      var v = estado.parametros[p.id] !== undefined ? estado.parametros[p.id] : p.valor;
      h += '<tr><td>' + esc(p.nombre) + '</td>';
      h += '<td class="hg-num">' + (desbloqueado
        ? '<input type="number" step="any" data-param="' + p.id + '" value="' + esc(v) + '"> ' + esc(p.unidad)
        : '<strong>' + esc(v) + '</strong> ' + esc(p.unidad)) +
        (v !== p.valor ? ' <span class="hg-tag">editado, original ' + esc(p.valor) + '</span>' : '') + '</td>';
      h += '<td class="hg-fuente">' + esc(p.fuente) + '</td></tr>';
    });
    h += '</tbody></table>';

    h += '<h3 class="hg-bloque">Umbrales de los gates</h3>';
    h += '<p class="hg-intro">Cambiar un umbral aquí <em>no</em> cambia el de la wiki: sirve para simular. ' +
         'La regla del proyecto es que un gate no alcanzado se itera o se detiene, no se rebaja.</p>';
    h += '<table class="hg-tabla"><thead><tr><th>Gate</th><th>Métrica</th><th>Umbral</th></tr></thead><tbody>';
    datos.gates.forEach(function (g) {
      g.criterios.forEach(function (c) {
        var u = umbral(g.id, c.id, c.umbral);
        h += '<tr><td>' + esc(g.id) + '</td><td>' + esc(c.metrica) + '</td>';
        h += '<td class="hg-num">' + esc(c.comparador) + ' ' + (desbloqueado
          ? '<input type="number" step="any" data-umbral="' + g.id + '.' + c.id + '" value="' + esc(u) + '">'
          : '<strong>' + esc(u) + '</strong>') + ' ' + esc(c.unidad) +
          (u !== c.umbral ? ' <span class="hg-tag">original ' + esc(c.umbral) + '</span>' : '') + '</td></tr>';
      });
    });
    h += '</tbody></table>';

    if (desbloqueado) {
      h += '<button class="hg-btn hg-btn-sec" id="hg-restaurar">Restaurar todos los valores de la wiki</button>';
    }
    return h;
  }

  // -- exportar / importar --------------------------------------------------
  function exportarJSON() {
    descargar('homegreen-seguimiento.json', JSON.stringify(estado, null, 1), 'application/json');
  }

  function exportarCSV() {
    var filas = [['partida_id', 'fase', 'bloque', 'partida', 'cantidad', 'unidad', 'modo',
                  'precio_plan_mxn', 'subtotal_plan_mxn', 'proveedor_plan', 'comprado',
                  'pagado_mxn', 'donde', 'fecha']];
    datos.compras.forEach(function (c) {
      var e = estado.compras[c.id] || {};
      var v = vigente(c);
      filas.push([c.id, c.fase, c.bloque, c.nombre, c.cantidad, c.unidad, modo,
                  v.precio, v.subtotal, v.donde, e.comprado ? 'si' : 'no',
                  e.real === undefined ? '' : e.real, e.donde || '', e.fecha || '']);
    });
    var csv = filas.map(function (f) {
      return f.map(function (v) {
        var s = String(v === undefined || v === null ? '' : v);
        return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
      }).join(',');
    }).join('\n');
    descargar('homegreen-compras.csv', csv, 'text/csv;charset=utf-8');
  }

  function descargar(nombre, contenido, tipo) {
    var a = document.createElement('a');
    var url = URL.createObjectURL(new Blob([contenido], { type: tipo }));
    a.href = url; a.download = nombre;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function importar(archivo) {
    var fr = new FileReader();
    fr.onload = function () {
      try {
        var d = JSON.parse(fr.result);
        if (!d || typeof d !== 'object') throw new Error('formato');
        var v = vacio();
        Object.keys(v).forEach(function (k) { if (d[k] === undefined) d[k] = v[k]; });
        estado = d; guardar(); render();
      } catch (e) {
        window.alert('Ese archivo no es un respaldo válido del tablero.');
      }
    };
    fr.readAsText(archivo);
  }

  // -- armado y eventos -----------------------------------------------------
  function render() {
    var c = el('hg-contenido');
    if (!c) return;
    if (pestana === 'compras') c.innerHTML = renderCompras();
    else if (pestana === 'gates') c.innerHTML = renderGates();
    else if (pestana === 'validaciones') c.innerHTML = renderValidaciones();
    else c.innerHTML = renderParametros();

    Array.prototype.forEach.call(document.querySelectorAll('[data-tab]'), function (b) {
      b.className = 'hg-tab' + (b.getAttribute('data-tab') === pestana ? ' hg-tab-on' : '');
    });
    var filtros = el('hg-filtros');
    if (filtros) filtros.style.display = pestana === 'compras' ? '' : 'none';
  }

  function conjunto(obj, id, campo, valor) {
    obj[id] = obj[id] || {};
    obj[id][campo] = valor;
  }

  function enlazar(raiz) {
    raiz.addEventListener('change', function (ev) {
      var t = ev.target, a;
      if ((a = t.getAttribute('data-compra'))) { conjunto(estado.compras, a, 'comprado', t.checked); guardar(); render(); return; }
      if ((a = t.getAttribute('data-real'))) { conjunto(estado.compras, a, 'real', t.value); guardar(); render(); return; }
      if ((a = t.getAttribute('data-donde'))) { conjunto(estado.compras, a, 'donde', t.value); guardar(); return; }
      if ((a = t.getAttribute('data-fecha'))) { conjunto(estado.compras, a, 'fecha', t.value); guardar(); return; }
      if ((a = t.getAttribute('data-gate'))) {
        conjunto(estado.gates, a, t.getAttribute('data-crit'), t.value); guardar(); render(); return;
      }
      if ((a = t.getAttribute('data-gatenota'))) { conjunto(estado.gates, a, 'nota', t.value); guardar(); return; }
      if ((a = t.getAttribute('data-val'))) { conjunto(estado.validaciones, a, 'estado', t.value); guardar(); render(); return; }
      if ((a = t.getAttribute('data-valfecha'))) { conjunto(estado.validaciones, a, 'fecha', t.value); guardar(); return; }
      if ((a = t.getAttribute('data-valnota'))) { conjunto(estado.validaciones, a, 'nota', t.value); guardar(); return; }
      if ((a = t.getAttribute('data-param'))) { estado.parametros[a] = Number(t.value); guardar(); render(); return; }
      if ((a = t.getAttribute('data-umbral'))) { estado.umbrales[a] = Number(t.value); guardar(); render(); return; }
    });

    raiz.addEventListener('click', function (ev) {
      var t = ev.target.closest ? ev.target.closest('[data-tab],#hg-restaurar') : null;
      if (!t) return;
      if (t.id === 'hg-restaurar') {
        if (window.confirm('¿Restaurar todos los parámetros y umbrales a los valores de la wiki? ' +
                           'Tu avance de compras, gates y validaciones no se toca.')) {
          estado.parametros = {}; estado.umbrales = {}; guardar(); render();
        }
        return;
      }
      pestana = t.getAttribute('data-tab');
      render();
    });

    raiz.addEventListener('submit', async function (ev) {
      if (ev.target.id !== 'hg-login') return;
      ev.preventDefault();
      var msg = el('hg-passmsg');
      var h = await sha256(el('hg-pass').value);
      if (h === HASH) { desbloqueado = true; render(); }
      else { msg.textContent = 'Contraseña incorrecta.'; msg.className = 'hg-mal'; }
    });
  }

  // -- arranque -------------------------------------------------------------
  function iniciar() {
    var raiz = el('hg-seguimiento');
    if (!raiz) return;

    // La pagina puede vivir en cualquier profundidad del sitio; se resuelve la
    // ruta del JSON contra la raiz que Material publica en el <body>.
    var base = document.body.getAttribute('data-md-base') || '';
    var url = base ? base.replace(/\/?$/, '/') + DATOS_URL : '../' + DATOS_URL;

    fetch(url).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (d) {
      datos = d;
      raiz.innerHTML =
        '<div class="hg-tabs">' +
          '<button class="hg-tab hg-tab-on" data-tab="compras">Compras</button>' +
          '<button class="hg-tab" data-tab="gates">Gates</button>' +
          '<button class="hg-tab" data-tab="validaciones">Validaciones</button>' +
          '<button class="hg-tab" data-tab="parametros">Parámetros</button>' +
        '</div>' +
        '<div class="hg-barra-sup">' +
          '<div id="hg-filtros">' +
            '<label>Fase <select id="hg-fase">' +
              '<option value="todas">todas</option><option value="0">Fase 0</option>' +
              '<option value="1">Fase 1</option><option value="2">Fase 2</option></select></label>' +
            '<label class="hg-inline"><input type="checkbox" id="hg-pend"> solo lo que falta</label>' +
            '<label>Cómo compro <select id="hg-modo">' +
              '<option value="presencial">en persona</option>' +
              '<option value="linea">en línea</option></select></label>' +
          '</div>' +
          '<div class="hg-acciones">' +
            '<button class="hg-btn hg-btn-sec" id="hg-exp-json">Exportar respaldo</button>' +
            '<button class="hg-btn hg-btn-sec" id="hg-exp-csv">Compras a CSV</button>' +
            '<label class="hg-btn hg-btn-sec">Importar<input type="file" accept="application/json" id="hg-imp" hidden></label>' +
          '</div>' +
        '</div>' +
        '<div id="hg-guardado" class="hg-guardado"></div>' +
        '<div id="hg-contenido"></div>';

      enlazar(raiz);
      el('hg-fase').addEventListener('change', function () { filtroFase = this.value; render(); });
      el('hg-pend').addEventListener('change', function () { soloPendientes = this.checked; render(); });
      el('hg-modo').addEventListener('change', function () { modo = this.value; render(); });
      el('hg-exp-json').addEventListener('click', exportarJSON);
      el('hg-exp-csv').addEventListener('click', exportarCSV);
      el('hg-imp').addEventListener('change', function () { if (this.files[0]) importar(this.files[0]); });

      render();
      if (estado.actualizado) {
        var f = new Date(estado.actualizado);
        el('hg-guardado').textContent = 'Último cambio guardado en este navegador · ' +
          f.toLocaleDateString('es-MX') + ' ' + f.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
      } else {
        el('hg-guardado').textContent = 'Todavía no hay nada guardado en este navegador.';
      }
    }).catch(function () {
      raiz.innerHTML = '<div class="hg-aviso">No se pudieron cargar los datos del tablero (' +
        esc(url) + '). Si estás viendo la wiki en local, corre <code>mkdocs serve</code> ' +
        'en vez de abrir el HTML directo del disco.</div>';
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();

  // Material con navigation.instant cambia de pagina sin recargar: hay que
  // volver a montar el tablero cuando el usuario navega hasta el.
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(function () { desbloqueado = false; iniciar(); });
  }
})();
