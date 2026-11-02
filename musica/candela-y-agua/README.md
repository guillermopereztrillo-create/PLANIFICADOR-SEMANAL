# «Candela y agua» — sevillanas

Cuatro sevillanas rocieras originales para bailar, en la línea de Los Romeros de la Puebla y Brisa de la Puebla. Llevan dos guitarras rasgueadas, gaita rociera con tamboril, bandurria en trémolo, pandereta, palmas, castañuelas y coro. La melodía, la armonía y la letra son nuevas.

| Archivo | Para qué sirve |
|---|---|
| `candela-y-agua.mp3` | Para escucharla (3:34). Maqueta con instrumentos sampleados (banco de sonidos MuseScore General). |
| `candela-y-agua.musicxml` | La partitura: voz con letra y cifrado, segunda voz, gaita rociera y dos trompetas. Se abre con MuseScore, Finale, Sibelius o Dorico. |
| `candela-y-agua.mid` | Una pista por instrumento, con la letra incluida. Sirve para GarageBand, Logic, Cubase, etc. |
| `componer.py` | El script que genera los tres archivos anteriores con `python3 componer.py`. Para el audio necesita `fluidsynth`, `ffmpeg` y el banco de sonidos MuseScore General (paquete `musescore-general-soundfont-lossless`). |

## Ficha

- **Compás:** 3/4 con el acento en el 1, a ♩ = 174.
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
| 1–7 | **Introducción** (7) | — | La guitarra rasguea y la gaita y la guitarra 2 tocan el tema. **El primer tiempo calla**, como es costumbre. |
| 8–13 | **Salida** (6) | Versos 1-2 | La voz casi sola. La guitarra solo marca el 1 y el 3, sin palmas. |
| 14–25 | **Primer tercio** (12) | Versos 1-2-3-4 | El compás completo: las dos guitarras, tamboril y palmas. La gaita dobla el cante. |
| 26–27 | **Pasada** (2) | — | Rasgueo fuerte, gaita, bandurria y tamboril. En la 3.ª y la 4.ª, también trompetas. |
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

## El compás de la guitarra

```
corchea:   1        y      2      y      3      y
          GOLPE   arriba  abajo  ARRIBA  ABAJO  arriba
          (abanico que acaba en el 1)
```

- Al final de cada verso se quita el último «y» y el 3 queda seco, como remate.
- Las palmas marcan sobre todo el 1, más suave el 3 y muy poco el 2.
- Las castañuelas hacen la carretilla que llega al 1 y luego tocan el «y» del 2 y el 3.

## Armonía

```
Introducción   | E | E | A | B7 | E | B7 | B7 |
Salida         | E | E | B7 | B7 | B7 | E |
Tercios 1 y 2  | E | E | A | B7 | B7 | E | A | B7 | E | C | B7 | E |
Tercer tercio  | A | C | B7 | E | A | B7 | F#m7 | B7 | E |  ‖ E (parada)
```

Es la armonía de las sevillanas rocieras: tónica, dominante y subdominante. El color propio lo pone el **Do mayor** (♭VI). Aparece en el último verso de cada tercio y al empezar el estribillo, y le da un tono más oscuro antes de volver a Mi.

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

## Para llevarla a un grupo de verdad

- La maqueta usa instrumentos grabados, pero la voz es un coro sampleado que canta «aah»: ningún banco de sonidos puede cantar la letra. Para la versión final hace falta un cantaor, o cargar la pista de voz del MIDI en un programa de voz sintética.
- La melodía suena una octava más baja de lo escrito, para tenor. Para otra voz, transpón todo con el programa de música.
