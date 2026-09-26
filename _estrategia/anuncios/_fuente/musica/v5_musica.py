# -*- coding: utf-8 -*-
"""
v5_musica.py — pista original para el reel V5 (sintetizada desde cero, sin samples).

Estilo: hip-hop / trap sobrio, moderno y algo urbano, pensado como fondo (no protagonista).
120 BPM con snare en el tercer tiempo (half-time), 808 con deslizamientos, hi-hats en
semicorcheas con redobles, piano eléctrico oscuro (Am9 – Fmaj7 – Dm9 – Em7) y textura de vinilo.
Compases de 2 s alineados con los cortes del video (26 s):
   0– 4 s  piano filtrado, vinilo y hats suaves (la planta se dibuja)
   4– 6 s  entran 808, bombo y snare (el dron asciende)
   6–18 s  groove completo (render vs dron, órbita, fachada, interiores)
  18–21 s  quiebre: sin batería; a los 20,75 s silencio seco y a los 21,0 s cae el 808
           (el dron llega a la mano)
  22–26 s  groove de cierre; golpe final a los 25 s y cola

Uso:  python3 v5_musica.py      → V5-musica.wav (44,1 kHz, estéreo, normalizada a −14 LUFS)
Requiere numpy, scipy y ffmpeg.
"""
import json, os, re, subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
BEAT = 0.5
PASO = BEAT / 4            # semicorchea = 0,125 s
BAR = 2.0
DUR = 26.0
T_CORTE, T_CAIDA, T_FIN = 20.75, 21.0, 25.0
N = int(SR * (DUR + 0.3))
rng = np.random.default_rng(11)
AQUI = os.path.dirname(os.path.abspath(__file__))


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def t_(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
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


# ------------------------------------------------------------------ armonía
# (raíz del 808 en MIDI, voces del piano sin fundamental)
AM, F, DM, EM = (33, [60, 64, 67, 71]), (29, [57, 60, 64, 67]), (38, [57, 60, 64, 65]), (40, [55, 59, 62, 66])
COMPASES = [AM, F, DM, EM, AM, F, DM, EM, AM, F, EM, F, EM]  # 13 compases de 2 s

# ------------------------------------------------------------------ instrumentos
def piano(m, dur, vel=1.0, corte=3000):
    """piano eléctrico FM con leve vaivén de cinta"""
    n = int(dur * SR); t = t_(n); f = hz(m)
    fase = 2 * np.pi * np.cumsum(f * (1 + 0.0025 * np.sin(2 * np.pi * 0.7 * t))) / SR
    ind = 1.8 * np.exp(-t / 0.22) + 0.25
    x = np.sin(fase + ind * np.sin(fase)) + 0.12 * np.sin(2 * fase)
    env = np.minimum(1, t / 0.004) * np.exp(-t / 1.6)
    env[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))
    return lp(x * env * vel, corte)


def acorde(notas, dur, vel=1.0, corte=3000):
    n = int((dur + 0.1) * SR)
    L, R = np.zeros(n), np.zeros(n)
    for k, m in enumerate(notas):
        v = piano(m, dur, vel, corte)
        i = int(k * 0.012 * SR)                       # rasgueo leve
        trem = 0.12 * np.sin(2 * np.pi * 4.2 * t_(len(v)))
        L[i:i + len(v)] += v * (1 + trem)
        R[i:i + len(v)] += v * (1 - trem)
    return np.stack([L, R], 1) / len(notas)


def ochoocho(m, dur, glide_de=None):
    n = int(dur * SR); t = t_(n); f = hz(m)
    fr = np.full(n, f)
    if glide_de is not None:
        g = min(n, int(0.09 * SR)); fr[:g] = np.linspace(hz(glide_de), f, g)
    fr = fr * (1 + 1.0 * np.exp(-t / 0.012))          # ataque con golpe de tono
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR)
    env = np.minimum(1, t / 0.003) * np.exp(-t / 0.75)
    env[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return np.tanh(2.6 * x * env) * 0.8              # saturación: se oye en parlantes de celular


def bombo():
    n = int(0.2 * SR); t = t_(n)
    f = 52 + 110 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)


def snare(vel=1.0):
    n = int(0.3 * SR); t = t_(n)
    cuerpo = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    ruido = bp(rng.standard_normal(n), 1800, 9000) * np.exp(-t / 0.11)
    clap = bp(rng.standard_normal(n), 1000, 4000)
    env = sum(np.exp(-np.maximum(0, t - d) / 0.01) * (t >= d) for d in (0.0, 0.009, 0.018))
    return np.tanh(1.4 * (0.5 * cuerpo + 0.7 * ruido + 0.35 * clap * env)) * vel * 1.3


def hat(vel=1.0, abierto=False):
    n = int((0.22 if abierto else 0.045) * SR); t = t_(n)
    metal = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0))
    x = hp(metal * 0.3 + rng.standard_normal(n), 7500, 4)
    return lp(x, 13000) * np.exp(-t / (0.07 if abierto else 0.011)) * vel * 0.85


def campana(m):
    n = int(0.9 * SR); t = t_(n); f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.08)
    return x * np.minimum(1, t / 0.002) * np.exp(-t / 0.35) * 0.5


def vinilo(dur):
    n = int(dur * SR)
    x = lp(rng.standard_normal(n), 5000) * 0.012
    for i in rng.integers(0, n - 200, int(dur * 22)):
        x[i:i + 60] += hp(rng.standard_normal(60), 1500) * rng.uniform(0.02, 0.08)
    return hp(x, 300)


def swell(dur):
    """golpe de platillo invertido que crece hacia el corte"""
    n = int(dur * SR); t = t_(n)
    x = hp(rng.standard_normal(n), 3000) * np.exp(-(dur - t) / (dur / 3))
    return x * 0.35


# ------------------------------------------------------------------ arreglo
teclas, bajo, bat, fx, envio = bus(), bus(), bus(), bus(), bus()
golpes = []
KICK = {0: [0, 6, 10], 1: [0, 3, 11, 14]}             # patrones de 808/bombo por compás par/impar
MOTIVO = [(0, 76), (6, 74), (10, 72), (16, 71), (22, 72), (26, 69)]   # campana, cada 2 compases

pon(fx, vinilo(DUR), 0.0, 1.0)

for bar, (raiz, voces) in enumerate(COMPASES):
    t0 = bar * BAR
    intro, entra, groove, quiebre, cierre = bar < 2, bar == 2, 3 <= bar < 9, bar in (9, 10), bar >= 11

    # piano: acorde al inicio y reataque suave en el "y" del 2
    corte = 1200 if intro else (2200 if entra else (1600 if quiebre else 3200))
    for dt, vel, dur in ((0.0, 1.0, 1.25), (1.25, 0.55, 0.75)):
        if quiebre and t0 + dt >= T_CORTE:
            continue
        if cierre and t0 + dt >= T_FIN:
            continue
        a = acorde(voces, dur, vel, corte)
        pon(teclas, a, t0 + dt, 0.5); pon(envio, a, t0 + dt, 0.35)

    if quiebre:
        # hats suaves en corcheas hasta el corte
        for s in range(0, 16, 2):
            ts = t0 + s * PASO
            if ts < T_CORTE:
                pon(bat, hat(0.35), ts, 1.0, 0.3)
        continue

    patron = KICK[bar % 2]
    for s in range(16):
        ts = t0 + s * PASO
        if ts >= T_FIN:
            break
        # 808 + bombo
        if not intro and s in patron:
            sig = patron[patron.index(s) + 1] if patron.index(s) + 1 < len(patron) else 16
            dur = (sig - s) * PASO
            glide = raiz + 12 if (s == 14 and (groove or cierre)) else None
            nota = raiz + 12 if s == 14 else raiz
            pon(bajo, ochoocho(nota, dur, raiz if glide else None), ts, 0.75)
            pon(bat, bombo(), ts, 0.8); golpes.append(ts)
        # snare en el tercer tiempo + fantasma
        if not intro and s == 8:
            sn = snare(); pon(bat, sn, ts, 0.62); pon(envio, sn, ts, 0.25)
        if (groove or cierre) and s == 15 and bar % 2:
            pon(bat, snare(0.22), ts, 0.62)
        # hi-hats
        if intro:
            if s % 2 == 0:
                pon(bat, hat(0.35), ts, 1.0, 0.3)
        else:
            vel = 0.75 if s % 2 == 0 else 0.45
            ultimo_tiempo = s >= 12 and bar % 2 == 1
            if ultimo_tiempo and s == 12:              # redoble en tresillo de semicorchea
                for k in range(6):
                    pon(bat, hat(0.35 + 0.08 * k), ts + k * BEAT / 6, 1.0, 0.3 - 0.1 * k)
            elif not (ultimo_tiempo and s in (13,)):
                pon(bat, hat(vel), ts, 1.0, 0.3 if s % 2 else 0.15)
            if (groove or cierre) and s == 6:
                pon(bat, hat(0.35, True), ts, 1.0, -0.3)
    # campana (motivo discreto) en el groove
    if groove or cierre:
        for s, m in MOTIVO:
            if (bar % 2) * 16 <= s < (bar % 2 + 1) * 16:
                ts = t0 + (s - (bar % 2) * 16) * PASO
                if ts < T_FIN:
                    c = campana(m)
                    pon(fx, c, ts, 0.12, -0.35); pon(fx, c, ts + 0.375, 0.05, 0.35); pon(envio, c, ts, 0.15)

# transición al groove (8 s): platillo invertido
pon(fx, swell(1.0), 5.0, 0.8)
# quiebre: platillo invertido hacia el corte, silencio seco 18,75–19,0 y caída del 808 a los 19,0
pon(fx, swell(1.5), T_CORTE - 1.5, 1.0)
am_raiz, am_voces = AM
pon(bajo, ochoocho(am_raiz, 1.0, am_raiz + 12), T_CAIDA, 0.9)
pon(bat, bombo(), T_CAIDA, 1.0); golpes.append(T_CAIDA)
sn = snare(); pon(bat, sn, T_CAIDA, 0.5); pon(envio, sn, T_CAIDA, 0.4)
a = acorde(am_voces, 1.0, 0.9, 3200); pon(teclas, a, T_CAIDA, 0.5); pon(envio, a, T_CAIDA, 0.4)
for s in range(8, 16):                               # hats vuelven medio segundo después
    pon(bat, hat(0.3 + 0.05 * (s - 8)), T_CAIDA + (s - 8) * PASO + 0.5, 1.0, 0.2)
# final en Am
pon(bajo, ochoocho(am_raiz, 1.0), T_FIN, 0.9)
pon(bat, bombo(), T_FIN, 1.0); golpes.append(T_FIN)
a = acorde(am_voces, 1.0, 1.0, 3000); pon(teclas, a, T_FIN, 0.55); pon(envio, a, T_FIN, 0.6)

# ------------------------------------------------------------------ mezcla
tt = t_(N)
duck = np.ones(N)
for tk in golpes:
    i = int(tk * SR); n = min(int(0.25 * SR), N - i)
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.3 * np.exp(-tt[:n] / 0.08))
duck = duck[:, None]

nir = int(1.4 * SR); tir = t_(nir)
ir = np.stack([lp(rng.standard_normal(nir), 4500) * np.exp(-tir / 0.35) for _ in range(2)], 1) * 0.025
verb = np.stack([hp(fftconvolve(envio[:, c], ir[:, c])[:N], 300) for c in range(2)], 1)

mezcla = teclas * duck * 1.1 + bajo * 0.55 + bat * 1.0 + fx * 0.8 + verb
# silencio seco antes de la caída (deja solo el vinilo)
i0, i1 = int(T_CORTE * SR), int(T_CAIDA * SR)
mezcla[i0:i1] *= 0.0
mezcla[i0:i1] += fx[i0:i1] * 0.3
mezcla = np.stack([hp(mezcla[:, c], 30) for c in range(2)], 1)
fin_n = int(0.6 * SR); i_fin = int(DUR * SR) - fin_n
mezcla[i_fin:i_fin + fin_n] *= np.linspace(1, 0, fin_n)[:, None]
mezcla[i_fin + fin_n:] = 0
mezcla /= np.max(np.abs(mezcla)) + 1e-9
mezcla = np.tanh(1.5 * mezcla) / np.tanh(1.5)

tmp = os.path.join(AQUI, '_tmp.wav')
wavfile.write(tmp, SR, (mezcla[:int(DUR * SR)] * 0.89 * 32767).astype(np.int16))

# normalización a −14 LUFS en dos pasadas (lineal, sin bombeo)
salida = os.path.join(AQUI, 'V5-musica.wav')
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
                      '-f', 'null', '-'], capture_output=True, text=True).stderr
d = json.loads(re.search(r'\{[^{}]*\}', med[med.rfind('{') - 1:], re.S).group(0))
af = ('loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:'
      'measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}').format(**d)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', str(SR), salida], check=True)
os.remove(tmp)
print('ok', salida)
