# Simulacro de 45 minutos (en inglés)

Formato: 5 partes con tiempo fijo. Contesta en voz alta, con papel para formular.
Debajo de cada pregunta están los **puntos clave** de una buena respuesta, con tus números. No los leas antes de contestar.

| Parte | Tiempo | Qué evalúa |
|---|---|---|
| 1. Tú y tu trabajo | 7 min | pitch, una historia con resultados |
| 2. Formulación en vivo: batería | 15 min | modelar desde cero, en voz alta, en orden |
| 3. ML + optimización | 10 min | validación, incertidumbre, predict-then-optimize |
| 4. Preguntas rápidas de IO | 8 min | teoría que debe salir sin pensar |
| 5. Comportamiento y cierre | 5 min | trabajo con negocio, tus preguntas |

---

## Parte 1 · 7 min: tú y tu trabajo

**1.1** *"Walk me through your background in two minutes."*
- Ingeniero industrial, MSc en Estadística e IO (UPC). Unos 8 años.
- 3 MILP en producción: Siigo (6 h → 7 min, 5 países), Banco Agrario (2 días → 15 min), y la asignación de leads.
- Construyes también lo de alrededor: validación de datos, paquetes en R, APIs.
- Cierra con por qué este cargo: predicción + optimización en industria; empezaste en planeación en Ajover.

**1.2** *"Tell me about the model you're most proud of."* (elige Siigo o Banco Agrario)
- Siigo en 80 s (`09_red_siigo.md`): una red por persona, camino = horario, reglas en la red, cobertura como restricción lateral con falta penalizada → plan de contratación.
- Termina con el número: 6 h → 7 min.
- Seguimiento probable: *"How did you handle infeasibility?"* → cobertura elástica: la falta penalizada nunca deja el modelo infactible y dice dónde falta gente.

---

## Parte 2 · 15 min: formulación en vivo

> *"We operate a 10 MW / 20 MWh battery and trade it in the day-ahead market. Tomorrow's hourly prices are forecast.
> Round-trip efficiency is about 90 %. How would you decide when to charge and discharge? Formulate the model."*

Responde en el orden de siempre: **decisiones → objetivo → restricciones → tamaño → si no escala → cómo lo valido**.

### Puntos clave
**Decisiones** (por hora t = 1..24): `c_t` MW de carga, `d_t` MW de descarga, `s_t` MWh guardados al final de la hora.

**Objetivo:** max `Σ_t p_t·(d_t − c_t) − k·Σ_t d_t`. El segundo término es el desgaste (por ejemplo 4 €/MWh descargado). Sin él, el modelo cicla por ganancias mínimas.

**Restricciones:**
- Balance: `s_t = s_{t−1} + η_c·c_t − d_t/η_d`, con `η_c = η_d = 0,95`. Es la conservación de flujo de la lección 5, en el tiempo: la batería es un inventario.
- Límites: `0 ≤ c_t, d_t ≤ 10` y `0 ≤ s_t ≤ 20`.
- Estado final: `s_24 = s_0`. Si no, el modelo vacía la batería al final del día porque mañana "no existe".
- Cargar y descargar a la vez: con precios positivos el LP no lo hace (pierde energía). Con la batería llena y precios muy negativos sí podría, para quemar energía cobrando. Si pasa, se agrega una binaria `u_t`: `c_t ≤ 10·u_t`, `d_t ≤ 10·(1 − u_t)`. **Primero el LP; la binaria solo si hace falta.**

**Tamaño:** 72 variables continuas y unas 25 restricciones: un LP que resuelve en milisegundos. El espacio de decisiones es continuo; lo difícil no es el tamaño.

**Lo difícil es el pronóstico.** Con los precios de `python/bateria_arbitraje.py`:
- El plan carga en la noche y al mediodía (precio solar bajo, una hora negativa) y vende en los picos de la mañana y la tarde: **4.147 € por día**.
- Cobrado contra 200 días con error de pronóstico de 25 €/MWh por hora: 4.198 € de media. Con el precio real conocido se ganarían 5.446 €.
- **Un pronóstico perfecto valdría hasta 1.247 € por día** (unos 450.000 € al año). Es el EVPI de la lección 8: dice cuánto invertir en el modelo de precios.

**Si te piden más** (los seguimientos típicos):
- *"Prices are uncertain."* → escenarios de precio desde los errores del pronóstico (lección 11) y un modelo de 2 etapas: el día siguiente se compromete en el mercado diario (1ª etapa), y se ajusta en intradía o balance (2ª etapa, recurso). Evaluar fuera de la muestra.
- *"Add a solar plant behind the meter."* → nueva entrada al balance: la batería carga con solar propia; límite de conexión a la red `|d_t − c_t + solar_t| ≤ capacidad`.
- *"Degradation depends on cycles."* → costo por MWh descargado (lineal) o límite de ciclos por día `Σ d_t ≤ 2·20`. Profundidad de descarga real → por tramos (lineal a trozos).
- *"Many batteries and a grid constraint."* → índice por batería y una restricción común de red por nodo; el dual de esa restricción es el precio nodal (lección 5).

**Cómo lo valido:** backtest con precios reales de los últimos 12 meses: ingreso del plan contra la estrategia actual del operador (por ejemplo, regla de "carga en las 4 horas más baratas"); revisar con el trader los días raros.

---

## Parte 3 · 10 min: ML + optimización

**3.1** *"How would you build the price forecast that feeds this model?"*
- Baseline primero: el precio de la misma hora de la semana pasada (naive estacional).
- Gradient boosting con features: hora, día, festivos, pronóstico de viento y solar, demanda, precio de gas y CO₂, rezagos del precio.
- Validación **en el tiempo** (rolling origin), nunca mezclando días futuros en train: fuga de datos.
- Métrica: además del MAE, el **ingreso de la batería** con el pronóstico. Lo que importa es acertar el orden de las horas (cuáles son baratas y caras), no cada precio.

**3.2** *"Your quantile forecast says P10, but reality falls below it 20 % of the time. What do you do?"*
- Es el caso de la lección 11: cobertura de 81 % en vez de 90 %. Calibración conformal con errores fuera de la muestra (allí, corrida de 4 días).
- Vigilar la cobertura en producción: si se cae, reentrenar.

**3.3** *"Tell me about a project combining ML and optimization."*
- La lección 11, contada como caso: RUL de multiplicadoras con boosting → MILP de mantenimiento con cuadrillas.
- Tres puntos: `GroupKFold` (10 contra 15 días); escenarios desde los errores, no el punto; evaluar por costo de la decisión (13 a 21 % más barato que el punto).

---

## Parte 4 · 8 min: preguntas rápidas (20–30 s cada una)

| Pregunta | Debe salir |
|---|---|
| Why is MILP harder than LP? | No convexo; branch & bound sobre relajaciones LP; NP-difícil |
| What is the gap? | (mejor solución − mejor cota) / mejor solución; lo peor que puede pasar |
| Why is big-M bad? | Relajación débil: con y = 0,5 las dos ramas se aflojan M/2 (L7: cota 0 contra 6) |
| Shadow price? | Cambio del objetivo por unidad de lado derecho, dentro del rango; holgura → 0 |
| Why does an assignment solve fast? | Matriz totalmente unimodular: el LP ya da enteros |
| CP-SAT or MILP for job shop? | CP-SAT: intervalos y NoOverlap; MILP indexado en el tiempo si el tiempo es grueso |
| Your model is too slow. | Formulación, gap y límite de tiempo, warm start, reducir, descomponer |
| Benders in one sentence. | Maestro con las decisiones de hoy + θ; subproblemas LP por escenario; cortes desde los duales; parar cuando las cotas se juntan |
| Weighted sum vs ε-constraint? | Ponderado esconde tasas de cambio y no ve puntos no soportados (L10: 2 de 5) |
| Infeasible model? | Revisar datos; holguras penalizadas; IIS |

---

## Parte 5 · 5 min: comportamiento y cierre

**5.1** *"A planner doesn't trust your model's output. What do you do?"*
- Reproducir con el modelo decisiones pasadas que el planner reconoce; mostrar el trade-off con escenarios; dejarlo modificar y registrar los cambios; medir lado a lado.
- Ejemplo real: Ajover. La planificación fallaba por datos de entrada; tu validación automática hizo que se adoptara.

**5.2** *"Do you have questions for us?"* Usa 2 de `05_sector.md`:
- What decisions does the team support today, and which one would my first project target?
- How are models deployed: inside existing digital products, or as standalone tools for planners?

---

## Rúbrica para evaluarte (1 a 3 por fila)

| Criterio | 1 | 3 |
|---|---|---|
| Orden al formular | saltó a las restricciones | decisiones → objetivo → restricciones → tamaño → escala → validación |
| Números propios | respuestas genéricas | cada respuesta con un número tuyo o de las lecciones |
| Incertidumbre | ignoró el pronóstico | habló de escenarios, valor del pronóstico y evaluación fuera de la muestra |
| Claridad | más de 2 min por respuesta | 30–90 s, empieza por la conclusión |
| Negocio | solo técnica | conectó con ingreso, riesgo, adopción y validación con usuarios |

Total ≥ 12 de 15: listo. Menos: repite solo las preguntas donde sacaste 1.
