# «Candela y agua» — sevillana

Una sevillana original para bailar, en la línea de las sevillanas rocieras de Los Romeros de la Puebla y Brisa de la Puebla: guitarras rasgueadas, palmas, castañuelas y coro, con gaita rociera y trompetas. La melodía, la armonía y la letra son nuevas.

| Archivo | Para qué sirve |
|---|---|
| `candela-y-agua.mp3` | Para escucharla (48 s, una sevillana completa). Maqueta con instrumentos sampleados (banco de sonidos MuseScore General). |
| `candela-y-agua.musicxml` | La partitura: voz con letra y cifrado, segunda voz, gaita rociera y dos trompetas. Se abre con MuseScore, Finale, Sibelius o Dorico. |
| `candela-y-agua.mid` | Una pista por instrumento, con la letra incluida. Sirve para GarageBand, Logic, Cubase, etc. |
| `componer.py` | El script que genera los tres archivos anteriores con `python3 componer.py`. Para el audio necesita `fluidsynth`, `ffmpeg` y el banco de sonidos MuseScore General (paquete `musescore-general-soundfont-lossless`). |

## Ficha

- **Compás:** 3/4 con el acento en el 1, a ♩ = 192.
- **Tonalidad:** Re mayor.
- **Instrumentos:** voz y segunda voz (coro), dos guitarras flamencas, gaita rociera con tamboril, dos trompetas, mandolina, cuerdas, violonchelo, contrabajo, palmas y castañuelas.

## Forma: la de la sevillana para bailar

Una sevillana tiene siempre la misma medida, porque cada parte del baile cae en un sitio fijo de la música. Esta sigue esa medida al compás:

| Compases | Parte | Qué canta | Qué suena |
|---|---|---|---|
| 1–7 | **Introducción** (7) | — | Guitarra rasgueada, gaita y guitarra 2 con el tema, palmas, castañuelas y tamboril. **El primer tiempo calla**, como es costumbre. |
| 8–13 | **Salida** (6) | Versos 1-2 | La voz casi sola. La guitarra solo marca el 1 y el 3, sin palmas. |
| 14–25 | **Primer tercio** (12) | Versos 1-2-3-4 | Entra el compás completo: guitarra 1 rasgueando, guitarra 2 contestando en el 2 y el 3, palmas y contrabajo. |
| 26–27 | **Pasada** (2) | — | Trompetas en terceras, castañuelas y tamboril. |
| 28–39 | **Segundo tercio** (12) | Versos 3-4-3-4 | Igual que el primero, pero la segunda mitad sube. Entran la segunda voz y las cuerdas. |
| 40–41 | **Pasada** (2) | — | Como la primera, más fuerte. |
| 42–50 | **Tercer tercio** (9) | Estribillo 5-6-7 | Todo el grupo. Las trompetas doblan el cante en los dos últimos versos. |
| 51 | **Parada** | — | Golpe seco de todos en el 1 y silencio, para el «bien parado». |

Introducción aparte, son 44 compases: los 43 de la copla y el de la parada final. Cada verso dura 3 compases. La sílaba acentuada cae siempre en un primer tiempo: «Ten-go‿un cas-co de **PLA**-ta», «y‿u-na‿es-ca-**LE**-ra».

Una sevillana sola dura menos de un minuto. Para bailar se tocan cuatro seguidas («las cuatro sevillanas»). Esta sería la primera.

## El compás de la guitarra

Cada compás de la guitarra 1 se toca así:

```
tiempo:     1          2     y     3     y
          ABANICO→GOLPE  abajo arriba abajo arriba
```

- El abanico rápido termina justo **en** el 1, así que el golpe cae a tiempo.
- Al final de cada verso, el 3 es un remate seco.
- La guitarra 2 deja el 1 libre y contesta en el 2 y el 3, con acordes agudos.
- Las palmas van en los tres tiempos con el acento en el 1. Hay dos palmeros, uno muy poco detrás del otro.
- Las castañuelas hacen la carretilla que llega al 1 y luego tocan el 2 y el 3.

## Armonía

```
Introducción   | D | D | G | A7 | D | A7 | A7 |
Salida         | D | D | A7 | A7 | A7 | D |
Tercios 1 y 2  | D | D | G | A7 | A7 | D | G | A7 | D | Bb | A7 | D |
Tercer tercio  | G | Bb | A7 | D | G | A7 | Em7 | A7 | D |  ‖ D (parada)
```

La armonía es la de las sevillanas rocieras: tónica y dominante, con la subdominante al empezar cada verso. El color propio lo pone el **Si♭ mayor** (♭VI). Aparece en el último verso de cada tercio y al empezar el estribillo, y le da un tono más oscuro y nostálgico antes de volver a Re.

## Letra

Es una seguidilla de 7-5-7-5 sílabas con estribillo de 5-7-5 (la sinalefa se marca con «‿»):

> Tengo un casco de plata
> y una escalera
> para subir al cielo
> cuando tú quieras.
> *Que no hay candela*
> *que me queme por dentro*
> *como tu ausencia.*

Cómo se reparte al cantarla:
- **Salida:** versos 1-2.
- **Primer tercio:** versos 1-2-3-4.
- **Segundo tercio:** versos 3-4-3-4.
- **Tercer tercio:** estribillo.

## Para llevarla a un grupo de verdad

- La maqueta usa instrumentos grabados, pero la voz es un coro sampleado que canta «aah»: ningún banco de sonidos puede cantar la letra. Para la versión final hace falta un cantaor, o cargar la pista de voz del MIDI en un programa de voz sintética.
- La tonalidad está pensada para tenor (la melodía suena una octava más baja de lo escrito). Para otra voz, transpón todo con el programa de música.
