# AVERARQ · Respaldos de la nube

La nube (Cloudflare KV) **no guarda versiones ni papelera**: si algo se borra ahí, se
perdió. Estos dos scripts bajan todo a tu computador y permiten devolverlo.

## Qué se respalda

```
0.AV\respaldos\
  2026-09-28\datos.json        organizador + cubicaciones del gestor + metadatos
  2026-10-05\datos.json
  documentos\<id>__<archivo>   los archivos reales, compartidos entre respaldos
```

- **Organizador**: proyectos, pagos, cuotas, leads y configuración (`estado:global`).
- **GESTOR**: todas las cubicaciones sincronizadas (`gestor:<id>`), con su estado completo.
- **Documentos**: los archivos se guardan una sola vez en `documentos\` y los respaldos
  siguientes solo bajan los nuevos. Cuando un respaldo antiguo se elimina por rotación,
  los archivos que ya nadie menciona se borran del pool.

No incluye el PDF de fondo de una cubicación: el GESTOR nunca lo sube, solo guarda su nombre.

Al terminar, el script anota la fecha en la nube (`/api/respaldo/registro`). Con eso el
ORGANIZADOR y el GESTOR muestran **cuántos días llevas sin respaldar** y avisan los viernes.

## Configuración (una sola vez)

1. Copia `respaldo.config.example.json` a **`respaldo.config.json`**.
2. Pon la URL del Worker y el token (el mismo del ORGANIZADOR).
3. `guardar` es cuántos respaldos se conservan; el resto se borra solo.

Ese archivo tiene el token: no lo subas a GitHub ni lo compartas.

## Respaldar

```
cd "C:\Users\Alejandro Vera\Documents\0.AVERARQ\0.WEB\0.AV\averarq-backend"
node respaldar.mjs
```

Los archivos quedan en **`0.AV\respaldos\`**, en una carpeta por fecha. Con `--sin-docs`
baja solo los datos, sin tocar los documentos (toma segundos).

### Dejarlo semanal (lunes 9:00)

En PowerShell, una vez:

```
schtasks /create /tn "Respaldo AVERARQ" /sc weekly /d MON /st 09:00 ^
  /tr "node \"C:\Users\Alejandro Vera\Documents\0.AVERARQ\0.WEB\0.AV\averarq-backend\respaldar.mjs\""
```

Se revisa o se borra desde el Programador de tareas de Windows. Corre solo si el
computador está encendido; si estuvo apagado, Windows lo ejecuta al volver.

## Restaurar

```
node restaurar.mjs ..\respaldos\2026-09-28
```

Pide confirmación escribiendo `SI`. Opciones:

- `--solo-gestor` — solo las cubicaciones.
- `--solo-organizador` — solo proyectos, pagos y leads.
- `--sin-documentos` — omite los archivos.
- `--si` — sin preguntar (para automatizar).

**Qué hace exactamente:** sobrescribe en la nube lo que venga en el respaldo, conservando
los mismos identificadores (un documento restaurado mantiene su id, así los pagos siguen
apuntando a su comprobante). **No borra** lo que se haya creado después y no esté en el
archivo. Si quieres dejar la nube exactamente como el respaldo, borra antes lo sobrante
desde el organizador o el gestor.

Después de restaurar, en cada navegador conviene pulsar "Sincronizar ahora" en el GESTOR
y recargar el ORGANIZADOR.

## Límites y cuidados

- Un valor en KV admite hasta 25 MB, así que un documento más pesado que eso nunca entró
  a la nube y tampoco estará en el respaldo.
- El primer respaldo baja todos los documentos (hoy son 113, unos 180 MB) y puede demorar
  varios minutos. Los siguientes solo bajan lo nuevo.
- El archivo de respaldo contiene **todo en claro**, incluidos los documentos de clientes.
  Guárdalo donde guardas el resto del material de la oficina, no en carpetas compartidas.
- El respaldo se baja con el token: quien tenga el token puede bajarlo todo. Si alguna vez
  se filtra, cámbialo con `npx wrangler secret put API_TOKEN` y vuelve a conectarlo en el
  ORGANIZADOR y en el GESTOR.
