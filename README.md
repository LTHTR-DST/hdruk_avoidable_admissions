# HDRUK Avoidable Admissions Analytics

HDRUK Data Science Collaboration on Avoidable Admissions in the NHS.

Please see <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/> for more information.

## Project Setup

The project setup is based on an opinionated [cookiecutter datascience project](https://drivendata.github.io/cookiecutter-data-science/).
There are a few additional components to ease development and facilitate a collaborative workspace.

The setup has only been tested on Windows 10.
Before setting this project up, the following requirements need to be met:

- Anaconda or Miniconda installed and access to the Anaconda Powershell prompt
- Mamba (`conda install mamba -n base`)
- Git

### Steps

1. Start Anaconda powershell prompt and navigate to the root of this folder.
2. Execute `./init.bat`
3. Activate the environment with `conda activate hdruk`
4. Start JupyterLab with `jupyter-lab`
5. Alternatively open an IDE (e.g. Code) and set python environment to hdruk_aa

### Known issues

- _pandas-profiling_ is not compatible with Python 3.11 yet. If this is critical, the options are either to downgrade Python to 3.10 or to use a separate environment with Python<=3.10 to run pandas-profiling. As pandas-profiling will only be used infrequently, the latter may be a better option. Suggestions welcome.

## Project Organization

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
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
