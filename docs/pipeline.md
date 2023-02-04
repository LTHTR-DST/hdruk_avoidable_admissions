# Data Analysis Pipeline

Data harmonisation is a vital step in constructing a reproducible, reusable data analytics pipeline.

Please refer to the detailed data specification and analysis plan developed by the lead team at Sheffield University.

These documentation as well as detailed, step-by-step information on setting up a Python environment and getting started on this project are available at <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/>.

The Avoidable Admissions project requires the preparation and analysis of 2 distinct datasets - for admitted care and emergency care.
The steps are identical for both and are shown in the flow chart below.

Click on the flowchart elements for more information as it applies to the Admitted Care Dataset.
Similar functions are available for the Emergency Care Dataset.

``` mermaid
flowchart TB
    subgraph Admitted_Care_Pipeline
        direction TB
        subgraph Preprocessing
            A(Extract) --> B(Validate)
            B --> C{Errors?}
            C -->|Yes| D(Fix Errors)
            D --> B
        end
        subgraph Feature_Engineering
            C -->|No| E(Generate Features)
            E --> F(Validate)
            F --> G{Errors?}
            G -->|Yes| H(Fix Errors)
            H --> F
        end
        subgraph Analysis
            G -->|No| I(Analysis)
        end
    end
    style A stroke:#526cfe,stroke-width:4px
    style E stroke:#526cfe,stroke-width:4px
    style I stroke:#526cfe,stroke-width:4px

    style B stroke:#26b079, stroke-width:4px
    style F stroke:#26b079, stroke-width:4px

    style D stroke:#ff7872
    style H stroke:#ff7872


    click B "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_admitted_care_data"
    click F "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_admitted_care_features"

    click C "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_dataframe--validation-example"
    click G "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_dataframe--validation-example"


    click E "/hdruk_avoidable_admissions/features/#avoidable_admissions.features.build_features.build_admitted_care_features"

    click D "/hdruk_avoidable_admissions/validation/#fixing-errors"

```

## Complete Pipeline Example

This is an example using the Admitted Care Dataset.
The same principles apply for the Emergency Care Dataset.

``` python

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
df = pd.read_csv('../data/raw/admitted_care)

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
# TODO: Sample Jupyter Notebook for generating descriptive analytics

```
