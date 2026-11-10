"""Descomposición de Benders con el problema de repuestos de la lección 8.

Problema (2 etapas):
    Hoy compro q módulos a 40.000 € cada uno.
    En cada invierno s (probabilidad π_s) fallan D_s módulos; lo que falte se trae de urgencia a 250.000 €.
    min 40 q + Σ_s π_s · 250 · e_s    s.a.  q + e_s ≥ D_s,  e_s ≥ 0,  q entero (en miles de €)

Benders lo parte en dos:
    Maestro:      min 40 q + θ   s.a. los cortes que ha recibido   (θ = lo que el maestro cree que costarán las urgencias)
    Subproblema:  para cada invierno, con q fijo: min 250 e_s  s.a.  e_s ≥ D_s − q   → costo y precio sombra λ_s
    Corte:        θ ≥ Σ_s π_s · λ_s · (D_s − q)

Corre: python python/benders_repuestos.py
"""
import logging

import numpy as np
import pyomo.environ as pyo

logging.getLogger("pyomo.contrib.appsi").setLevel(logging.ERROR)
SOLVER = pyo.SolverFactory("appsi_highs")
COMPRA, URGENCIA = 40, 250  # miles de €
ESCENARIOS = {"suave": (0.4, 0), "normal": (0.4, 2), "duro": (0.2, 6)}  # (probabilidad, fallas)


def subproblema(q, fallas):
    """Un invierno con q fijo. Devuelve (costo de urgencias, precio sombra de 'q + e ≥ D')."""
    m = pyo.ConcreteModel()
    m.e = pyo.Var(within=pyo.NonNegativeReals)
    m.obj = pyo.Objective(expr=URGENCIA * m.e, sense=pyo.minimize)
    m.cubre = pyo.Constraint(expr=q + m.e >= fallas)
    m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    SOLVER.solve(m)
    return pyo.value(m.obj), m.dual[m.cubre]


def maestro(cortes):
    """min 40 q + θ con los cortes recibidos. Cada corte es una lista de (π_s, λ_s, D_s)."""
    m = pyo.ConcreteModel()
    m.q = pyo.Var(within=pyo.NonNegativeIntegers, bounds=(0, 8))
    m.theta = pyo.Var(within=pyo.NonNegativeReals)  # las urgencias nunca cuestan menos de 0
    m.obj = pyo.Objective(expr=COMPRA * m.q + m.theta, sense=pyo.minimize)
    m.cortes = pyo.ConstraintList()
    for corte in cortes:
        m.cortes.add(m.theta >= sum(p * lam * (d - m.q) for p, lam, d in corte))
    SOLVER.solve(m)
    return round(pyo.value(m.q)), pyo.value(m.theta), pyo.value(m.obj)


def benders(max_iter=10):
    cortes, mejor = [], float("inf")
    for it in range(1, max_iter + 1):
        q, theta, cota_inferior = maestro(cortes)
        respuestas = {s: subproblema(q, d) for s, (p, d) in ESCENARIOS.items()}
        urgencias = sum(ESCENARIOS[s][0] * costo for s, (costo, _) in respuestas.items())
        mejor = min(mejor, COMPRA * q + urgencias)  # cota superior: un plan real, evaluado de verdad
        corte = [(p, respuestas[s][1], d) for s, (p, d) in ESCENARIOS.items()]
        pendiente = -sum(p * lam for p, lam, _ in corte)
        independiente = sum(p * lam * d for p, lam, d in corte)
        print(f"Iteración {it}: maestro propone q = {q} (cree que las urgencias cuestan {abs(theta):.0f}) | "
              f"cota inferior {cota_inferior:.0f} | urgencias reales {urgencias:.0f} | cota superior {mejor:.0f}")
        print(f"   precios sombra λ: { {s: round(lam) for s, (_, lam) in respuestas.items()} } "
              f"→ corte θ ≥ {independiente:.0f} {pendiente:+.0f}·q")
        if mejor - cota_inferior < 1e-6:
            print(f"Óptimo: comprar {q} módulos, costo esperado {mejor:.0f} mil €")
            return
        cortes.append(corte)


def benders_montecarlo(n=10_000, semilla=999, max_iter=30):
    """Lo mismo con n inviernos de Monte Carlo (lección 8). El subproblema de cada invierno es tan simple
    que su costo y su precio sombra se calculan con numpy: 250 si falta algo, 0 si no."""
    rng = np.random.default_rng(semilla)
    tipo = rng.choice(3, size=n, p=[0.5, 0.35, 0.15])
    fallas = rng.poisson(np.array([1.0, 3.0, 7.0])[tipo])
    cortes, mejor = [], float("inf")  # cortes agregados: θ ≥ a − b·q
    for it in range(1, max_iter + 1):
        m = pyo.ConcreteModel()
        m.q = pyo.Var(within=pyo.NonNegativeIntegers, bounds=(0, 30))
        m.theta = pyo.Var(within=pyo.NonNegativeReals)
        m.obj = pyo.Objective(expr=COMPRA * m.q + m.theta, sense=pyo.minimize)
        m.cortes = pyo.ConstraintList()
        for a, b in cortes:
            m.cortes.add(m.theta >= a - b * m.q)
        SOLVER.solve(m)
        q, cota_inferior = round(pyo.value(m.q)), pyo.value(m.obj)
        falta = fallas > q
        lam = np.where(falta, URGENCIA, 0.0)  # precio sombra de cada invierno
        urgencias = (URGENCIA * np.maximum(fallas - q, 0)).mean()
        mejor = min(mejor, COMPRA * q + urgencias)
        print(f"Iteración {it}: q = {q:>2} | cota inferior {cota_inferior:6.1f} | cota superior {mejor:6.1f}")
        if mejor - cota_inferior < 1e-6:
            print(f"Óptimo con {n:,} inviernos".replace(",", ".") + f": comprar {q} módulos, {mejor:.1f} mil €. "
                  "El maestro nunca tuvo más de 2 variables.")
            return
        cortes.append(((lam * fallas).mean(), lam.mean()))


if __name__ == "__main__":
    print("== 3 escenarios ==")
    benders()
    print("\n== 10.000 inviernos de Monte Carlo ==")
    benders_montecarlo()
