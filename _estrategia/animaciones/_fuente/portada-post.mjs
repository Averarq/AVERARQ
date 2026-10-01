// portada-post.mjs — imagen fija de portada para el post (4:5), a 2160 × 2700 y 1080 × 1350.
// Uso: node portada-post.mjs [pieza] [reel]   (la pieza debe definir window.renderPortada)
//   con 'reel' sale en 9:16 (1080 × 1920 y 2160 × 3840) para la portada de un reel
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const PIEZA = process.argv[2] || 'albanileria-confinada';
const REEL = process.argv[3] === 'reel', HH = REEL ? 1920 : 1350;
const browser = await pw.chromium.launch();
for (const S of [2, 1]) {
  const page = await browser.newPage({ viewport: { width: 1080 * S, height: HH * S } });
  await page.goto(pathToFileURL(join(aqui, `${PIEZA}.html`)).href + `?escala=${S}${REEL ? '&formato=reel' : ''}`);
  await page.evaluate(() => window.ready);
  await page.evaluate(() => window.renderPortada());
  const out = join(aqui, '..', `${PIEZA}-${REEL ? 'reel' : 'post'}-portada${S > 1 ? '-2160' : ''}.jpg`);
  await (await page.$('canvas')).screenshot({ path: out, type: 'jpeg', quality: 95 });
  console.log('✓', out);
  await page.close();
}
await browser.close();
