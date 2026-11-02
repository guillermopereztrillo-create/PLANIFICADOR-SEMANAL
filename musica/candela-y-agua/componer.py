#!/usr/bin/env python3
"""«Candela y agua» — sevillana original.

Genera, desde una única descripción de la obra:
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

BPM = 190
BAR = 3                   # 3/4
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
    'D': [50, 57, 62, 66], 'E/D': [50, 59, 64, 68], 'G': [43, 47, 50, 55, 59, 67],
    'A': [45, 52, 57, 61, 64], 'A7': [45, 52, 55, 61, 64], 'Bm': [47, 54, 59, 62, 66],
    'C': [48, 52, 55, 60, 64], 'F#m': [42, 49, 54, 57, 61, 66], 'B7': [47, 51, 57, 59, 66],
    'Em': [40, 47, 52, 55, 59, 64], 'Em7': [40, 47, 50, 55, 59, 64],
    'Bb': [46, 53, 58, 62, 65], 'E': [40, 47, 52, 56, 59, 64],
}
QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10]}


class Chord:
    def __init__(self, name, t=0):
        base, bass = (name.split('/') + [None])[:2]
        root = base[:2] if len(base) > 1 and base[1] in '#b' else base[:1]
        self.q = base[len(root):]
        self.root = (PC[root] + t) % 12
        self.bass = (PC[bass] + t) % 12 if bass else self.root
        self.pcs = [(self.root + i) % 12 for i in QUAL[self.q]]
        self.voicing = [v + t for v in VOICING[name]]
        self.name = SPELL[self.root] + self.q + ('/' + SPELL[self.bass] if bass else '')


# ---------------------------------------------------------------- la obra
# Melodía de la copla (en Re). Cada compás: (duración en negras, nota).
#   'r' silencio · '-X' ligadura (misma sílaba) · '~X' melisma (nueva nota, misma sílaba)
COPLA_CHORDS = ['D', 'D', 'G', 'A7', 'D', 'A',
                'F#m', 'B7', 'Em', 'C', 'A7', 'D',
                'G', 'Bb', 'C', 'D', 'Em', 'A7', 'D', 'D',
                'Bb', 'C', 'A7', 'Em7', 'A7', 'D']
COPLA_MELODY = [
    # A · versos 1-2
    [(1, 'r'), (1, 'A4'), (1, 'D5')],
    [(1, 'F#5'), (1, 'E5'), (1, 'D5')],
    [(1, 'G5'), (.5, '~A5'), (.5, '~G5'), (1, 'F#5')],
    [(1, 'r'), (.5, 'E5'), (.5, 'F#5'), (1, 'G5')],
    [(2, 'F#5'), (1, 'E5')],
    [(3, '-E5')],
    # B · versos 3-4
    [(1, 'r'), (1, 'C#5'), (1, 'E5')],
    [(1, 'F#5'), (1, 'A5'), (1, 'F#5')],
    [(2, 'G5'), (1, 'E5')],
    [(1, 'r'), (.5, 'E5'), (.5, 'D5'), (1, 'E5')],
    [(2, 'G5'), (1, 'F#5')],
    [(3, '-F#5')],
    # C · estribillo (versos 5-6-7)
    [(1, 'r'), (.5, 'B4'), (.5, 'D5'), (1, 'G5')],
    [(1, 'F5'), (.5, '~G5'), (.5, '~F5'), (1, 'D5')],
    [(1, 'r'), (1, 'E5'), (1, 'G5')],
    [(1, 'A5'), (1, 'F#5'), (1, 'D5')],
    [(1, 'G5'), (.5, '~A5'), (.5, '~G5'), (1, 'E5')],
    [(1, 'r'), (.5, 'C#5'), (.5, 'E5'), (1, 'G5')],
    [(2, 'F#5'), (1, 'D5')],
    [(3, '-D5')],
    # C' · se repiten los versos 6-7, más arriba
    [(1, 'r'), (1, 'D5'), (1, 'F5')],
    [(1, 'G5'), (1, 'E5'), (1, 'G5')],
    [(1, 'A5'), (.5, '~B5'), (.5, '~A5'), (1, 'G5')],
    [(1, 'r'), (.5, 'E5'), (.5, 'F#5'), (1, 'G5')],
    [(2, 'E5'), (1, 'D5')],
    [(3, '-D5')],
]
HOLD_BARS = [5, 11, 19, 25]          # compases donde la voz sostiene y entra un relleno
ESTRIBILLO_FROM = 12
REPETICION_FROM = 20

LETRA = [  # seguidillas: 7-5-7-5 / 5-7-5   («‿» = sinalefa)
    ["A-gua de ma-dru-ga-da", "so-bre la bra-sa,", "lo que‿el fue-go le-van-ta",
     "el a-gua‿en cal-ma.", "Si-re-na‿y a-gua,", "que‿en-tre‿el hu-mo‿y la no-che",
     "des-pun-ta‿el al-ba."],
    ["Ten-go‿un cas-co de pla-ta", "y‿u-na‿es-ca-le-ra", "pa-ra su-bir al cie-lo",
     "cuan-do tú quie-ras.", "Que no‿hay can-de-la", "que me que-me por den-tro",
     "co-mo tu‿au-sen-cia."],
    ["Se-vi-lla tie-ne‿un rí-o", "que no se‿a-pa-ga,", "y‿un fue-go‿en ca-da pa-tio",
     "que‿el a-gua guar-da.", "Can-de-la‿y a-gua,", "mi Se-vi-lla‿es un can-te",
     "que nun-ca‿a-ca-ba."],
]
ORDEN = [0, 1, 2, 3, 4, 5, 6, 5, 6]   # el estribillo repite sus dos últimos versos

LLAMADA = [  # gaita rociera sola con el tamboril, antes de que entren las guitarras
    [(.5, 'A5'), (.5, 'B5'), (.5, 'A5'), (.5, 'G5'), (1, 'F#5')],
    [(.5, 'E5'), (.5, 'F#5'), (.5, 'G5'), (.5, 'A5'), (1, 'E5')],
    [(.5, 'F#5'), (.5, 'A5'), (1, 'D6'), (.5, 'C#6'), (.5, 'B5')],
    [(2, 'A5'), (1, 'r')],
]
LLAMADA_CHORDS = ['D', 'A7', 'D', 'A7']

TEMA = [  # tema instrumental, sobre D E/D D E/D Bm C A A7
    [(1.5, 'F#5'), (.5, 'E5'), (1, 'D5')],
    [(2, 'G#5'), (.5, 'F#5'), (.5, 'E5')],
    [(1, 'A5'), (1, 'F#5'), (1, 'D5')],
    [(2, 'E5'), (1, 'B4')],
    [(1, 'D5'), (1, 'F#5'), (1, 'B5')],
    [(1.5, 'G5'), (.5, 'E5'), (1, 'C5')],
    [(1, 'C#5'), (1, 'E5'), (1, 'A5')],
    [(2, 'G5'), (1, 'E5')],
]
TEMA_CHORDS = ['D', 'E/D', 'D', 'E/D', 'Bm', 'C', 'A', 'A7']
TEMA_A_MI = [(1, 'A5'), (1, 'F#5'), (1, 'D#5')]   # último compás de la 2.ª pasada (sobre B7)

SALIDA = [[(3, 'A4')], [(.5, '~B4'), (.5, '~A4'), (2, '~D5')],
          [(1, '~E5'), (1, '~F#5'), (1, '~E5')], [(2, '~C#5'), (1, 'r')]]

REMATE = [[(.5, 'G4'), (.5, 'C5'), (1, 'E5'), (.5, 'D5'), (.5, 'C5')],
          [(.5, 'B4'), (.5, 'A4'), (.5, 'F#4'), (.5, 'D#4'), (.5, 'F#4'), (.5, 'A4')],
          [(1, 'B4')]]

# Forma (compases)
S_GAITA, S_INTRO, S_SALIDA, S_C1, S_P1, S_C2, S_P2, S_C3, S_CODA, N_BARS = 0, 4, 16, 20, 46, 54, 80, 88, 114, 117
SECTIONS = [(S_GAITA, 'Llamada de gaita'), (S_INTRO, 'Introducción'), (S_SALIDA, 'Salida'),
            (S_C1, 'Copla 1'), (S_P1, 'Pasada'), (S_C2, 'Copla 2'), (S_P2, 'Pasada (modula a Mi)'),
            (S_C3, 'Copla 3'), (S_CODA, 'Remate')]
COPLAS = ((S_C1, 0), (S_C2, 0), (S_C3, 2))

chords = [None] * N_BARS
for i, c in enumerate(LLAMADA_CHORDS):
    chords[S_GAITA + i] = Chord(c)
for i, c in enumerate(['D', 'E/D', 'D', 'E/D'] + TEMA_CHORDS):
    chords[S_INTRO + i] = Chord(c)
for i, c in enumerate(['D', 'D', 'A7', 'A7']):
    chords[S_SALIDA + i] = Chord(c)
for start, t in COPLAS:
    for i, c in enumerate(COPLA_CHORDS):
        chords[start + i] = Chord(c, t)
for i, c in enumerate(TEMA_CHORDS):
    chords[S_P1 + i] = Chord(c)
    chords[S_P2 + i] = Chord(c if i < 7 else 'B7')
for i, c in enumerate(['C', 'B7', 'E']):
    chords[S_CODA + i] = Chord(c)


def key_at(bar):
    return 4 if bar >= S_C3 else 2     # tónica: Re o Mi


def scale_at(bar):
    k = key_at(bar)
    pcs = [(k + i) % 12 for i in (0, 2, 4, 5, 7, 9, 11)]
    for cp in chords[bar].pcs:         # el acorde manda (Fa natural en Sib, Re# en Si7...)
        pcs = [cp if (p - cp) % 12 in (1, 11) else p for p in pcs]
    return sorted(set(pcs))


def copla_rel(bar):
    """Compás dentro de la copla (0-25), o None fuera de las coplas."""
    for start, _ in COPLAS:
        if start <= bar < start + 26:
            return bar - start
    return None


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
    return out


def syllabify(line):
    out = []
    for w in line.split():
        parts = w.split('-')
        for i, p in enumerate(parts):
            kind = 'single' if len(parts) == 1 else 'begin' if i == 0 else 'end' if i == len(parts) - 1 else 'middle'
            out.append((p, kind))
    return out


def nearest(pcs, lo, hi, target):
    cands = [p for p in range(lo, hi + 1) if p % 12 in pcs]
    return min(cands, key=lambda p: (abs(p - target), p))


def third_below(p, bar):
    ch = chords[bar]
    cands = [q for q in range(p - 5, p - 2) if q % 12 in ch.pcs]
    if not cands:
        cands = [q for q in range(p - 5, p - 1) if q % 12 in scale_at(bar)] or [p - 4]
    return min(cands, key=lambda q: abs(p - 4 - q))


def harmonize(src, trk, vel_drop, lo=None, hi=None):
    for n in src:
        notes.append(N(trk, n.t, n.d, third_below(n.p, int(n.t // BAR)), n.v - vel_drop, n.syl, n.tie))


# --- voz principal y segunda voz (coro)
voice_notes = put_line('voz', S_SALIDA, SALIDA, 92, syllables=[('¡Ay!', 'single')])
for ci, (start, t) in enumerate(COPLAS):
    sy = [s for li in ORDEN for s in syllabify(LETRA[ci][li])]
    voice_notes += put_line('voz', start, COPLA_MELODY, 88 + 4 * ci, transpose=t, syllables=sy)
harmonize([n for n in voice_notes if (S_C2 + ESTRIBILLO_FROM) * BAR <= n.t < (S_C2 + 26) * BAR
           or S_C3 * BAR <= n.t < (S_C3 + 26) * BAR], 'voz2', 14)

# --- gaita rociera (flauta de tres agujeros, suena muy aguda) y trompetas
put_line('gaita', S_GAITA, LLAMADA, 92, transpose=12)
put_line('gaita', S_INTRO + 4, TEMA, 80, transpose=12)
put_line('mandolina', S_INTRO + 8, TEMA[4:], 72)
tp = put_line('trompeta1', S_P1, TEMA, 88)
harmonize(tp, 'trompeta2', 8)
put_line('mandolina', S_P1, TEMA, 74)
pasada2 = TEMA[:7] + [TEMA_A_MI]
put_line('gaita', S_P2, pasada2, 88, transpose=12)
tp = put_line('trompeta1', S_P2, pasada2, 96)
harmonize(tp, 'trompeta2', 8)
put_line('mandolina', S_P2, pasada2, 80)
# las trompetas doblan a la voz en la repetición final del estribillo de la copla 3
tp = [N('trompeta1', n.t, n.d, n.p - 12, 78, None, n.tie) for n in voice_notes
      if (S_C3 + REPETICION_FROM) * BAR <= n.t < (S_C3 + 26) * BAR]
notes.extend(tp)
harmonize(tp, 'trompeta2', 8)


def fill(bar, trk, vel, octave=0):
    """Relleno de corcheas mientras la voz sostiene: arpegio que sube y escala que baja."""
    ch, sc = chords[bar], scale_at(bar)
    run = [p for p in range(74, 96) if p % 12 in ch.pcs][:4]
    p = run[-1]
    for _ in range(2):
        p -= 1
        while p % 12 not in sc:
            p -= 1
        run.append(p)
    out = []
    for i, p in enumerate(run):
        n = N(trk, bar * BAR + i * .5, .5 if i < 5 else 1, p + octave, vel + (6 if i == 3 else 0))
        notes.append(n)
        out.append(n)
    return out


for hb in HOLD_BARS:
    fill(S_C1 + hb, 'gtr2', 84, -12)
    fill(S_C2 + hb, 'gaita', 78)
    harmonize(fill(S_C3 + hb, 'trompeta1', 90, -12), 'trompeta2', 8)
    fill(S_C3 + hb, 'mandolina', 70, -12)

# remate: trompetas y mandolina, gaita una octava arriba
tp = put_line('trompeta1', S_CODA, REMATE, 100, transpose=12)
harmonize(tp, 'trompeta2', 6)
put_line('mandolina', S_CODA, REMATE, 84)
put_line('gaita', S_CODA, REMATE[:2] + [[(1, 'E5')]], 86, transpose=24)

# cuerdas: notas largas en el estribillo de la copla 2 y en toda la copla 3
prev = 81
for start, frm, vel in ((S_C2, ESTRIBILLO_FROM, 56), (S_C3, 0, 64)):
    for b in range(frm, 26):
        if b in HOLD_BARS:
            continue
        bar = start + b
        prev = nearest(chords[bar].pcs, 72, 84, prev)
        notes.append(N('cuerdas', bar * BAR, 3, prev, vel))
        notes.append(N('cuerdas', bar * BAR, 3, third_below(prev, bar), vel - 8))

# violonchelo: contracanto grave
prev = 50
for bar in range(S_INTRO + 4, S_CODA + 2):
    ch = chords[bar]
    vel = 56 if S_C1 <= bar < S_P1 else 64
    prev = nearest(ch.pcs, 43, 62, prev)
    if copla_rel(bar) in HOLD_BARS:
        notes.append(N('chelo', bar * BAR, 2, prev, vel))
        nxt = nearest(chords[bar + 1].pcs, 43, 62, prev)
        step = prev + (1 if nxt > prev else -1) * (2 if abs(nxt - prev) > 2 else 1)
        notes.append(N('chelo', bar * BAR + 2, 1, step, vel - 6))
    else:
        notes.append(N('chelo', bar * BAR, 3, prev, vel))

# contrabajo
for bar in range(S_INTRO + 4, S_CODA + 3):
    ch = chords[bar]
    root = nearest([ch.bass], 38, 50, 44)
    if bar == S_CODA + 2:
        notes.append(N('bajo', bar * BAR, 1, root, 110))
        break
    fifth = root + 7 if root + 7 <= 52 else root - 5
    notes.append(N('bajo', bar * BAR, 1.8, root, 96))
    notes.append(N('bajo', bar * BAR + 2, .9, fifth, 76))

# guitarra 2: arpegio de la introducción
for bar in range(S_INTRO, S_INTRO + 4):
    v = chords[bar].voicing
    for i, idx in enumerate([0, 1, 2, 3, 2, 1]):
        notes.append(N('gtr2', bar * BAR + i * .5, 1.5, v[idx], 66 + 5 * (bar - S_INTRO)))


def phrase_end(bar):
    return copla_rel(bar) in HOLD_BARS or bar in (S_INTRO + 11, S_SALIDA + 3, S_P1 + 7, S_P2 + 7)


def rasgueo(bar, vel):
    """Guitarra 1: floreo de cuatro dedos al empezar el compás y golpes en 2 y 3."""
    v, t0 = chords[bar].voicing, bar * BAR
    if bar % 2 == 0 or phrase_end(bar):
        for k in range(4):
            strums.append(('gtr1', t0 + k * .09, v, 'down', vel * (0.6 + 0.1 * k), .1 if k < 3 else .9))
    else:
        strums.append(('gtr1', t0, v, 'down', vel, 1))
    strums.append(('gtr1', t0 + 1, v, 'down', vel * .8, 1))
    strums.append(('gtr1', t0 + 2, v, 'up', vel * .66, .5))
    strums.append(('gtr1', t0 + 2.5, v, 'down', vel * .55, .5))


def contestacion(bar, vel):
    """Guitarra 2 (coplas 2 y 3): acorde en las cuerdas agudas, a contratiempo."""
    v = chords[bar].voicing[-3:]
    v = [p + 12 for p in v] if v[-1] < 70 else v
    t0 = bar * BAR
    strums.append(('gtr2', t0 + 1, v, 'down', vel, .5))
    strums.append(('gtr2', t0 + 1.5, v, 'up', vel * .7, .5))
    strums.append(('gtr2', t0 + 2, v, 'down', vel * .9, 1))


for bar in range(S_INTRO + 4, S_CODA + 2):
    base = 80 if bar < S_INTRO + 8 else 92 if bar < S_C1 else 84 if bar < S_P1 else 94
    rasgueo(bar, base)
    if bar >= S_C2 and copla_rel(bar) not in HOLD_BARS:
        contestacion(bar, 66 if bar < S_C3 else 74)
final_t = (S_CODA + 2) * BAR
strums.append(('gtr1', final_t, chords[S_CODA + 2].voicing, 'down', 120, 1.2))
strums.append(('gtr2', final_t, [p + 12 for p in chords[S_CODA + 2].voicing[-3:]], 'down', 110, 1.2))
notes.extend(N('trompeta1', final_t, 1.2, p, 108) for p in (71, 76))  # acorde final de las trompetas
notes.append(N('gaita', final_t, 1, 88, 96))


# --- percusión
def palmas(bar, kind, contra=False):
    t0 = bar * BAR
    for b in range(3):
        perc.append(('palma_' + kind, t0 + b, 104 if b == 0 else 84))
        if contra:
            perc.append(('palma_contra', t0 + b + .5, 72))


def cajon(bar, end):
    t0 = bar * BAR
    if end:
        hits = ((0, 'cajon_grave', 104), (1, 'cajon_agudo', 84), (1.5, 'cajon_agudo', 74),
                (2, 'cajon_agudo', 94), (2.5, 'cajon_agudo', 100))
        perc.extend((k, t0 + t, v) for t, k, v in hits)
    else:
        perc.extend([('cajon_grave', t0, 100), ('cajon_agudo', t0 + 1.5, 50), ('cajon_agudo', t0 + 2, 90)])


def castanuelas(bar):
    t0 = bar * BAR
    for k in range(4):                 # «ria»: carretilla de cuatro dedos
        perc.append(('casta', t0 + k * .09, 60 + 10 * k))
    perc.extend([('casta', t0 + 1, 80), ('casta', t0 + 2, 100)])


def tamboril(bar, end=False):
    t0 = bar * BAR
    perc.extend([('tamboril', t0, 100), ('tamboril', t0 + 1, 70), ('tamboril', t0 + 2, 84),
                 ('tamboril', t0 + 2.5, 64)])
    if end:
        perc.extend(('tamboril', t0 + 1 + k * .25, 50 + 8 * k) for k in range(4))


for bar in range(S_GAITA, S_INTRO):
    tamboril(bar, end=bar == S_INTRO - 1)
for bar in range(S_INTRO + 4, S_CODA + 2):
    rel = copla_rel(bar)
    end = rel in HOLD_BARS or bar in (S_P1 + 7, S_P2 + 7, S_CODA + 1)
    if bar < S_INTRO + 8 or S_C1 <= bar < S_P1:
        palmas(bar, 'sorda')
    else:
        palmas(bar, 'clara', contra=bar >= S_C3)
    if bar >= S_P1:
        cajon(bar, end)
    if S_P1 <= bar < S_C2 or S_P2 <= bar < S_C3 or bar >= S_CODA:
        tamboril(bar, end)
    if (S_INTRO + 8 <= bar < S_C1) or (S_P1 <= bar < S_C2) or (S_P2 <= bar < S_C3) or bar >= S_CODA \
            or (rel is not None and bar >= S_C2 and (end or rel >= ESTRIBILLO_FROM)):
        castanuelas(bar)
perc += [('palma_clara', final_t, 124), ('palma_contra', final_t, 112), ('casta', final_t, 124),
         ('cajon_grave', final_t, 124), ('tamboril', final_t, 120)]

TOTAL_BEATS = N_BARS * BAR

# ================================================================ MIDI
TPB = 480
# pista: (nombre, canal, banco, programa, volumen, panorama 0-127, reverb)
INSTRUMENTS = [
    ('voz', 'Voz (coro)', 0, 0, 52, 100, 64, 70),
    ('voz2', 'Segunda voz', 1, 0, 53, 82, 74, 70),
    ('gaita', 'Gaita rociera', 2, 0, 72, 78, 84, 60),
    ('gtr1', 'Guitarra flamenca 1', 3, 0, 24, 118, 44, 40),
    ('gtr2', 'Guitarra flamenca 2', 4, 0, 24, 100, 86, 40),
    ('mandolina', 'Mandolina', 5, 16, 25, 72, 100, 50),
    ('chelo', 'Violonchelo', 6, 0, 42, 64, 36, 70),
    ('bajo', 'Contrabajo', 7, 0, 32, 100, 64, 20),
    ('trompeta', 'Trompetas', 8, 0, 56, 92, 76, 64),
    ('cuerdas', 'Cuerdas', 10, 0, 49, 58, 54, 80),
]
# percusión en el canal 10 (kit estándar): (nota GM, ajuste de velocidad, desplazamiento)
DRUMS = {'palma_clara': (39, 1.0), 'palma_contra': (39, .85), 'palma_sorda': (39, .55),
         'casta': (85, 1.0), 'cajon_grave': (36, .8), 'cajon_agudo': (37, 1.0), 'tamboril': (38, .8)}


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
    return int(max(-2.5 * sd_ticks, min(2.5 * sd_ticks, random.gauss(0, sd_ticks))))


def write_midi(path):
    tempo = int(60_000_000 / BPM)
    meta = [(0, 0, b'\xff\x51\x03' + tempo.to_bytes(3, 'big')), (0, 0, b'\xff\x58\x04\x03\x02\x18\x08'),
            (0, 0, b'\xff\x59\x02\x02\x00'), (tk(S_C3 * BAR), 2, b'\xff\x59\x02\x04\x00')]
    for bar, name in SECTIONS:
        txt = name.encode('utf-8')
        meta.append((tk(bar * BAR), 1, b'\xff\x06' + vlq(len(txt)) + txt))
    tracks = [midi_track(meta, 'Candela y agua')]
    for key, name, ch, bank, prog, vol, pan, rev in INSTRUMENTS:
        ev = [(0, 0, bytes([0xB0 | ch, 0, bank])), (0, 0, bytes([0xB0 | ch, 32, 0])),
              (0, 0, bytes([0xC0 | ch, prog])), (0, 0, bytes([0xB0 | ch, 7, vol])),
              (0, 0, bytes([0xB0 | ch, 10, pan])), (0, 0, bytes([0xB0 | ch, 91, rev])),
              (0, 0, bytes([0xB0 | ch, 93, 20]))]
        src = [n for n in notes if n.trk == key or n.trk.startswith(key) and key == 'trompeta']
        for trk, t, v, direction, vel, d in strums:
            if trk == key:
                order = v if direction == 'down' else list(reversed(v))
                spread = .035 if direction == 'down' else .025
                for i, p in enumerate(order):
                    src.append(N(key, t + i * spread, d - i * spread * .5, p, int(min(127, vel * random.uniform(.9, 1.05)))))
        merged = []                                   # une notas ligadas
        for n in sorted(src, key=lambda n: (n.t, n.p)):
            prevs = [m for m in merged[-4:] if m.p == n.p and abs(m.t + m.d - n.t) < 1e-6]
            if n.tie and prevs:
                prevs[-1].d += n.d
                continue
            merged.append(N(n.trk, n.t, n.d, n.p, n.v, n.syl))
        legato = key in ('voz', 'voz2', 'gaita', 'trompeta', 'cuerdas', 'chelo')
        sd = 4 if key in ('gtr1', 'gtr2', 'bajo') else 7
        for n in merged:
            on = tk(n.t) + jitter(sd)
            off = tk(n.t + n.d) - (5 if legato else 30)
            v = int(max(1, min(127, n.v * random.uniform(.93, 1.05))))
            ev.append((max(0, on), 2, bytes([0x90 | ch, n.p, v])))
            ev.append((max(on + 20, off), 0, bytes([0x80 | ch, n.p, 0])))
            if n.syl and key == 'voz':
                txt = (n.syl[0] + ('-' if n.syl[1] in ('begin', 'middle') else ' ')).encode('utf-8')
                ev.append((max(0, on), 1, b'\xff\x05' + vlq(len(txt)) + txt))
        tracks.append(midi_track(ev, name))
    ev = [(0, 0, bytes([0xB9, 7, 110])), (0, 0, bytes([0xB9, 91, 45]))]
    for k, t, v in perc:
        note, scale = DRUMS[k]
        on = tk(t) + jitter(5)
        vel = int(max(1, min(127, v * scale * random.uniform(.9, 1.06))))
        ev.append((max(0, on), 2, bytes([0x99, note, vel])))
        ev.append((max(0, on) + 90, 0, bytes([0x89, note, 0])))
    tracks.append(midi_track(ev, 'Palmas, cajón, tamboril y castañuelas'))
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

    def part_xml(pid, src, lead, octave_shift=0):
        events = sorted(src, key=lambda n: n.t)
        measures, ei, carry = [], 0, []
        for bar in range(N_BARS):
            m0, m1 = bar * BAR * DIV, (bar + 1) * BAR * DIV
            xml = [f'<measure number="{bar + 1}">']
            if bar == 0:
                oc = f'<clef-octave-change>{octave_shift}</clef-octave-change>' if octave_shift else ''
                xml.append(f'<attributes><divisions>{DIV}</divisions><key><fifths>2</fifths></key>'
                           '<time><beats>3</beats><beat-type>4</beat-type></time>'
                           f'<clef><sign>G</sign><line>2</line>{oc}</clef></attributes>')
                if lead:
                    xml.append('<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit>'
                               f'<per-minute>{BPM}</per-minute></metronome></direction-type><sound tempo="{BPM}"/></direction>')
            if bar == S_C3:
                xml.append('<attributes><key><fifths>4</fifths></key></attributes>')
            if lead:
                for sb, name in SECTIONS:
                    if sb == bar:
                        xml.append(f'<direction placement="above"><direction-type><rehearsal>{name}</rehearsal>'
                                   '</direction-type></direction>')
                ch = chords[bar]
                bass = ''
                if ch.bass != ch.root:
                    bn = SPELL[ch.bass]
                    bass = f'<bass><bass-step>{bn[0]}</bass-step>' + \
                           (f'<bass-alter>{1 if bn[1:] == "#" else -1}</bass-alter>' if bn[1:] else '') + '</bass>'
                rn = SPELL[ch.root]
                ralt = f'<root-alter>{1 if rn[1:] == "#" else -1}</root-alter>' if rn[1:] else ''
                xml.append(f'<harmony><root><root-step>{rn[0]}</root-step>{ralt}</root>'
                           f'<kind>{KINDS[ch.q]}</kind>{bass}</harmony>')
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
                    '-o', 'synth.reverb.room-size=0.55', '-o', 'synth.reverb.damp=0.35',
                    '-o', 'synth.reverb.width=0.9', '-o', 'synth.reverb.level=0.6',
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
