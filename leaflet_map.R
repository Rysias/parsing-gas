library(leaflet)
library(tidyverse)

# Load data
dist_dat <- readr::read_csv("data/gas_fjernvarme_distances.csv") %>%
  # A bit of a hack to play nice with leaflet
  mutate(distance_category = case_when(
    distance < 500 ~ "near",
    between(distance, 500, 1000) ~ "middle",
    distance > 1000 ~ "far"
  )) %>%
  mutate(
    dist_label = str_c("Distance: ", round(distance), sep = ""),
    dist_label = str_c(dist_label, "m")
  )

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
    lng = ~ gas_long,
    lat = ~ gas_lat,
    icon = near_icon,
    label = ~dist_label,
    clusterOptions = markerClusterOptions(),
    group = "<500m"
  ) %>%
  addAwesomeMarkers(
    data = middledat,
    lng = ~ gas_long,
    lat = ~ gas_lat,
    label = ~dist_label,
    icon = middle_icon,
    clusterOptions = markerClusterOptions(),
    group = "500-1000m"
  ) %>%
  addAwesomeMarkers(
    data = fardat,
    lng = ~ gas_long,
    lat = ~ gas_lat,
    icon = far_icon,
    label = ~dist_label,
    clusterOptions = markerClusterOptions(),
    group = ">1000m"
  ) %>%
  addLayersControl(overlayGroups = c("<500m", "500-1000m", ">1000m"))


mapview::mapshot(gasmap, "testmap.html")
