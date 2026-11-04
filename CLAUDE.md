# Contexto para seguir en otro chat

## Para quién y para qué
Andrés Insuasty, analista de datos con experiencia en investigación de operaciones (IO). Vive en Polonia.
Se prepara para una entrevista de **Senior Data Scientist (modelado y optimización), sector energía: miércoles 11 nov 2026**.
Este repo tiene su ruta de estudio: lecciones en notebooks (`notebooks/`) y material de entrevista (`interview_prep/`).

## Cómo escribirle
- Español, frases cortas, al grano. Datos concretos antes que adjetivos. Cero lenguaje de anuncio.
- Si pide una decisión: **una** recomendación, no varias opciones.
- Aprende con analogías. Usa su vida: su hijo (nació en nov 2022), su esposa polaca, Cracovia, el polaco que está aprendiendo, eToro, la babcia.
  Y su trabajo: Siigo (red de turnos), Banco Agrario (asignación de cartera), Ajover (planeación).
- Ejemplos del sector energía: parques eólicos en el Báltico, subestaciones, cartera de proyectos, precios nodales.

## Estado al 4 nov 2026
- **Rama de trabajo: `claude/optimistic-lovelace-e8kk6a`.** Parte de `claude/clever-cray-8tywgt` (lecciones 1 a 6) y agrega la L7 (`06_secuenciacion.ipynb`).
  Todavía no tiene PR. Reemplaza a `claude/clever-cray-8tywgt`, `claude/affectionate-planck-x31ic6` (L3) y `claude/nifty-volta-o9qira` (L4): no abrir PR de esas.
- `master` tiene las lecciones 1 y 2.
- Calendario vigente: `interview_prep/00_plan.md` §3. Lo que falta:

| Fecha | Qué | Notebook / apoyo |
|---|---|---|
| Mié 4 nov | L7: secuenciación (máquinas y barcos) | **hecho**: `notebooks/06_secuenciacion.ipynb` |
| Jue 5 | L8: incertidumbre (Monte Carlo, escenarios, estocástica de 2 etapas) | crear `notebooks/07_incertidumbre.ipynb`; `python/simulation_scenarios.py` |
| Vie 6 | L11: ML + optimización (RUL → mantenimiento) | `python/rul_maintenance.py` |
| Sáb 7 | L9 heurísticas + L10 varias metas | `python/sa_scheduling.py`, `python/cartera_simulada.py` |
| Dom 8 | ML, estadística, producción + Python/SQL cronometrado | `interview_prep/03_question_bank.md`, `04_coding_drills.md` |
| Lun 9 | Simulacro único (formulación en vivo + ML + sector) | `interview_prep/05_sector.md` |

- Lecciones 5 y 6 van juntas en `05_redes_y_turnos.ipynb`. Por eso el número del archivo va uno atrás: L7 = `06_...`, L8 = `07_...`.
- **OR-Tools y HiGHS:** `ortools` trae su propio HiGHS y choca con `highspy` 1.15 (`undefined symbol`). En notebooks que usan los dos: `%pip install -q pyomo "highspy==1.14.0" "ortools==9.15.6755"`.
- **Límite de tiempo en Pyomo:** `SOLVER.solve(m, timelimit=10)`. Con la interfaz `SolverFactory("appsi_highs")`, `solve` sobrescribe `solver.config.time_limit`.
- Por confirmar con Andrés (en `interview_prep/09_red_siigo.md`): ventanas exactas de descanso y tamaño real del modelo de Siigo (personas, nodos, arcos, tiempo).

## Estructura de cada notebook (mantenerla en las lecciones nuevas)
1. Título, **Qué vas a aprender** (incluye "Escribir el modelo en notación matemática…") y **Cómo usar**.
2. §0 entorno: `%pip install -q pyomo highspy` (+ lo que haga falta), imports, `SOLVER = pyo.SolverFactory("appsi_highs")`, `eur()`.
3. §1 **Dónde quedamos**: puente con la lección anterior y una analogía.
4. Problema chico → fuerza bruta → modelo en Pyomo → **Lectura**. Después el modelo crece: datos en tablas pandas (formato largo, como SQL),
   solución de vuelta a tablas, top 5 de cada pieza, **Lectura para el jefe**.
5. Cada problema lleva:
   - **Las 3 piezas** en palabras (decido, objetivo, restricciones).
   - **En notación**: bloque `$$\begin{aligned} … \end{aligned}$$`, y una tabla de símbolos nuevos (símbolo | se lee | significa | Python/SQL/AMPL) la primera vez que aparecen.
   - **Los dos tamaños**: el modelo (con la función `tamano(m)`: variables, binarias, restricciones y no ceros con `generate_standard_repn`) y el espacio de búsqueda, con notación $O(\cdot)$.
6. Al final: resumen de conceptos (con columna en inglés), **Notación de hoy**, 3 ejercicios, celda vacía, **En la entrevista** (frases en inglés) y **Soluciones**.
- Una celda hace una sola cosa e imprime lo que creó.
- Los números de las celdas **Lectura** salen de ejecutar el notebook. Si hay óptimos alternativos, advertir que los detalles pueden cambiar con la versión de HiGHS.
- La sensibilidad en un MILP se hace por re-solve, no con precios sombra.

## Verificar antes de subir
1. `pip install pyomo "highspy==1.14.0" "ortools==9.15.6755" networkx scipy matplotlib nbconvert ipykernel`
2. Ejecutar cada notebook tocado: `jupyter nbconvert --to notebook --execute notebooks/<x>.ipynb --output-dir <scratchpad> --ExecutePreprocessor.timeout=900`.
   El repo guarda los notebooks **sin salidas**.
3. Validar cada fórmula con KaTeX (`npm install katex`, `katex.renderToString(tex, {throwOnError: true})`).
   En tablas, nunca `|` dentro de una fórmula: usar `\lvert … \rvert`. Decimales con coma: `0{,}83`.
4. Mirar los gráficos (por ejemplo, exportando las imágenes del notebook ejecutado).
5. Formato del JSON: `indent=1`, `ensure_ascii=False`, cada celda con `id`, metadata con `colab.provenance`.
6. Actualizar `notebooks/README.md`: tabla de lecciones, línea "Listas", rama del paso 4, lista de notación y tabla de los dos tamaños.

## Decisiones ya tomadas (no volver a discutir)
- Notación matemática y los dos tamaños en **todo** problema nuevo.
- Calendario comprimido del 3 nov (L5 + L6 juntas, L11 el viernes, L9 + L10 el sábado, un solo simulacro).
- La red de turnos de la L6 es una versión de estudio: un descanso de 30 min (en Siigo eran dos de 15).
