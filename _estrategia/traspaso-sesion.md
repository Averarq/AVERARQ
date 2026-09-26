# Traspaso de sesión — AVERARQ · Marca y Meta Ads

> Pega este archivo en una sesión nueva de Claude Code, o pídele que lo lea: `lee _estrategia/traspaso-sesion.md y continúa`.
> Resume una sesión en la nube del 25–26 de septiembre de 2026.

## Quién y qué

- **Cliente:** Arq. Alejandro Vera Donoso (PUCV), Averarq SpA. Base en Llay-Llay, Valle del Aconcagua (V Región). Contacto: ai.veradonoso@gmail.com, WhatsApp +56 9 5431 7945, @averarq.
- **Perfil:** arquitecto independiente, muy interesado en aplicar tecnología a su trabajo y a su marca. Se comunica en español de Chile, tuteando.
- **Opera en:** Llay-Llay, San Felipe, Los Andes, Rinconada y Catemu. Evalúa expandirse a Putaendo.
- **Objetivo:** convertir a Averarq en la oficina de arquitectura dominante de la Región de Valparaíso en 24 meses, captando clientes con Meta Ads (Facebook e Instagram).
- **Repositorio:** `Averarq/AVERARQ` es el sitio averarq.cl en GitHub Pages. Es **público**: se le advirtió al cliente que `_estrategia/` queda visible en GitHub, aunque no se publica en la web porque Jekyll ignora las carpetas que empiezan con `_`.
- **Rama de trabajo:** `claude/averarq-brand-meta-ads-deld59`. Tiene 2 commits sobre `main` y no hay pull request.

## Qué se hizo (todo está en la rama)

### 1. Plan estratégico → `_estrategia/plan-marca-meta-ads-2026.md`

**Competencia.** Se analizaron 12 competidores con fuentes web:
- **En el valle y la zona:**
  - Hut Arquitectura (valle, casas prefabricadas en panel SIP): es el competidor directo más fuerte.
  - Domus Eaton (Quillota): regularizaciones y tasaciones, sin diseño.
  - Tu Solución Diseño y Arquitectura (San Felipe): oferta económica, presencia digital débil.
  - Prefabricadas locales: le venden al dueño de parcela antes de que piense en un arquitecto.
- **De Santiago que proyectan en la zona:** Moreno·Sosa (premium), Loi, ANDES Arquitectos.
- **De Gran Valparaíso y la costa:** planosdearquitectura.cl (regularizaciones a $650.000–$1.800.000, con precios publicados y buen SEO), Estudio LAC, Andes Arquitectura y Construcción (Villa Alemana), especialistas en regularización.
- **Pendiente:** la Biblioteca de Anuncios de Meta no se pudo consultar desde la nube. En el plan quedó un protocolo de 30 minutos (§2.4) para completar a mano los anuncios activos, seguidores y frecuencia de publicación.

**Hueco de mercado.** Nadie en el valle une diseño con identidad, dominio de la DOM y regularizaciones, y transparencia digital.

**Posicionamiento.** Promesa: *"Diseño con identidad. Permisos sin sorpresas."* Cuatro pilares: territorio, evidencia técnica, transparencia y acompañamiento.

**Diagnóstico del sitio:**
- No tiene Meta Pixel ni ningún tipo de analítica.
- `index.html` pesa **17 MB** porque las imágenes están embebidas en base64. No sirve como destino de anuncios.
- Falta la landing `/casa-en-tu-parcela`.
- Fortalezas: siete landings por comuna con buen SEO, `/regularizaciones`, estimador de honorarios en UF (`#cotizador`), portal `/seguimiento` y herramientas internas (Solar Lab, Wind Lab, acreditación térmica, resistencia al fuego, Gestor, Organizador con CRM).
- El estimador cobra 1,0 UF/m² (solo arquitectura) y 1,6 UF/m² (con ingenierías), por debajo del mercado (1,2 a 4 UF/m²). Se sugirió revisar la tarifa a los 12 meses.

**Tres embudos:**
- **A. Regularización:** por WhatsApp. La Ley del Mono está vigente hasta el 31-dic-2027 y hay un proyecto en el Senado que la extendería a 2029 y subiría el tope de avalúo de 1.000 a 2.000 UF.
- **B. Casa en tu parcela:** landing más estimador de honorarios.
- **C. Comercial:** locales, patentes y cambio de destino.

**Presupuesto.** Escenario medio de **$300.000/mes más IVA**, es decir **$2.142.000 en 6 meses**. Escenario bajo de $150.000/mes y alto de $600.000/mes.

**Cronograma de 6 meses** (octubre 2026 a marzo 2027):
- La semana 0 es de preparación: Pixel, landing, WhatsApp Business y perfil de empresa en Google.
- Luego vienen tres fases: lanzamiento, optimización y escalamiento.
- Métricas y objetivos: CTR ≥ 1 %, costo por conversación de WhatsApp ≤ $6.000, costo por lead en landing ≤ $20.000, ROAS de honorarios ≥ 5×.

**Referencias de costos Meta en Chile (con fuentes en el plan):**
- CPM ≈ US$2,44.
- Costo por mensaje en un servicio profesional local ≈ $2.800.
- CPL inmobiliario de casas: $12.000–$25.000.
- Inversión mínima: $150.000/mes.
- Noviembre y diciembre encarecen entre 30 % y 80 %.

### 2. Lote 1 de anuncios → `_estrategia/anuncios/`

**Las piezas.** Son 30 imágenes JPG en `piezas/`, y `vista-general.jpg` las muestra todas juntas:
- **A1:** carrusel de 5 láminas, "¿Ampliaste sin permiso?".
- **A2:** "31 DIC 2027" (Ley del Mono), en feed e historia.
- **A3:** "¿Vas a vender o pedir un crédito?", en feed e historia.
- **B1:** "De tu parcela a tu casa", con fotos reales de la obra de Casa San Carlos (Catemu) y el render del proyecto.
- **B2:** estimador de honorarios.
- **B3:** carrusel de 7 láminas, "5 cosas antes de construir en tu parcela".
- **B4:** carrusel de 5 láminas, proyectos del valle.
- **C1:** Restobar Esmeralda, en feed e historia.
- **C2:** "¿Te piden recepción final para la patente?".
- **M1:** anuncio de marca, en feed e historia.

**El README.** `README.md` trae, para cada anuncio, el texto principal, el título, el botón, el destino y un código de seguimiento en el mensaje de WhatsApp (`REG1`, `CASA2`, etc.) para anotarlo en el Organizador. También indica qué probar la primera semana.

**El generador.** Está en `_fuente/`:
- `generar.py` escribe los HTML. Los textos se editan aquí, en las funciones `a1_carrusel`, `a2_plazo`, etc.
- `render.mjs` los convierte a JPG con Playwright.
- `img/` tiene las fotos extraídas del sitio y `fonts/` la tipografía Barlow local, porque el Chromium headless no cargaba Google Fonts.
- `html/` está en `.gitignore`.

**Para volver a generar las piezas:**
```
cd _estrategia/anuncios/_fuente
python3 generar.py
node render.mjs
```
En local, eso requiere tener instalado `pip install pillow`, `npm i -g playwright` y `npx playwright install chromium`.

**Identidad.** Naranjo #FC4C02, oscuro #111110, claro #F2F0EB, Barlow y Barlow Condensed en mayúsculas para los titulares, e isotipo triangular. La fuente de verdad de la marca está en el skill `informe-avance` (`brand.py`). El wordmark blanco está en `img/wordmark-blanco.png`.

**Fotos disponibles en el sitio:**
- Casa San Carlos: render, planta y 6 fotos reales de obra.
- Casa La Colonia y Casa Doble L: renders.
- Casa 31: cocina.
- Restobar Esmeralda: renders.
- La Dehesa: antes y después.
- Stripcenter La Perla (Miami): renders.
- **No hay ninguna foto de Alejandro.**

## Advertencias vigentes

- **La pieza A2 lleva la fecha 31-dic-2027.** Si el Senado aprueba la extensión a 2029 o el tope de 2.000 UF, hay que regenerarla y preparar una campaña especial.
- **Antes de publicar B3,** verificar con `normativa-averarq` las referencias al art. 55 de la LGUC y a la solución sanitaria ante la SEREMI.
- **B2 apunta a `averarq.cl/#cotizador`,** la portada de 17 MB, hasta que exista `/casa-en-tu-parcela`.
- **Los datos de competencia marcados "?"** están sin verificar y los completa el cliente con el protocolo §2.4.
- **Las proyecciones de resultados son hipótesis** que se recalibran con los datos del día 30.

## Próximos pasos ofrecidos (el cliente aún no elige)

1. **Guiones de reels** plano por plano, para grabar con dron en una jornada. Los reels son más baratos en CPM.
2. **Landing `/casa-en-tu-parcela`**: liviana (menos de 1 MB), con estimador, casos del valle, botón de WhatsApp y Pixel. Pasarle QA con el skill `qa-web-averarq`.
3. **Versiones animadas** de las piezas estáticas.
4. **Semana 0 técnica:**
   - Instalar Meta Pixel con los eventos `Contact` (clic en WhatsApp), `ViewContent` (uso del estimador) y `Lead`.
   - Agregar un aviso de privacidad antes de que entre en vigor la Ley 21.719 (1-dic-2026, verificar la fecha).
   - Sacar las imágenes base64 de `index.html`.
   - Agregar la opción "Meta Ads" al campo Fuente del Organizador (`organizador/index.html`).

## Notas de trabajo

- Hacer commits en la rama `claude/averarq-brand-meta-ads-deld59`. No crear un pull request salvo que el cliente lo pida.
- El sitio no tiene build: son HTML estáticos. Las landings por comuna pesan unos 15 KB y sirven de plantilla para páginas nuevas.
- Skills propios del cliente que conviene usar: `normativa-averarq`, `qa-web-averarq`, `carta-averarq`, `informe-avance` y `utilidad-presupuesto-averarq`.
