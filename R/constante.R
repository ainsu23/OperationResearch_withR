#' Retorna matriz simple triplet con la constante a multiplicar a variable del 
#' problema
#' @description Devuelve la columna constante teniendo cuenta la lista de 
#' columnas a filtras y los valores de estos mismos 
#'
#' @param tabla dataframe con información a realizar filtros
#' @param col_filtros lista de columnas a filtrar de la tabla 
#' @param indices lista con los indices o rango de valores a filtrar en columnas
#' @param col_valor columna que se requiere devolver
#' @example 
#' constante(tabla = trabajadores$disponibilidad,
#'           filtros = list("id_cl" = 1:5,"id_tr" = 1:14),
#'           col_valor = "disponibilidad")
#' @return matriz simple triplet con información de indices y col_valor

constante <- function (tabla,
                       filtros = list(),
                       col_valor = ""){
 
   tabla[is.na(tabla)] <- 0
   
 base <- 
   purrr::map2(
     .x = names(filtros),
     .y = filtros,
     function(.x,.y){
       tabla %>% 
         mutate(!!rlang::sym(col_valor) := 
                   if_else(condition = !!rlang::sym(.x) %in% .y, 
                           true = !!rlang::sym(col_valor),
                           false = 0,
                           missing =  0
                           )
                )
     }) %>% 
    purrr::reduce(left_join) %>% 
    pull(!!rlang::sym(col_valor)) 
    return(base)
}