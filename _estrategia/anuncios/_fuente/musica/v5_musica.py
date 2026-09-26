# -*- coding: utf-8 -*-
"""
v5_musica.py — pista original para el reel V5 (sintetizada desde cero, sin samples).

120 BPM, La menor (Am – F – C – G), compases de 2 s alineados con los cortes del video:
   0– 8 s  intro contenida (pad, bajo pulsante filtrado, hats); bombo desde los 4 s; barrido al drop
   8–16 s  drop: groove completo, arpegio con delay, crash de entrada
  16–20 s  quiebre: sin bombo, tensión creciente; impacto a los 19,0 s (el dron llega a la mano)
  20–24 s  cierre: groove completo, golpe final a los 23 s y cola de reverberación

Uso:  python3 v5_musica.py      → V5-musica.wav (44,1 kHz, estéreo)
Requiere numpy y scipy.
"""
import os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
BPM = 120
BEAT = 60 / BPM            # 0,5 s
BAR = 4 * BEAT             # 2 s
DUR = 24.0
N = int(SR * (DUR + 0.2))
rng = np.random.default_rng(7)
AQUI = os.path.dirname(os.path.abspath(__file__))


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_(n):
    return np.arange(n) / SR


def lp(x, f, o=2):
    return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)


def bp(x, f1, f2, o=2):
    return sosfilt(butter(o, [f1, f2], 'band', fs=SR, output='sos'), x)


def saw(f, n, fase=0.0):
    return 2 * ((f * t_(n) + fase) % 1.0) - 1


def adsr(n, a, d, s, r):
    e = np.full(n, s, dtype=float)
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n); e[:na] = np.linspace(0, 1, na, endpoint=False)
    nd = min(nd, n - na); e[na:na + nd] = np.linspace(1, s, nd, endpoint=False)
    if nr and n > nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def pon(buf, sig, t, gan=1.0, pan=0.0):
    """suma una señal mono (o estéreo) en el bus en el segundo t, con paneo -1..1"""
    i = int(round(t * SR))
    if i >= len(buf):
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l, sig * r], 1) * np.sqrt(2)
    n = min(len(sig), len(buf) - i)
    buf[i:i + n] += sig[:n] * gan


def bus():
    return np.zeros((N, 2))


# ---------------------------------------------------------------- armonía
ACORDES = [  # (raíz del bajo, notas del pad, notas del arpegio)
    (33, [57, 60, 64, 71], [69, 72, 76, 71, 76, 72]),   # Am(add9)
    (29, [53, 57, 60, 64], [65, 69, 72, 76, 72, 69]),   # Fmaj7
    (36, [55, 60, 64, 71], [67, 72, 76, 79, 76, 72]),   # Cmaj7
    (31, [55, 59, 62, 69], [67, 71, 74, 79, 74, 71]),   # G(add9)
]
N_BARS = 12


def acorde(bar):
    return ACORDES[bar % 4]


# ---------------------------------------------------------------- instrumentos
def bombo():
    n = int(0.45 * SR); t = t_(n)
    f = 45 + 95 * np.exp(-t / 0.035)
    fase = 2 * np.pi * np.cumsum(f) / SR
    cuerpo = np.sin(fase) * np.exp(-t / 0.16)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.6 * (cuerpo + click))


def clap():
    n = int(0.35 * SR); t = t_(n)
    ruido = bp(rng.standard_normal(n), 900, 5000)
    env = np.zeros(n)
    for k, d in enumerate((0.0, 0.011, 0.022)):
        i = int(d * SR)
        env[i:] += np.exp(-(t[:n - i]) / (0.008 if k < 2 else 0.09))
    return ruido * env * 0.5


def hat(abierto=False):
    n = int((0.28 if abierto else 0.05) * SR); t = t_(n)
    return hp(rng.standard_normal(n), 7000, 4) * np.exp(-t / (0.09 if abierto else 0.012))


def crash(dur=1.8):
    n = int(dur * SR); t = t_(n)
    x = hp(rng.standard_normal(n), 3500, 2) * np.exp(-t / (dur / 3.5))
    return x * 0.5


def bajo(m, dur, corte):
    n = int(dur * SR); f = hz(m)
    x = 0.6 * saw(f, n) + 0.4 * saw(f * 1.005, n, 0.3) + 0.35 * np.sin(2 * np.pi * f * t_(n))
    x = lp(x, corte, 2)
    return x * adsr(n, 0.004, 0.12, 0.55, 0.03)


def pad(notas, dur, corte):
    n = int(dur * SR)
    L = np.zeros(n); R = np.zeros(n)
    for m in notas:
        f = hz(m)
        for det, lado in ((-0.07, 'L'), (0.0, 'C'), (0.07, 'R')):
            v = saw(f * 2 ** (det / 12), n, rng.random())
            if lado in 'LC': L += v
            if lado in 'RC': R += v
    env = adsr(n, 0.35, 0.3, 0.8, 0.35)
    return np.stack([lp(L, corte, 2) * env, lp(R, corte, 2) * env], 1) / (len(notas) * 2)


def pluck(m, corte=3200):
    n = int(0.3 * SR); t = t_(n); f = hz(m)
    x = 0.5 * saw(f, n) + 0.5 * np.sign(np.sin(2 * np.pi * f * 1.002 * t))
    return lp(x, corte, 2) * np.exp(-t / 0.07)


def barrido(dur, f0=400, f1=9000):
    n = int(dur * SR); t = t_(n)
    ruido = rng.standard_normal(n)
    out = np.zeros(n); paso = 1024
    for i in range(0, n, paso):
        k = i / n
        fc = f0 * (f1 / f0) ** k
        seg = bp(ruido[max(0, i - 2048):i + paso], fc * 0.8, min(fc * 1.25, SR / 2 - 100))
        out[i:i + paso] = seg[-len(out[i:i + paso]):]
    tono = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * t / dur)) / SR) * 0.15
    return (out * 0.6 + tono) * (t / dur) ** 2


def impacto():
    n = int(2.6 * SR); t = t_(n)
    f = 32 + 50 * np.exp(-t / 0.12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
    ruido = lp(rng.standard_normal(n), 1800) * np.exp(-t / 0.35) * 0.4
    return np.tanh(1.3 * (boom + ruido))


def redoble(t0, t1, buf):
    t = t0
    while t < t1:
        k = (t - t0) / (t1 - t0)
        paso = BEAT / 2 if k < 0.5 else (BEAT / 4 if k < 0.8 else BEAT / 8)
        pon(buf, clap() * (0.25 + 0.6 * k), t, 1.0, rng.uniform(-0.2, 0.2))
        t += paso


# ---------------------------------------------------------------- arreglo
bat, bass, pads, arp, fx, verb_send = bus(), bus(), bus(), bus(), bus(), bus()
golpes = []  # tiempos de bombo para el sidechain

for bar in range(N_BARS):
    t0 = bar * BAR
    raiz, notas, arpn = acorde(bar)
    intro, drop, quiebre, cierre = bar < 4, 4 <= bar < 8, 8 <= bar < 10, bar >= 10

    # pad: de cerrado a abierto
    corte = 900 + 1600 * min(1, bar / 4) if intro else (2600 if drop else (3200 if quiebre else 2800))
    pp = pad(notas, BAR + 0.3, corte)
    pon(pads, pp, t0, 0.55 if not quiebre else 0.75)
    pon(verb_send, pp, t0, 0.25)

    for b in range(4):
        tb = t0 + b * BEAT
        # bombo
        if (2 <= bar < 8) or (cierre and tb < 23.0):
            pon(bat, bombo(), tb, 0.95); golpes.append(tb)
        # clap en 2 y 4
        if (drop or cierre) and b in (1, 3) and tb < 23.0:
            c = clap(); pon(bat, c, tb, 0.55); pon(verb_send, c, tb, 0.2)
        # hats
        for s in range(4):
            ts = tb + s * BEAT / 4
            if ts >= 23.0:
                continue
            if intro or drop or cierre:
                vel = (0.10 if s % 2 else 0.16) * (0.6 if intro else 1.0)
                pon(bat, hat(), ts, vel, 0.35 if s % 2 else -0.25)
            if (drop or cierre) and s == 2:
                pon(bat, hat(True), ts, 0.12, 0.2)
        # bajo en corcheas
        for s in range(2):
            ts = tb + s * BEAT / 2
            if ts >= 23.0:
                continue
            if intro:
                cb = 260 + 500 * (bar / 4)
            elif quiebre:
                continue
            else:
                cb = 1100
            pon(bass, bajo(raiz + (12 if s == 1 else 0), BEAT / 2 * 0.95, cb), ts, 0.5 if s == 0 else 0.38)
        # arpegio en semicorcheas
        if drop or quiebre or cierre:
            for s in range(4):
                ts = tb + s * BEAT / 4
                if ts >= 23.0:
                    continue
                m = arpn[(b * 4 + s) % len(arpn)]
                corte_a = 3200 if not quiebre else 900 + 2800 * ((ts - 16) / 4) ** 1.5
                ganancia = 0.16 if not quiebre else 0.08 + 0.12 * ((ts - 16) / 4)
                pl = pluck(m, corte_a)
                pan = -0.3 if s % 2 else 0.3
                pon(arp, pl, ts, ganancia, pan)
                # delay de corchea con puntillo, alternando lados
                for k, (dt, g) in enumerate(((0.375, 0.45), (0.75, 0.22))):
                    pon(arp, pl, ts + dt, ganancia * g, -pan if k == 0 else pan)
                pon(verb_send, pl, ts, ganancia * 0.5)

    # sub sostenido durante el quiebre
    if quiebre:
        n = int((BAR + 0.25) * SR)
        sub = np.sin(2 * np.pi * hz(raiz + 12) * t_(n)) * adsr(n, 0.3, 0.2, 0.9, 0.3)
        pon(bass, lp(sub, 400), t0, 0.14)

# transiciones
pon(fx, barrido(2.0), 6.0, 0.45); redoble(7.0, 8.0, fx)
pon(fx, barrido(3.0, 300, 10000), 16.0, 0.5); redoble(18.0, 19.0, fx)
for tc in (8.0, 20.0):
    c = crash(); pon(fx, c, tc, 0.55); pon(verb_send, c, tc, 0.3)
imp = impacto(); pon(fx, imp, 19.0, 0.9); pon(verb_send, imp, 19.0, 0.35)
pon(fx, crash(1.2), 19.0, 0.35)

# golpe final a los 23 s: bombo + bajo + acorde + crash
pon(bat, bombo(), 23.0, 1.0)
pon(bass, bajo(33, 0.9, 900), 23.0, 0.6)
fin = pad([57, 60, 64, 69], 1.0, 3000); pon(pads, fin, 23.0, 0.9); pon(verb_send, fin, 23.0, 0.6)
c = crash(1.2); pon(fx, c, 23.0, 0.5); pon(verb_send, c, 23.0, 0.4)

# ---------------------------------------------------------------- mezcla
# sidechain: el bajo, el pad y el arpegio respiran con el bombo
tt = t_(N)
duck = np.ones(N)
for tk in golpes:
    i = int(tk * SR); n = min(int(0.3 * SR), N - i)
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.55 * np.exp(-tt[:n] / 0.09))
duck = duck[:, None]

# reverberación: respuesta al impulso sintética de 1,8 s
nir = int(1.8 * SR); tir = t_(nir)
ir = np.stack([lp(rng.standard_normal(nir), 6000) * np.exp(-tir / 0.45) for _ in range(2)], 1) * 0.02
verb = np.stack([fftconvolve(verb_send[:, c], ir[:, c])[:N] for c in range(2)], 1)
verb = np.stack([hp(verb[:, c], 250) for c in range(2)], 1)

mezcla = bat * 0.9 + bass * duck * 0.9 + pads * duck * 0.7 + arp * duck * 0.8 + fx * 0.8 + verb * 0.9
mezcla = np.stack([hp(mezcla[:, c], 28) for c in range(2)], 1)

# fundido final y limitador suave
fin_n = int(0.5 * SR); i_fin = int(DUR * SR) - fin_n
mezcla[i_fin:i_fin + fin_n] *= np.linspace(1, 0, fin_n)[:, None]
mezcla[i_fin + fin_n:] = 0
mezcla /= np.max(np.abs(mezcla)) + 1e-9
mezcla = np.tanh(1.8 * mezcla) / np.tanh(1.8)
mezcla *= 10 ** (-1 / 20)

salida = os.path.join(AQUI, 'V5-musica.wav')
wavfile.write(salida, SR, (mezcla[:int(DUR * SR)] * 32767).astype(np.int16))
print('ok', salida)
