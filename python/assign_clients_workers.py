"""Asignación de clientes a trabajadores con capacidad (MILP, Pyomo + HiGHS).

Port a Python de R/AssignClients_toWorkers_withCapacity.R. El script en R solo
genera los datos; aquí se completa el modelo:

    Conjuntos   C clientes, W trabajadores
    Parámetros  cap[w], A = pares (c, w) permitidos (misma oficina y el cargo
                de w atiende el sub_servicio de c)
    Variables   x[c,w] ∈ {0,1}, u[c] ∈ {0,1} (cliente sin asignar), z ≥ 0 (carga máxima)
    Objetivo    min  M * Σ u[c]  +  z
    Restricc.   Σ_w x[c,w] + u[c] = 1           ∀c
                Σ_c x[c,w] ≤ cap[w]             ∀w
                Σ_c x[c,w] ≤ z * cap[w]         ∀w   (min-max de utilización)

Puntos de entrevista:
- u[c] con penalización grande vuelve el modelo siempre factible (elastic model).
- z linealiza min max_w (carga_w / cap_w).
- Objetivo ponderado: M debe dominar a z (z ≤ 1, así que M = 10 basta).
"""
import numpy as np
import pandas as pd
import pyomo.environ as pyo

rng = np.random.default_rng(23)

N_CLIENTES, N_TRABAJADORES, N_OFICINAS = 600, 40, 5
N_SUBSERVICIOS, CARGOS = 10, list("ABCD")

# Cada oficina tiene al menos un trabajador por cargo; el resto se reparte al azar
base = [(o, c) for o in range(N_OFICINAS) for c in CARGOS]
extra = N_TRABAJADORES - len(base)
trabajadores = pd.DataFrame({
    "id": range(N_TRABAJADORES),
    "oficina": [o for o, _ in base] + list(rng.integers(0, N_OFICINAS, extra)),
    "cargo": [c for _, c in base] + list(rng.choice(CARGOS, extra)),
})
capacidad_cargo = dict(zip(CARGOS, rng.choice(range(30, 65, 5), len(CARGOS))))
trabajadores["capacidad"] = trabajadores["cargo"].map(capacidad_cargo)

clientes = pd.DataFrame({
    "id": range(N_CLIENTES),
    "oficina": rng.integers(0, N_OFICINAS, N_CLIENTES),
    "sub_servicio": rng.integers(0, N_SUBSERVICIOS, N_CLIENTES),
})

# Cada sub_servicio lo pueden atender 2 cargos
estructura = pd.DataFrame(
    [(s, c) for s in range(N_SUBSERVICIOS) for c in rng.choice(CARGOS, 2, replace=False)],
    columns=["sub_servicio", "cargo"],
)

# Pares permitidos: generarlos con un join evita crear 600 x 30 variables inútiles
pares = (
    clientes.merge(estructura, on="sub_servicio")
    .merge(trabajadores, on=["oficina", "cargo"], suffixes=("_c", "_w"))
)
A = list(zip(pares["id_c"], pares["id_w"]))
cap = trabajadores.set_index("id")["capacidad"].to_dict()

m = pyo.ConcreteModel()
m.C = pyo.Set(initialize=clientes["id"].tolist())
m.W = pyo.Set(initialize=trabajadores["id"].tolist())
m.A = pyo.Set(initialize=A, dimen=2)
m.x = pyo.Var(m.A, within=pyo.Binary)
m.u = pyo.Var(m.C, within=pyo.Binary)
m.z = pyo.Var(within=pyo.NonNegativeReals)

por_cliente = pares.groupby("id_c")["id_w"].apply(list).to_dict()
por_trabajador = pares.groupby("id_w")["id_c"].apply(list).to_dict()

m.asignar = pyo.Constraint(
    m.C, rule=lambda m, c: sum(m.x[c, w] for w in por_cliente.get(c, [])) + m.u[c] == 1
)
m.capacidad = pyo.Constraint(
    m.W, rule=lambda m, w: sum(m.x[c, w] for c in por_trabajador.get(w, [])) <= cap[w]
)
m.balance = pyo.Constraint(
    m.W, rule=lambda m, w: sum(m.x[c, w] for c in por_trabajador.get(w, [])) <= m.z * cap[w]
)
M = 10
m.obj = pyo.Objective(expr=M * pyo.quicksum(m.u[c] for c in m.C) + m.z, sense=pyo.minimize)

res = pyo.SolverFactory("appsi_highs").solve(m)
print("Estado:", res.solver.termination_condition)
print(f"Variables x: {len(A)} (vs {N_CLIENTES * N_TRABAJADORES} sin filtrar)")

sin_asignar = int(sum(pyo.value(m.u[c]) for c in m.C))
carga = pd.Series({w: sum(pyo.value(m.x[c, w]) for c in por_trabajador.get(w, [])) for w in m.W})
util = (carga / pd.Series(cap)).round(2)
print(f"Clientes sin asignar: {sin_asignar}")
print(f"Utilización máxima z: {pyo.value(m.z):.2f}")
print("Utilización por trabajador (describe):")
print(util.describe().round(2).to_string())

# Ejercicios:
# 1. Agrega continuidad: bonifica mantener al cliente con su asesor histórico.
# 2. Cambia el objetivo ponderado por lexicográfico: primero min Σu, fija ese
#    valor como restricción y luego min z. Compara resultados.
# 3. ¿Cuántos clientes quedan sin asignar si capacidad baja 20 %? ¿Qué oficina falla?
