# Tu red de turnos de Siigo (reconstruida contigo)

Diagrama: `diagramas/red_turnos_siigo.png`. Editable en draw.io: `diagramas/red_turnos_siigo.drawio`.

## Cómo era
- **Una red por persona.** Andrés, Klaudia, Oliver… tienen la misma estructura, cada uno con un solo `inicio` y un solo `Fin` para toda la semana.
- **Camino = horario.** Una unidad de flujo va del `inicio` al `Fin`. El camino que recorre es el horario de la semana de esa persona.
- **Bloques de 30 min.** Cada nodo es (persona, día, tipo, bloque). Los tipos son trabajo, descanso, almuerzo, libre, mañana libre y tarde libre.
- **Entrada:** 07:00, 07:30, 08:00 u 08:30.
- **Almuerzo:** empieza a las 12:00, 12:30, 13:00 o 13:30 y dura siempre 1 hora (2 nodos).
- **Descansos:** 2 de 15 min. Cada bloque de 30 min tiene dos nodos de descanso posibles, por ejemplo `08:30_30` y `08:30_45`. El cuarto de hora da la hora exacta del descanso en el horario de la persona. Para la demanda, el bloque entero cuenta como no disponible.
- **Etapas:** el trabajo se divide en etapas (antes de Descanso1, antes del almuerzo, antes de Descanso2 y después). Solo se pasa de una etapa a la siguiente por un descanso o por el almuerzo, así que ningún camino se los salta.
- **Días:** no hay inicio ni Fin por día. Los nodos donde termina un día se conectan directamente con los nodos donde empieza el siguiente.
- **Solo redes factibles:** si ya se sabía que alguien tenía libre un día, ese día solo tenía el nodo Libre, sin nodos de trabajo.
- **Costos = horas:** 0,5 por bloque trabajado; 4 al entrar y 4 al salir de Libre. Cada día suma un total fijo: 8 h de trabajo, más 1 h de almuerzo y 30 min de descanso = 9,5 h en la empresa. Por eso la salida queda fija según la entrada: 07:00 → 16:30; 08:30 → 18:00.
- **Demanda:** cada bloque de 30 min tiene su demanda. Restricción por franja: personas trabajando en el bloque + demanda no atendida ≥ demanda. Quien está en descanso no cuenta.
- **Demanda no atendida:** si no alcanzaba la gente, esos clientes no se atendían y había una penalización. El modelo siempre entregaba un horario, y la demanda no atendida por franja mostraba cuánta gente faltaba: con eso se planeaba cuánta gente contratar.

## Por confirmar
- Horas exactas de las ventanas de descanso.
- Costo de los arcos de descanso, almuerzo y entre días.
- Horario de Mañana_libre y Tarde_libre.

## Lo que puedes destacar
- **Las reglas viven en la red.** Un turno ilegal no existe como camino, así que no hace falta una restricción por cada regla.
- **Red más chica.** Solo se crean los nodos factibles; los días libres conocidos no generan nodos de trabajo.
- **Fácil para el solver.** Sin las restricciones de demanda y de horas, cada persona es un problema de camino más corto, una estructura de red que el solver resuelve muy rápido (`07_conceptos.md` §1).
- **Del horario a la contratación.** La misma salida del modelo operativo (la demanda no atendida) servía para una decisión táctica: cuánta gente contratar. Eso es justo lo que la oferta llama *decision support*.

## Explicación corta (en inglés, ~80 segundos)
> At Siigo I scheduled support agents across five countries. I modeled each agent's week as a path in a time-expanded network: one start node and one end node per agent, and in between, 30-minute nodes for work, breaks, lunch and days off. The network itself encoded the labor rules: four start times, a one-hour lunch at one of four times, and two 15-minute breaks. Work nodes were split into stages of the day, and the only way to move to the next stage was through a break or lunch node, so no schedule could skip them. I only generated the feasible part of each network: a known day off had only a day-off node. Arc costs were hours, and a side constraint fixed the hours per day. Coverage constraints linked the agents: in each 30-minute block, agents working had to meet demand, and agents on a break did not count. When there weren't enough agents, unmet demand was penalized, so the model always returned a schedule, and that shortfall told us how many people to hire. It ran in AMPL, with R for the data and Python for the API, and cut the process from 6 hours to 7 minutes.

## Preguntas probables
- *"Why a network and not plain constraints?"* → Each rule becomes structure: illegal schedules are not paths. That means fewer constraints, and for each agent it is a shortest-path problem, which solvers handle very well.
- *"What if demand couldn't be met?"* → "Coverage was elastic: unmet demand in each block was a penalized slack variable, so the model always returned a schedule. The slack showed where and how many agents were missing, and we used it to plan hiring."
- *"How big was it?"* → [Completa: personas, días, nodos, arcos y tiempo de solución.]
