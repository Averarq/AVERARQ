# AVERARQ — Anuncios Meta Ads, lote 1 (octubre 2026)

Hay 30 piezas listas para subir en `piezas/`, y `vista-general.jpg` las muestra todas en una sola imagen. Están hechas con la identidad del sitio (naranjo #FC4C02, Barlow / Barlow Condensed, isotipo) y con proyectos y fotos de obra reales de averarq.cl. Corresponden a las campañas del plan (`../plan-marca-meta-ads-2026.md`, §4).

**Formatos**
- Feed 4:5, de 1080×1350.
- Historias y reels 9:16, de 1080×1920. Los bordes superior (250 px) e inferior (340 px) quedan libres para la interfaz de Instagram.
- Carrusel 1:1, de 1080×1080.

**Regla de oro al subir:** en cada anuncio, asigna la versión *feed* a Feeds y la versión *story* a Historias y Reels usando "Personalizar recurso por ubicación". Así Meta no recorta.

---

## Destinos y códigos de seguimiento

| Código | Destino | Mensaje de bienvenida en WhatsApp (se configura en el anuncio) |
|---|---|---|
| `REG1` | WhatsApp +56 9 5431 7945 | Hola Averarq, vi su anuncio y quiero regularizar mi casa [REG1] |
| `REG2` | WhatsApp | Hola Averarq, quiero saber si mi casa califica para la Ley del Mono [REG2] |
| `REG3` | WhatsApp | Hola Averarq, voy a vender o pedir un crédito y necesito la recepción final [REG3] |
| `CASA1` | WhatsApp | Hola Averarq, tengo una parcela y quiero diseñar mi casa [CASA1] |
| `CASA2` | `https://averarq.cl/?utm_source=meta&utm_medium=paid&utm_campaign=AVQ_CASA&utm_content=B2#cotizador` | — (sitio web, estimador) |
| `CASA3` | WhatsApp | Hola Averarq, vi las 5 cosas para construir en mi parcela y quiero conversar [CASA3] |
| `CASA4` | WhatsApp | Hola Averarq, vi sus proyectos del valle y quiero conversar el mío [CASA4] |
| `COM1` | WhatsApp | Hola Averarq, tengo un local y necesito permisos / remodelación [COM1] |
| `COM2` | WhatsApp | Hola Averarq, me piden recepción final para la patente [COM2] |
| `MARCA` | Instagram @averarq o WhatsApp | Hola Averarq, quiero conversar un proyecto [MARCA] |
| `VCASA` | WhatsApp | Hola Averarq, vi el video de la casa en Catemu y tengo una parcela [VCASA] |
| `VREG` | WhatsApp | Hola Averarq, vi el video y quiero regularizar mi casa [VREG] |
| `VCALC` | `https://averarq.cl/?utm_source=meta&utm_medium=paid&utm_campaign=AVQ_CASA&utm_content=V3#cotizador` | — (sitio web, estimador) |
| `VCOM` | WhatsApp | Hola Averarq, vi el video del restobar y tengo un local [VCOM] |
| `VSC` | WhatsApp | Hola Averarq, vi el video de la casa en Catemu y tengo una parcela [VSC] |

> **Cuando exista `/casa-en-tu-parcela`**, cambia el destino de `CASA2` a esa landing y conserva los mismos UTM. Hoy apunta al estimador de la portada (`#cotizador`), que desde la Semana 0 pesa 64 KB de HTML (las imágenes ya no van embebidas).

En el **Organizador**, registra cada contacto con Fuente = "Meta Ads" y el código que aparece al final del primer mensaje.

---

## A · Regularización → campaña `AVQ_REG_MSG` (objetivo: Mensajes · WhatsApp)

### A1 · Carrusel "¿Ampliaste sin permiso?" (5 láminas 1:1) · `REG1`
Piezas: `A1-regularizacion-carrusel-01…05.jpg`. Van en ese orden; desactiva "mostrar primero las tarjetas con mejor rendimiento".

- **Texto principal:**
  ¿Quieres vender tu casa y el banco te pidió la recepción final? 🏠
  Una ampliación sin permiso puede frenar la venta, el crédito o la herencia.
  Soy arquitecto en el Valle del Aconcagua y regularizo ante la DOM de San Felipe, Los Andes, Llay-Llay, Catemu y Rinconada, incluida la Ley del Mono cuando aplica.
  Escríbeme y en 24 h te digo por dónde va tu caso.
- **Títulos por tarjeta:** 1 "¿Ampliaste sin permiso?" · 2 "Lo que pierdes sin recepción" · 3 "4 pasos a la recepción final" · 4 "Ley del Mono: ¿calificas?" · 5 "Revisión gratis en 24 h"
- **Botón:** Enviar mensaje de WhatsApp

### A2 · "31 DIC 2027" (feed + historia) · `REG2`
Piezas: `A2-ley-del-mono-plazo-feed.jpg` + `A2-ley-del-mono-plazo-story.jpg`

- **Texto principal:**
  La Ley del Mono tiene plazo: hoy está vigente hasta el 31 de diciembre de 2027.
  Si construiste un dormitorio, un segundo piso o un quincho sin permiso, este es el camino más simple para ponerlo en regla, si tu caso califica.
  Revisamos tu caso gratis por WhatsApp. Arquitecto PUCV con base en Llay-Llay.
- **Título:** Ley del Mono: revisa si tu casa califica
- **Descripción:** Revisión gratuita por WhatsApp
- **Botón:** Enviar mensaje de WhatsApp

> ⚠️ Si el Senado aprueba la extensión a 2029 o el tope de 2.000 UF, **esta pieza queda desactualizada ese mismo día**. Hay que cambiar la fecha en `_fuente/generar.py` (función `a2_plazo`) y volver a generarla.

### A3 · "¿Vas a vender o pedir un crédito?" (feed + historia) · `REG3`
Piezas: `A3-vender-credito-feed.jpg` + `A3-vender-credito-story.jpg`

- **Texto principal:**
  Casi todo es regularizable. Lo que cambia es el camino.
  Depende de la antigüedad, la superficie y lo que permite tu plan regulador. Mi trabajo es leer tu caso, decirte la verdad y dejarlo resuelto hasta la recepción final.
  📍 Valle del Aconcagua · Putaendo (incluye zona típica) · La Calera
- **Título:** Tu casa en regla, lista para vender
- **Botón:** Enviar mensaje de WhatsApp

---

## B · Casa en tu parcela → campaña `AVQ_CASA` (fase 1: Tráfico / Mensajes; luego Clientes potenciales cuando el Pixel acumule datos)

### B1 · "De tu parcela a tu casa" (feed + historia) · `CASA1`
Piezas: `B1-de-tu-parcela-a-tu-casa-feed.jpg` + `B1-de-tu-parcela-a-tu-casa-story.jpg`. Son fotos reales de la obra de Casa San Carlos (Catemu) más el render del proyecto.

- **Texto principal:**
  Así empieza una casa en el valle: un terreno, una buena lectura del lugar y un proyecto pensado para él.
  Casa San Carlos, Catemu: diseño, permiso e inspección técnica de obra hasta la recepción final. Ladrillo, madera y teja con criterio contemporáneo.
  ¿Tienes una parcela? Conversemos tu proyecto.
- **Título:** De tu parcela a tu casa
- **Descripción:** Diseño + permiso + ITO en el Valle del Aconcagua
- **Botón:** Enviar mensaje de WhatsApp

### B2 · "¿Cuánto cuesta diseñar tu casa?" (feed + historia) · `CASA2`
Piezas: `B2-estimador-honorarios-feed.jpg` + `B2-estimador-honorarios-story.jpg`

- **Texto principal:**
  ¿Cuánto cuesta diseñar una casa? Sin letra chica.
  En mi web tienes un estimador en UF: eliges superficie y nivel de detalle y ves una referencia al instante. Incluye visitas a terreno y levantamiento con dron.
  Arquitecto en Llay-Llay · Todo el Valle del Aconcagua.
- **Título:** Calcula tus honorarios en 1 minuto
- **Descripción:** Referencia en UF al instante · averarq.cl
- **Botón:** Más información → URL de `CASA2`

### B3 · Carrusel "5 cosas antes de construir en tu parcela" (7 láminas 1:1) · `CASA3`
Piezas: `B3-5-cosas-parcela-carrusel-01…07.jpg`, en orden fijo.

- **Texto principal:**
  Antes de dibujar el primer plano, hay 5 cosas que deciden qué puedes construir en tu parcela (y cuánto te va a costar). 👇
  Desde mayo de 2025 rige el nuevo Plan Regulador Metropolitano en 10 comunas del valle: si compraste antes, las reglas pueden haber cambiado.
  Guárdalo y, si tienes dudas con tu terreno, escríbeme.
- **Títulos por tarjeta:** "5 cosas antes de construir" · "¿Urbano o rural?" · "Papeles al día" · "Agua y alcantarillado" · "Topografía y acceso" · "Sol y viento" · "Conversemos tu parcela"
- **Botón:** Enviar mensaje de WhatsApp
- También sirve como **publicación orgánica** en Instagram, porque se guarda y se comparte mucho.

> Antes de publicar, confirma con `normativa-averarq` las referencias de la lámina 2 (art. 55 LGUC) y de la lámina 3 (solución sanitaria particular ante la SEREMI). El texto es general a propósito, pero conviene tener la cita lista si alguien pregunta.

### B4 · Carrusel "Proyectos del valle" (5 láminas 1:1) · `CASA4`
Piezas: `B4-proyectos-del-valle-carrusel-01…05.jpg`. Aquí sí puedes dejar activado que Meta ordene las tarjetas según su rendimiento, pero la número 5 (cierre) debe quedar al final.

- **Texto principal:**
  Casas pensadas para el valle, no copiadas de un catálogo.
  Catemu, Llay-Llay, Rinconada: cada proyecto parte leyendo el terreno, el sol y la normativa de su comuna, y lo acompaño hasta la recepción final.
  ¿Cuál es el tuyo? Conversemos.
- **Títulos por tarjeta:** "Casa San Carlos · Catemu" · "Casa La Colonia · Catemu" · "Casa Doble L · Llay-Llay" · "Casa 31 · Rinconada" · "Tu proyecto, aquí"
- **Botón:** Enviar mensaje de WhatsApp

---

## C · Comercial → campaña `AVQ_COM_MSG` (Mensajes)

### C1 · "Del local vacío al negocio funcionando" (feed + historia) · `COM1`
Piezas: `C1-restobar-feed.jpg` + `C1-restobar-story.jpg`. Es un render del Restobar Esmeralda en Los Andes, y la pieza lo indica.

- **Texto principal:**
  Del local vacío al negocio funcionando: diseño interior, remodelación y permisos en un solo equipo.
  Ejemplo: Restobar Esmeralda, Los Andes (110 m²).
  San Felipe · Los Andes · Llay-Llay · Quillota · La Calera.
- **Título:** Tu local, diseñado y en regla
- **Botón:** Enviar mensaje de WhatsApp

### C2 · "¿Te piden recepción final para la patente?" (feed) · `COM2`
Pieza: `C2-patente-recepcion-feed.jpg`

- **Texto principal:**
  ¿Te piden recepción final para sacar la patente? 🧾
  Regularizo locales, gestiono cambios de destino y diseño el interior de tu negocio para que abras en regla.
  Revisamos la factibilidad de tu local gratis antes de que firmes el arriendo.
- **Título:** Revisión gratuita de tu local
- **Botón:** Enviar mensaje de WhatsApp

---

## M · Marca → campaña `AVQ_MARCA` (Reconocimiento / ThruPlay) y retargeting

### M1 · "Diseño con identidad. Permisos sin sorpresas." (feed + historia) · `MARCA`
Piezas: `M1-marca-feed.jpg` + `M1-marca-story.jpg`

- **Texto principal:**
  Arquitecto con base en Llay-Llay. Diseño viviendas con identidad del valle y las acompaño desde el primer plano hasta la recepción final en la DOM.
  Estudio de sol y viento, levantamiento con dron propio y seguimiento del proyecto desde tu celular.
- **Título:** Arquitectura del Valle del Aconcagua
- **Botón:** Enviar mensaje (en retargeting) o Más información (en reconocimiento)

---

## Qué probar primero (semana 1)

| Conjunto | Anuncios activos | Qué se aprende |
|---|---|---|
| REG · Valle alto | A1 carrusel · A2 · A3 | ¿Funciona mejor el dolor (vender o crédito), la urgencia (plazo) o la educación (carrusel)? |
| REG · Valle bajo | A1 · A2 · A3 | Lo mismo, en otra geografía |
| CASA · Valle | B1 · B2 · B4 | ¿Pesa más la prueba de obra real, la transparencia de precio o el portafolio? |
| MARCA | M1 · B1 | Llena los públicos de retargeting |

B3 y los anuncios comerciales (C1, C2) entran en la semana 5, como indica el plan. Mientras tanto, publica B3 en orgánico.

## Editar o crear piezas

```
cd _estrategia/anuncios/_fuente
python3 generar.py     # escribe los HTML (edita los textos en este archivo)
node render.mjs        # regenera los JPG en ../piezas/
```

- Las fotos fuente están en `_fuente/img/` y fueron extraídas de averarq.cl. Las tipografías están en `_fuente/fonts/`.
- Para agregar una pieza nueva, copia una función existente (por ejemplo `c2_patente`), cámbiale el nombre y súmala a `ANUNCIOS`.

## Lo que falta y conviene producir (mayor rendimiento en Meta)

- **Video corto (reels):** los reels suelen tener menor CPM que las imágenes. Las piezas B1, B2 y A3 son la base de los guiones del plan (§4.3). Lo ideal es grabar a Alejandro a cámara y un vuelo de dron sobre una parcela real.
- **Foto de Alejandro:** una foto profesional en obra humaniza la marca. Ninguna pieza lleva rostro todavía porque no hay retrato disponible en el sitio.
- **Caso real de regularización con antes y después:** por ejemplo La Parva (Los Andes) o Lo Vicuña (Putaendo), con autorización del propietario.

---

## Videos · reels 9:16 (lote 1)

Cinco reels de 13 a 24 s en `videos/`, cada uno con su miniatura (`-portada.jpg`). Son 1080×1920, H.264, 30 fps. **V1 a V4 van sin audio**: al subirlos, agrega música desde la biblioteca de audio de Meta (así queda licenciada) o déjalos en silencio. **V5 trae música original** compuesta y sintetizada para el video (sin samples de terceros), así que se puede subir tal cual. El texto de todos se lee sin sonido.

| Video | Campaña | Código | Qué muestra |
|---|---|---|---|
| **V1 · Del render a la obra** (16,5 s) | `AVQ_CASA` | `VCASA` | Casa La Colonia (Catemu): render → 4 fotos reales de obra (oct–nov 2025) → render y obra lado a lado → cierre "¿Tienes la parcela? Conversemos." |
| **V2 · ¿Ampliaste sin permiso?** (14 s) | `AVQ_REG_MSG` | `VREG` | Tipográfico: pregunta → "tu casa no existe para el sistema" → Ley del Mono vigente hasta el 31 DIC 2027 → "En 24 h te digo por dónde va tu caso". |
| **V3 · ¿Cuánto cuesta diseñar tu casa?** (13 s) | `AVQ_CASA` | `VCALC` | El estimador en acción: 60 → 120 m², luego "con ingenierías" (120–144 → 192–230 UF) → "Calcula el tuyo en 1 minuto · averarq.cl". |
| **V5 · Render vs. realidad** (24 s, con música) ★ | `AVQ_CASA` | `VSC` | Casa San Carlos (Catemu): render aéreo contra foto de dron del mismo ángulo → modelo 3D contra vista cenital → órbita de dron real → recorrido de obra → Alejandro recibe el dron en la mano → cierre. Los cortes caen cada 2 compases de la música y el impacto coincide con el dron llegando a la mano (19,0 s). Es el más fuerte del lote: usa material propio grabado en agosto de 2026. |
| **V4 · Del local vacío al negocio** (13 s) | `AVQ_COM_MSG` | `VCOM` | Tríptico del Restobar Esmeralda (Los Andes) con diseño interior, remodelación y permisos → "¿Tienes un local? Lo dejamos listo para abrir en regla." |

**Textos para el anuncio**

- **V1** · Texto principal: *En Catemu la dibujamos en julio de 2025 y en noviembre ya tenía techumbre. Diseño, permiso e inspección de obra hasta la recepción final, con el mismo arquitecto de principio a fin.* · Título: *De tu parcela a tu casa* · Botón: Enviar mensaje.
- **V2** · Texto principal: *Si construiste un dormitorio, un segundo piso o un quincho sin permiso, revisemos si tu caso califica para la Ley del Mono. Revisión gratis por WhatsApp.* · Título: *¿Ampliaste sin permiso?* · Botón: Enviar mensaje.
- **V3** · Texto principal: *Servicio, superficie y nivel de detalle: el estimador de averarq.cl te da una referencia en UF en un minuto. Sin letra chica.* · Título: *¿Cuánto cuesta diseñar tu casa?* · Botón: Más información.
- **V5** · Texto principal: *Así la dibujamos en 2025 y así se ve hoy desde el dron. Casa San Carlos, Catemu: 144 m² de ladrillo, madera y teja, con diseño, permiso e inspección de obra del mismo arquitecto.* · Título: *Del render a la realidad* · Botón: Enviar mensaje.
- **V4** · Texto principal: *Diseño interior, remodelación, cambio de destino y recepción final en un solo equipo, para que abras en regla.* · Título: *Del local vacío al negocio funcionando* · Botón: Enviar mensaje.

**Qué probar primero:** V5 y V1 contra B1 (misma campaña, video contra imagen) y V2 contra A2. Si el video baja el costo por conversación más de un 20 %, pasa el presupuesto del conjunto a video.

**Advertencia:** V2 lleva la fecha 31-dic-2027, igual que A2. Si se aprueba la prórroga de la Ley del Mono, cambia la fecha en `video/V2-ampliaste-sin-permiso.html` y vuelve a renderizar.

**Editar o renderizar**

```
cd _estrategia/anuncios/_fuente
npm i --no-save playwright-core      # una vez; usa Edge o Chrome instalados
python3 extraer_secuencias.py        # una vez: tramos de video para V5 → secuencias/ (no va a git)
python3 musica/v5_musica.py          # regenera la música de V5 (musica/V5-musica.wav)
node render-video.mjs                # todos → ../videos/
node render-video.mjs V2 --cuadros   # uno solo, y guarda cuadros de control en frames/
```

- Cada video es un HTML en `_fuente/video/` con una función `frame(t)`. Ábrelo en el navegador para verlo en bucle (clic = reiniciar). Los tiempos de cada escena están al inicio del `<script>`.
- Las fotos de obra de V1 vienen de `2025/2025_Oscar Aguilera/FOTOS` y los renders de `RENDERS` (`v-lc-*.jpg` en `_fuente/img/`). Las de V4, de `0.WEB/Proyectos Seleccionados` (`v-esmeralda-*.jpg`). Las de V5, de `2025/2025_Andrés Martinez` (`RENDERS`, `portafolio` y `audiovisual`, en `v-sc-*.jpg`); sus tramos de video se definen en `TRAMOS` dentro de `extraer_secuencias.py`.
- El texto importante queda entre y≈250 y y≈1450 px, fuera de lo que tapa la interfaz de Reels.
