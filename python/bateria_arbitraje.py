"""Caso del simulacro: una batería que compra y vende en el mercado diario (arbitraje).

Batería de 10 MW y 20 MWh (2 horas). Eficiencia de 95 % al cargar y 95 % al descargar (90 % ida y vuelta).
Precios por hora del día siguiente (€/MWh), con forma típica: noche barata, pico de la mañana,
valle al mediodía por la solar (una hora con precio negativo) y pico de la tarde.

Decisiones por hora t:  c_t = MW que carga, d_t = MW que descarga, s_t = MWh guardados.
    max  Σ_t p_t·(d_t − c_t) − 4·Σ_t d_t                 (4 €/MWh de desgaste por energía descargada)
    s.a. s_t = s_{t−1} + 0,95·c_t − d_t / 0,95            (balance de energía)
         0 ≤ c_t, d_t ≤ 10,  0 ≤ s_t ≤ 20,  s_0 = s_24 = 10
    Con la batería llena y varias horas de precio muy negativo, el LP podría cargar y descargar a la vez
    para "quemar" energía cobrando. La binaria u_t (1 = carga, 0 = descarga) lo impide:
    c_t ≤ 10·u_t,  d_t ≤ 10·(1 − u_t). En este día no pasa: el LP y el MILP dan lo mismo.
    Regla: primero resuelve el LP y revisa; agrega la binaria solo si hace falta.

Corre: python python/bateria_arbitraje.py
"""
import logging

import numpy as np
import pyomo.environ as pyo

logging.getLogger("pyomo.contrib.appsi").setLevel(logging.ERROR)
SOLVER = pyo.SolverFactory("appsi_highs")

PRECIOS = [72, 65, 60, 58, 60, 75, 110, 140, 125, 95, 70, 45,
           20, -15, 10, 40, 80, 130, 175, 160, 120, 100, 90, 80]
P_MAX, E_MAX, EF, DESGASTE, S0 = 10, 20, 0.95, 4, 10


def bateria(precios, binaria=False):
    T = range(len(precios))
    m = pyo.ConcreteModel()
    m.c = pyo.Var(T, bounds=(0, P_MAX))
    m.d = pyo.Var(T, bounds=(0, P_MAX))
    m.s = pyo.Var(T, bounds=(0, E_MAX))
    m.obj = pyo.Objective(expr=sum(precios[t] * (m.d[t] - m.c[t]) - DESGASTE * m.d[t] for t in T), sense=pyo.maximize)
    m.balance = pyo.Constraint(T, rule=lambda m, t: m.s[t] == (S0 if t == 0 else m.s[t - 1]) + EF * m.c[t] - m.d[t] / EF)
    m.final = pyo.Constraint(expr=m.s[len(precios) - 1] == S0)
    if binaria:
        m.u = pyo.Var(T, within=pyo.Binary)
        m.solo_carga = pyo.Constraint(T, rule=lambda m, t: m.c[t] <= P_MAX * m.u[t])
        m.solo_descarga = pyo.Constraint(T, rule=lambda m, t: m.d[t] <= P_MAX * (1 - m.u[t]))
    SOLVER.solve(m)
    return m


def resumen(m, nombre):
    c = np.array([pyo.value(m.c[t]) for t in m.c])
    d = np.array([pyo.value(m.d[t]) for t in m.d])
    a_la_vez = [t for t in range(len(c)) if c[t] > 1e-6 and d[t] > 1e-6]
    print(f"{nombre}: ganancia {pyo.value(m.obj):,.0f} € | carga {c.sum():.1f} MWh | descarga {d.sum():.1f} MWh | "
          f"horas cargando y descargando a la vez: {a_la_vez}".replace(",", "."))
    print("   hora:  " + " ".join(f"{t:>3}" for t in range(24)))
    print("   neto:  " + " ".join(f"{d[t] - c[t]:>3.0f}" for t in range(24)) + "   (+ vende, − compra, MW)")


if __name__ == "__main__":
    print("Precios:", PRECIOS)
    resumen(bateria(PRECIOS), "LP")
    resumen(bateria(PRECIOS, binaria=True), "MILP con binaria")

    # Incertidumbre: el plan se hace con el pronóstico, pero se cobra el precio real.
    rng = np.random.default_rng(11)
    plan = bateria(PRECIOS)
    neto = np.array([pyo.value(plan.d[t]) - pyo.value(plan.c[t]) for t in plan.c])
    desgaste = DESGASTE * sum(pyo.value(plan.d[t]) for t in plan.d)
    reales, perfectos = [], []
    for _ in range(200):
        real = np.array(PRECIOS) + rng.normal(0, 25, 24)  # error del pronóstico: 25 €/MWh por hora
        reales.append(float(real @ neto - desgaste))
        perfectos.append(pyo.value(bateria(list(real)).obj))
    eur = lambda x: f"{x:,.0f}".replace(",", ".") + " €"
    print(f"Plan hecho con el pronóstico, cobrado en 200 días reales: {eur(np.mean(reales))} de media "
          f"(promete {eur(pyo.value(plan.obj))}) | si se conociera el precio real: {eur(np.mean(perfectos))}")
    print(f"Lo máximo que vale un pronóstico perfecto: {eur(np.mean(perfectos) - np.mean(reales))} por día")
