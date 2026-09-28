// render-video.mjs — renderiza albanileria-confinada.html cuadro a cuadro y lo codifica en MP4 (H.264).
// Uso:
//   node render-video.mjs                 → ../albanileria-confinada-4x5.mp4 + portada JPG
//   node render-video.mjs --fotos 4 12 20 → solo cuadros sueltos (PNG) para revisar
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

const FPS = 30;
const args = process.argv.slice(2);
const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
page.on('console', m => console.log('[página]', m.text()));
await page.goto(pathToFileURL(join(aqui, 'albanileria-confinada.html')).href);
await page.evaluate(() => window.ready);
const lienzo = await page.$('canvas');

if (args[0] === '--fotos') {
  for (const s of args.slice(1)) {
    await page.evaluate(t => window.render(t), +s);
    await lienzo.screenshot({ path: join(aqui, `foto-${s}.png`) });
    console.log('✓ foto', s);
  }
  await browser.close(); process.exit(0);
}

const dur = await page.evaluate(() => window.DUR);
const salida = join(aqui, '..', 'albanileria-confinada-4x5.mp4');
const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida], { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round(dur * FPS);
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.render(t), f / FPS);
  const buf = await lienzo.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 90 === 0) console.log(`cuadro ${f}/${total}`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
// portada (cuadro final completo) para usar como miniatura
await page.evaluate(t => window.render(t), 28.4);
await lienzo.screenshot({ path: join(aqui, '..', 'albanileria-confinada-portada.jpg'), type: 'jpeg', quality: 92 });
await browser.close();
console.log('✓', salida);
