/* motor.js — animación determinista para los reels de AVERARQ.
 *
 * Cada video define:
 *   window.DURACION = segundos;
 *   window.PORTADA  = segundo que se usa como miniatura;
 *   window.frame    = function (t) { ... }   // pinta el estado exacto en el segundo t
 *
 * Abierto en el navegador se reproduce en bucle (clic = reiniciar).
 * render-video.mjs lo abre con ?render y llama frame(t) cuadro a cuadro.
 */
(function () {
  var clamp = function (x, a, b) { return Math.min(b === undefined ? 1 : b, Math.max(a || 0, x)); };

  // progreso 0→1 de t entre a y b
  window.p = function (t, a, b) { return clamp((t - a) / (b - a)); };
  window.lerp = function (a, b, k) { return a + (b - a) * k; };
  window.ease = {
    out: function (x) { return 1 - Math.pow(1 - x, 3); },
    inOut: function (x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; },
    back: function (x) { var c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }
  };
  window.$ = function (s) { return document.querySelector(s); };
  window.$$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  // visible entre [a, b): para escenas completas
  window.escena = function (el, t, a, b) {
    if (typeof el === 'string') el = $(el);
    el.style.display = (t >= a && t < b) ? '' : 'none';
    return t >= a && t < b;
  };

  // entrada típica: sube y aparece
  window.sube = function (el, t, a, dur, dist) {
    if (typeof el === 'string') el = $(el);
    var k = ease.out(p(t, a, a + (dur || 0.5)));
    el.style.opacity = k;
    el.style.transform = 'translateY(' + ((1 - k) * (dist === undefined ? 60 : dist)) + 'px)';
  };

  // Ken Burns sobre un <img> dentro de un marco con overflow:hidden
  window.kb = function (el, t, a, b, s0, s1, x0, x1, y0, y1) {
    if (typeof el === 'string') el = $(el);
    var k = ease.inOut(p(t, a, b));
    el.style.transform = 'translate(' + lerp(x0 || 0, x1 || 0, k) + 'px,' + lerp(y0 || 0, y1 || 0, k) + 'px) scale(' + lerp(s0, s1, k) + ')';
  };

  // tramo de video: muestra en el <img> el cuadro que corresponde al segundo t
  // (las carpetas las genera extraer_secuencias.py a 30 fps). Devuelve una promesa
  // que el render espera, para no capturar un cuadro sin decodificar.
  window.secuencia = function (el, carpeta, n, t, a) {
    if (typeof el === 'string') el = $(el);
    var i = Math.min(n, Math.max(1, Math.floor((t - a) * 30) + 1));
    var src = '../secuencias/' + carpeta + '/' + ('000' + i).slice(-4) + '.jpg';
    if (el.getAttribute('src') === src) return Promise.resolve();
    el.setAttribute('src', src);
    return el.decode().catch(function () {});
  };

  // espera fuentes e imágenes
  window.listo = (async function () {
    await new Promise(function (r) { if (document.readyState === 'complete') r(); else addEventListener('load', r); });
    await document.fonts.ready;
    await Promise.all($$('img').filter(function (i) { return i.getAttribute('src'); })
      .map(function (i) { return i.decode().catch(function () {}); }));
    return true;
  })();

  if (location.search.indexOf('render') < 0) {
    listo.then(function () {
      var t0 = performance.now();
      document.addEventListener('click', function () { t0 = performance.now(); });
      (function loop() {
        var t = ((performance.now() - t0) / 1000) % DURACION;
        frame(t);
        requestAnimationFrame(loop);
      })();
    });
  }
})();
