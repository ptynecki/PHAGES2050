from setuptools import setup
from glob import glob
from pathlib import Path


CURRENT_DIR = Path(__file__).parent

long_description = (CURRENT_DIR / "README.md").read_text(encoding="utf8")

description = (
    "PHAGES2050 is a novel Python 3.8+ programming language framework"
    " to boost bacteriophage research & therapy"
)

# Read requirements and process as list of strings
dependencies = (CURRENT_DIR / "requirements.txt").read_text()
dependencies = list(map(str.strip, filter(None, dependencies.split("\n"))))


version = "0.0.8"

setup(
    name="phages2050",
    version=version,
    license="MIT",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Piotr Tynecki",
    author_email="p.tynecki@doktoranci.pb.edu.pl",
    url="https://github.com/ptynecki/PHAGES2050",
    download_url=f"https://github.com/ptynecki/PHAGES2050/archive/v{version}.tar.gz",
    setup_requires=["setuptools>=50.3.0", "wheel>=0.35.1"],
    install_requires=dependencies,
    packages=[
        "phages2050",
        "phages2050.crawlers",
        "phages2050.crawlers.ncbi",
        "phages2050.crawlers.millardlab",
        "phages2050.features",
        "phages2050.features.extractors",
        "phages2050.features.io",
        "phages2050.features.transformers",
        "phages2050.embeddings",
        "phages2050.embeddings.proteins",
        "phages2050.embeddings.nucleotides",
        "phages2050.classifiers",
        "phages2050.classifiers.proteins",
    ],
    data_files=glob("examples/*/**"),
    include_package_data=True,
    keywords=[
        "bacteriophages",
        "phages",
        "phage therapy",
        "phage research",
        "amr",
        "genome embedding",
        "protein embedding",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)
