# Asignacion de clientes a vendedores con capacidad

# Cargue  librerías y conexión a PostrSQL---------------------------------------
rm(list = ls())
source("R/global.R")

# Data
nClientes <- 2000
nTrabaja <- 30
nOficinas <- 5
nServicios <- 10
