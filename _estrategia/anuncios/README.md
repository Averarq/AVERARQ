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

> **Cuando exista `/casa-en-tu-parcela`**, cambia el destino de `CASA2` a esa landing y conserva los mismos UTM. Hoy apunta al estimador de la portada (`#cotizador`). Esa página pesa 17 MB, así que conviene revisar la tasa de rebote durante los primeros días.

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
