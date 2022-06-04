# parsing-gas
Final Project for Spatial Analytics (Cultural Data Science at Aarhus University)


## Methods and Design
### Data

Filename | Description | License | How to get| In Repository
---- | --- | --- | --- | --- 
FULL BBR | SOMETHING HERE | (link to licence) | LINK TO SOURCE | :x:
`bbr_clean.csv`| Processed dataset | (link to licence) | [Instructions here](#downloading-the-data) | :x:
``| Processed dataset | (link to licence) | [Instructions here](#downloading-the-data) | :x:

# TODO

### Software Design
This project also follows the SOLID-principles. The overaching goal is to make experimentation as easy as possible. Throughout these assignments I have discovered that the more I follow the principles contra corner-cutting, the happier I become in the end.  

- **Single responsibility**: 
- **Open-closed**: 
- **Liskov substitution**: 
- **Interface segregation**: 
- **Dependency Inversion**: 

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
Below is a high level overview of the different scripts in the repo:

Name | Component of Pipeline | Description | Part of `reproduce.sh` 
---- | :----: | :---: | ---:
[`nameofscript.py`](LINK)| Extraction | SOMETHING HERE | :heavy_check_mark:
[`nameofscript.py`](LINK)| Extraction | SOMETHING HERE | :heavy_check_mark:
[`nameofscript.py`](LINK)| Extraction | SOMETHING HERE | :heavy_check_mark:

All of the python scripts are documented using [argparse](https://docs.python.org/3/library/argparse.html). This means that full documentation can be found using the `--help`-flag. Below are the results output for the respective scripts. The R scripts take no arguments. 


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
    - [ ] Remove dead files
    - [ ] Document scripts
- [ ] Explain artifacts
    - [ ] Explain scripts
    - [ ] Explain datasets (generated and downloaded)