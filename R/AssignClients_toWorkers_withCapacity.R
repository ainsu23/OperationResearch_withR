# Asignacion de clientes a vendedores con capacidad

# Cargue  librerías y conexión a PostrSQL---------------------------------------
rm(list = ls())
source("R/global.R")

# Parámetros del modelo ----
n_clientes <- 2000
n_trabajadores <- 30
n_oficinas <- 5
n_servicios <- 4
n_subservicios <- 10
n_cargos <- 4

# Creación de datos ----
#### Trabajadores ####
trabajadores <- list(
  "base" = data.frame()
)

trabajadores$base <- data.frame(
  "id" = sample(1:n_trabajadores,replace = FALSE),
  "oficina" = rep(sample(1:n_oficinas,replace = TRUE)),
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
        }) %>% 
        unlist()
      ),
    by = "cargo"
    )

#### Clientes ####
clientes <- list(
  "base" = data.frame()
)

clientes$base <- data.frame(
  "id" = sample(1:n_clientes,replace = FALSE),
  "oficina" = rep(sample(1:n_oficinas,replace = TRUE)),
  "servicio" = 1 %>% purrr::map(function(x){
    paste("servicio_",sample(1:n_servicios,replace = TRUE),sep = "")
  }) %>% unlist(),
  "sub_servicio" = 1 %>% purrr::map(function(x){
    paste("sub_servicio_",sample(1:n_subservicios,replace = TRUE),sep = "")
  }) %>% unlist()
)

#### servicios ####
servicios <- list(
  "estructura" = data.frame()
)

servicios$estructura <- data.frame(
  "sub_servicio" = paste("sub_servicio_",1:n_subservicios,sep = ""),
  "servicio" = 1:n_subservicios %>% purrr::map(function(x){
    paste("servicio_",sample(1:n_servicios,replace = TRUE),sep = "")
  }) %>% unlist(),
  "cargo" = 1:(n_subservicios*n_servicios) %>% purrr::map(function(x){
    sample(LETTERS[1:n_cargos],1,replace = TRUE)
  }) %>% unlist()
) %>% distinct()

