#!/usr/bin/env Rscript

library(tidyverse)
library(fs)
library(wesanderson)
print("I'm in R!")
######################################
# PLOT COMPARISON OF ROAD AND EUCLID #
######################################

kommunekode <- read_csv("kommunekode.csv")
data_files <- fs::dir_ls(path="./output", glob="*_road_dist.csv")

df <- map_dfr(data_files, read_csv)

comparison_plot <- df %>% 
  mutate(rowid = row_number()) %>% 
  select(rowid, kommunekode, euclid_distance=distance, road_distance=road_dist) %>% 
  left_join(kommunekode) %>% 
  select(-kommunekode) %>% 
  pivot_longer(-c(rowid, kommunenavn)) %>% 
  mutate(name = str_remove(name, "_distance")) %>% 
  ggplot(aes(x=value, fill=name)) + 
  scale_x_log10() + 
  geom_density(alpha=0.5) + 
  facet_wrap(~kommunenavn) + 
  theme_minimal() + 
  labs(title = "Distribution of Distances", subtitle = "Comparison of different methods and municipalities", 
       x = "Distance to District Heating (m)", legend = "Distance Metric", y=NULL) + 
  scale_fill_manual(name = "Distance Method", values=wesanderson::wes_palette(name="Darjeeling1"))

ggsave("plots/comparison.png", width=3000, height=1080, unit="px")

###########################
# PLOT TOTAL DISTRIBUTION # 
###########################
fulldat <- read_csv("./output/gas_fjernvarme_xy.csv")
plot_dat <- fulldat %>% 
  mutate(
    dist_cat = case_when(
      distance < 500 ~ "<500m",
      between(distance, 500, 1000) ~ "500m-1000m",
      distance > 1000 ~ ">1000m"
    )
  ) %>% 
  mutate(dist_cat = factor(dist_cat, levels = c("<500m", "500m-1000m", ">1000m")))

# Summarise results
sum_dat <- plot_dat %>% 
  group_by(dist_cat) %>% 
  count() 
print(sum_dat)

palette <- wes_palette("Darjeeling1", 5)
log_palette <- c(palette[2], palette[4], palette[1])
log_plot <- ggplot(plot_dat, aes(x=distance, fill=dist_cat)) +
  geom_histogram(bins=100) + 
  theme_minimal() + 
  scale_x_log10() + 
  scale_fill_manual(values=log_palette, name=NULL) + 
  labs(title = "Distance to District Heating Network", x="Distance (m)", y="Count")
ggsave("plots/full_distribution.png",log_plot, width=3000, height=1080, unit="px")

