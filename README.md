# OperationResearch_withR
Basic Operation Research examples solved with packages from R.

sources:
 - https://ampl.com/resources/the-ampl-book/chapter-downloads/
 - https://www.gurobi.com/documentation/9.1/examples/a_list_of_the_grb_examples.html
 - http://roi.r-forge.r-project.org/introduction.html

R folder contains the following examples: 

 - Allocation of clients to workers with capacity.

## Python (Pyomo, OR-Tools, scikit-learn, SimPy)

`python/` contains Python versions of the R models plus practice cases:

| Script | Topic |
|---|---|
| `assign_clients_workers.py` | Client-to-worker assignment MILP with capacity and min-max balancing (port of the R example) |
| `assign_workers_shifts.py` | Worker-to-shift MILP, LP relaxation and shadow prices (port of the R example) |
| `jobshop_cpsat.py` | Job shop scheduling with OR-Tools CP-SAT |
| `sa_scheduling.py` | Simulated annealing vs exact MILP for single-machine weighted tardiness |
| `simulation_scenarios.py` | SimPy discrete-event simulation + Monte Carlo scenario comparison |
| `rul_maintenance.py` | Predict-then-optimize: remaining-useful-life model feeding a maintenance MILP |
| `cartera_simulada.py` | Simulated portfolio-to-advisor allocation: weighted vs lexicographic objective and a small Pareto front |
| `turnos_red.py` | Shift scheduling with breaks as a network-flow MILP (each agent's shift is a path) |

```bash
pip install -r requirements.txt
python python/assign_clients_workers.py
```

`interview_prep/` holds study notes for a modelling & optimization data science interview.

`notebooks/` holds step-by-step lessons in Spanish, from a 2-variable LP to larger models (see `notebooks/README.md`). `diagramas/` holds the shift-network diagram (SVG, PNG and draw.io).
