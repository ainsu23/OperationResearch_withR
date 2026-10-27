# Plan de preparación — Senior Data Scientist (modelado y optimización), sector energía

Entrevista técnica: **11 nov 2026**. Estudio: lun 26 oct – mar 10 nov (16 días).
Supuesto: ~2 h entre semana, ~4 h fin de semana.

## 1. CV contra la oferta

### Dónde encajas fuerte
| Requisito | Tu evidencia |
|---|---|
| Optimización en producción | 3 MILP desplegados: Banco Agrario 2025 (Pyomo, 2 días → 15 min), Siigo (AMPL+R+Python, 14 restricciones, 5 países, 6 h → 7 min), Banco Agrario 2020 (ompr, 80 h/mes → automatizado) |
| Formación | MSc Estadística e IO (UPC) + Ing. Industrial |
| 5+ años | 8+ años |
| Industrial / manufactura (nice to have) | Ajover: Master Planning y Detail Scheduling |
| Stakeholders | Consultores, directores, 5 países |
| SQL, datos no estructurados | SQL 7+ años; RAG sobre PDFs; extracción de facturas con LLM |
| Ubicación | Vives en la ciudad del cargo; permiso de trabajo en la UE |

### Brechas (aquí va el estudio)
1. **ML: la más grande.** El CV dice "1 yr" y no tiene un proyecto predictivo con métricas. La oferta pone ML primero. → `python/rul_maintenance.py` se vuelve tu caso.
2. **Python vs R.** La entrevista será en Python. → todos los scripts de `python/`.
3. **Metaheurísticas.** → `python/sa_scheduling.py`.
4. **Simulación / escenarios / digital twin.** → `python/simulation_scenarios.py`.
5. **Producción / MLOps** (Docker, CI/CD, tests, MLflow, monitoreo). → día 5 nov.
6. **Seniority** ("Leadership 1 yr"). → historias STAR de influencia.

### Arreglos rápidos al CV
- "Artiﬁtial" → "Artificial".
- Fechas solapadas: Ajover 03/2017–05/2021 y Banco Agrario 08/2020–07/2021. Ten lista la explicación.
- "Profesional Senior Analytics" → "Senior Analytics Professional".
- Hueco desde 07/2026: una frase (mudanza a Polonia, estudio, proyectos).
- Python primero en Skills; agrega Git, Pyomo, HiGHS/Gurobi, OR-Tools, scikit-learn.

## 2. Qué esperar
- Formular un MILP en vivo con contexto industrial.
- Teoría de IO: linealizaciones, dualidad, B&B, gap, multiobjetivo, escalabilidad.
- ML: validación, leakage, métricas, gradient boosting, incertidumbre.
- Predict-then-optimize.
- Python + SQL.
- Despliegue de un optimizador como servicio.
- Contexto del sector y de la empresa.

## 3. Calendario (actualizado el 27 oct)
El calendario anterior tenía los días de la semana corridos en uno: el 26 de octubre fue lunes. La entrevista es el **miércoles 11 de noviembre**.

Desde el 27 de octubre sigues la ruta de `notebooks/README.md`: una lección por día, de modelos pequeños a grandes.

| Fecha | Lección o bloque | Material de apoyo |
|---|---|---|
| Lun 26 oct | Pitch + historias STAR | `01_star_stories.md` |
| Mar 27 | L1: tu primer modelo (programa lineal) | `notebooks/01_primer_modelo.ipynb` |
| Mié 28 | L2: cuánto vale una hora más (sensibilidad) | `03_question_bank.md` §A |
| Jue 29 | L3: decisiones sí/no (variables binarias) | `02_formulation_drills.md` (linealizaciones) |
| Vie 30 | L4: asignación (la estructura de tu modelo de cartera) | `07_conceptos.md` §1 |
| Sáb 31 | L5: redes y flujo | `07_conceptos.md` §1 |
| Dom 1 nov | L6: tu red de turnos de Siigo | `09_red_siigo.md`, `diagramas/red_turnos_siigo.png` |
| Lun 2 | L7: secuenciación (máquinas y barcos) | `python/jobshop_cpsat.py`, `08_modelos_sector.md` |
| Mar 3 | L8: incertidumbre (simulación y escenarios) | `python/simulation_scenarios.py` |
| Mié 4 | L9: heurísticas contra el óptimo | `python/sa_scheduling.py` |
| Jue 5 | L10: varias metas (ponderado, lexicográfico, Pareto) | `python/cartera_simulada.py`, `07_conceptos.md` §2–5 |
| Vie 6 | L11: ML + optimización (RUL → mantenimiento) | `python/rul_maintenance.py` |
| Sáb 7 | ML, estadística y producción + Python/SQL cronometrado | `03_question_bank.md` §B–D, `04_coding_drills.md` |
| Dom 8 | Simulacro 1: formulación en vivo + ML | — |
| Lun 9 | Simulacro 2: caso completo + contexto del sector | `05_sector.md` |
| Mar 10 | Repaso ligero, STAR en voz alta. Dormir bien | `01_star_stories.md` |
| Mié 11 | Entrevista | — |

Para los simulacros puedes pedirme: "hazme una entrevista técnica de 45 min para este cargo, en inglés, una pregunta a la vez".

## Analogía para contar tu perfil
Un MILP es el GPS: te da la mejor ruta con las calles que conoce. El ML es el reporte del tráfico: predice cómo estarán las calles. La empresa busca a alguien que construya los dos y los conecte. Tus 3 MILP prueban que sabes hacer el GPS. El caso RUL → mantenimiento prueba que sabes conectarlo con el pronóstico.
