# AVERARQ — Plan de posicionamiento de marca y captación vía Meta Ads

**Oficina:** Averarq SpA · Arq. Alejandro Vera Donoso (PUCV) · Base Llay-Llay, Valle del Aconcagua
**Horizonte:** plan ejecutable de 6 meses (oct-2026 → mar-2027) dentro de una visión de 24 meses
**Fecha de elaboración:** 25-sep-2026 · UF de referencia: **$41.016,28** (25-sep-2026)

> **Nota de método.** Todo dato de competencia y de costos de Meta Ads viene de búsqueda web (fuentes al final). Donde un dato **no se pudo verificar** (seguidores exactos, frecuencia de publicación, anuncios activos en la Biblioteca de Anuncios de Meta), el documento lo indica como **"por verificar"** y entrega un protocolo de 30 minutos para completarlo (§2.4). La Biblioteca de Anuncios exige navegador con sesión y JavaScript; no fue posible consultarla desde este entorno. Las proyecciones de resultados son **hipótesis a validar** con los datos de las primeras 4 semanas, no promesas.

---

## 0. Resumen ejecutivo (1 página)

**El hueco de mercado.** En el Valle del Aconcagua nadie combina, bajo una sola marca, **(1) diseño residencial con identidad**, **(2) dominio de la tramitación DOM y regularizaciones** y **(3) transparencia digital** (precio de referencia en línea, seguimiento del proyecto, evidencia técnica). La competencia real se reparte así:

- **Diseño + construcción industrializada** (Hut Arquitectura, SIP): vende la casa, no el proyecto ni la tramitación.
- **Tramitación sin diseño** (Domus Eaton en Quillota; especialistas en regularización de Gran Valparaíso): resuelven papeles, no arquitectura.
- **Oficinas premium de Santiago** (Moreno·Sosa, Loi) que proyectan ocasionalmente en la zona: buen diseño, pero sin conocimiento de las DOM locales ni presencia en obra.
- **Directorios y prefabricadas** (Habitissimo lista 21 arquitectos solo en San Felipe; múltiples "casas prefabricadas San Felipe" en Facebook): compiten por precio y capturan al cliente que no sabe que necesita arquitecto.

**Posicionamiento propuesto:** *"El arquitecto del Valle: diseño con identidad y permisos sin sorpresas."* Averarq es la oficina que conoce cada DOM del valle, respalda cada decisión con análisis técnico propio (sol, viento, térmica, fuego, dron) y acompaña hasta la recepción final.

**Tres embudos Meta Ads:**
1. **Regularización** (Ley del Mono / sin recepción). Es el embudo de volumen: se activa con WhatsApp y hay una ventana de urgencia real. El plazo vigente vence el 31-dic-2027 y hay un proyecto en el Senado que lo extendería a 2029.
2. **Casa en tu parcela** (obra nueva en sitio o parcela de agrado). Es el embudo de ticket alto: se activa con landing, estimador de honorarios y video con dron.
3. **Comercial / cambio de destino** (locales, patentes, equipamiento). Es un embudo de bajo volumen y alto valor: se activa con casos reales y retargeting.

**Inversión recomendada (escenario medio):** **$300.000/mes en medios + IVA** (≈ $357.000), es decir, **≈ $2,14 millones en 6 meses**. Un solo proyecto de diseño de 120 m² a la tarifa actual del estimador (1,0 UF/m² ≈ $4,9 millones) paga más de dos veces el plan completo.

**Antes de gastar un peso en anuncios (semana 0) hay que resolver cuatro cosas:**
1. Instalar el Meta Pixel y los eventos de conversión: hoy el sitio **no tiene ningún tipo de medición**.
2. Aligerar la portada: pesa **17 MB** porque tiene las imágenes embebidas en base64, y una landing así pierde gran parte del tráfico móvil.
3. Crear la landing `/casa-en-tu-parcela`.
4. Etiquetar los enlaces de WhatsApp por campaña para saber qué anuncio trajo a cada cliente.

**Meta a 24 meses ("dominante" medido, no declarado):**
- Primera posición local en Google Maps para "arquitecto + comuna" en San Felipe, Los Andes y Llay-Llay.
- Más de 50 reseñas en Google.
- Más de 20 proyectos/año firmados por canal digital.
- Costo de adquisición por proyecto bajo el 10 % de los honorarios.

---

## 1. Diagnóstico de mercado y contexto normativo (motores de demanda)

| Motor de demanda | Dato verificado | Implicancia comercial |
|---|---|---|
| **Ley del Mono (20.898)** | Plazo vigente extendido al **31-dic-2027** por Ley 21.725. Un proyecto aprobado por la Cámara (en el Senado, sep-2026) lo extendería al **31-dic-2029** para obras anteriores al 28-nov-2025 y subiría el tope de avalúo de **1.000 a 2.000 UF**. | Urgencia legítima ("el plazo existe y vence"), sin prometer lo que el Senado aún no aprueba. Si sube el tope a 2.000 UF, se amplía mucho el universo de viviendas que califican: hay que tener lista una campaña para ese día. |
| **PREMVAL Satélite Alto Aconcagua** | Vigente desde el **29-may-2025** (Res. 31, GORE Valparaíso). Regula el área urbana y rural de San Esteban, Rinconada, Los Andes, Calle Larga, Putaendo, Santa María, San Felipe, Catemu, Panquehue y Llay-Llay. | Cambió "qué se puede construir y dónde" en las 10 comunas donde opera Averarq. Contenido educativo con autoridad: "¿Qué dice el nuevo plan regulador de tu parcela?" |
| **Nuevo PRC La Calera (2026)** | Según averarq.cl/arquitecto-la-calera, sectores como El Trigal y Entrepuentes salieron de la zona de restricción. | Microcampaña geolocalizada a esos sectores: "ahora sí puedes regularizar". |
| **Zona Típica Putaendo** | Centro histórico y calle Comercio (2002), Hacienda Lo Vicuña (2008). Requiere autorización del CMN (Ley 17.288). | Nicho con muy poca competencia: pocos arquitectos gestionan DOM y CMN a la vez. Buena puerta de entrada para la expansión a Putaendo. |
| **Parcelas de agrado** | Oferta activa en Putaendo (Rinconada de Silva, Camino Caracoles), San Felipe y Rinconada de Los Andes, con valores de UF 1.510 a UF 13.500. | Hay demanda de primera y segunda vivienda en parcela, con propietarios que muchas veces viven en Santiago o Gran Valparaíso. Es un público geográficamente distinto al del proyecto. |
| **Precios de mercado** | Honorarios habituales de **1,2 a 4 UF/m²** (referencia frecuente: 1,7 UF/m²). Regularización en Gran Valparaíso: **$650.000 a $1.800.000** (planosdearquitectura.cl). | El estimador de Averarq (1,0 UF/m² solo arquitectura, con visitas y dron incluidos) está **bajo el promedio de mercado**. No hay que competir por precio en los anuncios: la ventaja es el valor. Conviene revisar la tarifa hacia 1,2–1,4 UF/m² cuando la demanda lo permita. |

---

## 2. Análisis de competencia

### 2.1 Fichas de competidores

Leyenda: **✔** verificado en fuente · **?** por verificar con el protocolo §2.4.

| # | Competidor | Base / cobertura | Presencia digital | Tipo de proyectos | Posicionamiento | Tono visual/comunicacional | Frecuencia publicación / Ads | Debilidades evidentes |
|---|---|---|---|---|---|---|---|---|
| 1 | **Hut Arquitectura** | Valle del Aconcagua ✔ | Web hut.cl ✔ · IG/FB ? | Diseño y construcción de viviendas de alta eficiencia energética, prefabricadas en panel SIP. También hormigón, albañilería y tierra. Más de 50 proyectos y más de 40.000 m² intervenidos ✔ | Medio / medio-alto (llave en mano) | Técnico-constructivo, centrado en el sistema SIP | ? / ? | La marca está atada a un sistema constructivo: el cliente que quiere albañilería o teja, o que necesita regularizar, no se ve reflejado. No comunica tramitación DOM ni patrimonio. **Es el competidor directo más fuerte en el valle.** |
| 2 | **Domus Eaton** (Constructora Domus Eaton Ltda.) | Quillota, O'Higgins 229 of. 204 ✔ · "todo Chile" | Web domuseaton.cl ✔ · 2 páginas de Facebook ✔ · X @domuseaton1 ✔ · perfil homify ✔ | Regularizaciones, tasaciones, subdivisiones, cambio de uso de suelo, construcción ✔ | Medio (gestión técnica) | Corporativo, de servicios, sin identidad de diseño | ? / ? | Vende trámites, no arquitectura. Su presencia digital está fragmentada en varias cuentas. No tiene foco en el valle alto (San Felipe y Los Andes). |
| 3 | **Moreno·Sosa Arquitectos** | Santiago + México ✔ · proyecta en Quillota (Casa JL) ✔ | Web morenososa.com (ES/EN) ✔ · IG @morenososaarquitectos con reels ✔ · FB ✔ | Casas nuevas, remodelaciones, comercial, visualización 3D ✔ | **Premium** (Las Condes, Lo Barnechea, Vitacura, clientes expat, costa central) ✔ | Editorial, render de alta calidad, bilingüe | Reels activos ✔ / Ads ? | No es local: sin relación con las DOM del valle ni presencia en obra. Es caro para el cliente medio del valle. Compite solo por el propietario santiaguino con parcela. |
| 4 | **Loi Arquitectos** | Santiago, desde 2002 ✔ | Web loi.cl ✔ · IG ? | Residencial, oficinas, equipamiento. Hizo el Centro Médico Los Andes (285 m²) ✔ | Medio-alto / institucional (Harvard GSD) | Sobrio, institucional | ? / ? | Presencia puntual en Los Andes, sin foco territorial. Referente para el segmento de equipamiento y salud, no para vivienda del valle. |
| 5 | **ANDES Arquitectos y Asociados Ltda.** | Nacional, foco en la Región Metropolitana ✔ | Web arqandes.cl ✔ | Unos 400 proyectos, gestión de permisos y recepciones ✔ | Medio (tramitación) | Técnico | ? / ? | No es local, pero **captura búsquedas por su nombre** ("Andes" ≈ "Los Andes"). Es un riesgo en SEO y SEM, no en Meta. |
| 6 | **Andes Arquitectura y Construcción** | Villa Alemana (aparece en directorios de la provincia de Los Andes) ✔ | Perfiles en Habitissimo y 2x3 ✔ · web propia ? | Diseño de viviendas exclusivas, cálculo, instalaciones, paisajismo, ITO. Más de 15 años ✔ | Económico-medio | Genérico de directorio | ? / ? | Depende de directorios. Base lejana al valle alto. Sin marca visual propia verificable. |
| 7 | **Tu Solución Diseño y Arquitectura** (Arq. Marcela Galdames Schweitzer, U. de Chile) | San Felipe ✔ | Página en el directorio arquitecturachile.cl (formato .htm antiguo) ✔ · IG/FB ? | Diseño, planos, remodelación, construcción. "Precios justos" ✔ | **Económico** | Tradicional, basado en precio | ? / ? | Presencia digital débil y desactualizada. Mensaje centrado en precio. Es **competidor local directo en San Felipe**, pero se le puede ganar con facilidad en lo digital. |
| 8 | **planosdearquitectura.cl** (Arq. Valerie Soto Aravena) | Valparaíso, Viña, Quilpué, Villa Alemana, Concón ✔ | Web con SEO fuerte: posiciona "Ley del Mono actualizada 2026" y páginas por servicio ✔ | Regularizaciones (**$650.000–$1.800.000**, desde $900.000 obra menor y $1.300.000 obra nueva, con planes de pago), diseño y ampliaciones ✔ | **Económico-medio, con precios publicados** | Informativo, orientado a búsqueda | ? / ? | No cubre el valle. Es **el referente a imitar en SEO y transparencia de precio** y a superar en diseño y marca. Si amplía cobertura, compite directo en regularización. |
| 9 | **RA® Regularizarquitectos** (@regularizarquitectos.cl) | ? (probablemente la Región Metropolitana) | Instagram-first, unos 2.788 seguidores al momento de la búsqueda ✔ | Especialistas en regularización, Ley 20.898, permisos municipales ✔ | Medio | Educativo en redes | ? / ? | Nicho de un solo servicio. Sirve de benchmark de contenido educativo en Instagram sobre regularización. |
| 10 | **Prefabricadas locales** (Aconcagua Prefabricadas, Casas Prefabricadas San Felipe, Casas Prefabricadas ProChile, avisos en eVisos) | San Felipe y el valle ✔ | Páginas de Facebook y avisos clasificados ✔ | Casas prefabricadas y cabañas de madera, ampliaciones, cobertizos, cierres ✔ | **Económico** | Catálogo de modelos y precio por m² | Probable pauta en Facebook ? | **Competidor sustituto:** captan al dueño de parcela *antes* de que piense en un arquitecto. Suelen dejar pendientes el permiso y la recepción, lo que más tarde genera clientes de regularización. |
| 11 | **Estudio LAC®** | Viña del Mar ✔ | Web estudiolac.cl ✔ | Corporativo, oficinas, comercial, gastronómico, "branding arquitectónico" ✔ | Medio-alto | Marca cuidada, estética de estudio | ? / ? | Compite en el segmento comercial y gastronómico (del tipo Restobar Esmeralda), pero desde la costa. Sin presencia en el valle. |
| 12 | **Especialistas en regularización de Gran Valparaíso** (890 ARQ Ltda., Prat 865 of. 63; Arq. Juan-Luis Menares, Viña del Mar) | Valparaíso y Viña ✔ | Avisos en Slideshare, Yapo y similares ✔ | Regularización Ley del Mono ✔ | Económico | Aviso clasificado | ? / ? | Marketing de bajo costo y sin marca. No cubren el valle. |
| — | **Costa norte (segundo nivel):** NOS Arquitectura (Zapallar, 5 arquitectos + paisajista), LFG Arquitectura (Zapallar, 12 años), CIA.ARQ (Cristián Irarrázaval) ✔ | Zapallar, Papudo, Puchuncaví | Web e Instagram ✔ | Residencial de segunda vivienda en la costa | **Premium** | Editorial | ? | No compiten en el valle. Son referencia de estética para la línea premium. |
| — | **Directorios** (Habitissimo: 21 arquitectos en San Felipe y 25 en la provincia; Fixando: 31 en Quillota; 2x3; StarOfService) ✔ | — | Plataformas de cotización | Todo tipo | Comparación por precio | — | — | El cliente que llega por directorio compara precio. Averarq debe estar presente (captura de demanda), pero su marca no debe depender de ellos. |

### 2.2 Matriz comparativa

Ejes: **posicionamiento de precio** (↓ económico · ↑ premium) × **especialización** (← tramitación / regularización · → diseño de autor), con **presencia digital** indicada como ● fuerte, ◐ media, ○ débil. Las calificaciones de presencia digital son juicio del consultor a partir de lo visible en la búsqueda.

```
                       PREMIUM
                          ▲
   Loi ◐                  │         Moreno·Sosa ●   NOS / LFG ◐
                          │                 Estudio LAC ◐
                          │
   ANDES Arq. y Asoc. ◐   │   ★ AVERARQ OBJETIVO (medio-alto, local,
                          │     diseño + DOM + tecnología)
   Domus Eaton ◐          │         Hut Arquitectura ◐
TRAMITACIÓN ◄─────────────┼─────────────────────────────► DISEÑO
   Regularizarquitectos ● │   ☆ AVERARQ HOY (precio bajo mercado,
   planosdearquitectura ● │     sin medición ni pauta)
   890 ARQ / avisos ○     │   Andes Arq. y Constr. ○
                          │   Tu Solución ○   Prefabricadas ◐
                          ▼
                      ECONÓMICO
```

### 2.3 Huecos de mercado que Averarq puede ocupar

1. **"Diseño + DOM" bajo una sola firma, en el valle alto.** Hoy el cliente elige entre alguien que diseña bonito pero no conoce la DOM de Catemu, y alguien que tramita pero no diseña. Averarq tiene ambas cosas y además proyectos reales en Catemu, Llay-Llay, Los Andes y Rinconada.
2. **Transparencia de precio con marca.** Solo planosdearquitectura.cl (fuera del valle) publica precios. Averarq ya tiene un **estimador en UF en línea**, un activo único en el valle que hay que usar en los anuncios como "Calcula en 1 minuto cuánto cuesta diseñar tu casa".
3. **Evidencia técnica visible.** Nadie en la zona muestra estudios de asoleamiento, viento o acreditación térmica como parte de su propuesta. Averarq tiene Solar Lab, Wind Lab, acreditación térmica (art. 4.1.10), resistencia al fuego (art. 4.3.3) y levantamiento con dron. Son herramientas internas que se convierten en **contenido demostrable**.
4. **Patrimonio en Putaendo.** Gestionar DOM y Consejo de Monumentos a la vez es un nicho de oferta mínima. Es la cabeza de playa para la expansión.
5. **El "después" de la prefabricada.** Cada casa prefabricada sin permiso es un futuro cliente de regularización. Además, se puede ofrecer "proyecto + permiso para tu prefabricada" como producto.
6. **El propietario santiaguino con parcela en el valle.** Premium de Santiago es caro y lejano, y los locales no le hablan a ese público. Averarq puede ofrecerle un seguimiento remoto con portal de avance (`/seguimiento`) e informes con dron.

### 2.4 Protocolo de verificación de 30 minutos (completar antes del lanzamiento)

1. **Biblioteca de Anuncios de Meta** (facebook.com/ads/library) → País: Chile → Categoría: Todos los anuncios. Buscar por nombre de cada competidor y por palabras clave: `arquitecto San Felipe`, `arquitecto Los Andes`, `regularización`, `ley del mono`, `casas prefabricadas`, `planos`. Anotar para cada uno si tiene anuncios activos (sí/no), fecha de inicio, formato (video, carrusel, imagen) y CTA (WhatsApp, formulario, web). *Un anuncio activo hace más de 60 días suele indicar que le está funcionando.*
2. **Instagram y Facebook** de cada competidor: seguidores, número de publicaciones de los últimos 30 días, uso de reels y enlaces a WhatsApp.
3. **Google Maps**: buscar "arquitecto" en San Felipe, Los Andes, Llay-Llay y Quillota. Anotar los tres primeros resultados y su número de reseñas: esa es la vara a superar.
4. Volcar todo en la columna "?" de la tabla §2.1 y guardar capturas en el Organizador (sección Documentos).

---

## 3. Diagnóstico de marca Averarq

### 3.1 Qué tiene hoy (revisión de averarq.cl, en este repositorio)

**Fortalezas reales:**
- **Estructura SEO local ya construida:** siete landings por comuna (Llay-Llay, San Felipe, Los Andes, Catemu, Putaendo, La Calera) más `/regularizaciones`, con meta descripciones específicas, datos estructurados JSON-LD y un sitemap. Es un buen activo, por encima de casi toda la competencia local.
- **Contenido territorial genuino:** cada landing cita normativa real (PREMVAL 2025, PRC La Calera 2026, Zona Típica de Putaendo, el PRC de Llay-Llay de 1999). Transmite autoridad y no es un texto genérico.
- **Estimador de honorarios en UF** con el valor de la UF del día. Es transparencia que ningún competidor del valle ofrece.
- **Portal de seguimiento para el cliente** (`/seguimiento`) y **herramientas técnicas propias** (Solar Lab, Wind Lab, térmica, fuego, Gestor, Organizador con CRM de captación que ya incluye el campo "Fuente").
- **Casos reales en el territorio:** Casa San Carlos y Casa La Colonia (Catemu), Casa Doble L (Llay-Llay), Casa 31 (Rinconada), Restobar Esmeralda (Los Andes), regularizaciones en La Parva (Los Andes), Las Compuertas (Catemu) y Lo Vicuña (Putaendo, zona típica).
- **Identidad gráfica definida:** naranjo #FC4C02, isotipo, tipografía propia.
- **WhatsApp con mensaje precargado distinto por página**, lo que ya permite atribuir la página de origen.

**Brechas críticas para Meta Ads:**

| Brecha | Impacto | Acción |
|---|---|---|
| **No hay Meta Pixel, Conversions API ni analítica** en ninguna página | No se puede optimizar hacia conversiones, hacer retargeting ni medir el retorno | Instalar Pixel + eventos (§4.6) en la semana 0 |
| **La portada pesa 17 MB** (imágenes en base64 dentro del HTML) | En 4G, la gran mayoría del tráfico de Meta abandona antes de que cargue | No usar la portada como destino de anuncios. Llevar el tráfico a landings livianas (menos de 15 KB de HTML, como las de comuna) y, a mediano plazo, externalizar las imágenes de la portada (pasar QA con el skill `qa-web-averarq`) |
| **No existe una landing de "obra nueva / casa en parcela"** | El embudo de mayor ticket no tiene destino específico | Crear `/casa-en-tu-parcela` |
| **No existe una landing comercial** | El embudo comercial no tiene destino | Crear `/comercial` (locales, cambio de destino, patentes) |
| **Mensaje de portada genérico** ("Tu terreno, tu diseño, tu casa") | No diferencia frente a Hut, prefabricadas o Santiago | Reemplazar por la promesa de posicionamiento (§3.3) |
| Proyectos fuera del valle en la portada (Miami, La Dehesa) | Diluyen el mensaje "arquitecto del valle" | Mantenerlos como "también trabajamos fuera", pero después de los casos del valle |
| No hay reseñas ni testimonios visibles | Menos confianza para un cliente que llega frío desde un anuncio | Pedir reseña en Google a cada cliente cerrado y mostrar 3 testimonios en cada landing |

### 3.2 Fortalezas diferenciadoras (frente a la competencia detectada)

| Diferenciador | Frente a quién gana | Cómo se demuestra en un anuncio |
|---|---|---|
| **Conoce cada DOM del valle** y la normativa vigente (PREMVAL 2025, PRC locales, Zona Típica) | Premium de Santiago, directorios | "He tramitado en Catemu, Los Andes, Llay-Llay y Putaendo" + mapa de obras |
| **Diseño con identidad del valle** (ladrillo, madera, teja, criterio contemporáneo) | Prefabricadas, Hut (SIP), tramitadores | Render → obra ("transición de proyecto") |
| **Análisis técnico propio** (sol, viento, térmica, fuego, dron) | Todos | Reel de 20 s: "Así se mueve el sol sobre tu parcela en invierno" |
| **Precio de referencia en línea** (estimador en UF) | Todos, excepto planosdearquitectura.cl | Anuncio: "Calcula en 1 minuto cuánto cuesta diseñar tu casa" |
| **Acompañamiento hasta la recepción final**, con ITO y portal de seguimiento | Tramitadores, prefabricadas | "Tu proyecto con código de seguimiento: ves cada avance desde el celular" |
| **Patrimonio (DOM + CMN)** | Todos | Caso Lo Vicuña, Putaendo |

### 3.3 Posicionamiento de marca propuesto

**Declaración de posicionamiento (uso interno):**
> Para propietarios del Valle del Aconcagua que quieren construir, ampliar o regularizar sin perder tiempo ni dinero en la DOM, **Averarq** es la oficina de arquitectura local que une **diseño con identidad** y **tramitación sin sorpresas**, respaldada por **análisis técnico propio** y **acompañamiento hasta la recepción final**. A diferencia de las prefabricadas y los tramitadores, Averarq diseña; a diferencia de las oficinas de Santiago, conoce cada Dirección de Obras del valle.

**Promesa (cara al cliente):** **"Diseño con identidad. Permisos sin sorpresas."**
**Alternativas para A/B:** "Arquitectura del Valle, de principio a recepción." · "Tu casa, pensada para el valle y aprobada por la DOM."

**Pilares de mensaje** (todo contenido debe caer en uno):
1. **Territorio.** Conozco tu comuna, tu DOM y tu plan regulador.
2. **Evidencia.** Decido con datos: sol, viento, térmica, dron.
3. **Transparencia.** Precio de referencia en línea y avance visible.
4. **Acompañamiento.** Del primer plano a la recepción final.

**Tono:** primera persona ("yo diseño, yo tramito"), cercano, directo, técnico sin jerga. Siempre tuteo. Nada de "la casa de tus sueños".
**Visual:**
- Naranjo #FC4C02 como acento, nunca de fondo completo.
- Fotografía real de obra y dron por sobre el render genérico.
- Subtítulos siempre en los videos, porque la mayoría se ve sin sonido.
- Isotipo en la esquina, no en el centro.

---

## 4. Estrategia Meta Ads

### 4.1 Referencias de costo en Chile (fuentes al final)

| Métrica | Referencia | Fuente |
|---|---|---|
| CPM promedio Chile | ≈ **US$2,44** | Fuelads LatAm Q2-2026 |
| Evolución CPM | +20 % a +35 % en los últimos 2 años | Impulsados, Rableb |
| Estacionalidad | Noviembre-diciembre (Cyber y Navidad): +30 % a +80 % de CPM | Impulsados |
| Costo por mensaje (servicio profesional local, clínica dental en Providencia) | **$2.800 por conversación**, con 3–4 de cada 10 convirtiendo en cita | Impulsados |
| CPL inmobiliario (casas) | **$12.000–$25.000**. Proyectos nuevos: $15.000–$35.000 | Muller & Pérez |
| Inversión mínima recomendada | **$150.000/mes** (≈ $5.000/día). Rango para escalar: $300.000–$1.000.000/mes | Rableb |
| Presupuesto de prueba | $200.000–$300.000/mes. Meta recomienda US$15/día como mínimo y US$50/día para salir de la fase de aprendizaje | Impulsados |
| Formatos | Reels y stories tienen menor CPM que el feed. Un video que detiene el scroll puede bajar el CPM hasta un 40 % | Rableb |
| Gestión por agencia (referencia de costo evitado) | Desde $150.000/mes (Escalatunegocio) hasta $890.000/mes (Muller & Pérez) | Sitios de agencias |
| Facturación | Meta factura en CLP en Chile desde abril de 2026 | Chattigo |
| IVA | Los servicios digitales extranjeros pagan IVA del 19 % en Chile (Ley 21.210) | — |

**Hipótesis de trabajo para Averarq** (a validar en las semanas 1–4):
- **Costo por conversación de WhatsApp de $3.000–$6.000.** Es algo mayor que el de la clínica dental porque el público es de nicho y la audiencia regional es más chica.
- **Costo por lead con formulario o landing de $12.000–$25.000**, alineado con el inmobiliario de casas.

### 4.2 Públicos objetivo y propuesta de valor

| | **A · Regularización** | **B · Casa en tu parcela** | **C · Comercial / equipamiento** |
|---|---|---|---|
| **Quién** | Propietario de 35–65 años con ampliación o casa sin permiso o sin recepción. Detonantes: vender, crédito hipotecario, herencia, subsidio, multa | Propietario de 30–60 años con sitio o parcela de agrado sin construir. Local, o residente de Santiago o Gran Valparaíso con segunda vivienda en el valle | Dueño de local, restaurante, bodega, taller u oficina. Pyme que necesita patente, cambio de destino o remodelación. Pequeño inversionista (strip center, equipamiento) |
| **Dolor** | "No puedo vender ni pedir crédito porque la casa no está regularizada" | "No sé qué puedo construir en mi parcela, cuánto cuesta ni por dónde empezar" | "No me dan la patente sin recepción" / "Quiero abrir, pero el local no tiene destino comercial" |
| **Propuesta de valor** | Te digo con franqueza por dónde va tu caso y lo dejo resuelto ante la DOM, con Ley del Mono si aplica | Diseño tu casa para tu parcela, con estudio de sol y levantamiento con dron, y la acompaño hasta la recepción final | Resuelvo la parte de arquitectura para que abras con patente: regularización, cambio de destino y diseño interior |
| **Oferta de entrada** | **Diagnóstico por WhatsApp en 24 h** (gratis) | **Estimador de honorarios + reunión gratuita de 30 min**. Imán a futuro: "Estudio de asoleamiento de tu parcela" | **Revisión de factibilidad del local** (gratis) |
| **Destino** | WhatsApp directo (click-to-WhatsApp) | Landing `/casa-en-tu-parcela` con estimador → WhatsApp | Landing `/comercial` o formulario instantáneo |
| **Ticket de referencia** | $650.000–$1.800.000 (mercado) | 120 m² × 1,0 UF = 120 UF ≈ **$4,9 millones** (tarifa actual del estimador) | Variable. Restobar de 110 m² como referencia |
| **Peso en el presupuesto** | 45 % | 40 % | 15 % |

### 4.3 Creatividades y copys listos para usar

> Formato general: 9:16 (reels y stories) + 4:5 (feed). Subtítulos siempre. Primeros 2 segundos con gancho visual (dron, antes/después, plano sobre terreno). Máximo 20–30 s.

#### Público A — Regularización

**Creatividades:**
- **A1. Carrusel antes/después** (5 láminas): foto de la ampliación → levantamiento as-built → plano → certificado de recepción → "Casa en regla". Caso: La Parva, Los Andes.
- **A2. Reel "3 señales de que tu casa no está regularizada"** (Alejandro a cámara, 20 s).
- **A3. Imagen fija de urgencia:** "Ley del Mono: el plazo vigente vence el 31-dic-2027".

**Copy A-1 (dolor / venta):**
> ¿Quieres vender tu casa y el banco te pidió la recepción final? 🏠
> Una ampliación sin permiso puede frenar la venta, el crédito o la herencia.
> Soy arquitecto en el Valle del Aconcagua y regularizo ante la DOM de San Felipe, Los Andes, Llay-Llay, Catemu y Rinconada, incluida la Ley del Mono cuando aplica.
> Escríbeme y en 24 h te digo por dónde va tu caso.
> **CTA:** Enviar mensaje (WhatsApp)

**Copy A-2 (urgencia legal, sin exagerar):**
> La Ley del Mono tiene plazo: hoy está vigente hasta el 31 de diciembre de 2027.
> Si construiste un dormitorio, un segundo piso o un quincho sin permiso, este es el camino más simple para ponerlo en regla.
> Revisamos tu caso gratis por WhatsApp. Arquitecto PUCV con base en Llay-Llay.
> **CTA:** Enviar mensaje

**Copy A-3 (franqueza / confianza):**
> Casi todo es regularizable. Lo que cambia es el camino.
> Depende de la antigüedad, la superficie y lo que permite tu plan regulador. Mi trabajo es leer tu caso, decirte la verdad y dejarlo resuelto hasta la recepción final.
> 📍 Valle del Aconcagua · Putaendo (incluye zona típica) · La Calera
> **CTA:** Enviar mensaje

*Variante geolocalizada para La Calera (El Trigal y Entrepuentes):* "Con el nuevo Plan Regulador, tu sector salió de la zona de restricción. Ahora sí puedes regularizar tu casa."

#### Público B — Casa en tu parcela

**Creatividades:**
- **B1. Reel con dron:** vuelo sobre una parcela real → superposición del volumen de la casa → render → obra (Casa San Carlos, Catemu). Texto en pantalla: "De tu parcela a tu casa".
- **B2. Reel del Solar Lab:** trayectoria solar sobre la parcela en junio y diciembre → "así decido dónde van el living y los dormitorios".
- **B3. Carrusel "5 cosas que debes saber antes de construir en tu parcela"** (PREMVAL 2025, rol y subdivisión, factibilidad sanitaria, acceso, orientación). La última lámina dirige al estimador.
- **B4. Carrusel de proyectos del valle** (San Carlos, La Colonia, Doble L, Casa 31) con comuna y m² visibles.

**Copy B-1 (autoridad técnica):**
> Antes de dibujar tu casa, estudio cómo se mueve el sol sobre tu parcela. ☀️
> Levantamiento con dron, estudio de asoleamiento y diseño con identidad del valle: ladrillo, madera y teja con criterio contemporáneo.
> Y te acompaño hasta la recepción final en la DOM.
> Calcula en 1 minuto una referencia de honorarios 👇
> **CTA:** Más información → /casa-en-tu-parcela

**Copy B-2 (transparencia de precio):**
> ¿Cuánto cuesta diseñar una casa? Sin letra chica.
> En mi web tienes un estimador en UF: eliges superficie y nivel de detalle y ves una referencia al instante. Incluye visitas a terreno y levantamiento con dron.
> Arquitecto en Llay-Llay · Todo el Valle del Aconcagua.
> **CTA:** Calcular ahora

**Copy B-3 (segunda vivienda, público de Santiago):**
> Tienes la parcela en el valle. Yo estoy aquí.
> Diseño tu casa en San Felipe, Putaendo, Catemu o Los Andes y tú sigues cada avance desde tu celular con un código de proyecto. Visitas de obra semanales, informes con dron y tramitación con la DOM local.
> **CTA:** Enviar mensaje

#### Público C — Comercial / equipamiento

**Creatividades:**
- **C1. Antes/después del Restobar Esmeralda** (Los Andes): reel de 15 s.
- **C2. Imagen fija "¿Te piden recepción final para la patente?"**
- **C3. Render del Stripcenter La Perla** como prueba de escala (solo en retargeting).

**Copy C-1:**
> ¿Te piden recepción final para sacar la patente? 🧾
> Regularizo locales, gestiono cambios de destino y diseño el interior de tu negocio para que abras en regla.
> Ejemplo: Restobar Esmeralda, Los Andes (110 m²).
> **CTA:** Enviar mensaje

**Copy C-2:**
> Abrir un local sin la arquitectura en regla sale caro: clausuras, multas, patente rechazada.
> Revisamos la factibilidad de tu local gratis antes de que firmes el arriendo.
> Arquitecto en el Valle del Aconcagua.
> **CTA:** Solicitar revisión

**Copy C-3:**
> Del local vacío al negocio funcionando: diseño interior, remodelación y permisos en un solo equipo.
> San Felipe · Los Andes · Llay-Llay · Quillota · La Calera.
> **CTA:** Más información → /comercial

### 4.4 Estructura de campañas en el Administrador de anuncios

**Configuración de cuenta (semana 0):**
- Portfolio comercial (Business Manager) con dominio averarq.cl verificado.
- Página de Facebook y cuenta de Instagram @averarq vinculadas.
- WhatsApp Business conectado.
- Pixel en todas las landings.
- Método de pago en CLP.
- Si Meta marca algún anuncio en una *categoría especial* (vivienda), aceptar las restricciones de segmentación (edad, radio mínimo) y no intentar evadirlas.

| Campaña | Objetivo Meta | Conjuntos de anuncios | Ubicación geográfica | Optimización |
|---|---|---|---|---|
| **C1 · REG-Valle** | Interacción → Mensajes (WhatsApp) | 1) Valle alto: San Felipe, Los Andes, Putaendo, Santa María, Calle Larga, San Esteban, Rinconada, Panquehue. 2) Valle bajo: Llay-Llay, Catemu, Hijuelas, La Calera, Quillota, La Cruz, Nogales | Por comuna, más un radio de unos 15 km alrededor de Llay-Llay, San Felipe y Los Andes | Conversaciones iniciadas |
| **C2 · CASA-Parcela** | Clientes potenciales (web) o Tráfico mientras el Pixel acumula datos | 1) Valle: todas las comunas de cobertura. 2) **Santiago oriente/norte** (prueba desde el mes 2): público de segunda vivienda | Valle por comuna. Región Metropolitana solo en su conjunto de prueba | Fase 1: clics en enlace o vistas de página de destino → desde unas 50 conversiones/semana: evento `Lead` o `Contact` |
| **C3 · MARCA-Video** | Reconocimiento → ThruPlay | Todo el valle y la costa (Viña, Valparaíso, Concón) en rotación | Región de Valparaíso | ThruPlay (alimenta los públicos de retargeting) |
| **C4 · RETARGETING** | Mensajes o Clientes potenciales | Visitantes web (30–90 días), personas que interactuaron con IG/FB (90 días), quienes vieron el 50 % de un video (60 días) | Igual que C1 + C2 | Conversaciones o Lead |
| **C5 · COMERCIAL** | Mensajes o Formulario instantáneo | Toda la cobertura, con segmentación amplia (Advantage+ audiencia) | Valle + Quillota + La Calera | Conversaciones |

**Criterios de segmentación:**
- Priorizar **segmentación amplia con Advantage+ audiencia** y dejar que la creatividad filtre al público. Los copys mencionan la comuna y el problema.
- Excluir a los clientes actuales (lista subida desde el Organizador).
- Público similar (lookalike) del 1 % desde clientes y leads en cuanto haya más de 100 registros.
- Edad 30–65. En público A, sin límite superior si Meta lo permite.

**Nomenclatura:** `AVQ_{Público}_{Objetivo}_{Geo}_{Creatividad}_{AAAAMM}`, por ejemplo `AVQ_REG_MSG_VALLEALTO_A1carrusel_202610`.

**UTM y atribución:**
- Todas las URL llevan `?utm_source=meta&utm_medium=paid&utm_campaign={campaign.name}&utm_content={ad.name}`.
- Los mensajes precargados de WhatsApp llevan un código corto, por ejemplo "Hola Averarq, vi su anuncio [REG1]", para registrar la fuente en el Organizador.

### 4.5 Presupuesto por fase (escenario medio: $300.000/mes; los otros escenarios, a escala en §6)

| Fase | Días | Presupuesto diario | C1 REG | C2 CASA | C3 MARCA | C4 RETARG | C5 COM | Regla de decisión |
|---|---|---|---|---|---|---|---|---|
| **Lanzamiento** | 1–30 | ≈ $10.000/día | 45 % | 35 % | 20 % | — (no hay audiencia aún) | — | Sin tocar nada durante 7 días. Apagar anuncios con CTR de enlace < 0,8 % después de más de 3.000 impresiones |
| **Optimización** | 31–60 | ≈ $10.000/día | 40 % | 30 % | 10 % | 15 % | 5 % | Mantener las 2 mejores creatividades por público. Crear 2 nuevas cada 2 semanas. Activar la prueba de Santiago en C2 |
| **Escalamiento** | 61–90 | $10.000 → $13.000/día (+20 % semanal si el costo por lead calificado se mantiene) | 35 % | 35 % | 10 % | 15 % | 5 % | Escalar solo lo que tenga costo por lead calificado ≤ objetivo (§4.7). No escalar en noviembre-diciembre si el CPM sube más del 30 % |

### 4.6 Embudo completo

```
ANUNCIO (reel / carrusel / imagen)
   │  código de campaña en el mensaje de WhatsApp + UTM en la URL
   ▼
DESTINO
   A · WhatsApp directo con mensaje precargado ("…[REG1]")
   B · /casa-en-tu-parcela → estimador → botón WhatsApp o formulario
   C · /comercial o formulario instantáneo de Meta
   │  Eventos del Pixel: PageView · ViewContent (usó el estimador) · Contact (clic en WhatsApp) · Lead (formulario)
   ▼
PRIMER CONTACTO (menos de 1 h en horario hábil; respuesta automática fuera de horario)
   Respuesta rápida de WhatsApp con 4 preguntas de calificación:
   1) Comuna y dirección aproximada  2) ¿Obra nueva, ampliación, regularización o comercial?
   3) Superficie aproximada  4) ¿Tiene rol SII, escritura y CIP?
   → Se registra en el Organizador (Fuente = "Meta Ads" + código)
   ▼
CALIFICACIÓN
   ✔ Calificado: dentro de la cobertura, con antecedentes o con decisión en menos de 6 meses → llamada de 15 min
   ✘ No calificado: fuera de zona o solo "cotizando precio" → enviar el estimador y una guía PDF, sin perseguir
   ▼
REUNIÓN / VISITA A TERRENO (gratuita, 30–45 min) con dron si aplica
   ▼
PROPUESTA DE HONORARIOS en 48 h (PDF con marca, skill carta-averarq) en UF, por etapas
   ▼
SEGUIMIENTO día 2 · día 7 · día 14 (WhatsApp) → CIERRE → código de /seguimiento
   ▼
POST-VENTA: pedir reseña en Google al cierre de cada etapa + autorización para usar el caso en contenido
```

**Configuración técnica del Pixel** (semana 0; el código del Pixel se pega en el `<head>` de cada landing):
- `Contact`: se dispara en el clic a `wa.me/...`.
- `ViewContent`: se dispara cuando el usuario cambia la superficie en el estimador.
- `Lead`: se dispara al enviar un formulario, si se crea uno.
- **Conversions API** opcional a futuro (vía Cloudflare Worker, que ya se usa para el Organizador).
- **Privacidad:** agregar un aviso de privacidad y cookies. La Ley 21.719 de protección de datos personales entra en vigor el **1-dic-2026** (verificar la fecha exacta), así que conviene dejarlo resuelto antes.

### 4.7 Métricas de éxito y reporte

| Nivel | Métrica | Objetivo inicial (hipótesis, se recalibra el día 30) |
|---|---|---|
| Anuncio | CTR de enlace | ≥ 1,0 % |
| Anuncio | Retención de video a 3 s (hook rate) | ≥ 25 % |
| Anuncio | Frecuencia (7 días) | ≤ 3,0 (sobre eso, rotar creatividad) |
| Costo | Costo por conversación de WhatsApp (A, C) | ≤ $6.000 |
| Costo | Costo por lead en landing (B) | ≤ $20.000 |
| Calidad | % de leads calificados | ≥ 30 % |
| Comercial | Lead calificado → visita o reunión | ≥ 40 % |
| Comercial | Propuesta → cierre | ≥ 25 % |
| Negocio | **CAC** (inversión ÷ proyectos cerrados) | ≤ 10 % de los honorarios del proyecto |
| Negocio | **ROAS de honorarios** (honorarios firmados ÷ inversión) | ≥ 5× a los 90 días |
| Marca | Reseñas en Google | +4 por mes |
| Marca | Seguidores de IG del valle y búsquedas de "Averarq" | Tendencia creciente mes a mes |

**Frecuencia de reporte (Alejandro):**
- **Diario (5 min):** responder WhatsApp y registrar en el Organizador.
- **Lunes (20 min):** panel del Administrador de anuncios (gasto, CPM, CTR, costo por resultado) + embudo del Organizador (leads → calificados → visitas → propuestas → cierres). Decidir qué apagar y qué duplicar.
- **Mensual (1 h):** informe de una página (CAC, ROAS de honorarios, aprendizajes, creatividades ganadoras, próximo mes).
- **Trimestral (2 h):** revisar posicionamiento, precios (UF/m²) y la matriz de competencia (volver a correr el protocolo §2.4).

---

## 5. Plan de ejecución — 6 meses (responsable único: Alejandro)

**Dedicación estimada:** 6–8 h/semana, que se reducen a 4–5 h/semana una vez en régimen.
**Método de producción por lotes:** un día al mes de grabación (dron + obra + cámara) rinde 8–12 piezas.

### Semana 0 — Preparación (28-sep → 4-oct-2026)

| Qué se produce | Qué se activa | Qué se mide |
|---|---|---|
| Completar el protocolo de competencia §2.4 · Crear `/casa-en-tu-parcela` (liviana, con estimador, casos del valle y botón de WhatsApp) · Actualizar el titular de la portada con la nueva promesa · Mensajes de WhatsApp con código por campaña | Portfolio comercial, verificación de dominio, Pixel + eventos, WhatsApp Business (respuestas rápidas, horario, mensaje de ausencia) · Perfil de empresa en Google con las 10 fotos mejores y el área de servicio | Probar los eventos del Pixel con la herramienta de prueba de eventos · Registrar la línea base: seguidores, reseñas, consultas/mes actuales |

### Mes 1 — Lanzamiento (octubre 2026)

| Semana | Produce | Publica (orgánico IG/FB, 3×/semana) | Activa en Ads | Mide |
|---|---|---|---|---|
| S1 (5–11 oct) | Jornada de grabación 1: dron sobre Casa San Carlos y Casa La Colonia, Alejandro a cámara (A2, B1) · Carrusel A1 (La Parva) | Presentación "Quién soy y dónde trabajo" · A1 · B4 | **C1 REG** (A1, A2, A3) + **C2 CASA** (B1, B2) + **C3 MARCA** (B1) — ≈ $10.000/día | Solo verificar la entrega. No optimizar |
| S2 (12–18) | Reel del Solar Lab (B2) · Carrusel B3 | B2 · B3 · caso Lo Vicuña, Putaendo | Sin cambios (fase de aprendizaje) | Costo por conversación preliminar |
| S3 (19–25) | Guía PDF "Regularizar tu casa en el valle: 7 pasos" (para no calificados) | Reel "3 señales" · C1 Restobar | Apagar los anuncios con CTR < 0,8 %. Sumar A2-copy2 | CTR, hook rate, % calificados |
| S4 (26 oct–1 nov) | Informe mensual 1 | Testimonio (si hay) · Proceso de regularización | Redistribuir hacia el público con menor costo por lead calificado | **Informe mes 1:** fijar los objetivos reales de costo por lead |

### Mes 2 — Optimización (noviembre 2026)

| Semana | Produce | Publica | Activa en Ads | Mide |
|---|---|---|---|---|
| S5 | Jornada de grabación 2: obra en curso + regularización en terreno | Avance de obra (ITO) · "Qué es la Ley del Mono" | **C4 RETARGETING** (visitantes web + video al 50 %) · **C5 COMERCIAL** (C1, C2) | Tamaño de las audiencias de retargeting |
| S6 | Landing `/comercial` | Caso comercial · PREMVAL explicado | Prueba de C2 en **Santiago** (B3), $2.000/día | Costo por lead Santiago vs. valle |
| S7 | 2 creatividades nuevas (renovar la ganadora) | Antes/después · FAQ de honorarios | Cyber: si el CPM sube más del 30 %, bajar C3 y proteger C1 y C4 | CPM semanal |
| S8 | Informe mensual 2 | Reseña de cliente | Apagar el conjunto de Santiago si el costo por lead supera 1,5 veces el del valle | **Informe mes 2** |

### Mes 3 — Escalamiento (diciembre 2026)

| Semana | Produce | Publica | Activa en Ads | Mide |
|---|---|---|---|---|
| S9 | Jornada de grabación 3: resumen del año, obras terminadas | "Mi año en el valle" (reel) | +20 % en los conjuntos ganadores (si el CPM está estable) | Costo por lead tras escalar |
| S10 | Microcampaña de La Calera (El Trigal y Entrepuentes) | Oportunidad PRC La Calera | Conjunto geolocalizado en La Calera dentro de C1 | Conversaciones en La Calera |
| S11–S12 | Informe trimestral · Revisión de tarifa UF/m² | Contenido liviano (fiestas) | Mantener el presupuesto, sin escalar en semanas de Navidad | **Revisión de 90 días:** CAC, ROAS de honorarios, decisión de escenario para el primer semestre de 2027 |

### Meses 4–6 — Consolidación (enero → marzo 2027)

| Mes | Produce | Publica | Activa en Ads | Mide |
|---|---|---|---|---|
| **Enero** | Imán de leads: **"Estudio de asoleamiento express de tu parcela"** (versión simplificada del Solar Lab, entregado en PDF) · Jornada de grabación 4 | Serie "Parcelas del valle" (1 por semana: Putaendo, San Felipe, Catemu, Rinconada) | C2 con el imán como oferta (formulario instantáneo) · Retargeting permanente · Escalamiento a $13.000/día si el ROAS de honorarios es mayor o igual a 5× | Costo por lead del imán vs. el del estimador |
| **Febrero** | Landing y campaña **Putaendo** (patrimonio + parcelas) · Casos documentados (3) | Serie Putaendo · Proceso DOM + CMN | Conjunto Putaendo dedicado · Público similar del 1 % de clientes (si hay más de 100 registros) | Costo por lead en Putaendo y conversaciones patrimoniales |
| **Marzo** | Informe semestral · Actualizar la matriz de competencia (§2.4) · Estado del proyecto de la Ley del Mono en el Senado | Resultados: "X casas en regla, Y proyectos en diseño" | Si se aprueba el tope de 2.000 UF o el plazo 2029: **campaña especial REG** el mismo día con copys ya preparados · Plan del segundo semestre | **Informe semestral:** CAC, ROAS de honorarios, reseñas, posición en Google Maps, decisión de escenario |

### Hitos de la visión a 24 meses

| Plazo | Hito |
|---|---|
| 6 meses | Embudos medidos y rentables (ROAS de honorarios ≥ 5×) · 25 o más reseñas · Landings de parcela, comercial y Putaendo operativas |
| 12 meses | Top 3 en Google Maps para "arquitecto" en San Felipe, Los Andes y Llay-Llay · Imán de asoleamiento consolidado · Más de 10 proyectos/año por canal digital · Tarifa revisada (1,2–1,4 UF/m²) |
| 24 meses | Referente regional: más de 50 reseñas, más de 20 proyectos/año por canal digital, presencia en Quillota y La Calera y en la costa (Viña y Concón) con casos propios · Evaluar sumar un colaborador para dibujo y tramitación |

---

## 6. Presupuesto estimado (CLP)

### 6.1 Inversión en medios (Meta)

| Escenario | Mensual (neto) | IVA 19 % | Mensual con IVA | **6 meses con IVA** | Cuándo elegirlo |
|---|---|---|---|---|---|
| **Bajo** | $150.000 | $28.500 | $178.500 | **$1.071.000** | Mínimo recomendado para Chile. Aprendizaje lento: solo C1 y C2, sin prueba en Santiago |
| **Medio (recomendado)** | $300.000 | $57.000 | $357.000 | **$2.142.000** | Permite los 5 conjuntos, retargeting y la prueba en Santiago |
| **Alto** | $600.000 | $114.000 | $714.000 | **$4.284.000** | Solo si el ROAS de honorarios a 90 días es mayor o igual a 5× y hay capacidad para atender más proyectos |

*Referencias:*
- El mínimo recomendado para Chile es de $150.000/mes, y el rango para escalar va de $300.000 a $1.000.000/mes (Rableb).
- El presupuesto de prueba típico es de $200.000–$300.000/mes (Impulsados).

### 6.2 Proyección de resultados (escenario medio; hipótesis a validar)

| Supuesto | Valor |
|---|---|
| Inversión mensual | $300.000 |
| Distribución | ≈ 55 % en mensajes (C1 + C5 + parte de C4), ≈ 35 % en leads (C2) y ≈ 10 % en marca |
| Conversaciones de WhatsApp (a $3.000–$6.000) | 27–55 al mes |
| Leads desde landing (a $12.000–$25.000) | 4–9 al mes |
| Leads calificados (30 %) | 9–19 al mes |
| Cierres (40 % visita × 25 % cierre ≈ 10 % de los calificados) | **1–2 proyectos al mes** |
| Honorarios por proyecto | Regularización ≈ $650.000–$1.800.000 (mercado) · Diseño de 120 m² ≈ $4,9 millones |

### 6.3 Punto de equilibrio

Con el escenario medio ($357.000/mes con IVA), se cubre la inversión con cualquiera de estos resultados:
- **1 regularización al mes** de alrededor de $650.000 (el mínimo del rango de mercado).
- **1 proyecto de diseño de 120 m² cada 6 meses.**

### 6.4 Otros costos (no son medios)

| Ítem | Costo | Comentario |
|---|---|---|
| Producción de contenido | Tiempo propio (4 jornadas de grabación + 6–8 h/semana) | Ya cuenta con dron y herramientas propias |
| Gestión de campañas | Tiempo propio | El costo evitado frente a una agencia va de $150.000 a $890.000/mes |
| Edición de video (opcional) | A cotizar con un editor freelance por pieza | Recomendable solo si el tiempo se vuelve el cuello de botella |
| Fotografía profesional de obra terminada (opcional) | A cotizar por sesión | Una vez por obra terminada: sirve para años de contenido |

---

## 7. Checklist de arranque (imprimible)

- [ ] Protocolo de competencia §2.4 completado (Biblioteca de Anuncios + IG + Google Maps)
- [ ] Portfolio comercial + dominio verificado + Pixel con eventos `Contact`, `ViewContent` y `Lead` probados
- [ ] Landing `/casa-en-tu-parcela` publicada (peso < 1 MB, QA con `qa-web-averarq`)
- [ ] Portada: nueva promesa + aviso de privacidad. Plan para sacar las imágenes base64 (17 MB → < 2 MB)
- [ ] WhatsApp Business: respuestas rápidas con las 4 preguntas, mensaje de ausencia, etiquetas por embudo
- [ ] Organizador: opción "Meta Ads" en el campo Fuente + códigos de campaña
- [ ] Perfil de empresa en Google completo + enlace para pedir reseñas
- [ ] Jornada de grabación 1 lista (A1, A2, B1, B2)
- [ ] Campañas C1, C2 y C3 creadas con la nomenclatura y las UTM
- [ ] Recordatorio en el calendario: lunes 20 min de reporte, fin de mes 1 h de informe

---

## Fuentes

**Competencia**
- Hut Arquitectura — https://hut.cl/ · http://hut.cl/servicios/
- Domus Eaton — https://www.domuseaton.cl/ · https://www.facebook.com/domuseatonarquitectura/ · https://x.com/domuseaton1 · https://cibec.cl/domus-eaton-arquitectura-y-construcci-n-17177835837754726789/
- Moreno·Sosa Arquitectos — https://morenososa.com/en/ · https://www.instagram.com/reel/C4stbXpO2dW/
- Loi Arquitectos — https://loi.cl/quienes-somos/
- ANDES Arquitectos y Asociados — https://www.arqandes.cl/
- Andes Arquitectura y Construcción — https://empresas.habitissimo.cl/pro/andes-arquitectura-construccion · https://www.2x3.cl/profesional/andes-arquitectura-y-construccion
- Tu Solución Diseño y Arquitectura (San Felipe) — http://arquitecturachile.cl/arquitecto%20san%20felipe.htm
- planosdearquitectura.cl — https://planosdearquitectura.cl/ · https://planosdearquitectura.cl/la-ley-del-mono-actualizada/
- RA® Regularizarquitectos — https://www.instagram.com/regularizarquitectos.cl/
- Prefabricadas locales — https://www.facebook.com/constructoraLN/ · https://www.facebook.com/p/Casas-prefabricadas-San-Felipe-100063484719838/ · https://www.facebook.com/CasasPrefabricadasProChile/
- Estudio LAC — https://www.estudiolac.cl/oficina
- Regularización en Gran Valparaíso — https://es.slideshare.net/ClculoEstructuralArq/regularizaciones-ley-del-mono-valparaso-56941055309 · https://slideshare.net/ArquitectoCatapilco/regularizaciones-ley-del-mono-valparaiso
- Costa norte — https://woodarch.cl/portfolio_page/oficina-nos-arquitectura-zapallar/ · https://lfgrez.cl/
- Directorios — https://empresas.habitissimo.cl/arquitectos/san-felipe-de-aconcagua/san-felipe · https://empresas.habitissimo.cl/arquitectos/san-felipe-de-aconcagua · https://www.fixando.cl/15/Quillota/1145/servicios-arquitectonicos
- Colegio de Arquitectos Aconcagua — https://www.instagram.com/ca_aconcagua/

**Costos de Meta Ads y marketing en Chile**
- Impulsados — https://impulsados.cl/costo-publicidad-instagram-facebook-chile/ · https://impulsados.cl/presupuesto-anunciarse-facebook-ads/
- Rableb — https://rableb.com/guias/cuanto-cuesta-anunciar-en-meta/ · https://rableb.com/guias/presupuesto-minimo-para-meta-ads/
- Fuelads, benchmarks LatAm Q2-2026 — https://fuelads.tech/benchmarks-latam-2026
- Muller & Pérez — https://www.mulleryperez.cl/blog/marketing-inmobiliario-agencia-marketing-digital-chile-2025 · https://www.mulleryperez.cl/servicios/facebook-ads-chile
- Escalatunegocio (precios de agencia) — https://escalatunegocio.cl/precios
- Chattigo (facturación en CLP y WhatsApp) — https://blog.chattigo.com/whatsapp-business/cuanto-cobra-whatsapp-business-por-mensaje
- Biblioteca de Anuncios de Meta — https://www.facebook.com/ads/library/

**Normativa y mercado**
- Ley del Mono, proyecto 2026 — https://www.biobiochile.cl/noticias/servicios/explicado/2026/08/20/ley-del-mono-como-regularizar-tu-vivienda-y-cuales-son-los-cambios-que-propone-nuevo-proyecto.shtml · https://g5noticias.cl/2026/09/08/nueva-ley-del-mono-avanza-a-su-debate-en-particular/ · https://www.diarioconstitucional.cl/2026/04/19/proyecto-de-ley-extiende-la-ley-del-mono-hasta-2030-e-incorpora-procedimiento-de-subsanacion/ · https://calculaobrachile.com/guias/ley-del-mono-chile/
- PREMVAL Satélite Alto Aconcagua — https://www.bcn.cl/leychile/navegar?idNorma=1213758 · https://www.elaconcagua.cl/2025/05/31/entro-en-vigencia-modificacion-del-plan-regulador-metropolitano-valparaiso-satelite-alto-aconcagua/
- Honorarios de arquitecto — https://materiaestates.com/blog/honorarios-arquitecto-vivienda-unifamiliar/ · https://scsarquitecto.cl/valores-referenciales-cobro-honorarios-arquitectos/
- Parcelas en el valle — https://casas.mitula.cl/casas/terrenos-agrado-putaendo · https://listado.mercadolibre.cl/parcelas-de-agrado-san-felipe
- Valor UF — https://www.uf-hoy.com/ · https://patrimore.com/herramientas/valor-de-la-uf
