# Pitch + historias STAR (en inglés, para decirlas en voz alta)

Borrador basado en tu CV. Cambia lo que no sea exacto y agrega números que recuerdes.
Cada historia: ~90 segundos. Termina siempre con el número del resultado.

## Pitch de 2 minutos
> I'm an industrial engineer with a master's in Statistics and Operations Research from UPC Barcelona, and about eight years turning data into decisions. My core is prescriptive analytics: I've designed and deployed three mixed-integer optimization models in production — workforce scheduling across five countries, client-to-advisor allocation in a national bank, and lead assignment for a sales force. In each case the measure of success was operational: from six hours to seven minutes, or from two days to fifteen minutes.
> I also build the pieces around the model — data validation pipelines, R packages and APIs — because a model only creates value once people use it. More recently I've worked with LLMs, building a RAG system and an invoice extraction pipeline on AWS Bedrock.
> What attracts me to this role is the combination of prediction and optimization in an industrial setting. I started my career in manufacturing planning at Ajover, and I want to bring that back together with what I've learned since.

## 1. MILP para asignar cartera (Banco Agrario, 2025–2026)
Completa lo que está entre corchetes.
- **S:** At Banco Agrario, the collections team assigned [N] overdue clients to [M] advisors nationwide by hand every cycle. It took about two days, and it was hard to respect stage capacity, continuity and workload balance at the same time.
- **T:** I was asked to automate the allocation so the highest-value clients went to the most strategic advisors without overloading anyone.
- **A:** I built a MILP in Pyomo over [N] feasible advisor–client pairs, pre-filtered by profile, segment and region. Constraints: at most one advisor per client; capacity per advisor, in total and per collection stage, scaled by an availability factor for leave; and a min-max load balance per segment. The objective maximizes the outstanding balance assigned, weighted by advisor hierarchy, with a bonus for keeping the historical advisor.
- **R:** The process went from two days to 15 minutes. [Agrega: % de clientes que mantuvieron su asesor, carga máxima antes/después, desde cuándo lo usan. Ver `07_conceptos.md` §6.]
- **Pregunta de seguimiento probable:** "Why a weighted objective?" → "It was quick to agree with the business in a single model, and the weight ratios are large, so it behaves almost lexicographically. Today I'd make that explicit: maximize value first, then minimize imbalance within a tolerance, and show the business the Pareto front." (`07_conceptos.md` §2, §4 y §5)

## 2. Motor de asignación de personal (Siigo, 2022–2024)
- **S:** Staffing of support agents across 5 countries was done by hand, ~6 hours per run.
- **T:** Automate shift and break assignment respecting labor law.
- **A:** Network-flow MILP in AMPL. Each agent's week was a path through a network of 30-minute nodes: work, breaks, lunch and days off, with one start and one end node per agent. The network and a few side constraints encoded the rules: four start times (7:00–8:30), lunch at one of four times and always one hour, two 15-minute breaks, and eight working hours a day. I only generated the feasible part of each person's network: for example, a known day off had no work nodes. 14 operational constraints covered shifts, breaks and labor rules. R for data engineering, Python for the API, ran in Databricks. Diagrama: `diagramas/red_turnos_siigo.png`.
- **R:** 6 hours → 7 minutes. The unmet demand per block also fed hiring plans. Dashboards in Power BI for model monitoring.
- **Seguimiento:** "How did you handle infeasibility?" → "Coverage was elastic: unmet demand in each block was a penalized slack variable, so the model always returned a schedule. The slack showed where and how many agents were missing, and we used it to plan hiring."
- Tu red real, con la explicación de 60 segundos: `09_red_siigo.md`. Ejemplo genérico de la técnica: `python/turnos_red.py`.

## 3. Calidad de datos que rompía el planificador (Ajover, 2017–2021) → conflicto / influencia
- **S:** Consultants deployed Master Planning and Detail Scheduling; outputs were inconsistent and users stopped trusting them.
- **T:** Find the root cause without formal authority over consultants or data owners.
- **A:** Traced the bad outputs to input data (BOMs, routings, lead times). Built an automated validation pipeline that audited inputs before every run and reported errors to each owner.
- **R:** 100% of inputs validated before each run; plan adopted after a 6-month stabilization period. **Lesson:** most optimization failures are data failures.

## 4. Sistema RAG (Carvajal, 2024–2025) → aprender algo nuevo rápido
- **A:** LangChain + local FAISS for privacy, Q&A over PDF manuals. Semantic cache for the invoice pipeline cut LLM calls. (Prepara: cómo evaluaste la calidad de las respuestas.)

## 5. Refactor de código R 17 → 4 min (Banco Agrario) → calidad de software
- **A:** Profiled, vectorized, removed repeated queries. (Prepara: qué cambiaste exactamente, tests.)

## 6. Error o fracaso
Elige uno real. Estructura: what went wrong → what I did → what I changed in my process. Ejemplo de forma: a model that was optimal on paper but was not used because a rule was missing → now I validate with users on real cases before scaling.

## Preguntas de comportamiento que debes poder responder con estas historias
- Tell me about a time you translated a vague business problem into a model.
- A stakeholder disagreed with your model's output. What did you do?
- How do you decide between a simple heuristic and an exact model?
- Tell me about a project that failed.
- How do you explain a complex model to a non-technical manager?
