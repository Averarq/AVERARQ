import { execSync } from 'node:child_process'; import { dirname, join } from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = dirname(fileURLToPath(import.meta.url)); let pw;
try { pw = await import('playwright'); } catch { pw = await import(pathToFileURL(join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')).href); }
const b = await pw.chromium.launch(), p = await b.newPage({ viewport: { width: 1400, height: 900 } });
p.on('pageerror', e => console.error(e.message));
await p.goto(pathToFileURL(join(aqui, 'vista.html')).href); await p.screenshot({ path: process.argv[2] }); await b.close();
