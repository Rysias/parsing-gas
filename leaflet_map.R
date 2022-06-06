library(leaflet)
library(tidyverse)
library(htmltools)
library(sf)

# Adds coordinates from geometry
# From https://stackoverflow.com/a/54734971/10524429
add_coordinates <- function(sfdat) {
  sfdat %>% 
    mutate(long = unlist(map(sfdat$geometry,1)),
           lat = unlist(map(sfdat$geometry,2)))
}


tag.map.title <- tags$style(HTML("
  .leaflet-control.map-title { 
    transform: translate(-50%,20%);
    position: fixed !important;
    left: 50%;
    text-align: center;
    padding-left: 10px; 
    padding-right: 10px;
    font-weight: bold;
    font-size: 16px;
  }
"))


title <- tags$div(
  tag.map.title, HTML("Distance to District Heating")
)  

# Load data
dist_dat <- readr::read_csv("output/gas_fjernvarme_xy.csv") %>%
  # A bit of a hack to play nice with leaflet
  mutate(distance_category = case_when(
    distance < 500 ~ "near",
    between(distance, 500, 1000) ~ "middle",
    distance > 1000 ~ "far"
  )) %>%
  mutate(
    dist_label = str_c("Distance: ", round(distance), sep = ""),
    dist_label = str_c(dist_label, "m")
  ) %>% 
  st_as_sf(coords=c("gas_x", "gas_y"), crs=25832) %>% 
  st_transform(crs=4326) %>% 
  add_coordinates() %>% 
  select(distance_category, lat, long, dist_label)


# FOR TESTING
# dist_dat <- sample_n(dist_dat, 10)


neardat <- dist_dat %>% 
  filter(distance_category == "near")
middledat <- dist_dat %>% 
  filter(distance_category == "middle")
fardat <- dist_dat %>% 
  filter(distance_category == "far")


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

gasmap <- leaflet() %>%
  addTiles() %>%
  addAwesomeMarkers(
    data = neardat,
    lng = ~ long,
    lat = ~ lat,
    icon = near_icon,
    label = ~dist_label,
    clusterOptions = markerClusterOptions(),
    group = "<500m"
  ) %>%
  addAwesomeMarkers(
    data = middledat,
    lng = ~ long,
    lat = ~ lat,
    label = ~dist_label,
    icon = middle_icon,
    clusterOptions = markerClusterOptions(),
    group = "500-1000m"
  ) %>%
  addAwesomeMarkers(
    data = fardat,
    lng = ~ long,
    lat = ~ lat,
    icon = far_icon,
    label = ~dist_label,
    clusterOptions = markerClusterOptions(),
    group = ">1000m"
  ) %>%
  addLayersControl(overlayGroups = c("<500m", "500-1000m", ">1000m")) %>% 
  addControl(title, position = "topright", className="map-title")

# gasmap # Uncomment to test

htmlwidgets::saveWidget(gasmap, "gasmap.html")

