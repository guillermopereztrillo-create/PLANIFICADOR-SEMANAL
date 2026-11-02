#!/usr/bin/env python3
"""«Candela y agua» — sevillanas originales.

Cuatro sevillanas seguidas con la misma música y distinta copla, como en los
discos de sevillanas (para bailar «las cuatro»). Cada una sigue la forma fija:
  introducción (7 compases, el primer tiempo en silencio) · salida (6) ·
  primer tercio (12) · pasada (2) · segundo tercio (12) · pasada (2) ·
  tercer tercio (9) · parada seca en el primer tiempo del compás siguiente.

Tempo, tonalidad y dibujo del rasgueo tomados de una medición de «Las Palmas»
(Brisa de la Puebla): ♩ ≈ 174, Mi mayor, golpe en el 1 y corcheas seguidas con
acento en el «y» del 2 y en el 3. La melodía, la armonía y la letra son nuevas.

Genera:
  - candela-y-agua.mid       MIDI con una pista por instrumento y la letra
  - candela-y-agua.musicxml  partitura: voz con letra y cifrado, segunda voz, gaita y trompetas
  - candela-y-agua.wav/.mp3  grabación con instrumentos sampleados (si hay fluidsynth y ffmpeg)

Uso:  python3 componer.py [carpeta_salida] [--sin-audio]
Para el audio hace falta fluidsynth y un banco de sonidos .sf2 (por defecto, el
MuseScore General de /usr/share/sounds/sf2; se puede indicar otro con SF2=ruta).
"""
import math
import os
import random
import shutil
import subprocess
import sys

BPM = 174
BAR = 3                   # 3/4, acento en el 1
T = 2                     # la melodía está escrita en Re y suena en Mi
random.seed(1955)

# ---------------------------------------------------------------- utilidades
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6,
      'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
SPELL = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def midi(name):
    """'F#5' -> 78"""
    n, o = (name[:2], name[2:]) if len(name) > 2 and name[1] in '#b' else (name[:1], name[1:])
    return 12 * (int(o) + 1) + PC[n]


VOICING = {  # guitarra 1, posiciones abiertas en Mi (cuerdas de grave a agudo)
    'E': [40, 47, 52, 56, 59, 64], 'A': [45, 52, 57, 61, 64], 'B7': [47, 51, 57, 59, 66],
    'C': [48, 52, 55, 60, 64], 'F#m7': [42, 49, 52, 57, 61, 64],
    'Am': [45, 52, 57, 60, 64], 'G': [43, 47, 50, 55, 59, 67], 'F': [41, 48, 53, 57, 60, 65],
}
HIGH = {  # guitarra 2: acordes arriba del mástil
    'E': [64, 68, 71, 76], 'A': [64, 69, 73, 76], 'B7': [63, 66, 69, 71], 'C': [64, 67, 72, 76],
    'F#m7': [61, 64, 69, 73], 'Am': [64, 69, 72, 76], 'G': [62, 67, 71, 74], 'F': [65, 69, 72, 77],
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


# ---------------------------------------------------------------- la música (una sevillana)
# Cada compás: (duración en negras, nota), escrito en Re (suena un tono más alto).
#   'r' silencio · '-X' ligadura (misma sílaba) · '~X' melisma (nueva nota, misma sílaba)
# Cada verso ocupa 3 compases. Verso de 7 sílabas: | · 1 2 | 3 4 5 | 6— 7 |
#                              verso de 5 sílabas: | · 1 2 | 3——   | 4— 5 |
INTRO = [
    [(1, 'r'), (1, 'A5'), (1, 'B5')],
    [(1, 'A5'), (.5, 'G5'), (.5, 'F#5'), (1, 'D5')],
    [(1, 'B5'), (1, 'D6'), (1, 'B5')],
    [(1.5, 'A5'), (.5, 'G5'), (1, 'E5')],
    [(1, 'F#5'), (.5, 'G5'), (.5, 'A5'), (1, 'F#5')],
    [(1, 'G5'), (1, 'E5'), (1, 'C#5')],
    [(1, 'A5'), (2, 'r')],
]
SALIDA = [
    [(1, 'r'), (1, 'A4'), (1, 'D5')],
    [(1, 'F#5'), (.5, 'G5'), (.5, '~F#5'), (1, 'E5')],
    [(1, 'E5'), (.5, '~G5'), (.5, '~F#5'), (1, 'E5')],
    [(1, 'r'), (1, 'C#5'), (1, 'E5')],
    [(3, 'G5')],
    [(2, 'F#5'), (1, 'D5')],
]
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
# Falseta de la introducción (ya en Mi, sin transportar): cadencia andaluza Lam-Sol-Fa-Mi
# que desemboca en el Mi mayor del cante. El primer tiempo calla.
FALSETA = [
    [(1, 'r'), (.5, 'E5'), (.5, 'F5'), (.5, 'E5'), (.5, 'D5')],
    [(.5, 'C5'), (.5, 'D5'), (.5, 'B4'), (.5, 'C5'), (1, 'D5')],
    [(.5, 'C5'), (.5, 'A4'), (.5, 'F4'), (.5, 'A4'), (1, 'C5')],
    [(1.5, 'B4'), (.5, 'A4'), (.5, 'G#4'), (.5, 'F4')],
    [(.5, 'E5'), (.5, 'A5'), (.5, 'C6'), (.5, 'B5'), (.5, 'A5'), (.5, 'G5')],
    [(.5, 'F5'), (.5, 'E5'), (.5, 'D5'), (.5, 'C5'), (.5, 'B4'), (.5, 'A4')],
    [(1, 'G#4'), (2, 'r')],
]
# Pasada (ya en Mi): cadencia frigia Fa-Mi
FANFARRIA = [[(1, 'A4'), (.5, 'C5'), (.5, 'B4'), (1, 'A4')], [(1, 'G#4'), (1, 'B4'), (1, 'E5')]]
PASADA_GAITA = [[(3, 'r')], [(.5, 'G#5'), (.5, 'B5'), (.5, 'E6'), (.5, 'D6'), (1, 'B5')]]

INTRO_CHORDS = ['Am', 'G', 'F', 'E', 'Am', 'F', 'E']
SALIDA_CHORDS = ['E', 'E', 'B7', 'B7', 'B7', 'E']
TERCIO_CHORDS = ['E', 'E', 'A', 'B7', 'B7', 'E', 'A', 'B7', 'E', 'C', 'B7', 'E']
PASADA_CHORDS = ['F', 'E']
TERCIO_C_CHORDS = ['A', 'C', 'B7', 'E', 'A', 'B7', 'F#m7', 'B7', 'E']

# forma de una sevillana, en compases desde su comienzo
I_INTRO, I_SALIDA, I_T1, I_P1, I_T2, I_P2, I_T3, I_PARADA, LEN = 0, 7, 13, 25, 27, 39, 41, 50, 51
PARTES = [(I_INTRO, 'Introducción', INTRO_CHORDS), (I_SALIDA, 'Salida', SALIDA_CHORDS),
          (I_T1, 'Primer tercio', TERCIO_CHORDS), (I_P1, 'Pasada', PASADA_CHORDS),
          (I_T2, 'Segundo tercio', TERCIO_CHORDS), (I_P2, 'Pasada', PASADA_CHORDS),
          (I_T3, 'Tercer tercio', TERCIO_C_CHORDS), (I_PARADA, 'Parada', ['E'])]

# ---------------------------------------------------------------- las cuatro coplas
COPLAS = [  # seguidillas 7-5-7-5 con estribillo 5-7-5   («‿» = sinalefa)
    ["A-gua de ma-dru-ga-da", "so-bre la bra-sa,", "lo que‿el fue-go le-van-ta", "el a-gua‿en cal-ma.",
     "Si-re-na‿y a-gua,", "que‿en-tre‿el hu-mo‿y la no-che", "des-pun-ta‿el al-ba."],
    ["Ten-go‿un cas-co de pla-ta", "y‿u-na‿es-ca-le-ra", "pa-ra su-bir al cie-lo", "cuan-do tú quie-ras.",
     "Que no‿hay can-de-la", "que me que-me por den-tro", "co-mo tu‿au-sen-cia."],
    ["Se-vi-lla tie-ne‿un rí-o", "que no se‿a-pa-ga,", "y‿un fue-go‿en ca-da pa-tio", "que‿el a-gua guar-da.",
     "Can-de-la‿y a-gua,", "mi Se-vi-lla‿es un can-te", "que nun-ca‿a-ca-ba."],
    ["Cuan-do‿a-pa-gue la no-che", "la‿úl-ti-ma lla-ma,", "ven-dré por la ri-be-ra", "con la ma-ña-na.",
     "A-gua que can-ta,", "can-de-la que se‿en-cien-de", "cuan-do tú bai-las."],
]
N_SEV = len(COPLAS)
N_BARS = N_SEV * LEN
SECTIONS = []
chords = [None] * N_BARS
for k in range(N_SEV):
    for off, name, seq in PARTES:
        label = f'Sevillana {k + 1}' if name == 'Introducción' else name
        SECTIONS.append((k * LEN + off, label))
        for i, c in enumerate(seq):
            chords[k * LEN + off + i] = Chord(c)


def scale_at(bar):
    pcs = [(4 + i) % 12 for i in (0, 2, 4, 5, 7, 9, 11)]   # Mi mayor
    for cp in chords[bar].pcs:         # el acorde manda (Sol natural en Do...)
        pcs = [cp if (p - cp) % 12 in (1, 11) else p for p in pcs]
    return sorted(set(pcs))


def part_of(bar):
    rel, name = bar % LEN, None
    for off, n, _ in PARTES:
        if rel >= off:
            name = n
    return name


def line_end(bar):
    rel = bar % LEN
    for s0, length in ((I_SALIDA, 6), (I_T1, 12), (I_T2, 12), (I_T3, 9)):
        if s0 <= rel < s0 + length:
            return (rel - s0) % 3 == 2
    return rel in (I_INTRO + 6, I_P1 + 1, I_P2 + 1)


# ---------------------------------------------------------------- notas
class N:
    __slots__ = ('trk', 't', 'd', 'p', 'v', 'syl', 'tie')

    def __init__(self, trk, t, d, p, v, syl=None, tie=False):
        self.trk, self.t, self.d, self.p, self.v = trk, t, d, p, v
        self.syl, self.tie = syl, tie


notes = []          # notas con altura
strums = []         # rasgueos: (pista, t, voicing, dirección, velocidad, duración)
perc = []           # percusión: (instrumento, t, velocidad)


def put_line(trk, bar0, bars, vel, transpose=T, syllables=None):
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


def syllables(copla, *lines):
    out = []
    for li in lines:
        for w in copla[li - 1].split():
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


def fill(bar, trk, vel, beat0=1, octave=0):
    """Respuesta en corcheas mientras el cante sostiene una nota larga."""
    ch, sc = chords[bar], scale_at(bar)
    run = [p for p in range(76, 98) if p % 12 in ch.pcs][:3]
    p = run[-1]
    while len(run) < int((3 - beat0) * 2):
        p -= 1
        while p % 12 not in sc:
            p -= 1
        run.append(p)
    out = []
    for i, p in enumerate(run):
        n = N(trk, bar * BAR + beat0 + i * .5, .5, p + octave, vel)
        notes.append(n)
        out.append(n)
    return out


# ---------------------------------------------------------------- guitarras
# Compás de 3/4 (¡UN!-dos-tres): golpe en el 1, el 3 marcado y corcheas seguidas,
# según lo medido en «Las Palmas» (1: 1.00 · y: 0.28 · 2: 0.38 · y: 0.52 · 3: 0.58 · y: 0.42)
PATRON = [(0, 'down', 1.15), (.5, 'up', .58), (1, 'down', .5), (1.5, 'up', .74), (2, 'down', .86), (2.5, 'up', .6)]
# Aire de 6/8: las seis corcheas en dos grupos de tres (¡UN!-y-dos ¡Y!-tres-y). El 1 sigue mandando.
PATRON_68 = [(0, 'down', 1.15), (.5, 'up', .4), (1, 'down', .5), (1.5, 'down', .98), (2, 'up', .45), (2.5, 'down', .55)]


def seis_por_ocho(bar):
    """Compases en que la guitarra se va al 6/8 mientras las palmas siguen en 3/4: el compás
    central de cada verso, el primero de cada pasada y el penúltimo de la introducción."""
    rel = bar % LEN
    for s0, length in ((I_SALIDA, 6), (I_T1, 12), (I_T2, 12), (I_T3, 9)):
        if s0 <= rel < s0 + length:
            return (rel - s0) % 3 == 1
    return rel in (I_INTRO + 5, I_P1, I_P2)


def rasgueo(trk, bar, vel, high=False, lag=0.0):
    """Compás de sevillana. Dos guitarras lo tocan a la vez, la segunda en acordes agudos
    y un pelo detrás, como dos guitarristas de verdad."""
    ch, t0 = chords[bar], bar * BAR + lag
    v = ch.high if high else ch.voicing
    first = bar % LEN == I_INTRO                  # el primer tiempo de la introducción calla
    shape = 1 + .06 * math.sin(2 * math.pi * (bar % 6) / 6)     # el pulso respira un poco
    for off, direction, f in (PATRON_68 if seis_por_ocho(bar) else PATRON):
        if first and off == 0:
            continue
        if off == 0 and bar % 2 == 0 and not high:   # abanico rápido que acaba EN el 1
            for k, pre in enumerate((-.18, -.12, -.06)):
                strums.append((trk, t0 + pre, v, 'down' if k != 1 else 'up', vel * (.4 + .08 * k), .06))
        if line_end(bar) and off == 2.5:         # remate al final del verso: el 3 seco, sin el «y»
            continue
        f *= random.uniform(.9, 1.06) * shape
        strums.append((trk, t0 + off, v, direction, vel * f, .5 if not (line_end(bar) and off == 2) else .4))


def acompanamiento_suave(bar, vel):
    """Durante la salida la guitarra casi calla: un acorde en el 1 y otro en el 3."""
    v, t0 = chords[bar].voicing, bar * BAR
    strums.append(('gtr1', t0, v, 'down', vel, 2))
    strums.append(('gtr1', t0 + 2, v, 'down', vel * .7, 1))


# ---------------------------------------------------------------- percusión rociera
def palmas(bar, vel=1.0):
    t0 = bar * BAR
    for b, v in ((0, 116), (1, 32), (2, 46)):
        if not (bar % LEN == I_INTRO and b == 0):
            perc.append(('palma', t0 + b, v * vel))
            perc.append(('palma2', t0 + b + .012, v * vel * .8))   # un segundo palmero, algo detrás


def castanuelas(bar, vel=1.0):
    t0 = bar * BAR
    if bar % LEN != I_INTRO:
        for k, off in enumerate((-.24, -.18, -.12, -.06)):        # carretilla que llega al 1
            perc.append(('casta', t0 + off, (54 + 8 * k) * vel))
        perc.append(('casta', t0, 104 * vel))
    if seis_por_ocho(bar):
        perc.extend([('casta', t0 + 1.5, 80 * vel), ('casta', t0 + 2.5, 50 * vel)])
    else:
        perc.extend([('casta', t0 + 1.5, 50 * vel), ('casta', t0 + 2, 58 * vel)])


def golpe(bar, vel=1.0):
    """Golpe flamenco con el anular en la tapa de la guitarra, con el rasgueo del 1
    (y en el «y» del 2 cuando el compás va a 6/8)."""
    t0 = bar * BAR
    if bar % LEN != I_INTRO:
        perc.append(('golpe', t0, 92 * vel))
    if seis_por_ocho(bar):
        perc.append(('golpe', t0 + 1.5, 70 * vel))


def tamboril(bar, vel=1.0):
    """Tamboril rociero: golpe con la maza en el 1, redoble corto hacia el 3."""
    t0 = bar * BAR
    if bar % LEN != I_INTRO:
        perc.append(('tamboril', t0, 100 * vel))
        perc.append(('tamboril_bombo', t0, 90 * vel))
    perc.extend([('tamboril', t0 + 1.5, 38 * vel), ('tamboril', t0 + 1.75, 46 * vel),
                 ('tamboril', t0 + 2, 40 * vel), ('tamboril', t0 + 2.5, 42 * vel)])


def pandereta(bar, vel=1.0):
    """Pandereta: sacude en las corcheas, con el golpe en el 1 y el acento del rasgueo."""
    t0 = bar * BAR
    for off, v in ((0, 108), (.5, 32), (1, 30), (1.5, 46), (2, 40), (2.5, 34)):
        if not (bar % LEN == I_INTRO and off == 0):
            perc.append(('pandereta', t0 + off, v * vel))


# ---------------------------------------------------------------- una sevillana completa
def doblar(src, trk, vel, octave):
    """Un instrumento rociero dobla el cante nota a nota (con melismas y ligaduras)."""
    out = []
    for n in src:
        c = N(trk, n.t, n.d, n.p + octave, vel * random.uniform(.94, 1.04), None, n.tie)
        notes.append(c)
        out.append(c)
    return out


def sevillana(k):
    """k = 0..3. La música es la misma; el arreglo crece de una a otra."""
    s0 = k * LEN
    c = COPLAS[k]

    # cante: salida (1-2) · tercio 1 (1-2-3-4) · tercio 2 (3-4-3-4) · tercio 3 (estribillo 5-6-7)
    sal = put_line('voz', s0 + I_SALIDA, SALIDA, 90, syllables=syllables(c, 1, 2))
    t1 = put_line('voz', s0 + I_T1, TERCIO_A, 92, syllables=syllables(c, 1, 2, 3, 4))
    t2 = put_line('voz', s0 + I_T2, TERCIO_B, 96, syllables=syllables(c, 3, 4, 3, 4))
    t3 = put_line('voz', s0 + I_T3, TERCIO_C, 100, syllables=syllables(c, 5, 6, 7))
    last = N('voz', (s0 + I_PARADA) * BAR, 1, midi('E5'), 100, tie=True)  # la última sílaba llega a la parada
    notes.append(last)
    harmonize(t1 + t2 + t3 + [last] if k >= 1 else t3 + [last], 'voz2', 14)

    # la gaita rociera lleva la melodía de principio a fin, una octava por encima del cante;
    # la mandolina (como una bandurria) la dobla en trémolo desde la segunda sevillana
    doblar(sal + t1 + t2 + t3 + [last], 'gaita', 78 + 3 * k, 12)
    if k >= 1:
        doblar((t2 + t3 + [last]) if k < 3 else (t1 + t2 + t3 + [last]), 'mandolina', 70 + 3 * k, 0)

    # introducción: gaita y guitarra 2 con el tema; mandolina desde la segunda
    put_line('gtr2', s0, FALSETA, 90, transpose=0)
    if k in (0, 3):
        put_line('gaita', s0 + 4, FALSETA[4:], 82, transpose=12)
    if k >= 1:
        put_line('mandolina', s0 + 4, FALSETA[4:], 74, transpose=0)

    # pasadas: gaita y mandolina; las trompetas solo en la tercera y la cuarta
    for p in (s0 + I_P1, s0 + I_P2):
        put_line('gaita', p, PASADA_GAITA, 86, transpose=0)
        put_line('mandolina', p, FANFARRIA, 76, transpose=0)
        if k >= 2:
            harmonize(put_line('trompeta1', p, FANFARRIA, 80 + 4 * k, transpose=0), 'trompeta2', 8)

    # punteos de la guitarra 2 cuando el cante sostiene una nota larga
    for rel in (I_T1 + 4, I_T1 + 10, I_T2 + 4, I_T2 + 10, I_SALIDA + 4, I_T3 + 1, I_T3 + 7):
        fill(s0 + rel, 'gtr2', 82, octave=-12)

    # contrabajo, discreto
    for bar in range(s0, s0 + I_PARADA + 1):
        root = nearest([chords[bar].bass], 40, 51, 45)
        if bar == s0 + I_PARADA:
            notes.append(N('bajo', bar * BAR, 1, root, 104))
        elif part_of(bar) == 'Salida':
            notes.append(N('bajo', bar * BAR, 2.5, root, 64))
        else:
            start = 1 if bar == s0 else 0
            notes.append(N('bajo', bar * BAR + start, 2.6 - start, root, 84))   # solo en el 1

    # guitarras: las dos rasguean el compás; la 2 se calla cuando puntea
    filled = {int(n.t // BAR) for n in notes if n.trk == 'gtr2'}
    for bar in range(s0, s0 + I_PARADA):
        part = part_of(bar)
        if part == 'Salida':
            acompanamiento_suave(bar, 70)
            continue
        vel = 104 if part == 'Pasada' else 96 if part == 'Introducción' else 90 + 3 * k
        rasgueo('gtr1', bar, vel)
        if bar not in filled:
            rasgueo('gtr2', bar, vel * .72, high=True, lag=.03)

    # percusión: palmas, tamboril y pandereta en todo el compás; castañuelas que van creciendo
    for bar in range(s0, s0 + I_PARADA):
        part = part_of(bar)
        if part == 'Salida':
            continue
        palmas(bar, .85 if part == 'Primer tercio' and k == 0 else 1.0)
        golpe(bar, .8 if part.endswith('tercio') else 1.0)
        tamboril(bar, 1.0 if part in ('Introducción', 'Pasada') else .75)
        if k >= 1 or part in ('Pasada', 'Tercer tercio'):
            pandereta(bar, .9 if part.endswith('tercio') else 1.0)
        if part in ('Introducción', 'Pasada') or (part == 'Tercer tercio' and k >= 1) or line_end(bar):
            castanuelas(bar, .85 if part.endswith('tercio') and k < 2 else 1.0)

    # parada: todos a la vez en el primer tiempo
    ft = (s0 + I_PARADA) * BAR
    strums.append(('gtr1', ft, chords[s0 + I_PARADA].voicing, 'down', 124, 1))
    strums.append(('gtr2', ft, chords[s0 + I_PARADA].high, 'down', 116, 1))
    if k >= 2:
        notes.extend(N('trompeta1', ft, 1, p, 100 + 2 * k) for p in (68, 71, 76))
    notes.append(N('mandolina', ft, 1, midi('E5'), 96))
    perc.extend([('palma', ft, 124), ('palma2', ft + .01, 110), ('casta', ft, 124), ('tamboril', ft, 120),
                 ('tamboril_bombo', ft, 110), ('pandereta', ft, 116)])
    for i, off in enumerate((-.24, -.18, -.12, -.06)):
        perc.append(('casta', ft + off, 60 + 10 * i))


for k in range(N_SEV):
    sevillana(k)

TOTAL_BEATS = N_BARS * BAR

# ================================================================ MIDI
TPB = 480
# pista: (clave, nombre, canal, banco, programa, volumen, panorama 0-127, reverb)
INSTRUMENTS = [
    ('voz', 'Voz (coro)', 0, 0, 52, 80, 64, 60),
    ('voz2', 'Segunda voz', 1, 0, 53, 64, 70, 60),
    ('gaita', 'Gaita rociera', 2, 0, 72, 84, 76, 50),
    ('gtr1', 'Guitarra flamenca 1', 3, 0, 24, 127, 40, 28),
    ('gtr2', 'Guitarra flamenca 2', 4, 0, 24, 112, 90, 32),
    ('mandolina', 'Mandolina (bandurria)', 5, 16, 25, 88, 100, 40),
    ('bajo', 'Contrabajo', 7, 0, 32, 80, 64, 16),
    ('trompeta', 'Trompetas', 8, 0, 56, 80, 80, 56),
]
DRUMS = {'palma': (39, 1.0), 'palma2': (39, .9), 'casta': (85, 1.0), 'tamboril': (38, .62), 'golpe': (37, .55),
         'tamboril_bombo': (41, .6), 'pandereta': (54, .8)}
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
            (0, 0, b'\xff\x59\x02\x04\x00')]
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
        sd = 4 if key in ('gtr1', 'gtr2', 'bajo') else 6
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
    ev = [(0, 0, bytes([0xB9, 7, 92])), (0, 0, bytes([0xB9, 91, 38]))]
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
                xml.append(f'<attributes><divisions>{DIV}</divisions><key><fifths>4</fifths></key>'
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
