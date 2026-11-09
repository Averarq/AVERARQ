/* ===========================================================================
   HERO AVERARQ COMPARTIDO — arma el fondo de la portada (video del valle en
   panel diagonal + isotipo que se dibuja) dentro de cada <div data-av-hero>.
   El video se carga solo si el usuario no pidió reducir movimiento ni ahorrar
   datos, y en pantallas angostas usa la versión liviana (720 px).
   Ver hero.css para el uso.
   =========================================================================== */
(function () {
  var s = document.currentScript;
  var BASE = s && s.src ? s.src.replace(/[^\/]*$/, '') : '/media/hero/';
  var ISO = 'M43.17 0 L6.83 88.53 L74.87 88.53 L79.51 99.87 L93.04 99.74 L83.89 77.19 L24.61 77.19 L47.68 20.23 L54.12 36.73 L67.40 36.73 L52.58 0 Z';
  var TRAZO = 'M60.76 36.73 L47.88 0 L15.70 82.86 L79.38 82.86 L86.28 99.80';
  var n = 0;

  function armar(el) {
    if (el.getAttribute('data-av-hero-listo')) return;
    el.setAttribute('data-av-hero-listo', '1');
    el.classList.add('av-hero');
    el.setAttribute('aria-hidden', 'true');
    var m = 'avhMask' + (n++);
    el.innerHTML =
      '<div class="avh-grid"></div>' +
      '<div class="avh-video"><video muted loop playsinline preload="none" poster="' + BASE + 'hero-valle.webp"></video></div>' +
      '<div class="avh-iso"><svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' +
        '<defs><mask id="' + m + '" maskUnits="userSpaceOnUse" x="-25" y="-25" width="150" height="150">' +
          '<path class="avh-reveal" pathLength="100" d="' + TRAZO + '" fill="none" stroke="#fff" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>' +
        '</mask></defs>' +
        '<path class="avh-halo" d="' + ISO + '"/>' +
        '<path class="avh-fill" d="' + ISO + '" mask="url(#' + m + ')"/>' +
      '</svg></div>';
    video(el.querySelector('video'));
  }

  function video(v) {
    if (!v) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var c = navigator.connection;
    if (c && (c.saveData || /2g/.test(c.effectiveType || ''))) return;
    v.muted = true;
    v.src = BASE + (window.matchMedia('(max-width: 1100px)').matches ? 'hero-valle_720.mp4' : 'hero-valle_1440.mp4');
    v.addEventListener('playing', function () { v.classList.add('listo'); }, { once: true });
    var p = v.play(); if (p && p.catch) p.catch(function () {});
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) v.pause();
      else { var q = v.play(); if (q && q.catch) q.catch(function () {}); }
    });
  }

  function iniciar() { document.querySelectorAll('[data-av-hero]').forEach(armar); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
