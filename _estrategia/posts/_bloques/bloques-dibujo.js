/* Dibuja bloques extraídos de láminas AVERARQ (bloques.js) con la línea gráfica del post.
   bloque(g, nombre, x, y, w, h, opt) encaja el bloque en el rectángulo [x, y, w, h] (px) manteniendo proporción.
   opt: { lin: color líneas, acc: color de lo azul (accesibilidad), rot: giro en rad, grosor: factor de trazo, sinAcc: omite lo azul } */
function bloque(g, nombre, x, y, w, h, opt = {}) {
  const B = window.BLOQUES[nombre], lin = opt.lin || 'rgba(242,240,235,0.9)', acc = opt.acc || '#FC4C02';
  const rot = opt.rot || 0, cw = Math.abs(Math.cos(rot)), sw = Math.abs(Math.sin(rot));
  const bw = B.w * cw + B.h * sw, bh = B.w * sw + B.h * cw, s = Math.min(w / bw, h / bh);
  g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(rot); g.scale(s, s); g.translate(-B.w / 2, -B.h / 2);
  g.lineCap = 'round'; g.lineJoin = 'round';
  const col = c => c === 'a' ? acc : c === 'r' ? acc : c === 'w' ? (opt.fondo || '#111110') : lin;
  for (const p of B.p) {
    if (opt.sinAcc && (p.s === 'a' || p.f === 'a')) continue;
    g.beginPath(); let cur = null;
    for (const o of p.o) {
      if (o[0] === 'l') { if (!cur || cur[0] !== o[1][0] || cur[1] !== o[1][1]) g.moveTo(...o[1]); g.lineTo(...o[2]); cur = o[2]; }
      else if (o[0] === 'c') { if (!cur || cur[0] !== o[1][0] || cur[1] !== o[1][1]) g.moveTo(...o[1]); g.bezierCurveTo(...o[2], ...o[3], ...o[4]); cur = o[4]; }
      else if (o[0] === 're') { g.rect(o[1], o[2], o[3], o[4]); cur = null; }
      else if (o[0] === 'qu') { g.moveTo(...o[1]); g.lineTo(...o[2]); g.lineTo(...o[3]); g.lineTo(...o[4]); g.closePath(); cur = null; }
    }
    if (p.cerrar) g.closePath();
    if (p.f && p.f !== 'w') { g.fillStyle = p.f === 'a' ? (opt.accFill || 'rgba(252,76,2,0.25)') : col(p.f); g.fill(); }
    else if (p.f === 'w' && opt.tapar) { g.fillStyle = col('w'); g.fill(); }
    if (p.s) { g.strokeStyle = col(p.s); g.lineWidth = Math.max(p.w, .3) * (opt.grosor || 1) * (p.s === 'a' ? 1.6 : 1) + 1.1 / s; g.stroke(); }
  }
  g.restore();
  return s;
}
