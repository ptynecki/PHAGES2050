# Changelog
All notable changes to this project will be documented in this file.


## [0.0.8] - 11.10.2020
### Added
* Initial online documentation;

### Changed
* Migrated the codebase to Python 3.8+; 


## [0.0.7] - 18.09.2020
### Added
* new extention for `embedding` module with ESM transformer-based protein embedding model;

### Changed
* `requirements.txt` updated;
* Updated `README.md`;


## [0.0.6] - 01.09.2020
### Added
* [K-mer transformer](https://en.wikipedia.org/wiki/K-mer) with parallelization support;
* Embedding for bacteriophages nucleotides with new Example in Jupyter Notebook format;

### Changed
* `requirements.txt` with pandarallel, scikit-learn, gensim and numpy;


## [0.0.5] - 27.08.2020
### Added
* Initial Travis CI integration;
* Bacteriophage structural protein classifier;

### Changed
* Updated `README.md`;


## [0.0.4] - 24.08.2020
### Added
* Examples in Jupyter Notebook format;
### Changed
* Improved `setup.py` script and dependencies;
* Updated `README.md`;


## [0.0.3] - 24.08.2020
### Changed
* Added `setup.py` script for Python Index Packages (PyPI);


## [0.0.2] - 20.08.2020
### Added
* `embedding` module with BERT pre-trained embedding model for proteins with support for single protein vectorization as well as for proteins sets which are averagend to bacteriophage level;


## [0.0.1] - 10.08.2020
### Added
* `features` module with protein-based (amino-acid) feature extractor for single protein sequence as well as for multifasta;
* `crawlers` module with MillardLab website support;

### Changed
* `requirements.txt` with fake-useragent, biopython, lxml, python-requests and pandas;
