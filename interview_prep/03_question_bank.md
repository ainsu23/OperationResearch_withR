# Banco de preguntas (en inglés, con respuesta corta)

Practica en voz alta. Respuesta ideal: 30–60 s, con un ejemplo tuyo cuando se pueda.

## A. Optimización

1. **LP vs MILP: why is MILP hard?** LP is convex and solved in polynomial time (interior point) or very fast in practice (simplex). Integer variables make the feasible set non-convex; MILP is NP-hard and solved by branch & bound / branch & cut over LP relaxations.
2. **Explain branch & bound.** Solve the LP relaxation → bound. Branch on a fractional variable, creating two subproblems. Prune nodes whose bound is worse than the best integer solution found (incumbent). Gap = |incumbent − best bound| / |incumbent|.
3. **What makes a formulation "strong"?** Its LP relaxation is close to the convex hull of integer solutions. Small big-Ms, aggregated vs disaggregated constraints (`x_ij ≤ y_j` vs `Σx_ij ≤ n·y_j`), symmetry breaking, valid inequalities.
4. **Shadow price / dual value?** Change in the optimal objective per unit increase in a constraint's right-hand side, valid within the RHS range. Reduced cost = how much a variable's cost must improve to enter the solution. Only well-defined for LP (or the LP at the final node). → `python/assign_workers_shifts.py`.
5. **Weak duality / strong duality?** Any dual feasible solution bounds the primal; at optimality, both objectives are equal (LP). Complementary slackness: a constraint with slack has a zero dual.
6. **Your model takes too long. What do you do?** In order: check the formulation (big-Ms, symmetry); accept a gap (1–2%) and a time limit; warm start with a heuristic solution; reduce the model (pre-filter variables like `assign_clients_workers.py`, aggregate time); decompose (Benders, Lagrangian, column generation); rolling horizon; metaheuristic.
7. **Multi-objective options?** Weighted sum (simple, misses non-convex parts of the Pareto front, weights hard to explain); lexicographic (strict priorities); ε-constraint (traces the Pareto front, good for showing trade-offs to stakeholders); goal programming.
8. **Model is infeasible. How do you debug?** Compute an IIS (irreducible infeasible subsystem); add penalized slack variables to find which constraints are violated; check the data first — in my experience usually the cause.
9. **Column generation in one sentence.** Start with a few columns (e.g., vessel routes), solve the restricted master LP, use the duals to price out a new column with negative reduced cost via a subproblem, repeat; branch-and-price for integrality.
10. **Benders in one sentence.** Fix the complicating (integer) variables in a master problem, solve the easy subproblem, and send back cuts (optimality/feasibility) from its duals.
11. **When CP instead of MILP?** Scheduling with disjunctions, sequencing, logical constraints and small integer domains; MILP when the objective is cost-like with a strong LP relaxation.
12. **When a metaheuristic instead of an exact method?** Very large instances, strict time limits, black-box or non-linear objectives, rules that keep changing. Always benchmark it against exact optima on small instances and report variance across seeds. → `python/sa_scheduling.py`.
13. **Stochastic vs robust optimization?** Stochastic: optimize expected cost over scenarios with probabilities (two-stage: decide now, recourse later). Robust: optimize the worst case within an uncertainty set; no probabilities needed; more conservative. Value of stochastic solution (VSS) and EVPI quantify the benefit.
14. **Solvers you know?** HiGHS (open source), CBC, SYMPHONY (used in R/ompr), Gurobi/CPLEX (commercial), OR-Tools CP-SAT. Modeling: Pyomo, AMPL, ompr, PuLP.
15. **How do you validate an optimization model with the business?** Re-run historical cases and compare against what planners did; review solutions with domain experts; check every constraint is binding somewhere for a reason; KPI dashboard after go-live.

## B. Machine learning

16. **Bias–variance trade-off.** Error = bias² + variance + noise. Simple models underfit (high bias); flexible models overfit (high variance). Control with regularization, more data, cross-validation.
17. **How do you validate a model properly?** Split matching how it will be used: GroupKFold when rows share an entity (same machine), time-based splits for forecasting, hold-out test touched once. → `python/rul_maintenance.py`.
18. **Data leakage examples.** Features computed with future data (rolling windows centered, target encoding on the full set), same entity in train and test, scaling fitted on all data. Fix with pipelines and correct splits.
19. **Regression metrics?** MAE (robust, interpretable in units), RMSE (punishes big errors), MAPE (bad near zero). Pick the one matching business cost; in maintenance, late predictions cost more than early → asymmetric loss or quantiles.
20. **Classification metrics?** Precision, recall, F1, ROC-AUC, PR-AUC for imbalance; choose the threshold from the cost matrix, not 0.5.
21. **Imbalanced data?** Use proper metrics, class weights, threshold tuning; resampling (SMOTE) only inside CV folds.
22. **Random forest vs gradient boosting.** RF: bagging of deep trees, reduces variance, robust defaults. GB: sequential shallow trees fitting residuals, reduces bias, usually more accurate, needs tuning (learning rate, depth, early stopping).
23. **How do you explain a model?** Global: permutation importance, partial dependence. Local: SHAP values. And sanity checks with domain experts (does vibration increase risk?).
24. **Uncertainty in predictions?** Quantile regression, prediction intervals via conformal prediction, ensembles, Bayesian models. Check calibration/coverage on held-out data.
25. **Time series forecasting approach?** Baselines first (naive, seasonal naive), then ETS/ARIMA, then ML with lag features (gradient boosting) using rolling-origin backtesting.
26. **Predict-then-optimize pitfalls?** The optimizer exploits prediction errors (optimizer's curse); point forecasts ignore risk. Use quantiles/scenarios, stochastic or robust optimization, or decision-focused learning.
27. **Model drift?** Monitor input distributions (PSI, KS), prediction distribution, and realized error when labels arrive; retrain on schedule or trigger.
28. **Censoring (survival analysis)?** In maintenance, many machines haven't failed yet: their lifetime is right-censored. Survival models (Cox, Weibull AFT, random survival forests) handle it; naive regression on failed units only is biased.

## C. Estadística

29. **p-value?** Probability of data at least as extreme as observed if H0 is true. Not the probability that H0 is true.
30. **Linear regression assumptions.** Linearity, independence, homoscedasticity, normal errors (for inference), no perfect multicollinearity.
31. **Confidence interval vs prediction interval.** CI for a mean/parameter; PI for a new observation (wider, includes noise).
32. **A/B test design.** Define metric and minimum detectable effect, compute sample size (power 80%, α 5%), randomize, avoid peeking (or use sequential tests).
33. **Monte Carlo: how many replications?** Enough so the CI half-width is below the decision tolerance; half-width ≈ 1.96·s/√n. Use common random numbers to compare scenarios. → `python/simulation_scenarios.py`.

## D. Producción e ingeniería

34. **How would you deploy an optimization model?** Package the model as a Python library with tests; expose via an API (FastAPI) or a scheduled job (Databricks/Airflow); containerize with Docker; inputs validated with a schema (pydantic); log inputs, solution, solve time, gap; time limit and a fallback heuristic; dashboards for KPIs.
35. **How would you deploy an ML model?** Same plus experiment tracking and model registry (MLflow), versioned data, drift monitoring, retraining pipeline, shadow mode before replacing the current process.
36. **Testing a model?** Unit tests on data transformations; tests that small known instances give the known optimum; property tests (all clients assigned, no capacity violated); regression tests on fixed seeds.
37. **Git workflow?** Feature branches, pull requests with review, CI running lint + tests, semantic commits.
38. **Agile with data science?** Short iterations with a usable increment: baseline heuristic first, then an exact model; demo to users every sprint.

## E. Preguntas abiertas tipo caso

39. **"Our vessel fleet utilization is low. How would you help?"** Clarify the decision (scheduling? fleet size? contracts?), KPIs, data available; descriptive analysis first; then a forecast of demand; scheduling optimization; simulation for robustness; pilot on one region.
40. **"How would you predict manufacturing lead times?"** Define target (order → ship), features (product family, routing, load at release, supplier), GroupKFold by product, quantile models because planners need P90; feed P90 into the planning MILP.
41. **"A manager doesn't trust your model."** Show it reproducing past decisions they recognize; explain trade-offs with scenarios; let them override and log it; measure results side by side.
