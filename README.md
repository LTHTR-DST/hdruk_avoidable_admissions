[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=dev&repo=590237327&machine=basicLinux32gb&location=WestEurope)

# HDRUK Avoidable Admissions Analytics

HDRUK Data Science Collaboration on Avoidable Admissions in the NHS.

Please see <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/> for more information.

## Installation

For contributing to this repo, please see [Development Setup](#development-setup) section below.

The following describes installation of the package within an existing environment.
A separate virtual environment is recommended.

The package maybe installed directly from GitHub.

```shell
pip install "avoidable_admissions @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"
```

Additional installation options are described in the [documentation](https://lthtr-dst.github.io/hdruk_avoidable_admissions/).

Replace `<release-name>` with the latest release version e.g. `v0.1.0-alpha`.
Omit `<release-name>` to install the latest code in the repo.

List of releases can be found here - <https://github.com/LTHTR-DST/hdruk_avoidable_admissions/releases>.

## Quickstart

Detailed instructions are available in the [documentation](https://lthtr-dst.github.io/hdruk_avoidable_admissions/) including a [complete pipeline example](https://lthtr-dst.github.io/hdruk_avoidable_admissions/admitted_care_pipeline_example).

```python
import pandas as pd
from avoidable_admissions.data.validate import (
    validate_dataframe,
    AdmittedCareEpisodeSchema,
    AdmittedCareFeatureSchema
)
from avoidable_admissions.features.build_features import (
    build_admitted_care_features
)


# Load raw data typically extracted using SQL from source database
df = pd.read_csv("../data/raw/admitted_care.csv")

# First validation step using Episode Schema
# Review, fix DQ issues and repeat this step until all data passes validation
good, bad = validate_dataframe(df, AdmittedCareEpisodeSchema)

# Feature engineering using the _good_ dataframe
df_features = build_admitted_care_features(good)

# Second validation step using Feature Schema
# Review and fix DQ issues.
# This may require returning to the first validation step or even extraction.
good_f, bad_f = validate_dataframe(df, AdmittedCareFeatureSchema)

# Use the good_f dataframe for analysis as required by lead site
```

## Development Setup

The project setup is based on an opinionated [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science/) template.
There are a few additional components to ease development and facilitate a collaborative workspace.

The setup has only been tested on Windows 10.
Before setting this project up, the following requirements need to be met:

- Anaconda or Miniconda installed and access to the Anaconda Powershell prompt
- Mamba (`conda install mamba -n base`)
- Git
- Fork and clone this repo

### Steps

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
This requires [Docker Desktop](https://www.docker.com/products/docker-desktop) to be installed.
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

- `pandas-profiling` is not compatible with Python 3.11 yet. If this is critical, the options are either to downgrade Python to 3.10 or to use a separate environment with Python<=3.10 to run pandas-profiling. As pandas-profiling will only be used infrequently, the latter may be a better option. Suggestions welcome.

## Project Organisation

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── avoidable_admissions <- Source code for use in this project.
    │   ├── __init__.py    <- Makes avoidable_admissions a Python module
    │   │
    │   ├── data           <- Scripts to download or generate and validate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

:file_folder: The following directories are not in version control and will need to be manually created by the user.

    ├── data
        ├── external       <- Data from third party sources.
        ├── interim        <- Intermediate data that has been transformed.
        ├── processed      <- The final, canonical data sets for modeling.
        └── raw            <- The original, immutable data dump.

Alternatively, create a `.env` file with database credentials, paths to data directories, etc. and
load this using `python-dotenv`.
See `.env.sample`  and <https://pypi.org/project/python-dotenv/> for how to do this.
Avoid hardcoding local paths in notebooks or code to ensure reproducibility between collaborators.

:x: **DO NOT COMMIT CREDENTIALS TO VERSION CONTROL!**

:x: **ENSURE NO PII IS EXPOSED BEFORE COMMITING TO VERSION CONTROL!**

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
