# -*- coding: utf-8 -*-
"""
crear_lut.py — genera la LUT de color AVERARQ (averarq.cube, 33³, Rec.709 SDR).

Una sola línea visual para renders, fotos y video de dron, celular y recorridos:
  · verdes hacia oliva cálido, vivos pero sin flúor
  · cielos hacia turquesa limpio
  · naranjos y terracotas intactos: tejas, ladrillo y el naranjo de marca son el acento
  · vibración: realza los colores apagados más que los ya saturados
  · curva con contraste en medios, negros apenas levantados y altas suaves
  · sombras levemente frías y luces cálidas

Sirve también en CapCut, Premiere, DaVinci o Photoshop (Ajuste > Consulta de colores).
Uso:  python3 crear_lut.py
"""
import os
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
N = 33


def rgb_a_hsv(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    mx, mn = c.max(-1), c.min(-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 1e-9, (mx - mn) / (mx + 1e-9), 0)
    return h, s, mx


def hsv_a_rgb(h, s, v):
    h = (h % 360) / 60
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    sel = [np.stack(x, -1) for x in ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))]
    out = np.zeros(h.shape + (3,))
    for k in range(6):
        out[i == k] = sel[k][i == k]
    return out


def banda(h, centro, ancho):
    d = np.abs((h - centro + 180) % 360 - 180)
    return np.clip(1 - d / ancho, 0, 1) ** 1.5


def graduar(c):
    h, s, v = rgb_a_hsv(c)
    verde = banda(h, 95, 60)
    azul = banda(h, 212, 45)
    naranjo = banda(h, 22, 22)
    h = h - 18 * verde - 12 * azul                     # verde→oliva cálido, azul→turquesa
    s = s * (1 - 0.30 * verde) * (1 - 0.22 * azul) * (1 + 0.15 * naranjo) * 0.98
    s = np.clip(s + 0.45 * s * (1 - s), 0, 1)            # vibración
    c = hsv_a_rgb(h, s, v)

    # curva de película por canal: contraste suave en medios, negros apenas levantados, altas suaves
    c = c + 0.26 * (c - 0.5) * (1 - np.abs(2 * c - 1))
    c = 0.025 + (0.965 - 0.025) * np.clip(c, 0, 1)
    # virado: sombras frías, luces cálidas
    y = (c * [0.2126, 0.7152, 0.0722]).sum(-1, keepdims=True)
    c = c + (1 - y) ** 2 * np.array([-0.018, 0.005, 0.026]) + y ** 2 * np.array([0.028, 0.012, -0.022])
    return np.clip(c, 0, 1)


if __name__ == '__main__':
    g = np.linspace(0, 1, N)
    # orden .cube: R varía más rápido
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')
    grilla = np.stack([r, gg, b], -1).reshape(-1, 3)
    out = graduar(grilla)
    ruta = os.path.join(AQUI, 'averarq.cube')
    with open(ruta, 'w', newline='\n') as f:
        f.write('TITLE "AVERARQ"\n# Linea visual AVERARQ - generada por crear_lut.py\nLUT_3D_SIZE %d\n' % N)
        for px in out:
            f.write('%.6f %.6f %.6f\n' % tuple(px))
    negro = graduar(np.zeros((1, 3)))[0]
    print('ok', ruta, '- negro graduado = #%02x%02x%02x' % tuple((negro * 255).round().astype(int)))
