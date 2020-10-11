<p align="center">
  <img src="http://tynecki.pl/phages2050-logo.png">
</p>

> "Keep calm, use AI for phages and stop AMR"

PHAGES2050 is a novel [Python 3.8+ programming language](https://python.org) framework to boost bacteriophage research & therapy and infrastructure in order to achieve the full potential to fight against antimicrobial resistant bacteria within **Natural Language Processing (NLP)** and **Deep Learning**.

Our project is about developing a AI-based framework for microbiologists and bioinformaticians who hunt, explore and classify phages. Applying the framework will shorten the duration of computational methods required to match phages with bacteria for specific patient cases. Having such organised framework at hand and freely-available will help develop personalized phage therapy and make it accessible to people worldwide.

Watch the [PHAVES #3](https://www.youtube.com/watch?v=gh_Q135t9ps) talk to learn more.

[![Travis CI](https://travis-ci.com/ptynecki/PHAGES2050.svg?branch=master)](https://travis-ci.com/github/ptynecki/PHAGES2050)
[![codecov](https://codecov.io/gh/ptynecki/PHAGES2050/branch/master/graph/badge.svg)](https://codecov.io/gh/ptynecki/PHAGES2050)
[![Documentation Status](https://readthedocs.org/projects/phages2050/badge/?version=stable)](https://phages2050.readthedocs.io/en/stable/?badge=stable)
[![PyPI version](https://img.shields.io/pypi/v/phages2050.svg)](https://pypi.org/project/phages2050/)
[![PyPI license](https://img.shields.io/pypi/l/phages2050.svg)](https://pypi.python.org/pypi/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/phages2050.svg)](https://pypi.python.org/pypi/phages2050/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://static.pepy.tech/badge/phages2050)](https://pepy.tech/project/phages2050)

## Table of Contents

[Framework modules](https://github.com/ptynecki/PHAGES2050#framework-modules) | [Usage](https://github.com/ptynecki/PHAGES2050#usage) | [Documentation](https://github.com/ptynecki/PHAGES2050#documentation) | [Installation](https://github.com/ptynecki/PHAGES2050#installation) | [Community and Contributions](https://github.com/ptynecki/PHAGES2050#community-and-contributions) | [Have a question?](https://github.com/ptynecki/PHAGES2050#have-a-question) | [Found a bug?](https://github.com/ptynecki/PHAGES2050#found-a-bug) | [Team](https://github.com/ptynecki/PHAGES2050#team) | [Change log](https://github.com/ptynecki/PHAGES2050#change-log) | [Code of Conduct](https://github.com/ptynecki/PHAGES2050#code-of-conduct) | [License](https://github.com/ptynecki/PHAGES2050#license)

## Framework modules

`crawlers` - set of functions responsible for bacteriophages data scraping from different sources (MillardLab, NCBI)  
`features` - set of functions responsible for nucleotides and proteins feature extraction for Machine Learning classification and deeper analysis  
`embeddings` - set of pre-trained Embedding models for nucleotides and proteins vectorization  
`classifiers` - set of pre-trained Machine Learning models dedicated for bacteriophage research  
`explore` - set of data visualization techniques in 2D or 3D dedicated for deeper bacteriophages exploration

## Usage

The repository includes numerous examples of using the framework in Jupyter Notebook format (*.ipynb). The most expected ones by the community are listed below:

##### Crawlers
* [MillardLab bacteriophage crawler](https://github.com/ptynecki/PHAGES2050/blob/master/examples/crawlers/MillardLab-bacteriophage-crawler.ipynb)
* NCBI bacteriophages crawlers (planned):
  * taxonomy, host and other expected meta-data;
  * complete genome sequences in FASTA format;
  * set of genes and proteins in FASTA format;

##### Embeddings
* [Bacteriophage proteins embedding](https://github.com/ptynecki/PHAGES2050/blob/master/examples/embeddings/Bacteriophage-proteins-embedding.ipynb)
* [Bacteriophage DNA embedding](https://github.com/ptynecki/PHAGES2050/blob/master/examples/embeddings/Bacteriophage-nucleotides-embedding.ipynb)
* Bacteriophage sequence-based biological and biochemical features extraction (planned)

##### Classifiers
* [Bacteriophage structural protein classifier with 95% of accuracy](https://github.com/ptynecki/PHAGES2050/blob/master/examples/classifiers/Bacteriophage-structural-protein-classifier.ipynb)
* Bacteriophage lifecycle classifier including chronic infection (planned)
* Bacteriophage taxonomy classifier (planned)
* Bacteriophage prophage detector and extractor (planned)
* Lysis zones multi-level-classification (in progress)

##### Explore
* Bacteriophages in 3D space based on:
  * DNA embedding (planned)
  * proteins embedding (planned)
  * biological and biochemical features (planned)
  * custom user features (planned)

## Documentation

The official documentation is hosted on ReadTheDocs: https://phages2050.readthedocs.io

## Installation

_PHAGES2050_ can be installed by running:

```
pip install phages2050
```

It requires Python 3.8.0+ to run. You can also use Conda:

```
conda install -c conda-forge phages2050
```

#### Install from GitHub

If you can't wait for the latest hotness and want to install from GitHub, use:

```
pip install git+git://github.com/ptynecki/PHAGES2050
```

#### Proteins' embedding

If you want to use Bacteriophage proteins vectorizers then remember to install extra package for proteins embedding:

```
pip install -U "bio-embeddings[all] @ git+https://github.com/sacdallago/bio_embeddings.git"
pip install git+https://github.com/facebookresearch/esm.git
```

## Community and Contributions

Happy to see you willing to make the PHAGES2050 better. Development on the latest stable version of Python 3+ is preferred. As of this writing it's 3.8. You can use any operating system.

If you're fixing a bug or adding a new feature, add a test with *[pytest](https://github.com/pytest-dev/pytest)* and check the code with *[Black](https://github.com/psf/black/)* and *[mypy](https://github.com/python/mypy)*. Before adding any large feature, first open an issue for us to discuss the idea with the core devs and community.

## Have a question?

Obviously if you have a private question or want to cooperate with us, you can always reach out to us directly via our [Phage Directory Slack](https://phage.directory/slack) (channel **#PHAGES2050**).

## Found a bug?

Feel free to add a new issue with a respective title and description on the [the PHAGES2050 repository](https://github.com/ptynecki/PHAGES2050/issues). If you already found a solution to your problem, we would be happy to review your pull request.

## Team

Core Developers, Domain Experts, Community Managers and Educators who contributing to PHAGES2050:

* Piotr Tynecki
* Yana Minina
* Iwona Świętochowska
* Przemysław Mitura
* Joanna Kazimierczak
* Arkadiusz Guziński
* Bogusław Zimnoch
* Jessica Sacher, PhD
* Shawna McCallin, PhD
* Marie-Agnes Petit, PhD
* Jan Zheng

## Change log

The log's will become rather long. It moved to its own file.

See [CHANGELOG.md](https://github.com/ptynecki/PHAGES2050/blob/master/CHANGELOG.md).

## Code of Conduct

Everyone interacting in the PHAGES2050 project's development, issue trackers and Slack discussion is expected to follow the [Code of Conduct](https://github.com/ptynecki/PHAGES2050/blob/master/CODE_OF_CONDUCT.md).

## License

The PHAGES2050 package and pre-trained models are released under the under terms of [the MIT License](https://github.com/ptynecki/PHAGES2050/blob/master/LICENSE).
