# Conceptos explicados

Cada concepto: qué es, una analogía, dónde está en tu repo y una frase en inglés para la entrevista.

## 1. Matriz totalmente unimodular (TU): por qué a veces el LP ya da enteros
**Qué es.**
- Un MILP se resuelve relajándolo: se quita "entero" y se resuelve el LP. Normalmente el LP da fracciones (x = 0,5) y hay que ramificar (branch & bound).
- Algunas matrices son totalmente unimodulares: toda submatriz cuadrada tiene determinante 0, 1 o −1. Si la matriz es TU y los lados derechos son enteros, todas las esquinas de la región factible son enteras.
- El simplex siempre termina en una esquina. Entonces el LP ya da la solución entera, sin ramificar.
- Ejemplos clásicos: transporte, asignación y flujo en redes (camino más corto, flujo máximo, flujo de costo mínimo).

**Analogía.** Un polígono dibujado en papel cuadriculado. Si todas sus esquinas caen justo en intersecciones de la cuadrícula, el simplex, que siempre se detiene en una esquina, siempre cae en un punto entero.

**En un modelo de asignación de cartera.**
- El núcleo es "cada cliente ≤ 1 asesor" más las capacidades de cada asesor: total, y por etapa dentro del total.
- Es un problema de transporte: los clientes son orígenes con 1 unidad; los asesores, destinos con capacidad.
- Las capacidades por etapa están anidadas dentro de la total. Los grupos anidados (familias laminares) mantienen la matriz TU.
- El balance por segmento agrupa clientes de forma que cruza las etapas, y une a varios asesores con la misma z. Eso rompe la estructura: el LP puede dar fracciones.

**En la red de turnos (`python/turnos_red.py`).** Cada agente, solo, es un camino más corto (TU). La cobertura y las horas de contrato acoplan a los agentes: el LP da 267 arcos fraccionarios. Aun así su valor (38) es igual al del MILP. La cota es exacta y por eso resuelve en menos de 1 s.

> *"The core is a transportation structure, which is totally unimodular, so the LP relaxation is almost integral. Only the balancing constraints break that. That's why tens of thousands of binaries solve fast."*

## 2. Objetivo ponderado (weighted objective)
**Qué es.** Juntar varias metas en un solo número con pesos: max w₁·meta₁ + w₂·meta₂ − λ·penalización. En un modelo de asignación de cartera: saldo × peso de jerarquía × bono de continuidad − λ·Σz.

**Analogía.** Elegir carro con una sola nota: 0,5·precio + 0,3·consumo + 0,2·seguridad. Funciona, pero alguien decidió cuántos zlotys vale un punto de seguridad. Los pesos son tasas de cambio.

**Ventaja:** un solo modelo y una sola corrida.

**Problemas:**
- Los pesos son difíciles de justificar ante negocio.
- Mezcla unidades: pesos colombianos contra número de clientes.
- Si un término es enorme, los demás solo desempatan (en la réplica: 4,9 millones contra 1.000).
- El resultado cambia con pequeños cambios de pesos. Y con suma ponderada no se alcanzan algunos puntos de la frontera de Pareto (cuando no es convexa).

> *"A weighted objective is quick, but the weights are implicit exchange rates. I prefer to make the trade-off explicit to the business."*

## 3. "¿Qué tan balanceado queda?"
**Qué te preguntan.** Si entiendes qué controla de verdad tu restricción de balance.

**Lo que controla el min-max.** z ≥ carga de cada asesor. Minimizar z solo baja la carga **máxima**. Las demás pueden quedar en cualquier valor por debajo.

**Ejemplo.**
- Cargas (50, 50, 10) y (50, 30, 30) tienen el mismo máximo: para el modelo valen igual, aunque la segunda es más pareja.
- En la réplica, la ponderada y la lexicográfica con ε = 0 tienen el mismo Σz = 32. Pero la carga Junior mínima es 19 en una y 18 en la otra.

**Analogía.** Un profesor que solo mira la pila de tareas más alta. Mientras ninguna la supere, no le importa que un alumno no tenga nada.

**Además:** balancea cantidad de clientes, no saldo. Un asesor con 50 clientes de 1 millón y otro con 50 de 50 millones "pesan" igual.

**Alternativas:**
- Penalizar la desviación respecto a la media: |carga − media| = d⁺ + d⁻, con dos variables ≥ 0.
- Min-max más max-min: subir también la carga mínima.
- Balancear también el saldo.

> *"Min-max only controls the peak. If the spread matters, I penalize deviations from the average load, and I'd balance value, not only counts."*

## 4. Objetivo lexicográfico en 2 pasos
**Qué es.** Optimizar las metas en orden de prioridad, en vez de mezclarlas con pesos.
- Paso 1: maximizar el valor → V*.
- Paso 2: agregar valor ≥ (1 − ε)·V* y minimizar el desbalance Σz.
- ε es cuánto valor aceptas ceder por más balance (0 = nada).

**Analogía.** Buscar apartamento en Kraków. Paso 1: el arriendo más barato, digamos 3.000 zł. Paso 2: entre los que cuestan como máximo 2 % más (3.060 zł), el más cerca del jardín infantil de tu hijo. Nunca tuviste que decidir cuántos zlotys vale un minuto de caminata.

**Ventajas:** sin pesos mágicos, cada meta en sus unidades, y el gap del solver no "se traga" la segunda meta.

**La trampa (la vimos en la réplica).** En el paso 2 el solver busca cualquier forma de bajar Σz. Con ε = 1 % y sin otra restricción, soltó 116 clientes, los de menor saldo. Hay que proteger cada meta que importa: Σx ≥ asignados del paso 1.

> *"I'd solve it lexicographically: maximize value first, then keep value within a tolerance and minimize imbalance, protecting coverage."*

## 5. Frontera de Pareto y ε-constraint
**Qué es.**
- Frontera de Pareto: las soluciones donde no puedes mejorar una meta sin empeorar otra. Cada punto es un trade-off distinto.
- ε-constraint: optimizas una meta y conviertes la otra en restricción con un límite ε. Cambias ε, resuelves otra vez y juntas los puntos: esa es la curva.

**Analogía.** Pasajes de tren Kraków–Varsovia: precio contra duración. La frontera es la lista de pasajes donde ningún otro es a la vez más barato y más rápido. Le muestras la lista al cliente y él elige. Tú no decides el peso por él.

**En la réplica (`python/cartera_simulada.py`):**

| Valor cedido (ε) | Σz | Carga Junior | Continuidad |
|---|---|---|---|
| 0 % | 32 | 18–32 | 72,9 % |
| 0,1 % | 27 | 26–27 | 69,9 % |
| 1 % | 27 | 26–27 | 61,7 % |

Para negocio: "Cediendo 0,1 % del valor, la carga máxima baja 16 % y los asesores quedan casi iguales (26–27)."

Ojo con la última fila: ceder 1 % no mejora el balance y la continuidad cae a 61,7 %. Ese punto no está en la frontera: el de 0,1 % es mejor en todo. El paso 2 solo mira Σz y no cuida lo que no le pides.

> *"Instead of picking weights myself, I'd show stakeholders the Pareto front and let them choose the trade-off."*

## 6. Métricas de resultado: continuidad, balance, adopción
"Agrega: % de continuidad, balance de carga, adopción" quiere decir: el tiempo (2 días → 15 min) es un resultado, pero el entrevistador también quiere saber si el modelo mejoró el negocio. Tres números:
- **% de continuidad:** de los clientes con asesor histórico, cuántos lo mantuvieron. Ej.: *"92 % of clients kept their advisor."*
- **Balance de carga:** la carga máxima o el rango, antes contra después. Ej.: *"The most loaded advisor went from 180 to 120 clients."*
- **Adopción:** ¿lo usan? Ej.: *"Used every month since [fecha]; planners stopped using Excel."* O el % de asignaciones aceptadas sin cambios manuales.

Si no tienes el dato exacto, da un orden de magnitud honesto o di cómo lo medirías.

## 7. Infactibilidad: "How did you handle infeasibility?"
**Qué es.** Un modelo es infactible cuando ninguna solución cumple todas las restricciones a la vez. Ej.: un día pide 25 agentes y solo hay 22 disponibles.

**Analogía.** Le pides al GPS llegar a las 8:00 cuando son las 7:55 y el viaje dura 30 min. Un GPS rígido dice "no hay ruta". Uno elástico dice "llegas 8:25, 25 min tarde": te da un plan y el tamaño del problema.

**Tres herramientas:**
1. **Holguras penalizadas (modelo elástico).** A la restricción dura le sumas una variable de faltante ≥ 0 y la castigas fuerte en el objetivo. Siempre hay solución, y la holgura dice dónde y cuánto falta. En tu repo: `u[c]` en `assign_clients_workers.py` y `falta[h]` en `turnos_red.py`.
2. **Chequeos previos.** Pruebas baratas sobre los datos antes de armar el modelo. Ej.: disponibles del día < requerimiento. En tu repo: `assign_workers_shifts.py`, como el bloque "IIS" de tu script en R.
3. **IIS (irreducible infeasible subsystem).** El solver te da el conjunto mínimo de restricciones que chocan entre sí. En Gurobi: `computeIIS()`; en CPLEX: conflict refiner.

**Tu respuesta real (Siigo):** *"Coverage was elastic: unmet demand in each block was a penalized slack variable, so the model always returned a schedule. The slack showed where and how many agents were missing, and we used it to plan hiring."*

## 8. Heurística, metaheurística y método exacto
**Qué es.**
- **Heurística:** regla práctica que encuentra una buena solución rápido, sin garantía de óptimo. Ej.: "atiende primero el pedido que vence antes" (EDD); "asigna cada cliente al mejor asesor libre, de mayor a menor saldo" (greedy).
- **Metaheurística:** estrategia general para mejorar una heurística y escapar de óptimos locales: simulated annealing, algoritmos genéticos, búsqueda tabú.
- **Método exacto** (MILP, CP): garantiza el óptimo, o te dice qué tan lejos estás (gap).

**Analogía.** Ir del trabajo a casa. Exacto: revisar todas las rutas y demostrar que no hay una mejor. Heurística: "siempre tomo la avenida principal" (rápido, casi siempre bien). Metaheurística: "pruebo variaciones y a veces acepto una calle peor para descubrir un atajo".

**Datos de tu repo (`python/sa_scheduling.py`, 10 trabajos):** EDD = 299; SA = 113 en 0,5 s; MILP = 113 en 37 s.

**Cuándo usar una heurística:** instancias enormes, tiempo límite estricto, como solución inicial para el MILP (warm start) o como respaldo si el solver falla en producción.

> *"I benchmark the heuristic against the exact optimum on small instances, then use it where the MILP doesn't scale."*

## 9. Red de flujo (network flow) para turnos
**Qué es.** El turno de cada agente es un camino en una red de tiempo.
- Nodo = (hora, horas seguidas trabajadas, ¿ya descansó?).
- Arcos = entrar, trabajar una hora, descansar, salir.
- Cualquier camino de la entrada a la salida es un turno legal: las reglas laborales viven en la red.

**Analogía.** Un mapa de metro. Las estaciones son estados (hora, cansancio, descanso tomado) y las líneas son "trabajar", "descansar" y "salir". Cada viaje válido de la entrada a la salida es un turno legal. El optimizador elige un viaje por agente para que, en cada hora, haya suficientes pasajeros en la línea "trabajar".

**"Person-specific connectivity arcs":** cada persona tiene sus propios arcos de entrada (las horas en que puede empezar), según su contrato y disponibilidad.

**Por qué conviene:** la red ya garantiza descansos y máximos de horas seguidas. El MILP solo agrega horas de contrato, cobertura y topes (p. ej., máximo 2 personas en descanso a la vez).

**Ejemplo genérico:** `python/turnos_red.py` (14 agentes, 1.242 arcos, < 1 s). Tu red real, reconstruida contigo: `09_red_siigo.md`.
