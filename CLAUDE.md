# CLAUDE.md

Contexto para trabajar en este repositorio. Responde siempre en español.

## Qué es

Planificador semanal de estudio y entrenamiento para Guillermo, opositor a Bombero del Ayuntamiento de Sevilla. Él indica las horas de estudio de cada día y la app reparte el tiempo entre materias y entrenos.

## Archivos

- `src/app.html`: el código fuente. Es una sola página (HTML + CSS + JS sin librerías) escrita sin `<!doctype>`, `<html>`, `<head>` ni `<body>`, porque también se publica como artifact de Claude, que añade esa cabecera.
- `index.html`: la misma página con la cabecera HTML completa (manifiesto, iconos y metas para instalarla en la pantalla de inicio), para abrirla en el navegador o en GitHub Pages. **Se genera desde `src/app.html`; no la edites a mano.** Después de cambiar `src/app.html`, regénerala con `./build.sh`.
- `manifest.webmanifest` e `icons/`: nombre, colores e iconos de la app instalada. Los iconos salen del logo de Guillermo (escudo con hacha y ola). El logo de la cabecera va dentro de `src/app.html` como `data:` WebP, porque el artifact no puede cargar imágenes externas.
- `const VERSION` en `src/app.html`: súbela (fecha + número) en cada cambio que se publique. La app instalada la compara con la del servidor al abrirse y se recarga si hay otra, porque GitHub Pages deja la página 10 min en caché.
- `README.md`: descripción para el usuario. Mantenlo al día si cambia el funcionamiento.

## Datos

- Todo se guarda en `localStorage` con la clave `parte-semanal-v1`. El objeto lleva un campo `v` (ahora `15`).
- Si cambias la forma de los datos, sube `v` y añade una migración desde la versión anterior que conserve lo que el usuario ya ha configurado (días, bloques fijos, temas marcados).
- Envuelve cada lectura y escritura de `localStorage` en `try/catch`.

## Contenido de la oposición (Decreto 36/2025, de 11 de febrero, Andalucía)

- **Temario (Anexo I):** 12 temas generales, 33 específicos y 5 propios del servicio que convoca. Los 5 de Sevilla aún dependen de las bases, así que están como huecos con el texto «según bases».
- **Pruebas físicas (Anexo III):** cada una se puntúa de 0 a 10 y hay que sacar al menos un 5 en todas. Marcas para hombres:

| Prueba | Para un 5 | Para un 10 |
|---|---|---|
| Dominadas | 12 rep | 30 rep |
| 100 m lisos | 14,50 s | 12,20 s |
| 1500 m | 6:06 | 4:32 |
| 100 m natación | 1:50 | 1:18 |

Estas marcas salen de resúmenes de academias, no del BOJA original. Si el usuario aporta el anexo oficial, corrígelas.

## Reglas del organizador

- **Un día sin horas de estudio no se organiza**: ni estudio ni entrenos, solo el rato diario de callejero. Las horas empiezan vacías y solo las pone el usuario.
- **Propios de Sevilla fuera por ahora**: con `S.sevOn` en `false` (por defecto) la materia `sev` no entra en el reparto. En Ajustes, «Incluir en la semana» la activa con su peso.
- El estudio va en bloques (50 min + 10 de pausa por defecto) y alterna materias según su peso: Generales 2, Específicos 3, Propios de Sevilla 1, Test y repaso 1. El reparto se equilibra en toda la semana.
- Cada bloque de estudio toma el siguiente tema pendiente de su materia. Si el usuario fija cuántos temas quiere estudiar ese día (`days[i].topics`), el tiempo del día se reparte entre esos temas (mínimo 15 min cada uno) y un tema puede ocupar varios bloques seguidos; vacío (`null`) = un tema por bloque. Con 2 temas, uno es de Generales y otro de Específicos (el más atrasado de los dos va primero).
- **Callejero de Sevilla**: materia `cal` de tipo `daily`, fuera del reparto por pesos. Va **todos los días**, automáticamente. En días con horas se lleva `S.calPct` % del estudio (25 % por defecto: de 4 h, 1 h de callejero y 3 h para lo demás) y abre la primera sesión; en días sin horas va solo, `S.calFree` minutos (60 por defecto). Con `S.calWeekly` (por defecto) va **el mismo distrito toda la semana**: la semana N desde `S.calStart` toma el puesto N de `S.topics.cal`, saltando los marcados como hechos, así que «Cambiar» en un bloque de callejero cambia el distrito de toda la semana. Sin `calWeekly`, cada día toma el siguiente distrito pendiente (11 distritos, rondas y avenidas, edificios singulares). Si dura más de un bloque se parte en bloques iguales; si están todos hechos, «Repaso general del callejero». No cuenta como tema del día.
- **Mañana y tarde**: cada día tiene hora de inicio de mañana (`am`, 09:00 entre semana y 10:00 el fin de semana) y de tarde (`pm`, 16:30 y 17:00). Vacía = no se estudia en esa franja. Con 2 h o más y las dos franjas, la mitad del estudio va por la mañana (sin pasar de las 14:00, hora de comer) y el resto por la tarde; con menos de 2 h, todo por la tarde. Natación y dominadas «antes» van al principio de la primera sesión y «después» al final de la última.
- Entrenos por defecto (lo pidió Guillermo: 2 días de CrossFit, 3 de carrera, 1 de natación y 2 de dominadas): natación 1×45 min, carrera 1500 m 2×40, velocidad 100 m 1×35 (1500 m + 100 m = 3 días de carrera), dominadas 2×20.
- **Cambiar entreno**: «Cambiar» en un entreno no hecho deja elegir otro. Se guarda el reparto de esa semana en `S.trainPlan[semana]` (array de 7 días con ids): el día pasa a tener el elegido y el día más cercano que lo tenía recibe el anterior. `generate` usa ese reparto en vez de `assignTraining()`. Se borra (`resetTrainPlan`) al cambiar sesiones o minutos de entrenos, días sin entreno o bloques fijos.
- Dominadas, 1500 m y 100 m nunca van en días seguidos, y se evita juntar 1500 m y 100 m el mismo día. Como máximo hay 2 entrenos por día, con 15 min de margen tras entrenar (también tras el CrossFit). Ningún entreno acaba después de las 23:30.
- **CrossFit: lunes y miércoles de 20:00 a 21:00**, como bloque fijo. Esos días no se añade ningún otro entreno (si no cabe, se avisa de las sesiones que faltan).
- Se evita correr (1500 m o 100 m) dos días seguidos.
- Carrera y 100 m son al aire libre y nunca van a mediodía por el calor de Sevilla. Por defecto van temprano (`morningAt`, 07:30) si terminan con 15 min de margen antes de la primera sesión de estudio; si no, o si el usuario elige `outdoor: "evening"`, van por la noche: no antes de las 21:00 de junio a septiembre, 20:00 en mayo y octubre, 19:00 el resto del año. Natación y dominadas siguen `trainPos` (antes o después del estudio).
- **Cambiar tema**: en un bloque de estudio no hecho, «Cambiar» abre la lista de temas pendientes de esa materia. Al elegir uno se intercambian los dos en el orden de `S.topics[materia]` y se regenera la semana: el elegido queda en ese bloque y el anterior pasa al sitio que tenía el elegido.
- **Técnicas de estudio**: pinchar en un bloque de estudio (fuera de «Cambiar» y del círculo) abre `#techSheet` con técnicas según la materia (`TECH.general`, `TECH.test`, `TECH.cal`). El Pomodoro va primero: `S.pomo` guarda los minutos de estudio y descanso (25/5) para todos los bloques, se muestra el reparto del bloque y hay temporizador (un solo pomodoro activo, sigue en una píldora flotante al cerrar la hoja). No cambia el plan de la semana.
- **Juego «Mi parque de bomberos»**: vista aparte en `#parque` (el planificador es `#viewPlan`, el juego `#viewGame`; se entra por la tarjeta `#gameCard`). Datos en `S.game` = {min, spent, owned, claimed, manual, log}. Monedas = `floor(min/6) - spent` (10 por hora). Por reclamar: bloques de estudio hechos de cualquier semana cuya clave `semana|día|materia|tema|parte` no esté en `claimed`, más el estudio añadido a mano sin reclamar. `SHOP` tiene 19 mejoras (10–200 monedas); todo pide antes la obra del parque. «Mi parque» es una escena 3D con Three.js r128 (cdnjs) y OrbitControls (jsDelivr), cargados solo al abrir esa pestaña (`load3D`, `buildPark`): edificio sin techo con cocheras (BUL, BUP, autoescala y rescate dentro), cocina, dormitorios, gimnasio y cuarto de EPI; fuera torre, dron, piscina, helipuerto, NRBQ, bandera, árboles y farolas. Solo se pone lo comprado, lo nuevo aparece con animación, colores de las variables CSS (`--sky`, `--brick`…; en oscuro es de noche con luces). Botones «Vista 3D» y «Desde arriba». Si Three.js no carga (sin conexión o sin WebGL) se usa el dibujo plano `sceneSVG()`. Rangos en `RANKS` según monedas invertidas. `freshGame()` deja el juego a cero y marca como reclamados los bloques ya hechos (lo usa «Reiniciar el juego» en Registrar y la migración v13 → v14, que reinició el juego tras las compras de prueba de Guillermo).
- **Clases de la oposición**: por semana, porque los días cambian: `S.classes[semana][día] = {start, end}` (17:00–19:00 al añadir). En `generate` la clase es un bloque `type:"class"` (`subj:"clase"`) que además se añade a los fijos del día con 10 min de margen después. Si la clase cae por la tarde, la mañana se lleva lo que no quepa en la tarde antes de las 21:00. Se marca como hecha y da monedas en el juego como el estudio.
- Nunca se coloca nada encima de un bloque fijo.
- Cualquier cambio reorganiza al momento la semana visible (y las futuras ya generadas). Se conservan los bloques ya marcados como hechos: se reconocen por día, materia, tema y parte, no por la hora.

## Estilo

- Una sola página sin pestañas: cabecera con la semana, balance, una tarjeta por día (horas y temas con botones − / + dentro de la propia tarjeta) y, al final, «Temario» y «Ajustes» como secciones plegables.
- Pensada sobre todo para el móvil: debe funcionar a 400 px de ancho sin scroll horizontal.
- Tema claro y oscuro con variables CSS en `:root`. Azul marino y amarillo reflectante (franja de alta visibilidad en la cabecera). Fuentes Archivo (títulos), Public Sans (texto) y JetBrains Mono (horas). Los colores de cada materia se guardan en los datos como nombre de variable (`--c-leg`, `--c-esp`, `--c-fix`, `--c-test`, `--c-nat`, `--c-car`, `--signal`, `--c-dom`): no los renombres.
- En los bloques de estudio manda el tema que toca (texto grande); la materia va encima en pequeño y en mayúsculas. En los entrenos y bloques fijos el nombre sigue siendo lo principal.
- Textos de la interfaz en español, claros y directos.

## Comprobar

No hay tests. Antes de subir cambios, ejecuta el script y comprueba que la semana generada es coherente. Por ejemplo, carga la lógica en Node con un DOM mínimo de pega, pon horas a varios días e imprime los bloques.
