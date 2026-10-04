// generar.mjs — exporta el carrusel (5 láminas 4:5) y la historia (9:16): node generar.mjs → ../*.jpg (1080 y 2160)
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const b = await pw.chromium.launch();
for (const sl of ['1', '2', '3', '4', '5', 'h', 'r']) for (const S of [1, 2]) {
  const H = 'hr'.includes(sl) ? 1920 : 1350, p = await b.newPage({ viewport: { width: 1080 * S, height: H * S } });
  await p.goto(pathToFileURL(join(aqui, 'carrusel.html')).href + `?slide=${sl}&escala=${S}`);
  await p.evaluate(() => window.ready);
  const n = sl === 'h' ? 'historia' : sl === 'r' ? 'historia-registro' : `carrusel-0${sl}`;
  await (await p.$('canvas')).screenshot({ path: join(aqui, '..', `${n}${S > 1 ? '-2160' : ''}.jpg`), type: 'jpeg', quality: 95 });
  await p.close();
}
await b.close();
