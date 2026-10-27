# Modelos para el sector energía, explicados

Lee esto antes de formular en `02_formulation_drills.md`.
Para cada modelo: el problema, una analogía, qué se decide, qué se optimiza, la restricción clave y el truco de modelado.

## 1. Barcos de instalación a proyectos offshore
- **Problema:** las empresas de servicios submarinos instalan equipos con barcos especializados. Son pocos, cuestan mucho por día y cada campaña dura semanas. El clima cierra ventanas de trabajo.
- **Analogía:** reservar salas en un calendario. Cada reunión (proyecto) necesita una sala compatible (barco) por días seguidos. Una sala no puede tener dos reuniones. Algunos días la sala está cerrada (clima).
- **Se decide:** qué barco hace cada proyecto y qué día empieza.
- **Se optimiza:** costo de los barcos + penalización por retraso.
- **Restricción clave:** sin solapamiento en cada barco; solo se empieza en días con ventana de clima.
- **Truco:** modelo indexado en el tiempo (x[p,v,t] = el proyecto p empieza el día t con el barco v). Si crece mucho: generación de columnas, donde cada columna es el calendario completo de un barco.

## 2. Job shop con setups (manufactura)
- **Problema:** piezas (válvulas, conectores, forjados) pasan por máquinas en un orden fijo: torno → fresado → prueba.
- **Analogía:** la cocina de un restaurante. Cada plato tiene su receta en orden (cortar → cocinar → emplatar). Cada estación hace una cosa a la vez. Pasar de pescado a postre exige limpiar (setup).
- **Se decide:** el orden de las tareas en cada máquina.
- **Se optimiza:** terminar todo lo antes posible (makespan) o minimizar retrasos.
- **Restricción clave:** en cada máquina, "i va antes que j, o j antes que i".
- **Truco:** con big-M el LP es débil. CP-SAT razona con intervalos y suele ganar (`python/jobshop_cpsat.py`).

## 3. Repuestos críticos en varias bodegas
- **Problema:** si falla una pieza crítica en una plataforma y no hay repuesto cerca, la producción se detiene. Los repuestos son caros y la demanda es rara e incierta.
- **Analogía:** una cadena de farmacias que decide cuántas unidades de un medicamento raro guarda cada farmacia. Guardar cuesta; no tenerlo cuando un paciente lo necesita cuesta mucho más.
- **Se decide:** el stock por bodega e ítem, y qué bodega cubre cada plataforma.
- **Se optimiza:** costo de inventario + envío, con un nivel de servicio mínimo.
- **Restricción clave:** tiempo de respuesta máximo y nivel de servicio (probabilidad de tener stock).
- **Truco:** el nivel de servicio no es lineal en el stock (demanda Poisson). Se precalcula el stock mínimo para cada nivel y se modela con binarias por nivel.

## 4. Ubicación de bases logísticas (facility location)
- **Problema:** dónde abrir bases o bodegas para atender pozos y plataformas.
- **Analogía:** abrir jardines infantiles en una ciudad. Cada uno tiene costo fijo de apertura y cupo limitado. Cada familia va a uno. Quieres pagar poco por abrir y que las familias se desplacen poco.
- **Se decide:** qué bases abrir y quién se atiende desde cada una.
- **Se optimiza:** costo fijo de apertura + costo de transporte.
- **Restricción clave:** capacidad de cada base; solo se atiende desde bases abiertas.
- **Truco:** agregar x[i,j] ≤ y[j] aunque parezca redundante. Esa desigualdad fuerte mejora mucho la relajación LP.

## 5. Ingenieros a proyectos con habilidades
- **Problema:** asignar ingenieros (subsea, procesos, eléctricos) a proyectos que piden ciertas habilidades y horas.
- **Analogía:** armar equipos de fútbol. Cada partido (proyecto) necesita arquero, defensas y delanteros. Cada jugador juega ciertas posiciones y tiene horas limitadas.
- **Se decide:** quién trabaja en qué proyecto y cuántas horas.
- **Se optimiza:** valor de los proyectos cubiertos − costo.
- **Restricción clave:** horas requeridas por habilidad, horas disponibles por persona y máximo de proyectos por persona.
- **Truco:** es la misma estructura de tus casos de Siigo y Banco Agrario. Cuéntalo así: *"same structure, different domain"*.

## 6. Mantenimiento con vida útil remanente (RUL)
- **Problema:** equipos con sensores; un modelo de ML predice cuántos días les quedan antes de fallar.
- **Analogía:** un taller que atiende un carro por día. Cada carro tiene una vida estimada. Si lo atiendes tarde, se daña (carísimo). Si lo atiendes muy temprano, desperdicias vida útil.
- **Se decide:** qué día se mantiene cada equipo.
- **Se optimiza:** vida útil desperdiciada + penalización por falla.
- **Restricción clave:** capacidad diaria de la cuadrilla; mantener antes del RUL.
- **Truco:** usar un RUL pesimista (cuantil 10 %) o escenarios (estocástica de 2 etapas: hoy decides el plan; en cada escenario de vida real cuentas las fallas). En `python/rul_maintenance.py`, con el cuantil, 2 equipos igual quedaron tarde: la cobertura real fue 76 %, no 90 %.

## 7. Simulación de una base logística (digital twin sencillo)
- **Problema:** ¿cuántos muelles necesita una base para que los barcos de suministro no esperen?
- **Analogía:** las cajas de un supermercado. En promedio alcanzan, pero los clientes llegan en grupos y se forman colas.
- **Se decide:** el número de muelles (escenarios con 2, 3 y 4).
- **Se mide:** espera media, con intervalo de confianza.
- **Dato:** con 2 muelles el uso promedio es 83 % y parece suficiente, pero la espera media es 5,5 h. Con 3 baja a 0,6 h.
- **Truco:** la simulación evalúa escenarios; la optimización elige entre ellos. Juntas forman un digital twin sencillo (`python/simulation_scenarios.py`).
