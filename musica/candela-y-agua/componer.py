#!/usr/bin/env python3
"""«Candela y agua» — sevillana original.

Sigue la forma fija de la sevillana para bailar:
  introducción (7 compases, el primer tiempo en silencio) · salida (6) ·
  primer tercio (12) · pasada (2) · segundo tercio (12) · pasada (2) ·
  tercer tercio (9) · parada seca en el primer tiempo del compás siguiente.

Genera:
  - candela-y-agua.mid       MIDI con una pista por instrumento y la letra
  - candela-y-agua.musicxml  partitura: voz con letra y cifrado, segunda voz, gaita y trompetas
  - candela-y-agua.wav/.mp3  grabación con instrumentos sampleados (si hay fluidsynth y ffmpeg)

Uso:  python3 componer.py [carpeta_salida] [--sin-audio]
Para el audio hace falta fluidsynth y un banco de sonidos .sf2 (por defecto, el
MuseScore General de /usr/share/sounds/sf2; se puede indicar otro con SF2=ruta).
"""
import os
import random
import shutil
import subprocess
import sys

BPM = 192
BAR = 3                   # 3/4, acento en el 1
random.seed(1955)

# ---------------------------------------------------------------- utilidades
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6,
      'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
SPELL = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def midi(name):
    """'F#5' -> 78"""
    n, o = (name[:2], name[2:]) if len(name) > 2 and name[1] in '#b' else (name[:1], name[1:])
    return 12 * (int(o) + 1) + PC[n]


VOICING = {  # posiciones de guitarra (cuerdas de grave a agudo)
    'D': [50, 57, 62, 66], 'G': [43, 47, 50, 55, 59, 67], 'A7': [45, 52, 55, 61, 64],
    'Bb': [46, 53, 58, 62, 65], 'Em7': [40, 47, 50, 55, 59, 64],
}
HIGH = {  # guitarra 2: acordes arriba del mástil
    'D': [62, 66, 69, 74], 'G': [62, 67, 71, 74], 'A7': [61, 64, 67, 69], 'Bb': [62, 65, 70, 74],
    'Em7': [62, 67, 71, 76],
}
QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10]}


class Chord:
    def __init__(self, name):
        root = name[:2] if len(name) > 1 and name[1] in '#b' else name[:1]
        self.q = name[len(root):]
        self.root = self.bass = PC[root]
        self.pcs = [(self.root + i) % 12 for i in QUAL[self.q]]
        self.voicing, self.high = VOICING[name], HIGH[name]
        self.name = name


# ---------------------------------------------------------------- la obra
# Cada compás: (duración en negras, nota).
#   'r' silencio · '-X' ligadura (misma sílaba) · '~X' melisma (nueva nota, misma sílaba)
# Cada verso ocupa 3 compases. Verso de 7 sílabas: | · 1 2 | 3 4 5 | 6— 7 |
#                              verso de 5 sílabas: | · 1 2 | 3——   | 4— 5 |
INTRO = [  # gaita (una octava más alta) y guitarra 2; el primer tiempo calla
    [(1, 'r'), (1, 'A5'), (1, 'B5')],
    [(1, 'A5'), (.5, 'G5'), (.5, 'F#5'), (1, 'D5')],
    [(1, 'B5'), (1, 'D6'), (1, 'B5')],
    [(1.5, 'A5'), (.5, 'G5'), (1, 'E5')],
    [(1, 'F#5'), (.5, 'G5'), (.5, 'A5'), (1, 'F#5')],
    [(1, 'G5'), (1, 'E5'), (1, 'C#5')],
    [(1, 'A5'), (2, 'r')],
]
INTRO_CHORDS = ['D', 'D', 'G', 'A7', 'D', 'A7', 'A7']

SALIDA = [
    [(1, 'r'), (1, 'A4'), (1, 'D5')],
    [(1, 'F#5'), (.5, 'G5'), (.5, '~F#5'), (1, 'E5')],
    [(1, 'E5'), (.5, '~G5'), (.5, '~F#5'), (1, 'E5')],
    [(1, 'r'), (1, 'C#5'), (1, 'E5')],
    [(3, 'G5')],
    [(2, 'F#5'), (1, 'D5')],
]
SALIDA_CHORDS = ['D', 'D', 'A7', 'A7', 'A7', 'D']

TERCIO_A = [
    [(1, 'r'), (1, 'A4'), (1, 'D5')],
    [(1, 'F#5'), (1, 'E5'), (1, 'D5')],
    [(1, 'G5'), (.5, '~A5'), (.5, '~G5'), (1, 'F#5')],
    [(1, 'r'), (1, 'E5'), (1, 'F#5')],
    [(3, 'G5')],
    [(2, 'F#5'), (1, 'E5')],
    [(1, 'r'), (1, 'B4'), (1, 'D5')],
    [(1, 'E5'), (1, 'A5'), (1, 'G5')],
    [(1, 'F#5'), (.5, '~A5'), (.5, '~G5'), (1, 'F#5')],
    [(1, 'r'), (1, 'D5'), (1, 'F5')],
    [(3, 'G5')],
    [(2, 'E5'), (1, 'D5')],
]
TERCIO_B = TERCIO_A[:6] + [  # el segundo tercio sube en su segunda mitad
    [(1, 'r'), (1, 'D5'), (1, 'G5')],
    [(1, 'A5'), (1, 'B5'), (1, 'A5')],
    [(1, 'A5'), (.5, '~B5'), (.5, '~A5'), (1, 'F#5')],
    [(1, 'r'), (1, 'F5'), (1, 'G5')],
    [(3, 'A5')],
    [(2, 'E5'), (1, 'D5')],
]
TERCIO_CHORDS = ['D', 'D', 'G', 'A7', 'A7', 'D', 'G', 'A7', 'D', 'Bb', 'A7', 'D']

TERCIO_C = [  # el estribillo, más corto: acaba en la parada
    [(1, 'r'), (1, 'B4'), (1, 'D5')],
    [(3, 'F5')],
    [(2, 'E5'), (1, 'C#5')],
    [(1, 'r'), (1, 'D5'), (1, 'F#5')],
    [(1, 'G5'), (1, 'B5'), (1, 'A5')],
    [(1, 'A5'), (.5, '~B5'), (.5, '~A5'), (1, 'G5')],
    [(1, 'r'), (1, 'E5'), (1, 'F#5')],
    [(3, 'G5')],
    [(2, 'E5'), (1, 'D5')],
]
TERCIO_C_CHORDS = ['G', 'Bb', 'A7', 'D', 'G', 'A7', 'Em7', 'A7', 'D']

LETRA = {  # seguidilla 7-5-7-5 con estribillo 5-7-5   («‿» = sinalefa)
    1: "Ten-go‿un cas-co de pla-ta", 2: "y‿u-na‿es-ca-le-ra", 3: "pa-ra su-bir al cie-lo",
    4: "cuan-do tú quie-ras.", 5: "Que no‿hay can-de-la", 6: "que me que-me por den-tro",
    7: "co-mo tu‿au-sen-cia.",
}

# Forma (compases)
S_INTRO, S_SALIDA, S_T1, S_P1, S_T2, S_P2, S_T3, S_PARADA, N_BARS = 0, 7, 13, 25, 27, 39, 41, 50, 51
SECTIONS = [(S_INTRO, 'Introducción'), (S_SALIDA, 'Salida'), (S_T1, 'Primer tercio'), (S_P1, 'Pasada'),
            (S_T2, 'Segundo tercio'), (S_P2, 'Pasada'), (S_T3, 'Tercer tercio'), (S_PARADA, 'Parada')]
PASADA_CHORDS = ['D', 'A7']

chords = [None] * N_BARS
for start, seq in ((S_INTRO, INTRO_CHORDS), (S_SALIDA, SALIDA_CHORDS), (S_T1, TERCIO_CHORDS),
                   (S_P1, PASADA_CHORDS), (S_T2, TERCIO_CHORDS), (S_P2, PASADA_CHORDS),
                   (S_T3, TERCIO_C_CHORDS), (S_PARADA, ['D'])):
    for i, c in enumerate(seq):
        chords[start + i] = Chord(c)


def scale_at(bar):
    pcs = [(2 + i) % 12 for i in (0, 2, 4, 5, 7, 9, 11)]   # Re mayor
    for cp in chords[bar].pcs:         # el acorde manda (Fa natural en Sib...)
        pcs = [cp if (p - cp) % 12 in (1, 11) else p for p in pcs]
    return sorted(set(pcs))


def section_of(bar):
    name = None
    for start, n in SECTIONS:
        if bar >= start:
            name = n
    return name


# ---------------------------------------------------------------- notas
class N:
    __slots__ = ('trk', 't', 'd', 'p', 'v', 'syl', 'tie')

    def __init__(self, trk, t, d, p, v, syl=None, tie=False):
        self.trk, self.t, self.d, self.p, self.v = trk, t, d, p, v
        self.syl, self.tie = syl, tie


notes = []          # notas con altura
strums = []         # rasgueos: (pista, t, voicing, dirección, velocidad, duración)
perc = []           # percusión: (instrumento, t, velocidad)


def put_line(trk, bar0, bars, vel, transpose=0, syllables=None):
    out, si, t = [], 0, bar0 * BAR
    for bar in bars:
        for d, s in bar:
            if s != 'r':
                kind = s[0] if s[0] in '-~' else ''
                syl = None
                if kind == '' and syllables is not None:
                    syl = syllables[si]
                    si += 1
                n = N(trk, t, d, midi(s.lstrip('-~')) + transpose, vel, syl, tie=(kind == '-'))
                notes.append(n)
                out.append(n)
            t += d
    if syllables is not None:
        assert si == len(syllables), (bar0, si, len(syllables))
    return out


def syllables(*lines):
    out = []
    for li in lines:
        for w in LETRA[li].split():
            parts = w.split('-')
            for i, p in enumerate(parts):
                kind = 'single' if len(parts) == 1 else 'begin' if i == 0 else 'end' if i == len(parts) - 1 else 'middle'
                out.append((p, kind))
    return out


def nearest(pcs, lo, hi, target):
    cands = [p for p in range(lo, hi + 1) if p % 12 in pcs]
    return min(cands, key=lambda p: (abs(p - target), p))


def third_below(p, bar):
    cands = [q for q in range(p - 5, p - 2) if q % 12 in chords[bar].pcs]
    if not cands:
        cands = [q for q in range(p - 5, p - 1) if q % 12 in scale_at(bar)] or [p - 4]
    return min(cands, key=lambda q: abs(p - 4 - q))


def harmonize(src, trk, vel_drop):
    for n in src:
        notes.append(N(trk, n.t, n.d, third_below(n.p, int(n.t // BAR)), n.v - vel_drop, n.syl, n.tie))


# --- cante: salida (versos 1-2) · tercio 1 (1-2-3-4) · tercio 2 (3-4-3-4) · tercio 3 (estribillo 5-6-7)
voz = put_line('voz', S_SALIDA, SALIDA, 90, syllables=syllables(1, 2))
voz += put_line('voz', S_T1, TERCIO_A, 92, syllables=syllables(1, 2, 3, 4))
t2 = put_line('voz', S_T2, TERCIO_B, 96, syllables=syllables(3, 4, 3, 4))
t3 = put_line('voz', S_T3, TERCIO_C, 100, syllables=syllables(5, 6, 7))
notes.append(N('voz', S_PARADA * BAR, 1, midi('D5'), 100, tie=True))   # la última sílaba llega a la parada
harmonize(t2 + t3 + [notes[-1]], 'voz2', 14)

# --- gaita rociera, mandolina y trompetas
put_line('gaita', S_INTRO, INTRO, 88, transpose=12)
put_line('gtr2', S_INTRO, INTRO, 86)
put_line('mandolina', S_INTRO + 3, INTRO[3:], 70)
FANFARRIA = [[(1, 'A4'), (.5, 'D5'), (.5, 'E5'), (1, 'F#5')], [(1, 'E5'), (1, 'C#5'), (1, 'A4')]]
for p, vel in ((S_P1, 90), (S_P2, 100)):
    harmonize(put_line('trompeta1', p, FANFARRIA, vel), 'trompeta2', 8)
    put_line('gaita', p, [[(3, 'r')], [(.5, 'E6'), (.5, 'F#6'), (.5, 'E6'), (.5, 'C#6'), (1, 'A5')]], 84)
# en el tercer tercio las trompetas doblan al cante en los dos últimos versos
tp = [N('trompeta1', n.t, n.d, n.p - 12, 74, None, n.tie) for n in t3 if n.t >= (S_T3 + 3) * BAR]
notes.extend(tp)
harmonize(tp, 'trompeta2', 8)


def fill(bar, trk, vel, beat0=1, octave=0):
    """Respuesta en corcheas mientras el cante sostiene una nota larga."""
    ch, sc = chords[bar], scale_at(bar)
    run = [p for p in range(74, 96) if p % 12 in ch.pcs][:3]
    p = run[-1]
    while len(run) < int((3 - beat0) * 2):
        p -= 1
        while p % 12 not in sc:
            p -= 1
        run.append(p)
    for i, p in enumerate(run):
        notes.append(N(trk, bar * BAR + beat0 + i * .5, .5, p + octave, vel))


# las notas largas del cante (3.ª sílaba de los versos de 5) se contestan
for rel in (4, 10):
    fill(S_T1 + rel, 'gtr2', 84, octave=-12)
    fill(S_T2 + rel, 'gaita', 74)
fill(S_SALIDA + 4, 'gtr2', 70, octave=-12)
fill(S_T3 + 1, 'mandolina', 72, octave=-12)
fill(S_T3 + 7, 'gaita', 80)

# parada: todos a la vez en el primer tiempo
ft = S_PARADA * BAR
notes.extend(N('trompeta1', ft, 1, p, 110) for p in (66, 69, 74))
notes.append(N('gaita', ft, 1, midi('D6'), 96))
notes.append(N('mandolina', ft, 1, midi('D5'), 90))

# cuerdas y violonchelo: notas largas que sostienen la armonía en los tercios
prev = 78
for bar in range(S_T1, S_PARADA):
    if S_P1 <= bar < S_T2 or S_P2 <= bar < S_T3:
        continue
    vel = 50 if bar < S_T2 else 58 if bar < S_T3 else 64
    if bar >= S_T2:
        prev = nearest(chords[bar].pcs, 72, 84, prev)
        notes.append(N('cuerdas', bar * BAR, 3, prev, vel))
        notes.append(N('cuerdas', bar * BAR, 3, third_below(prev, bar), vel - 8))
    notes.append(N('chelo', bar * BAR, 3, nearest([chords[bar].root], 38, 50, 45) + 12, vel))

# contrabajo: tónica en el 1 y quinta en el 3
for bar in range(S_INTRO, S_PARADA + 1):
    ch = chords[bar]
    root = nearest([ch.bass], 38, 50, 44)
    if bar == S_PARADA:
        notes.append(N('bajo', bar * BAR, 1, root, 112))
    elif S_SALIDA <= bar < S_T1:
        notes.append(N('bajo', bar * BAR, 2.5, root, 70))
    else:
        start = 1 if bar == S_INTRO else 0
        notes.append(N('bajo', bar * BAR + start, 1.8 - start, root, 96))
        notes.append(N('bajo', bar * BAR + 2, .9, root + 7 if root + 7 <= 52 else root - 5, 78))


# --- guitarras: el rasgueado lleva el compás
def rasgueo(bar, vel, line_end=False):
    """Guitarra 1, compás de sevillana: GOLPE en el 1 (con abanico rápido que acaba EN el tiempo),
    abajo en el 2, arriba en el «y», abajo en el 3. Al final de cada verso, remate en el 3."""
    v, t0 = chords[bar].voicing, bar * BAR
    if bar == S_INTRO:                            # el primer tiempo de la introducción calla
        pass
    else:
        if bar % 2 == 0:                          # abanico de tres dedos antes del golpe
            for k, off in enumerate((-.21, -.14, -.07)):
                strums.append(('gtr1', t0 + off, v, 'down' if k % 2 == 0 else 'up', vel * (.42 + .08 * k), .07))
        strums.append(('gtr1', t0, v, 'down', vel, 1))
    strums.append(('gtr1', t0 + 1, v, 'down', vel * .74, .5))
    strums.append(('gtr1', t0 + 1.5, v, 'up', vel * .56, .5))
    if line_end:                                  # remate: golpe fuerte y seco en el 3
        strums.append(('gtr1', t0 + 2, v, 'down', vel * .95, .45))
    else:
        strums.append(('gtr1', t0 + 2, v, 'down', vel * .8, .5))
        strums.append(('gtr1', t0 + 2.5, v, 'up', vel * .5, .5))


def acompanamiento_suave(bar, vel):
    """Durante la salida la guitarra casi calla: un acorde en el 1 y otro en el 3."""
    v, t0 = chords[bar].voicing, bar * BAR
    strums.append(('gtr1', t0, v, 'down', vel, 2))
    strums.append(('gtr1', t0 + 2, v, 'down', vel * .7, 1))


def contestacion(bar, vel):
    """Guitarra 2 en los tercios: acorde agudo en el 2 y el 3, deja el 1 a la guitarra 1."""
    v, t0 = chords[bar].high, bar * BAR
    strums.append(('gtr2', t0 + 1, v, 'down', vel, .5))
    strums.append(('gtr2', t0 + 2, v, 'down', vel * .85, .5))
    strums.append(('gtr2', t0 + 2.5, v, 'up', vel * .6, .5))


def line_end(bar):
    for s0, length in ((S_SALIDA, 6), (S_T1, 12), (S_T2, 12), (S_T3, 9)):
        if s0 <= bar < s0 + length:
            return (bar - s0) % 3 == 2
    return bar in (S_INTRO + 6, S_P1 + 1, S_P2 + 1)


filled = {int(n.t // BAR) for n in notes if n.trk == 'gtr2'}
for bar in range(S_INTRO, S_PARADA):
    if S_SALIDA <= bar < S_T1:
        acompanamiento_suave(bar, 70)
        continue
    base = 96 if bar < S_SALIDA else 104 if section_of(bar) == 'Pasada' else 90 if bar < S_T2 else 96
    rasgueo(bar, base, line_end(bar))
    if bar >= S_T1 and section_of(bar) != 'Pasada' and bar not in filled:
        contestacion(bar, 64 if bar < S_T2 else 72)
strums.append(('gtr1', S_PARADA * BAR, chords[S_PARADA].voicing, 'down', 124, 1))
strums.append(('gtr2', S_PARADA * BAR, chords[S_PARADA].high, 'down', 116, 1))


# --- percusión: palmas en los tres tiempos (acento en el 1), castañuelas y tamboril
def palmas(bar, vel=1.0):
    t0 = bar * BAR
    for b, v in ((0, 108), (1, 80), (2, 90)):
        if not (bar == S_INTRO and b == 0):
            perc.append(('palma', t0 + b, v * vel))
            perc.append(('palma2', t0 + b + .012, v * vel * .8))   # un segundo palmero, algo detrás


def castanuelas(bar, vel=1.0):
    t0 = bar * BAR
    if not bar == S_INTRO:
        for k, off in enumerate((-.24, -.18, -.12, -.06)):        # carretilla que llega al 1
            perc.append(('casta', t0 + off, (54 + 8 * k) * vel))
        perc.append(('casta', t0, 104 * vel))
    perc.extend([('casta', t0 + 1, 76 * vel), ('casta', t0 + 2, 92 * vel)])


def tamboril(bar, vel=1.0):
    t0 = bar * BAR
    perc.extend([('tamboril', t0, 100 * vel), ('tamboril', t0 + 2, 80 * vel), ('tamboril', t0 + 2.5, 60 * vel)])


for bar in range(S_INTRO, S_PARADA):
    sec = section_of(bar)
    if sec == 'Salida':
        continue
    palmas(bar, .8 if sec == 'Primer tercio' else 1.0)
    if sec in ('Introducción', 'Pasada', 'Tercer tercio') or (sec == 'Segundo tercio' and line_end(bar)):
        castanuelas(bar)
    if sec in ('Introducción', 'Pasada'):
        tamboril(bar)
ft = S_PARADA * BAR
perc += [('palma', ft, 124), ('palma2', ft + .01, 110), ('casta', ft, 124), ('tamboril', ft, 120)]
for k, off in enumerate((-.24, -.18, -.12, -.06)):
    perc.append(('casta', ft + off, 60 + 10 * k))

TOTAL_BEATS = N_BARS * BAR

# ================================================================ MIDI
TPB = 480
# pista: (clave, nombre, canal, banco, programa, volumen, panorama 0-127, reverb)
INSTRUMENTS = [
    ('voz', 'Voz (coro)', 0, 0, 52, 104, 64, 62),
    ('voz2', 'Segunda voz', 1, 0, 53, 84, 72, 62),
    ('gaita', 'Gaita rociera', 2, 0, 72, 76, 86, 55),
    ('gtr1', 'Guitarra flamenca 1', 3, 0, 24, 122, 46, 34),
    ('gtr2', 'Guitarra flamenca 2', 4, 0, 24, 100, 84, 36),
    ('mandolina', 'Mandolina', 5, 16, 25, 70, 100, 45),
    ('chelo', 'Violonchelo', 6, 0, 42, 58, 38, 64),
    ('bajo', 'Contrabajo', 7, 0, 32, 96, 64, 18),
    ('trompeta', 'Trompetas', 8, 0, 56, 90, 78, 58),
    ('cuerdas', 'Cuerdas', 10, 0, 49, 54, 54, 76),
]
DRUMS = {'palma': (39, 1.0), 'palma2': (39, .9), 'casta': (85, 1.0), 'tamboril': (38, .7)}
TREMOLO = {'mandolina'}


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(b))


def midi_track(events, name):
    data = b'\x00\xff\x03' + vlq(len(name.encode())) + name.encode()
    last = 0
    for tick, _, ev in sorted(events, key=lambda e: (e[0], e[1])):
        data += vlq(tick - last) + ev
        last = tick
    data += b'\x00\xff\x2f\x00'
    return b'MTrk' + len(data).to_bytes(4, 'big') + data


def tk(beats):
    return max(0, int(round(beats * TPB)))


def jitter(sd_ticks):
    return int(max(-2 * sd_ticks, min(2 * sd_ticks, random.gauss(0, sd_ticks))))


def write_midi(path):
    tempo = int(60_000_000 / BPM)
    meta = [(0, 0, b'\xff\x51\x03' + tempo.to_bytes(3, 'big')), (0, 0, b'\xff\x58\x04\x03\x02\x18\x08'),
            (0, 0, b'\xff\x59\x02\x02\x00')]
    for bar, name in SECTIONS:
        txt = name.encode('utf-8')
        meta.append((tk(bar * BAR), 1, b'\xff\x06' + vlq(len(txt)) + txt))
    tracks = [midi_track(meta, 'Candela y agua')]
    for key, name, ch, bank, prog, vol, pan, rev in INSTRUMENTS:
        ev = [(0, 0, bytes([0xB0 | ch, 0, bank])), (0, 0, bytes([0xB0 | ch, 32, 0])),
              (0, 0, bytes([0xC0 | ch, prog])), (0, 0, bytes([0xB0 | ch, 7, vol])),
              (0, 0, bytes([0xB0 | ch, 10, pan])), (0, 0, bytes([0xB0 | ch, 91, rev])),
              (0, 0, bytes([0xB0 | ch, 93, 0]))]
        src = [n for n in notes if n.trk == key or (key == 'trompeta' and n.trk.startswith(key))]
        for trk, t, v, direction, vel, d in strums:
            if trk == key:
                order = v if direction == 'down' else list(reversed(v))
                spread = .028 if direction == 'down' else .02     # ~9 ms entre cuerdas
                for i, p in enumerate(order):
                    src.append(N(key, t + i * spread, d - i * spread, p, int(min(127, vel * random.uniform(.92, 1.04)))))
        merged = []                                   # une notas ligadas
        for n in sorted(src, key=lambda n: (n.t, n.p)):
            prevs = [m for m in merged[-4:] if m.p == n.p and abs(m.t + m.d - n.t) < 1e-6]
            if n.tie and prevs:
                prevs[-1].d += n.d
                continue
            merged.append(N(n.trk, n.t, n.d, n.p, n.v, n.syl))
        if key in TREMOLO:                            # trémolo de púa: repite la nota en semicorcheas
            trem = []
            for n in merged:
                k = 0
                while k * .25 < n.d - .01:
                    trem.append(N(n.trk, n.t + k * .25, .25, n.p, n.v * (1 if k % 2 == 0 else .8)))
                    k += 1
            merged = trem
        legato = key in ('voz', 'voz2', 'gaita', 'trompeta', 'cuerdas', 'chelo')
        sd = 2 if key in ('gtr1', 'gtr2', 'bajo') else 5
        for n in merged:
            on = tk(n.t) + jitter(sd)
            off = tk(n.t + n.d) - (5 if legato else 20)
            v = int(max(1, min(127, n.v * random.uniform(.95, 1.04))))
            ev.append((max(0, on), 2, bytes([0x90 | ch, n.p, v])))
            ev.append((max(on + 15, off), 0, bytes([0x80 | ch, n.p, 0])))
            if n.syl and key == 'voz':
                txt = (n.syl[0] + ('-' if n.syl[1] in ('begin', 'middle') else ' ')).encode('utf-8')
                ev.append((max(0, on), 1, b'\xff\x05' + vlq(len(txt)) + txt))
        tracks.append(midi_track(ev, name))
    ev = [(0, 0, bytes([0xB9, 7, 112])), (0, 0, bytes([0xB9, 91, 38]))]
    for k, t, v in perc:
        note, scale = DRUMS[k]
        on = tk(t) + jitter(3)
        vel = int(max(1, min(127, v * scale * random.uniform(.92, 1.05))))
        ev.append((max(0, on), 2, bytes([0x99, note, vel])))
        ev.append((max(0, on) + 60, 0, bytes([0x89, note, 0])))
    tracks.append(midi_track(ev, 'Palmas, castañuelas y tamboril'))
    head = b'MThd' + (6).to_bytes(4, 'big') + (1).to_bytes(2, 'big') + len(tracks).to_bytes(2, 'big') + TPB.to_bytes(2, 'big')
    with open(path, 'wb') as f:
        f.write(head + b''.join(tracks))


# ================================================================ MusicXML
def write_musicxml(path):
    DIV = 4
    KINDS = {'': 'major', 'm': 'minor', '7': 'dominant', 'm7': 'minor-seventh'}
    TYPES = [(12, 'half', 1), (8, 'half', 0), (6, 'quarter', 1), (4, 'quarter', 0), (3, 'eighth', 1),
             (2, 'eighth', 0), (1, '16th', 0)]

    def pitch_xml(p):
        name = SPELL[p % 12]
        step, alter = name[0], {'#': 1, 'b': -1}.get(name[1:2], 0)
        a = f'<alter>{alter}</alter>' if alter else ''
        return f'<pitch><step>{step}</step>{a}<octave>{p // 12 - 1}</octave></pitch>'

    def pieces(d):
        out = []
        while d > 0:
            for u, typ, dot in TYPES:
                if u <= d:
                    out.append((u, typ, dot))
                    d -= u
                    break
        return out

    def rest(u, typ, dot):
        return f'<note><rest/><duration>{u}</duration><type>{typ}</type>{"<dot/>" * dot}</note>'

    def part_xml(pid, src, lead):
        events = sorted(src, key=lambda n: n.t)
        measures, ei, carry = [], 0, []
        for bar in range(N_BARS):
            m0, m1 = bar * BAR * DIV, (bar + 1) * BAR * DIV
            xml = [f'<measure number="{bar + 1}">']
            if bar == 0:
                xml.append(f'<attributes><divisions>{DIV}</divisions><key><fifths>2</fifths></key>'
                           '<time><beats>3</beats><beat-type>4</beat-type></time>'
                           '<clef><sign>G</sign><line>2</line></clef></attributes>')
                if lead:
                    xml.append('<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit>'
                               f'<per-minute>{BPM}</per-minute></metronome></direction-type><sound tempo="{BPM}"/></direction>')
            if lead:
                for sb, name in SECTIONS:
                    if sb == bar:
                        xml.append(f'<direction placement="above"><direction-type><rehearsal>{name}</rehearsal>'
                                   '</direction-type></direction>')
                ch = chords[bar]
                rn = SPELL[ch.root]
                ralt = f'<root-alter>{1 if rn[1:] == "#" else -1}</root-alter>' if rn[1:] else ''
                xml.append(f'<harmony><root><root-step>{rn[0]}</root-step>{ralt}</root><kind>{KINDS[ch.q]}</kind></harmony>')
            seg, carry = list(carry), []
            while ei < len(events) and events[ei].t * DIV < m1:
                n = events[ei]
                s, e = int(round(n.t * DIV)), int(round((n.t + n.d) * DIV))
                seg.append([s, e, n.p, n.syl if lead else None, n.tie, False])
                ei += 1
            fixed = []
            for s in seg:
                if s[1] > m1:
                    carry.append([m1, s[1], s[2], None, True, False])
                    s[1], s[5] = m1, True
                fixed.append(s)
            pos = m0
            for s, e, p, syl, tie_in, tie_out in sorted(fixed):
                if s > pos:
                    xml.extend(rest(*x) for x in pieces(s - pos))
                ps = pieces(e - s)
                for k, (u, typ, dot) in enumerate(ps):
                    tin, tout = tie_in or k > 0, tie_out or k < len(ps) - 1
                    ties = ('<tie type="stop"/>' if tin else '') + ('<tie type="start"/>' if tout else '')
                    tied = ('<tied type="stop"/>' if tin else '') + ('<tied type="start"/>' if tout else '')
                    lyr = ''
                    if syl and k == 0:
                        lyr = f'<lyric number="1"><syllabic>{syl[1]}</syllabic><text>{syl[0]}</text></lyric>'
                    xml.append(f'<note>{pitch_xml(p)}<duration>{u}</duration>{ties}<type>{typ}</type>'
                               f'{"<dot/>" * dot}' + (f'<notations>{tied}</notations>' if tied else '') + f'{lyr}</note>')
                pos = e
            if pos < m1:
                xml.extend(rest(*x) for x in pieces(m1 - pos))
            if bar == N_BARS - 1:
                xml.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
            xml.append('</measure>')
            measures.append(''.join(xml))
        return f'<part id="{pid}">' + '\n'.join(measures) + '</part>'

    def mono(trk):
        """Una sola voz por pentagrama: si dos notas se solapan, manda la más reciente."""
        src = sorted([n for n in notes if n.trk == trk], key=lambda n: (n.t, -n.p))
        out = []
        for n in src:
            if out and out[-1].t == n.t:
                continue
            c = N(n.trk, n.t, n.d, n.p, n.v, n.syl, n.tie)
            if out and out[-1].t + out[-1].d > c.t:
                out[-1].d = c.t - out[-1].t
            out.append(c)
        return [n for n in out if n.d > 0]

    parts = [('P1', 'Voz', part_xml('P1', mono('voz'), True)),
             ('P2', 'Segunda voz', part_xml('P2', mono('voz2'), False)),
             ('P3', 'Gaita rociera', part_xml('P3', mono('gaita'), False)),
             ('P4', 'Trompeta 1', part_xml('P4', mono('trompeta1'), False)),
             ('P5', 'Trompeta 2', part_xml('P5', mono('trompeta2'), False))]
    plist = ''.join(f'<score-part id="{pid}"><part-name>{name}</part-name></score-part>' for pid, name, _ in parts)
    doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" '
           '"http://www.musicxml.org/dtds/partwise.dtd">\n'
           '<score-partwise version="3.1"><work><work-title>Candela y agua</work-title></work>'
           '<identification><creator type="composer">Sevillana original</creator></identification>'
           f'<part-list>{plist}</part-list>\n' + '\n'.join(x for _, _, x in parts) + '</score-partwise>\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)


# ================================================================ audio
def render_audio(mid, wav, mp3):
    sf2 = os.environ.get('SF2', '/usr/share/sounds/sf2/MuseScore_General_Full.sf2')
    if not (shutil.which('fluidsynth') and os.path.exists(sf2)):
        print('Sin fluidsynth o sin banco de sonidos: no se genera el audio.')
        return
    raw = wav + '.raw.wav'
    subprocess.run(['fluidsynth', '-ni', '-q', '-r', '44100', '-g', '0.5',
                    '-o', 'synth.reverb.room-size=0.45', '-o', 'synth.reverb.damp=0.4',
                    '-o', 'synth.reverb.width=0.9', '-o', 'synth.reverb.level=0.5',
                    '-o', 'synth.chorus.active=0', '-o', 'synth.polyphony=512',
                    '-F', raw, sf2, mid], check=True)
    if shutil.which('ffmpeg'):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-af',
                        'highpass=f=35,loudnorm=I=-14:TP=-1.2:LRA=11', '-ar', '44100', wav], check=True)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-codec:a', 'libmp3lame', '-b:a', '192k',
                        '-metadata', 'title=Candela y agua (sevillana)', mp3], check=True)
        os.remove(raw)
    else:
        os.replace(raw, wav)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out = args[0] if args else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, 'candela-y-agua')
    write_midi(base + '.mid')
    write_musicxml(base + '.musicxml')
    if '--sin-audio' not in sys.argv:
        render_audio(base + '.mid', base + '.wav', base + '.mp3')
    print(f'{N_BARS} compases, {TOTAL_BEATS * 60 / BPM:.1f} s a {BPM} negras por minuto')
