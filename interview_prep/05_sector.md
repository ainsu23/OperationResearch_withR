# Contexto del sector: energía offshore

Información general del sector, sin datos de ninguna empresa en particular.
Antes de la entrevista, revisa por tu cuenta el último reporte anual y la web de la empresa.

## Qué hace una empresa de tecnología submarina
- **Equipos submarinos:** árboles de producción, manifolds, umbilicales, risers y flowlines.
- **Equipos de superficie:** cabezales de pozo y equipos de control.
- **Instalación:** flota propia de barcos especializados en tendido de tubería y construcción.
- **Tendencias:** contratos integrados (ingeniería, compras, construcción e instalación en uno solo) y equipos estandarizados y configurables, con menos piezas y entrega más rápida.

## Dónde encaja un DS de optimización (tus hipótesis para conversar)
| Área | Decisión | Técnica |
|---|---|---|
| Flota de barcos | Qué barco hace qué campaña y cuándo, con ventanas de clima | MILP indexado en el tiempo, simulación de clima |
| Manufactura | Secuenciar órdenes en plantas, setups | CP-SAT / MILP, lead time con ML |
| Supply chain | Inventario de repuestos y materiales de entrega larga (long-lead items) | Inventario estocástico, MILP |
| Proyectos | Planificación de recursos de ingeniería | Asignación con skills (tu caso Siigo) |
| Equipos instalados | Mantenimiento e intervención | RUL + MILP (tu `rul_maintenance.py`) |
| Comercial | Cotizar y priorizar ofertas | Modelos de propensión + optimización de cartera |

## Cómo conectar tu experiencia
- Equipos configurables por catálogo ↔ Master Planning y Detail Scheduling en Ajover.
- Asignación de recursos escasos con reglas duras ↔ tus 3 MILP.
- Producto digital usado por otros ↔ R packages, APIs, Databricks.

## 3 preguntas para hacerles
1. What decisions does the team support today, and which one would my first project target?
2. How are models deployed: inside existing digital products, or as standalone tools for planners?
3. Which optimization and ML stack do you use (solvers, cloud, MLOps), and how do you measure the value of a delivered model?
