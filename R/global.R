### global.R contiene el cargue de liberías, conexiones a PostgrSQL

# Cargue liberías---------------------------------------------------------------
options(scipen = 999)
library(DBI)
library(RPostgres)
library(dplyr)
library(tidyr)
library(ROI)
library(ROI.plugin.symphony)
library(ROI.plugin.lpsolve)
library(ompr)
library(ompr.roi)
library(stringr)
library(tibble)
library(Matrix)
library(lubridate)
library(shinyWidgets)
library(shiny)

# Se establece conexión a una instancia de PostgrSQL
conn <- dbConnect(
  RPostgres::Postgres(),
  dbname = Sys.getenv("DATABASE_NAME"),
  user = Sys.getenv("DATABASE_USER"),
  password = Sys.getenv("DATABASE_PW"),
  host = Sys.getenv("DATABASE_HOST"),
  port = Sys.getenv("DATABASE_PORT"),
  bigint = "integer",
  sslmode = "allow")

