# HDRUK Avoidable Admissions Docs and Codeshare

HDRUK Data Science Collaboration on Avoidable Admissions in the NHS.

Please see <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/> for an explanation of how to use this repository.

## Project Setup

The project setup is based on an opinionated [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science/) template but has been significantly simplified to soften the learning curve and help newcomers. If you are new to python we recommend you use this template.

The setup has only been tested on Windows 10 but should work in linux/mac if a conda environment is used. We recommend using local version control within your trust / Uni environment for all development work. Please also psuedonymise all data you are using according to local standard operating procedures prior to using this template. Never work with non-psuedonymised research data.

# New to Python?

If you are new to python we recommend you go to [how to guides](https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/how_to_guides/) and don't worry too much about the rest of this readme. If you just want to get cracking then follow the below instructions:

### Requirements

Before setting this project up, the following requirements need to be met:

- Anaconda or Miniconda installed and access to the Anaconda Powershell prompt
- Mamba (`conda install mamba -n base -c conda-forge`)
- Git

How to do all of the above is covered in the how-to-guides. Please go to [how to guides](https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/how_to_guides/) for details on how to do the above because setting up such things in the NHS and elsewhere is not always straightforward due to permissions etc.

### Quick Start Steps

If you are already set up with the above the below steps should get you going but we take newcomers through this in the main guide. For newcomers we recommend using juptyer notebooks or jupter-lab which are both browser based and require no additional installations. For the more experienced VS code may be preferable. It will work with either.

1. Start Anaconda powershell prompt and navigate to the root of this folder.
2. Execute `./init.bat`
3. Activate the environment with `conda activate hdruk_aa`
4. Start JupyterLab with `jupyter-lab`
5. Alternatively open an IDE (e.g. Code) and set python environment to hdruk_aa

## Additional features

### pre-commit

The project expects collaboration using `git` and GitHub and uses [`pre-commit`](https://pre-commit.com/) git hooks
to help with identifying and resolving issues with code quality.
See `.pre-commit-config.yaml` for what features are enabled by default.

### Development Containers

This repo allows the usage of containers for full-featured development using [development containers](https://containers.dev/).
This can be done either locally using [Visual Studio Code](https://code.visualstudio.com/docs/devcontainers/containers)  or remotely using [GitHub Codespaces](https://github.com/features/codespaces).

**Local Development:**
To enable containerised development locally, clone the repositiory and open in VS Code.
Code should automatically prompt to reopen in a devcontainer.
This requires [Docker Desktop](https://www.docker.com/products/docker-desktop) to be installed. (Please be aware there are licensing requirements for this within big institutions. In Linux you do not require docker desktop)
It can take several minutes for the container to be created the first time while all required dependencies are installed.
This removes the need for creating a new conda environment.
Access to data should be configured as described at the end of [project organisation.](#project-organisation)

**Remote Development:**
Remote development is made easy using [GitHub Codespaces](https://github.com/features/codespaces) with configurable compute.
Compute instances are not deployable in the UK region yet which raises data governance issues :warning:.
However, this option is useful for writing documentation and code that is not dependent on data.
For instance, updating Markdown cells in Jupyter notebooks and docstrings is entirely possible.
Making API calls from this environment to generate code lists is also supported.

Important: :no_entry: Patient level data must not be uploaded into a codepace even if it is excluded from version control.

## Known issues

- `pandas-profiling` is not compatible with Python 3.11 yet. Therefore we have set the .yaml spec for the conda environment at Python 3.10.

## Project Organisation

    ├── mkdocs.yml               <- The configuration file for these docs (only necessary for docs development)
    ├── pipefile and lock        <- alternative environment setup (only necessary for docs development)
    ├── licence                  <- Project Licence - MIT (Permissive)
    ├── .pre-commit-config.yaml  <- Pre-commit hooks to prevent metadata retention inside notebooks during commits
    ├── environment.yml          <- Environment setup file
    ├── init.sh and bat          <- Setup scripts for windows and linux shells / command line
    ├── setup.py                 <- Sets up the python packages
    ├── README.md                <- Taken from https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/README.md and simplified. Thanks to vvcb and the LTHRT team for all their work on this!
    │
    ├── docs/
    │   ├── index.md             <- The index page
    │   ├── documentation        <- A brief explanation of the project - consult the main protocol for more details
    │   ├── data_models          <- The data model specs for the project
    │   ├── how-to-guides        <- How to Guides including starting from scratch
    │   ├── code.md              <- Codeshares and docstrings
    │
    ├── data_exraction/
    │   ├── synthetic_data       <- Dummy data for testing (please note the dataset provided is incomplete and provided for demonstation of only a part of the process to get started)
    │   ├── extraction.ipynb     <- Simple example of extraction process and cleaning with python
    │
    ├── data_harmonization/
    │   ├── synthetic_data       <- Dummy data for testing - will be generated by data_extraction phase (please note the dataset provided is incomplete and provided for demotion of only a part of the process to get you started)
    │   ├── harmonization.ipynb  <- Simple example of data harmonization with python
    │
    ├── data_analysis/
    │   ├── synthetic_data       <- Dummy data for testing - will be generated by data_harmonization phase (please note the dataset provided is incomplete and provided for onstation of only a part of the process to get you started)
    │   ├── harmonization.ipynb  <- Simple example of data harmonization with python
    │   ├── outputs/             <- Output folder for final aggregated results
    ├── modules/                 <- Modules mostly for data harmonization
