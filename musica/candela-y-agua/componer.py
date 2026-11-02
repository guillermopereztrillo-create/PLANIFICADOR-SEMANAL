#!/usr/bin/env python3
"""«Candela y agua» — sevillana original.

Genera, desde una única descripción de la obra:
  - candela-y-agua.mid       (MIDI General MIDI, una pista por instrumento, con letra)
  - candela-y-agua.musicxml  (partitura: voz con letra y cifrado, segunda voz y flauta)
  - candela-y-agua.wav       (grabación sintetizada, sin samples ni librerías externas)

Solo necesita Python 3 y numpy.  Uso:  python3 componer.py [carpeta_salida]
"""
import math
import os
import sys
import wave

import numpy as np

BPM = 190
SR = 44100
SPB = 60.0 / BPM          # segundos por negra
BAR = 3                   # 3/4
rng = np.random.default_rng(1955)

# ---------------------------------------------------------------- utilidades
PC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6,
      'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
SPELL = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def midi(name):
    """'F#5' -> 78"""
    n, o = (name[:2], name[2:]) if len(name) > 2 and name[1] in '#b' else (name[:1], name[1:])
    return 12 * (int(o) + 1) + PC[n]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


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

TEMA = [  # tema instrumental (flauta / bandurria), sobre D E/D D E/D Bm C A A7
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

# Forma (compases):
#  0 intro (12) · 12 salida (4) · 16 copla 1 (26) · 42 pasada (8) · 50 copla 2 (26)
#  76 pasada que modula (8) · 84 copla 3 en Mi (26) · 110 remate (3)
S_INTRO, S_SALIDA, S_C1, S_P1, S_C2, S_P2, S_C3, S_CODA, N_BARS = 0, 12, 16, 42, 50, 76, 84, 110, 113
SECTIONS = [(S_INTRO, 'Introducción'), (S_SALIDA, 'Salida'), (S_C1, 'Copla 1'), (S_P1, 'Pasada'),
            (S_C2, 'Copla 2'), (S_P2, 'Pasada (modula a Mi)'), (S_C3, 'Copla 3'), (S_CODA, 'Remate')]

chords = [None] * N_BARS
for i, c in enumerate(['D', 'E/D', 'D', 'E/D'] + TEMA_CHORDS):
    chords[S_INTRO + i] = Chord(c)
for i, c in enumerate(['D', 'D', 'A7', 'A7']):
    chords[S_SALIDA + i] = Chord(c)
for start, t in ((S_C1, 0), (S_C2, 0), (S_C3, 2)):
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
    ch = chords[bar]
    for cp in ch.pcs:                  # el acorde manda (Fa natural en Sib, Re# en Si7...)
        pcs = [cp if (p - cp) % 12 in (1, 11) else p for p in pcs]
    return sorted(set(pcs))


# ---------------------------------------------------------------- notas
class N:
    __slots__ = ('trk', 't', 'd', 'p', 'v', 'syl', 'vowel', 'tie')

    def __init__(self, trk, t, d, p, v, syl=None, vowel=None, tie=False):
        self.trk, self.t, self.d, self.p, self.v = trk, t, d, p, v
        self.syl, self.vowel, self.tie = syl, vowel, tie


notes = []          # todas las notas con altura (y percusión con nota GM)
strums = []         # rasgueos de guitarra: (t, voicing, dirección, velocidad, duración)


def put_line(trk, bar0, bars, vel, transpose=0, syllables=None, vowels=None):
    """Coloca una línea melódica compás a compás. Devuelve las notas creadas."""
    out, si, t = [], 0, bar0 * BAR
    last_vowel = 'a'
    for bar in bars:
        for d, s in bar:
            if s != 'r':
                kind = s[0] if s[0] in '-~' else ''
                p = midi(s.lstrip('-~')) + transpose
                syl = None
                if kind == '' and syllables is not None:
                    syl = syllables[si]
                    last_vowel = vowels[si]
                    si += 1
                n = N(trk, t, d, p, vel, syl, last_vowel, tie=(kind == '-'))
                notes.append(n)
                out.append(n)
            t += d
    return out


def syllabify(line):
    """'lo que‿el fue-go' -> [('lo','single'), ('que‿el','single'), ('fue','begin'), ('go','end')]"""
    out = []
    for w in line.split():
        parts = w.split('-')
        for i, p in enumerate(parts):
            kind = 'single' if len(parts) == 1 else 'begin' if i == 0 else 'end' if i == len(parts) - 1 else 'middle'
            out.append((p, kind))
    return out


def vowel_of(s):
    s = s.lower().translate(str.maketrans('áéíóú', 'aeiou'))
    strong = [c for c in s if c in 'aeo']
    if strong:
        return strong[-1]
    weak = [c for c in s if c in 'iu']
    return weak[-1] if weak else 'a'


def nearest(pcs, lo, hi, target):
    cands = [p for p in range(lo, hi + 1) if p % 12 in pcs]
    return min(cands, key=lambda p: (abs(p - target), p))


# --- voz principal y segunda voz
voice_notes = []
voice_notes += put_line('voz', S_SALIDA, SALIDA, 92, syllables=[('¡Ay!', 'single')], vowels=['a'])
for ci, (start, t) in enumerate(((S_C1, 0), (S_C2, 0), (S_C3, 2))):
    sy = [s for li in ORDEN for s in syllabify(LETRA[ci][li])]
    vw = [vowel_of(s) for s, _ in sy]
    voice_notes += put_line('voz', start, COPLA_MELODY, 88 + 4 * ci, transpose=t, syllables=sy, vowels=vw)


def second_voice(start, from_bar):
    for n in [n for n in voice_notes if start * BAR + from_bar * BAR <= n.t < (start + 26) * BAR]:
        bar = int(n.t // BAR)
        ch = chords[bar]
        cands = [p for p in range(n.p - 5, n.p - 2) if p % 12 in ch.pcs]
        if not cands:
            cands = [p for p in range(n.p - 5, n.p - 1) if p % 12 in scale_at(bar)] or [n.p - 4]
        p = min(cands, key=lambda q: abs(n.p - 4 - q))
        notes.append(N('voz2', n.t, n.d, p, n.v - 14, n.syl, n.vowel, n.tie))


second_voice(S_C2, ESTRIBILLO_FROM)
second_voice(S_C3, 0)

# --- tema instrumental
put_line('flauta', S_INTRO + 4, TEMA, 78)
put_line('bandurria', S_INTRO + 8, TEMA[4:], 70)
put_line('flauta', S_P1, TEMA, 84, transpose=12)
put_line('bandurria', S_P1, TEMA, 74)
put_line('flauta', S_P2, TEMA[:7] + [TEMA_A_MI], 90, transpose=12)
put_line('bandurria', S_P2, TEMA[:7] + [TEMA_A_MI], 80)


def fill(bar, trk, vel, octave=0):
    """Relleno de corcheas mientras la voz sostiene: arpegio que sube y escala que baja."""
    ch, sc = chords[bar], scale_at(bar)
    tones = [p for p in range(74, 96) if p % 12 in ch.pcs][:4]
    run = list(tones)
    p = tones[-1]
    for _ in range(2):
        p -= 1
        while p % 12 not in sc:
            p -= 1
        run.append(p)
    for i, p in enumerate(run):
        notes.append(N(trk, bar * BAR + i * .5, .5 if i < 5 else 1, p + octave, vel + (6 if i == 3 else 0)))


for hb in HOLD_BARS:
    fill(S_C1 + hb, 'gtr_punteo', 76, -12)
    fill(S_C2 + hb, 'flauta', 80)
    fill(S_C3 + hb, 'flauta', 88)
    fill(S_C3 + hb, 'bandurria', 70, -12)

# contracanto largo de flauta (estribillo de la copla 2 y toda la copla 3)
prev = 81
for start, frm, vel in ((S_C2, ESTRIBILLO_FROM, 50), (S_C3, 0, 58)):
    for b in range(frm, 26):
        if b in HOLD_BARS:
            continue
        bar = start + b
        prev = nearest(chords[bar].pcs, 76, 88, prev)
        notes.append(N('flauta', bar * BAR, 3, prev, vel))

# remate
put_line('flauta', S_CODA, [[(.5, 'G5'), (.5, 'C6'), (1, 'E6'), (.5, 'D6'), (.5, 'C6')],
                            [(.5, 'B5'), (.5, 'A5'), (.5, 'F#5'), (.5, 'D#5'), (.5, 'F#5'), (.5, 'A5')],
                            [(1, 'B5')]], 96)
put_line('bandurria', S_CODA, [[(.5, 'G4'), (.5, 'C5'), (1, 'E5'), (.5, 'D5'), (.5, 'C5')],
                               [(.5, 'B4'), (.5, 'A4'), (.5, 'F#4'), (.5, 'D#4'), (.5, 'F#4'), (.5, 'A4')],
                               [(1, 'E5')]], 84)

# --- violonchelo: contracanto grave, una nota por compás (dos en los finales de frase)
prev = 50
for bar in range(S_INTRO + 4, S_CODA + 2):
    ch = chords[bar]
    vel = 52 if S_C1 <= bar < S_P1 else 60
    prev = nearest(ch.pcs, 43, 62, prev)
    rel = (bar - S_C1) % 26 if S_C1 <= bar < S_CODA and not (S_P1 <= bar < S_C2 or S_P2 <= bar < S_C3) else None
    if rel in HOLD_BARS:
        notes.append(N('chelo', bar * BAR, 2, prev, vel))
        nxt = nearest(chords[bar + 1].pcs, 43, 62, prev)
        step = prev + (1 if nxt > prev else -1) * (2 if abs(nxt - prev) > 2 else 1)
        notes.append(N('chelo', bar * BAR + 2, 1, step, vel - 6))
    else:
        notes.append(N('chelo', bar * BAR, 3, prev, vel))
notes.append(N('chelo', S_CODA * BAR + 2 * BAR, 1, 40, 80))

# --- contrabajo
for bar in range(S_INTRO + 4, S_CODA + 3):
    ch = chords[bar]
    root = nearest([ch.bass], 38, 50, 44)
    if bar == S_CODA + 2:
        notes.append(N('bajo', bar * BAR, 1, root, 100))
        break
    fifth = root + 7 if root + 7 <= 52 else root - 5
    notes.append(N('bajo', bar * BAR, 1.8, root, 92))
    notes.append(N('bajo', bar * BAR + 2, .9, fifth, 70))

# --- guitarra: arpegio en la intro, rasgueado después
for bar in range(S_INTRO, S_INTRO + 4):
    v = chords[bar].voicing
    for i, idx in enumerate([0, 1, 2, 3, 2, 1]):
        notes.append(N('gtr_punteo', bar * BAR + i * .5, 1.5, v[idx], 62 + 4 * (bar - S_INTRO)))


def rasgueo(bar, vel):
    v, t0 = chords[bar].voicing, bar * BAR
    rel = (bar - S_C1) % 26
    phrase_end = rel in HOLD_BARS or bar in (S_INTRO + 11, S_SALIDA + 3, S_P1 + 7, S_P2 + 7)
    if bar % 2 == 0 or phrase_end:     # floreo de cuatro dedos al principio del compás
        for k in range(4):
            strums.append((t0 + k * .09, v, 'down', vel * (0.55 + 0.1 * k), .1 if k < 3 else .9))
    else:
        strums.append((t0, v, 'down', vel, 1))
    strums.append((t0 + 1, v, 'down', vel * .78, 1))
    strums.append((t0 + 2, v, 'up', vel * .62, .5))
    strums.append((t0 + 2.5, v, 'down', vel * .5, .5))


for bar in range(S_INTRO + 4, S_CODA + 2):
    base = 74 if bar < S_INTRO + 8 else 86 if bar < S_C1 else 78 if bar < S_P1 else 86
    rasgueo(bar, base)
strums.append((S_CODA * BAR + 2 * BAR, chords[S_CODA + 2].voicing, 'down', 110, 1))

# --- percusión (nombre, instante, velocidad)
perc = []


def palmas(bar, kind, contra=False):
    t0 = bar * BAR
    for b in range(3):
        perc.append(('palma_' + kind, t0 + b, 100 if b == 0 else 78))
        if contra:
            perc.append(('palma_contra', t0 + b + .5, 70))


def cajon(bar, end):
    t0 = bar * BAR
    if end:
        for t, k, v in ((0, 'cajon_grave', 100), (1, 'cajon_agudo', 80), (1.5, 'cajon_agudo', 70),
                        (2, 'cajon_agudo', 90), (2.5, 'cajon_agudo', 96)):
            perc.append((k, t0 + t, v))
    else:
        perc.extend([('cajon_grave', t0, 100), ('cajon_agudo', t0 + 1.5, 45), ('cajon_agudo', t0 + 2, 88)])


def castanuelas(bar):
    t0 = bar * BAR
    perc.extend([('casta_ria', t0, 80), ('casta', t0 + 1, 70), ('casta', t0 + 2, 92)])


for bar in range(S_INTRO + 4, S_CODA + 2):
    rel = (bar - S_C1) % 26
    in_copla = (S_C1 <= bar < S_P1) or (S_C2 <= bar < S_P2) or (S_C3 <= bar < S_CODA)
    end = (in_copla and rel in HOLD_BARS) or bar in (S_P1 + 7, S_P2 + 7, S_CODA + 1)
    if bar < S_INTRO + 8:
        palmas(bar, 'sorda')
    elif S_C1 <= bar < S_P1:
        palmas(bar, 'sorda')
    else:
        palmas(bar, 'clara', contra=bar >= S_C3)
    if bar >= S_P1:
        cajon(bar, end)
    if (S_INTRO + 8 <= bar < S_C1) or (S_P1 <= bar < S_C2 and bar >= S_P1 + 4) or \
       (S_P2 <= bar < S_C3) or bar >= S_CODA or (bar >= S_C3 and (end or rel >= ESTRIBILLO_FROM)):
        castanuelas(bar)
final_t = (S_CODA + 2) * BAR
perc += [('palma_clara', final_t, 120), ('palma_contra', final_t, 110), ('casta', final_t, 120),
         ('cajon_grave', final_t, 120)]

TOTAL_BEATS = N_BARS * BAR

# ================================================================ MIDI
TPB = 480


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


def write_midi(path):
    tk = lambda beats: int(round(beats * TPB))
    tracks = []
    tempo = int(60_000_000 / BPM)
    meta = [(0, 0, b'\xff\x51\x03' + tempo.to_bytes(3, 'big')), (0, 0, b'\xff\x58\x04\x03\x02\x18\x08'),
            (0, 0, b'\xff\x59\x02\x02\x00')]
    for bar, name in SECTIONS:
        txt = name.encode('utf-8')
        meta.append((tk(bar * BAR), 1, b'\xff\x06' + vlq(len(txt)) + txt))
    meta.append((tk(S_C3 * BAR), 2, b'\xff\x59\x02\x04\x00'))
    tracks.append(midi_track(meta, 'Candela y agua'))
    inst = [('voz', 'Voz', 0, 53), ('voz2', 'Segunda voz', 1, 53), ('flauta', 'Flauta', 2, 73),
            ('gtr', 'Guitarra flamenca', 3, 24), ('bandurria', 'Bandurria', 4, 25),
            ('chelo', 'Violonchelo', 5, 42), ('bajo', 'Contrabajo', 6, 32)]
    for key, name, ch, prog in inst:
        ev = [(0, 0, bytes([0xC0 | ch, prog]))]
        src = [n for n in notes if n.trk == key or (key == 'gtr' and n.trk == 'gtr_punteo')]
        if key == 'gtr':
            for t, v, direction, vel, d in strums:
                order = v if direction == 'down' else list(reversed(v))
                for i, p in enumerate(order):
                    src.append(N('gtr', t + i * .02, d, p, int(min(127, vel))))
        merged = []                          # une notas ligadas
        for n in sorted(src, key=lambda n: n.t):
            if n.tie and merged and merged[-1].p == n.p:
                merged[-1].d += n.d
                continue
            merged.append(N(n.trk, n.t, n.d, n.p, n.v, n.syl))
        for n in merged:
            on, off = tk(n.t), tk(n.t + n.d) - 10
            v = int(max(1, min(127, n.v)))
            ev.append((on, 2, bytes([0x90 | ch, n.p, v])))
            ev.append((max(on + 1, off), 0, bytes([0x80 | ch, n.p, 0])))
            if n.syl and key == 'voz':
                txt = (n.syl[0] + ('-' if n.syl[1] in ('begin', 'middle') else ' ')).encode('utf-8')
                ev.append((on, 1, b'\xff\x05' + vlq(len(txt)) + txt))
        tracks.append(midi_track(ev, name))
    gm = {'palma_clara': 39, 'palma_contra': 39, 'palma_sorda': 39, 'casta': 85, 'casta_ria': 85,
          'cajon_grave': 64, 'cajon_agudo': 63}
    ev = []
    for k, t, v in perc:
        if k == 'palma_sorda':
            v = int(v * .6)
        on = tk(t)
        ev.append((on, 2, bytes([0x99, gm[k], min(127, v)])))
        ev.append((on + 60, 0, bytes([0x89, gm[k], 0])))
    tracks.append(midi_track(ev, 'Palmas, cajón y castañuelas'))
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

    def part_xml(pid, src, harmonies, lyrics):
        events = sorted(src, key=lambda n: n.t)
        measures = []
        ei = 0
        carry = []
        for bar in range(N_BARS):
            m0, m1 = bar * BAR * DIV, (bar + 1) * BAR * DIV
            xml = [f'<measure number="{bar + 1}">']
            if bar == 0:
                xml.append(f'<attributes><divisions>{DIV}</divisions><key><fifths>2</fifths></key>'
                           '<time><beats>3</beats><beat-type>4</beat-type></time>'
                           '<clef><sign>G</sign><line>2</line></clef></attributes>')
                xml.append('<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit>'
                           f'<per-minute>{BPM}</per-minute></metronome></direction-type><sound tempo="{BPM}"/></direction>')
            if bar == S_C3:
                xml.append('<attributes><key><fifths>4</fifths></key></attributes>')
            if harmonies:
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
            pos = m0
            # notas que caen en este compás (troceadas en la barra)
            seg = list(carry)
            carry = []
            while ei < len(events) and events[ei].t * DIV < m1:
                n = events[ei]
                s, e = int(round(n.t * DIV)), int(round((n.t + n.d) * DIV))
                seg.append([s, min(e, m1), n.p, n.syl if lyrics else None, n.tie, False])
                if e > m1:
                    seg[-1][5] = True
                    carry.append([m1, e, n.p, None, True, False])
                ei += 1
            # el trozo arrastrado puede volver a pasar de la barra
            fixed = []
            for s in seg:
                if s[1] > m1:
                    carry.append([m1, s[1], s[2], None, True, False])
                    s[1], s[5] = m1, True
                fixed.append(s)
            for s, e, p, syl, tie_in, tie_out in sorted(fixed):
                if s > pos:
                    for u, typ, dot in pieces(s - pos):
                        xml.append(f'<note><rest/><duration>{u}</duration><type>{typ}</type>{"<dot/>" * dot}</note>')
                ps = pieces(e - s)
                for k, (u, typ, dot) in enumerate(ps):
                    tin = tie_in or k > 0
                    tout = tie_out or k < len(ps) - 1
                    ties = ('<tie type="stop"/>' if tin else '') + ('<tie type="start"/>' if tout else '')
                    tied = ('<tied type="stop"/>' if tin else '') + ('<tied type="start"/>' if tout else '')
                    lyr = ''
                    if syl and k == 0:
                        txt = syl[0].replace('&', '&amp;')
                        lyr = f'<lyric number="1"><syllabic>{syl[1]}</syllabic><text>{txt}</text></lyric>'
                    xml.append(f'<note>{pitch_xml(p)}<duration>{u}</duration>{ties}<type>{typ}</type>'
                               f'{"<dot/>" * dot}' + (f'<notations>{tied}</notations>' if tied else '') + f'{lyr}</note>')
                pos = e
            if pos < m1:
                for u, typ, dot in pieces(m1 - pos):
                    xml.append(f'<note><rest/><duration>{u}</duration><type>{typ}</type>{"<dot/>" * dot}</note>')
            if bar == N_BARS - 1:
                xml.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
            xml.append('</measure>')
            measures.append(''.join(xml))
        return f'<part id="{pid}">' + '\n'.join(measures) + '</part>'

    def mono(trk):
        """Una sola voz por pentagrama: si dos notas se solapan, manda la más reciente."""
        src = sorted([n for n in notes if n.trk == trk], key=lambda n: n.t)
        out = []
        for n in src:
            c = N(n.trk, n.t, n.d, n.p, n.v, n.syl, n.vowel, n.tie)
            if out and out[-1].t + out[-1].d > c.t:
                out[-1].d = c.t - out[-1].t
            out.append(c)
        return [n for n in out if n.d > 0]

    parts = [('P1', 'Voz', part_xml('P1', mono('voz'), True, True)),
             ('P2', 'Segunda voz', part_xml('P2', mono('voz2'), False, False)),
             ('P3', 'Flauta', part_xml('P3', mono('flauta'), False, False))]
    plist = ''.join(f'<score-part id="{pid}"><part-name>{name}</part-name></score-part>' for pid, name, _ in parts)
    doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" '
           '"http://www.musicxml.org/dtds/partwise.dtd">\n'
           '<score-partwise version="3.1"><work><work-title>Candela y agua</work-title></work>'
           '<identification><creator type="composer">Sevillana original</creator></identification>'
           f'<part-list>{plist}</part-list>\n' + '\n'.join(x for _, _, x in parts) + '</score-partwise>\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)


# ================================================================ síntesis
TOTAL_S = int((TOTAL_BEATS * SPB + 3.5) * SR)
tracks = {}


def track(name):
    if name not in tracks:
        tracks[name] = np.zeros(TOTAL_S)
    return tracks[name]


def add(name, t_sec, sig):
    buf = track(name)
    i = int(t_sec * SR)
    if i < 0:
        sig, i = sig[-i:], 0
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[:j - i]


def human(t, sd=0.006):
    return t * SPB + float(np.clip(rng.normal(0, sd), -2.5 * sd, 2.5 * sd))


def ks(freq, dur, amp, bright=.6, t60=2.0, pos=.18):
    """Cuerda pulsada (Karplus-Strong vectorizado por periodos, con afinación exacta por remuestreo)."""
    N_ = max(2, int(SR / freq))
    f_eff = SR / (N_ + .5)
    ratio = freq / f_eff
    L = int(dur * SR)
    Lg = int(L * ratio) + 2 * N_ + 4
    x = rng.uniform(-1, 1, N_)
    k = 1 + int((1 - bright) * 10)
    if k > 1:
        x = np.convolve(np.concatenate([x, x]), np.ones(k) / k, 'same')[N_ // 2: N_ // 2 + N_]
    p = int(pos * N_)
    if p:
        x = x - .6 * np.roll(x, p)
    x -= x.mean()
    x /= (np.abs(x).max() + 1e-9)
    d = 10 ** (-3 / (t60 * f_eff))
    nper = Lg // N_ + 2
    out = np.empty(nper * N_)
    out[:N_] = x
    last = 0.0
    for i in range(1, nper):
        prev = out[(i - 1) * N_: i * N_]
        sh = np.empty(N_)
        sh[0] = last
        sh[1:] = prev[:-1]
        last = prev[-1]
        out[i * N_:(i + 1) * N_] = d * .5 * (prev + sh)
    y = np.interp(np.arange(L) * ratio, np.arange(len(out)), out)
    r = min(L, int(.03 * SR))
    y[L - r:] *= np.linspace(1, 0, r)
    return y * amp


def env_adsr(L, a, r, sus=1.0, dec=0.0):
    e = np.ones(L) * sus
    A = min(L, int(a * SR))
    e[:A] = np.linspace(0, 1, A) if A else e[:A]
    if dec > 0 and L > A:
        Dn = min(L - A, int(dec * SR))
        e[A:A + Dn] = np.linspace(1, sus, Dn)
    R = min(L, int(r * SR))
    e[L - R:] *= np.linspace(1, 0, R)
    return e


def additive(f, amps):
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.zeros(len(f))
    fmax = f.max()
    for k, a in enumerate(amps, 1):
        if a and k * fmax < SR * .45:
            y += a * np.sin(k * ph)
    return y


FORMANTS = {  # voz masculina: (frecuencia, ancho, ganancia)
    'a': [(730, 110, 1.0), (1090, 120, .55), (2440, 170, .25), (3300, 250, .12)],
    'e': [(530, 90, 1.0), (1840, 130, .45), (2480, 170, .3), (3300, 250, .12)],
    'i': [(300, 70, 1.0), (2290, 150, .35), (3010, 200, .28), (3600, 250, .1)],
    'o': [(570, 90, 1.0), (840, 100, .6), (2410, 170, .18), (3300, 250, .08)],
    'u': [(320, 70, 1.0), (870, 100, .35), (2240, 170, .1), (3300, 250, .05)],
}


def sing(f0, dur, amp, vowel, prev_f=None, vib=.016, shift=1.0, breath=.02):
    L = int(dur * SR)
    t = np.arange(L) / SR
    f = np.full(L, f0)
    if prev_f:
        f = f0 * (prev_f / f0) ** np.exp(-t / .035)
    onset = np.clip((t - .12) / .25, 0, 1)
    f = f * (1 + vib * onset * np.sin(2 * np.pi * 5.6 * t + rng.uniform(0, 6)))
    nh = int(SR * .45 / f0)
    amps = []
    for k in range(1, nh + 1):
        fk = k * f0
        a = .25 / k ** .7
        for F, B, g in FORMANTS[vowel]:
            a += g * math.exp(-((fk - F * shift) / B) ** 2)
        amps.append(a)
    y = additive(f, amps)
    y += breath * rng.normal(0, 1, L) * (np.abs(y).max() / 3)
    y *= env_adsr(L, .05 if not prev_f else .02, .09, .92, .12)
    return y * amp / (np.abs(y).max() + 1e-9)


def flute(f0, dur, amp):
    L = int(dur * SR)
    t = np.arange(L) / SR
    onset = np.clip((t - .15) / .3, 0, 1)
    f = f0 * (1 + .004 * onset * np.sin(2 * np.pi * 5.0 * t))
    y = additive(f, [1, .38, .16, .08, .04, .02])
    e = env_adsr(L, .045, .07, .9, .1)
    trem = 1 + .05 * onset * np.sin(2 * np.pi * 5.0 * t + .5)
    return y * e * trem * amp, e * amp


def bowed(f0, dur, amp):
    L = int(dur * SR)
    t = np.arange(L) / SR
    onset = np.clip((t - .2) / .3, 0, 1)
    f = f0 * (1 + .005 * onset * np.sin(2 * np.pi * 5.2 * t))
    amps = []
    for k in range(1, 30):
        fk = k * f0
        a = 1 / k ** 1.1 * (1 + 1.2 * math.exp(-((fk - 280) / 120) ** 2) + .6 * math.exp(-((fk - 1500) / 500) ** 2))
        amps.append(a)
    y = additive(f, amps)
    y *= env_adsr(L, .16, .2, .85, .2)
    return y * amp / (np.abs(y).max() + 1e-9)


def noise_burst(L, decay):
    t = np.arange(L) / SR
    return rng.normal(0, 1, L) * np.exp(-t / decay)


def clap(amp, low=False):
    L = int(.12 * SR)
    y = np.zeros(L)
    for k in range(rng.integers(2, 4)):          # varias manos, ligeramente desfasadas
        off = int(rng.uniform(0, .011) * SR)
        b = noise_burst(L - off, .028 if low else .016)
        y[off:] += b * rng.uniform(.6, 1)
    if low:
        y = np.convolve(y, np.ones(9) / 9, 'same')
    else:
        y = np.diff(np.concatenate([[0], y]))
    return y * amp / (np.abs(y).max() + 1e-9)


def castanet(amp):
    L = int(.06 * SR)
    t = np.arange(L) / SR
    y = noise_burst(L, .003) * .5
    for f, dcy in ((2350, .012), (3550, .008), (5200, .005)):
        y += np.sin(2 * np.pi * f * t) * np.exp(-t / dcy)
    return y * amp / (np.abs(y).max() + 1e-9)


def cajon_low(amp):
    L = int(.4 * SR)
    t = np.arange(L) / SR
    f = 75 + 70 * np.exp(-t / .025)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16)
    y += .25 * noise_burst(L, .006)
    return y * amp / (np.abs(y).max() + 1e-9)


def cajon_high(amp):
    L = int(.25 * SR)
    t = np.arange(L) / SR
    y = .6 * np.sin(2 * np.pi * 210 * t) * np.exp(-t / .03)
    wires = np.diff(np.concatenate([[0], noise_burst(L, .07)]))
    y += noise_burst(L, .012) * .5 + wires * .9
    return y * amp / (np.abs(y).max() + 1e-9)


def render():
    # --- guitarra rasgueada
    for t, v, direction, vel, d in strums:
        order = v if direction == 'down' else list(reversed(v))
        t0 = human(t, .004)
        for i, p in enumerate(order):
            a = (vel / 127) ** 1.6 * (.9 if direction == 'down' else .7) * rng.uniform(.85, 1)
            dur = d * SPB + .05
            add('gtr', t0 + i * (.011 if direction == 'down' else .008),
                ks(hz(p), dur, a * .35, bright=.45 + .4 * vel / 127, t60=1.6))
    for n in notes:
        tr = n.trk
        if tr == 'gtr_punteo':
            add('gtr', human(n.t, .004), ks(hz(n.p), n.d * SPB + .3, (n.v / 127) ** 1.5 * .5, bright=.75, t60=1.8, pos=.12))
        elif tr == 'bandurria':
            dur = n.d * SPB
            step = SPB / 4                  # trémolo
            k, tt = 0, 0.0
            while tt < dur - .02:
                a = (n.v / 127) ** 1.5 * .22 * (1 if k % 2 == 0 else .75) * rng.uniform(.85, 1.05)
                for det in (.997, 1.003):
                    add('bandurria', n.t * SPB + tt, ks(hz(n.p) * det, min(step * 1.6, dur - tt + .05), a,
                                                        bright=.95, t60=.9, pos=.1))
                tt += step
                k += 1
        elif tr == 'bajo':
            add('bajo', human(n.t, .003), ks(hz(n.p), n.d * SPB + .1, (n.v / 127) ** 1.3 * .9, bright=.1, t60=1.4, pos=.3))
        elif tr == 'chelo':
            add('chelo', n.t * SPB - .03, bowed(hz(n.p), n.d * SPB + .15, (n.v / 127) * .5))
        elif tr == 'flauta':
            y, e = flute(hz(n.p), n.d * SPB + .03, (n.v / 127) ** 1.2 * .5)
            add('flauta', human(n.t, .004), y)
            add('flauta_aire', human(n.t, .0), e)
    for vt, shift, vib in (('voz', 1.0, .016), ('voz2', 1.06, .011)):
        seq = sorted([n for n in notes if n.trk == vt], key=lambda n: n.t)
        merged = []
        for n in seq:
            if n.tie and merged and merged[-1].p == n.p:
                merged[-1].d += n.d
            else:
                merged.append(N(n.trk, n.t, n.d, n.p, n.v, n.syl, n.vowel))
        prev_end, prev_f = -9, None
        for n in merged:
            f0 = hz(n.p - 12)                # voz de tenor: suena una octava por debajo de lo escrito
            legato = abs(n.t - prev_end) < .05
            add(vt, n.t * SPB - .02, sing(f0, n.d * SPB + (.06 if legato else 0), (n.v / 127) * .6, n.vowel,
                                          prev_f if legato else None, vib, shift))
            prev_end, prev_f = n.t + n.d, f0
    for k, t, v in perc:
        a = (v / 127) ** 1.4
        tt = human(t, .005)
        if k == 'palma_clara':
            add('palmas_i', tt, clap(a * .55))
        elif k == 'palma_contra':
            add('palmas_d', tt, clap(a * .45))
        elif k == 'palma_sorda':
            add('palmas_s', tt, clap(a * .7, low=True))
        elif k == 'casta':
            add('casta', tt, castanet(a * .5))
        elif k == 'casta_ria':
            for i in range(4):
                add('casta', tt + i * .028, castanet(a * (.3 + .07 * i)))
        elif k == 'cajon_grave':
            add('cajon', tt, cajon_low(a * .8))
        elif k == 'cajon_agudo':
            add('cajon', tt, cajon_high(a * .45))


def eq(x, pts):
    """Ecualización por FFT: pts = [(Hz, dB), ...] interpolados en escala logarítmica."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    lf = np.log10(np.maximum(f, 10))
    fx = np.log10([p[0] for p in pts])
    g = 10 ** (np.interp(lf, fx, [p[1] for p in pts]) / 20)
    return np.fft.irfft(X * g, len(x))


def reverb_ir(seconds=2.2, t60=1.7):
    L = int(seconds * SR)
    t = np.arange(L) / SR
    irs = []
    for ch in range(2):
        n = rng.normal(0, 1, L) * np.exp(-6.9 * t / t60)
        n = eq(n, [(20, -10), (200, 0), (2500, -2), (6000, -10), (16000, -24)])
        n[:int(.012 * SR)] = 0
        for d, g in ((.013, .5), (.021, .38), (.029, .3), (.037, .25)):
            n[int((d + .002 * ch) * SR)] += g * 6
        irs.append(n / np.sqrt(np.sum(n ** 2)))
    return irs


def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]


MIX = {  # nivel, panorama (-1 izq … 1 der), envío a reverb, ecualización
    'voz': (1.00, 0.0, .30, [(20, -30), (120, -6), (250, 0), (3000, 2), (8000, -6), (16000, -20)]),
    'voz2': (.62, .18, .34, [(20, -30), (150, -6), (300, 0), (3000, 0), (8000, -8), (16000, -20)]),
    'flauta': (.62, .38, .35, [(20, -30), (300, -4), (1000, 0), (5000, 0), (12000, -10)]),
    'flauta_aire': (.0, .38, .35, None),
    'gtr': (.85, -.18, .16, [(20, -30), (80, -6), (150, 0), (250, 2), (900, -2), (3500, 2), (9000, -4), (16000, -18)]),
    'bandurria': (.42, .5, .25, [(20, -40), (250, -8), (700, 0), (3000, 3), (10000, -6)]),
    'chelo': (.40, -.42, .38, [(20, -20), (60, 0), (2500, -4), (6000, -16)]),
    'bajo': (.62, 0.0, .06, [(20, -30), (40, -4), (70, 0), (200, 0), (800, -8), (3000, -24)]),
    'palmas_i': (.42, -.55, .18, [(20, -40), (500, -6), (1500, 2), (4000, 0), (12000, -8)]),
    'palmas_d': (.32, .55, .18, [(20, -40), (500, -6), (1700, 2), (4500, 0), (12000, -8)]),
    'palmas_s': (.45, -.2, .14, [(20, -30), (250, 0), (900, -2), (2500, -14)]),
    'casta': (.32, .3, .14, [(20, -40), (1200, -4), (3000, 0), (12000, -6)]),
    'cajon': (.50, .06, .10, [(20, -30), (50, -6), (90, 0), (400, -2), (3000, 0), (10000, -8)]),
}


def mixdown(path):
    # aire de la flauta: ruido con la envolvente de las notas
    if 'flauta_aire' in tracks:
        air = eq(rng.normal(0, 1, TOTAL_S) * tracks.pop('flauta_aire'),
                 [(20, -60), (1200, -18), (2800, 0), (5000, -6), (12000, -30)])
        tracks['flauta'] += .05 * air
    L = np.zeros(TOTAL_S)
    R = np.zeros(TOTAL_S)
    WL = np.zeros(TOTAL_S)
    WR = np.zeros(TOTAL_S)
    levels = {}
    for name, x in tracks.items():
        lvl, pan, send, curve = MIX[name]
        if curve:
            x = eq(x, curve)
        rms = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) if np.any(np.abs(x) > 1e-4) else 1
        x = x / (rms + 1e-9) * .1 * lvl            # equilibrio por energía y nivel de mezcla
        levels[name] = rms
        gl, gr = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        L += x * gl
        R += x * gr
        WL += x * gl * send
        WR += x * gr * send
    ir = reverb_ir()
    L += .55 * conv(WL, ir[0])
    R += .55 * conv(WR, ir[1])
    st = np.stack([L, R], 1)
    st = eq(st[:, 0], [(20, -30), (35, -12), (60, -2), (90, 0), (16000, 0)]), eq(st[:, 1], [(20, -30), (35, -12), (60, -2), (90, 0), (16000, 0)])
    st = np.stack(st, 1)
    peak = np.abs(st).max()
    st = np.tanh(1.6 * st / peak) / np.tanh(1.6) * .93     # saturación suave
    fade = int(.8 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    pcm = (st * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return levels


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out = args[0] if args else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out, exist_ok=True)
    write_midi(os.path.join(out, 'candela-y-agua.mid'))
    write_musicxml(os.path.join(out, 'candela-y-agua.musicxml'))
    if '--sin-audio' not in sys.argv:
        render()
        mixdown(os.path.join(out, 'candela-y-agua.wav'))
    print(f'{N_BARS} compases, {TOTAL_BEATS * SPB:.1f} s a {BPM} negras por minuto')
