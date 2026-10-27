"""Simulación de eventos discretos (SimPy) + Monte Carlo para evaluar escenarios.

Caso: base logística offshore. Llegan barcos de suministro con tiempos
aleatorios y necesitan un muelle para cargar. ¿Cuántos muelles hacen falta para
que la espera media sea menor a 2 h?

Por qué simular y no optimizar: la variabilidad (colas) es el problema. Un
modelo determinista con promedios dice que 2 muelles alcanzan (83 % de uso); la simulación
muestra las colas. La simulación evalúa escenarios ("what-if"); la
optimización elige entre ellos. Juntas forman un digital twin sencillo.
"""
import numpy as np
import simpy

HORAS = 24 * 30                 # un mes
LLEGADA_MEDIA = 3.0             # h entre barcos (exponencial)
CARGA_MEDIA, CARGA_SD = 5.0, 1.5  # h de carga (normal truncada)
REPLICAS = 200


def una_corrida(muelles: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    muelle = simpy.Resource(env, capacity=muelles)
    esperas = []

    def barco(env):
        llegada = env.now
        with muelle.request() as req:
            yield req
            esperas.append(env.now - llegada)
            yield env.timeout(max(0.5, rng.normal(CARGA_MEDIA, CARGA_SD)))

    def generador(env):
        while True:
            yield env.timeout(rng.exponential(LLEGADA_MEDIA))
            env.process(barco(env))

    env.process(generador(env))
    env.run(until=HORAS)
    return float(np.mean(esperas))


print(f"Utilización determinista con 2 muelles: {CARGA_MEDIA / LLEGADA_MEDIA / 2:.0%}")
print(f"{'muelles':>7} {'espera media (h)':>17} {'IC 95%':>16} {'P(media>2h)':>13}")
for k in [2, 3, 4]:
    res = np.array([una_corrida(k, s) for s in range(REPLICAS)])
    media, se = res.mean(), res.std(ddof=1) / np.sqrt(REPLICAS)
    print(f"{k:>7} {media:>17.2f} {f'[{media - 1.96 * se:.2f}, {media + 1.96 * se:.2f}]':>16} {(res > 2).mean():>13.0%}")

# Ejercicios:
# 1. El script ya usa las mismas semillas en cada escenario (common random
#    numbers). Calcula el IC de la diferencia pareada 2 vs 3 muelles y compáralo
#    con semillas distintas por escenario: con CRN el IC es más angosto.
# 2. Agrega cierre por clima: 10 % de los días no se puede cargar.
# 3. Agrega costo por muelle y por hora de espera y elige k que minimiza el costo esperado.
