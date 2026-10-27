"""Simulated annealing vs MILP: una máquina, retraso total ponderado (1||Σ wT).

Idea para la entrevista: el MILP da el óptimo y una cota (gap), pero crece mal.
La metaheurística no garantiza nada, pero escala y es fácil de adaptar a reglas
raras del negocio. En instancias pequeñas se mide la metaheurística contra el
óptimo; en las grandes se reporta contra la mejor cota del MILP.
"""
import math
import time

import numpy as np
import pyomo.environ as pyo

rng = np.random.default_rng(23)
N = 10
p = rng.integers(2, 10, N)              # duración
w = rng.integers(1, 5, N)               # peso (prioridad del cliente)
d = rng.integers(5, int(p.sum() * 0.6), N)  # fecha de entrega


def costo(seq):
    t, total = 0, 0
    for j in seq:
        t += p[j]
        total += w[j] * max(0, t - d[j])
    return total


def simulated_annealing(iters=20000, T0=50.0, alfa=0.9995, seed=0):
    r = np.random.default_rng(seed)
    actual = list(np.argsort(d))        # arranque: regla EDD (earliest due date)
    c_act = costo(actual)
    mejor, c_mejor, T = actual[:], c_act, T0
    for _ in range(iters):
        i, k = sorted(r.choice(N, 2, replace=False))
        vecino = actual[:]
        vecino[i], vecino[k] = vecino[k], vecino[i]   # vecindad: swap
        c_vec = costo(vecino)
        delta = c_vec - c_act
        # acepta peores soluciones con probabilidad e^(-delta/T) para salir de óptimos locales
        if delta <= 0 or r.random() < math.exp(-delta / T):
            actual, c_act = vecino, c_vec
            if c_act < c_mejor:
                mejor, c_mejor = actual[:], c_act
        T *= alfa
    return mejor, c_mejor


def milp():
    """Formulación disyuntiva con big-M: y[i,j]=1 si i va antes de j."""
    M = int(p.sum())
    J = range(N)
    m = pyo.ConcreteModel()
    m.C = pyo.Var(J, within=pyo.NonNegativeReals)   # tiempo de fin
    m.T = pyo.Var(J, within=pyo.NonNegativeReals)   # retraso
    m.y = pyo.Var([(i, j) for i in J for j in J if i < j], within=pyo.Binary)
    m.c = pyo.ConstraintList()
    for j in J:
        m.c.add(m.C[j] >= p[j])
        m.c.add(m.T[j] >= m.C[j] - d[j])
    for i in J:
        for j in J:
            if i < j:
                m.c.add(m.C[j] >= m.C[i] + p[j] - M * (1 - m.y[i, j]))
                m.c.add(m.C[i] >= m.C[j] + p[i] - M * m.y[i, j])
    m.obj = pyo.Objective(expr=sum(w[j] * m.T[j] for j in J))
    pyo.SolverFactory("appsi_highs").solve(m)
    return pyo.value(m.obj)


t0 = time.time()
seq, c_sa = simulated_annealing()
t_sa = time.time() - t0
t0 = time.time()
c_opt = milp()
t_milp = time.time() - t0

print(f"EDD (regla simple): {costo(list(np.argsort(d)))}")
print(f"SA:   {c_sa}  ({t_sa:.2f} s)  secuencia {[int(j) for j in seq]}")
print(f"MILP: {c_opt:.0f}  ({t_milp:.2f} s)")
print(f"Gap SA vs óptimo: {100 * (c_sa - c_opt) / max(c_opt, 1):.1f} %")

# Ejercicios:
# 1. Con N=10 el MILP ya tarda ~40 s y el SA <1 s. Sube N a 12 y 15: ¿qué pasa
#    con el MILP (usa un time limit y mira el gap)? ¿y con el SA?
# 2. Prueba otra vecindad (insertar un trabajo en otra posición) y compara.
# 3. Corre el SA con 10 semillas y reporta media y peor caso: así se presenta
#    una metaheurística con honestidad.
