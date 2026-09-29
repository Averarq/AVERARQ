# Animaciones técnicas AVERARQ

## DET. 01 · Albañilería confinada (feed 4:5)

- **Video para el feed:** `albanileria-confinada-4x5.mp4`. 1080×1350, 34,5 s, 30 fps, H.264. Es la resolución máxima que Instagram y Facebook muestran en 4:5. Se dibuja a 2160×2700 y se reduce con filtro Lanczos (sobremuestreo), así que las líneas finas quedan limpias y sin pixelado. **Este es el que se sube.**
- **Video maestro:** `albanileria-confinada-4x5-2160.mp4`. 2160×2700, misma animación, para la web, presentaciones o pantalla grande.
- **Portada:** `albanileria-confinada-portada.jpg` (2160×2700), el cuadro final del detalle. Úsala como miniatura del reel o del anuncio.

**Secuencia (8 etapas):**
1. Trazado y excavación
2. Emplantillado
3. Armadura de pilares
4. Cimiento corrido
5. Sobrecimiento
6. Muro de ladrillo con endentado y escalerillas cada 4 hiladas
7. Pilares de H.A.
8. Cadena de H.A.

Al final aparece una contraportada con la llamada a la acción: "¿Vas a construir en el valle? Háblanos.", averarq.cl, @averarq y WhatsApp. Queda como último cuadro.

Niveles del detalle: fondo de excavación −0,65 · sobrecimiento +0,30 · muro de ladrillo hasta +2,20 (22 hiladas) · cadena de coronación hasta +2,50. Todas las dimensiones son **referenciales**, y la animación lo indica en la nota al pie.

### Texto sugerido para la publicación

> ¿Qué hay dentro de un muro de albañilería confinada? 🧱
> Del suelo a la cadena, en 8 pasos:
> 1️⃣ Trazado y excavación · 2️⃣ Emplantillado · 3️⃣ Armadura de pilares · 4️⃣ Cimiento corrido · 5️⃣ Sobrecimiento · 6️⃣ Muro de ladrillo con escalerillas · 7️⃣ Pilares de hormigón armado · 8️⃣ Cadena
> La clave: primero se levanta el muro y después se hormigonan pilares y cadenas contra él. El endentado traba ambos materiales y el muro trabaja en conjunto.
> ¿Vas a construir en el Valle del Aconcagua? Diseño, permisos y construcción hasta la recepción final. Escríbeme 👉 averarq.cl
> #arquitectura #construccion #albañileriaconfinada #detalleconstructivo #valledelaconcagua #sanfelipe #losandes #llayllay

**Como anuncio:** úsalo en la campaña de marca (C3 · ThruPlay). Así llena el público de retargeting con personas interesadas en construir.

### Editar o regenerar

```
cd _fuente
node render-video.mjs --fotos 9 18 28   # cuadros sueltos para revisar
node render-video.mjs                   # video maestro 2160 + feed 1080 (~8 min)
```

- La escena está en `_fuente/albanileria-confinada.html`: geometría en cm, textos de cada etapa en `ET` y tiempos en segundos.
- Requiere Playwright y ffmpeg con libx264 (`pip install imageio-ffmpeg`).
- Para crear otro detalle (por ejemplo tabiquería, radier o techumbre), copia el HTML y cambia la geometría.
