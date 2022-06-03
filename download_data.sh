mkdir -p "data/raw"
ZIP_PATH="data/raw/data.zip"
gdown 1bSWGPgW8K4S9BiWFasG32rhqevCG8OkM --output $ZIP_PATH
unzip $ZIP_PATH -d data/raw
rm $ZIP_PATH
