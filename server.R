
shinyServer(function(input, output,session) {

    opciones <- reactiveValues(
        # "turnos" = 10,
        # "trabajadores" = 10,
        # "rango" = 10:20
    )
    
    observe({
        opciones$turnos = input$num_turnos
        opciones$trabajadores = input$num_trabajadores
        opciones$rango = input$salarios
    }) %>% 
        bindEvent(input$exe)
    
    output$asignacion <- renderTable({
        if(input$exe){
            assign_WtoShifts(ntu = opciones$turnos,
                             ntr = opciones$trabajadores,
                             rango = opciones$rango)
        }
    })
    
    # output$distPlot <- renderPlot({
    # 
    #     # generate bins based on input$bins from ui.R
    #     x    <- faithful[, 2]
    #     bins <- seq(min(x), max(x), length.out = input$bins + 1)
    # 
    #     # draw the histogram with the specified number of bins
    #     hist(x, breaks = bins, col = 'darkgray', border = 'white')
    # 
    # })

})
