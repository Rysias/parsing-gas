eval "$(conda shell.bash hook)"
conda install mamba -n base -c conda-forge
mamba env create -f full_environment.yml
conda activate parsegas2
