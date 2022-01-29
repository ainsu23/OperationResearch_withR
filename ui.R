



# Define UI for application that draws a histogram
ui <- 
    shinyUI(
        fluidPage(
            titlePanel("Operation Research problems"),
            sidebarLayout(
                sidebarPanel(
                  selectInput(inputId = "or_problems",
                              label = NULL,
                              choices = "asignacion turnos"),
                  numericInput(inputId = "num_trabajadores",
                               label =  "# workers:",
                               value = 10
                               ),
                  numericInput(inputId = "num_turnos",
                               label = "# shifts",
                               value = 10),
                  numericRangeInput(inputId = "salarios",
                                     label = "salary range",
                                     value = c(10,20)
                                       ),
                  actionButton(inputId = "exe",
                               label = "Run")
                    ),
                mainPanel(
                  tableOutput("asignacion")#,
                    # plotOutput("distPlot")
                    )
                )
            )
        )
