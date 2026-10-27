"""Predict-then-optimize: vida útil remanente (RUL) con ML -> plan de mantenimiento MILP.

1. Datos (1 ciclo = 1 día): degradación simulada de equipos con sensores (estilo NASA C-MAPSS;
   para practicar con datos reales descarga C-MAPSS y reemplaza simular()).
2. ML: gradient boosting para RUL, validado con GroupKFold por equipo.
   Validar por fila filtraría información (el mismo equipo en train y test).
3. Incertidumbre: un modelo de cuantil 10 % da un RUL "pesimista".
4. Optimización: asignar a cada equipo un día de mantenimiento antes de su RUL
   pesimista, con capacidad de cuadrilla diaria, minimizando la vida útil que
   se desperdicia por intervenir temprano + penalización si no cabe.
"""
import numpy as np
import pandas as pd
import pyomo.environ as pyo
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold

rng = np.random.default_rng(23)


def simular(n_equipos: int, censurar: bool) -> pd.DataFrame:
    filas = []
    for e in range(n_equipos):
        vida = rng.integers(120, 300)
        tasa = rng.uniform(0.6, 1.4)
        fin = rng.integers(40, vida - 10) if censurar else vida
        for t in range(fin):
            dano = (t / vida) ** 2 * tasa
            filas.append({
                "equipo": e, "ciclo": t, "rul": vida - t,
                "temp": 600 + 40 * dano + rng.normal(0, 3),
                "presion": 30 - 6 * dano + rng.normal(0, 0.5),
                "vibracion": 0.2 + 1.5 * dano + rng.normal(0, 0.08),
            })
    df = pd.DataFrame(filas)
    # features de ventana: tendencia reciente por equipo (sin mirar al futuro)
    for s in ["temp", "presion", "vibracion"]:
        g = df.groupby("equipo")[s]
        df[f"{s}_m10"] = g.transform(lambda x: x.rolling(10, min_periods=1).mean())
        df[f"{s}_d10"] = g.transform(lambda x: x.diff(10)).fillna(0)
    return df


train = simular(100, censurar=False)
X_cols = [c for c in train.columns if c not in ("equipo", "rul")]
X, y, grupos = train[X_cols], train["rul"].clip(upper=150), train["equipo"]

# --- 2. validación cruzada agrupada por equipo
maes = []
for tr, te in GroupKFold(n_splits=5).split(X, y, grupos):
    mod = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05).fit(X.iloc[tr], y.iloc[tr])
    maes.append(mean_absolute_error(y.iloc[te], mod.predict(X.iloc[te])))
print(f"MAE GroupKFold: {np.mean(maes):.1f} ± {np.std(maes):.1f} ciclos (RUL recortado a 150)")

modelo = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05).fit(X, y)
modelo_q10 = HistGradientBoostingRegressor(loss="quantile", quantile=0.10, max_iter=300, learning_rate=0.05).fit(X, y)

# --- 3. flota en operación: último ciclo observado de cada equipo
flota = simular(25, censurar=True).groupby("equipo").tail(1).set_index("equipo")
flota["rul_pred"] = modelo.predict(flota[X_cols]).round()
flota["rul_q10"] = np.clip(modelo_q10.predict(flota[X_cols]).round(), 1, None)
cobertura = (flota["rul"] >= flota["rul_q10"]).mean()
print(f"Cobertura real del cuantil 10 % en la flota: {cobertura:.0%} (ideal ~90 %)")

# --- 4. MILP de mantenimiento en los próximos H días
H, CUADRILLA, PEN_FALLA = 60, 1, 1000
E, D = flota.index.tolist(), range(1, H + 1)
limite = flota["rul_q10"].to_dict()

m = pyo.ConcreteModel()
m.x = pyo.Var(E, D, within=pyo.Binary)       # mantener equipo e el día d
m.f = pyo.Var(E, within=pyo.Binary)          # no cabe antes del límite (riesgo de falla)
m.uno = pyo.Constraint(E, rule=lambda m, e: sum(m.x[e, d] for d in D) + m.f[e] == 1)
m.cap = pyo.Constraint(D, rule=lambda m, d: sum(m.x[e, d] for e in E) <= CUADRILLA)
# no se puede programar después del RUL pesimista
for e in E:
    for d in D:
        if d > limite[e]:
            m.x[e, d].fix(0)
# equipos con RUL > H no necesitan mantenimiento en este horizonte: f no penaliza
m.obj = pyo.Objective(expr=sum(
    (min(limite[e], H) - d) * m.x[e, d] for e in E for d in D
) + sum((PEN_FALLA if limite[e] <= H else 0) * m.f[e] for e in E))
pyo.SolverFactory("appsi_highs").solve(m)

plan = pd.DataFrame({
    "rul_real": flota["rul"], "rul_pred": flota["rul_pred"], "rul_q10": flota["rul_q10"],
    "dia": [next((d for d in D if pyo.value(m.x[e, d]) > 0.5), None) for e in E],
}, index=E)
urgentes = plan[plan["rul_q10"] <= H].sort_values("rul_q10")
print(f"\nEquipos que requieren mantenimiento en {H} días: {len(urgentes)}")
print(urgentes.to_string())
fallas = int((urgentes["dia"].isna()).sum())
tarde = int((urgentes["dia"] > urgentes["rul_real"]).sum())
print(f"Sin cupo: {fallas} | programados después de la falla real: {tarde}")

# Ejercicios:
# 1. Usa rul_pred en vez de rul_q10 como límite: ¿cuántos quedan tarde? Ese es
#    el argumento de negocio para modelar incertidumbre.
# 2. Sube CUADRILLA a 2 y mide cuánta vida útil desperdiciada se ahorra
#    (= valor de contratar otra cuadrilla).
# 3. La cobertura del cuantil 10 % sale por debajo del 90 %. ¿Por qué? (pista:
#    la flota está censurada y su distribución difiere de train). Calíbralo con
#    conformal prediction o un buffer y vuelve a medir los equipos tarde.
# 4. Explica el modelo con permutation importance o SHAP.
