# PLANIFICADOR-SEMANAL

Planificador semanal de estudio y entrenamiento pensado para la oposición de Bombero del Ayuntamiento de Sevilla. Indicas cuánto tiempo tienes cada día, qué tienes que estudiar y qué entrenamientos hacer, y la app organiza la semana por ti.

## Cómo se usa

Abre `index.html` en el navegador (o actívalo en GitHub Pages: *Settings → Pages → Deploy from branch → main / root*). Todo se guarda en el propio navegador.

Es una sola página, sin pestañas:

- **La semana**: una tarjeta por día. Con los botones − y + pones las horas de estudio y cuántos temas quieres ver ese día, y debajo a qué hora empiezas por la mañana y por la tarde («Auto» = un tema por bloque). La semana se reorganiza sola al cambiar algo y conserva los bloques ya marcados como hechos. Un día sin horas solo lleva el callejero.
- **Técnicas de estudio**: al pinchar en un bloque de estudio se abre una hoja con técnicas para ese tema (recuerdo activo, Feynman, esquema, repaso espaciado; mapa en blanco y rutas para el callejero; simulacro y cuaderno de fallos para los test). La primera es el **Pomodoro**: ajustas los minutos de estudio y de descanso (25/5 por defecto), ves cómo queda repartido el bloque y tienes un temporizador con aviso sonoro.
- **Cambiar entreno**: en cada entreno pulsa «Cambiar» y elige otro. Ese día pasa a tener el elegido y el día que lo tenía recibe el que había. Al tocar las sesiones, los días sin entreno o los bloques fijos se vuelve al reparto automático.
- **Cambiar tema**: en cada bloque de estudio pulsa «Cambiar» y elige otro tema pendiente de esa materia. El elegido ocupa ese hueco y el que había pasa al sitio donde estaba el elegido; la semana se reorganiza sola. También sirve para el callejero.
- **Mi parque de bomberos** (juego): desde la tarjeta del planificador. Cada bloque de estudio que marcas como hecho da monedas: **10 por hora** (2 h = 20 monedas).
  - **Registrar**: reclamas las monedas de los bloques hechos y puedes añadir a mano el estudio que hagas fuera del plan. Al final está «Reiniciar el juego» para empezar de cero (lo ya estudiado no vuelve a dar monedas).
  - **Tienda**: 19 mejoras, de 10 a 200 monedas según su importancia. Primero la obra del parque (20); después mangueras, gimnasio, cocina, dormitorios, torre de prácticas, piscina, vehículos (BUL, BUP, autoescala, rescate, NRBQ), dron, helipuerto…
  - **Mi parque**: el dibujo de tu parque con todo lo que has comprado (de noche en el tema oscuro) y tu rango, de Aspirante a Jefe de parque.
- **Temario** (plegable): el de Bombero del Decreto 36/2025, de 11 de febrero (Anexo I): 12 temas generales, 33 específicos y 5 propios del SPEIS de Sevilla (fuera de la semana hasta que salgan las bases; se activan en Ajustes → Temas propios de Sevilla → «Incluir en la semana»), más bloques de test y repaso y el callejero de Sevilla por distritos. Marca los temas terminados o añade los tuyos.
- **Ajustes** (plegable): sesiones y minutos de las cuatro pruebas físicas (por defecto: carrera 3 días, 2 de 1500 m y 1 de 100 m; natación 1; dominadas 2; más los 2 de CrossFit) del Anexo III (dominadas, 100 m lisos, 1500 m y 100 m natación, con las marcas del 5 y del 10), días sin entreno, entreno antes o después del estudio, cuándo correr (temprano o por la noche), peso de cada materia, duración de bloques y pausas, y bloques fijos (CrossFit lunes y miércoles de 20:00 a 21:00 ya viene cargado).

## Cómo organiza la semana

- **Todos los días** hay **callejero de Sevilla**. En los días con horas de estudio se lleva una cuarta parte (de 4 h, 1 h de callejero y 3 h para lo demás) y abre la mañana; en los días sin horas va solo 1 h. Recorre los 11 distritos, las rondas y avenidas y los edificios clave: por defecto **un mismo distrito toda la semana** y el siguiente la semana después (en Ajustes se puede cambiar a uno distinto cada día). Se ajusta en Ajustes.
- El estudio se reparte **entre mañana y tarde**: cada día tiene su hora de empezar por la mañana y por la tarde (déjala vacía si esa franja no puedes). Con 2 h o más, la mitad va por la mañana (hasta las 14:00) y el resto por la tarde.
- Reparte el estudio en bloques (50 min + 10 de pausa por defecto) alternando materias según su peso, con el reparto equilibrado en toda la semana.
- Si indicas cuántos temas quieres estudiar un día, reparte ese tiempo a partes iguales entre esos temas (mínimo 15 min por tema); si lo dejas vacío, cada bloque es un tema nuevo.
- Con 2 temas en un día, uno es de Generales (legislación) y el otro de Específicos.
- No coloca entrenos que acaben más tarde de las 23:30.
- Coloca los entrenos evitando repetir dominadas, 1500 m o 100 m en días seguidos y sin correr dos días seguidos.
- Los días de CrossFit no añade ningún otro entreno.
- Carrera y 100 m (al aire libre) nunca van a mediodía: temprano (07:30 por defecto, si terminas antes de empezar a estudiar) o por la noche, no antes de las 21:00 de junio a septiembre, las 20:00 en mayo y octubre y las 19:00 el resto del año. Natación y dominadas van antes o después del estudio.
- Nunca pone nada encima de un bloque fijo y deja 15 min de margen tras entrenar (también después del CrossFit).
- Si los entrenos no caben en los días con tiempo, el balance de la semana avisa de cuántas sesiones faltan.

## Instalarla en el móvil

Con la web publicada en GitHub Pages, ábrela en el móvil y:

- **iPhone (Safari):** Compartir → «Añadir a pantalla de inicio».
- **Android (Chrome):** menú ⋮ → «Instalar aplicación» o «Añadir a pantalla de inicio».

Aparece como «Mi semana» con su logo y se abre a pantalla completa.

El código está en `src/app.html`; `index.html` se genera con `./build.sh` y lleva la cabecera HTML completa, el manifiesto y los iconos.
