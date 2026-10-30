# PLANIFICADOR-SEMANAL

Planificador semanal de estudio y entrenamiento pensado para la oposición de Bombero del Ayuntamiento de Sevilla. Indicas cuánto tiempo tienes cada día, qué tienes que estudiar y qué entrenamientos hacer, y la app organiza la semana por ti.

## Cómo se usa

Abre `index.html` en el navegador (o actívalo en GitHub Pages: *Settings → Pages → Deploy from branch → main / root*). Todo se guarda en el propio navegador.

- **Semana**: línea de tiempo de cada día con sus bloques. Marca cada bloque al terminarlo y el balance de la semana se actualiza.
- **Temario**: el de Bombero del Decreto 36/2025, de 11 de febrero (Anexo I): 12 temas generales, 33 específicos y 5 propios del SPEIS de Sevilla (se renombran cuando salgan las bases), más bloques de test y repaso. Cada bloque de estudio toma el siguiente tema pendiente.
- **Ajustes**: hora de inicio y horas de estudio por día, sesiones y minutos de las cuatro pruebas físicas del Anexo III (dominadas, 100 m lisos, 1500 m y 100 m natación, con las marcas del 5 y del 10), peso de cada materia, duración de bloques y pausas, y bloques fijos (CrossFit lunes y miércoles de 20:00 a 21:00 ya viene cargado). Un día sin horas de estudio no se organiza.

## Cómo organiza la semana

- Reparte el estudio en bloques (50 min + 10 de pausa por defecto) alternando materias según su peso, con el reparto equilibrado en toda la semana.
- Coloca los entrenos evitando repetir dominadas, 1500 m o 100 m en días seguidos, sin dominadas los días de CrossFit y con natación como descarga.
- Los días de CrossFit no añade otro entreno salvo que no quepa en el resto de la semana.
- Nunca pone nada encima de un bloque fijo y deja 15 min de margen tras entrenar (también después del CrossFit).
- Si los entrenos no caben en los días con tiempo, el balance de la semana avisa de cuántas sesiones faltan.

El código está en `src/app.html`; `index.html` es la misma página con la cabecera HTML completa.
