// bocetos.mjs — fotogramas fijos de bocetos.html: node bocetos.mjs 4 5 6 7 [--escala 2]
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const args = process.argv.slice(2), iE = args.indexOf('--escala'), S = iE >= 0 ? +args[iE + 1] : 1;
const dets = args.filter((v, i) => /^\d+$/.test(v) && args[i - 1] !== '--escala');
const browser = await pw.chromium.launch();
for (const d of dets) {
  const page = await browser.newPage({ viewport: { width: 1080 * S, height: 1350 * S }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[det', d + ']', m.text()));
  await page.goto(pathToFileURL(join(aqui, 'bocetos.html')).href + `?escala=${S}&det=${d}`);
  await page.evaluate(() => window.ready);
  await (await page.$('canvas')).screenshot({ path: join(aqui, `foto-boceto-det0${d}.png`) });
  console.log('✓ DET.', d);
  await page.close();
}
await browser.close();
