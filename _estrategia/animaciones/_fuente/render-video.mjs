// render-video.mjs — renderiza una animación (HTML en esta carpeta) cuadro a cuadro y la codifica en MP4 (H.264).
//
// Se dibuja a 2× (2160 × 2700) y de una sola pasada salen dos archivos:
//   ../<pieza>-4x5.mp4        1080 × 1350 para el feed (reducido con Lanczos: bordes más limpios)
//   ../<pieza>-4x5-2160.mp4   2160 × 2700 maestro (web, presentaciones, pantalla grande)
// y la portada en JPG a 2160 × 2700.
//
// Uso:
//   --pieza paneles-sip                      → elige la animación (por defecto albanileria-confinada)
//   node render-video.mjs                    → video completo (maestro + feed) y portada
//   node render-video.mjs --fotos 9 18 28.4  → solo cuadros sueltos (PNG a 1080; con --escala 2, a 2160)
//   node render-video.mjs --escala 1         → render directo a 1080 (más rápido, para pruebas)
//   --reel                                   → formato reel 9:16: ../<pieza>-9x16.mp4 (1080 × 1920) y ../<pieza>-9x16-2160.mp4 (2160 × 3840)
// Requiere Playwright y ffmpeg con libx264 (pip install imageio-ffmpeg lo trae).
import { spawn, execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
let ffmpeg = 'ffmpeg';
try { ffmpeg = execSync('python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"').toString().trim(); } catch {}

const REEL = process.argv.includes('--reel');
const FPS = 30, W = 1080, H = REEL ? 1920 : 1350, FMT = REEL ? '9x16' : '4x5';
const args = process.argv.slice(2);
const fotos = args.includes('--fotos');
const iEsc = args.indexOf('--escala');
const iPz = args.indexOf('--pieza');
const PIEZA = iPz >= 0 ? args[iPz + 1] : 'albanileria-confinada';
const S = iEsc >= 0 ? +args[iEsc + 1] : (fotos ? 1 : 2);
const arg = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const DESDE = +(arg('--desde') ?? 0), HASTA = arg('--hasta'), SALIDA = arg('--salida'); // tramo, para armar compilados

const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: W * S, height: H * S }, deviceScaleFactor: 1 });
page.on('console', m => console.log('[página]', m.text()));
await page.goto(pathToFileURL(join(aqui, `${PIEZA}.html`)).href + `?escala=${S}${REEL ? '&formato=reel' : ''}`);
await page.evaluate(() => window.ready);
const lienzo = await page.$('canvas');

if (fotos) {
  const tiempos = args.slice(args.indexOf('--fotos') + 1).filter(v => !isNaN(+v) && !['--escala'].includes(v));
  for (const s of tiempos.filter((v, i) => args[args.indexOf(v) - 1] !== '--escala')) {
    await page.evaluate(t => window.render(t), +s);
    await lienzo.screenshot({ path: join(aqui, `foto-${PIEZA}${REEL ? '-reel' : ''}-${s}.png`) });
    console.log('✓ foto', s);
  }
  await browser.close(); process.exit(0);
}

const dur = await page.evaluate(() => window.DUR);
const feed = SALIDA ? SALIDA : join(aqui, '..', `${PIEZA}-${FMT}.mp4`);
const maestro = SALIDA ? SALIDA.replace(/\.mp4$/, `-${W * S}.mp4`) : join(aqui, '..', `${PIEZA}-${FMT}-${W * S}.mp4`);
const x264 = ['-c:v', 'libx264', '-preset', 'slow', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'];
const salidas = S > 1
  ? ['-filter_complex', `[0:v]split=2[a][b];[b]scale=${W}:${H}:flags=lanczos[f]`,
     '-map', '[a]', ...x264, '-crf', '14', maestro,
     '-map', '[f]', ...x264, '-crf', '14', feed]
  : [...x264, '-crf', '14', feed];
const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...salidas],
  { stdio: ['pipe', 'inherit', 'inherit'] });
const fin = HASTA != null ? +HASTA : dur, total = Math.round((fin - DESDE) * FPS);
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.render(t), DESDE + f / FPS);
  const buf = await lienzo.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 90 === 0) console.log(`cuadro ${f}/${total}`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
// portada (cuadro final del detalle, antes de la contraportada) para usar como miniatura
if (!REEL && !SALIDA) { // la portada del reel se genera aparte con portada-post.mjs
  await page.evaluate(() => window.render(window.PORTADA));
  await lienzo.screenshot({ path: join(aqui, '..', `${PIEZA}-portada.jpg`), type: 'jpeg', quality: 95 });
}
await browser.close();
console.log('✓', feed); if (S > 1) console.log('✓', maestro);
