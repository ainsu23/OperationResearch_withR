# Hoja final: leer una vez el martes y una vez mañana en el desayuno

## Tu perfil en 30 segundos
> *"I'm an industrial engineer with a master's in Statistics and Operations Research, and about eight years turning data into decisions.
> I've deployed three MILP models in production: from six hours to seven minutes at Siigo, from two days to fifteen minutes at Banco Agrario.
> I want to combine prediction and optimization in an industrial setting, which is exactly this role."*

## Tres números que tienen que salir
| Caso | Número |
|---|---|
| Siigo: red de turnos, 5 países | 6 h → 7 min |
| Banco Agrario: asignación de cartera | 2 días → 15 min |
| Ajover: validación de datos del planificador | 100 % de entradas validadas antes de cada corrida |

## Al formular, siempre en este orden
**Decisiones → objetivo → restricciones → tamaño → qué hago si no escala → cómo lo valido con negocio.**

## Una frase por lección, con su número
| Tema | La frase | El número |
|---|---|---|
| L2 Precio sombra | Change in the objective per unit of right-hand side, within its range | holgura → precio 0 |
| L3 Binarias | Rounding the LP fails; the LP gives a bound, B&B prunes with it | gap = lo peor que puede pasar |
| L4 Asignación | Totally unimodular: the LP is already integral | 50 × 20 sin ramificar |
| L5 Redes | The dual of flow conservation is the nodal price | precio nodal = dual |
| L7 Secuenciación | Big-M is weak; CP-SAT for sequencing, time-indexed MILP for coarse time | cota LP 0 contra óptimo 6 |
| L8 Incertidumbre | Averages are optimistic; two-stage, SAA, evaluate out of sample | promete 80 mil, cuesta 280 mil |
| L8 Benders | Master with first-stage decisions; LP subproblems send dual cuts | 10.000 escenarios en 5 iteraciones |
| L9 Heurísticas | Heuristic as warm start; the solver gives the bound | ATC + CP-SAT: gap 5,9 % |
| L10 Varias metas | Weights hide exchange rates; lexicographic or ε-constraint | el ponderado vio 2 de 5 carteras |
| L11 ML + optimización | Group k-fold; scenarios from errors; evaluate by decision cost | 10 contra 15 días; 13–21 % más barato |

## Linealizaciones que deben salir sin pensar
| Necesitas | Lineal |
|---|---|
| `max(0, a)` en un objetivo que minimiza | `T ≥ a`, `T ≥ 0` |
| `min max_i f_i` | `min t`, `t ≥ f_i` |
| Costo fijo si `x > 0` | `x ≤ U·y`, costo `f·y` |
| `z = x·y` binarias | `z ≤ x`, `z ≤ y`, `z ≥ x + y − 1` |
| Either-or | big-M con una binaria; M lo más chico que sea válido |

## Si te bloqueas
- Pide un minuto y escribe las tres piezas en el papel: decido, objetivo, restricciones.
- Empieza por el caso chico: "let me first solve it for 2 jobs and 1 machine".
- Di en voz alta lo que supones: "I'll assume prices are known for now, and come back to uncertainty".

## Tus 3 preguntas para ellos
1. What decisions does the team support today, and which one would my first project target?
2. How are models deployed: inside existing digital products, or as standalone tools for planners?
3. Which optimization and ML stack do you use, and how do you measure the value of a delivered model?
