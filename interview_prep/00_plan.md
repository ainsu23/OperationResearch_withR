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
5. **Producción / MLOps** (Docker, CI/CD, tests, MLflow, monitoreo). → dom 8 nov.
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

## 3. Calendario (actualizado el 10 nov)
El 26 de octubre fue lunes. La entrevista es el **miércoles 11 de noviembre**.

Desde el 27 de octubre sigues la ruta de `notebooks/README.md`: una lección por día, de modelos pequeños a grandes.

**Ajuste del 3 nov.** El 31 oct, el 1 y el 2 nov no hubo estudio: 3 lecciones atrás. Para no perder lo importante:
- L5 y L6 van juntas en un notebook (`05_redes_y_turnos.ipynb`).
- L11 (ML + optimización) sube al viernes y tiene un día completo: es la brecha más grande.
- L9 y L10 van juntas el sábado: ya tienes los scripts.
- Los 2 simulacros quedan en 1.

**Ajuste del 7 nov.** La L8 y la L11 pasan del viernes al sábado. Hoy van las 4 lecciones que faltan (unas 6 h 30), en este orden:

| Bloque | Lección | Notebook | Tiempo |
|---|---|---|---|
| 1 | L8: incertidumbre (escenarios, 2 etapas, Monte Carlo, simulación) | `notebooks/07_incertidumbre.ipynb` | 1 h 45 |
| 2 | L11: ML + optimización (RUL → mantenimiento). Es la brecha más grande y usa la L8 | `notebooks/10_ml_y_optimizacion.ipynb` | 1 h 45 |
| 3 | L9: heurísticas contra el óptimo | `notebooks/08_heuristicas.ipynb` | 1 h 30 |
| 4 | L10: varias metas (ponderado, lexicográfico, Pareto) | `notebooks/09_varias_metas.ipynb` | 1 h 30 |

Si no alcanza: la sección 6 de la L10 (la cartera de Banco Agrario, que ya conoces) pasa al domingo a primera hora. Lo demás de hoy no se mueve.

### Hecho
| Fecha | Lección o bloque |
|---|---|
| Lun 26 oct | Pitch + historias STAR |
| Mar 27 | L1: tu primer modelo (programa lineal) |
| Mié 28 | L2: cuánto vale una hora más (sensibilidad) |
| Jue 29 | L3: decisiones sí/no (variables binarias) |
| Vie 30 | L4: asignación (la estructura de tu modelo de cartera) |

### Lo que falta
| Fecha | Lección o bloque | Material de apoyo |
|---|---|---|
| Mar 3 nov | L5 + L6: redes y tu red de turnos de Siigo | `notebooks/05_redes_y_turnos.ipynb`, `09_red_siigo.md`, `diagramas/red_turnos_siigo.png` |
| Mié 4 | L7: secuenciación (máquinas y barcos) | `notebooks/06_secuenciacion.ipynb`, `python/jobshop_cpsat.py`, `08_modelos_sector.md` |
| Sáb 7 (6 h 30) | L8 → L11 → L9 → L10 (ver el ajuste del 7 nov). La L8 y la L11 vienen del jueves y el viernes | `notebooks/07_incertidumbre.ipynb`, `10_ml_y_optimizacion.ipynb`, `08_heuristicas.ipynb`, `09_varias_metas.ipynb`; apoyo: `07_conceptos.md` §2–5 |
| Mar 10 (3 h 45) | Las sesiones del domingo, el lunes y el martes, juntas: ML y producción, código, simulacro, STAR, hoja final. Dormir bien | `10_dia_final.md`, `11_simulacro.md`, `12_hoja_final.md` |
| Mié 11 | Entrevista | — |

Para los simulacros puedes pedirme: "hazme una entrevista técnica de 45 min para este cargo, en inglés, una pregunta a la vez".

## Analogía para contar tu perfil
Un MILP es el GPS: te da la mejor ruta con las calles que conoce. El ML es el reporte del tráfico: predice cómo estarán las calles. La empresa busca a alguien que construya los dos y los conecte. Tus 3 MILP prueban que sabes hacer el GPS. El caso RUL → mantenimiento prueba que sabes conectarlo con el pronóstico.
