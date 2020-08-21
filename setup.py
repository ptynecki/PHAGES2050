from distutils.core import setup


long_description = (
    "PHAGES2050 is a novel Python 3.6+ programming language framework"
    " to boost bacteriophage research & therapy and infrastructure in"
    " order to achieve the full potential to fight against antimicrobial"
    " resistant bacteria within **Natural Language Processing (NLP)** and **Deep Learning**."
)


with open("requirements.txt") as requirements:
    # Read requirements and process as list of strings
    packages = list(map(str.strip, requirements.readlines()))

    setup(
        name="phages2050",
        version="0.2.0",
        license="MIT",
        description=long_description,
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Piotr Tynecki",
        author_email="p.tynecki@doktoranci.pb.edu.pl",
        url="https://github.com/ptynecki/PHAGES2050",
        download_url="https://github.com/ptynecki/PHAGES2050/archive/v0.2.0.tar.gz",
        install_requires=packages,
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
            "Programming Language :: Python :: 3.6",
        ],
        python_requires=">=3.6",
    )
