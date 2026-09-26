# -*- coding: utf-8 -*-
"""
extraer_secuencias.py — prepara el material de V5 con la línea visual AVERARQ.

1. Tramos de video (dron 4K, celular, recorrido): corta, encuadra en vertical
   1080×1920 a 30 fps y guarda JPG numerados en secuencias/<nombre>/0001.jpg …
2. Imágenes fijas (renders y fotos de dron): las guarda en secuencias/_fijas/.

A todo le aplica la misma LUT de color (color/averarq.cube). El video del iPhone
viene en HDR (HLG, BT.2020) y se convierte a SDR antes de la LUT.
secuencias/ está fuera de git: se regenera con este script.

Uso:
    python3 extraer_secuencias.py          # lo que falte
    python3 extraer_secuencias.py --forzar # rehace todo (p. ej. tras cambiar la LUT)

Requiere ffmpeg (con zscale). Las rutas apuntan a las carpetas de proyecto en el
PC de Alejandro; si cambian, edita PROYECTO.
"""
import os, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, 'secuencias')
PROYECTO = r'C:/Users/Alejandro Vera/Documents/0.AVERARQ/2025/2025_Andrés Martinez'
ORIGEN = PROYECTO + '/audiovisual'
LUT = 'color/averarq.cube'   # relativa a AQUI (ffmpeg corre con cwd=AQUI)
FPS = 30

HDR_A_SDR = ('zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=203,format=gbrpf32le,'
             'zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p')

# nombre: (archivo, inicio s, duración s, centro del encuadre al inicio y al final [0-1] o None si ya es vertical,
#          ajuste previo de exposición/contraste para igualar fuentes)
TRAMOS = {
    'sc-orbita':    ('DJI_20260818111851_0106_D.MP4', 3.0, 4.2, 0.52, 0.52, 'eq=brightness=0.0'),
    # Alejandro recibe el dron en la mano; corta a los 24,4 s, antes de que sonría
    'sc-dron-mano': ('IMG_5241.MOV', 20.4, 4.0, None, None, 'eq=brightness=0.03:contrast=0.97'),
    'sc-alero':     ('compose_video_1787102807464.mp4', 81.4, 1.4, None, None, 'eq=contrast=0.97'),
    'sc-techumbre': ('compose_video_1787102807464.mp4', 85.4, 1.4, None, None, 'eq=contrast=0.97'),
    'sc-estar':     ('compose_video_1787102807464.mp4', 65.4, 1.4, None, None, 'eq=contrast=0.97'),
}

# imágenes fijas: nombre de salida → (ruta dentro del proyecto, ajuste previo)
FIJAS = {
    'render-aereo': ('/RENDERS/Escena 4.png', 'eq=saturation=0.92:contrast=1.03'),
    'dron-oblicua': ('/audiovisual/DJI_20260818111940_0108_D.JPG', 'eq=brightness=0.0'),
    'axonometrica': ('/portafolio/2026_am3.png', 'eq=saturation=0.95'),
    'dron-cenital': ('/audiovisual/DJI_20260818111726_0098_D.JPG', 'eq=brightness=0.0'),
}


def info(ruta):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=width,height,color_transfer', '-of', 'csv=p=0', ruta]).decode()
    w, h, tr = (out.strip().split(',') + [''])[:3]
    return int(w), int(h), tr


def ffmpeg(args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, check=True, cwd=AQUI)


def extraer(nombre, archivo, inicio, dur, c0, c1, ajuste, forzar):
    dst = os.path.join(SALIDA, nombre)
    if os.path.isdir(dst) and os.listdir(dst) and not forzar:
        print('--', nombre, '(ya existe)')
        return
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    ruta = os.path.join(ORIGEN, archivo)
    w, h, tr = info(ruta)
    cadena = [HDR_A_SDR] if tr == 'arib-std-b67' else []
    cadena.append('fps=%d' % FPS)
    if c0 is not None:
        cw = round(h * 9 / 16)
        # el centro del encuadre se desplaza linealmente durante el tramo (sigue al sujeto)
        x = "max(0,min(iw-{cw},({c0}+({c1}-{c0})*t/{d})*iw-{cw}/2))".format(cw=cw, c0=c0, c1=c1, d=dur)
        cadena.append("crop={cw}:{h}:'{x}':0".format(cw=cw, h=h, x=x))
    cadena += ['scale=1080:1920:flags=lanczos', ajuste, 'lut3d=' + LUT]
    ffmpeg(['-ss', str(inicio), '-t', str(dur), '-i', ruta, '-vf', ','.join(cadena), '-q:v', '3',
            os.path.join(dst, '%04d.jpg')])
    print('ok', nombre, len(os.listdir(dst)), 'cuadros')


def fija(nombre, ruta, ajuste, forzar):
    dst = os.path.join(SALIDA, '_fijas', nombre + '.jpg')
    if os.path.exists(dst) and not forzar:
        print('--', nombre, '(ya existe)')
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    # PIL limpia metadatos dañados (algunos PNG exportados traen EXIF inválido que ffmpeg rechaza)
    from PIL import Image
    im = Image.open(PROYECTO + ruta).convert('RGB')
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    tmp = dst + '.tmp.png'
    im.save(tmp)
    ffmpeg(['-i', tmp, '-vf', ajuste + ',lut3d=' + LUT, '-frames:v', '1', '-q:v', '2', dst])
    os.remove(tmp)
    print('ok', nombre)


if __name__ == '__main__':
    forzar = '--forzar' in sys.argv
    for nombre, (archivo, inicio, dur, c0, c1, ajuste) in TRAMOS.items():
        extraer(nombre, archivo, inicio, dur, c0, c1, ajuste, forzar)
    for nombre, (ruta, ajuste) in FIJAS.items():
        fija(nombre, ruta, ajuste, forzar)
