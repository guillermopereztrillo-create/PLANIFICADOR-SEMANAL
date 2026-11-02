# «Candela y agua» — sevillana

Una sevillana original. Toma de Los Romeros de la Puebla la idea de fondo: guitarra rasgueada con aire rociero, palmas, coros en terceras y una letra de copla que se canta. La música no copia ninguna de sus sevillanas, ni en la armonía, ni en la melodía, ni en la forma.

| Archivo | Para qué sirve |
|---|---|
| `candela-y-agua.mp3` | Para escucharla (1:53). Maqueta con instrumentos sampleados (banco de sonidos MuseScore General). |
| `candela-y-agua.musicxml` | La partitura: voz con letra y cifrado, segunda voz, gaita rociera y dos trompetas. Se abre con MuseScore, Finale, Sibelius o Dorico. |
| `candela-y-agua.mid` | Una pista por instrumento, con la letra incluida. Sirve para GarageBand, Logic, Cubase, etc. |
| `componer.py` | El script que genera los tres archivos anteriores con `python3 componer.py`. Para el audio necesita `fluidsynth`, `ffmpeg` y el banco de sonidos MuseScore General (paquete `musescore-general-soundfont-lossless`). |

## Ficha

- **Compás:** 3/4, a ♩ = 190. Cada copla se baila con su remate.
- **Tonalidad:** Re mayor. La tercera copla sube un tono, a Mi mayor.
- **Instrumentos:** voz y segunda voz (coro), dos guitarras flamencas (rasgueado y punteo o contestaciones), gaita rociera con tamboril, dos trompetas, mandolina en trémolo, cuerdas, violonchelo, contrabajo, cajón, palmas (sordas, claras y a contratiempo) y castañuelas.

## Forma

| Compases | Sección | Qué pasa |
|---|---|---|
| 1–4 | **Llamada de gaita** | La gaita rociera sola con el tamboril, como abre un camino del Rocío. |
| 5–16 | **Introducción** | La guitarra 2 arpegia sola sobre un pedal de Re (D – E/D) con color **lidio** (el Sol♯). En el compás 9 entran la guitarra 1 rasgueando y la gaita con el tema, y en el 13 la mandolina, las castañuelas y las palmas. |
| 17–20 | **Salida** | Un «¡Ay!» melismático de la voz, con las guitarras. |
| 21–46 | **Copla 1** | Voz, guitarra rasgueada, contrabajo, violonchelo y palmas sordas. Los rellenos son punteos de la guitarra 2. |
| 47–54 | **Pasada** | Dos trompetas en terceras toman el tema, con la mandolina. Entran el cajón y el tamboril. |
| 55–80 | **Copla 2** | Palmas claras y contestaciones de la guitarra 2. En el estribillo entran la segunda voz y las cuerdas, y la gaita hace los rellenos. |
| 81–88 | **Pasada que modula** | Gaita, trompetas y mandolina juntas. El último compás va a Si7 para llevar a Mi. |
| 89–114 | **Copla 3 (en Mi)** | Todo el grupo: dos voces, cuerdas, palmas a contratiempo, castañuelas en el estribillo, rellenos de trompetas, y las trompetas doblando la voz en la última repetición. |
| 115–117 | **Remate** | C – B7 – E con trompetas, gaita y mandolina. Corte seco en el primer tiempo, como se para el baile. |

Cada copla dura 26 compases y se divide en frases de **6 + 6 + 8 + 6**: versos 1-2, versos 3-4, estribillo, y repetición de los dos últimos versos más aguda. En los compases en que la voz sostiene la nota, un instrumento hace un relleno.

## Armonía de la copla (en Re)

```
Versos 1-2   | D    | D    | G    | A7   | D    | A    |
Versos 3-4   | F#m  | B7   | Em   | C    | A7   | D    |
Estribillo   | G    | Bb   | C    | D    | Em   | A7   | D   | D |
Repetición   | Bb   | C    | A7   | Em7  | A7   | D    |
```

## Qué la hace distinta

1. **No usa la cadencia andaluza** (Lam–Sol–Fa–Mi), que es la marca de casi todas las sevillanas. Esta canción vive en el modo mayor y saca el color de préstamos modales:
   - el **Sol♯ lidio** de la introducción (E/D sobre pedal de Re);
   - el **Do mayor (♭VII)**, que da un aire mixolidio;
   - el **Si♭ mayor (♭VI)**, que aparece al empezar el estribillo y oscurece el final: «Si-re-na‿y **a**-gua» cae sobre un Fa natural.
2. **El B7 del verso 3** (dominante secundaria hacia Mim) mete un Re♯ cromático en la guitarra.
3. **Las frases son de 6 y 8 compases**, no de 4.
4. **La instrumentación** mezcla lo rociero con lo de banda: gaita y tamboril abren la canción, las trompetas en terceras llevan las pasadas y la mandolina hace trémolos. El violonchelo lleva un contracanto grave y el cajón no entra hasta la primera pasada. La copla 1 es casi desnuda y la 3 suena con todo el grupo.
5. **Sube un tono para la tercera copla** con una pasada que modula, y **remata con ♭VI–V–I** (C–B7–E) en vez del cierre frigio habitual.

## Letra

Son seguidillas de 7-5-7-5 sílabas con estribillo de 5-7-5. Las rimas son asonantes (á-a en la 1.ª y la 3.ª, é-a en la 2.ª). La sinalefa se marca con «‿».

**Salida:** ¡Ay!

**Copla 1**
> Agua de madrugada
> sobre la brasa,
> lo que el fuego levanta
> el agua, en calma.
> *Sirena y agua,*
> *que entre el humo y la noche*
> *despunta el alba.*

**Copla 2**
> Tengo un casco de plata
> y una escalera
> para subir al cielo
> cuando tú quieras.
> *Que no hay candela*
> *que me queme por dentro*
> *como tu ausencia.*

**Copla 3**
> Sevilla tiene un río
> que no se apaga,
> y un fuego en cada patio
> que el agua guarda.
> *Candela y agua,*
> *mi Sevilla es un cante*
> *que nunca acaba.*

Orden en que se canta cada copla: versos 1-2 · 3-4 · 5-6-7 · 6-7.

## Melodía de la copla (voz, en Re)

La melodía se escribe en clave de sol y la canta un tenor una octava más baja. Su ámbito es de La a Si (en Mi, de Si a Do♯). Cada sílaba acentuada cae en un primer tiempo o en una nota larga: «ma-dru-**GA**-da», «so-bre la **BRA**-sa».

```
| -  A  D | F# E  D | G (A G) F# | -  E F# G | F#--  E | E~~~~~ |
  ·  A- gua de ma dru  ga        da   so-bre la  bra    sa
```

La partitura completa con todas las sílabas está en `candela-y-agua.musicxml`.

## Para llevarla a un grupo de verdad

- La maqueta usa instrumentos grabados, pero la voz es un coro sampleado que canta «aah»: ningún banco de sonidos puede cantar la letra. Para la versión final hace falta un cantaor, o cargar la pista de voz del MIDI en un programa de voz sintética.
- La tonalidad está pensada para tenor. Para otra voz, transpón todo con el programa o cambia en `componer.py` el transporte de cada copla (`(S_C1, 0), (S_C2, 0), (S_C3, 2)`).
