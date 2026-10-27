"""Job shop scheduling con OR-Tools CP-SAT.

Contexto: un taller de equipos para energía. Piezas (forjados, válvulas, conectores) que pasan por
máquinas en un orden fijo. Minimizar el makespan.

Por qué CP-SAT y no MILP: con big-M para "la tarea i va antes o después de j"
la relajación LP es muy débil. CP-SAT razona sobre intervalos directamente
(NoOverlap) y suele ganar en scheduling puro.
"""
from collections import defaultdict

from ortools.sat.python import cp_model

# trabajo -> lista de (máquina, duración en horas), en orden de ruta
TRABAJOS = {
    "valvula_1": [(0, 3), (1, 2), (2, 2)],
    "valvula_2": [(0, 2), (2, 1), (1, 4)],
    "conector_1": [(1, 4), (2, 3)],
    "conector_2": [(2, 2), (0, 3), (1, 1)],
    "forjado_1": [(0, 5), (1, 2)],
}
# Fecha de entrega por trabajo (horas). Usada en el ejercicio 2.
ENTREGA = {"valvula_1": 10, "valvula_2": 12, "conector_1": 9, "conector_2": 11, "forjado_1": 14}

horizonte = sum(d for ruta in TRABAJOS.values() for _, d in ruta)
m = cp_model.CpModel()

tareas = {}
por_maquina = defaultdict(list)
for j, ruta in TRABAJOS.items():
    for k, (maq, dur) in enumerate(ruta):
        ini = m.new_int_var(0, horizonte, f"ini_{j}_{k}")
        fin = m.new_int_var(0, horizonte, f"fin_{j}_{k}")
        intervalo = m.new_interval_var(ini, dur, fin, f"int_{j}_{k}")
        tareas[j, k] = (ini, fin, maq, dur)
        por_maquina[maq].append(intervalo)
    # precedencia dentro de la ruta
    for k in range(len(ruta) - 1):
        m.add(tareas[j, k + 1][0] >= tareas[j, k][1])

for intervalos in por_maquina.values():
    m.add_no_overlap(intervalos)

makespan = m.new_int_var(0, horizonte, "makespan")
m.add_max_equality(makespan, [tareas[j, len(r) - 1][1] for j, r in TRABAJOS.items()])
m.minimize(makespan)

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10
estado = solver.solve(m)
print("Estado:", solver.status_name(estado), "| makespan =", solver.value(makespan), "h")

for maq in sorted(por_maquina):
    fila = sorted(
        (solver.value(ini), solver.value(fin), j)
        for (j, k), (ini, fin, mq, _) in tareas.items() if mq == maq
    )
    print(f"Máquina {maq}: " + "  ".join(f"[{a}-{b}] {j}" for a, b, j in fila))

for j, r in TRABAJOS.items():
    fin = solver.value(tareas[j, len(r) - 1][1])
    print(f"{j:11s} termina en {fin:2d} h, entrega {ENTREGA[j]:2d} h, retraso {max(0, fin - ENTREGA[j])} h")

# Ejercicios:
# 1. Escribe el mismo problema como MILP con big-M (y[i,j] binaria de orden) en
#    Pyomo y compara tiempo de solución al duplicar el número de trabajos.
# 2. Cambia el objetivo a minimizar el retraso total ponderado usando ENTREGA.
# 3. Agrega un tiempo de setup de 1 h cuando cambia el tipo de pieza en una máquina.
