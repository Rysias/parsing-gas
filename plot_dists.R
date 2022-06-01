pacman::p_load(tidyverse, fs, wesanderson)

kommunekode <- read_csv("kommunekode.csv")
data_files <- fs::dir_ls(path="./out", glob="*_road_dist.csv")

df <- map_dfr(data_files, read_csv)

df %>% 
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


df
