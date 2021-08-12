# Ejemplo sencillo de asignación de personal a turnos 
# usando paquetes ompr

# Cargue  librerías y conexión a PostrSQL---------------------------------------
rm(list = ls())
source("R/global.R")

# Data
ntu <- 365
ntr <- 30
turnos<- list(
  "turnos" = data.frame(
    "turnos" = seq.Date(today(),today()+ntu-1,by = "days"),
    "turnos_id" = seq(1:ntu),
    "requerimientos" = sample((ntr-3):ntr,ntu,TRUE)
    ),
  "num_turnos" = ntu
)

trabajadores <- list(
  "base" = data.frame(),
  "num_trabajadores" = 0,
  "disponibilidad" = data.frame()
)

trabajadores$base <- data.frame(
  "Nombre" = purrr::map(1:ntr, function (x) {
    paste("Andrés ",
          sample(LETTERS,1),
          sample(LETTERS,1),
          sample(LETTERS,1),
          ".",
          sep = "") 
    }) %>% unlist(),
  "id" = 1:ntr,
  "daily_salary" = sample(10:24,ntr,replace = TRUE)
)

trabajadores$num_trabajadores <- nrow(trabajadores$base)

trabajadores$disponibilidad <- data.frame(
    "id" = rep(trabajadores$base$id,turnos$num_turnos),
    "disponibilidad" = 
      sample(x = 0:1,
             size = trabajadores$num_trabajadores*length(turnos$turnos$turnos),
             replace = TRUE,c(0.2,0.8)
             )
    ) %>% 
    arrange(id) %>% 
    mutate(
      "turnos_fecha" = 
        rep(turnos$turnos$turnos,trabajadores$num_trabajadores),
      "turnos_id" = rep(turnos$turnos$turnos_id,trabajadores$num_trabajadores)
      )

disponibilidad_ <- function(tr, tu){
  bases <- tu %>% purrr::map(function(tu){
    tr %>% purrr::map(function(tr){
      trabajadores$disponibilidad %>%
        filter(id==tr & turnos_id==tu) %>% pull("disponibilidad")

    })
  })
  return(unlist(bases))
}

# IIS model 
factibilidad <- 
  trabajadores$disponibilidad %>% 
  group_by(turnos_fecha) %>% 
  summarise(total_trabajadores = sum(disponibilidad)) %>% 
  cbind(requerimiento = turnos$turnos$requerimientos) %>% 
  mutate(satisface = ifelse(requerimiento <= total_trabajadores, 
                            TRUE,
                            FALSE
                            )
         ) 
IIS <- FALSE
if (FALSE %in% (factibilidad$satisface)) {
  turnos$num_turnos <- nrow(
    factibilidad %>% 
      filter(satisface == TRUE)
      )
  IIS <- TRUE
}

if (IIS){
  turnos$turnos <- turnos$turnos %>% 
    inner_join(
      factibilidad %>% 
        filter(satisface == TRUE), 
      by = c("turnos"="turnos_fecha")) %>% 
    mutate(turnos_id = row_number())
  
  trabajadores$disponibilidad <- trabajadores$disponibilidad %>% 
    inner_join(
      factibilidad %>% 
        filter(satisface == TRUE), 
      by = "turnos_fecha") %>% 
    select(-turnos_id) %>% 
    mutate(turnos_id = rep(1:turnos$num_turnos,trabajadores$num_trabajadores))
}

ma <- 
  MILPModel() %>% 
  add_variable(ship[tr,tu],
               tr=1:trabajadores$num_trabajadores,tu=1:turnos$num_turnos,
               type="binary") %>%
  add_constraint(
    sum_expr(ship[tr,tu] * colwise(disponibilidad_(tr,tu)),
             tr=1:trabajadores$num_trabajadores) == turnos$turnos$requerimientos,
    tu=1:turnos$num_turnos) %>% 
  # ompr::extract_constraints()
  set_objective(sum_expr(
    colwise(
      trabajadores$base %>% arrange(id) %>% pull(daily_salary)) * ship[tr,tu],
                         tr=1:trabajadores$num_trabajadores, tu=1:turnos$num_turnos)
                ,"min") %>%
  # ompr::objective_function()
  solve_model(with_ROI(solver = "symphony", verbosity=1)) 
    

asignados <-
  get_solution(ma,ship[tr, tu]) %>% 
    filter(value == 1) %>% 
    select(-tu) %>% 
    mutate(tu = rep(turnos$turnos$turnos_id,turnos$turnos$requerimientos)) %>% 
    left_join(trabajadores$disponibilidad,
            by = c("tr"="id","tu"="turnos_id")) %>% 
    select(-satisface)
