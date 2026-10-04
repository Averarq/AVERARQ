#!/usr/bin/env node
// AVERARQ · Respaldo de la nube (organizador + gestor + documentos)
//
//   node respaldar.mjs              -> datos + documentos nuevos
//   node respaldar.mjs --sin-docs   -> solo datos (rápido)
//
// Estructura que deja en 0.AV\respaldos:
//   2026-09-28\datos.json     estado del organizador, cubicaciones del gestor y metadatos
//   documentos\<id>__<archivo>   archivos reales, compartidos entre respaldos (no se bajan dos veces)
//
// Configuración: respaldo.config.json junto a este archivo
//   { "url": "...", "token": "...", "guardar": 12 }

import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, statSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { hostname } from "node:os";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..", "respaldos");
const POOL = join(RAIZ, "documentos");

function config() {
  let c = {};
  try { c = JSON.parse(readFileSync(join(AQUI, "respaldo.config.json"), "utf8")); } catch {}
  const url = (process.env.AVERARQ_URL || c.url || "").replace(/\/$/, "");
  const token = process.env.AVERARQ_TOKEN || c.token || "";
  if (!url || !token) {
    console.error("Falta la configuración. Copia respaldo.config.example.json a respaldo.config.json");
    console.error("y pon la URL del Worker y el token (el mismo del ORGANIZADOR).");
    process.exit(1);
  }
  return { url, token, guardar: Number(c.guardar) > 0 ? Number(c.guardar) : 12 };
}

const mb = (n) => (n < 1048576 ? (n / 1024).toFixed(0) + " KB" : (n / 1048576).toFixed(1) + " MB");
const limpio = (s) => String(s || "archivo").replace(/[^\w.\- ]+/g, "_").slice(0, 80);

async function main() {
  const { url, token, guardar } = config();
  const head = { Authorization: "Bearer " + token };
  const conDocs = !process.argv.includes("--sin-docs");

  // 1. Datos (liviano): organizador + gestor + metadatos de documentos
  process.stdout.write("Bajando datos de " + url + " ... ");
  const r = await fetch(url + "/api/respaldo", { headers: head });
  if (r.status === 401) { console.error("\nToken incorrecto."); process.exit(1); }
  if (!r.ok) { console.error(`\nEl servidor respondió ${r.status}.`); process.exit(1); }
  const texto = await r.text();
  let datos;
  try { datos = JSON.parse(texto); }
  catch {
    console.error("\nLa respuesta llegó incompleta o no es JSON. Si acabas de cambiar el Worker,");
    console.error("vuelve a desplegarlo (npx wrangler deploy) y reintenta. No se guardó nada.");
    process.exit(1);
  }
  if (datos._formato !== "averarq-respaldo") { console.error("\nFormato inesperado."); process.exit(1); }
  if (datos._error) { console.error("\nEl respaldo llegó con error: " + datos._error); process.exit(1); }

  const fecha = new Date().toISOString().slice(0, 10);
  const carpeta = join(RAIZ, fecha);
  mkdirSync(carpeta, { recursive: true });
  writeFileSync(join(carpeta, "datos.json"), texto, "utf8");
  console.log("listo.");

  const gestor = Array.isArray(datos.gestor) ? datos.gestor : [];
  const docs = Array.isArray(datos.documentos) ? datos.documentos.map(d => d.meta || d) : [];
  const org = datos.estado || {};
  console.log(`  organizador  ${(org.proyectos || []).length} proyecto(s) · ${(org.leads || []).length} lead(s)`);
  console.log(`  gestor       ${gestor.length} cubicación(es)`);

  // 2. Documentos: solo los que aún no están en el pool (o cambiaron de tamaño)
  let bajados = 0, saltados = 0, fallos = 0, bytes = 0;
  if (conDocs && docs.length) {
    mkdirSync(POOL, { recursive: true });
    console.log(`  documentos   ${docs.length} en la nube; bajando los que falten...`);
    for (const m of docs) {
      if (!m || !m.id) continue;
      const destino = join(POOL, `${m.id}__${limpio(m.fileName || m.nombre)}`);
      if (existsSync(destino) && (!m.size || statSync(destino).size === Number(m.size))) { saltados++; continue; }
      try {
        const rd = await fetch(`${url}/api/documentos/${encodeURIComponent(m.id)}/file`, { headers: head });
        if (!rd.ok) throw new Error("HTTP " + rd.status);
        const buf = Buffer.from(await rd.arrayBuffer());
        writeFileSync(destino, buf);
        bajados++; bytes += buf.length;
        process.stdout.write(`\r    ${bajados} bajado(s), ${saltados} ya estaban${fallos ? ", " + fallos + " con error" : ""}   `);
      } catch (e) {
        fallos++;
        console.log(`\n    ✗ ${m.nombre || m.id}: ${e.message}`);
      }
    }
    console.log(`\r    ${bajados} bajado(s) (${mb(bytes)}), ${saltados} ya estaban${fallos ? ", " + fallos + " con error" : ""}      `);
  } else if (!conDocs) {
    console.log(`  documentos   ${docs.length} (solo metadatos; no se bajaron archivos)`);
  }

  // 3. Rotación: deja las últimas N carpetas de datos
  const carpetas = readdirSync(RAIZ, { withFileTypes: true })
    .filter(d => d.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(d.name))
    .map(d => d.name).sort();
  for (const c of carpetas.slice(0, Math.max(0, carpetas.length - guardar))) {
    rmSync(join(RAIZ, c), { recursive: true, force: true });
    console.log(`  (se eliminó el respaldo antiguo ${c})`);
  }
  // Limpia del pool los archivos que ya no menciona ningún respaldo vigente
  if (existsSync(POOL)) {
    const vivos = new Set();
    for (const c of readdirSync(RAIZ).filter(n => /^\d{4}-\d{2}-\d{2}$/.test(n))) {
      try {
        const d = JSON.parse(readFileSync(join(RAIZ, c, "datos.json"), "utf8"));
        for (const x of d.documentos || []) { const m = x.meta || x; if (m && m.id) vivos.add(m.id); }
      } catch {}
    }
    for (const f of readdirSync(POOL)) {
      const id = f.split("__")[0];
      if (!vivos.has(id)) { rmSync(join(POOL, f), { force: true }); console.log(`  (documento fuera de uso eliminado: ${f})`); }
    }
  }

  // 4. Deja registrado el respaldo en la nube (para el aviso del organizador y el gestor)
  try {
    const total = tamañoDe(carpeta) + (conDocs ? tamañoDe(POOL) : 0);
    const res = await fetch(url + "/api/respaldo/registro", {
      method: "PUT",
      headers: { ...head, "Content-Type": "application/json" },
      body: JSON.stringify({ fecha: new Date().toISOString(), equipo: hostname(), archivos: gestor.length, documentos: conDocs ? docs.length : 0, bytes: total }),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    console.log("  registro     anotado en la nube (el aviso de respaldo se reinicia)");
  } catch (e) {
    console.log("  registro     no se pudo anotar en la nube (" + e.message + "); el respaldo sí quedó guardado");
  }

  console.log(`\nGuardado en ${carpeta}`);
  if (fallos) process.exit(1);
}

function tamañoDe(dir) {
  let n = 0;
  try { for (const f of readdirSync(dir)) { const p = join(dir, f); const st = statSync(p); n += st.isDirectory() ? tamañoDe(p) : st.size; } } catch {}
  return n;
}

main().catch(e => { console.error("\nNo se pudo respaldar: " + e.message); process.exit(1); });
