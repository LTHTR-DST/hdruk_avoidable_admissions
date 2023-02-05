# Welcome to Avoidable Admissions

This Python package is being developed as part of a federated multi-site collaboration led by the [School of Health and Related Research](https://www.sheffield.ac.uk/scharr) at [Sheffield University](https://www.sheffield.ac.uk/) and coordinated by [HDRUK](https://www.hdruk.ac.uk/).

The study documentation is maintained at <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs>.

The code in this repository and its use are documented here.

## Installation

Please see the [README.md](https://github.com/LTHTR-DST/hdruk_avoidable_admissions#readme) file for more information on environment setup for contributing to development.

The following describes installation of the package within an existing environment.
A separate virtual environment is recommended.

The package maybe installed directly from GitHub using one of the following commands:

To install only the package:

`pip install "avoidable_admissions @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"`

To install with optional dependencies for _exploratory data analysis_:

`pip install "avoidable_admissions[eda] @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"`

To install with optional dependecies for _contributing to development and documentation_:

`pip install "avoidable_admissions[dev] @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"`

Replace `<release-name>` with the latest release version e.g. `v.0.1.0-alpha`.
Omit `<release-name>` to install the latest code in the repo.

List of releases can be found here - <https://github.com/LTHTR-DST/hdruk_avoidable_admissions/releases>.

## Quickstart

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

See <https://lthtr-dst.github.io/hdruk_avoidable_admissions/admitted_care_pipeline_example> for a complete example.
