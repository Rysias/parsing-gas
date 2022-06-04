# parsing-gas
Final Project for Spatial Analytics (Cultural Data Science at Aarhus University)


## Methods and Design
### Data
# TODO

### Software Design
This project also follows the SOLID-principles. The overaching goal is to make experimentation as easy as possible. Throughout these assignments I have discovered that the more I follow the principles contra corner-cutting, the happier I become in the end.  

- **Single responsibility**: Each function and script does one thing well like [`src/augment.py`](src/augment.py) for augmenting data, and splitting each model into its own file. 
- **Open-closed**: By providing abstract interfaces for the classifiers (in the sense that all iterations of convnets need the same inputs), it becomes easy to add other models. 
- **Liskov substitution**: Not quite applicable as the design is more functional than object oriented.
- **Interface segregation**: By using type hints, most functions are clear about what they expect. Also, the main functions are kept fairly clean with minimal inputs given the `src/` layout, to reduce dependencies
- **Dependency Inversion**: Not explicitly used but most functions are easy to replace (i.e. having another vectorizer), which is because of the strong design of scikit-learn and spacy. 

## Reproducing the results 
TL;DR: An example of the entire setup and running the pipeline can be run using the bash-script `reproduce.sh`. 

Below I explain how to reproduce the analyses and plots of my report. 

### Setting up the Environment
This project uses [mamba](https://mamba.readthedocs.io/en/latest/), a blazingly fast cross-platform package manager for data science. As described in their docs, it is most easy to install through either [miniconda](LINK) or [anaconda](LINK) so make sure to have one of these installed on your system! After that it is as easy as running the [`setup.sh`](./setup.sh) script in a bash terminal. 

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
    - [ ] Create reproduce instructions
- [ ] Clean repo
    - [x] Create plot folder
    - [ ] Remove dead files
    - [ ] Document scripts