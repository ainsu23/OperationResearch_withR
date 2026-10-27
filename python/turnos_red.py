"""Turnos con descansos como red de flujo (MILP).

Ejemplo genérico inspirado en la línea de Siigo del CV ("network flow,
person-specific connectivity arcs, shifts, breaks, labor rules"). No es el
modelo original: sirve para entender y explicar la técnica.

Idea: el turno de cada agente es un CAMINO en una red de tiempo.
    Nodo (t, k, b)   hora t, k horas seguidas trabajadas, b = ya tomó descanso
    Arcos            inicio  s → (t,0,0)            solo en las horas permitidas al agente
                     trabajo (t,k,b) → (t+1,k+1,b)   si k < MAX_SEGUIDAS
                     descanso (t,k,0) → (t+1,0,1)    si k ≥ MIN_ANTES_DESCANSO
                     fin     (t,k,1) → f             ya descansó y trabajó después
Cualquier camino de s a f es un turno legal: las reglas viven en la red, no en
restricciones. Los arcos de inicio distintos por persona son los "person-specific
connectivity arcs".

    Variables   y[arco] ∈ {0,1};  falta[h], sobra[h] ≥ 0
    Objetivo    min 10·Σ falta + Σ sobra
    Restricc.   conservación de flujo por agente y nodo; 1 unidad sale de s
                Σ arcos de trabajo del agente = horas de contrato
                Σ agentes trabajando en h + falta[h] − sobra[h] = demanda[h]
                agentes en descanso en h ≤ MAX_DESCANSOS

Sin las tres últimas, cada agente es un problema de camino más corto
(matriz de red, totalmente unimodular): el LP daría solución entera.
La cobertura acopla a los agentes y por eso es un MILP.
En AMPL sería igual: set ARCOS; var y {ARCOS} binary; s.t. flujo {...}; etc.
"""
from collections import defaultdict

import pyomo.environ as pyo

H = 16                      # horas de 6:00 a 22:00; el arco de trabajo t cubre la hora 6+t
MAX_SEGUIDAS = 5
MIN_ANTES_DESCANSO = 2
MAX_DESCANSOS = 2           # agentes en descanso a la vez
DEMANDA = [2, 4, 7, 9, 9, 8, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2]

# agente: (horas de contrato, horas de inicio permitidas como índice t)
AGENTES = {
    **{f"TC{i}": (8, range(0, 3)) for i in range(1, 6)},    # tiempo completo mañana: 6:00–8:00
    **{f"TC{i}": (8, range(5, 8)) for i in range(6, 9)},    # tiempo completo tarde: 11:00–13:00
    **{f"MT{i}": (6, range(0, 5)) for i in range(1, 4)},    # medio tiempo: 6:00–10:00
    **{f"ES{i}": (6, range(8, 10)) for i in range(1, 4)},   # estudiantes: 14:00–15:00
}


def generar_arcos():
    """Recorre la red desde los nodos de inicio de cada agente."""
    arcos = []                                  # (agente, tipo, origen, destino, hora)
    for p, (_, inicios) in AGENTES.items():
        pila = [(t, 0, 0) for t in inicios]
        vistos = set(pila)
        arcos += [(p, "inicio", "s", n, None) for n in pila]
        while pila:
            t, k, b = nodo = pila.pop()
            salidas = []
            if t < H and k < MAX_SEGUIDAS:
                salidas.append(("trabajo", (t + 1, k + 1, b), t))
            if t < H and b == 0 and k >= MIN_ANTES_DESCANSO:
                salidas.append(("descanso", (t + 1, 0, 1), t))
            if b == 1 and k >= 1:
                arcos.append((p, "fin", nodo, "f", None))
            for tipo, destino, hora in salidas:
                arcos.append((p, tipo, nodo, destino, hora))
                if destino not in vistos:
                    vistos.add(destino)
                    pila.append(destino)
    return arcos


ARCOS = generar_arcos()


def construir(binario=True):
    m = pyo.ConcreteModel()
    m.A = pyo.RangeSet(0, len(ARCOS) - 1)
    m.y = pyo.Var(m.A, within=pyo.Binary if binario else pyo.UnitInterval)
    m.falta = pyo.Var(range(H), within=pyo.NonNegativeReals)
    m.sobra = pyo.Var(range(H), within=pyo.NonNegativeReals)

    entra, sale = defaultdict(list), defaultdict(list)
    trabajo_h, descanso_h, trabajo_p = defaultdict(list), defaultdict(list), defaultdict(list)
    for i, (p, tipo, o, d, h) in enumerate(ARCOS):
        sale[p, o].append(i)
        entra[p, d].append(i)
        if tipo == "trabajo":
            trabajo_h[h].append(i)
            trabajo_p[p].append(i)
        elif tipo == "descanso":
            descanso_h[h].append(i)

    m.flujo = pyo.ConstraintList()
    for p in AGENTES:
        m.flujo.add(sum(m.y[i] for i in sale[p, "s"]) == 1)
    for (p, n) in set(entra) | set(sale):
        if n not in ("s", "f"):
            m.flujo.add(sum(m.y[i] for i in entra[p, n]) == sum(m.y[i] for i in sale[p, n]))

    m.horas = pyo.Constraint(list(AGENTES), rule=lambda m, p: sum(m.y[i] for i in trabajo_p[p]) == AGENTES[p][0])
    m.cobertura = pyo.Constraint(range(H), rule=lambda m, h: (
        sum(m.y[i] for i in trabajo_h[h]) + m.falta[h] - m.sobra[h] == DEMANDA[h]))
    m.descansos = pyo.Constraint(range(H), rule=lambda m, h: (
        sum(m.y[i] for i in descanso_h[h]) <= MAX_DESCANSOS if descanso_h[h] else pyo.Constraint.Skip))
    m.obj = pyo.Objective(expr=10 * sum(m.falta.values()) + sum(m.sobra.values()))
    return m


print(f"Agentes: {len(AGENTES)} | arcos (variables binarias): {len(ARCOS)} | "
      f"horas contratadas: {sum(h for h, _ in AGENTES.values())} | demanda: {sum(DEMANDA)}")

lp = construir(binario=False)
pyo.SolverFactory("appsi_highs").solve(lp)
fraccionarios = sum(1e-6 < pyo.value(lp.y[i]) < 1 - 1e-6 for i in lp.A)
print(f"LP relajado: objetivo {pyo.value(lp.obj):.1f}, arcos fraccionarios: {fraccionarios}")

m = construir()
res = pyo.SolverFactory("appsi_highs").solve(m)
print(f"MILP: {res.solver.termination_condition}, objetivo {pyo.value(m.obj):.1f}\n")

print("hora   " + "".join(f"{6 + h:>3}" for h in range(H)))
for p in AGENTES:
    fila = ["  ·"] * H
    for i, (q, tipo, _, _, h) in enumerate(ARCOS):
        if q == p and h is not None and pyo.value(m.y[i]) > 0.5:
            fila[h] = "  T" if tipo == "trabajo" else "  D"
    print(f"{p:<7}" + "".join(fila))
cubierto = [round(DEMANDA[h] - pyo.value(m.falta[h]) + pyo.value(m.sobra[h])) for h in range(H)]
print("demanda" + "".join(f"{d:>3}" for d in DEMANDA))
print("cubre  " + "".join(f"{c:>3}" for c in cubierto))
print("falta  " + "".join(f"{round(pyo.value(m.falta[h])):>3}" for h in range(H)))
print("sobra  " + "".join(f"{round(pyo.value(m.sobra[h])):>3}" for h in range(H)))

# Ejercicios:
# 1. Cambia MAX_SEGUIDAS a 4: ¿qué pasa con las opciones de turno de 8 h?
# 2. Agrega un segundo país con otras reglas (p. ej. descanso tras 4 h): basta
#    con generar su red con otros parámetros; el modelo no cambia.
# 3. Agrega habilidades: dos colas (contable y nómina) con demanda propia y
#    agentes que solo atienden una.
# 4. Pasa a bloques de 30 min: la red crece, la formulación es la misma.
