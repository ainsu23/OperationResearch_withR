# Ruta de aprendizaje: investigación de operaciones desde cero

Una lección por notebook. Cada una parte de un modelo pequeño y crece en tamaño y en estrategia de desarrollo.
Los conceptos se explican sin dar nada por sabido, con ejemplos del sector energía.

## Dónde correrlos: Google Colab
No necesitas instalar nada.
1. Entra a https://colab.research.google.com.
2. **Archivo → Abrir notebook → pestaña GitHub.**
3. Escribe `ainsu23/OperationResearch_withR`. Si el repo es privado, marca *Include private repos* y autoriza tu cuenta de GitHub.
4. Elige la rama `master` y abre el notebook de la lección. Si la lección nueva aún no está en `master`, elige la rama donde se subió. Las lecciones 1 a 6 con notación matemática están en `claude/clever-cray-8tywgt`.
5. Corre celda por celda con `Shift + Enter`. Antes de cada celda, adivina qué va a imprimir.
6. Para guardar tus notas: **Archivo → Guardar una copia en Drive**.

Si una celda no se entiende, pega la celda y su salida en el chat y la vemos juntos.

## Notación matemática
Cada problema trae su formulación como se escribe en un libro o en una entrevista, justo al lado de su versión en palabras y en Pyomo.
- La primera vez que aparece un símbolo, una tabla dice cómo se lee, qué significa y su equivalente en Python o SQL.
- Al final de cada lección, una tabla **Notación de hoy** junta los símbolos nuevos.
- Orden en que aparecen: lección 1 ($\max$, $\sum$, $\forall$, $\in$, índices), lección 2 (dual, $\Delta$, funciones por tramos, matrices y transpuesta),
  lección 3 ($\{0,1\}$ contra $[0,1]$, $\subseteq$, piso y techo, lógica $\Rightarrow \land \lor \neg$, big-M),
  lección 4 (doble suma, permutaciones, $\det$, $\mathbb{Z}$, conjuntos por comprensión, función indicadora),
  lecciones 5–6 ($G = (N, A)$, $\delta^+$ y $\delta^-$, $N \setminus O$, matriz de incidencia, precio nodal $\pi_i$, nodos como tuplas, $\bigcup$, $\notin$).

## Lecciones
| # | Lección | Conceptos | Tamaño | Estrategia nueva |
|---|---|---|---|---|
| 1 | Tu primer modelo: el taller | variable, objetivo, restricción, región factible, esquina, holgura | 2 productos × 2 máquinas | a mano → fuerza bruta → Pyomo pieza por pieza → función |
| 2 | ¿Cuánto vale una hora más? | precio sombra, rango, costo reducido, dual, holgura complementaria | 30 productos × 8 máquinas | datos en tablas (pandas); ver el top 5 de cada pieza |
| 3 | Decisiones sí/no | variables binarias, reglas lógicas, costo fijo, big-M, branch & bound, gap | 5 → 20 proyectos | por qué redondear el LP no sirve; sensibilidad por re-solve |
| 4 | Asignación | asignación, goloso, matriz TU, pares factibles, modelo elástico, método húngaro | 3 × 3 → 50 ingenieros × 20 proyectos | crear solo los pares posibles (join); revisar candidatos antes de resolver |
| 5 | Redes | nodos, arcos, conservación de flujo, transporte, matriz de incidencia, precio nodal, camino más corto | 2 almacenes → 3 bases → 4 parques eólicos | construir la red desde tablas (`groupby` para arcos que entran y salen) |
| 6 | Tu red de turnos (Siigo) | red de tiempo, camino = turno, restricción extra, cobertura elástica, contratación | 1 persona, 1 día → 12 personas, 1 semana | generar solo la red factible; listar todos los caminos antes de optimizar |
| 7 | Secuenciación | disyuntivas, big-M débil, CP-SAT | taller y barcos | elegir MILP o CP |
| 8 | Incertidumbre | Monte Carlo, simulación, escenarios, estocástica de 2 etapas | muelles, repuestos | simular antes de optimizar |
| 9 | Heurísticas | greedy, simulated annealing, warm start, límite de tiempo | 10 → 200 trabajos | comparar contra el óptimo |
| 10 | Varias metas | ponderado, lexicográfico, Pareto | cartera simulada | resolver en secuencia |
| 11 | ML + optimización | predict-then-optimize, cuantiles | RUL → mantenimiento | pipeline de punta a punta |

Listas: lección 1 (`01_primer_modelo.ipynb`), lección 2 (`02_precio_sombra.ipynb`), lección 3 (`03_decisiones_si_no.ipynb`), lección 4 (`04_asignacion.ipynb`) y lecciones 5 y 6 juntas (`05_redes_y_turnos.ipynb`). Las siguientes se agregan una por una, a tu ritmo.
