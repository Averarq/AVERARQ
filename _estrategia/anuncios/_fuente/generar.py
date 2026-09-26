# -*- coding: utf-8 -*-
"""
generar.py — Piezas gráficas de Meta Ads de AVERARQ.

Cada anuncio es un HTML con la identidad de la marca (naranjo #FC4C02,
Barlow / Barlow Condensed, isotipo). Este script escribe los HTML en
_fuente/html/ y luego render.mjs los convierte a JPG en ../piezas/.

Uso:
    python3 generar.py            # escribe los HTML
    node render.mjs               # genera los JPG (requiere Playwright)

Para editar un texto: cambiar el anuncio en la lista ANUNCIOS y volver a correr ambos pasos.
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "html")

NARANJO = "#FC4C02"
OSCURO = "#111110"
CLARO = "#F2F0EB"

# Formatos Meta
FEED = (1080, 1350)   # 4:5 feed Facebook / Instagram
STORY = (1080, 1920)  # 9:16 historias y reels
CUAD = (1080, 1080)   # 1:1 carrusel

ISOTIPO = (
    '<svg class="iso" viewBox="41.6 33.0 21.9 25.4" xmlns="http://www.w3.org/2000/svg">'
    '<path fill="currentColor" d="M 57.574219 52.507812 L 46.25 52.507812 L 51.9375 38.394531 '
    'L 53.53125 42.492188 L 56.828125 42.492188 L 53.164062 33.398438 L 50.796875 33.398438 '
    'L 41.816406 55.308594 L 45.125 55.304688 L 58.695312 55.304688 L 59.8125 58.101562 '
    'L 63.183594 58.101562 L 60.898438 52.464844 Z"/></svg>'
)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;overflow:hidden}
body{font-family:'Barlow',sans-serif;color:__OSCURO__;background:__CLARO__;position:relative;-webkit-font-smoothing:antialiased}
.d{font-family:'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.01em}
.o{color:__NARANJO__}
.abs{position:absolute}
.img{position:absolute;background-size:cover;background-position:center}
.iso{width:1em;height:1.16em;display:inline-block;vertical-align:middle}
/* marca */
.brand{display:flex;align-items:center;gap:18px}
.brand .iso{font-size:54px;color:__NARANJO__}
.brand img{height:40px}
.brand.neg img{filter:brightness(0)}
.brand.blanco .iso{color:#fff}
.firma{font-size:26px;letter-spacing:.04em;opacity:.8}
/* chip */
.chip{display:inline-block;background:__NARANJO__;color:#fff;font-family:'Barlow Condensed';font-weight:600;
      font-size:30px;letter-spacing:.12em;text-transform:uppercase;padding:10px 22px 8px}
.chip.line{background:none;color:__NARANJO__;border:3px solid __NARANJO__}
/* titulares */
.h1{font-family:'Barlow Condensed';font-weight:700;text-transform:uppercase;line-height:.92;letter-spacing:-.005em}
.h2{font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;line-height:1}
.p{font-size:38px;line-height:1.3}
.small{font-size:26px;letter-spacing:.03em}
.lbl{position:absolute;background:rgba(17,17,16,.78);color:#fff;font-size:24px;letter-spacing:.05em;padding:10px 18px}
.rule{height:8px;width:120px;background:__NARANJO__}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,17,16,.0) 35%,rgba(17,17,16,.88) 100%)}
.shade-full{position:absolute;inset:0;background:rgba(17,17,16,.62)}
ul.x{list-style:none}
ul.x li{font-size:40px;line-height:1.25;padding:22px 0 22px 70px;position:relative;border-top:2px solid rgba(17,17,16,.14)}
ul.x li:before{content:'✕';position:absolute;left:4px;top:20px;color:__NARANJO__;font-weight:600}
ol.pasos{list-style:none;counter-reset:n}
ol.pasos li{counter-increment:n;position:relative;padding:0 0 0 110px;margin:0 0 42px}
ol.pasos li:before{content:counter(n);position:absolute;left:0;top:-6px;width:78px;height:78px;background:__NARANJO__;color:#fff;
  font-family:'Barlow Condensed';font-weight:700;font-size:52px;display:flex;align-items:center;justify-content:center}
ol.pasos b{display:block;font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;font-size:44px;line-height:1}
ol.pasos span{font-size:30px;line-height:1.3;opacity:.85}
.dots{display:flex;gap:10px}
.dots i{width:14px;height:14px;border-radius:50%;background:currentColor;opacity:.3}
.dots i.on{opacity:1;background:__NARANJO__}
.swipe{font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:30px}
"""


def pagina(w, h, cuerpo, fondo=None):
    css = (CSS.replace("__W__", str(w)).replace("__H__", str(h))
              .replace("__NARANJO__", NARANJO).replace("__OSCURO__", OSCURO)
              .replace("__CLARO__", CLARO))
    estilo = ' style="background:%s"' % fondo if fondo else ""
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="../fonts/fonts.css"><style>%s</style></head>'
            '<body%s>%s</body></html>' % (css, estilo, cuerpo))


def img(nombre):
    return "../img/%s.jpg" % nombre


def brand(neg=False, x=None, y=None, extra="", blanco=False):
    pos = ' style="left:%dpx;top:%dpx;%s"' % (x, y, extra) if x is not None else ""
    cls = "brand neg" if neg else ("brand blanco" if blanco else "brand")
    return ('<div class="%s abs"%s>%s<img src="../img/wordmark-blanco.png" alt="AVERARQ"></div>'
            % (cls, pos, ISOTIPO))


def dots(n, on, color="#fff", x=80, y=990):
    d = "".join('<i class="on"></i>' if i == on else "<i></i>" for i in range(n))
    return '<div class="dots abs" style="left:%dpx;top:%dpx;color:%s">%s</div>' % (x, y, color, d)


def foto(nombre, x, y, w, h, pos="center"):
    return ('<div class="img" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;'
            'background-image:url(%s);background-position:%s"></div>' % (x, y, w, h, img(nombre), pos))


COBERTURA = "Llay-Llay · Catemu · San Felipe · Los Andes · Rinconada · Putaendo · Quillota · La Calera"

# ======================================================================
# A · REGULARIZACIÓN
# ======================================================================

def a1_carrusel():
    n = 5
    s = []
    # 1 — portada
    s.append(pagina(*CUAD, fondo=NARANJO, cuerpo=
        brand(x=80, y=80, blanco=True) +
        '<div class="abs" style="left:80px;top:250px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:150px">¿Ampliaste<br>sin permiso?</div>'
        '<div class="p" style="margin-top:40px;font-size:44px;color:#fff">Así se pone en regla tu casa ante la DOM, paso a paso.</div></div>'
        '<div class="abs swipe" style="right:80px;top:975px;color:#fff">Desliza →</div>' +
        dots(n, 0, "#fff")))
    # 2 — problema
    s.append(pagina(*CUAD, cuerpo=
        '<div class="abs" style="left:80px;top:80px;width:920px">'
        '<span class="chip">Regularizaciones</span>'
        '<div class="h1" style="font-size:88px;margin:36px 0 34px">Sin recepción final,<br>tu casa <span class="o">no existe</span><br>para el sistema</div>'
        '<ul class="x"><li>No se vende con escritura limpia</li><li>No califica para crédito hipotecario</li>'
        '<li>Traba la herencia y la subdivisión</li><li>Queda expuesta a multas municipales</li></ul></div>' +
        dots(n, 1, OSCURO)))
    # 3 — proceso
    s.append(pagina(*CUAD, fondo=OSCURO, cuerpo=
        '<div class="abs" style="left:80px;top:80px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:88px;margin-bottom:56px">Casi todo es<br><span class="o">regularizable</span></div>'
        '<ol class="pasos">'
        '<li><b>Conversamos tu caso</b><span>Reviso la factibilidad y te digo con franqueza por dónde va.</span></li>'
        '<li><b>Visita y levantamiento</b><span>Mido lo efectivamente construido (as-built).</span></li>'
        '<li><b>Expediente y DOM</b><span>Ingreso, respondo observaciones y gestiono por ti.</span></li>'
        '<li><b>Recepción final</b><span>Lista para vender, hipotecar o heredar.</span></li>'
        '</ol></div>' + dots(n, 2, "#fff")))
    # 4 — Ley del Mono
    s.append(pagina(*CUAD, cuerpo=
        '<div class="abs" style="left:80px;top:80px;width:920px">'
        '<span class="chip line">Ley 20.898 · “Ley del Mono”</span>'
        '<div class="h1" style="font-size:96px;margin:40px 0 30px">El camino<br>más simple,<br><span class="o">si tu caso califica</span></div>'
        '<div class="p" style="font-size:36px">Procedimiento simplificado: permiso y recepción en un mismo trámite, '
        'para viviendas y ampliaciones que cumplen requisitos de superficie y antigüedad.</div>'
        '<div class="d" style="margin-top:44px;font-size:44px;font-weight:600">Vigente hasta el <span class="o">31 de diciembre de 2027</span></div>'
        '</div>' + dots(n, 3, OSCURO)))
    # 5 — CTA
    s.append(pagina(*CUAD, fondo=OSCURO, cuerpo=
        foto("sancarlos-planta", 0, 0, 1080, 1080) + '<div class="shade-full"></div>' +
        '<div class="abs" style="left:80px;top:150px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:120px">Escríbeme.<br><span class="o">En 24 h</span> te digo<br>por dónde va<br>tu caso.</div>'
        '<div class="small" style="margin-top:46px;opacity:.85">%s</div></div>' % COBERTURA +
        brand(x=80, y=920) +
        '<div class="abs d" style="right:80px;top:935px;color:#fff;font-size:34px;font-weight:600">averarq.cl</div>'))
    return [("A1-regularizacion-carrusel-%02d" % (i + 1), CUAD, h) for i, h in enumerate(s)]


def a2_plazo():
    def cuerpo(w, h):
        story = h > 1500
        top = 330 if story else 90
        fecha_fs = 330 if story else 215
        return pagina(w, h, fondo=OSCURO, cuerpo=
            foto("sancarlos-planta", 0, 0, w, h) + '<div class="shade-full" style="background:rgba(17,17,16,.8)"></div>' +
            brand(x=80, y=top) +
            '<div class="abs" style="left:80px;top:%dpx;width:920px;color:#fff">' % (top + 150) +
            '<span class="chip">Ley del Mono · 20.898</span>'
            '<div class="h2" style="font-size:64px;margin-top:40px;opacity:.9">Hoy está vigente hasta el</div>'
            '<div class="h1 o" style="font-size:%dpx;margin-top:10px">31 DIC<br>2027</div>' % fecha_fs +
            '<div class="p" style="margin-top:40px;color:#fff">Si construiste un dormitorio, un segundo piso o un quincho sin permiso, '
            'revisemos si tu caso califica.</div>'
            '<div class="d" style="margin-top:44px;font-size:46px;font-weight:600">Revisión gratis por WhatsApp →</div>'
            '</div>' +
            ('' if story else '<div class="abs small" style="left:80px;bottom:70px;color:#fff;opacity:.7">Arquitecto PUCV · Valle del Aconcagua · averarq.cl</div>'))
    return [("A2-ley-del-mono-plazo-feed", FEED, cuerpo(*FEED)),
            ("A2-ley-del-mono-plazo-story", STORY, cuerpo(*STORY))]


def a3_venta():
    def cuerpo(w, h):
        story = h > 1500
        top = 330 if story else 90
        return pagina(w, h, cuerpo=
            brand(neg=True, x=80, y=top) +
            '<div class="abs" style="left:80px;top:%dpx;width:920px">' % (top + 140) +
            '<div class="h1" style="font-size:%dpx">¿Vas a vender<br>o pedir un<br>crédito?</div>' % (170 if story else 124) +
            '<div class="rule" style="margin:44px 0"></div>'
            '<div class="h2" style="font-size:%dpx">El banco te va a pedir<br>la <span class="o">recepción final</span>.</div>' % (88 if story else 66) +
            '<div class="p" style="margin-top:40px">Una ampliación sin permiso puede frenar la venta, el crédito o la herencia. '
            'Regularizo ante la DOM, incluida la Ley del Mono cuando aplica.</div></div>' +
            '<div class="abs" style="left:80px;right:80px;bottom:%dpx;border-top:3px solid %s;padding-top:26px">'
            % (400 if story else 70, OSCURO) +
            '<div class="small">%s</div></div>' % COBERTURA)
    return [("A3-vender-credito-feed", FEED, cuerpo(*FEED)),
            ("A3-vender-credito-story", STORY, cuerpo(*STORY))]


# ======================================================================
# B · CASA EN TU PARCELA
# ======================================================================

def b1_parcela_a_casa():
    out = []
    # FEED: foto grande del render + dos fotos reales de obra
    w, h = FEED
    out.append(("B1-de-tu-parcela-a-tu-casa-feed", FEED, pagina(w, h, fondo=OSCURO, cuerpo=
        foto("obra-terreno", 0, 0, 356, 560, "center 60%") +
        foto("obra-cerchas", 362, 0, 356, 560) +
        foto("sancarlos-render", 724, 0, 356, 560, "38% center") +
        '<div class="lbl" style="left:0;top:500px">1 · Terreno</div>'
        '<div class="lbl" style="left:362px;top:500px">2 · Obra</div>'
        '<div class="lbl" style="left:724px;top:500px">3 · Proyecto</div>' +
        '<div class="abs" style="left:80px;top:630px;width:920px;color:#fff">'
        '<span class="chip">Casa en tu parcela</span>'
        '<div class="h1" style="font-size:118px;margin-top:34px">De tu parcela<br>a <span class="o">tu casa</span></div>'
        '<div class="p" style="margin-top:30px;color:#fff;opacity:.9">Diseño, permiso e inspección de obra hasta la recepción final.</div>'
        '</div>' +
        '<div class="abs small" style="left:80px;top:1215px;color:#fff;opacity:.75">Casa San Carlos · Catemu · 144 m² · en construcción</div>' +
        brand(x=735, y=1200, extra="transform:scale(.8);transform-origin:right center"))))
    # STORY: tres fotos apiladas + panel oscuro con el titular
    w, h = STORY
    out.append(("B1-de-tu-parcela-a-tu-casa-story", STORY, pagina(w, h, fondo=OSCURO, cuerpo=
        foto("obra-terreno", 0, 0, 1080, 420, "center 60%") +
        foto("obra-ladrillo", 0, 426, 1080, 380, "center 55%") +
        foto("sancarlos-render", 0, 812, 1080, 420, "40% 70%") +
        '<div class="abs" style="left:0;top:0;width:1080px;height:420px;background:linear-gradient(180deg,rgba(17,17,16,.25),rgba(17,17,16,0))"></div>' +
        brand(x=80, y=250) +
        '<div class="lbl" style="left:80px;top:360px">1 · Tu terreno</div>'
        '<div class="lbl" style="left:80px;top:746px">2 · La obra</div>'
        '<div class="lbl" style="left:80px;top:1172px">3 · Tu casa</div>' +
        '<div class="abs" style="left:80px;top:1270px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:124px">De tu parcela<br>a <span class="o">tu casa</span></div>'
        '<div class="small" style="margin-top:22px;opacity:.8">Casa San Carlos · Catemu · 144 m² · en construcción</div></div>')))
    return out


def b2_estimador():
    def tarjeta(escala=1.0):
        fila = ('<div style="display:flex;justify-content:space-between;border-bottom:2px solid #e3e0d8;padding:20px 0;font-size:32px">'
                '<span style="opacity:.7">%s</span><b>%s</b></div>')
        return ('<div style="background:#fff;padding:44px 50px;box-shadow:0 30px 60px rgba(0,0,0,.35);transform:scale(%s);transform-origin:left top">' % escala +
                '<div class="d" style="font-size:30px;letter-spacing:.12em;color:%s;font-weight:600">Estimador de honorarios · averarq.cl</div>' % NARANJO +
                fila % ("Servicio", "Arquitectura + ingenierías") +
                fila % ("Superficie", "120 m²") +
                fila % ("Nivel de detalle", "Estándar") +
                fila % ("Ubicación", "Valle del Aconcagua") +
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:26px">'
                '<span class="d" style="font-size:34px;font-weight:600">Referencia en UF</span>'
                '<span class="d" style="font-size:40px;font-weight:600;background:#FC4C02;color:#fff;padding:12px 26px 10px">Calcular →</span></div></div>')

    w, h = FEED
    feed = pagina(w, h, cuerpo=
        foto("doblel-terraza", 0, 0, 1080, 620, "center 60%") +
        '<div class="abs" style="left:80px;top:420px;width:760px">%s</div>' % tarjeta() +
        '<div class="abs" style="left:80px;top:1000px;width:920px">'
        '<div class="h1" style="font-size:92px">¿Cuánto cuesta<br><span class="o">diseñar tu casa?</span></div>'
        '<div class="p" style="margin-top:20px;font-size:34px">Calcula una referencia en UF en 1 minuto. Sin letra chica.</div></div>' +
        '<div class="abs small" style="right:80px;top:40px;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.6)">Casa Doble L · Llay-Llay</div>')
    w, h = STORY
    story = pagina(w, h, cuerpo=
        foto("doblel-terraza", 0, 0, 1080, 900, "center 60%") +
        brand(x=80, y=250) +
        '<div class="abs" style="left:80px;top:640px;width:840px">%s</div>' % tarjeta(1.08) +
        '<div class="abs" style="left:80px;top:1290px;width:920px">'
        '<div class="h1" style="font-size:108px">¿Cuánto cuesta<br><span class="o">diseñar tu casa?</span></div>'
        '<div class="p" style="margin-top:24px">Calcula una referencia en UF en 1 minuto en averarq.cl</div></div>')
    return [("B2-estimador-honorarios-feed", FEED, feed), ("B2-estimador-honorarios-story", STORY, story)]


def b3_carrusel_5_cosas():
    temas = [
        ("¿Urbano o rural?", "Pide el Certificado de Informaciones Previas (CIP) en la DOM. Desde mayo de 2025 rige el Plan Regulador "
         "Metropolitano Satélite Alto Aconcagua: las reglas cambiaron en 10 comunas del valle."),
        ("Papeles al día", "Escritura inscrita y rol del SII de tu lote. Fuera del límite urbano aplican reglas especiales (art. 55 LGUC)."),
        ("Agua y alcantarillado", "Factibilidad sanitaria o solución particular aprobada por la SEREMI de Salud. Define dónde y cuánto puedes construir."),
        ("Topografía y acceso", "Pendientes, deslindes y acceso vehicular. Un levantamiento con dron lo resuelve en una visita."),
        ("Sol y viento", "La orientación decide dónde van el living y los dormitorios. La estudio antes de dibujar el primer plano."),
    ]
    n = len(temas) + 2
    s = [pagina(*CUAD, fondo=OSCURO, cuerpo=
        foto("obra-terreno", 600, 0, 480, 1080, "center 60%") +
        '<div class="abs" style="left:80px;top:80px;width:500px;color:#fff">'
        '<span class="chip">Casa en tu parcela</span>'
        '<div class="h1" style="font-size:108px;margin-top:40px"><span class="o">5 cosas</span><br>antes de<br>construir<br>en tu<br>parcela</div></div>'
        '<div class="abs swipe" style="left:80px;top:975px;color:#fff">Desliza →</div>')]
    for i, (t, d) in enumerate(temas):
        s.append(pagina(*CUAD, cuerpo=
            '<div class="abs d o" style="left:80px;top:60px;font-size:300px;font-weight:700;line-height:1">%d</div>' % (i + 1) +
            '<div class="abs" style="left:80px;top:420px;width:920px">'
            '<div class="h1" style="font-size:104px">%s</div>'
            '<div class="rule" style="margin:40px 0"></div>'
            '<div class="p" style="font-size:40px">%s</div></div>' % (t, d) +
            dots(n, i + 1, OSCURO)))
    s.append(pagina(*CUAD, fondo=NARANJO, cuerpo=
        brand(x=80, y=80, blanco=True) +
        '<div class="abs" style="left:80px;top:260px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:118px">¿Tienes<br>la parcela?<br>Conversemos.</div>'
        '<div class="p" style="margin-top:40px;color:#fff">Reunión gratuita de 30 min y referencia de honorarios en averarq.cl</div></div>' +
        dots(n, n - 1, "#fff")))
    return [("B3-5-cosas-parcela-carrusel-%02d" % (i + 1), CUAD, h) for i, h in enumerate(s)]


def b4_carrusel_proyectos():
    proyectos = [
        ("sancarlos-render", "Casa San Carlos", "Catemu", "144 m² · Diseño e ITO · 2025–26", "38% center"),
        ("lacolonia-render", "Casa La Colonia", "Catemu", "138 m² · Diseño e ITO · 2025–26", "center"),
        ("doblel-jardin", "Casa Doble L", "Llay-Llay", "120 m² · Diseño · 2023", "center"),
        ("casa31-cocina", "Cocina & Living · Casa 31", "Rinconada", "Condominio Los Placeres · 2024", "center"),
    ]
    n = len(proyectos) + 1
    s = []
    for i, (f, nombre, comuna, meta, pos) in enumerate(proyectos):
        s.append(pagina(*CUAD, fondo=OSCURO, cuerpo=
            foto(f, 0, 0, 1080, 760, pos) +
            '<div class="chip abs" style="left:80px;top:60px">%s</div>' % comuna +
            '<div class="abs" style="left:80px;top:800px;width:920px;color:#fff">'
            '<div class="h1" style="font-size:84px">%s</div>'
            '<div class="small" style="margin-top:14px;opacity:.8;font-size:30px">%s</div></div>' % (nombre, meta) +
            dots(n, i, "#fff", x=80, y=1000) +
            ('<div class="abs swipe" style="right:80px;top:990px;color:#fff">Desliza →</div>' if i == 0 else "")))
    s.append(pagina(*CUAD, fondo=NARANJO, cuerpo=
        brand(x=80, y=80, blanco=True) +
        '<div class="abs" style="left:80px;top:250px;width:920px;color:#fff">'
        '<div class="h1" style="font-size:112px">Arquitectura<br>del Valle,<br>de principio<br>a recepción.</div>'
        '<div class="p" style="margin-top:36px;color:#fff">Tu terreno, tu diseño, tu casa. Conversemos.</div></div>' +
        dots(n, n - 1, "#fff")))
    return [("B4-proyectos-del-valle-carrusel-%02d" % (i + 1), CUAD, h) for i, h in enumerate(s)]


# ======================================================================
# C · COMERCIAL
# ======================================================================

def c1_restobar():
    def cuerpo(w, h):
        story = h > 1500
        return pagina(w, h, fondo=OSCURO, cuerpo=
            foto("restobar-barra", 0, 0, w, h, "center") + '<div class="shade" style="background:linear-gradient(180deg,rgba(17,17,16,.55) 0%,rgba(17,17,16,0) 30%,rgba(17,17,16,.2) 50%,rgba(17,17,16,.92) 78%)"></div>' +
            brand(x=80, y=250 if story else 80) +
            '<div class="abs" style="left:80px;bottom:%dpx;width:920px;color:#fff">' % (420 if story else 90) +
            '<span class="chip">Comercial</span>'
            '<div class="h1" style="font-size:%dpx;margin-top:30px">Del local vacío<br>al negocio<br><span class="o">funcionando</span></div>' % (118 if story else 106) +
            '<div class="p" style="margin-top:26px;color:#fff;opacity:.9">Diseño interior, remodelación y permisos en un solo equipo.</div>'
            '<div class="small" style="margin-top:22px;opacity:.75">Restobar Esmeralda · Los Andes · 110 m² · render del proyecto</div></div>')
    return [("C1-restobar-feed", FEED, cuerpo(*FEED)), ("C1-restobar-story", STORY, cuerpo(*STORY))]


def c2_patente():
    w, h = FEED
    return [("C2-patente-recepcion-feed", FEED, pagina(w, h, cuerpo=
        foto("restobar-salon", 0, 0, 1080, 560) +
        '<div class="abs" style="left:80px;top:610px;width:920px">'
        '<div class="h1" style="font-size:100px">¿Te piden<br>recepción final<br>para la <span class="o">patente?</span></div>'
        '<div class="p" style="margin-top:34px">Regularizo locales, gestiono cambios de destino y diseño tu negocio para que abras en regla.</div>'
        '<div class="d" style="margin-top:34px;font-size:42px;font-weight:600">Revisión gratuita de tu local →</div></div>' +
        brand(neg=True, x=80, y=1240, extra="transform:scale(.8);transform-origin:left center")))]


# ======================================================================
# M · MARCA / RETARGETING
# ======================================================================

def m1_marca():
    def cuerpo(w, h):
        story = h > 1500
        return pagina(w, h, fondo=OSCURO, cuerpo=
            foto("lacolonia-render", 0, 0, w, 760 if not story else 1000, "center") +
            '<div class="shade" style="height:%dpx;background:linear-gradient(180deg,rgba(17,17,16,.35),rgba(17,17,16,0) 40%%,rgba(17,17,16,.95))"></div>' % (760 if not story else 1000) +
            brand(x=80, y=250 if story else 80) +
            '<div class="abs" style="left:80px;top:%dpx;width:920px;color:#fff">' % (1000 if story else 700) +
            '<div class="h1" style="font-size:%dpx">Diseño con identidad.<br><span class="o">Permisos sin sorpresas.</span></div>' % (104 if story else 96) +
            '<div class="p" style="margin-top:30px;color:#fff;opacity:.9">Arquitecto con base en Llay-Llay. Estudio de sol y viento, dron propio y acompañamiento hasta la recepción final.</div>'
            '<div class="small" style="margin-top:34px;opacity:.7;line-height:1.6">%s</div></div>' % COBERTURA)
    return [("M1-marca-feed", FEED, cuerpo(*FEED)), ("M1-marca-story", STORY, cuerpo(*STORY))]


ANUNCIOS = (a1_carrusel() + a2_plazo() + a3_venta() +
            b1_parcela_a_casa() + b2_estimador() + b3_carrusel_5_cosas() + b4_carrusel_proyectos() +
            c1_restobar() + c2_patente() + m1_marca())

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "_lista.txt"), "w") as lista:
        for nombre, (w, h), html in ANUNCIOS:
            with open(os.path.join(OUT, nombre + ".html"), "w", encoding="utf-8") as f:
                f.write(html)
            lista.write("%s %d %d\n" % (nombre, w, h))
    print("%d piezas escritas en %s" % (len(ANUNCIOS), OUT))
