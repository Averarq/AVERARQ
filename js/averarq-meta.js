/* Averarq · Meta Pixel con consentimiento
 *
 * 1. Pega el ID del Pixel en PIXEL_ID (Administrador de eventos de Meta →
 *    Orígenes de datos → tu Pixel → "ID del conjunto de datos").
 *    Mientras esté vacío, este script no hace nada: no carga Meta ni muestra aviso.
 * 2. El Pixel solo se carga si la persona acepta en el aviso inferior
 *    (Ley 19.628 y Ley 21.719). La decisión se recuerda en este navegador.
 *
 * Eventos que se envían:
 *   PageView     → al cargar cualquier página que incluya este script.
 *   Contact      → clic en cualquier enlace a WhatsApp (wa.me).
 *   ViewContent  → primera vez que se usa el estimador de honorarios (#cotizador).
 *   Lead         → clic en "Conversemos tu proyecto" del estimador, con el
 *                  valor mínimo estimado en CLP (sirve para medir ROAS de honorarios).
 */
(function () {
  var PIXEL_ID = '';

  if (!PIXEL_ID) return;

  var CLAVE = 'avq-consentimiento-meta';
  var cargado = false;

  function leer() {
    try { return localStorage.getItem(CLAVE); } catch (e) { return null; }
  }
  function guardar(v) {
    try { localStorage.setItem(CLAVE, v); } catch (e) {}
  }

  function cargarPixel() {
    if (cargado) return;
    cargado = true;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', PIXEL_ID);
    fbq('track', 'PageView');
  }

  function track(evento, datos) {
    if (cargado && window.fbq) fbq('track', evento, datos || {});
  }

  // --- Eventos ---
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('wa.me/') >= 0) {
      track('Contact', { content_name: location.pathname });
    }
    if (a.classList.contains('result-cta')) {
      var clp = document.getElementById('result-clp');
      var num = clp ? parseInt((clp.textContent.split('–')[0] || '').replace(/\D/g, ''), 10) : 0;
      track('Lead', num ? { value: num, currency: 'CLP', content_name: 'estimador' } : { content_name: 'estimador' });
    }
  });

  var cotizador = document.getElementById('cotizador');
  if (cotizador) {
    var visto = false;
    var marcar = function () {
      if (visto) return;
      visto = true;
      track('ViewContent', { content_name: 'estimador' });
    };
    cotizador.addEventListener('click', function (e) {
      if (e.target.closest('.opcion')) marcar();
    });
    cotizador.addEventListener('input', marcar);
  }

  // --- Aviso de consentimiento ---
  var decision = leer();
  if (decision === 'si') { cargarPixel(); return; }
  if (decision === 'no') return;

  var css = document.createElement('style');
  css.textContent =
    '.avq-aviso{position:fixed;left:16px;right:16px;bottom:16px;z-index:300;max-width:560px;margin:0 auto;' +
    'background:#1e1e1c;color:#f2f0eb;border:0.5px solid rgba(255,255,255,0.12);border-radius:4px;' +
    'padding:16px 18px;font-family:Barlow,sans-serif;font-size:14px;font-weight:300;line-height:1.5;' +
    'box-shadow:0 8px 32px rgba(0,0,0,0.45);display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center}' +
    '.avq-aviso p{flex:1 1 280px;margin:0;max-width:none}' +
    '.avq-aviso a{color:#FF4D00;text-decoration:none}' +
    '.avq-aviso-btns{display:flex;gap:8px;margin-left:auto}' +
    '.avq-aviso button{font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:13px;letter-spacing:0.08em;' +
    'text-transform:uppercase;padding:9px 16px;border-radius:2px;cursor:pointer;border:0.5px solid rgba(242,240,235,0.25);' +
    'background:none;color:#f2f0eb}' +
    '.avq-aviso button.avq-si{background:#FF4D00;border-color:#FF4D00;color:#fff}';
  document.head.appendChild(css);

  var aviso = document.createElement('div');
  aviso.className = 'avq-aviso';
  aviso.setAttribute('role', 'region');
  aviso.setAttribute('aria-label', 'Aviso de privacidad');
  aviso.innerHTML =
    '<p>Uso cookies de Meta para saber qué anuncios funcionan. El sitio funciona igual si las rechazas. ' +
    '<a href="/privacidad/">Política de privacidad</a></p>' +
    '<div class="avq-aviso-btns"><button type="button" class="avq-no">Rechazar</button>' +
    '<button type="button" class="avq-si">Aceptar</button></div>';
  document.body.appendChild(aviso);

  aviso.querySelector('.avq-si').addEventListener('click', function () {
    guardar('si'); aviso.remove(); cargarPixel();
  });
  aviso.querySelector('.avq-no').addEventListener('click', function () {
    guardar('no'); aviso.remove();
  });
})();
