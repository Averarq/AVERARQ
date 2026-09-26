// render-video.mjs — convierte los reels de _fuente/video/*.html en MP4 1080×1920 (../videos/).
//
// Uso:
//   node render-video.mjs              # todos los videos
//   node render-video.mjs V1 V3        # solo los que empiezan con esos códigos
//   node render-video.mjs V1 --cuadros # además guarda 6 cuadros de control en frames/
//
// Si el HTML define window.AUDIO, se agrega esa pista (ver musica/).
// Requiere ffmpeg en el PATH y Playwright: `npm i --no-save playwright-core`
// (usa Microsoft Edge o Chrome instalados) o `playwright` con su Chromium.
import { readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawn, execSync } from 'node:child_process';

const aqui = dirname(fileURLToPath(import.meta.url));
const FPS = 30;

async function cargarPlaywright() {
  for (const nombre of ['playwright-core', 'playwright']) {
    try { return await import(nombre); } catch {}
  }
  const global = execSync('npm root -g').toString().trim();
  return await import(pathToFileURL(join(global, 'playwright', 'index.mjs')).href);
}

async function abrirNavegador(pw) {
  for (const channel of ['msedge', 'chrome', undefined]) {
    try { return await pw.chromium.launch(channel ? { channel } : {}); } catch {}
  }
  throw new Error('No encontré Edge, Chrome ni el Chromium de Playwright.');
}

const args = process.argv.slice(2);
const cuadros = args.includes('--cuadros');
const filtros = args.filter(a => !a.startsWith('--'));
const videos = readdirSync(join(aqui, 'video'))
  .filter(f => /^V\d.*\.html$/.test(f))
  .filter(f => !filtros.length || filtros.some(c => f.startsWith(c)));

const salida = join(aqui, '..', 'videos');
mkdirSync(salida, { recursive: true });
if (cuadros) mkdirSync(join(aqui, 'frames'), { recursive: true });

const pw = await cargarPlaywright();
const browser = await abrirNavegador(pw);

for (const archivo of videos) {
  const nombre = archivo.replace(/\.html$/, '');
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(join(aqui, 'video', archivo)).href + '?render', { waitUntil: 'load' });
  await page.evaluate(() => window.listo);
  const { dur, portada, audio } = await page.evaluate(() => ({ dur: window.DURACION, portada: window.PORTADA, audio: window.AUDIO }));
  const total = Math.round(dur * FPS);

  // si el video define window.AUDIO (ruta relativa al HTML), se mezcla como pista AAC
  const pista = audio ? ['-i', join(aqui, 'video', audio), '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-t', String(dur)] : [];
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...pista,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    join(salida, nombre + '.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const fin = new Promise((ok, mal) => ff.on('close', c => c === 0 ? ok() : mal(new Error('ffmpeg salió con ' + c))));

  const control = new Set(Array.from({ length: 6 }, (_, i) => Math.round((i + 0.5) * total / 6)));
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.frame(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (cuadros && control.has(i)) writeFileSync(join(aqui, 'frames', `${nombre}-${String(i).padStart(3, '0')}.jpg`), buf);
  }
  ff.stdin.end();
  await fin;

  // miniatura (portada del reel)
  await page.evaluate(t => window.frame(t), portada);
  await page.screenshot({ path: join(salida, nombre + '-portada.jpg'), type: 'jpeg', quality: 92 });
  await page.close();
  console.log(`✓ ${nombre}.mp4 · ${dur}s · ${total} cuadros`);
}
await browser.close();
