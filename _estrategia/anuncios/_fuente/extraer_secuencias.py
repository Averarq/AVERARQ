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
SEP = 'Septiembre 2026/'
TRAMOS = {
    # cenital del 16-sep que asciende; el cuadro inicial (36,0 s) calza con la planta rotada (ver V5, escena 1)
    'sc-cenital':   (SEP + 'DJI_20260916111716_0203_D.MP4', 36.0, 3.0, 0.50, 0.50, 'eq=brightness=0.0'),
    'sc-orbita':    (SEP + 'DJI_20260916112103_0209_D.MP4', 3.0, 2.1, 0.50, 0.50, 'eq=brightness=0.0'),
    'sc-fachada':   (SEP + 'DJI_20260916113524_0216_D.MP4', 6.0, 2.1, 0.50, 0.50, 'eq=brightness=0.0'),
    # Alejandro recibe el dron en la mano; corta a los 24,4 s, antes de que sonría
    'sc-dron-mano': ('IMG_5241.MOV', 20.4, 4.0, None, None, 'eq=brightness=0.03:contrast=0.97'),
}

# imágenes fijas: nombre de salida → (ruta dentro de PROYECTO o patrón glob, ajuste previo o None = gráfica sin LUT)
FIJAS = {
    'render-aereo': ('/RENDERS/Escena 4.png', 'eq=saturation=0.92:contrast=1.03'),
    'dron-oblicua': ('/audiovisual/' + SEP + 'DJI_20260916111954_0208_D.JPG', 'eq=brightness=0.0'),
    'int-cielo':    ('/audiovisual/' + SEP + '1790392291243.jpg', 'eq=brightness=0.01'),
    'int-ventanal': ('/audiovisual/' + SEP + '1790392290144.jpg', 'eq=brightness=0.0'),
    'int-puerta':   ('/audiovisual/' + SEP + '1790392290481.jpg', 'eq=brightness=0.0'),
}

# gráficas de marca (sin LUT). Las plantas se recortan al dibujo y se rotan 90° para calzar con el cenital.
GRAFICAS = {
    'planta-naranjo': ('/audiovisual/Patr*-08.png', True),
    'planta-blanca':  ('/audiovisual/Patr*-09.png', True),
    'patron':         ('/audiovisual/Patr*-10.png', False),
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
    import glob as _g
    im = Image.open(_g.glob(PROYECTO + ruta)[0]).convert('RGB')
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    tmp = dst + '.tmp.png'
    im.save(tmp)
    ffmpeg(['-i', tmp, '-vf', ajuste + ',lut3d=' + LUT, '-frames:v', '1', '-q:v', '2', dst])
    os.remove(tmp)
    print('ok', nombre)


def graficas(forzar):
    import glob
    from PIL import Image
    ref = glob.glob(PROYECTO + GRAFICAS['planta-naranjo'][0])[0]
    import numpy as np
    al = np.asarray(Image.open(ref))[..., 3]
    yy, xx = np.where(al > 20)
    caja = (xx.min(), yy.min(), xx.max() + 1, yy.max() + 1)     # misma caja para ambas plantas
    for nombre, (patron, es_planta) in GRAFICAS.items():
        dst = os.path.join(SALIDA, '_fijas', nombre + ('.png' if es_planta else '.jpg'))
        if os.path.exists(dst) and not forzar:
            print('--', nombre, '(ya existe)')
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im = Image.open(glob.glob(PROYECTO + patron)[0])
        if es_planta:
            im = im.crop(caja).rotate(90, expand=True)
            im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
            im.save(dst, optimize=True)
        else:
            im = im.convert('RGB'); im.thumbnail((1400, 2240), Image.LANCZOS); im.save(dst, quality=90)
        print('ok', nombre, im.size)


if __name__ == '__main__':
    forzar = '--forzar' in sys.argv
    for nombre, (archivo, inicio, dur, c0, c1, ajuste) in TRAMOS.items():
        extraer(nombre, archivo, inicio, dur, c0, c1, ajuste, forzar)
    for nombre, (ruta, ajuste) in FIJAS.items():
        fija(nombre, ruta, ajuste, forzar)
    graficas(forzar)
