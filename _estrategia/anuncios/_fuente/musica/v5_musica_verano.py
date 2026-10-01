# -*- coding: utf-8 -*-
"""
v5_musica_verano.py — variante musical para V5: instrumental cálido, relajado y levemente psicodélico.

Soul / surf psicodélico de tarde de verano: guitarra limpia de cuerda pulsada (Karplus-Strong) con
coro, eco de cinta y reverb; bajo redondo con notas de paso; baquetazo en el aro, hats con swing
perezoso y pandero suave; órgano con vibrato tipo Leslie en segundo plano; vaivén de cinta (wow y
flutter) sobre toda la mezcla. Acordes Dmaj9 → F#m7 → Gmaj7 → Gm6 (el iv menor da la nostalgia).
Sin explosiones: pequeñas variaciones mantienen el interés.

120 BPM, 26 s, compases de 2 s alineados con los cortes del video:
   0– 4 s  guitarra sola con órgano lejano
   4– 6 s  entran bajo y percusión suave
   6–18 s  groove relajado; la guitarra varía sus frases; desde 14 s un "slide" melódico
  18–21 s  queda la percusión liviana y un crescendo invertido de guitarra
  21,0 s   vuelve la batería con naturalidad (el dron llega a la mano)
  22–26 s  final; acorde que queda sonando desde los 25 s

Uso:  python3 v5_musica_verano.py   → V5-musica-verano.wav (−14 LUFS)
"""
import json, os, re, subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, lfilter
from scipy.io import wavfile

SR = 44100
BEAT = 0.5
PASO = BEAT / 4
SWING = 0.032
BAR = 2.0
DUR = 26.0
T_PAUSA, T_VUELVE, T_FIN = 18.0, 21.0, 25.0
N = int(SR * (DUR + 1.0))
rng = np.random.default_rng(5)
AQUI = os.path.dirname(os.path.abspath(__file__))


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def bus(): return np.zeros((N, 2))


def pon(buf, sig, t, gan=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= len(buf) or i < 0:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l, sig * r], 1) * np.sqrt(2)
    n = min(len(sig), len(buf) - i)
    buf[i:i + n] += sig[:n] * gan


def paso(s):
    return s * PASO + (SWING if s % 2 else 0.0)


# ------------------------------------------------------------------ armonía
DMAJ9 = (38, [54, 57, 61, 64])
FSM7 = (42, [57, 61, 64, 66])
GMAJ7 = (43, [54, 59, 62, 67])
GM6 = (43, [55, 58, 62, 64])
COMPASES = [DMAJ9, FSM7, GMAJ7, GM6] * 3 + [DMAJ9]
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81]          # Re mayor pentatónica


# ------------------------------------------------------------------ instrumentos
def guitarra(m, dur, vel=1.0, brillo=0.5):
    """cuerda pulsada (Karplus-Strong) con cuerpo"""
    f = hz(m); n = int(dur * SR)
    L = int(round(SR / f))
    exc = np.zeros(n)
    ruido = rng.standard_normal(L)
    exc[:L] = lp(ruido, 1500 + 5000 * brillo) * vel
    d = 0.4985 - 0.0005 * (1 - brillo)
    a = np.zeros(L + 2); a[0] = 1; a[L] = -d; a[L + 1] = -d
    y = lfilter([1.0], a, exc)
    y = bp(y, 90, 6000)
    env = np.ones(n); env[-int(0.03 * SR):] = np.linspace(1, 0, int(0.03 * SR))
    return y * env * 0.6


def coro(x, prof=0.0025, vel=0.7, base=0.014):
    """coro/vibrato por retardo modulado (estéreo)"""
    n = len(x); t = t_(n); idx = np.arange(n)
    out = []
    for fase in (0.0, np.pi / 2):
        dl = (base + prof * np.sin(2 * np.pi * vel * t + fase)) * SR
        out.append(0.6 * x + 0.5 * np.interp(idx - dl, idx, x, left=0))
    return np.stack(out, 1)


def organo(notas, dur):
    n = int(dur * SR); t = t_(n)
    x = np.zeros(n)
    for m in notas:
        f = hz(m) * (1 + 0.003 * np.sin(2 * np.pi * 6.1 * t))          # Leslie lento
        for k, g in ((1, 1.0), (2, 0.5), (3, 0.25), (4, 0.12)):
            x += g * np.sin(2 * np.pi * f * k * t + rng.random() * 6)
    env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    am = 1 + 0.25 * np.sin(2 * np.pi * 6.1 * t)
    return np.stack([lp(x * env * am, 2500), lp(x * env * (2 - am), 2500)], 1) / (len(notas) * 5)


def bajo(m, dur, vel=1.0, glide_de=None):
    n = int(dur * SR); t = t_(n); f = hz(m)
    fr = np.full(n, f)
    if glide_de is not None:
        g = min(n, int(0.06 * SR)); fr[:g] = np.linspace(hz(glide_de), f, g)
    fase = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(fase) + 0.3 * np.sin(2 * fase) + 0.1 * np.sin(3 * fase)
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.6)
    env[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return lp(np.tanh(1.3 * x * env), 800) * vel


def bombo():
    n = int(0.3 * SR); t = t_(n)
    f = 55 + 60 * np.exp(-t / 0.03)
    return lp(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14), 1500)


def aro(vel=1.0):
    """baquetazo en el aro (cross-stick)"""
    n = int(0.12 * SR); t = t_(n)
    tono = np.sin(2 * np.pi * 480 * t) * np.exp(-t / 0.018) + 0.6 * np.sin(2 * np.pi * 1650 * t) * np.exp(-t / 0.01)
    click = bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t / 0.006)
    return (tono * 0.6 + click * 0.5) * 0.5 * vel


def hat(vel=1.0):
    n = int(0.05 * SR); t = t_(n)
    return lp(hp(rng.standard_normal(n), 7000, 4), 12000) * np.exp(-t / 0.012) * 0.3 * vel


def pandero(vel=1.0):
    n = int(0.18 * SR); t = t_(n)
    jingle = sum(np.sin(2 * np.pi * f * t) for f in (5200, 6700, 7900, 9300)) * 0.2
    x = (hp(rng.standard_normal(n), 6000) * 0.8 + jingle) * np.exp(-t / 0.05)
    return x * 0.3 * vel


def slide(notas, dur):
    """melodía con glissando tipo slide (seno + armónicos suaves, vibrato tardío)"""
    n = int(dur * SR); t = t_(n)
    tramo = n // len(notas)
    fr = np.concatenate([np.full(tramo, hz(m)) for m in notas] + [np.full(n - tramo * len(notas), hz(notas[-1]))])
    fr = np.convolve(fr, np.ones(2400) / 2400, mode='same')          # glissando entre notas
    fr *= 1 + 0.008 * np.sin(2 * np.pi * 5 * t) * np.minimum(1, t / 0.5)
    fase = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(fase) + 0.3 * np.sin(2 * fase) + 0.12 * np.sin(3 * fase)
    env = np.minimum(1, t / 0.1) * np.minimum(1, (dur - t) / 0.3)
    return lp(x * env, 3000) * 0.22


# ------------------------------------------------------------------ arreglo
guit, bat, bajos, orgs, envio, eco = bus(), bus(), bus(), bus(), bus(), bus()
# frases de guitarra: (semicorchea, grado de la pentatónica o 'a#' = nota del acorde, duración en pasos)
FRASES = [
    [(0, 'a0', 6), (6, 'a2', 4), (10, 'a1', 6)],
    [(0, 'a1', 3), (3, 'a3', 3), (6, 'a2', 10)],
    [(2, 4, 2), (4, 3, 2), (6, 2, 4), (10, 'a0', 6)],
    [(0, 'a3', 4), (4, 'a2', 4), (8, 'a1', 8)],
    [(0, 5, 2), (2, 4, 2), (4, 2, 4), (8, 1, 2), (10, 'a0', 6)],
    [(0, 'a0', 2), (2, 'a1', 2), (4, 'a2', 2), (6, 'a3', 10)],
]
BAJO = [(0, 0, 5), (6, 7, 2), (8, 12, 3), (11, 7, 2), (14, 'paso', 2)]

for bar, (raiz, voces) in enumerate(COMPASES):
    t0 = bar * BAR
    intro = bar < 2
    pausa = T_PAUSA <= t0 < T_VUELVE - 1
    siguiente = COMPASES[min(bar + 1, len(COMPASES) - 1)][0]

    # órgano lejano todo el tiempo
    o = organo(voces, BAR + 0.3); pon(orgs, o, t0, 0.5); pon(envio, o, t0, 0.25)

    # guitarra: frase distinta cada compás
    if t0 < T_FIN:
        frase = FRASES[bar % len(FRASES)] if not intro else FRASES[bar]
        for (s, g, d) in frase:
            m = voces[int(g[1])] + 12 if isinstance(g, str) else PENTA[g]
            v = guitarra(m, d * PASO + 0.9, 0.9, 0.35 + 0.1 * (bar % 3))
            pon(guit, coro(v), t0 + paso(s), 0.55)
            pon(eco, v, t0 + paso(s), 0.5); pon(envio, v, t0 + paso(s), 0.35)
        # rasgueo suave del acorde en el tiempo 3 (a partir del groove)
        if not intro and not pausa:
            for k, m in enumerate(voces):
                v = guitarra(m, 0.9, 0.35, 0.2)
                pon(guit, coro(v), t0 + 1.0 + k * 0.012, 0.35)

    if intro:
        continue

    # bajo con nota de paso cromática hacia el acorde siguiente
    if t0 < T_FIN and not pausa:
        for (s, iv, d) in BAJO:
            if iv == 'paso':
                m = siguiente + (1 if siguiente < raiz else -1) if siguiente != raiz else raiz + 7
            else:
                m = raiz + iv
            pon(bajos, bajo(m, d * PASO * 0.95, 0.9 if s == 0 else 0.7), t0 + paso(s), 0.8)
    elif pausa:
        pon(bajos, bajo(raiz, BAR * 0.95, 0.35), t0, 0.8)

    # batería relajada
    for s in range(16):
        ts = t0 + paso(s)
        if ts >= T_FIN:
            break
        if not pausa:
            if s in (0, 10) or (s == 7 and bar % 2):
                pon(bat, bombo(), ts, 0.65)
            if s in (4, 12):
                pon(bat, aro(), ts, 0.8, -0.1); pon(envio, aro(), ts, 0.15)
            if s % 2 == 0:
                pon(bat, hat(1.0 if s % 4 == 2 else 0.65), ts, 1.4, 0.3)
        if s in (4, 12) and (pausa or t0 >= 6):
            pon(bat, pandero(0.7), ts, 1.0, 0.4)
        if pausa and s % 2 == 1:
            pon(bat, hat(0.35), ts, 1.0, 0.3)

# slide melódico discreto desde los 14 s
for t0, notas in ((14.0, [74, 76, 78]), (16.0, [81, 78, 76]), (22.0, [78, 76, 74])):
    v = slide(notas, 1.8); pon(eco, v, t0 + 0.25, 0.9); pon(envio, v, t0 + 0.25, 0.4); pon(guit, coro(v), t0 + 0.25, 0.6)

# crescendo invertido de guitarra hacia los 21 s (el acorde de vuelta, al revés)
raiz, voces = COMPASES[int(T_VUELVE // BAR)]
rev = sum(guitarra(m + 12, 2.5, 0.8, 0.6) for m in voces)
rev = hp(rev[::-1], 150) * np.linspace(0, 1, len(rev)) ** 1.5
pon(eco, rev, T_VUELVE - 2.5, 0.35); pon(envio, rev, T_VUELVE - 2.5, 0.3)
pon(bat, pandero(1.0), T_VUELVE, 1.0, 0.3)

# acorde final que queda sonando
raiz, voces = DMAJ9
for k, m in enumerate(voces + [voces[0] + 12]):
    v = guitarra(m + 12, 3.5, 0.8, 0.45); pon(guit, coro(v), T_FIN + k * 0.035, 0.5); pon(envio, v, T_FIN + k * 0.035, 0.6)
pon(bajos, bajo(raiz, 1.5, 0.9), T_FIN, 0.8)
pon(bat, bombo(), T_FIN, 0.8)

# ------------------------------------------------------------------ efectos y mezcla
# eco de cinta en corchea con puntillo, oscureciéndose con cada repetición
retardo = np.zeros_like(eco)
for k, (dt, g, f) in enumerate(((0.375, 0.45, 3500), (0.75, 0.28, 2500), (1.125, 0.16, 1800))):
    i = int(dt * SR)
    capa = lp(eco, f)
    if k % 2:
        capa = capa[:, ::-1]
    retardo[i:] += capa[:-i] * g

nir = int(3.0 * SR); tir = t_(nir)
ir = np.stack([lp(rng.standard_normal(nir), 5500) * np.exp(-tir / 0.8) for _ in range(2)], 1) * 0.02
verb = np.stack([hp(fftconvolve(envio[:, c], ir[:, c])[:N], 200) for c in range(2)], 1)

# la guitarra lleva la canción; en la intro (sin batería) sube para que el arranque no quede débil
g_int = np.ones(N); g_int[:int(4.0 * SR)] = 1.8; g_int[int(4.0 * SR):int(4.5 * SR)] = np.linspace(1.8, 1.0, int(0.5 * SR))
mezcla = (guit * 1.7 + retardo * 1.0) * g_int[:, None] + bat * 1.0 + bajos * 0.5 + orgs * 0.9 + verb * 1.2
mezcla = lp(hp(mezcla, 32), 12500)                   # techo cálido, algo "vintage"

# vaivén de cinta: wow lento + flutter leve
tt = t_(N); idx = np.arange(N)
warp = (0.0016 * np.sin(2 * np.pi * 0.45 * tt) + 0.00025 * np.sin(2 * np.pi * 6.3 * tt)) * SR
mezcla = np.stack([np.interp(idx + warp, idx, mezcla[:, c]) for c in range(2)], 1)

fin_n = int(0.8 * SR); i_fin = int(DUR * SR) - fin_n
mezcla[i_fin:i_fin + fin_n] *= np.linspace(1, 0, fin_n)[:, None] ** 1.5
mezcla[i_fin + fin_n:] = 0
mezcla /= np.max(np.abs(mezcla)) + 1e-9
mezcla = np.tanh(1.3 * mezcla) / np.tanh(1.3)

tmp = os.path.join(AQUI, '_tmp.wav')
wavfile.write(tmp, SR, (mezcla[:int(DUR * SR)] * 0.89 * 32767).astype(np.int16))
salida = os.path.join(AQUI, 'V5-musica-verano.wav')
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
                      '-f', 'null', '-'], capture_output=True, text=True).stderr
d = json.loads(re.search(r'\{[^{}]*\}', med[med.rfind('{') - 1:], re.S).group(0))
af = ('loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:'
      'measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}').format(**d)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', str(SR), salida], check=True)
os.remove(tmp)
print('ok', salida)
