# Avoidable Admissions Analysis Pipeline Example

## Admitted Care Data Set

    Site: Lancashire Teaching Hospitals NHS Trust
    Created: 2023-02-04

    Lead site: SCHARR Institute, Sheffield University

## References

- Statistical Analysis Plan - <https://docs.google.com/document/d/1mpRKxNDbkTPwDhg7S_AaOXwbFQvHjXQRL7Qa31zn7DY/edit>
- Data Processing - <https://docs.google.com/document/d/1vysTKmvELK-5Rr7Dib3zDp8mCe_lUVr2e5EES23ShbQ/edit>
- Analysis Tables - <https://docs.google.com/document/d/10PuNTnEG5zTkWOVaMGlfOInleXJ0KA-_5hSH4upwhi4/edit>
- LTH GitHub Repo - <https://github.com/LTHTR-DST/hdruk_avoidable_admissions>
- Pipeline Docs - <https://lthtr-dst.github.io/hdruk_avoidable_admissions/>
- Collaboration Docs - <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/>

```python
%load_ext autoreload
%autoreload 2

from datetime import datetime

now = datetime.today()
print("Starting pipeline execution at", now)
```

    Starting pipeline execution at 2023-02-05 11:51:15.151223

```python
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("../.env")

dir_data = Path(os.getenv("DIR_DATA"))
dir_data
```

    WindowsPath('T:/Business Intelligence/Data Science/Work/hdruk_avoidable_adms')

```python
import numpy as np
import pandas as pd
from IPython.display import HTML

from avoidable_admissions.data.validate import (
    AdmittedCareEpisodeSchema,
    AdmittedCareFeatureSchema,
    get_schema_properties,
    validate_admitted_care_data,
    validate_admitted_care_features,
    validate_dataframe,
)
from avoidable_admissions.features import feature_maps
from avoidable_admissions.features.build_features import build_admitted_care_features
```

## Load Data

```python
# df_admcare = pd.read_csv(dir_data.joinpathpath('raw', 'admitted_care.csv')
df_admcare = pd.read_csv("../data/raw/admitted_care.csv")
```

```python
# Create a copy of the data to fix DQ issues to avoid reloading data from source everytime
dfa = df_admcare.copy()

"Raw dataframe contains %d rows and %d columns" % dfa.shape
```

    'Raw dataframe contains 47483 rows and 63 columns'

## Pipeline Overview

See <https://lthtr-dst.github.io/hdruk_avoidable_admissions/pipeline/> for more details.

## First Validation

This is done using the raw data typically extracted from SQL databases maintained by Business Intelligence.

Receiving the data in a format that matches the Sheffield specification as closely as possible will make subsequent steps easier.

Always, __always__, have friends in BI. Who is your [Quin](https://github.com/quindavies)?

### Admitted Care Episode Validation Rules

Use [`get_schema_properties(Schema)`](https://lthtr-dst.github.io/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.get_schema_properties) for an overview of what the expectations of the first validation schema are.

> _Help improve the validation rules and documentation, eg. title, description, etc. by contributing to the [GitHub repo](https://github.com/LTHTR-DST/hdruk_avoidable_admissions) or raising an [issue](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/issues)._

```python
schema_1 = (
    get_schema_properties(AdmittedCareEpisodeSchema)
    .sort_values("name")
    .set_index("name")
)
schema_1
```

<div>
<style scoped>
.dataframe {
  font-size: 0.6rem;
}
.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}

.dataframe tbody tr th {
vertical-align: top;
}

.dataframe thead th {
text-align: right;
}
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dtype</th>
      <th>nullable</th>
      <th>unique</th>
      <th>coerce</th>
      <th>required</th>
      <th>checks</th>
      <th>regex</th>
      <th>title</th>
    </tr>
    <tr>
      <th>name</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>admiage</th>
      <td>int64</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check greater_than_or_equal_to: greater_than_or_equal_to(18)&gt;, &lt;Check less_than_or_equal_to: less_than_or_equal_to(130)&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>admidate</th>
      <td>date</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check greater_than_or_equal_to: greater_than_or_equal_to(2021-10-01)&gt;, &lt;Check less_than_or_equal_to: less_than_or_equal_to(2022-09-30)&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>admimeth</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'31', '32', '28', '12', '24', '2A', '98', '82', '23', '81', '25', '13', '83', '2C', '21', '2D', '22', '2B', '11', '99'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>admisorc</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'53', '54', '66', '55', '65', '39', '37', '19', '98', '87', '79', '51', '88', '86', '52', '40', '56', '85', '29', '49', '99'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>admitime</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>True</td>
      <td>[&lt;Check str_matches: str_matches(re.compile('2[0-3]|[01]?[0-9]:[0-5][0-9]'))&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>diag_01</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>diag_[0-9]{2}</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>True</td>
      <td>None</td>
    </tr>
    <tr>
      <th>disdest</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'53', '54', '66', '48', '30', '65', '49', '39', '37', '19', '98', '87', '79', '84', '51', '88', '52', '85', '50', '29', '38', '99'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>dismeth</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'2', '8', '4', '1', '5', '9', '3'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>epiorder</th>
      <td>int64</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check greater_than_or_equal_to: greater_than_or_equal_to(0)&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>ethnos</th>
      <td>str</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'C', 'H', 'M', 'N', 'J', 'R', 'B', 'L', 'A', 'G', 'K', 'S', 'P', 'E', 'Z', 'F', '99', 'D'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>gender</th>
      <td>str</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check isin: isin({'2', 'X', '1', '9', '0'})&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>length_of_stay</th>
      <td>float64</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check greater_than_or_equal_to: greater_than_or_equal_to(0)&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>opdate_01</th>
      <td>datetime64[ns]</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>opdate_[0-9]{2}</th>
      <td>datetime64[ns]</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>True</td>
      <td>None</td>
    </tr>
    <tr>
      <th>opertn_01</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>opertn_[0-9]{2}</th>
      <td>str</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>True</td>
      <td>None</td>
    </tr>
    <tr>
      <th>patient_id</th>
      <td>int64</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>procodet</th>
      <td>str</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>sitetret</th>
      <td>str</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>townsend_score_decile</th>
      <td>int64</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>[&lt;Check greater_than_or_equal_to: greater_than_or_equal_to(0)&gt;, &lt;Check less_than_or_equal_to: less_than_or_equal_to(10)&gt;]</td>
      <td>False</td>
      <td>None</td>
    </tr>
    <tr>
      <th>visit_id</th>
      <td>int64</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>True</td>
      <td>[]</td>
      <td>False</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>

### Validate using AdmittedCareEpisodeSchema

The first time we try to validate the raw data, there are several errors for multiple reasons.

Spending a few minutes reading the schema validation error messages as well as reading the documentation for [Pandera](https://pandera.readthedocs.io/) will save days for this and future projects.

[`validate_dataframe(dfa, AdmittedCareEpisodeSchema)`](https://lthtr-dst.github.io/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_dataframe) is equivalent to [`validate_admitted_care_data(dfa)`](https://lthtr-dst.github.io/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_admitted_care_data)

```python
good, bad = validate_dataframe(dfa, AdmittedCareEpisodeSchema)

print("Good dataframe has %d rows" % good.shape[0])
print("Bad dataframe has %d rows" % bad.shape[0])
```

    Schema AdmittedCareEpisodeSchema: A total of 18 schema errors were found.

    Error Counts
    ------------
    - column_not_in_dataframe: 1
    - schema_component_check: 17

    Schema Error Summary
    --------------------
                                                                                                                                                                                                                                         failure_cases  n_failes
    schema_context  column                check
    DataFrameSchema <NA>                  column_in_dataframe                                                                                                                                                                               [visit_id]         1
    Column          admiage               greater_than_or_equal_to(18)                                                                                                                                   [0,3,12,14,4,15,2,6,11,5,1,16,17,10,7,8,13,9]        18
                    admidate              greater_than_                                                                                                               [TypeError("'>=' not supported between instances of 'str' and 'datetime.date'")]         1
                                          less_than_or_equal_to(2022-09-30)                                                                                           [TypeError("'<=' not supported between instances of 'str' and 'datetime.date'")]         1
                    admimeth              isin({'31','32','28','12','24','2A','98','82','23','81','25','13','83','2C','21','2D','22','2B','11','99'})                                                                                             [27]         1
                    admisorc              dtype('str')                                                                                                                                                                                         [int64]         1
                                          isin({'53','54','66','55','65','39','37','19','98','87','79','51','88','86','52','40','56','85','29','49','99'})                                                 [51,19,66,52,29,56,99,88,40,49,33,87,79,53]        14
                    disdest               dtype('str')                                                                                                                                                                                         [int64]         1
                                          isin({'53','54','66','48','30','65','49','39','37','19','98','87','79','84','51','88','52','85','50','29','38','99'})                       [19,99,79,88,29,51,52,85,84,54,38,50,37,66,65,53,87,49,48,98,30]        21
                    dismeth               dtype('str')                                                                                                                                                                                         [int64]         1
                                          isin({'2','8','4','1','5','9','3'})                                                                                                                                                              [1,4,2,8,9]         5
                    gender                dtype('str')                                                                                                                                                                                         [int64]         1
                                          isin({'2','X','1','9','0'})                                                                                                                                                                          [2,1,9]         3
                    opdate_01             dtype('datetime64[ns]')                                                                                                                                                                             [object]         1
                    townsend_score_decile dtype('int64')                                                                                                                                                                                     [float64]         1
                                          not_nullable                                                                                                                                                                                           [nan]         1

    Usage Tip
    ---------

    Directly inspect all errors by catching the exception:

    ```
    try:
        schema.validate(dataframe, lazy=True)
    except SchemaErrors as err:
        err.failure_cases  # dataframe of schema errors
        err.data  # invalid dataframe
    ```

    No data will pass validation due to column error. See output above.
    Good dataframe has 0 rows
    Bad dataframe has 246321 rows

### Iterative DQ Fixes

Fix one column or one error at a time and rerun `validate_dataframe(dfa, AdmittedCareEpisodeSchema)` in the previous cell to check if it has worked.

If you have made an error in data transformation, rerun `dfa = df_admcare.copy()` to start again.

__Error Behaviour:__ In case of errors other than [SchemaErrors](https://pandera.readthedocs.io/en/stable/reference/generated/pandera.errors.SchemaErrors.html?highlight=schemaerrors), `validate_dataframe` will print out the error message and return an empty `good` data frame and a `bad` dataframe containing all rows in input dataframe. Column errors, i.e., missing, misspelt or unexpected additional columns will also result in identical behaviour.

The `bad` dataframe may contain more rows than the input dataframe, as each error generates a new row. For instance, if one row in the input dataframe resulted in 5 errors in different columns, this will generate 5 rows in the `bad` dataframe, each with details on the specific errors available in additional columns.

TODO: vc to fix. If you get a `ufunc 'bitwise_or' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''` error, this is usually caused by a dtype mismatch between `datetime` in the input data when the validation code expects a `date` dtype.

__Feature Maps:__ These set out what values are allowed in various columns to pass first validation, how these will be transformed during feature engineering and what values are allowed in the new columns to pass second validation. <https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/features/feature_maps.py>

> _Help improve this process by raising a GitHub issue if validation fails when it shouldn't or you run into unexpected errors.

```python
"Starting with %d rows and %d columns" % dfa.shape
```

    'Starting with 47483 rows and 63 columns'

```python
dfa["visit_id"] = dfa.reset_index(drop=True).index
```

```python
dfa.patient_id = dfa.patient_id.astype(np.int64)
```

```python
dfa = dfa.loc[dfa.admiage >= 18].copy()
"Dataframe has %d rows and %d columns" % dfa.shape
```

    'Dataframe has 39168 rows and 64 columns'

```python
cols_opdate = dfa.filter(regex="opdate").columns
dfa[cols_opdate] = dfa[cols_opdate].apply(pd.to_datetime, dayfirst=True)
```

```python
dfa.admidate = pd.to_datetime(dfa.admidate, dayfirst=True).dt.date
```

```python
# dfa.admimeth = dfa.admimeth.astype(str)
dfa = dfa[dfa.admimeth != "27"]  # Careful
"Dataframe has %d rows and %d columns" % dfa.shape
```

    'Dataframe has 39167 rows and 64 columns'

```python
dfa.admisorc = dfa.admisorc.astype(str)
dfa = dfa[dfa.admisorc.isin(feature_maps.admisorc)]
dfa = dfa[dfa.admimeth != "27"]  # Careful
"Dataframe has %d rows and %d columns" % dfa.shape
```

    'Dataframe has 39166 rows and 64 columns'

```python
dfa.gender = dfa.gender.astype(str)
```

```python
dfa.disdest = dfa.disdest.astype(str)
dfa = dfa[dfa.disdest.isin(feature_maps.disdest)]
"Dataframe has %d rows and %d columns" % dfa.shape
```

    'Dataframe has 39166 rows and 64 columns'

```python
dfa.dismeth = dfa.dismeth.astype(str)
dfa = dfa[dfa.dismeth.isin(feature_maps.dismeth)]
"Dataframe has %d rows and %d columns" % dfa.shape
```

    'Dataframe has 39166 rows and 64 columns'

```python
# Set missing IMD values to 0 to pass validation. Address how this is dealth with at the analytics stage.
# This is to get around the quirks of what nan means in the Pandas (and Pandera) world.
dfa.townsend_score_decile = dfa.townsend_score_decile.fillna(0).astype(np.int64)
```

```python
# If everything above worked, this should not throw any errors.
good, bad = validate_admitted_care_data(dfa)

print("Good dataframe has %d rows" % good.shape[0])
print("Bad dataframe has %d rows" % bad.shape[0])
```

    Good dataframe has 39166 rows
    Bad dataframe has 0 rows

## Feature engineering

See documentation here: <https://lthtr-dst.github.io/hdruk_avoidable_admissions/features/>

This has been written to Sheffield's specifications and will change if the specification changes.

> _Help improve this process by raising a [GitHub issue](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/issues) or contributing code.

```python
dff = build_admitted_care_features(good.copy())
```

## Second validation

Second validation and addressing DQ is identical to the first validation process.

### Admitted Care Feature Validation Rules

The features dataframe should contain all columns from the initial dataframe _and_ the new generated features.

Once again have a look at [`feature_maps.py`](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/features/feature_maps.py) for more details.

Let's look at only the new features and the rules that apply to them.

```python
schema_2 = (
    get_schema_properties(AdmittedCareFeatureSchema)
    .sort_values("name")
    .set_index("name")
)
schema_2[~schema_2.index.isin(schema_1.index)]
```

<div>
<style scoped>
.dataframe {
  font-size: 0.6rem;
}
.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}

.dataframe tbody tr th {
vertical-align: top;
}

.dataframe thead th {
text-align: right;
}
</style>
<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>dtype</th>
<th>nullable</th>
<th>unique</th>
<th>coerce</th>
<th>required</th>
<th>checks</th>
<th>regex</th>
<th>title</th>
<th>description</th>
</tr>
<tr>
<th>name</th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<th>admiage_cat</th>
<td>str</td>
<td>False</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'65 - 69', '25 - 29', '75 ...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>admidayofweek</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Sunday', 'Wednesday', 'Mo...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>admisorc_cat</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Medical care', 'Residence...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>diag_01_acsc</th>
<td>None</td>
<td>False</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'COPD', 'Pneumothorax ', '...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>diag_seasonal_cat</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Respiratory infection', '...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>disdest_cat</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Medical care', 'Died', 'C...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>dismeth_cat</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Died', 'Discharged', 'Unk...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>ethnos_cat</th>
<td>str</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Other Ethnic Groups', 'As...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>gender_cat</th>
<td>str</td>
<td>False</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'Female', 'Indeterminate',...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>length_of_stay_cat</th>
<td>None</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check isin: isin({'&gt;=2 days', '&lt;2 days'})&gt;]</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>opertn_count</th>
<td>int64</td>
<td>False</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check greater_than_or_equal_to: greater_than...</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
<tr>
<th>townsend_score_quintile</th>
<td>int64</td>
<td>True</td>
<td>False</td>
<td>False</td>
<td>True</td>
<td>[&lt;Check in_range: in_range(0, 5)&gt;]</td>
<td>False</td>
<td>None</td>
<td>None</td>
</tr>
</tbody>
</table>
</div>

### Fix minor DQ issues and validate using AdmittedCareFeatureSchema

```python
# TODO: vc to fix. Easiest will be to validate this as datetime rather than date
dff.admidate = dff.admidate.dt.date
```

```python
# TODO: vc to fix. build_features makes this a categorical variable. Needs to be fixed either in build_features or in the validation schema
dff.admiage_cat = dff.admiage_cat.astype(str)
```

```python
good_f, bad_f = validate_dataframe(dff, AdmittedCareFeatureSchema)
print("Good dataframe has %d rows" % good_f.shape[0])
print("Bad dataframe has %d rows" % bad_f.shape[0])
```

    Good dataframe has 39166 rows
    Bad dataframe has 0 rows

## Analysis

Refer to <https://docs.google.com/document/d/10PuNTnEG5zTkWOVaMGlfOInleXJ0KA-_5hSH4upwhi4/edit> for details.

```python
df = good_f.copy()
```

This section describes the analysis populations or the analysis of the APC data. These populations will be referred to in the analysis descriptions that follow.

__All Acute Admissions__

This analysis population includes all acute admissions.

_Filter:_ (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1)

These filters should have been applied to the original data extract.

__All Acute Admissions for ACSCs__

This analysis population includes all acute admissions where the primary diagnosis from the first episode is an ACSC.

_Filter:_ (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1) & (diag_01 = ACSC_Code_APC)

__All Acute Admissions for Non-ACSCs__

This analysis population includes all acute admissions where the primary diagnosis from the first episode is not an ACSC.

_Filter:_ (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1) & (diag_01 != ACSC_Code_APC)

```python
# All acute admissions - this should be redundant if done at extraction
df = df[
    (df.admimeth.isin({"21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"}))
    & (df.epiorder == 1)
]

# Acute admissions by ACSC status
df["is_acsc"] = df.diag_01_acsc.where(df.diag_01_acsc == "-", "ACSC").replace(
    "-", "Non-ACSC"
)
```

### Age

```python
pd.concat(
    [df.admiage.describe().rename("All"), df.groupby("is_acsc").admiage.describe().T],
    axis=1,
).T
```

<div>
<style scoped>
.dataframe {
font-size: 0.6rem;
}
.dataframe tbody tr th:only-of-type {
vertical-align: middle;
}

.dataframe tbody tr th {
vertical-align: top;
}

.dataframe thead th {
text-align: right;
}
</style>
<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>count</th>
<th>mean</th>
<th>std</th>
<th>min</th>
<th>25%</th>
<th>50%</th>
<th>75%</th>
<th>max</th>
</tr>
</thead>
<tbody>
<tr>
<th>All</th>
<td>3#.##</td>
<td>5#.##</td>
<td>2#.##</td>
<td>1#.##</td>
<td>3#.##</td>
<td>6#.##</td>
<td>7#.##</td>
<td>1#.##</td>
</tr>
<tr>
<th>ACSC</th>
<td>1#.##</td>
<td>6#.##</td>
<td>1#.##</td>
<td>1#.##</td>
<td>5#.##</td>
<td>6#.##</td>
<td>8#.##</td>
<td>1#.##</td>
</tr>
<tr>
<th>Non-ACSC</th>
<td>2#.##</td>
<td>5#.##</td>
<td>2#.##</td>
<td>1#.##</td>
<td>3#.##</td>
<td>5#.##</td>
<td>7#.##</td>
<td>1#.##</td>
</tr>
</tbody>
</table>
</div>

```python
categorical_features = {
    "admiage_cat": "Age Bands",
    "gender_cat": "Gender",
    "ethnos_cat": "Ethnicity",
    "townsend_score_quintile": "Townsend Score Quintile",
    "admisorc_cat": "Admission Source",
    "admidayofweek": "Admission Day of Week",
    "diag_seasonal_cat": "Seasonal Diagnosis",
    "length_of_stay_cat": "Length of Stay",
    "disdest_cat": "Discharge Destination",
    "dismeth_cat": "Discharge Method",
}
```

```python
def make_crosstab(colname, tablename):
    x = pd.crosstab(df[k], df.is_acsc, margins=True, dropna=False, margins_name="Total")

    y = (
        pd.crosstab(
            df[k],
            df.is_acsc,
            normalize="index",
            dropna=False,
            margins_name="Total",
        )
        .mul(100)
        .round(2)
        .rename(columns={"ACSC": "ACSC %", "Non-ACSC": "Non-ACSC %"})
    )

    z = pd.concat([x, y], axis=1).sort_index(axis=1).fillna("-")

    z.index = pd.MultiIndex.from_tuples([(v, i) for i in z.index])

    return z
```

```python
# HTML Output
out = ""
df_results = []
for k, v in categorical_features.items():
    z = make_crosstab(k, v)
    df_results.append(z)
    out += f"""
        ### {v}
        {z.to_html()}

        """
df_results = pd.concat(df_results)
HTML(out)
```

### Age Bands

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="16" valign="top">Age Bands</th>
<th>18-19</th>
<td>1###</td>
<td>1#.##</td>
<td>7###</td>
<td>8#.##</td>
<td>9###</td>
</tr>
<tr>
<th>20 - 24</th>
<td>4###</td>
<td>2#.##</td>
<td>1###</td>
<td>7#.##</td>
<td>2###</td>
</tr>
<tr>
<th>25 - 29</th>
<td>4###</td>
<td>1#.##</td>
<td>2###</td>
<td>8#.##</td>
<td>2###</td>
</tr>
<tr>
<th>30 - 34</th>
<td>5###</td>
<td>2#.##</td>
<td>1###</td>
<td>7#.##</td>
<td>2###</td>
</tr>
<tr>
<th>35 - 39</th>
<td>5###</td>
<td>2#.##</td>
<td>1###</td>
<td>7#.##</td>
<td>2###</td>
</tr>
<tr>
<th>40 - 44</th>
<td>6###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>1###</td>
</tr>
<tr>
<th>45 - 49</th>
<td>7###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>1###</td>
</tr>
<tr>
<th>50 - 54</th>
<td>9###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>2###</td>
</tr>
<tr>
<th>55 - 59</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>2###</td>
</tr>
<tr>
<th>60 - 64</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>2###</td>
</tr>
<tr>
<th>65 - 69</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>2###</td>
</tr>
<tr>
<th>70 - 74</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>3###</td>
</tr>
<tr>
<th>75 - 79</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>3###</td>
</tr>
<tr>
<th>80 - 84</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>3###</td>
</tr>
<tr>
<th>&gt;85</th>
<td>2###</td>
<td>4#.##</td>
<td>2###</td>
<td>5#.##</td>
<td>4###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Gender

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="4" valign="top">Gender</th>
<th>Female</th>
<td>8###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Indeterminate</th>
<td>4</td>
<td>3#.##</td>
<td>9</td>
<td>6#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Male</th>
<td>7###</td>
<td>4#.##</td>
<td>9###</td>
<td>5#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Ethnicity

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="8" valign="top">Ethnicity</th>
<th>Asian or Asian British</th>
<td>7###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Black or Black British</th>
<td>1###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Mixed</th>
<td>9###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Not known</th>
<td>0</td>
<td>0#.##</td>
<td>1</td>
<td>1#.##</td>
<td>1</td>
</tr>
<tr>
<th>Not stated</th>
<td>5###</td>
<td>2#.##</td>
<td>1###</td>
<td>7#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Other Ethnic Groups</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>4###</td>
</tr>
<tr>
<th>White</th>
<td>1###</td>
<td>4#.##</td>
<td>2###</td>
<td>5#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Townsend Score Quintile

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="7" valign="top">Townsend Score Quintile</th>
<th>0</th>
<td>1###</td>
<td>2#.##</td>
<td>2###</td>
<td>7#.##</td>
<td>3###</td>
</tr>
<tr>
<th>1</th>
<td>3###</td>
<td>3#.##</td>
<td>5###</td>
<td>6#.##</td>
<td>9###</td>
</tr>
<tr>
<th>2</th>
<td>3###</td>
<td>3#.##</td>
<td>4###</td>
<td>6#.##</td>
<td>7###</td>
</tr>
<tr>
<th>3</th>
<td>2###</td>
<td>3#.##</td>
<td>3###</td>
<td>6#.##</td>
<td>5###</td>
</tr>
<tr>
<th>4</th>
<td>3###</td>
<td>3#.##</td>
<td>5###</td>
<td>6#.##</td>
<td>8###</td>
</tr>
<tr>
<th>5</th>
<td>3###</td>
<td>4#.##</td>
<td>4###</td>
<td>5#.##</td>
<td>7###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Admission Source

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="6" valign="top">Admission Source</th>
<th>Care Home</th>
<td>2</td>
<td>1#.##</td>
<td>1###</td>
<td>8#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Medical care</th>
<td>8###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Penal</th>
<td>5</td>
<td>5#.##</td>
<td>5</td>
<td>5#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Residence</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Unknown</th>
<td>1###</td>
<td>1#.##</td>
<td>5###</td>
<td>8#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Admission Day of Week

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="8" valign="top">Admission Day of Week</th>
<th>Friday</th>
<td>2###</td>
<td>4#.##</td>
<td>3###</td>
<td>5#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Monday</th>
<td>2###</td>
<td>3#.##</td>
<td>3###</td>
<td>6#.##</td>
<td>5###</td>
</tr>
<tr>
<th>Saturday</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>4###</td>
</tr>
<tr>
<th>Sunday</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Thursday</th>
<td>2###</td>
<td>4#.##</td>
<td>3###</td>
<td>5#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Tuesday</th>
<td>2###</td>
<td>3#.##</td>
<td>3###</td>
<td>6#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Wednesday</th>
<td>2###</td>
<td>4#.##</td>
<td>3###</td>
<td>5#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Seasonal Diagnosis

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="4" valign="top">Seasonal Diagnosis</th>
<th>-</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Chronic disease exacerbation</th>
<td>1###</td>
<td>9#.##</td>
<td>9###</td>
<td>7#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Respiratory infection</th>
<td>1###</td>
<td>8#.##</td>
<td>2###</td>
<td>1#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Length of Stay

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="3" valign="top">Length of Stay</th>
<th>&lt;2 days</th>
<td>7###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>1###</td>
</tr>
<tr>
<th>&gt;=2 days</th>
<td>8###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Discharge Destination

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="7" valign="top">Discharge Destination</th>
<th>Care Home</th>
<td>2###</td>
<td>3#.##</td>
<td>5###</td>
<td>6#.##</td>
<td>7###</td>
</tr>
<tr>
<th>Died</th>
<td>1###</td>
<td>3#.##</td>
<td>3###</td>
<td>6#.##</td>
<td>4###</td>
</tr>
<tr>
<th>Medical care</th>
<td>1###</td>
<td>2#.##</td>
<td>5###</td>
<td>7#.##</td>
<td>6###</td>
</tr>
<tr>
<th>Penal</th>
<td>3</td>
<td>1#.##</td>
<td>2###</td>
<td>8#.##</td>
<td>2###</td>
</tr>
<tr>
<th>Residence</th>
<td>1###</td>
<td>4#.##</td>
<td>1###</td>
<td>5#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Unknown</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>4###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

### Discharge Method

<table border="1" class="dataframe">
<thead>
<tr style="text-align: right;">
<th></th>
<th>is_acsc</th>
<th>ACSC</th>
<th>ACSC %</th>
<th>Non-ACSC</th>
<th>Non-ACSC %</th>
<th>Total</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="5" valign="top">Discharge Method</th>
<th>Died</th>
<td>5###</td>
<td>3#.##</td>
<td>1###</td>
<td>6#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Discharged</th>
<td>1###</td>
<td>3#.##</td>
<td>2###</td>
<td>6#.##</td>
<td>3###</td>
</tr>
<tr>
<th>Not Applicable</th>
<td>0</td>
<td>0#.##</td>
<td>1###</td>
<td>1#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Unknown</th>
<td>0</td>
<td>0#.##</td>
<td>1###</td>
<td>1#.##</td>
<td>1###</td>
</tr>
<tr>
<th>Total</th>
<td>1###</td>
<td>-</td>
<td>2###</td>
<td>-</td>
<td>3###</td>
</tr>
</tbody>
</table>

## Export Output for Sheffield

```python
timestamp = now.strftime("%Y_%m_%dT%H%M%S")
timestamp
```

    '2023_02_05T115115'

### Export as CSV

```python
# save df_results to a CSV to send to Sheffield for programmatic meta-analysis
# df_results.to_csv('path/to/results_timestamp.csv')
```

### Export as HTML

```python
output_head = f"""
<h1> LTH Admitted Care Analysis Tables Draft</h1>

<pre>
prepared: {timestamp}
email:    datascience@lthtr.nhs.uk
github:   <a href='https://github.com/LTHTR-DST/'>https://github.com/LTHTR-DST/</a>
</pre>
"""

fp = f"../reports/lth_admitted_care_analysis_tables_draft_{timestamp}.html"
with open(fp, "w") as f:
    x = df_results.to_html()
    x = output_head + x
    f.write(x)
```

```python
print(
    "Finished pipeline execution in",
    round((datetime.today() - now).total_seconds()),
    "seconds at",
    datetime.today(),
)
```

    Finished pipeline execution in 9 seconds at 2023-02-05 11:51:24.288155

The above outputs can easily be shared and if all sites used the same code, Sheffield should be able to generate the 'meta-analysis' more easily.

END OF NOTEBOOK

----------
