

# Define server logic ----
server <- function(input, output) {
  output$plot <- renderPlot({
    mu <- input$mean
    std <- input$std
    x <- seq(-5, 5, length.out = 50)
    z <- (x - mu) / std
    y <- exp(-z^2/2.0)
    
    plot(x, y, type = 'l', xlab = )
  })
}

# Run the app ----
shinyApp(ui = ui, server = server)