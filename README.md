# PLANIFICADOR-SEMANAL

Planificador semanal de estudio y entrenamiento pensado para la oposición de Bombero del Ayuntamiento de Sevilla. Indicas cuánto tiempo tienes cada día, qué tienes que estudiar y qué entrenamientos hacer, y la app organiza la semana por ti.

## Cómo se usa

Abre `index.html` en el navegador (o actívalo en GitHub Pages: *Settings → Pages → Deploy from branch → main / root*). Todo se guarda en el propio navegador.

Es una sola página, sin pestañas:

- **La semana**: una tarjeta por día. Con los botones − y + pones las horas de estudio y cuántos temas quieres ver ese día («Auto» = un tema por bloque). La semana se reorganiza sola al cambiar algo y conserva los bloques ya marcados como hechos. Un día sin horas no se organiza.
- **Temario** (plegable): el de Bombero del Decreto 36/2025, de 11 de febrero (Anexo I): 12 temas generales, 33 específicos y 5 propios del SPEIS de Sevilla, más bloques de test y repaso. Marca los temas terminados o añade los tuyos.
- **Ajustes** (plegable): sesiones y minutos de las cuatro pruebas físicas del Anexo III (dominadas, 100 m lisos, 1500 m y 100 m natación, con las marcas del 5 y del 10), días sin entreno, entreno antes o después del estudio, cuándo correr (temprano o por la noche), peso de cada materia, duración de bloques y pausas, y bloques fijos (CrossFit lunes y miércoles de 20:00 a 21:00 ya viene cargado).

## Cómo organiza la semana

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
