# -*- coding: utf-8 -*-
"""
extraer_secuencias.py — prepara los tramos de video que usan los reels.

Corta cada tramo de los videos originales (dron 4K y recorrido de obra),
lo encuadra en vertical 1080×1920 a 30 fps y lo guarda como JPG numerados en
_fuente/secuencias/<nombre>/0001.jpg … (carpeta ignorada por git: se regenera).

Uso:
    python3 extraer_secuencias.py          # todos los tramos que falten
    python3 extraer_secuencias.py --forzar # rehace todo

Requiere ffmpeg. Las rutas apuntan a las carpetas de proyecto en el PC de
Alejandro; si cambian, edita ORIGEN.
"""
import os, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, 'secuencias')
ORIGEN = r'C:/Users/Alejandro Vera/Documents/0.AVERARQ/2025/2025_Andrés Martinez/audiovisual'
FPS = 30

# nombre: (archivo, inicio s, duración s, centro horizontal del encuadre al inicio y al final [0-1])
# Para videos ya verticales (1080×1920) el centro se ignora.
TRAMOS = {
    'sc-orbita':    ('DJI_20260818111851_0106_D.MP4', 3.0, 4.2, 0.52, 0.52),
    'sc-piloto-1':  ('DJI_20260818110042_0083_D.MP4', 0.3, 1.3, 0.40, 0.46),
    'sc-piloto-2':  ('DJI_20260818110042_0083_D.MP4', 5.0, 2.4, 0.55, 0.49),
    'sc-alero':     ('compose_video_1787102807464.mp4', 81.4, 1.4, None, None),
    'sc-techumbre': ('compose_video_1787102807464.mp4', 85.4, 1.4, None, None),
    'sc-estar':     ('compose_video_1787102807464.mp4', 65.4, 1.4, None, None),
}


def dimensiones(ruta):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                   '-show_entries', 'stream=width,height', '-of', 'csv=p=0', ruta]).decode()
    w, h = out.strip().split(',')[:2]
    return int(w), int(h)


def extraer(nombre, archivo, inicio, dur, c0, c1, forzar):
    dst = os.path.join(SALIDA, nombre)
    if os.path.isdir(dst) and os.listdir(dst) and not forzar:
        print('--', nombre, '(ya existe)')
        return
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    ruta = os.path.join(ORIGEN, archivo)
    w, h = dimensiones(ruta)
    if w > h:
        cw = round(h * 9 / 16)
        # el centro del encuadre se desplaza linealmente durante el tramo (sigue al sujeto)
        x = "max(0,min(iw-{cw},({c0}+({c1}-{c0})*t/{d})*iw-{cw}/2))".format(cw=cw, c0=c0, c1=c1, d=dur)
        vf = "fps={fps},crop={cw}:{h}:'{x}':0,scale=1080:1920:flags=lanczos".format(fps=FPS, cw=cw, h=h, x=x)
    else:
        vf = 'fps={},scale=1080:1920:flags=lanczos'.format(FPS)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(inicio), '-t', str(dur), '-i', ruta,
                    '-vf', vf, '-q:v', '3', os.path.join(dst, '%04d.jpg')], check=True)
    print('ok', nombre, len(os.listdir(dst)), 'cuadros')


if __name__ == '__main__':
    forzar = '--forzar' in sys.argv
    for nombre, (archivo, inicio, dur, c0, c1) in TRAMOS.items():
        extraer(nombre, archivo, inicio, dur, c0, c1, forzar)
