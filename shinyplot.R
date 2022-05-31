

library(shiny)
library(leaflet)
library(dplyr)

# Load data
dist_dat <- readr::read_csv("data/gas_fjernvarme_distances.csv") %>% 
    # A bit of a hack to play nice with leaflet
  mutate(dist_colors2 = case_when(
    distance < 500 ~ "near", 
    between(distance, 500, 1000) ~ "middle", 
    distance > 1000 ~ "far"
))# %>% 
  #sample_n(100)

near_icon <- makeAwesomeIcon(
  icon = "info",
  iconColor = "black",
  markerColor = "green",
  library = "fa"
)
middle_icon <- makeAwesomeIcon(
  icon = "info",
  iconColor = "black",
  markerColor = "orange",
  library = "fa"
)
far_icon <- makeAwesomeIcon(
  icon = "info",
  iconColor = "black",
  markerColor = "darkred",
  library = "fa"
)
icon_list <- awesomeIconList(near = near_icon, 
                      middle = middle_icon,
                      far = far_icon)
r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

ui <- fluidPage(
  leafletOutput("mymap"),
  p(),
  selectInput("variable", "Variable:",
              c("Less than 500m" = "near",
                "Between 500m and 1000m" = "middle",
                "More than 1000m" = "far")),
)

server <- function(input, output, session) {
  plot_dat <- reactive({
    dist_dat %>% 
      dplyr::filter(dist_colors2 == input$variable)
  })
  
  output$mymap <- renderLeaflet({
    leaflet(plot_dat()) %>%
      addProviderTiles(providers$Stamen.TonerLite,
                       options = providerTileOptions(noWrap = TRUE)
      ) %>%
    addAwesomeMarkers(~gas_long, ~gas_lat, icon=~icon_list[dist_colors2], clusterOptions = markerClusterOptions(maxClusterRadius=30))
  })
}

shinyApp(ui, server)
