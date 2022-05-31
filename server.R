rm(list=ls())
dist_dat <- read_csv("data/gas_fjernvarme_distances.csv") %>% 
    # A bit of a hack to play nice with leaflet
  mutate(dist_colors2 = case_when(
    distance < 500 ~ "near", 
    between(distance, 500, 1000) ~ "middle", 
    distance > 1000 ~ "far"
))


choices <- c("near", "middle", "far")

library(leaflet)
library(shiny)
shinyApp(
  ui = fluidPage(
    sliderInput(inputId = "time", 
                label = "Years Before Present:", 
                min = -50, max = 15000, value = 0, step = 500),
    tags$div(title = "This input has a tool tip",
             selectInput(inputId = "distance", 
                         label = "Taxon of Interest", 
                         choices = choices
                           )),
    leafletOutput("MapPlot1")
  ),
  
  server = function(input, output) {
    
    output$MapPlot1 <- renderLeaflet({
      leaflet() %>% 
        addTiles() %>% 
        setView(lng = 9.5, lat = 56.26, zoom = 4)
    })
    
    observe({
      
      dist_choice <- input$distance
      
      sites <- dist_dat %>%
        filter(dist_colors2 == dist_choice)
        
      leafletProxy("MapPlot1") %>% clearMarkers() %>% 
        addAwesomeMarkers(lng = sites$gas_long,
                         lat = sites$gas_lat, clusterOptions = markerClusterOptions())
    })
  },
  options = list(height = 600)
)
