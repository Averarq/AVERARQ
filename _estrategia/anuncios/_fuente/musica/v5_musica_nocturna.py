# -*- coding: utf-8 -*-
"""
v5_musica_nocturna.py — variante musical para V5: deep house / nu-disco nocturno.

Cálida, sensual y bailable, sin voz: bombo suave a cuatro tiempos, hi-hat abierto a contratiempo,
shakers con swing, congas, bajo redondo que ondula en síncopa, piano eléctrico y colchón con
acordes de novena (Fmaj9 → Em9 → Dm9 → Cmaj9), arpegio soñador con eco y una melodía discreta.
Sin quiebres ni silencios: el groove nunca se detiene.

120 BPM, 26 s, compases de 2 s alineados con los cortes del video:
   0– 4 s  colchón, shaker y congas; bajo filtrado
   4– 6 s  entra el bombo, el hi-hat abierto y el piano
   6–18 s  groove completo; arpegio desde los 10 s y melodía desde los 14 s
  18–21 s  el groove se va "bajo el agua" (filtro) y sube un barrido
  21,0 s   se abre de golpe (el dron llega a la mano)
  22–26 s  groove final; acorde de cierre a los 25 s y cola

Uso:  python3 v5_musica_nocturna.py   → V5-musica-nocturna.wav (−14 LUFS)
"""
import json, os, re, subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
BEAT = 0.5
PASO = BEAT / 4
SWING = 0.018            # retraso de las semicorcheas impares (swing)
BAR = 2.0
DUR = 26.0
T_FILTRO, T_ABRE, T_FIN = 18.0, 21.0, 25.0
N = int(SR * (DUR + 0.5))
rng = np.random.default_rng(21)
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
    """tiempo de la semicorchea s dentro del compás, con swing en las impares"""
    return s * PASO + (SWING if s % 2 else 0.0)


# ------------------------------------------------------------------ armonía
# (raíz del bajo, voces del piano/colchón)
FMAJ9 = (41, [57, 60, 64, 67])
EM9 = (40, [55, 59, 62, 66])
DM9 = (38, [53, 57, 60, 64])
CMAJ9 = (36, [52, 55, 59, 62])
COMPASES = [FMAJ9, EM9, DM9, CMAJ9] * 3 + [FMAJ9]           # 13 compases de 2 s


# ------------------------------------------------------------------ instrumentos
def bombo():
    n = int(0.32 * SR); t = t_(n)
    f = 48 + 85 * np.exp(-t / 0.028)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13)
    return lp(np.tanh(1.3 * x), 3000)


def palma(vel=1.0):
    n = int(0.35 * SR); t = t_(n)
    ruido = bp(rng.standard_normal(n), 900, 6000)
    env = sum(np.exp(-np.maximum(0, t - d) / (0.012 if k < 2 else 0.14)) * (t >= d) for k, d in enumerate((0.0, 0.01, 0.02)))
    return ruido * env * 0.45 * vel


def hat_abierto(vel=1.0):
    n = int(0.2 * SR); t = t_(n)
    metal = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (317, 421, 563, 612, 845, 1120))
    x = hp(metal * 0.25 + rng.standard_normal(n), 8000, 4)
    return lp(x, 14000) * np.exp(-t / 0.07) * 0.5 * vel


def shaker(vel=1.0):
    n = int(0.06 * SR); t = t_(n)
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.02)
    return bp(rng.standard_normal(n), 5000, 11000) * env * 0.5 * vel


def conga(m, vel=1.0):
    n = int(0.25 * SR); t = t_(n); f = hz(m)
    fr = f * (1 + 0.25 * np.exp(-t / 0.01))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.09)
    x += bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t / 0.006) * 0.3
    return x * 0.55 * vel


def bajo(m, dur, corte=420, glide_de=None):
    n = int(dur * SR); t = t_(n); f = hz(m)
    fr = np.full(n, f)
    if glide_de is not None:
        g = min(n, int(0.05 * SR)); fr[:g] = np.linspace(hz(glide_de), f, g)
    fase = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(fase) + 0.35 * np.sin(2 * fase) + 0.25 * (2 * ((fase / (2 * np.pi)) % 1) - 1)
    env = np.minimum(1, t / 0.006) * np.exp(-t / 0.35)
    env[-int(0.015 * SR):] *= np.linspace(1, 0, int(0.015 * SR))
    return lp(np.tanh(1.2 * x * env), corte)


def piano(m, dur, vel=1.0, corte=3500):
    n = int(dur * SR); t = t_(n); f = hz(m)
    fase = 2 * np.pi * np.cumsum(f * (1 + 0.002 * np.sin(2 * np.pi * 0.5 * t))) / SR
    ind = 1.4 * np.exp(-t / 0.3) + 0.2
    x = np.sin(fase + ind * np.sin(fase)) + 0.1 * np.sin(2 * fase)
    env = np.minimum(1, t / 0.004) * np.exp(-t / 1.3)
    env[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
    return lp(x * env * vel, corte)


def acorde_piano(notas, dur, vel=1.0, corte=3500):
    n = int((dur + 0.1) * SR)
    L, R = np.zeros(n), np.zeros(n)
    for k, m in enumerate(notas):
        v = piano(m, dur, vel, corte)
        i = int(k * 0.01 * SR)
        trem = 0.18 * np.sin(2 * np.pi * 3.5 * t_(len(v)) + k)
        L[i:i + len(v)] += v * (1 + trem); R[i:i + len(v)] += v * (1 - trem)
    return np.stack([L, R], 1) / len(notas)


def colchon(notas, dur, corte=1800):
    n = int(dur * SR); t = t_(n)
    L, R = np.zeros(n), np.zeros(n)
    for m in notas + [notas[-1] + 12]:
        f = hz(m)
        for det, lado in ((-0.09, 'L'), (0.0, 'C'), (0.09, 'R')):
            v = 2 * ((f * 2 ** (det / 12) * t + rng.random()) % 1) - 1
            if lado in 'LC': L += v
            if lado in 'RC': R += v
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.5)
    return np.stack([lp(L, corte) * env, lp(R, corte) * env], 1) / 12


def campanita(m):
    n = int(0.6 * SR); t = t_(n); f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t / 0.05)
    return x * np.minimum(1, t / 0.003) * np.exp(-t / 0.22) * 0.4


def melodia(m, dur):
    """voz sintética suave (sin palabras): triángulo con vibrato que entra tarde"""
    n = int(dur * SR); t = t_(n); f = hz(m)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.3)
    fase = np.cumsum(f * vib) / SR
    x = 2 * np.abs(2 * (fase % 1) - 1) - 1
    env = np.minimum(1, t / 0.08) * np.minimum(1, (dur - t) / 0.12)
    return lp(x * env, 2600) * 0.35


def barrido(dur):
    n = int(dur * SR); t = t_(n)
    x = hp(rng.standard_normal(n), 2500) * (t / dur) ** 2.5
    return x * 0.3


def platillo(dur=1.6):
    n = int(dur * SR); t = t_(n)
    return hp(rng.standard_normal(n), 4000) * np.exp(-t / (dur / 4)) * 0.35


# ------------------------------------------------------------------ arreglo
ritmo, bajos, armonia, adorno, envio = bus(), bus(), bus(), bus(), bus()
golpes = []
BAJO = [(2, 0, 1), (3, 0, 1), (6, 12, 1), (7, 0, 1), (10, 0, 1), (11, 7, 1), (13, 0, 1), (14, 12, 2)]   # (semicorchea, intervalo, duración)
PIANO = [(0, 1.0, 3), (3, 0.6, 2), (6, 0.75, 3), (10, 0.6, 2), (14, 0.5, 2)]
CONGAS = [(3, 62, 0.7, -0.4), (6, 57, 0.9, 0.4), (7, 57, 0.5, 0.4), (11, 62, 0.8, -0.4), (14, 57, 0.7, 0.4)]
ARPEGIO = [0, 2, 1, 3, 2, 1, 3, 0]
MELODIA = [(0, 76, 0.75), (1.0, 74, 0.25), (1.25, 72, 0.75)]   # (segundo del compás, nota, duración) en compases impares

for bar, (raiz, voces) in enumerate(COMPASES):
    t0 = bar * BAR
    intro, entra, final = bar < 2, bar == 2, bar >= 11

    # colchón continuo
    c = colchon(voces, BAR + 0.4, 900 + 300 * bar if intro else 2200)
    pon(armonia, c, t0, 0.55); pon(envio, c, t0, 0.3)

    for s in range(16):
        ts = t0 + paso(s)
        if ts >= T_FIN + 0.01 and ts < T_FIN + BAR:
            continue
        # shaker en todas las semicorcheas (acento en contratiempos)
        pon(ritmo, shaker(1.0 if s % 4 == 2 else 0.55), ts, 1.2, 0.35 if s % 2 else -0.2)
        # congas
        for (sc, m, v, pan) in CONGAS:
            if s == sc and (bar % 2 or not intro):
                pon(ritmo, conga(m, v), ts, 1.0, pan)
        if intro:
            continue
        # bombo a cuatro tiempos, palma en 2 y 4, hi-hat abierto a contratiempo
        if s % 4 == 0:
            pon(ritmo, bombo(), ts, 0.8); golpes.append(ts)
        if s in (4, 12):
            p = palma(); pon(ritmo, p, ts, 0.5); pon(envio, p, ts, 0.25)
        if s % 4 == 2:
            pon(ritmo, hat_abierto(), ts, 1.05, 0.15)

    # bajo que ondula (filtrado en la intro)
    for (s, iv, d) in BAJO:
        ts = t0 + paso(s)
        corte = 250 + 120 * bar if intro else 520
        glide = raiz + iv - 12 if iv == 12 else None
        pon(bajos, bajo(raiz + iv, d * PASO * 0.95, corte, glide), ts, 0.75)

    # piano eléctrico en síncopa
    if not intro:
        for (s, v, d) in PIANO:
            a = acorde_piano(voces, d * PASO * 1.6, v, 3800)
            pon(armonia, a, t0 + paso(s), 0.55); pon(envio, a, t0 + paso(s), 0.3)

    # arpegio soñador con eco (desde los 10 s)
    if t0 >= 10:
        for s in range(0, 16, 2):
            m = voces[ARPEGIO[(s // 2) % len(ARPEGIO)]] + 12
            ts = t0 + paso(s)
            b = campanita(m); pan = -0.45 if (s // 2) % 2 else 0.45
            pon(adorno, b, ts, 0.16, pan)
            pon(adorno, b, ts + 0.375, 0.08, -pan); pon(adorno, b, ts + 0.75, 0.04, pan)
            pon(envio, b, ts, 0.2)

    # melodía discreta (desde los 14 s, compases impares)
    if t0 >= 14 and bar % 2 == 1 and t0 < T_FIN:
        for (dt, m, d) in MELODIA:
            v = melodia(m, d)
            pon(adorno, v, t0 + dt, 0.5, 0.1); pon(envio, v, t0 + dt, 0.5)

# transiciones suaves
pon(adorno, barrido(2.0), 2.0, 0.8)
pon(adorno, barrido(2.8), T_ABRE - 2.8, 1.0)
for tc in (4.0, 6.0, T_ABRE):
    pc = platillo(); pon(adorno, pc, tc, 0.6 if tc == T_ABRE else 0.35); pon(envio, pc, tc, 0.3)
# acorde de cierre
raiz, voces = FMAJ9
fin = acorde_piano(voces, 1.6, 1.0, 3500); pon(armonia, fin, T_FIN, 0.7); pon(envio, fin, T_FIN, 0.7)
pon(bajos, bajo(raiz, 1.2, 500), T_FIN, 0.8)
pon(ritmo, bombo(), T_FIN, 1.0); golpes.append(T_FIN)
pc = platillo(2.0); pon(adorno, pc, T_FIN, 0.4); pon(envio, pc, T_FIN, 0.4)

# ------------------------------------------------------------------ mezcla
tt = t_(N)
duck = np.ones(N)
for tk in golpes:
    i = int(tk * SR); n = min(int(0.22 * SR), N - i)
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.45 * np.exp(-tt[:n] / 0.1))
duck = duck[:, None]

nir = int(2.2 * SR); tir = t_(nir)
ir = np.stack([lp(rng.standard_normal(nir), 5000) * np.exp(-tir / 0.6) for _ in range(2)], 1) * 0.02
verb = np.stack([hp(fftconvolve(envio[:, c], ir[:, c])[:N], 250) for c in range(2)], 1)

groove = ritmo * 1.05 + bajos * duck * 0.62
# "bajo el agua": el groove se filtra de 18 a 21 s y se abre de golpe en 21,0
m = np.zeros(N)
a, b = int(T_FILTRO * SR), int((T_ABRE - 0.05) * SR)
m[a:b] = np.linspace(0, 1, b - a) ** 0.7
m[b:int(T_ABRE * SR)] = 1.0
m = m[:, None]
groove = groove * (1 - m) + lp(groove, 650, 4) * m * 0.95
mezcla = groove + armonia * duck * 1.15 + adorno * 1.1 + verb * 1.1
mezcla = hp(mezcla, 28)
fin_n = int(0.7 * SR); i_fin = int(DUR * SR) - fin_n
mezcla[i_fin:i_fin + fin_n] *= np.linspace(1, 0, fin_n)[:, None]
mezcla[i_fin + fin_n:] = 0
mezcla /= np.max(np.abs(mezcla)) + 1e-9
mezcla = np.tanh(1.4 * mezcla) / np.tanh(1.4)

tmp = os.path.join(AQUI, '_tmp.wav')
wavfile.write(tmp, SR, (mezcla[:int(DUR * SR)] * 0.89 * 32767).astype(np.int16))
salida = os.path.join(AQUI, 'V5-musica-nocturna.wav')
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
                      '-f', 'null', '-'], capture_output=True, text=True).stderr
d = json.loads(re.search(r'\{[^{}]*\}', med[med.rfind('{') - 1:], re.S).group(0))
af = ('loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:'
      'measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}').format(**d)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', str(SR), salida], check=True)
os.remove(tmp)
print('ok', salida)
