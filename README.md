# parsing-gas
This repository contains and data for the project ["Parsing Gas: a Scalable Pipeline for Nearest Neighbour Calculations on Spatial Data"](https://docs.google.com/document/d/1QARkB9bbmuBmNGZnxdJk5fv-x4OBOQfLu0BlF04vgGE/edit?usp=sharing). The overarching goal of the project is to answer the following question: *What ist the distribution of distances from gas-heated buildings to the district-heating network in Denmark?*. 

## Data
The repository depends on data from the BBR ("Building and Housing Register") - a public database maintained by the Housing Agency. Below are a description of the data artifacts. 

Filename | Description | License | Source | Generated in Reproduction
---- | --- | --- | --- | --- 
`BBR_Aktuelt_Totaludtraek_XML_20220517180008.zip` | The complete 65GB dataset from the BBR | NA | [datafordeler.dk](https://datafordeler.dk/) | :x:
`bbr_clean.csv`| Processed dataset | MIT | [Instructions here](#downloading-the-data) | :heavy_check_mark:
`output/gas_fjernvarme_xy.csv`| Euclidean distance to district heating network for each gas-heated building | MIT | Generated by [`analyse_distances.py`](./analyse_distances.py) | :heavy_check_mark:
`output/{KOMMUNE-ID}_road_dist.csv`| Comparison of road distance and Euclidean distance for a specific municipality (see codes [here](./kommunekode.csv)| MIT | Generated by [`analyse_road_dists.py`](./analyse_road_dists.py) | :heavy_check_mark:


## Reproducing the results 
TL;DR: An example of the entire setup and running the pipeline can be run using the bash-script `reproduce.sh`. 

Below I explain how to reproduce the analyses and plots of my report. 

### Setting up the Environment
This project uses [mamba](https://mamba.readthedocs.io/en/latest/), a blazingly fast cross-platform package manager for data science. As described in their docs, it is most easy to install through either [miniconda](LINK) or [anaconda](LINK) so make sure to have one of these installed on your system! After that it is as easy as running the [`setup.sh`](./setup.sh) script in a bash terminal. 

To see a complete list of the dependencies see the [`full_environment.yml`](./full_environment.yml)-file

### Tests
Parts of the project are developed using a [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development) framework using [pytest](https://docs.pytest.org/en/7.1.x/). The tests can be run using the following commands: 

```{console}
python -m pytest --cov-report term --cov ./src
```

This will print a coverage report to the terminal.  

### Downloading the data
The formatted data is stored in a .csv-file in Google Drive. It can be downloaded manually by following [this link](https://drive.google.com/file/d/1bSWGPgW8K4S9BiWFasG32rhqevCG8OkM/view?usp=sharing), and unzipping the file to the `data/raw` directory. However, the recommended way is to run the `download_data.sh` as this does it all automagically.

### Description of the Scripts
Below is a high level overview of the different scripts in the repo in relation to the analysis pipeline:

![Analysis pipeline](plots/analysis-pipeline.png)

Name | Component of Pipeline | Description | Part of `reproduce.sh` 
---- | :----: | :---: | ---:
[`extract_bbr.py`](/extract_bbr.py)| 1. Extract BBR | Parses building information from the full BBR xml | :x:
[`format_bbr.py`](/format_bbr.py)| 2. Format to CSV | Extracts relevant columns to a .CSV | :x:
[`analyse_distances.py`](LINK)| 3. Find Nearest District Heating | Does Euclidean distance calculations | :heavy_check_mark:
[`analyse_road_dists.py`](./analyse_road_dists.py)| 4. Compare Road Distances | Compares Euclidean Distances for Aabenraa and Gentofte respectively | :heavy_check_mark:
[`plot_dists.R`](/plot_dists.R)| 5.1 Plot Distributions| Plots distribution of distances (found [here](./plots/))| :heavy_check_mark:
[`leaflet_map.R`](/leaflet_map.R)| 5.2 Create Map | Creates an interactive map of gas-heated buildings and their distance | :heavy_check_mark:

All of the python scripts are documented using [argparse](https://docs.python.org/3/library/argparse.html). This means that full documentation can be found using the `--help`-flag.

### Description of /src
To maximize


# TODO 
- [ ] Finish reproducability
    - [x] Refactor leaflet map creation
    - [x] Add leaflet map to script 
    - [ ] Test run (again)
- [ ] Expand README
    - [x] Copy CDS template
    - [x] Create reproduce instructions
- [ ] Clean repo
    - [x] Create plot folder
    - [x] Remove dead files
    - [ ] Document scripts
- [ ] Explain artifacts
    - [ ] Explain scripts
    - [x] Explain datasets (generated and downloaded)
- [ ] WRITE(!)
    - [ ] Add Sources / references
    - [ ] Format into niceness