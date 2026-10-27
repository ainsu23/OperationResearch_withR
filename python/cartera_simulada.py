"""Asignación de cartera a asesores con datos simulados: varias metas a la vez.

Ejemplo genérico para comparar formas de combinar metas en un MILP.

    Conjuntos   C clientes, A asesores, P ⊆ A×C pares factibles (perfil, segmento, región)
    Variables   x[a,c] ∈ {0,1};  z[s] ≥ 0 carga máxima de un asesor Junior en el segmento s
    Valor       V(x) = Σ saldo[c] · w[tipo(a)] · (1 + 0,5·continuidad[a,c]) · x[a,c]
    Restricc.   Σ_a x[a,c] ≤ 1                          ∀c
                Σ_c x[a,c] ≤ ⌈cap[t] · f[a]⌉            ∀a      capacidad total
                Σ_{c∈e} x[a,c] ≤ ⌈cap[t,e] · f[a]⌉      ∀a,e    capacidad por etapa
                Σ_{c∈s} x[a,c] ≤ z[s]                   ∀a Junior, s

Compara dos formas de combinar las metas:
    ponderada       max V(x) − 1000 · Σz
    lexicográfica   paso 1: V* = max V(x)
                    paso 2: min Σz  s.a.  V(x) ≥ (1 − ε) · V*,  Σx ≥ asignados del paso 1
Con saldos en pesos, una asignación vale millones y la penalización es 1000:
el balance solo desempata. Si la ponderada no llega al óptimo exacto, el
gap del solver (0,01 %) es mayor que todo el término de balance.
"""
import math
import time

import numpy as np
import pandas as pd
import pyomo.environ as pyo

rng = np.random.default_rng(23)

N_CLIENTES = 1200
REGIONES = ["NORTE", "CENTRO", "SUR"]
ETAPAS = ["Temprana", "Media", "Tardia"]
SEGMENTOS = ["MICRO_A", "MICRO_B", "PYME", "EMPRESA"]
SEGMENTOS_MICRO = ["MICRO_A", "MICRO_B"]

PESO = {"Senior": 3, "Gestor": 2, "Junior": 1}  # prioridad por tipo de asesor
BONO_CONTINUIDAD = 0.5                           # +50 % si el cliente sigue con su asesor anterior
PENALIZACION_BALANCE = 1000
CAP_TOTAL = {"Senior": 70, "Gestor": 90, "Junior": 110}
CAP_ETAPA = {
    "Senior": {"Temprana": 30, "Media": 40, "Tardia": 30},
    "Gestor": {"Media": 60, "Tardia": 50},
    "Junior": {"Temprana": 80, "Media": 60},
}

# ---- Datos simulados ----
asesores = pd.DataFrame(
    [(f"S{i:02d}", "Senior", REGIONES[i % 3]) for i in range(6)]
    + [(f"G{i:02d}", "Gestor", None) for i in range(6)]
    + [(f"J{i:02d}", "Junior", None) for i in range(10)],
    columns=["asesor", "tipo", "region"],
)
# disponibilidad: 1 normal, 0.5 vacaciones parciales, 0 licencia
asesores["factor"] = rng.choice([1.0, 0.5, 0.0], len(asesores), p=[0.8, 0.15, 0.05])

clientes = pd.DataFrame({
    "cliente": [f"C{i:04d}" for i in range(N_CLIENTES)],
    "region": rng.choice(REGIONES, N_CLIENTES),
    "etapa": rng.choice(ETAPAS, N_CLIENTES, p=[0.45, 0.35, 0.20]),
    "segmento": rng.choice(SEGMENTOS, N_CLIENTES, p=[0.35, 0.25, 0.20, 0.20]),
    "saldo": np.round(rng.lognormal(np.log(3e6), 1.0, N_CLIENTES), -3),  # pesos
})

# Pares factibles con un cross join + filtros (formulación dispersa)
pares = clientes.merge(asesores, how="cross", suffixes=("_c", "_a"))
senior = (pares.tipo == "Senior") & (pares.region_c == pares.region_a)
gestor = (pares.tipo == "Gestor") & pares.etapa.isin(["Media", "Tardia"])
junior = (pares.tipo == "Junior") & pares.segmento.isin(SEGMENTOS_MICRO) & pares.etapa.isin(["Temprana", "Media"])
pares = pares[senior | gestor | junior].reset_index(drop=True)

# Asesor anterior: 60 % factible, 10 % no factible (el bono no aplica), 30 % sin asesor anterior
factibles = pares.groupby("cliente")["asesor"].apply(list)
anterior = {}
for c in clientes.cliente:
    u = rng.random()
    if u < 0.6:
        anterior[c] = str(rng.choice(factibles[c]))
    elif u < 0.7:
        anterior[c] = str(rng.choice(asesores.asesor))
clientes["anterior"] = clientes.cliente.map(anterior)
pares["cont"] = pares.asesor == pares.cliente.map(anterior)

con_anterior = clientes.anterior.notna().sum()
cont_factible = pares.loc[pares["cont"], "cliente"].nunique()
print(f"Clientes: {N_CLIENTES} | asesores: {len(asesores)} | pares factibles: {len(pares)} "
      f"(vs {N_CLIENTES * len(asesores)} sin filtrar)")
print(f"Con asesor anterior: {con_anterior}; de ellos sin par factible (el bono no aplica): "
      f"{con_anterior - cont_factible}")


def capacidad(tipo, factor, etapa=None):
    base = CAP_TOTAL[tipo] if etapa is None else CAP_ETAPA[tipo][etapa]
    return math.ceil(base * factor)


def construir(escala_saldo=1.0):
    """Modelo con el valor V(x) como Expression; el objetivo se agrega afuera."""
    P = list(zip(pares.asesor, pares.cliente))
    coef = pares.saldo / escala_saldo * pares.tipo.map(PESO) * (1 + BONO_CONTINUIDAD * pares["cont"])
    m = pyo.ConcreteModel()
    m.P = pyo.Set(initialize=P, dimen=2)
    m.x = pyo.Var(m.P, within=pyo.Binary)
    m.z = pyo.Var(SEGMENTOS_MICRO, within=pyo.NonNegativeReals)
    m.valor = pyo.Expression(expr=pyo.quicksum(k * m.x[p] for p, k in zip(P, coef)))

    m.unico = pyo.ConstraintList()
    for _, g in pares.groupby("cliente"):
        m.unico.add(pyo.quicksum(m.x[a, c] for a, c in zip(g.asesor, g.cliente)) <= 1)

    m.cap = pyo.ConstraintList()
    for (a, t, f), g in pares.groupby(["asesor", "tipo", "factor"]):
        m.cap.add(pyo.quicksum(m.x[a, c] for c in g.cliente) <= capacidad(t, f))
        for e, ge in g.groupby("etapa"):
            m.cap.add(pyo.quicksum(m.x[a, c] for c in ge.cliente) <= capacidad(t, f, e))

    m.balance = pyo.ConstraintList()
    for (a, s), g in pares[pares.tipo == "Junior"].groupby(["asesor", "segmento"]):
        m.balance.add(pyo.quicksum(m.x[a, c] for c in g.cliente) <= m.z[s])
    return m


def resolver(m):
    t0 = time.time()
    res = pyo.SolverFactory("appsi_highs").solve(m)
    return str(res.solver.termination_condition), time.time() - t0


def metricas(m, nombre, estado, seg):
    x = np.array([pyo.value(m.x[a, c]) > 0.5 for a, c in zip(pares.asesor, pares.cliente)])
    asig = pares[x]
    valor = (asig.saldo * asig.tipo.map(PESO) * (1 + BONO_CONTINUIDAD * asig["cont"])).sum()
    jun = asig[asig.tipo == "Junior"]
    activos = asesores.loc[(asesores.tipo == "Junior") & (asesores.factor > 0), "asesor"]
    carga = jun.groupby("asesor").size().reindex(activos, fill_value=0)
    return {
        "version": nombre,
        "estado": estado,
        "seg": round(seg, 1),
        "valor (×10⁹)": round(valor / 1e9, 3),
        "Σz": int(jun.groupby(["asesor", "segmento"]).size().groupby(level="segmento").max().sum()),
        "carga Junior min-max": f"{carga.min()}-{carga.max()}",
        "% continuidad": round(100 * asig["cont"].sum() / cont_factible, 1),
        "sin asignar": N_CLIENTES - asig.cliente.nunique(),
    }


resultados = []

# ---- Ponderada: saldo en pesos, penalización 1000
m = construir()
m.obj = pyo.Objective(expr=m.valor - PENALIZACION_BALANCE * pyo.quicksum(m.z.values()), sense=pyo.maximize)
resultados.append(metricas(m, f"ponderada λ={PENALIZACION_BALANCE}", *resolver(m)))
coef_mediano = (pares.saldo * pares.tipo.map(PESO)).median()
print(f"Valor mediano de una asignación: {coef_mediano:.1e} | penalización por unidad de z: "
      f"{PENALIZACION_BALANCE} | razón: {coef_mediano / PENALIZACION_BALANCE:.0e}")

# ---- Lexicográfica: saldo en millones para que la fila V(x) ≥ ... quede bien escalada
m = construir(escala_saldo=1e6)
m.obj1 = pyo.Objective(expr=m.valor, sense=pyo.maximize)
estado, seg = resolver(m)
v_estrella = pyo.value(m.valor)
resultados.append(metricas(m, "lex paso 1 (solo valor)", estado, seg))
n_asignados = sum(pyo.value(v) > 0.5 for v in m.x.values())
m.obj1.deactivate()
m.obj2 = pyo.Objective(expr=pyo.quicksum(m.z.values()), sense=pyo.minimize)
# Sin este piso, el paso 2 baja la carga dejando clientes sin asignar:
# cada meta que importa necesita su propia restricción.
m.cobertura = pyo.Constraint(expr=pyo.quicksum(m.x.values()) >= n_asignados)
for eps, proteger in [(0.0, True), (0.001, True), (0.01, True), (0.01, False)]:
    m.del_component("piso")
    # 1e-7 de holgura numérica para que la solución del paso 1 siga siendo factible
    m.piso = pyo.Constraint(expr=m.valor >= (1 - eps - 1e-7) * v_estrella)
    m.cobertura.activate() if proteger else m.cobertura.deactivate()
    nombre = f"lex paso 2 ε={eps:.1%}" + ("" if proteger else " SIN piso de cobertura")
    resultados.append(metricas(m, nombre, *resolver(m)))

print()
print(pd.DataFrame(resultados).to_string(index=False))

# Ejercicios:
# 1. Sube PENALIZACION_BALANCE a la escala de una asignación (~1e6) y compara
#    con la lexicográfica. ¿Por qué es frágil elegir λ a mano?
# 2. Balancea por saldo en vez de número de clientes. ¿Cambia quién queda más cargado?
# 3. Cambia el min-max por penalizar la desviación respecto a la carga media
#    (|carga − media| linealizado con dos variables ≥ 0).
# 4. Dibuja la frontera de Pareto (valor vs Σz) con más valores de ε: eso es el
#    método ε-constraint, y es lo que le mostrarías a negocio.
