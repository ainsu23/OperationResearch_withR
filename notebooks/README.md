# Ruta de aprendizaje: investigación de operaciones desde cero

Una lección por notebook. Cada una parte de un modelo pequeño y crece en tamaño y en estrategia de desarrollo.
Los conceptos se explican sin dar nada por sabido, con ejemplos del sector energía.

## Dónde correrlos: Google Colab
No necesitas instalar nada.
1. Entra a https://colab.research.google.com.
2. **Archivo → Abrir notebook → pestaña GitHub.**
3. Escribe `ainsu23/OperationResearch_withR`. Si el repo es privado, marca *Include private repos* y autoriza tu cuenta de GitHub.
4. Elige la rama `master` y abre el notebook de la lección. Si la lección nueva aún no está en `master`, elige la rama donde se subió (lección 3: `claude/affectionate-planck-x31ic6`; lección 4: `claude/nifty-volta-o9qira`).
5. Corre celda por celda con `Shift + Enter`. Antes de cada celda, adivina qué va a imprimir.
6. Para guardar tus notas: **Archivo → Guardar una copia en Drive**.

Si una celda no se entiende, pega la celda y su salida en el chat y la vemos juntos.

## Lecciones
| # | Lección | Conceptos | Tamaño | Estrategia nueva |
|---|---|---|---|---|
| 1 | Tu primer modelo: el taller | variable, objetivo, restricción, región factible, esquina, holgura | 2 productos × 2 máquinas | a mano → fuerza bruta → Pyomo pieza por pieza → función |
| 2 | ¿Cuánto vale una hora más? | precio sombra, rango, costo reducido, dual, holgura complementaria | 30 productos × 8 máquinas | datos en tablas (pandas); ver el top 5 de cada pieza |
| 3 | Decisiones sí/no | variables binarias, reglas lógicas, costo fijo, big-M, branch & bound, gap | 5 → 20 proyectos | por qué redondear el LP no sirve; sensibilidad por re-solve |
| 4 | Asignación | asignación, goloso, matriz TU, pares factibles, modelo elástico, método húngaro | 3 × 3 → 50 ingenieros × 20 proyectos | crear solo los pares posibles (join); revisar candidatos antes de resolver |
| 5 | Redes | nodos, arcos, conservación de flujo, transporte | plantas → bases → plataformas | construir la red desde tablas |
| 6 | Tu red de turnos (Siigo) | red de tiempo, camino = turno, cobertura de demanda | 1 persona, 1 día → equipo, 1 semana | generar solo la red factible |
| 7 | Secuenciación | disyuntivas, big-M débil, CP-SAT | taller y barcos | elegir MILP o CP |
| 8 | Incertidumbre | Monte Carlo, simulación, escenarios, estocástica de 2 etapas | muelles, repuestos | simular antes de optimizar |
| 9 | Heurísticas | greedy, simulated annealing, warm start, límite de tiempo | 10 → 200 trabajos | comparar contra el óptimo |
| 10 | Varias metas | ponderado, lexicográfico, Pareto | cartera simulada | resolver en secuencia |
| 11 | ML + optimización | predict-then-optimize, cuantiles | RUL → mantenimiento | pipeline de punta a punta |

Listas: lección 1 (`01_primer_modelo.ipynb`), lección 2 (`02_precio_sombra.ipynb`), lección 3 (`03_decisiones_si_no.ipynb`) y lección 4 (`04_asignacion.ipynb`). Las siguientes se agregan una por una, a tu ritmo.
