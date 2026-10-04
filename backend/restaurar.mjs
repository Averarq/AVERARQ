#!/usr/bin/env node
// AVERARQ · Restaurar la nube desde un respaldo
//
//   node restaurar.mjs ..\respaldos\2026-09-28
//   node restaurar.mjs <carpeta> --solo-gestor | --solo-organizador | --sin-documentos | --si
//
// Sobrescribe en la nube lo que traiga el respaldo, conservando los identificadores.
// No borra lo que se haya creado después y no esté en el respaldo.

import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { dirname, join, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline/promises";

const AQUI = dirname(fileURLToPath(import.meta.url));

function config() {
  let c = {};
  try { c = JSON.parse(readFileSync(join(AQUI, "respaldo.config.json"), "utf8")); } catch {}
  const url = (process.env.AVERARQ_URL || c.url || "").replace(/\/$/, "");
  const token = process.env.AVERARQ_TOKEN || c.token || "";
  if (!url || !token) { console.error("Falta respaldo.config.json (url y token)."); process.exit(1); }
  return { url, token };
}

function ubicarDatos(ruta) {
  if (existsSync(ruta) && statSync(ruta).isDirectory()) {
    const p = join(ruta, "datos.json");
    if (existsSync(p)) return { datos: p, raiz: dirname(ruta) };
    console.error("Esa carpeta no tiene datos.json."); process.exit(1);
  }
  if (existsSync(ruta)) return { datos: ruta, raiz: dirname(dirname(ruta)) };
  console.error("No encuentro " + ruta); process.exit(1);
}

async function main() {
  const arg = process.argv[2];
  if (!arg || arg.startsWith("--")) {
    console.error("Uso: node restaurar.mjs <carpeta del respaldo> [--solo-gestor|--solo-organizador] [--sin-documentos] [--si]");
    process.exit(1);
  }
  const soloGestor = process.argv.includes("--solo-gestor");
  const soloOrg = process.argv.includes("--solo-organizador");
  const sinDocs = process.argv.includes("--sin-documentos") || soloGestor || soloOrg;
  const { url, token } = config();
  const head = { Authorization: "Bearer " + token, "Content-Type": "application/json" };

  const { datos: rutaDatos, raiz } = ubicarDatos(arg);
  const datos = JSON.parse(readFileSync(rutaDatos, "utf8"));
  if (datos._formato !== "averarq-respaldo") { console.error("Ese archivo no es un respaldo AVERARQ."); process.exit(1); }
  const POOL = join(raiz, "documentos");

  const gestor = Array.isArray(datos.gestor) ? datos.gestor : [];
  const metas = (datos.documentos || []).map(d => d.meta || d).filter(m => m && m.id);
  const archivoDe = (id) => {
    if (!existsSync(POOL)) return null;
    const f = readdirSync(POOL).find(n => n.split("__")[0] === id);
    return f ? join(POOL, f) : null;
  };
  const conArchivo = metas.filter(m => archivoDe(m.id));

  console.log(`Respaldo del ${(datos._fecha || "").slice(0, 10)} · destino ${url}`);
  console.log(`  organizador  ${datos.estado ? "sí" : "no hay"}`);
  console.log(`  gestor       ${gestor.length} cubicación(es)`);
  console.log(`  documentos   ${conArchivo.length} con archivo, de ${metas.length}`);
  console.log("Sobrescribe lo que venga en el respaldo. No borra lo que se haya creado después.");

  if (!process.argv.includes("--si")) {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const resp = (await rl.question("¿Restaurar? (escribe SI) ")).trim();
    rl.close();
    if (resp.toUpperCase() !== "SI") { console.log("Cancelado."); process.exit(0); }
  }

  let ok = 0, fallos = 0;
  const enviar = async (ruta, cuerpo, etiqueta, metodo) => {
    try {
      const r = await fetch(url + ruta, { method: metodo || "PUT", headers: head, body: JSON.stringify(cuerpo) });
      if (!r.ok) throw new Error("HTTP " + r.status);
      ok++; console.log("  ✓ " + etiqueta);
    } catch (e) { fallos++; console.log("  ✗ " + etiqueta + " — " + e.message); }
  };

  if (datos.estado && !soloGestor) await enviar("/api/estado", datos.estado, "estado del organizador");
  if (!soloOrg) for (const p of gestor) {
    if (!p || !p.id || !p.data) continue;
    await enviar("/api/gestor/" + encodeURIComponent(p.id), { nombre: p.nombre, version: p.version, data: p.data }, "gestor: " + (p.nombre || p.id));
  }
  if (!sinDocs) for (const m of metas) {
    const f = archivoDe(m.id);
    if (!f) { console.log("  · " + (m.nombre || m.id) + " — sin archivo en el respaldo, se omite"); continue; }
    const b64 = readFileSync(f).toString("base64");
    await enviar("/api/restaurar/documento", { meta: m, b64 }, "documento: " + (m.nombre || basename(f)), "POST");
  }
  console.log(`\nListo: ${ok} restaurado(s)${fallos ? ", " + fallos + " con error" : ""}.`);
  if (fallos) process.exit(1);
}
main().catch(e => { console.error("No se pudo restaurar: " + e.message); process.exit(1); });
