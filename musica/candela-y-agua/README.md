# «Candela y agua» — sevillanas

Cuatro sevillanas rocieras originales para bailar, en la línea de Los Romeros de la Puebla y Brisa de la Puebla. Llevan dos guitarras rasgueadas, gaita rociera con tamboril, bandurria en trémolo, pandereta, palmas, castañuelas y coro. La melodía, la armonía y la letra son nuevas.

| Archivo | Para qué sirve |
|---|---|
| `candela-y-agua-cantada.mp3` | **Versión cantada** (3:34): la letra cantada por una voz sintética (solista y segunda voz en terceras) sobre la música. |
| `candela-y-agua.mp3` | Versión instrumental, con el coro haciendo «aah». Instrumentos sampleados (banco de sonidos MuseScore General). |
| `candela-y-agua.musicxml` | La partitura: voz con letra y cifrado, segunda voz, gaita rociera y dos trompetas. Se abre con MuseScore, Finale, Sibelius o Dorico. |
| `candela-y-agua.mid` | Una pista por instrumento, con la letra incluida. Sirve para GarageBand, Logic, Cubase, etc. |
| `cantar.py` | Genera la versión cantada con `python3 cantar.py`. Necesita además `mbrola` y las voces `mbrola-es1`, `mbrola-es2` y `mbrola-es4`. |
| `componer.py` | El script que genera los tres archivos anteriores con `python3 componer.py`. Para el audio necesita `fluidsynth`, `ffmpeg` y el banco de sonidos MuseScore General (paquete `musescore-general-soundfont-lossless`). |

## Ficha

- **Compás:** 3/4 con el acento fuerte siempre en el 1 (¡UN!-dos-tres), a ♩ = 174. La guitarra se va a veces al aire de 6/8.
- **Tonalidad:** Mi mayor.
- **Instrumentos rocieros, de principio a fin:**
  - **Gaita rociera:** lleva la melodía del cante entera, una octava por encima, además del tema de la introducción y las pasadas.
  - **Tamboril:** golpe con la maza en el 1 y un redoble corto hacia el 3.
  - **Dos guitarras flamencas:** rasguean el compás a la vez, la segunda en acordes agudos y un pelo detrás.
  - **Bandurria** (sonido de mandolina) en trémolo: dobla el cante.
  - **Pandereta, palmas y castañuelas.**
  - **Coro** con segunda voz.
  - Contrabajo discreto. Trompetas solo en las pasadas de la 3.ª y la 4.ª sevillana.

## Tomado de «Las Palmas» (Brisa de la Puebla)

No he podido escuchar la canción. Lo que sigue sale de medir el fragmento de 16 segundos que Spotify publica:

- **Tempo:** unas 174 negras por minuto (un compás por segundo, más o menos).
- **Tonalidad:** el fragmento está en la zona de Mi mayor.
- **Rasgueo:** golpe en el 1 y corcheas seguidas. Las más fuertes, después del 1, son el «y» del 2 y el 3; el 2 va flojo. Fuerza media medida en cada corchea:

| Corchea | 1 | y | 2 | y | 3 | y |
|---|---|---|---|---|---|---|
| «Las Palmas» | 1,00 | 0,28 | 0,38 | 0,52 | 0,58 | 0,42 |
| «Candela y agua» | 1,00 | 0,15–0,30 | 0,37–0,50 | 0,46–0,71 | 0,59–0,80 | 0,31–0,50 |

- **Duración:** la canción dura 3:53. A ese tempo caben unas cuatro sevillanas seguidas, así que esta también lleva cuatro, con la misma música y una copla distinta en cada una.

## Forma de cada sevillana

Una sevillana tiene siempre la misma medida, porque cada parte del baile cae en un sitio fijo de la música:

| Compases | Parte | Qué canta | Qué suena |
|---|---|---|---|
| 1–7 | **Introducción** (7) | — | Falseta flamenca de la guitarra 2 sobre la cadencia andaluza (Lam – Sol – Fa – Mi) que desemboca en el Mi mayor del cante. **El primer tiempo calla**, como es costumbre. |
| 8–13 | **Salida** (6) | Versos 1-2 | La voz casi sola. La guitarra solo marca el 1 y el 3, sin palmas. |
| 14–25 | **Primer tercio** (12) | Versos 1-2-3-4 | El compás completo: las dos guitarras, tamboril y palmas. La gaita dobla el cante. |
| 26–27 | **Pasada** (2) | — | Cadencia frigia Fa – Mi con rasgueo fuerte, gaita, bandurria y tamboril. En la 3.ª y la 4.ª, también trompetas. |
| 28–39 | **Segundo tercio** (12) | Versos 3-4-3-4 | Como el primero, pero la segunda mitad sube. |
| 40–41 | **Pasada** (2) | — | Igual que la primera. |
| 42–50 | **Tercer tercio** (9) | Estribillo 5-6-7 | El estribillo. |
| 51 | **Parada** | — | Golpe seco de todos en el 1 y silencio, para el «bien parado». |

Cada verso dura 3 compases. La sílaba acentuada cae siempre en un primer tiempo: «Ten-go‿un cas-co de **PLA**-ta».

### El arreglo crece de una sevillana a otra

| Sevillana | Qué suena |
|---|---|
| 1.ª | Gaita con el cante, tamboril, dos guitarras y palmas. Pandereta y castañuelas en las pasadas y el estribillo. |
| 2.ª | Se añaden la segunda voz, la bandurria doblando el cante desde el segundo tercio y la pandereta en todo el compás. |
| 3.ª | Igual, y las trompetas entran en las pasadas. |
| 4.ª | Todo junto: la bandurria dobla el cante desde el primer tercio. |

## El compás: 3/4 con aire de 6/8

Se cuenta de tres en tres, con el acento fuerte siempre en el 1: **¡UN!**-dos-tres, **¡UN!**-dos-tres. La guitarra alterna dos formas de repartir las seis corcheas del compás:

```
corchea:            1      y      2      y      3      y
3/4 (¡UN!-dos-tres) GOLPE  arriba abajo  arriba ABAJO  arriba
6/8 (¡UN!-y-dos ¡Y!-tres-y)
                    GOLPE  arriba abajo  GOLPE  arriba abajo
```

- **En qué compases va a 6/8:**
  - el del medio de cada verso;
  - el primero de cada pasada;
  - el penúltimo de la introducción.
- **El cruce de ritmos:** en esos compases las palmas siguen en 3/4 mientras la guitarra y las castañuelas se van al 6/8. Se cruzan dos ritmos, que es lo que le da a la sevillana su aire alegre.
- **Sonido flamenco:**
  - abanico rápido que acaba justo en el 1;
  - golpe con el anular en la tapa de la guitarra en el 1 (y en el «y» del 2 en los compases de 6/8);
  - remate seco en el 3 al final de cada verso.
- **Las frases se marcan solas:** cada verso dura 3 compases (3/4, 6/8 y remate), así que el baile sabe siempre dónde está.
- **Comprobado en la grabación:** midiendo la fuerza de cada corchea, el 1 es el golpe más fuerte en todos los compases. En los de 6/8, el segundo acento de la guitarra cae en el «y» del 2.

## Armonía

```
Introducción   | Am | G | F | E | Am | F | E |      (cadencia andaluza)
Salida         | E | E | B7 | B7 | B7 | E |
Tercios 1 y 2  | E | E | A | B7 | B7 | E | A | B7 | E | C | B7 | E |
Tercer tercio  | A | C | B7 | E | A | B7 | F#m7 | B7 | E |  ‖ E (parada)
Pasadas        | F | E |                                  (cadencia frigia)
```

El cante va en la armonía mayor de las sevillanas rocieras: tónica, dominante y subdominante. La introducción y las pasadas le dan el color flamenco con la cadencia andaluza y la frigia, que caen en el mismo acorde de Mi. El color propio lo pone el **Do mayor** (♭VI). Aparece en el último verso de cada tercio y al empezar el estribillo, y le da un tono más oscuro antes de volver a Mi.

## Letra

Son cuatro seguidillas de 7-5-7-5 sílabas con estribillo de 5-7-5, una por sevillana. Cada una se reparte así:

- **Salida:** versos 1-2.
- **Primer tercio:** versos 1-2-3-4.
- **Segundo tercio:** versos 3-4-3-4.
- **Tercer tercio:** estribillo.

**1.ª**
> Agua de madrugada / sobre la brasa, / lo que el fuego levanta / el agua, en calma.
> *Sirena y agua, / que entre el humo y la noche / despunta el alba.*

**2.ª**
> Tengo un casco de plata / y una escalera / para subir al cielo / cuando tú quieras.
> *Que no hay candela / que me queme por dentro / como tu ausencia.*

**3.ª**
> Sevilla tiene un río / que no se apaga, / y un fuego en cada patio / que el agua guarda.
> *Candela y agua, / mi Sevilla es un cante / que nunca acaba.*

**4.ª**
> Cuando apague la noche / la última llama, / vendré por la ribera / con la mañana.
> *Agua que canta, / candela que se enciende / cuando tú bailas.*

## La versión cantada

La genera `cantar.py` con MBROLA, un sintetizador de voz al que se le dan los sonidos de la letra con su nota y su duración exactas:

- **Pronunciación:** cada sílaba de la partitura se pasa a fonemas en castellano con seseo, como se canta en Sevilla («can-de-la» → *k a n · d e · l a*, «cie-lo» → *s je · l o*).
- **Consonantes:** las del ataque entran justo antes del tiempo, como hace un cantaor, para que la vocal caiga en su sitio.
- **Vocales:** sostienen la nota con un vibrato que entra poco a poco. Los melismas son cambios de altura dentro de la misma vocal.
- **Sinalefas:** «go‿un», «na‿es» se cantan como una sola sílaba que se desliza de una vocal a otra.
- **Voces:**
  - el solista (voz `es2`) canta la melodía;
  - la segunda voz (voz `es4`) le hace terceras por debajo, en el estribillo de la 1.ª sevillana y en las tres siguientes enteras.
- **Jaleos:** «¡Olé!» tras cada parada, «¡Arsa!» y «¡Eso es!» en las pasadas, y «¡Vamos allá!» antes de la cuarta, con una tercera voz (`es1`).
- **Mezcla:** el coro de «aah» desaparece, la gaita baja un poco para dejar sitio a la voz, y las voces llevan algo de eco de sala.

## Para llevarla a un grupo de verdad

- La voz cantada es sintética: se entiende la letra y va afinada y a tiempo, pero suena a máquina. Sirve de guía para que un cantaor la aprenda. Para la versión final hace falta grabar a un cantaor.
- La melodía suena una octava más baja de lo escrito, para tenor. Para otra voz, transpón todo con el programa de música.
