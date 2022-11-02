library(shiny)
library(shinythemes)
library(shinycssloaders)
library(shinyWidgets)

mynumericInput <- function(id, label = id, value = 0, min = 0, max = 1) {
  numericInput(id, label, value = value, min = min, max = max)
}

vars = tibble::tribble(
  ~ id,   ~ value, 
  "SPY",    1,     
  "SHY",    0,    
  "IEF",    0,    
  "TLT",    0,    
  "GLD",    0,    
  "DBC",    0,    
  "VNQ",    0  
)

ui <- fluidPage(
  
  theme = shinytheme("superhero"),
    
  # Application title
    titlePanel("Portfolio Backtest"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
          width = 2,
          
           pmap(vars, mynumericInput)
          
        ),

        # Show a plot of the generated distribution
        mainPanel(
          tabsetPanel(
            id = "tabset",
            tabPanel("panel 1", "one"),
            tabPanel("panel 2", "two")
          )
        )
    )
)


server <- function(input, output) {

    
}

shinyApp(ui = ui, server = server)
