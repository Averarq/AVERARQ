// render.mjs — convierte los HTML de _fuente/html/ en JPG listos para Meta (../piezas/).
// Uso: node render.mjs   (requiere Playwright; en el entorno de Claude se resuelve solo)
import { readFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execSync } from 'node:child_process';

const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }

const salida = join(aqui, '..', 'piezas');
mkdirSync(salida, { recursive: true });
const lista = readFileSync(join(aqui, 'html', '_lista.txt'), 'utf8').trim().split('\n').map(l => l.split(' '));

const browser = await pw.chromium.launch();
for (const [nombre, w, h] of lista) {
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(join(aqui, 'html', nombre + '.html')).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(salida, nombre + '.jpg'), type: 'jpeg', quality: 92 });
  await page.close();
  console.log('✓', nombre);
}
await browser.close();
