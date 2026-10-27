"""Asignación de trabajadores a turnos diarios (Pyomo + HiGHS).

Port a Python de R/AssingWorkers_toShifts.R:

    Variables   x[t,d] ∈ {0,1}   trabajador t cubre el día d (solo si está disponible)
    Objetivo    min Σ salario[t] * x[t,d]
    Restricc.   Σ_t x[t,d] = requerimiento[d]       ∀d
                Σ_d x[t,d] ≤ max_dias               ∀t   (nuevo: no está en R)

El script en R descarta días infactibles antes de resolver (su bloque "IIS").
Aquí se hace igual y luego se resuelve la relajación LP para leer precios sombra:
el dual de la restricción de un día dice cuánto sube el costo si ese día
pide una persona más.
"""
import numpy as np
import pandas as pd
import pyomo.environ as pyo

rng = np.random.default_rng(23)

N_DIAS, N_TRAB, MAX_DIAS = 60, 30, 42
salario = rng.integers(10, 25, N_TRAB)
requerimiento = rng.integers(N_TRAB - 10, N_TRAB - 5, N_DIAS)
disponible = rng.choice([0, 1], size=(N_TRAB, N_DIAS), p=[0.2, 0.8])

# Chequeo de factibilidad por día (equivalente al bloque IIS del script en R)
factible = disponible.sum(axis=0) >= requerimiento
print(f"Días infactibles descartados: {(~factible).sum()} de {N_DIAS}")
dias = [d for d in range(N_DIAS) if factible[d]]
pares = [(t, d) for t in range(N_TRAB) for d in dias if disponible[t, d]]


def construir(binario: bool) -> pyo.ConcreteModel:
    m = pyo.ConcreteModel()
    m.P = pyo.Set(initialize=pares, dimen=2)
    m.x = pyo.Var(m.P, within=pyo.Binary if binario else pyo.UnitInterval)
    m.cubrir = pyo.Constraint(
        dias, rule=lambda m, d: sum(m.x[t, d] for t in range(N_TRAB) if (t, d) in m.P) == requerimiento[d]
    )
    m.max_dias = pyo.Constraint(
        range(N_TRAB), rule=lambda m, t: sum(m.x[t, d] for d in dias if (t, d) in m.P) <= MAX_DIAS
    )
    m.obj = pyo.Objective(expr=sum(salario[t] * m.x[t, d] for t, d in pares), sense=pyo.minimize)
    return m


mip = construir(binario=True)
res = pyo.SolverFactory("appsi_highs").solve(mip)
print("MILP:", res.solver.termination_condition, "costo =", round(pyo.value(mip.obj), 1))

lp = construir(binario=False)
lp.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
pyo.SolverFactory("appsi_highs").solve(lp)
print("LP:  costo =", round(pyo.value(lp.obj), 1), "(gap de integralidad = MILP - LP)")

duales = pd.Series({d: lp.dual[lp.cubrir[d]] for d in dias}, name="precio_sombra")
print("\nDías más caros de cubrir (precio sombra de 1 persona extra):")
print(duales.sort_values(ascending=False).head(5).round(2).to_string())

dias_trab = pd.Series({t: sum(pyo.value(mip.x[t, d]) for d in dias if (t, d) in mip.P) for t in range(N_TRAB)})
print("\nTrabajadores en el tope de días:", int((dias_trab >= MAX_DIAS).sum()))

# Ejercicios:
# 1. ¿Por qué aquí el LP casi siempre da entero? (pista: estructura de flujo /
#    matriz totalmente unimodular sin la restricción max_dias).
# 2. Agrega "no más de 6 días seguidos" con ventanas deslizantes.
# 3. En vez de descartar días infactibles, agrega holgura penalizada.
