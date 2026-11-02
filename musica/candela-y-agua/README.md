# «Candela y agua» — sevillana

Una sevillana original. Toma de Los Romeros de la Puebla la idea de fondo: guitarra rasgueada con aire rociero, palmas, coros en terceras y una letra de copla que se canta. La música no copia ninguna de sus sevillanas, ni en la armonía, ni en la melodía, ni en la forma.

| Archivo | Para qué sirve |
|---|---|
| `candela-y-agua.mp3` | Para escucharla. Es una maqueta sintetizada (1:50). |
| `candela-y-agua.musicxml` | La partitura: voz con letra y cifrado, segunda voz y flauta. Se abre con MuseScore, Finale, Sibelius o Dorico. |
| `candela-y-agua.mid` | Una pista por instrumento, con la letra incluida. Sirve para GarageBand, Logic, Cubase, etc. |
| `componer.py` | El script que genera los tres archivos anteriores con `python3 componer.py`. Solo necesita numpy. |

## Ficha

- **Compás:** 3/4, a ♩ = 190. Cada copla se baila con su remate.
- **Tonalidad:** Re mayor. La tercera copla sube un tono, a Mi mayor.
- **Instrumentos:** voz solista (tenor), segunda voz, guitarra flamenca, flauta travesera, bandurria en trémolo, violonchelo, contrabajo, cajón, palmas (sordas, claras y a contratiempo) y castañuelas.

## Forma

| Compases | Sección | Qué pasa |
|---|---|---|
| 1–12 | **Introducción** | La guitarra arpegia sola sobre un pedal de Re (D – E/D) con color **lidio** (el Sol♯). En el compás 5 entra la flauta con el tema y en el 9 la bandurria, las castañuelas y las palmas. |
| 13–16 | **Salida** | Un «¡Ay!» melismático de la voz, con la guitarra. |
| 17–42 | **Copla 1** | Voz sola, guitarra, contrabajo, violonchelo y palmas sordas. Los rellenos son punteos de guitarra. |
| 43–50 | **Pasada** | La flauta toma el tema una octava más arriba, doblada por la bandurria. Entra el cajón. |
| 51–76 | **Copla 2** | Palmas claras. En el estribillo entran la segunda voz y el contracanto largo de la flauta. |
| 77–84 | **Pasada que modula** | Es el mismo tema, pero el último compás va a Si7 para llevar a Mi. |
| 85–110 | **Copla 3 (en Mi)** | Todo el grupo: dos voces de principio a fin, palmas a contratiempo y castañuelas en el estribillo. |
| 111–113 | **Remate** | C – B7 – E. Corte seco en el primer tiempo, como se para el baile. |

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
4. **La instrumentación** no es la del grupo: la flauta y la bandurria en trémolo llevan el tema, el violonchelo hace un contracanto grave y el cajón no entra hasta la segunda copla. La copla 1 es casi desnuda y la 3 suena con todo el grupo.
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

- La maqueta está hecha con síntesis, sin muestras de instrumentos reales, así que las voces son una aproximación. Sirve para oír la forma, la armonía y los arreglos. Para una versión final, carga el MIDI en tu programa de música con buenos instrumentos virtuales o dale la partitura a los músicos.
- La tonalidad está pensada para tenor. Para otra voz, transpón todo con el programa o cambia en `componer.py` el transporte de cada copla (`(S_C1, 0), (S_C2, 0), (S_C3, 2)`).
