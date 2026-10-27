# Python + SQL cronometrado

Regla: 10 min por ejercicio, en un editor sin autocompletado, hablando en inglés mientras escribes.
Soluciones abajo; no mires antes.

## Python (pandas / numpy)
1. DataFrame `ops(equipo, fecha, horas_operacion, falla)`. Para cada equipo calcula MTBF = horas totales / número de fallas. Equipos sin fallas → `inf`.
2. Misma tabla: agrega una columna con la media móvil de 7 días de `horas_operacion` por equipo, sin usar datos futuros.
3. Escribe `knapsack(valores, pesos, cap)` con programación dinámica. Devuelve el valor óptimo.
4. Dada una lista de tareas `(inicio, fin)`, devuelve el número mínimo de cuadrillas necesarias (intervalos que se solapan).
5. Formula y resuelve en Pyomo: 3 plantas con capacidad, 4 clientes con demanda, costo unitario de transporte. Minimiza el costo (problema de transporte).

## SQL
6. `pedidos(id, cliente, fecha, monto)`: top 3 clientes por monto en cada mes.
7. Misma tabla: para cada pedido, días desde el pedido anterior del mismo cliente.
8. `sensores(equipo, ts, valor)`: última lectura de cada equipo.
9. Porcentaje del monto acumulado de cada cliente sobre el total (Pareto 80/20).
10. `turnos(empleado, fecha)`: rachas de días consecutivos trabajados por empleado (gaps and islands).

---

## Soluciones

```python
# 1
g = ops.groupby("equipo").agg(h=("horas_operacion", "sum"), f=("falla", "sum"))
g["mtbf"] = g["h"] / g["f"].replace(0, np.nan)
g["mtbf"] = g["mtbf"].fillna(np.inf)

# 2
ops = ops.sort_values(["equipo", "fecha"])
ops["h_m7"] = ops.groupby("equipo")["horas_operacion"].transform(lambda s: s.rolling(7, min_periods=1).mean())

# 3
def knapsack(v, w, cap):
    dp = [0] * (cap + 1)
    for vi, wi in zip(v, w):
        for c in range(cap, wi - 1, -1):   # al revés: cada ítem una sola vez
            dp[c] = max(dp[c], dp[c - wi] + vi)
    return dp[cap]

# 4
import heapq
def cuadrillas(tareas):
    fines = []
    for ini, fin in sorted(tareas):
        if fines and fines[0] <= ini:
            heapq.heapreplace(fines, fin)
        else:
            heapq.heappush(fines, fin)
    return len(fines)

# 5
import pyomo.environ as pyo
cap = {"A": 50, "B": 60, "C": 40}
dem = {1: 30, 2: 40, 3: 35, 4: 25}
c = {(p, k): v for (p, k), v in zip([(p, k) for p in cap for k in dem],
                                    [4, 6, 9, 5, 5, 4, 7, 6, 8, 7, 4, 3])}
m = pyo.ConcreteModel()
m.x = pyo.Var(cap, dem, within=pyo.NonNegativeReals)
m.o = pyo.Objective(expr=sum(c[p, k] * m.x[p, k] for p in cap for k in dem))
m.cap = pyo.Constraint(cap, rule=lambda m, p: sum(m.x[p, k] for k in dem) <= cap[p])
m.dem = pyo.Constraint(dem, rule=lambda m, k: sum(m.x[p, k] for p in cap) >= dem[k])
pyo.SolverFactory("appsi_highs").solve(m)
```

```sql
-- 6
WITH t AS (
  SELECT cliente, DATE_TRUNC('month', fecha) AS mes, SUM(monto) AS total
  FROM pedidos GROUP BY 1, 2
)
SELECT * FROM (
  SELECT t.*, RANK() OVER (PARTITION BY mes ORDER BY total DESC) AS r FROM t
) x WHERE r <= 3;

-- 7
SELECT id, cliente, fecha,
       fecha - LAG(fecha) OVER (PARTITION BY cliente ORDER BY fecha) AS dias_desde_anterior
FROM pedidos;

-- 8
SELECT equipo, ts, valor FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY equipo ORDER BY ts DESC) AS rn FROM sensores s
) x WHERE rn = 1;

-- 9
WITH c AS (SELECT cliente, SUM(monto) AS total FROM pedidos GROUP BY 1)
SELECT cliente, total,
       SUM(total) OVER (ORDER BY total DESC) / SUM(total) OVER () AS pct_acumulado
FROM c ORDER BY total DESC;

-- 10
WITH g AS (
  SELECT empleado, fecha,
         fecha - (ROW_NUMBER() OVER (PARTITION BY empleado ORDER BY fecha))::int AS grupo
  FROM turnos
)
SELECT empleado, MIN(fecha) AS inicio, MAX(fecha) AS fin, COUNT(*) AS dias
FROM g GROUP BY empleado, grupo ORDER BY empleado, inicio;
```
