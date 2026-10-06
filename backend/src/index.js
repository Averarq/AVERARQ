// AVERARQ · Backend (Cloudflare Worker + KV, sin R2)
// ============================================================================
//  v8 · FUSIÓN TOTAL + ENLACE OBRA — 2026-10-06
//  Único archivo válido. Reúne, sin excepción:
//    · Portal de seguimiento con código del cliente y código secundario
//      para terceros (modo restringido: sin pagos, sin comprobantes).
//    · Calendario (feed ICS), PATCH de metadatos y PUT de archivo.
//    · Proyectos del GESTOR en la nube (gestor:*).
//    · Página /gestor servida por el propio Worker.
//    · Respaldo completo, registro del último respaldo y restauración.
//    · Enlace arquitectura ↔ obra: el portal del cliente muestra el estado
//      de pagos de sus obras del GESTOR, con lista blanca de campos.
//  Cualquier cambio futuro PARTE DE ESTE ARCHIVO. Desplegar una versión
//  que no incluya los dos lados vuelve a romper la mitad del sistema.
// ============================================================================
// Guarda TODOS los datos en la nube usando solo KV:
//   - estado global (proyectos, pagos, leads)
//   - documentos: metadatos + archivo (base64) en KV
//
// Límite por archivo: 25 MB (límite de un valor en KV). Suficiente para PDFs/imágenes.
//
// Rutas:
//   GET    /api/estado                -> estado completo (JSON)
//   PUT    /api/estado                -> guarda estado completo
//   GET    /api/documentos            -> lista metadatos (sin el archivo)
//   POST   /api/documentos            -> sube archivo (multipart/form-data)
//   GET    /api/documentos/:id/file   -> descarga el archivo
//   DELETE /api/documentos/:id        -> elimina metadato + archivo
//   GET    /api/respaldo[?docs=1]     -> respaldo completo en un JSON
//   GET/PUT /api/respaldo/registro    -> fecha del último respaldo (aviso de los viernes)
//   POST   /api/restaurar/documento   -> repone un documento con su id original
//   GET    /gestor                    -> la página del GESTOR (no es /api/)
//
// Auth: header  Authorization: Bearer <API_TOKEN>   (wrangler secret put API_TOKEN)

import GESTOR_HTML from "./gestor.html";

// Entrega el GESTOR inyectando el origen del propio Worker como URL de la nube
function servirGestor(origin) {
  const html = GESTOR_HTML.replace(
    "</head>",
    `<script>window.AVERARQ_NUBE_URL=${JSON.stringify(origin)};</script></head>`
  );
  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-cache",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}
function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: { "Content-Type": "application/json", ...corsHeaders(origin) },
  });
}
function authOk(request, env) {
  const auth = request.headers.get("Authorization") || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  return env.API_TOKEN && token === env.API_TOKEN;
}

// Convierte ArrayBuffer -> base64 (loop byte a byte, seguro en el runtime de CF)
function bufToBase64(buf) {
  const bytes = new Uint8Array(buf);
  let binary = "";
  const chunk = 8192;
  for (let i = 0; i < bytes.length; i += chunk) {
    const slice = bytes.subarray(i, Math.min(i + chunk, bytes.length));
    let s = "";
    for (let j = 0; j < slice.length; j++) s += String.fromCharCode(slice[j]);
    binary += s;
  }
  return btoa(binary);
}
function base64ToBytes(b64) {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

// Documentos del expediente D.O.M. (mismo catálogo que el organizador)
const DOM_DOCS_SRV = [
  { id: "listado", n: "0", label: "Listado de documentos" },
  { id: "form_minvu", n: "1", label: "Formulario de ingreso MINVU" },
  { id: "cip", n: "2", label: "Certificado de Informaciones Previas (CIP)" },
  { id: "decl_arq", n: "3", label: "Declaración profesional del arquitecto" },
  { id: "dominio", n: "4", label: "Antecedentes de la propiedad" },
  { id: "avaluo", n: "5", label: "Certificado de avalúo fiscal (SII)" },
  { id: "seim", n: "6", label: "Certificado SEIM para IMIV" },
  { id: "zonif", n: "7", label: "Certificado de zonificación" },
  { id: "accesib", n: "8", label: "Memoria de accesibilidad universal" },
  { id: "eett", n: "9", label: "Especificaciones técnicas" },
  { id: "ine", n: "10", label: "Certificado INE" },
  { id: "planim", n: "11", label: "Conjunto planimétrico" },
];
const PESO_PLANOS_SRV = 0.5;

// Avance ponderado 50/50 (documentos / planos), idéntico al organizador
function calcAvance(p) {
  const e = p.expediente || {};
  const lista = Array.isArray(e.docList)
    ? e.docList
    : DOM_DOCS_SRV.map((d) => ({ id: d.id, planim: d.id === "planim" }));

  let dTotal = 0, dHechos = 0;
  lista.forEach((d) => {
    if (d.planim || d.id === "planim") return;
    const it = e[d.id] || {};
    if (it.na) return;
    dTotal++;
    if (it.done) dHechos++;
  });
  const pl = e.planim || {};
  let pTotal = 0, pHechos = 0;
  const hayPlanim = lista.some((d) => d.planim || d.id === "planim");
  if (hayPlanim && !pl.na && Array.isArray(pl.subs)) {
    pl.subs.forEach((s) => { if (s.na) return; pTotal++; if (s.done) pHechos++; });
  }
  const docsPct = dTotal ? (dHechos / dTotal) * 100 : null;
  const planosPct = pTotal ? (pHechos / pTotal) * 100 : null;
  let pct;
  if (docsPct === null && planosPct === null) pct = 0;
  else if (docsPct === null) pct = planosPct;
  else if (planosPct === null) pct = docsPct;
  else pct = docsPct * (1 - PESO_PLANOS_SRV) + planosPct * PESO_PLANOS_SRV;
  return {
    pct: Math.round(pct),
    docsPct: docsPct === null ? null : Math.round(docsPct),
    planosPct: planosPct === null ? null : Math.round(planosPct),
    dTotal, dHechos, pTotal, pHechos,
  };
}

// Lista de estado del expediente apta para el cliente (sin notas internas)
function expedientePublico(p) {
  const e = p.expediente || {};
  // Si el proyecto tiene su propia lista (orden + docs custom), usarla; si no, el catálogo base
  const lista = Array.isArray(e.docList)
    ? e.docList
    : DOM_DOCS_SRV.map((d) => ({ id: d.id, label: d.label, planim: d.id === "planim" }));

  const docs = lista
    .filter((d) => !(d.planim || d.id === "planim"))
    .map((d) => {
      const it = e[d.id] || {};
      return { label: d.label, estado: it.na ? "na" : (it.done ? "ok" : "pend") };
    });

  const pl = e.planim || {};
  let planos = null;
  const hayPlanim = lista.some((d) => d.planim || d.id === "planim");
  if (hayPlanim && !pl.na && Array.isArray(pl.subs)) {
    planos = pl.subs.map((s) => ({
      label: s.label, estado: s.na ? "na" : (s.done ? "ok" : "pend"),
    }));
  }
  return { docs, planos };
}

// ---------------------------------------------------------------------------
//  RESUMEN DE OBRA PARA EL CLIENTE  (enlace ORGANIZADOR ↔ GESTOR)
//  Devuelve el consolidado de las obras del GESTOR cuyo mandante coincide.
//  REGLA INVIOLABLE: el registro "gestor:<id>" guarda el snapshot completo del
//  GESTOR —gastos, boletas, proveedores, utilidad, tarifas—. Aquí se arma un
//  objeto NUEVO campo por campo. Nunca se reenvía reg.data ni parte de él.
//  Si algún día hace falta un dato más, se agrega a esta lista a mano.
// ---------------------------------------------------------------------------
async function resumenObraCliente(env, cliente) {
  const objetivo = String(cliente || "").trim().toLowerCase();
  if (!objetivo) return null;
  const lista = await env.DOCS_KV.list({ prefix: "gestor:" });
  const obras = [];
  for (const k of lista.keys) {
    const raw = await env.DOCS_KV.get(k.name);
    if (!raw) continue;
    let reg;
    try { reg = JSON.parse(raw); } catch (e) { continue; }
    const d = reg && reg.data;
    if (!d) continue;
    const cli = ((d.obra && d.obra.info && d.obra.info.cliente) || "").trim().toLowerCase();
    if (cli !== objetivo) continue;

    const ctrl = d.control || {};
    const base = Number(ctrl.contrato) || 0;
    const adic = (Array.isArray(ctrl.adicionales) ? ctrl.adicionales : [])
      .reduce((acc, x) => acc + (Number(x.monto) || 0), 0);
    const contrato = base + adic;
    const abonado = Math.max(0, Number((d.planPago || {}).cobrado) || 0);
    if (contrato <= 0 && abonado <= 0) continue;   // obras sin montos no se muestran

    obras.push({
      nombre: d.proyecto || reg.nombre || "Obra",
      contrato: contrato,
      adicionales: adic,
      abonado: abonado,
      saldo: contrato - abonado,
      terminada: !!ctrl.terminado,
      actualizado: reg.actualizado || null,
    });
  }
  if (!obras.length) return null;
  obras.sort((a, b) =>
    String(a.nombre).localeCompare(String(b.nombre), "es", { numeric: true, sensitivity: "base" }));
  const t = obras.reduce(
    (a, o) => ({ contrato: a.contrato + o.contrato, abonado: a.abonado + o.abonado, saldo: a.saldo + o.saldo }),
    { contrato: 0, abonado: 0, saldo: 0 });
  return {
    obras: obras,
    contrato: t.contrato,
    abonado: t.abonado,
    saldo: t.saldo,
    pct: t.contrato > 0 ? Math.round((t.abonado / t.contrato) * 100) : 0,
    terminadas: obras.filter((o) => o.terminada).length,
    actualizado: obras.map((o) => o.actualizado).filter(Boolean).sort().pop() || null,
  };
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin");

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(origin) });
    }
    // ---------- GESTOR AVERARQ servido por el propio Worker ----------
    if (url.pathname === "/gestor" || url.pathname === "/gestor/") {
      if (request.method !== "GET") return json({ error: "method not allowed" }, 405, origin);
      return servirGestor(url.origin);
    }

    if (!url.pathname.startsWith("/api/")) {
      return json({ error: "not found" }, 404, origin);
    }

    const parts = url.pathname.split("/").filter(Boolean); // ["api", ...]

    // ============================================================
    //  RUTAS PÚBLICAS DE SEGUIMIENTO (portal del cliente)
    //  El código del proyecto ES la llave de acceso. No requieren token,
    //  pero SOLO exponen datos del proyecto correspondiente a ese código,
    //  y solo campos aptos para el cliente (nunca datos internos ni leads).
    // ============================================================
    if (parts[1] === "seguimiento") {
      try {
        const raw = await env.DOCS_KV.get("estado:global");
        const estado = raw ? JSON.parse(raw) : null;
        const proyectos = (estado && Array.isArray(estado.proyectos)) ? estado.proyectos : [];

        // GET /api/seguimiento/:codigo  -> datos filtrados del proyecto
        if (request.method === "GET" && parts.length === 3) {
          const codigo = String(parts[2] || "").toUpperCase().trim();
          if (!codigo) return json({ error: "Falta el código." }, 400, origin);

          // Puede entrar con el código del cliente (completo) o el secundario (restringido)
          let p = proyectos.find(
            (x) => (x.codigoCliente || "").toUpperCase() === codigo
          );
          let restringido = false;
          if (!p) {
            p = proyectos.find(
              (x) => x.codigoSecundarioOn && (x.codigoSecundario || "").toUpperCase() === codigo
            );
            if (p) restringido = true;
          }
          if (!p) {
            return json({ error: "No encontramos un proyecto con ese código." }, 404, origin);
          }

          // Documentos de ESTE proyecto (solo metadatos, nunca de otros).
          // En modo restringido se ocultan los comprobantes.
          const list = await env.DOCS_KV.list({ prefix: "docmeta:" });
          const docs = [];
          for (const k of list.keys) {
            const v = await env.DOCS_KV.get(k.name);
            if (!v) continue;
            const m = JSON.parse(v);
            if (m.proyectoId === p.id) {
              if (restringido && /comprobante/i.test(m.categoria || "")) continue;
              docs.push({
                id: m.id, nombre: m.nombre, categoria: m.categoria,
                fecha: m.fecha, size: m.size, type: m.type, fileName: m.fileName,
              });
            }
          }

          // Orden definido por el arquitecto desde el organizador
          const orden = (estado && estado.config && estado.config.ordenCliente) || "nombre-asc";
          docs.sort((a, b) => {
            if (orden === "nombre-asc") return (a.nombre || "").localeCompare(b.nombre || "", "es", { numeric: true });
            if (orden === "nombre-desc") return (b.nombre || "").localeCompare(a.nombre || "", "es", { numeric: true });
            if (orden === "fecha-asc") return (a.fecha || "").localeCompare(b.fecha || "");
            if (orden === "fecha-desc") return (b.fecha || "").localeCompare(a.fecha || "");
            return 0;
          });

          const avance = calcAvance(p);
          const pagos = (p.pagos || []).map((pg) => ({
            monto: pg.monto, fecha: pg.fecha, metodo: pg.metodo, nota: pg.nota || "",
          }));
          const totalAbonado = pagos.reduce((s, x) => s + Number(x.monto || 0), 0);

          // Cuotas futuras pactadas (visibles para el cliente)
          const cuotasFuturas = (p.cuotasFuturas || []).map((c) => ({
            monto: c.monto, fecha: c.fecha, nota: c.nota || "",
          })).sort((a, b) => (a.fecha || "").localeCompare(b.fecha || ""));

          const salida = {
            nombre: p.nombre,
            estado: p.estado,
            avance,
            documentos: docs,
            docOrden: p.docOrden || "nombre-asc",
            expediente: expedientePublico(p),
            restringido: restringido,
          };
          // Datos financieros SOLO para el cliente (código principal), nunca para terceros
          if (!restringido) {
            // Obra en ejecución: solo si el arquitecto activó el enlace en el
            // ORGANIZADOR. Lleva montos, así que queda fuera del modo restringido.
            if (p.obraOn && String(p.obraCliente || "").trim()) {
              const obra = await resumenObraCliente(env, p.obraCliente);
              if (obra) salida.obra = obra;
            }
            salida.total = p.total || 0;
            salida.totalAbonado = totalAbonado;
            salida.saldo = Math.max(0, (p.total || 0) - totalAbonado);
            salida.pagos = pagos;
            salida.cuotasFuturas = cuotasFuturas;
          }
          return json({ proyecto: salida }, 200, origin);
        }

        // GET /api/seguimiento/:codigo/documento/:docId  -> descarga
        if (request.method === "GET" && parts.length === 5 && parts[3] === "documento") {
          const codigo = String(parts[2] || "").toUpperCase().trim();
          const docId = parts[4];
          let p = proyectos.find(
            (x) => (x.codigoCliente || "").toUpperCase() === codigo
          );
          let restringido = false;
          if (!p) {
            p = proyectos.find(
              (x) => x.codigoSecundarioOn && (x.codigoSecundario || "").toUpperCase() === codigo
            );
            if (p) restringido = true;
          }
          if (!p) return json({ error: "Código no válido." }, 404, origin);

          const metaRaw = await env.DOCS_KV.get("docmeta:" + docId);
          if (!metaRaw) return json({ error: "Documento no encontrado." }, 404, origin);
          const meta = JSON.parse(metaRaw);
          // Verificación crítica: el documento debe pertenecer a ESTE proyecto
          if (meta.proyectoId !== p.id) {
            return json({ error: "Documento no disponible." }, 403, origin);
          }
          // En modo restringido, los comprobantes nunca se entregan
          if (restringido && /comprobante/i.test(meta.categoria || "")) {
            return json({ error: "Documento no disponible." }, 403, origin);
          }
          const b64 = await env.DOCS_KV.get("docfile:" + docId);
          if (!b64) return json({ error: "Archivo no encontrado." }, 404, origin);
          const bytes = base64ToBytes(b64);
          return new Response(bytes, {
            headers: {
              "Content-Type": meta.type,
              "Content-Disposition": `attachment; filename="${meta.fileName}"`,
              ...corsHeaders(origin),
            },
          });
        }

        return json({ error: "Ruta de seguimiento no válida." }, 404, origin);
      } catch (err) {
        return json({ error: String(err) }, 500, origin);
      }
    }

    if (!authOk(request, env)) {
      return json({ error: "No autorizado. Revisa el token de acceso." }, 401, origin);
    }

    try {
      // ---------- ESTADO COMPLETO ----------
      if (parts[1] === "estado") {
        if (request.method === "GET") {
          const raw = await env.DOCS_KV.get("estado:global");
          return json({ estado: raw ? JSON.parse(raw) : null }, 200, origin);
        }
        if (request.method === "PUT") {
          const body = await request.json();
          await env.DOCS_KV.put("estado:global", JSON.stringify(body));
          return json({ ok: true, savedAt: new Date().toISOString() }, 200, origin);
        }
      }

      // ---------- PROYECTOS DEL GESTOR (cubicaciones .avproj en la nube) ----------
      // Espacio propio, separado del organizador. Clave KV: "gestor:<id>"
      if (parts[1] === "gestor") {
        // GET /api/gestor -> lista de proyectos (metadatos, sin el cuerpo completo)
        if (request.method === "GET" && parts.length === 2) {
          const list = await env.DOCS_KV.list({ prefix: "gestor:" });
          const proyectos = [];
          for (const k of list.keys) {
            const v = await env.DOCS_KV.get(k.name);
            if (!v) continue;
            try {
              const p = JSON.parse(v);
              proyectos.push({
                id: k.name.slice("gestor:".length),
                nombre: p.nombre || "Proyecto sin título",
                actualizado: p.actualizado || null,
                version: p.version || null,
                // Mandante y estado: los usa el ORGANIZADOR para ofrecer la lista
                // de clientes al enlazar. Ruta con token, no la ve el cliente.
                cliente: (p.data && p.data.obra && p.data.obra.info && p.data.obra.info.cliente) || "",
                terminada: !!(p.data && p.data.control && p.data.control.terminado),
              });
            } catch (e) { /* ignora entradas corruptas */ }
          }
          proyectos.sort((a, b) => (b.actualizado || "").localeCompare(a.actualizado || ""));
          return json({ proyectos }, 200, origin);
        }
        // GET /api/gestor/:id -> trae un proyecto completo
        if (request.method === "GET" && parts.length === 3) {
          const raw = await env.DOCS_KV.get("gestor:" + parts[2]);
          if (!raw) return json({ error: "Proyecto no encontrado." }, 404, origin);
          return json({ proyecto: JSON.parse(raw) }, 200, origin);
        }
        // PUT /api/gestor/:id -> guarda/actualiza un proyecto
        if (request.method === "PUT" && parts.length === 3) {
          const body = await request.json();
          const registro = {
            id: parts[2],
            nombre: (body && body.nombre) || "Proyecto sin título",
            version: (body && body.version) || null,
            actualizado: new Date().toISOString(),
            data: (body && body.data) || null, // el snapshot() del GESTOR
          };
          if (!registro.data) return json({ error: "Falta el cuerpo del proyecto (data)." }, 400, origin);
          await env.DOCS_KV.put("gestor:" + parts[2], JSON.stringify(registro));
          return json({ ok: true, id: parts[2], actualizado: registro.actualizado }, 200, origin);
        }
        // DELETE /api/gestor/:id -> elimina un proyecto
        if (request.method === "DELETE" && parts.length === 3) {
          await env.DOCS_KV.delete("gestor:" + parts[2]);
          return json({ ok: true }, 200, origin);
        }
      }

      // ---------- CALENDARIO (feed ICS: dirección secreta o calendario público) ----------
      if (parts[1] === "calendario" && request.method === "GET") {
        const src = url.searchParams.get("src");
        const icsParam = url.searchParams.get("ics");

        let candidatos = [];
        if (icsParam) {
          // Dirección secreta: validamos que sea de Google (evita usar el Worker
          // como proxy hacia cualquier destino)
          let u;
          try {
            u = new URL(icsParam);
          } catch (e) {
            return json({ error: "La dirección del calendario no es una URL válida." }, 400, origin);
          }
          const hostOk =
            u.protocol === "https:" &&
            (u.hostname === "calendar.google.com" || u.hostname === "www.google.com");
          if (!hostOk) {
            return json({ error: "Solo se aceptan direcciones de Google Calendar." }, 400, origin);
          }
          candidatos = [icsParam];
        } else if (src) {
          const id = encodeURIComponent(src);
          candidatos = [
            "https://calendar.google.com/calendar/ical/" + id + "/public/basic.ics",
            "https://www.google.com/calendar/ical/" + id + "/public/basic.ics",
          ];
        } else {
          return json({ error: "Falta el calendario a consultar." }, 400, origin);
        }

        const intentos = [];
        for (const icsUrl of candidatos) {
          try {
            const r = await fetch(icsUrl, {
              headers: {
                "User-Agent":
                  "Mozilla/5.0 (compatible; AverarqOrganizador/1.0; +https://averarq.cl)",
                Accept: "text/calendar,text/plain,*/*",
              },
              redirect: "follow",
            });
            if (r.ok) {
              const text = await r.text();
              if (text.indexOf("BEGIN:VCALENDAR") >= 0) {
                return new Response(text, {
                  headers: {
                    "Content-Type": "text/calendar; charset=utf-8",
                    ...corsHeaders(origin),
                  },
                });
              }
              intentos.push({ status: r.status, nota: "sin datos de calendario" });
            } else {
              intentos.push({ status: r.status });
            }
          } catch (e) {
            intentos.push({ error: String(e) });
          }
        }
        return json(
          {
            error:
              "No se pudo leer el calendario. Si usas la dirección secreta, cópiala completa desde Google Calendar.",
            intentos,
          },
          502,
          origin
        );
      }

      // ---------- REGISTRO DEL ÚLTIMO RESPALDO ----------
      // GET  /api/respaldo/registro -> { registro: { fecha, equipo, archivos, bytes } | null }
      // PUT  /api/respaldo/registro -> lo graba (lo llama respaldar.mjs al terminar)
      if (parts[1] === "respaldo" && parts[2] === "registro") {
        if (request.method === "GET") {
          const raw = await env.DOCS_KV.get("respaldo:ultimo");
          return json({ registro: raw ? JSON.parse(raw) : null }, 200, origin);
        }
        if (request.method === "PUT") {
          const body = await request.json();
          const registro = {
            fecha: (body && body.fecha) || new Date().toISOString(),
            equipo: (body && body.equipo) || "",
            archivos: (body && body.archivos) || 0,
            bytes: (body && body.bytes) || 0,
            documentos: (body && body.documentos) || 0,
          };
          await env.DOCS_KV.put("respaldo:ultimo", JSON.stringify(registro));
          return json({ ok: true, registro }, 200, origin);
        }
      }

      // ---------- RESPALDO COMPLETO ----------
      // GET /api/respaldo        -> estado del organizador + proyectos del GESTOR + metadatos de documentos
      // GET /api/respaldo?docs=1 -> además el contenido de cada documento (base64)
      // El estado se copia TAL CUAL (bloque completo): así viajan también los campos
      // nuevos por proyecto —codigoSecundario, codigoSecundarioOn, cuotasFuturas,
      // docList— sin tener que enumerarlos aquí ni mantener esta lista al día.
      // Se escribe en streaming para no armar un texto gigante en memoria.
      if (parts[1] === "respaldo" && request.method === "GET") {
        const conDocs = url.searchParams.get("docs") === "1";
        const kv = env.DOCS_KV;
        const enc = new TextEncoder();
        const fecha = new Date().toISOString();
        const { readable, writable } = new TransformStream();
        const w = writable.getWriter();

        const escribir = (async () => {
          const push = (txt) => w.write(enc.encode(txt));
          try {
            await push(
              '{"_formato":"averarq-respaldo","_version":1,"_fecha":' +
                JSON.stringify(fecha) +
                ',"conDocumentos":' + (conDocs ? "true" : "false")
            );

            // Estado del organizador (proyectos, pagos, leads, configuración)
            const estadoRaw = await kv.get("estado:global");
            await push(',"estado":' + (estadoRaw || "null"));

            // Proyectos del GESTOR
            await push(',"gestor":[');
            const lg = await kv.list({ prefix: "gestor:" });
            let primero = true;
            for (const k of lg.keys) {
              const v = await kv.get(k.name);
              if (!v) continue;
              await push((primero ? "" : ",") + v);
              primero = false;
            }
            await push("]");

            // Documentos: metadatos siempre; contenido solo si se pidió.
            // La categoría se guarda textual (incluido "Comprobante"), de modo que
            // al restaurar el filtro del código secundario siga funcionando.
            await push(',"documentos":[');
            const ld = await kv.list({ prefix: "docmeta:" });
            primero = true;
            for (const k of ld.keys) {
              const metaRaw = await kv.get(k.name);
              if (!metaRaw) continue;
              const id = k.name.slice("docmeta:".length);
              let entrada = '{"meta":' + metaRaw;
              if (conDocs) {
                const b64 = await kv.get("docfile:" + id);
                if (b64) entrada += ',"b64":' + JSON.stringify(b64);
              }
              entrada += "}";
              await push((primero ? "" : ",") + entrada);
              primero = false;
            }
            await push("]}");
          } catch (e) {
            // El error queda dentro del propio archivo: el script lo detecta y no lo guarda
            try { await push(',"_error":' + JSON.stringify(String(e)) + "}"); } catch (e2) {}
          } finally {
            await w.close();
          }
        })();
        // Sin esto el runtime corta la petición al devolver la respuesta y el JSON llega truncado
        if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(escribir);

        const nombre = "averarq_respaldo_" + fecha.slice(0, 10) + (conDocs ? "_con_documentos" : "") + ".json";
        return new Response(readable, {
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Content-Disposition": 'attachment; filename="' + nombre + '"',
            "Cache-Control": "no-store",
            ...corsHeaders(origin),
          },
        });
      }

      // ---------- RESTAURAR UN DOCUMENTO (conservando su id original) ----------
      // POST /api/restaurar/documento  { meta: {...}, b64: "..." }
      // El metadato se repone literal, sin renombrar la categoría.
      if (parts[1] === "restaurar" && parts[2] === "documento" && request.method === "POST") {
        const body = await request.json();
        const meta = body && body.meta;
        const b64 = body && body.b64;
        if (!meta || !meta.id) return json({ error: "Falta el metadato del documento." }, 400, origin);
        if (b64) await env.DOCS_KV.put("docfile:" + meta.id, b64);
        await env.DOCS_KV.put("docmeta:" + meta.id, JSON.stringify(meta));
        return json({ ok: true, id: meta.id, conArchivo: !!b64 }, 200, origin);
      }

      // ---------- DOCUMENTOS ----------
      if (parts[1] === "documentos") {
        // GET /api/documentos  (lista de metadatos, sin archivo)
        if (request.method === "GET" && parts.length === 2) {
          const list = await env.DOCS_KV.list({ prefix: "docmeta:" });
          const items = await Promise.all(
            list.keys.map(async (k) => {
              const v = await env.DOCS_KV.get(k.name);
              return v ? JSON.parse(v) : null;
            })
          );
          return json({ documentos: items.filter(Boolean) }, 200, origin);
        }
        // POST /api/documentos  (subir)
        if (request.method === "POST" && parts.length === 2) {
          const form = await request.formData();
          const file = form.get("file");
          if (!file) return json({ error: "Falta el archivo." }, 400, origin);
          const buf = await file.arrayBuffer();
          if (buf.byteLength > 24 * 1024 * 1024) {
            return json({ error: "El archivo supera el límite de 24 MB." }, 413, origin);
          }
          const id = crypto.randomUUID();
          let b64;
          try {
            b64 = bufToBase64(buf);
          } catch (e) {
            return json({ error: "No se pudo procesar el archivo (base64): " + String(e) }, 500, origin);
          }
          const meta = {
            id,
            nombre: form.get("nombre") || file.name,
            categoria: form.get("categoria") || "",
            proyectoId: form.get("proyectoId") || "",
            proyectoNombre: form.get("proyectoNombre") || "",
            fecha: new Date().toISOString().slice(0, 10),
            size: buf.byteLength,
            type: file.type || "application/octet-stream",
            fileName: file.name,
          };
          try {
            await env.DOCS_KV.put("docfile:" + id, b64);
            await env.DOCS_KV.put("docmeta:" + id, JSON.stringify(meta));
          } catch (e) {
            return json({ error: "No se pudo guardar en KV: " + String(e) }, 500, origin);
          }
          return json({ documento: meta }, 201, origin);
        }
        // GET /api/documentos/:id/file  (descargar)
        if (request.method === "GET" && parts.length === 4 && parts[3] === "file") {
          const raw = await env.DOCS_KV.get("docmeta:" + parts[2]);
          if (!raw) return json({ error: "No encontrado." }, 404, origin);
          const meta = JSON.parse(raw);
          const b64 = await env.DOCS_KV.get("docfile:" + parts[2]);
          if (!b64) return json({ error: "Archivo no encontrado." }, 404, origin);
          const bytes = base64ToBytes(b64);
          return new Response(bytes, {
            headers: {
              "Content-Type": meta.type,
              "Content-Disposition": `attachment; filename="${meta.fileName}"`,
              ...corsHeaders(origin),
            },
          });
        }
        // PUT /api/documentos/:id/file  (reemplazar el archivo, conservando metadatos)
        if (request.method === "PUT" && parts.length === 4 && parts[3] === "file") {
          const raw = await env.DOCS_KV.get("docmeta:" + parts[2]);
          if (!raw) return json({ error: "Documento no encontrado." }, 404, origin);
          const meta = JSON.parse(raw);
          const form = await request.formData();
          const file = form.get("file");
          if (!file) return json({ error: "Falta el archivo." }, 400, origin);
          const buf = await file.arrayBuffer();
          if (buf.byteLength > 24 * 1024 * 1024) {
            return json({ error: "El archivo supera el límite de 24 MB." }, 413, origin);
          }
          let b64;
          try {
            b64 = bufToBase64(buf);
          } catch (e) {
            return json({ error: "No se pudo procesar el archivo (base64): " + String(e) }, 500, origin);
          }
          // Se conservan id, nombre, categoría y proyecto; se actualiza el archivo
          meta.size = buf.byteLength;
          meta.type = file.type || "application/octet-stream";
          meta.fileName = file.name;
          meta.fecha = new Date().toISOString().slice(0, 10);
          try {
            await env.DOCS_KV.put("docfile:" + parts[2], b64);
            await env.DOCS_KV.put("docmeta:" + parts[2], JSON.stringify(meta));
          } catch (e) {
            return json({ error: "No se pudo guardar en KV: " + String(e) }, 500, origin);
          }
          return json({ documento: meta }, 200, origin);
        }
        // PATCH /api/documentos/:id  -> editar nombre/categoría (sin resubir archivo)
        if (request.method === "PATCH" && parts.length === 3) {
          const raw = await env.DOCS_KV.get("docmeta:" + parts[2]);
          if (!raw) return json({ error: "Documento no encontrado." }, 404, origin);
          const meta = JSON.parse(raw);
          const body = await request.json().catch(() => ({}));
          if (typeof body.nombre === "string" && body.nombre.trim()) meta.nombre = body.nombre.trim();
          if (typeof body.categoria === "string") meta.categoria = body.categoria;
          await env.DOCS_KV.put("docmeta:" + parts[2], JSON.stringify(meta));
          return json({ documento: meta }, 200, origin);
        }
        // DELETE /api/documentos/:id
        if (request.method === "DELETE" && parts.length === 3) {
          await env.DOCS_KV.delete("docmeta:" + parts[2]);
          await env.DOCS_KV.delete("docfile:" + parts[2]);
          return json({ ok: true }, 200, origin);
        }
      }

      return json({ error: "Ruta no soportada." }, 404, origin);
    } catch (err) {
      return json({ error: String(err) }, 500, origin);
    }
  },
};
