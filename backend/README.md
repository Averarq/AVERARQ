# AVERARQ · Backend completo (datos en la nube)

Este backend guarda **todos** los datos del Organizador en la nube: proyectos,
pagos, leads de captación y documentos. Así puedes abrir el organizador desde
tu notebook, tu celular o cualquier dispositivo y ver siempre lo mismo.

Es gratis para tu volumen de uso (Cloudflare free tier).

## Requisitos (una sola vez)
- Cuenta gratis en Cloudflare (la misma del DNS de averarq.cl)
- Node.js instalado en tu computador

## Instalación paso a paso

Abre una terminal dentro de esta carpeta (`worker/`) y ejecuta en orden:

### 1. Iniciar sesión
```
npx wrangler login
```

### 2. Crear el almacenamiento de archivos (R2)
```
npx wrangler r2 bucket create averarq-documentos
```

### 3. Crear el espacio de datos (KV)
```
npx wrangler kv namespace create DOCS_KV
```
Copia el `id` que te muestra y pégalo en `wrangler.toml`
(reemplaza `REEMPLAZAR_CON_TU_KV_ID`).

### 4. Definir tu token de acceso
```
npx wrangler secret put API_TOKEN
```
Cuando te lo pida, escribe una clave larga e inventada por ti. Esta es la que
vas a pegar en el organizador (campo "Token de acceso").

### 5. Publicar
```
npx wrangler deploy
```
Te entrega una URL tipo:
```
https://averarq-backend.TU-USUARIO.workers.dev
```

### 6. (Opcional) Dominio propio
En Cloudflare → Workers & Pages → tu Worker → Settings → Domains & Routes,
agrega `docs.averarq.cl/*`. Así usas `https://docs.averarq.cl` como URL.

## Conectar el organizador

1. Abre el organizador (averarq.cl/organizador/), entra con tu clave.
2. Ve a la pestaña "📁 Documentos".
3. Pega la URL del Worker (paso 5) y el token (paso 4). Clic en "Conectar".
4. Listo. Desde ese momento:
   - El puntito junto al título se pone **verde** = conectado a la nube.
   - Todo lo que edites se guarda automáticamente en la nube.
   - En cualquier otro dispositivo, repites el paso 3 (misma URL y token) y
     verás los mismos datos.

## Cómo saber si está guardando
El puntito de color junto a "CAPTACIÓN · PROYECTOS · PAGOS":
- **Gris** = modo local (sin nube)
- **Verde** = conectado y guardado
- **Amarillo** = sincronizando
- **Rojo** = error de conexión (revisa URL/token o tu internet)

## Importante
- Es modo "un solo usuario". Si dos personas editan a la vez desde dos
  dispositivos, gana el último que guardó. Para tu uso individual está perfecto.
- El respaldo "Exportar" del organizador sigue funcionando como copia de
  seguridad extra.

## Costos (free tier de Cloudflare)
- R2: 10 GB gratis/mes
- Workers: 100.000 solicitudes/día gratis
- KV: 100.000 lecturas/día gratis

## Actualizar el backend más adelante
```
npx wrangler deploy
```
No necesitas repetir los pasos 1-4.
