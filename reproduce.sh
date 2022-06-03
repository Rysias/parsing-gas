eval "$(conda shell.bash hook)"
conda activate parsegas2
echo "# DOWNLOAD DATA #"
bash download_data.sh
echo "# CALCULATING DISTANCE #"
python analyse_distances.py
echo "# BENCHMARKING ROAD DISTS #"
# Gentofte
python analyse_road_dists.py --kommune-id 157
# Aabenraa
python analyse_road_dists.py --kommune-id 580 
