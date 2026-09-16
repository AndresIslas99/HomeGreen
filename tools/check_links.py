#!/usr/bin/env python3
"""Verifica los enlaces http(s) de la wiki: ``docs/**/*.md`` y ``README.md``.

Extrae las URL con una expresión regular, las deduplica y las verifica con ``urllib``
(HEAD y, si falla, GET) con User-Agent de navegador, timeout de 15 s y 2 reintentos, en
paralelo con ``ThreadPoolExecutor(8)``. Clasifica cada una como:

* ``ok``        2xx en la URL original.
* ``redirect``  2xx tras una o más redirecciones (la URL final se anota).
* ``blocked``   401 / 403 / 429 / 503, otros 5xx, error TLS, timeout, conexión rechazada
                (geobloqueo o anti-bot: no prueban que la página no exista) o dominio
                "dinámico" que no se verifica (buscadores y listados como
                ``listado.mercadolibre.com.mx``).
* ``dead``      404 / 410, DNS inexistente, video de YouTube que la API oEmbed reporta
                inexistente o privado, o una ruta de este repositorio que no existe.

Los videos de YouTube se verifican con la API **oEmbed** (``/oembed?url=...&format=json``),
que contesta 200 con el título si el video existe y es incrustable: es determinista, a
diferencia de buscar "Video unavailable" en el HTML, que da falsos positivos cuando YouTube
devuelve una página de consentimiento.

Las URL de este repositorio (``github.com/AndresIslas99/HomeGreen/blob|tree/...``) **no se
consultan por HTTP**: se verifican contra el árbol de trabajo local, así funcionan con el
repositorio privado y además detectan rutas mal escritas en la wiki.

Imprime una tabla Markdown y un resumen; **el código de salida es 1 solo si hay ``dead``**.

Uso::

    python3 tools/check_links.py                 # toda la wiki
    python3 tools/check_links.py --only-dead     # solo los muertos
    python3 tools/check_links.py --salida enlaces.md --hilos 8 --timeout 15
    python3 tools/check_links.py --listar        # solo extrae, no toca la red

Los enlaces de ``tools/enlaces-muertos-conocidos.txt`` se reportan como ``dead (conocido)``
pero no cambian el código de salida: solo un ``dead`` **nuevo** rompe el workflow.

Solo biblioteca estándar (Python 3.11). Respeta ``HTTPS_PROXY`` y ``SSL_CERT_FILE`` del entorno.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

RE_URL = re.compile(r"https?://[^\s<>\"'`\]\[{}|\\^]+")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
CABECERAS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
             "Accept-Language": "es-MX,es;q=0.9,en;q=0.8"}
PUNTUACION_FINAL = ".,;:!?)]}>'\"*_~"

#: Dominios o prefijos de búsqueda/listado muy dinámicos (o que bloquean bots siempre):
#: no se verifican; se marcan ``blocked`` con nota.
DOMINIOS_DINAMICOS = (
    "listado.mercadolibre.com.mx", "google.com/search", "google.com.mx/search", "youtube.com/results",
    "duckduckgo.com", "bing.com/search", "facebook.com", "instagram.com", "twitter.com", "x.com/",
    "linkedin.com", "wa.me", "api.whatsapp.com",
)
#: URL que no son enlaces reales (namespaces, placeholders, hosts locales).
IGNORAR = ("localhost", "127.0.0.1", "0.0.0.0", "example.com", ".local:", ".local/",
           "homeassistant.local", "nodo-riego-v1.local", "nodo-nft-v2.local", "nodo-ambiente.local",
           "www.w3.org/2000/svg",
           "www.w3.org/1999/xlink", "www.w3.org/1999/xhtml", "schemas.openxmlformats", "purl.org/dc")
PLACEHOLDERS = ("<", ">", "AAAA", "XXXX", "…", "{", "}")
ORDEN_ESTADO = {"dead": 0, "blocked": 1, "redirect": 2, "ok": 3}

#: Lista de enlaces que ya se sabe que están muertos y que ya están anotados como tales en
#: la página que los cita (ver el encabezado del archivo). Se siguen reportando, pero no
#: rompen el workflow: así un ``dead`` nuevo no se pierde entre el ruido viejo.
ARCHIVO_CONOCIDOS = Path(__file__).resolve().parent / "enlaces-muertos-conocidos.txt"


def cargar_conocidos(ruta: Path = ARCHIVO_CONOCIDOS) -> set[str]:
    if not ruta.exists():
        return set()
    return {li.strip() for li in ruta.read_text(encoding="utf-8").splitlines()
            if li.strip() and not li.lstrip().startswith("#")}

#: Un timeout o un "connection reset" desde un contenedor no prueban que la página no exista:
#: muchos sitios de gobierno de CDMX y algunas tiendas cortan la conexión a IP de centro de
#: datos o fuera de México. Se reportan como ``blocked`` para revisarlos a mano, no como
#: ``dead`` (que rompe el workflow).
TIMEOUT_NOTA = "timeout {t:.0f} s: no responde desde aquí; ábrelo en el navegador antes de darlo por muerto"
CONN_NOTA = "suele ser geobloqueo o filtro anti-bot, no un enlace roto: verifícalo a mano"

#: Repositorio y sitio de este proyecto. Los ``blob/`` y ``tree/`` se verifican **contra el
#: árbol local** (funciona con el repo privado y además detecta rutas mal escritas); el sitio
#: de Pages responde 404 hasta que se habilita Settings -> Pages -> Source: GitHub Actions.
REPO_PROPIO = "github.com/AndresIslas99/HomeGreen"
SITIO_PROPIO = "andresislas99.github.io/HomeGreen"
RE_REPO_RUTA = re.compile(r"github\.com/AndresIslas99/HomeGreen/(?:blob|tree|raw)/[^/]+/(.+?)/?$", re.I)


# ---------------------------------------------------------------------------
# Extracción
# ---------------------------------------------------------------------------

def limpiar_url(url: str) -> str:
    url = url.replace("&amp;", "&")
    while url and url[-1] in PUNTUACION_FINAL:
        if url[-1] == ")" and url.count("(") >= url.count(")"):
            break  # paréntesis balanceado (p. ej. Wikipedia)
        url = url[:-1]
    return url


def extraer_urls(texto: str) -> list[str]:
    out = []
    for m in RE_URL.finditer(texto):
        url = limpiar_url(m.group(0))
        siguiente = texto[m.end(): m.end() + 1]
        if siguiente == "<" or any(p in url for p in PLACEHOLDERS):
            continue  # https://www.youtube.com/embed/<ID>, plantillas
        if url.rstrip("/").endswith(("/embed", "/watch?v=", "/watch")):
            continue
        if len(url) < 12 or "." not in url.split("//", 1)[-1]:
            continue
        out.append(url)
    return out


#: El reporte que genera este mismo script: escanearlo duplicaría cada URL y ensuciaría la
#: columna "Dónde" con la página que solo las está listando.
AUTOGENERADOS = ("docs/referencia/enlaces.md",)


def archivos_fuente(raiz: Path, extras: list[str] | None) -> list[Path]:
    rutas = sorted((raiz / "docs").rglob("*.md")) if (raiz / "docs").exists() else []
    rutas = [r for r in rutas if r.relative_to(raiz).as_posix() not in AUTOGENERADOS]
    if (raiz / "README.md").exists():
        rutas.append(raiz / "README.md")
    for patron in extras or []:
        rutas += sorted(raiz.glob(patron))
    vistos, out = set(), []
    for r in rutas:
        if r.resolve() not in vistos:
            vistos.add(r.resolve())
            out.append(r)
    return out


def recolectar(raiz: Path, extras: list[str] | None) -> dict[str, list[str]]:
    """{url: [archivos relativos donde aparece]}"""
    donde: dict[str, list[str]] = defaultdict(list)
    for ruta in archivos_fuente(raiz, extras):
        try:
            texto = ruta.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(ruta.relative_to(raiz))
        for url in extraer_urls(texto):
            if rel not in donde[url]:
                donde[url].append(rel)
    return dict(donde)


# ---------------------------------------------------------------------------
# Verificación
# ---------------------------------------------------------------------------

def es_dinamico(url: str, extra: tuple[str, ...] = ()) -> bool:
    u = url.lower()
    return any(d in u for d in DOMINIOS_DINAMICOS + extra)


def es_ignorable(url: str) -> bool:
    u = url.lower()
    return any(i in u for i in IGNORAR)


RE_YT_ID = re.compile(r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})")


RE_YT_LISTA = re.compile(r"[?&]list=([A-Za-z0-9_-]{10,})")


def es_youtube(url: str) -> bool:
    u = url.lower()
    return "youtube.com/watch" in u or "youtu.be/" in u or "youtube.com/embed/" in u or "youtube.com/playlist" in u


def id_youtube(url: str) -> str | None:
    """ID de un video de 11 caracteres, o ``None`` si la URL es de playlist o de canal.

    Ojo con ``/embed/videoseries?list=...``: "videoseries" mide exactamente 11 caracteres y
    el regex de ID lo casaría; una playlist se resuelve por ``list=``, nunca por ID.
    """
    if RE_YT_LISTA.search(url) or "/playlist" in url.lower():
        return None
    m = RE_YT_ID.search(url)
    if m and m.group(1).lower() != "videoseries":
        return m.group(1)
    return None


def verificar_youtube(url: str, timeout: float = 15.0) -> dict | None:
    """Verifica un video o una playlist de YouTube con la API oEmbed, no leyendo el HTML.

    ``https://www.youtube.com/oembed?url=...&format=json`` contesta 200 con el título si el
    video existe y es incrustable, y 401/403/404 si no. Es determinista: la heurística de
    buscar "Video unavailable" en el HTML da falsos positivos cuando YouTube devuelve una
    página de consentimiento o un interstitial, y un video bueno se marcaba muerto un día sí
    y otro no. Devuelve ``None`` si la URL no es un video (el llamador sigue por HTTP).
    """
    vid = id_youtube(url)
    lista = RE_YT_LISTA.search(url)
    if vid is not None:
        destino = f"https://www.youtube.com/watch?v={vid}"
        que = "video"
    elif lista is not None:
        destino = f"https://www.youtube.com/playlist?list={lista.group(1)}"
        que = "playlist"
    else:
        return None  # canal, /results, /user: se verifica por HTTP normal
    api = f"https://www.youtube.com/oembed?url={destino}&format=json"
    base = {"url": url, "final": url, "ms": 0}
    try:
        req = urllib.request.Request(api, headers=CABECERAS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            cuerpo = resp.read(8000).decode("utf-8", errors="replace")
        try:
            datos = json.loads(cuerpo)
            titulo = str(datos.get("title", ""))[:60]
            autor = str(datos.get("author_name", ""))[:40]
        except (ValueError, AttributeError):
            titulo = autor = ""
        # El canal se reporta a propósito: así se detecta un video bien vivo pero atribuido
        # al autor equivocado, que es tan engañoso como un enlace roto.
        desc = " · ".join(x for x in (titulo, autor) if x)
        return {**base, "estado": "ok", "codigo": "oembed",
                "nota": f"{que} disponible: {desc}" if desc else f"{que} disponible (oEmbed)"}
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return {**base, "estado": "blocked", "codigo": str(e.code),
                    "nota": f"el {que} existe pero no permite incrustarse: enlázalo en vez de usar <iframe>"}
        if e.code in (404, 400):
            return {**base, "estado": "dead", "codigo": str(e.code),
                    "nota": f"YouTube: el {que} no existe, es privado o fue retirado (oEmbed)"}
        return {**base, "estado": "blocked", "codigo": str(e.code), "nota": f"oEmbed HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001 — sin prueba de muerte, no se marca muerto
        return {**base, "estado": "blocked", "codigo": "oembed",
                "nota": f"oEmbed no respondió ({type(e).__name__}): verifícalo a mano"}


def _clasificar_http(codigo: int) -> tuple[str, str]:
    if 200 <= codigo < 300:
        return "ok", ""
    if codigo in (404, 410):
        return "dead", f"HTTP {codigo}"
    if codigo in (401, 403, 429, 503):
        return "blocked", f"HTTP {codigo}"
    if codigo >= 500:
        return "blocked", f"HTTP {codigo} (error del servidor, transitorio)"
    return "blocked", f"HTTP {codigo}"


def verificar_propio(url: str, raiz: Path) -> dict | None:
    """Verifica una URL de este repositorio contra el árbol de trabajo local.

    Devuelve ``None`` si la URL no es del proyecto. Un ``blob/`` o ``tree/`` cuya ruta no
    existe en el repositorio es ``dead`` de verdad (referencia rota en la wiki); si existe,
    es ``ok`` aunque GitHub conteste 404 por ser un repositorio privado.
    """
    if SITIO_PROPIO in url:
        return {"url": url, "estado": "blocked", "codigo": "propio", "final": url, "ms": 0,
                "nota": "sitio del proyecto: 404 hasta habilitar Settings → Pages → Source: GitHub Actions"}
    if REPO_PROPIO not in url:
        return None
    m = RE_REPO_RUTA.search(url)
    if not m:
        return {"url": url, "estado": "blocked", "codigo": "propio", "final": url, "ms": 0,
                "nota": "repositorio del proyecto: GitHub contesta 404 mientras sea privado"}
    ruta = raiz / m.group(1)
    if ruta.exists():
        return {"url": url, "estado": "ok", "codigo": "local", "final": url, "ms": 0,
                "nota": f"verificado contra el árbol local: {m.group(1)} existe"}
    return {"url": url, "estado": "dead", "codigo": "local", "final": url, "ms": 0,
            "nota": f"ruta inexistente en el repositorio: {m.group(1)}"}


def verificar(url: str, timeout: float = 15.0, reintentos: int = 2, dinamicos: tuple[str, ...] = (),
              raiz: Path | None = None) -> dict:
    """Devuelve {estado, codigo, final, nota, ms}."""
    t0 = time.monotonic()
    res = {"url": url, "estado": "dead", "codigo": "", "final": url, "nota": ""}
    if raiz is not None:
        propio = verificar_propio(url, raiz)
        if propio is not None:
            return propio
    if es_youtube(url):
        yt = verificar_youtube(url, timeout)
        if yt is not None:
            yt["ms"] = int((time.monotonic() - t0) * 1000)
            return yt
    if es_dinamico(url, dinamicos):
        res.update(estado="blocked", nota="dominio dinámico: no verificado")
        return res
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    metodos = ("HEAD", "GET")
    ultimo: dict | None = None
    for intento in range(reintentos + 1):
        reintentar = False
        for metodo in metodos:
            req = urllib.request.Request(url, method=metodo, headers=CABECERAS)
            try:
                with opener.open(req, timeout=timeout) as resp:
                    codigo = resp.status
                    final = resp.geturl()
                    nota = ""
                    estado = "redirect" if final.rstrip("/") != url.rstrip("/") else "ok"
                    if estado == "redirect":
                        nota = f"→ {final}"
                    res.update(estado=estado, codigo=str(codigo), final=final, nota=nota)
                    res["ms"] = int((time.monotonic() - t0) * 1000)
                    return res
            except urllib.error.HTTPError as e:
                estado, nota = _clasificar_http(e.code)
                ultimo = {"estado": estado, "codigo": str(e.code), "nota": nota + (f" ({metodo})" if metodo == "GET" else "")}
                if metodo == "HEAD":
                    continue  # muchos servidores rechazan HEAD; probar GET
                if estado == "blocked" and e.code >= 500:
                    reintentar = True
                break
            except urllib.error.URLError as e:
                razon = e.reason
                if isinstance(razon, ssl.SSLError) or "CERTIFICATE" in str(razon).upper() or "SSL" in str(razon).upper():
                    ultimo = {"estado": "blocked", "codigo": "TLS", "nota": f"TLS: {str(razon)[:80]}"}
                    break
                if isinstance(razon, socket.gaierror) or "Name or service not known" in str(razon) or "nodename" in str(razon) or "getaddrinfo" in str(razon):
                    ultimo = {"estado": "dead", "codigo": "DNS", "nota": "DNS: dominio no resuelve"}
                    break
                if isinstance(razon, (socket.timeout, TimeoutError)) or "timed out" in str(razon):
                    ultimo = {"estado": "blocked", "codigo": "timeout", "nota": TIMEOUT_NOTA.format(t=timeout)}
                    reintentar = True
                    break
                ultimo = {"estado": "blocked", "codigo": "conn", "nota": f"conexión rechazada ({str(razon)[:60]}); {CONN_NOTA}"}
                reintentar = True
                break
            except (socket.timeout, TimeoutError):
                ultimo = {"estado": "blocked", "codigo": "timeout", "nota": TIMEOUT_NOTA.format(t=timeout)}
                reintentar = True
                break
            except ssl.SSLError as e:
                ultimo = {"estado": "blocked", "codigo": "TLS", "nota": f"TLS: {str(e)[:80]}"}
                break
            except (ConnectionError, OSError) as e:
                ultimo = {"estado": "blocked", "codigo": "conn", "nota": f"conexión rechazada ({str(e)[:60]}); {CONN_NOTA}"}
                reintentar = True
                break
            except Exception as e:  # noqa: BLE001 — desconocido: no marcar muerto sin pruebas
                ultimo = {"estado": "blocked", "codigo": "err", "nota": f"error: {type(e).__name__}: {str(e)[:60]}"}
                break
        if not reintentar or intento == reintentos:
            break
        time.sleep(1.5 * (intento + 1))
    if ultimo:
        res.update(ultimo)
    res["ms"] = int((time.monotonic() - t0) * 1000)
    return res


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------

def _md(s: str) -> str:
    return s.replace("|", "\\|")


def tabla_markdown(resultados: list[dict], donde: dict[str, list[str]], solo_dead: bool = False) -> str:
    filas = sorted(resultados, key=lambda r: (ORDEN_ESTADO.get(r["estado"], 9), r["url"]))
    if solo_dead:
        filas = [r for r in filas if r["estado"] == "dead"]
    lineas = ["| Estado | HTTP | URL | Dónde | Nota |", "|---|---|---|---|---|"]
    for r in filas:
        archivos = donde.get(r["url"], [])
        d = ", ".join(archivos[:3]) + (f" (+{len(archivos) - 3})" if len(archivos) > 3 else "")
        est = r["estado"] + (" (conocido)" if r.get("conocido") else "")
        lineas.append(f"| {est} | {r['codigo']} | {_md(r['url'])} | {_md(d)} | {_md(r['nota'])} |")
    if len(lineas) == 2:
        lineas.append("| — | — | (ninguno) | | |")
    return "\n".join(lineas) + "\n"


def resumen(resultados: list[dict], n_archivos: int, segundos: float) -> str:
    c = defaultdict(int)
    for r in resultados:
        c[r["estado"]] += 1
    conocidos = sum(1 for r in resultados if r.get("conocido"))
    nuevos = c["dead"] - conocidos
    return (f"\n**Resumen:** {len(resultados)} URL únicas en {n_archivos} archivos · "
            f"ok {c['ok']} · redirect {c['redirect']} · blocked {c['blocked']} · "
            f"**dead {c['dead']}** ({conocidos} ya conocidos y anotados, **{nuevos} nuevos**) · "
            f"{segundos:.0f} s.\n\nSalida 1 solo si hay algún **dead nuevo**; los conocidos están en "
            f"`tools/enlaces-muertos-conocidos.txt`. Los `blocked` se revisan a mano: un 403, un "
            f"timeout o una conexión cortada suelen ser anti-bot o geobloqueo, no un enlace roto.\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Verifica los enlaces http(s) de docs/**/*.md y README.md; tabla Markdown; salida 1 solo si hay enlaces muertos.",
        epilog="Estados: ok · redirect · blocked (401/403/429/503, 5xx, TLS, dominios dinámicos) · dead (404/410, DNS, timeout).",
    )
    p.add_argument("--raiz", default=str(Path(__file__).resolve().parent.parent), help="raíz del repositorio (default: la carpeta padre de tools/)")
    p.add_argument("--incluir", action="append", metavar="GLOB", help="archivos extra relativos a la raíz (p. ej. 'bom/*.csv')")
    p.add_argument("--only-dead", action="store_true", help="imprime solo los enlaces muertos")
    p.add_argument("--salida", metavar="ARCHIVO.md", help="escribe el reporte Markdown completo en este archivo")
    p.add_argument("--listar", action="store_true", help="solo extrae y lista las URL; no toca la red")
    p.add_argument("--max", type=int, default=0, help="verifica solo las primeras N URL (para probar)")
    p.add_argument("--timeout", type=float, default=15.0)
    p.add_argument("--reintentos", type=int, default=2)
    p.add_argument("--hilos", type=int, default=8)
    p.add_argument("--dinamico", action="append", metavar="DOMINIO", help="dominio extra a tratar como dinámico (blocked sin verificar)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    raiz = Path(args.raiz).resolve()
    donde = recolectar(raiz, args.incluir)
    n_archivos = len(archivos_fuente(raiz, args.incluir))
    urls = sorted(u for u in donde if not es_ignorable(u))
    if args.max:
        urls = urls[: args.max]
    if args.listar:
        for u in urls:
            print(f"{u}\t{', '.join(donde[u][:3])}")
        print(f"\n{len(urls)} URL únicas en {n_archivos} archivos (sin verificar).", file=sys.stderr)
        return 0
    dinamicos = tuple(args.dinamico or ())
    t0 = time.monotonic()
    resultados: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.hilos) as ex:
        futuros = {ex.submit(verificar, u, args.timeout, args.reintentos, dinamicos, raiz): u for u in urls}
        for i, fut in enumerate(concurrent.futures.as_completed(futuros), 1):
            resultados.append(fut.result())
            print(f"\r{i}/{len(urls)} verificadas", end="", file=sys.stderr, flush=True)
    print("", file=sys.stderr)
    conocidos = cargar_conocidos()
    for r in resultados:
        r["conocido"] = r["estado"] == "dead" and r["url"] in conocidos
        if r["conocido"]:
            r["nota"] = (r["nota"] + "; " if r["nota"] else "") + "ya anotado en la página que lo cita"
    seg = time.monotonic() - t0
    reporte = f"# Enlaces de la wiki — {time.strftime('%Y-%m-%d')}\n\n" + tabla_markdown(resultados, donde) + resumen(resultados, n_archivos, seg)
    print(tabla_markdown(resultados, donde, solo_dead=args.only_dead) + resumen(resultados, n_archivos, seg))
    if args.salida:
        Path(args.salida).write_text(reporte, encoding="utf-8")
        print(f"(reporte completo en {args.salida})")
    nuevos = [r for r in resultados if r["estado"] == "dead" and not r.get("conocido")]
    if nuevos:
        print(f"\nERROR: {len(nuevos)} enlace(s) muerto(s) NUEVO(s). Corrige la página que los cita "
              f"(busca la alternativa y anota el precio con su fecha) o, si es un informe histórico "
              f"ya anotado, agrégalos a tools/enlaces-muertos-conocidos.txt:", file=sys.stderr)
        for r in nuevos:
            print(f"  {r['codigo']:>8}  {r['url']}", file=sys.stderr)
    return 1 if nuevos else 0


if __name__ == "__main__":
    sys.exit(main())
