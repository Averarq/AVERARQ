// generar.mjs — exporta el carrusel de accesibilidad (9 láminas 4:5): node generar.mjs [escala] → ../AV_ACC_0N.png (y -2160 con escala 2)
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url));
let pw;
try { pw = await import('playwright'); }
catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const escalas = process.argv[2] ? [+process.argv[2]] : [1, 2];
const b = await pw.chromium.launch();
for (let sl = 1; sl <= 9; sl++) for (const S of escalas) {
  const p = await b.newPage({ viewport: { width: 1080 * S, height: 1350 * S } });
  p.on('pageerror', e => console.error(sl, e.message));
  await p.goto(pathToFileURL(join(aqui, 'carrusel.html')).href + `?slide=${sl}&escala=${S}`);
  await p.evaluate(() => window.ready);
  await (await p.$('canvas')).screenshot({ path: join(aqui, '..', `AV_ACC_0${sl}${S > 1 ? '-2160' : ''}.png`) });
  await p.close();
}
await b.close();
