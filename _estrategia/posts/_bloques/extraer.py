"""Extrae bloques vectoriales (artefactos, íconos) de una lámina PDF a bloques.json, sin textos.
Uso: /usr/bin/python3 extraer.py lamina.pdf  → bloques.json (coordenadas en pt relativas al recorte, y hacia abajo)."""
import json, sys, pymupdf as f

RECORTES = {  # nombre: (x0, y0, x1, y1) en pt de la lámina ARQ-01
    'isa_circulo': (1399, 692, 1484, 783),
    'bano_au': (1307, 472, 1445, 580),
    'sillas_espera': (1478, 767, 1641, 798),
    'sillon_dental': (1720, 737, 1798, 829),
    'lavamanos_redondo': (1801, 597, 1825, 623),
    'rampa_franjas': (1419, 790, 1471, 872),
    'inodoro': (1309, 499, 1351, 527),
    'isa': (1426, 708, 1474, 764),
}

def clase(c):
    if not c: return None
    r, g, b = c
    if b > .6 and r < .6: return 'a'      # azul: accesibilidad
    if r > .6 and g < .3: return 'r'      # rojo: notas
    if r > .9 and g > .9 and b > .9: return 'w'
    return 'k'

def pt(p, o): return [round(p.x - o[0], 2), round(p.y - o[1], 2)]

pag = f.open(sys.argv[1])[0]
dibujos = pag.get_drawings()
out = {}
for nom, R in RECORTES.items():
    clip = f.Rect(R); paths = []
    for d in dibujos:
        if not clip.contains(d['rect']): continue
        ops = []
        for it in d['items']:
            t = it[0]
            if t == 'l': ops.append(['l', pt(it[1], R), pt(it[2], R)])
            elif t == 'c': ops.append(['c', pt(it[1], R), pt(it[2], R), pt(it[3], R), pt(it[4], R)])
            elif t == 're': r = it[1]; ops.append(['re', round(r.x0 - R[0], 2), round(r.y0 - R[1], 2), round(r.width, 2), round(r.height, 2)])
            elif t == 'qu': q = it[1]; ops.append(['qu', pt(q.ul, R), pt(q.ur, R), pt(q.lr, R), pt(q.ll, R)])
        if not ops: continue
        paths.append({'s': clase(d.get('color')), 'f': clase(d.get('fill')), 'w': round(d.get('width') or 0, 2),
                      'd': bool(d.get('dashes') and d['dashes'] not in ('[] 0', '')), 'o': ops,
                      'cerrar': bool(d.get('closePath'))})
    out[nom] = {'w': R[2] - R[0], 'h': R[3] - R[1], 'p': paths}
    print(nom, len(paths))
json.dump(out, open('bloques.json', 'w'), separators=(',', ':'))
open('bloques.js', 'w').write('window.BLOQUES = ' + json.dumps(out, separators=(',', ':')) + ';\n')
