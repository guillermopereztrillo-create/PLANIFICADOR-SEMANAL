#!/usr/bin/env python3
"""Pone voz cantada a «Candela y agua» con el sintetizador de voz MBROLA.

Cada sílaba de la letra se convierte en fonemas (castellano con seseo, como se
canta en Sevilla). Las consonantes de ataque se adelantan al tiempo, como hace
un cantaor, y la vocal sostiene la nota con su vibrato. Los melismas son cambios
de altura dentro de la misma vocal.

Uso:  python3 cantar.py [carpeta_salida]
Necesita: mbrola, las voces mbrola-es2 (solista) y mbrola-es4 (segunda voz),
fluidsynth, ffmpeg y el banco de sonidos MuseScore General.
"""
import math
import os
import random
import subprocess
import sys
import unicodedata

import componer as C

random.seed(7)
SPB = 60.0 / C.BPM
VOCALES = 'aeiou'


# ---------------------------------------------------------------- de letras a fonemas
def sin_tilde(s):
    s = s.replace('ñ', '\0')
    s = ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) != 'Mn')
    return s.replace('\0', 'ñ')


def fonemas(silaba, inicio_palabra):
    """'quie' -> (ataque, vocales, coda), p. ej. (['k'], [('i', False), ('e', True)], [])."""
    raw = silaba.lower().replace('‿', '').strip('.,;:¡!¿?')
    acentuada = {sin_tilde(c) for c in raw if c in 'áéíóú'}
    s = sin_tilde(raw).replace('ü', 'w')
    out, i = [], 0
    while i < len(s):
        c, nxt = s[i], s[i + 1] if i + 1 < len(s) else '#'
        two = s[i:i + 2]
        if two == 'ch':
            out.append('tS'); i += 2; continue
        if two == 'll':
            out.append('jj'); i += 2; continue                # yeísmo
        if two == 'rr':
            out.append('rr'); i += 2; continue
        if two == 'qu':
            out.append('k'); i += 2; continue
        if two in ('gu',) and i + 2 < len(s) and s[i + 2] in 'ei':
            out.append('g'); i += 2; continue
        if c == 'c':
            out.append('s' if nxt in 'ei' else 'k')           # seseo
        elif c == 'z':
            out.append('s')
        elif c == 'g':
            out.append('x' if nxt in 'ei' else 'g')
        elif c == 'j':
            out.append('x')
        elif c == 'ñ':
            out.append('J')
        elif c == 'h':
            pass
        elif c == 'v':
            out.append('b')
        elif c == 'w':
            out.append('w')
        elif c == 'y':
            out.append('jj' if nxt in VOCALES else 'i')
        elif c == 'r':
            out.append('rr' if (i == 0 and inicio_palabra) else 'r')
        elif c == 'x':
            out.extend(['k', 's'])
        else:
            out.append(c)
        i += 1
    # separa ataque, núcleo vocálico y coda
    idx = [k for k, p in enumerate(out) if p in VOCALES]
    if not idx:
        return out, [('a', True)], []
    ataque, nucleo, coda = out[:idx[0]], out[idx[0]:idx[-1] + 1], out[idx[-1] + 1:]
    nucleo = [p for p in nucleo if p in VOCALES]
    fuerza = {'a': 3, 'e': 2, 'o': 2, 'i': 1, 'u': 1}
    principal = max(range(len(nucleo)), key=lambda k: (nucleo[k] in acentuada, fuerza[nucleo[k]], k))
    vocales = [(v, k == principal) for k, v in enumerate(nucleo)]
    # una u o una i débil delante de la vocal principal suena como semiconsonante
    pre = []
    for v, main in vocales:
        if main:
            break
        pre.append(v)
    if pre and all(v in 'iu' for v in pre):
        ataque = ataque + ['w' if v == 'u' else 'jj' for v in pre]
        vocales = vocales[len(pre):]
    limpias = []                                   # dos vocales iguales seguidas se cantan como una
    for v, main in vocales:
        if limpias and limpias[-1][0] == v:
            limpias[-1] = (v, limpias[-1][1] or main)
        else:
            limpias.append((v, main))
    return ataque, limpias, coda


DUR_CONS = {'r': .035, 'rr': .085, 's': .085, 'f': .075, 'x': .08, 'tS': .085, 'jj': .06, 'w': .05, 'J': .07,
            'm': .065, 'n': .06, 'l': .06, 'L': .06, 'p': .06, 't': .055, 'k': .065, 'b': .05, 'd': .045,
            'g': .05, 'T': .085}
SONORAS = {'m', 'n', 'l', 'L', 'J', 'r', 'rr', 'jj', 'w', 'b', 'd', 'g'}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- de la partitura a una línea de fonemas
def silabas_de(trk):
    """Agrupa las notas de una pista en sílabas: [(texto, inicio_palabra, [(t, d, nota), ...]), ...]."""
    src = sorted([n for n in C.notes if n.trk == trk], key=lambda n: n.t)
    out, fin_palabra = [], True
    for n in src:
        if n.syl:
            out.append([n.syl[0], fin_palabra, [(n.t, n.d, n.p)]])
            fin_palabra = n.syl[1] in ('single', 'end')
        elif out:
            t0, d0, p0 = out[-1][2][-1]
            if n.tie and p0 == n.p and abs(t0 + d0 - n.t) < 1e-6:
                out[-1][2][-1] = (t0, d0 + n.d, p0)
            else:
                out[-1][2].append((n.t, n.d, n.p))
    return out


def pitch_curve(notas, t_ini, t_fin, octava, vib=0.016):
    """Puntos (segundo, Hz) para una vocal que recorre una o varias notas, con vibrato."""
    pts = []
    t = t_ini
    step = .04
    while t <= t_fin + 1e-9:
        # nota que suena en t (con un deslizamiento de 45 ms entre notas)
        f = None
        for k, (nt, nd, p) in enumerate(notas):
            a, b = nt * SPB, (nt + nd) * SPB
            if a - .001 <= t < b or k == len(notas) - 1:
                f = hz(p + octava)
                if k > 0 and t - a < .045:
                    fp = hz(notas[k - 1][2] + octava)
                    f = fp * (f / fp) ** ((t - a) / .045)
                break
        edad = t - t_ini
        prof = vib * min(1, max(0, (edad - .18) / .3))
        f *= 1 + prof * math.sin(2 * math.pi * 5.4 * edad)
        pts.append((t, f))
        t += step
    return pts


def linea_pho(trk, octava=-12, vib=.016):
    sil = silabas_de(trk)
    evs = []          # (fonema, inicio, fin, [(t, Hz)])
    for i, (texto, ini_pal, notas) in enumerate(sil):
        ataque, vocales, coda = fonemas(texto, ini_pal)
        t_on = notas[0][0] * SPB
        t_off = (notas[-1][0] + notas[-1][1]) * SPB
        nxt_on = sil[i + 1][2][0][0] * SPB if i + 1 < len(sil) else 1e9
        legato = nxt_on - t_off < .02
        t_off -= .02 if legato else .06               # respiración breve si viene silencio
        # ataque: antes del tiempo
        dur_at = [DUR_CONS.get(p, .06) for p in ataque]
        t = t_on - sum(dur_at)
        if evs and t < evs[-1][2]:                    # roba tiempo a la vocal anterior
            ph, a, b, pts = evs[-1]
            evs[-1] = (ph, a, max(a + .05, t), [p for p in pts if p[0] < max(a + .05, t)] or pts[:1])
            t = evs[-1][2]
        f0 = hz(notas[0][2] + octava)
        for p, d in zip(ataque, dur_at):
            evs.append((p, t, t + d, [(t, f0), (t + d, f0)] if p in SONORAS else []))
            t += d
        # coda
        dur_co = [DUR_CONS.get(p, .06) for p in coda]
        v_fin = t_off - sum(dur_co)
        # vocales: las secundarias, breves; la principal sostiene la nota
        cortas = [v for v, main in vocales if not main]
        v_ini = t
        span = max(.08, v_fin - v_ini)
        tiempos = []
        tt = v_ini
        for v, main in vocales:
            d = .075 if not main else max(.06, span - .075 * len(cortas))
            tiempos.append((v, tt, tt + d))
            tt += d
        curva = pitch_curve(notas, v_ini, tt, octava, vib)
        for v, a, b in tiempos:
            pts = [(x, f) for x, f in curva if a <= x <= b] or [(a, f0)]
            evs.append((v, a, b, pts))
        t = tt
        fl = hz(notas[-1][2] + octava)
        for p, d in zip(coda, dur_co):
            evs.append((p, t, t + d, [(t, fl), (t + d, fl)] if p in SONORAS else []))
            t += d
    # a texto .pho con silencios
    lines, t = [], 0.0
    for ph, a, b, pts in evs:
        if a > t + .005:
            ms = int(round((a - t) * 1000))
            while ms > 0:                              # MBROLA no admite silencios muy largos
                lines.append(f'_ {min(ms, 10000)}')
                ms -= 10000
            t = a
        d = max(.012, b - t)
        ms = int(round(d * 1000))
        pp = ' '.join(f'{int(max(0, min(100, (x - t) / d * 100)))} {int(round(f))}' for x, f in pts)
        lines.append(f'{ph} {ms} {pp}'.rstrip())
        t += d
    lines.append('_ 500')
    return '\n'.join(lines) + '\n'


def sintetiza(pho, voz, wav):
    if voz == 'es4':                 # a esta voz le faltan /w/ y /j/ tras consonante: se cantan como u, i breves
        out, prev = [], '_'
        for l in pho.splitlines():
            ph = l.split()[0]
            if ph == 'w':
                l = 'u' + l[1:]
            elif ph == 'jj' and prev not in ('_', 'a', 'e', 'i', 'o', 'u'):
                l = 'i' + l[2:]
            out.append(l)
            prev = l.split()[0]
        pho = '\n'.join(out) + '\n'
    with open(wav + '.pho', 'w') as f:
        f.write(pho)
    subprocess.run(['mbrola', '-e', f'/usr/share/mbrola/{voz}/{voz}', wav + '.pho', wav], check=True)


def main(out):
    base = os.path.join(out, 'candela-y-agua')
    # 1) acompañamiento sin el coro (la voz cantada lo sustituye)
    keep = list(C.INSTRUMENTS)
    C.INSTRUMENTS[:] = [i for i in keep if i[0] not in ('voz', 'voz2')]
    C.INSTRUMENTS[:] = [(k, n, ch, b, p, (vol - 20 if k == 'gaita' else vol), pan, rev)
                        for k, n, ch, b, p, vol, pan, rev in C.INSTRUMENTS]
    C.write_midi(base + '-acompanamiento.mid')
    C.INSTRUMENTS[:] = keep
    C.render_audio(base + '-acompanamiento.mid', base + '-acompanamiento.wav', base + '-acompanamiento.mp3')
    # 2) voces
    sintetiza(linea_pho('voz', -12, .018), 'es2', base + '-voz.wav')
    sintetiza(linea_pho('voz2', -12, .012), 'es4', base + '-voz2.wav')
    # 3) mezcla: voces al frente, con algo de sala
    filtro = (
        '[1:a]aresample=44100,highpass=f=90,equalizer=f=3000:t=q:w=1.2:g=3,'
        'aecho=0.8:0.6:45|95:0.22|0.14,volume=2.4,pan=stereo|c0=0.98*c0|c1=0.9*c0[v1];'
        '[2:a]aresample=44100,highpass=f=90,aecho=0.8:0.6:55|110:0.22|0.14,volume=1.25,'
        'pan=stereo|c0=0.75*c0|c1=1.0*c0[v2];'
        '[0:a][v1][v2]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=11[m]'
    )
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', base + '-acompanamiento.wav',
                    '-i', base + '-voz.wav', '-i', base + '-voz2.wav', '-filter_complex', filtro,
                    '-map', '[m]', '-ar', '44100', base + '-cantada.wav'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', base + '-cantada.wav', '-codec:a', 'libmp3lame',
                    '-b:a', '192k', '-metadata', 'title=Candela y agua (cantada)', base + '-cantada.mp3'], check=True)
    print('Listo:', base + '-cantada.mp3')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
