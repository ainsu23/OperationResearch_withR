# Ejercicios de formulación (contexto energía / industria)

Método en la entrevista, siempre en este orden y en voz alta:
1. Decisiones (variables) → 2. Objetivo → 3. Restricciones → 4. Tamaño del modelo → 5. Qué hago si no escala → 6. Cómo lo valido con negocio.

Intenta cada uno en papel 15 min antes de mirar la solución.

---

## 1. Barcos de instalación a proyectos offshore
Proyectos `p` con duración `dur_p` y ventana `[a_p, b_p]`; barcos `v` con costo diario `c_v` y compatibilidad `ok_{pv}`; tiempo discreto `t`.
- `x_{pvt} ∈ {0,1}`: el proyecto p empieza en t con el barco v.
- min `Σ c_v·dur_p·x_{pvt}` + penalización por retraso.
- `Σ_{v,t} x_{pvt} = 1` ∀p (solo pares compatibles y `t ∈ [a_p, b_p − dur_p]`).
- No solapamiento por barco: `Σ_p Σ_{s=t−dur_p+1}^{t} x_{pvs} ≤ 1` ∀v,t.
- Clima: elimina los t de inicio cuyo intervalo cruza días sin ventana de clima.
- **Escala:** formulación indexada en el tiempo = relajación fuerte pero muchas variables. Alternativa: generación de columnas (cada columna = itinerario de un barco).

## 2. Job shop con setups
Ver `python/jobshop_cpsat.py`. Versión MILP:
- `S_{jk}` inicio de la operación k del trabajo j; `y_{ij}^m ∈ {0,1}` orden en la máquina m.
- `S_i ≥ S_j + p_j + s_{ji} − M·y_{ij}`, `S_j ≥ S_i + p_i + s_{ij} − M·(1 − y_{ij})`.
- Precedencia en la ruta, `C_max ≥ S_{j,last} + p_{j,last}`.
- **Clave:** big-M débil; M = horizonte ajustado. En la práctica: CP-SAT o heurística + MILP local.

## 3. Repuestos críticos multi-bodega
Bodegas `w`, plataformas `i`, ítems `k`; demanda rara (Poisson).
- `s_{wk}` stock entero; `y_{iwk} ∈ {0,1}` bodega w cubre i para k.
- min `Σ h_k·s_{wk}` + `Σ costo_envío·y`.
- `Σ_w y_{iwk} = 1`; `T_{iw} ≤ T_max` si `y = 1`.
- Nivel de servicio: precalcula `s_min(λ, fill rate)` por bodega y linealiza con binarias por nivel `z_{wkn}` (`s_{wk} = Σ n·z_{wkn}`).
- **Mencionar:** el nivel de servicio no es lineal en el stock → discretizar o separar en dos etapas.

## 4. Ubicación de bases logísticas (capacitated facility location)
- `y_j ∈ {0,1}` abrir base j; `x_{ij} ≥ 0` fracción de la demanda de i servida por j.
- min `Σ f_j y_j + Σ c_{ij} d_i x_{ij}`.
- `Σ_j x_{ij} = 1`; `Σ_i d_i x_{ij} ≤ Q_j y_j`; **desigualdad fuerte:** `x_{ij} ≤ y_j` (mejora mucho la relajación LP).

## 5. Ingenieros a proyectos con skills
- `x_{ep} ∈ {0,1}`; `h_{ep}` horas.
- max `Σ valor_p · cubierto_p` − costo.
- Skills: `Σ_{e con skill s} h_{ep} ≥ req_{ps}·cubierto_p`.
- Capacidad: `Σ_p h_{ep} ≤ H_e`; `h_{ep} ≤ H_e·x_{ep}`; máx. proyectos por persona `Σ_p x_{ep} ≤ 3`.
- Es tu caso Siigo/Banco Agrario: cuéntalo así.

## 6. Mantenimiento con RUL
Ver `python/rul_maintenance.py`. Extensión estocástica de 2 etapas:
- 1ª etapa: `x_{ed}` día planeado. 2ª etapa, por escenario de RUL `ω`: `f_{eω}` falla si `d > RUL_{eω}`.
- min `Σ costo_temprano·x + Σ_ω π_ω Σ_e c_falla f_{eω}`.
- `f_{eω} ≥ Σ_{d > RUL_{eω}} x_{ed}`.
- **Mensaje:** el cuantil fijo es una aproximación; los escenarios capturan el trade-off real entre costo y riesgo.

---

## Linealizaciones que debes escribir sin pensar
| Necesitas | Lineal |
|---|---|
| `z = x·y`, x,y binarias | `z ≤ x`, `z ≤ y`, `z ≥ x + y − 1` |
| `z = x·y`, x binaria, `0 ≤ y ≤ U` | `z ≤ U·x`, `z ≤ y`, `z ≥ y − U(1 − x)` |
| `min max_i f_i` | `min t`, `t ≥ f_i` |
| `|a|` en el objetivo (min) | `a = a⁺ − a⁻`, min `a⁺ + a⁻` |
| Either-or: `g₁ ≤ 0` o `g₂ ≤ 0` | `g₁ ≤ M·δ`, `g₂ ≤ M(1 − δ)` |
| Costo fijo si `x > 0` | `x ≤ U·y`, costo `f·y` |
| `x ∈ {0} ∪ [L, U]` (semi-continua) | `L·y ≤ x ≤ U·y` |
| Al menos k de n restricciones | `g_i ≤ M(1 − δ_i)`, `Σ δ_i ≥ k` |
