/* Dibuja bloques extraídos de láminas AVERARQ (bloques.js) con la línea gráfica del post.
   bloque(g, nombre, x, y, w, h, opt) encaja el bloque en el rectángulo [x, y, w, h] (px) manteniendo proporción.
   opt: { lin: color líneas, acc: color de lo azul (accesibilidad), rot: giro en rad, grosor: factor de trazo, sinAcc: omite lo azul } */
// caja ajustada al dibujo (no al recorte), para que el bloque quede centrado de verdad
function caja(B, sinAcc) {
  const k = sinAcc ? '_cs' : '_c'; if (B[k]) return B[k];
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const m = (x, y) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); };
  for (const p of B.p) { if (sinAcc && (p.s === 'a' || p.f === 'a')) continue; for (const o of p.o) { if (o[0] === 're') { m(o[1], o[2]); m(o[1] + o[3], o[2] + o[4]); } else o.slice(1).forEach(q => m(q[0], q[1])); } }
  return (B[k] = { w: x1 - x0, h: y1 - y0, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 });
}
function bloque(g, nombre, x, y, w, h, opt = {}) {
  const B = window.BLOQUES[nombre], lin = opt.lin || 'rgba(242,240,235,0.9)', acc = opt.acc || '#FC4C02';
  const C = caja(B, opt.sinAcc), rot = opt.rot || 0, cw = Math.abs(Math.cos(rot)), sw = Math.abs(Math.sin(rot));
  const bw = C.w * cw + C.h * sw, bh = C.w * sw + C.h * cw, s = Math.min(w / bw, h / bh);
  g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(rot); g.scale(s, s); g.translate(-C.cx, -C.cy);
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
