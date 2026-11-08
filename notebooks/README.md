# Ruta de aprendizaje: investigación de operaciones desde cero

Una lección por notebook. Cada una parte de un modelo pequeño y crece en tamaño y en estrategia de desarrollo.
Los conceptos se explican sin dar nada por sabido, con ejemplos del sector energía.

## Dónde correrlos: Google Colab
No necesitas instalar nada.
1. Entra a https://colab.research.google.com.
2. **Archivo → Abrir notebook → pestaña GitHub.**
3. Escribe `ainsu23/OperationResearch_withR`. Si el repo es privado, marca *Include private repos* y autoriza tu cuenta de GitHub.
4. Elige la rama `master` y abre el notebook de la lección. Si la lección nueva aún no está en `master`, elige la rama donde se subió. Las lecciones 1 a 11, con notación matemática, están en `claude/optimistic-lovelace-e8kk6a`.
5. Corre celda por celda con `Shift + Enter`. Antes de cada celda, adivina qué va a imprimir.
6. Para guardar tus notas: **Archivo → Guardar una copia en Drive**.

Si una celda no se entiende, pega la celda y su salida en el chat y la vemos juntos.

**Apoyo con dibujos:** `06_secuenciacion_dibujos.html` explica la lección 7 con un dibujo por cada restricción (retraso, disyuntiva con big-M, job shop, CP-SAT y barcos). Descárgalo y ábrelo en el navegador; al final trae un mapa a las celdas del notebook.
`07_incertidumbre_dibujos.html` hace lo mismo con la lección 8: escenarios, costo esperado como área, árbol de 2 etapas, EVPI y VSS, Monte Carlo y SAA, muelles y repuestos en 3 bases.

## Notación matemática
Cada problema trae su formulación como se escribe en un libro o en una entrevista, justo al lado de su versión en palabras y en Pyomo.
- La primera vez que aparece un símbolo, una tabla dice cómo se lee, qué significa y su equivalente en Python o SQL.
- Al final de cada lección, una tabla **Notación de hoy** junta los símbolos nuevos.
- Orden en que aparecen: lección 1 ($\max$, $\sum$, $\forall$, $\in$, índices), lección 2 (dual, $\Delta$, funciones por tramos, matrices y transpuesta),
  lección 3 ($\{0,1\}$ contra $[0,1]$, $\subseteq$, piso y techo, lógica $\Rightarrow \land \lor \neg$, big-M),
  lección 4 (doble suma, permutaciones, $\det$, $\mathbb{Z}$, conjuntos por comprensión, función indicadora),
  lecciones 5–6 ($G = (N, A)$, $\delta^+$ y $\delta^-$, $N \setminus O$, conjuntos indexados $S_i$ y sumas anidadas, $\emptyset$, $\cap$, familias laminares, matriz de incidencia, precio nodal $\pi_i$, nodos como tuplas, $\bigcup$, $\notin$),
  lección 7 ($S_j$ y $C_j$, retraso $\max\{0, C_j - d_j\}$ linealizado, $n!$, $\binom{n}{2}$, $\prod$, $C_{\max}$, intervalos $[a, b)$, $\text{NoOverlap}$, dominios enteros, $x_{pvt}$ indexada en el tiempo),
  lección 8 (escenarios $S$ y $\pi_s$, $\mathbb{E}[\cdot]$, primera etapa sin índice $s$ y segunda con $s$, $\mathbb{Z}_{\ge 0}$, $\text{Poisson}(\lambda)$, $\hat{\theta}$, $\frac{1}{N}\sum$, $\bar{x} \pm 1{,}96\, s/\sqrt{N}$, EVPI y VSS),
  lección 9 (permutación $\pi$ y $\Pi_n$, $C_{\pi_k}$ como suma acumulada, notación de Graham $1 \,\Vert\, \sum w_j T_j$, índice ATC con $\exp$, vecindad $\mathcal{N}(\pi)$, $\Delta$, $T$ y $\alpha$ del recocido, $e^{-\Delta/T}$),
  lección 10 ($f_1(x)$ y $f_2(x)$, dominancia $\succ$, $\iff$, $\nexists$, frontera $\mathcal{P}$, $f_k^*$, pesos $\lambda$, tolerancia $\varepsilon$, lexmax, $\omega_a$ y $\kappa_{ac}$, $z_\sigma$ min-max, $\prod_c (k_c + 1)$),
  lección 11 ($\hat{y}$, MAE con $\lvert \cdot \rvert$, cuantil $\tau$ y pérdida pinball $\rho_\tau$, cuantil calibrado $\hat{q} - \delta$, costo esperado precalculado $\bar{c}_{ed}$, $D \setminus \{0\}$).

## Los dos tamaños de cada problema
Todo problema tiene dos tamaños: el **modelo** (se cuenta con los conjuntos) y el **espacio de búsqueda** (cuántas soluciones hay).
El primero crece lineal o cuadrático; el segundo, casi siempre exponencial. El solver no recorre el espacio: usa la estructura.

| Lección | Problema | Modelo: variables · restricciones · no ceros | Espacio de búsqueda | Lo que revisó el método |
|---|---|---|---|---|
| 1 | Taller 2 × 2 | 2 · 3 · 5 | 10.201 planes enteros | 5 esquinas |
| 2 | Planta 30 × 8 | 30 · 38 · 142 | hasta $\binom{68}{30} \approx 10^{19}$ esquinas | simplex, 6 ms |
| 3 | Mochila de 5 proyectos | 5 · 1 · 5 | $2^5 = 32$ | 7 nodos de branch & bound |
| 3 | Cartera de 20 proyectos | 20 · 13 · 71 | $2^{20} \approx 10^6$ (22.912 factibles) | 1 nodo + cortes |
| 4 | Asignación 3 × 3 | 9 · 6 · 18 | $3! = 6$ asignaciones | el LP, sin ramificar |
| 4 | Equipos 50 × 20 | 160 · 65 · 300 | $2^{140} \approx 10^{42}$ (sin el join: $10^{301}$) | el LP, sin ramificar |
| 5 | Flujo con bases | 12 · 9 · 24 | — | el LP |
| 5 | Camino más corto en 40 × 40 cuadras | 3.280 calles | $\approx 10^{23}$ caminos | Dijkstra, 2 ms |
| 6 | Turnos: 12 personas, 1 semana | 3.038 · 2.166 · 9.502 | $60^{52} \approx 10^{92}$ semanas | < 1 s; crece lineal (pendiente ≈ 1) |
| 7 | Una máquina, 4 trabajos | 14 · 16 · 44 | $4! = 24$ órdenes | cota LP 0 h: big-M débil |
| 7 | Job shop 5 × 3 | 36 · 57 · 158 | 69.120 órdenes | MILP: cota LP 7 h contra 14 h; CP-SAT: 0,01 s |
| 7 | Job shop 40 × 5 | 3.900 binarias (MILP) | $(40!)^5 \approx 10^{240}$ | MILP: gap 87 % a los 10 s; CP-SAT: óptimo en 0,03 s |
| 7 | Barcos: 80 proyectos, 10 barcos, 120 días | 11.673 binarias | $(10 \cdot 120)^{80} \approx 10^{246}$ | LP a 0,1 % del MILP; < 1 s |
| 8 | Repuestos, 3 escenarios | 4 · 3 · 6 | 7 planes (0 a 6 módulos) | forma extendida |
| 8 | Repuestos, SAA con 10.000 inviernos | 10.001 · 10.000 · 20.000 | los mismos planes; lo caro es el valor esperado | 1 s; estable desde 1.000 escenarios |
| 8 | Red de repuestos: 3 bases, 4 parques, 1.000 escenarios | 16.006 · 7.003 · 31.006 | $7^3 = 343$ planes de stock | 2 s; estable desde 200 escenarios |
| 9 | Banco de prueba: 8 trabajos con pesos | 44 · 64 · 184 (28 binarias) | $8! = 40.320$ órdenes | ATC llega al óptimo; búsqueda local en 5 movimientos |
| 9 | 200 trabajos | 19.900 binarias (MILP) | $200! \approx 10^{375}$ | CP-SAT solo, peor que ATC; con pista, gap 5,9 % |
| 10 | Cartera de 8 proyectos, 2 metas | 8 · 1 · 8 | $2^8 = 256$ (103 factibles, 5 en la frontera) | el ponderado ve 2 de 5; ε-constraint, las 5 |
| 10 | Cartera Banco Agrario: 1.200 clientes, 22 asesores | 11.966 · 1.292 · 41.582 | $10^{1168}$ asignaciones | 1 a 17 s por punto de la frontera |
| 11 | Mantenimiento: 3 turbinas, 6 días | 21 · 9 · 39 | 229 planes factibles de $7^3 = 343$ | asignación: el LP ya da enteros |
| 11 | Mantenimiento: 640 turbinas, 60 días, 16 cuadrillas | 39.040 · 700 · 77.440 | $61^{640} \approx 10^{1143}$ | < 1 s; los escenarios no agregan variables |

## Lecciones
| # | Lección | Conceptos | Tamaño | Estrategia nueva |
|---|---|---|---|---|
| 1 | Tu primer modelo: el taller | variable, objetivo, restricción, región factible, esquina, holgura | 2 productos × 2 máquinas | a mano → fuerza bruta → Pyomo pieza por pieza → función |
| 2 | ¿Cuánto vale una hora más? | precio sombra, rango, costo reducido, dual, holgura complementaria | 30 productos × 8 máquinas | datos en tablas (pandas); ver el top 5 de cada pieza |
| 3 | Decisiones sí/no | variables binarias, reglas lógicas, costo fijo, big-M, branch & bound, gap | 5 → 20 proyectos | por qué redondear el LP no sirve; sensibilidad por re-solve |
| 4 | Asignación | asignación, goloso, matriz TU, pares factibles, modelo elástico, método húngaro | 3 × 3 → 50 ingenieros × 20 proyectos | crear solo los pares posibles (join); revisar candidatos antes de resolver |
| 5 | Redes | nodos, arcos, conservación de flujo, transporte, matriz de incidencia, precio nodal, camino más corto | 2 almacenes → 3 bases → 4 parques eólicos | construir la red desde tablas (`groupby` para arcos que entran y salen) |
| 6 | Tu red de turnos (Siigo) | red de tiempo, camino = turno, restricción extra, cobertura elástica, contratación | 1 persona, 1 día → 12 personas, 1 semana | generar solo la red factible; listar todos los caminos antes de optimizar |
| 7 | Secuenciación | disyuntiva, retraso, makespan, big-M débil, cota simple, CP-SAT, intervalos, NoOverlap, indexado en el tiempo | 1 máquina × 4 → 40 trabajos × 5 máquinas; 8 → 80 proyectos con barcos | elegir MILP o CP; precalcular costos por día y generar solo inicios factibles |
| 8 | Incertidumbre | escenarios, valor esperado, error del promedio, estocástica de 2 etapas, EVPI, VSS, Monte Carlo, SAA, intervalo de confianza, simulación de eventos | 1 parque con 3 escenarios → 3 bases × 4 parques con 1.000 escenarios; muelles | evaluar fuera de la muestra; subir escenarios hasta que el plan no cambie |
| 9 | Heurísticas | reglas de prioridad (EDD, WSPT, ATC), vecindad, búsqueda local, óptimo local, recocido simulado, warm start, cota y gap | 8 → 200 trabajos en una máquina | cadena regla → búsqueda local → SA → solver con pista; reportar varias semillas |
| 10 | Varias metas | dominancia, frontera de Pareto, ponderado, punto no soportado, lexicográfico, ε-constraint, proteger metas, min-max | 8 proyectos → 1.200 clientes × 22 asesores | resolver en secuencia; recorrer la frontera; un piso por cada meta que importa |
| 11 | ML + optimización | predict-then-optimize, fuga de datos, GroupKFold, baseline, error por tramo, cuantil, calibración conformal, costo de la decisión | 3 → 640 turbinas | escenarios desde los errores de validación; costo esperado precalculado |

Listas: lección 1 (`01_primer_modelo.ipynb`), lección 2 (`02_precio_sombra.ipynb`), lección 3 (`03_decisiones_si_no.ipynb`), lección 4 (`04_asignacion.ipynb`) lecciones 5 y 6 juntas (`05_redes_y_turnos.ipynb`), lección 7 (`06_secuenciacion.ipynb`), lección 8 (`07_incertidumbre.ipynb`), lección 9 (`08_heuristicas.ipynb`), lección 10 (`09_varias_metas.ipynb`) y lección 11 (`10_ml_y_optimizacion.ipynb`).
La ruta está completa.
