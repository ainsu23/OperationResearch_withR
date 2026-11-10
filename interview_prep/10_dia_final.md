# Martes 10 nov: las tres sesiones que faltaban, en un solo día

La entrevista es mañana. Faltaban tres sesiones del plan: domingo 8 (ML, estadística, producción y código), lunes 9 (simulacro) y hoy (repaso ligero).
Van juntas en **3 h 45 de estudio, más una pausa de 15 min**. Termina antes de las 19:00 y duerme bien: mañana rinde más una cabeza descansada que un repaso extra.

| Bloque | Tiempo | Qué | Material |
|---|---|---|---|
| 1 | 45 min | ML, estadística y producción (la sesión del domingo) | `03_question_bank.md` §B–D |
| 2 | 40 min | Python y SQL cronometrado | `04_coding_drills.md` |
| — | 15 min | Pausa: camina, sin pantalla | — |
| 3 | 60 min | Simulacro de 45 min + 15 min de revisión (la sesión del lunes) | `11_simulacro.md` |
| 4 | 45 min | Historias STAR en voz alta y completar los datos que faltan | `01_star_stories.md`, `09_red_siigo.md` |
| 5 | 15 min | Hoja final y logística de mañana | `12_hoja_final.md` |

**Si no alcanza el tiempo, este es el orden de prioridad:** 3 → 4 → 1 → 5 → 2. El simulacro y tus historias pesan más que el SQL.

## Bloque 1 · 45 min: ML, estadística y producción
Responde en voz alta, en inglés, máximo 60 s cada una. Graba 2 en el celular y escúchalas: busca muletillas y respuestas sin número.
Estas 10 son las que más probablemente salen para este cargo (número del banco de preguntas):

| # | Pregunta | Tu ejemplo para citar |
|---|---|---|
| 17 | How do you validate a model properly? | L11: 10 días de error por fila contra 15 por turbina (`GroupKFold`) |
| 18 | Data leakage examples | L11: el nivel base de cada turbina deja que el modelo la reconozca |
| 19 | Regression metrics? | L11: el MAE no ve que llegar tarde cuesta 60 veces más |
| 22 | Random forest vs gradient boosting | L11: lineal 19,5 días, boosting 15 |
| 24 | Uncertainty in predictions? | L11: cuantil 10 % que cubría 81 %, calibrado a 90 % con conformal |
| 26 | Predict-then-optimize pitfalls? | L11: mismo modelo, plan con el punto 13 a 21 % más caro que con escenarios |
| 27 | Model drift? | L11 §7: vigilar cobertura del cuantil y costo realizado del plan |
| 28 | Censoring? | L11: la flota está censurada; las turbinas que no han fallado no tienen RUL |
| 33 | Monte Carlo: how many replications? | L8: intervalo de 132 mil € con 100 inviernos, 4 mil € con 100.000 |
| 34–35 | How would you deploy an optimization / ML model? | Siigo: R + Python + API en Databricks; L11 §7: pipeline semanal |

## Bloque 2 · 40 min: Python y SQL
Cuatro ejercicios de `04_coding_drills.md`, 10 min cada uno, sin autocompletado y explicando en inglés mientras escribes:
**3** (mochila con programación dinámica), **4** (número mínimo de cuadrillas), **6** (top 3 por mes con `RANK`), **10** (rachas de días seguidos).
Las 10 soluciones del archivo se probaron hoy con datos de ejemplo (Python con pandas y Pyomo; SQL en DuckDB, que acepta la sintaxis de Postgres): todas dan el resultado correcto.

## Bloque 3 · 60 min: simulacro
Sigue `11_simulacro.md` con un cronómetro. Dos formas de hacerlo:
- **Conmigo (recomendado):** escribe *"hazme el simulacro del archivo 11, en inglés, una pregunta a la vez, y al final evalúame con la rúbrica"*.
- **Solo:** lee cada pregunta, contesta en voz alta y graba. Después compara con los puntos clave del archivo.

## Bloque 4 · 45 min: historias STAR y los datos que faltan
Cuenta en voz alta el pitch (2 min) y las historias 1, 2 y 3 (90 s cada una). Antes, completa lo que solo tú sabes:
- [ ] Banco Agrario: cuántos clientes ([N]), cuántos asesores ([M]), cuántos pares factibles.
- [ ] Banco Agrario: % de clientes que mantuvo su asesor, carga máxima antes y después, desde cuándo lo usan (`07_conceptos.md` §6 dice cómo decirlo si no tienes el dato exacto).
- [ ] Siigo: tamaño real del modelo (personas, días, nodos, arcos, tiempo de solución) y las ventanas exactas de descanso (`09_red_siigo.md`).
- [ ] RAG: cómo evaluaste la calidad de las respuestas.
- [ ] Refactor de R (17 → 4 min): qué cambiaste exactamente.
- [ ] Una historia de error o fracaso real, con lo que cambiaste en tu forma de trabajar.

## Bloque 5 · 15 min: hoja final y logística
Lee `12_hoja_final.md` una vez. Mañana, una sola lectura en el desayuno; nada nuevo.
- [ ] Revisa la web y el último reporte anual de la empresa (`05_sector.md` tiene las preguntas para hacerles).
- [ ] Si es en línea: cámara, micrófono, luz y el link probados hoy. Si es presencial: ruta y hora de salida.
- [ ] Papel y lápiz a mano: vas a formular en vivo.
- [ ] Agua, y nada de cafeína extra.
