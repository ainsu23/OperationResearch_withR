# Asignacion de clientes a vendedores con capacidad

# Cargue  librerías y conexión a PostrSQL---------------------------------------
rm(list = ls())
source("R/global.R")
source("R/constante.R")

# Parámetros del modelo ----
n_clientes <- 1000
n_trabajadores <- 6
n_oficinas <- 2
n_servicios <- 4
n_subservicios <- 10
n_cargos <- 4

# Creación de datos ----
#### Trabajadores ####
trabajadores <- list(
  "base" = data.frame()
)

trabajadores$base <- data.frame(
  "id_tr" = sample(1:n_trabajadores,replace = FALSE),
  "oficina" = 1:n_trabajadores %>% 
    purrr::map(function(x){
      rep(sample(1:n_oficinas,replace = FALSE),1)[1]
    }) %>% unlist(),
  "cargo" = 1:n_trabajadores %>% 
    purrr::map(function(x){
      sample(LETTERS[1:n_cargos],1,replace = TRUE)
    }) %>% 
    unlist()
) %>% 
  left_join(
    data.frame(
      "cargo" = LETTERS[1:n_cargos],
      "capacidad" = 1:n_cargos %>% purrr::map(function(x){
        sample(seq(50,100,10),1,replace = FALSE)
      }) %>% unlist(),
      "costo" = 1:n_cargos %>% purrr::map(function(x){
        sample(seq(10,50,5),1,replace = FALSE)
      }) %>% unlist()
    ),
    by = "cargo"
  )

#### Clientes ####
clientes <- list(
  "base" = data.frame()
)

clientes$base <- data.frame(
  "id_cl" = sample(1:n_clientes,replace = FALSE),
  "oficina" = rep(sample(1:n_oficinas,replace = TRUE)),
  "servicio" = 1 %>% purrr::map(function(x){
    paste("servicio_",sample(1:n_servicios,replace = TRUE),sep = "")
  }) %>% unlist(),
  "sub_servicio" = 1 %>% purrr::map(function(x){
    paste("sub_servicio_",sample(1:n_subservicios,replace = TRUE),sep = "")
  }) %>% unlist()
) %>% ungroup()

#### servicios ####
servicios <- list(
  "estructura" = data.frame()
)

servicios$estructura <- data.frame(
  "sub_servicio" = paste("sub_servicio_",1:n_subservicios,sep = ""),
  "servicio" = 1:n_subservicios %>% purrr::map(function(x){
    paste("servicio_",sample(1:(n_servicios*2),replace = TRUE),sep = "")
  }) %>% unlist(),
  "cargo" = 1:(n_subservicios*n_servicios) %>% purrr::map(function(x){
    sample(LETTERS[1:n_cargos],1,replace = TRUE)
  }) %>% unlist()
) %>% distinct()

## Modelo a optimizar ----
tic()
# future::plan("multiprocess")


modelo <-
  MILPModel() %>%
  add_variable(ship[tr, cl],
               tr = 1:n_trabajadores, cl = 1:n_clientes,
               type = "binary") %>%
  add_constraint(sum_expr(ship[tr, cl], cl = 1:n_clientes) <=
                   colwise(constante(tabla = trabajadores$base,
                                     filtros = list("id_tr" = tr),
                                     col_valor = "capacidad")
                           ), 
                 tr = 1:n_trabajadores
                 ) %>% 
  add_constraint(sum_expr(ship[tr, cl], tr = 1:n_trabajadores) == 1,
                 cl = 1:n_clientes) %>%
  set_objective(
    sum_expr(
      ship[tr, cl] * colwise(
        constante(tabla = clientes$base %>%
                    full_join(
                      servicios$estructura,
                      by = c("servicio","sub_servicio")) %>% 
                    full_join(
                      trabajadores$base,
                      by = c("oficina", "cargo")),
                  filtros = list(
                    "id_cl" = cl,
                    "id_tr" = tr),
                  col_valor = "costo")),
      tr = 1:n_trabajadores, cl = 1:n_clientes),
    sense = "min") %>%
  solve_model(with_ROI(solver = "symphony", verbosity=1))

toc()  
