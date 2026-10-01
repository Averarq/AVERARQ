// portada-compilado.mjs — portada del reel compilado del café: node portada-compilado.mjs → ../cafe-metodos-{reel,post}-portada[-2160].jpg
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const browser = await pw.chromium.launch();
for (const [fmt, H] of [['reel', 1920], ['post', 1350]]) for (const S of [1, 2]) {
  const page = await browser.newPage({ viewport: { width: 1080 * S, height: H * S } });
  await page.goto(pathToFileURL(join(aqui, 'portada-compilado.html')).href + `?formato=${fmt}&escala=${S}`);
  await page.evaluate(() => window.ready);
  await (await page.$('canvas')).screenshot({ path: join(aqui, '..', `cafe-metodos-${fmt}-portada${S > 1 ? '-2160' : ''}.jpg`), type: 'jpeg', quality: 95 });
  await page.close();
}
await browser.close();
