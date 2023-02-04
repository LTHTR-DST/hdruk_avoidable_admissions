# Data Validation

There are multiple schema defined for validation of different datasets at different pipeline stages.

::: avoidable_admissions.data.validate
    handler: python
    options:
        members:
            - validate_dataframe
            - validate_admitted_care_data
            - validate_admitted_care_features
            - validate_emergency_care_data
            - validate_emergency_care_features
            - get_schema_properties
        show_root_heading: false

## Fixing Errors

It is likely that data validation will fail on a subset of the data the first few times.
Fixing errors will be an iterative process and the following are some examples.

Please see <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/> for more examples.

Errors in validation after feature generation may be caused by extraneous codes that are not specified in the data specification.

### Examples

``` python
# Convert to date

df['admidate'] = pd.to_datetime(df['admidate'], yearfirst=True)
df['admidate'] = df['admidate'].dt.date


# Fill missing SNOMED codes with 0.
# Else valiation will fail as nan is treated as float.
df['accommodationstatus'] = df['accommodationstatus'].fillna(0)
```

## Mising Values

_To be finalised after further discussion and testing._

There is an entire chapter in Pandas documentation on [missing values](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#) which is an important read for any data scientist.

For the purposes of this project, several pragmatic choices have been made regarding how missing values are treated.

1. Where a definition exists for how missing values should be coded, for instance in the NHS data model, use this.
2. For SNOMED codes, which are always integers, use 0 (zero) to replace all missing values. This avoids validation errors caused by `NaN` values that are treated as `float` dtype by Pandas.
3. For strings, use `"-"` (without the quotes) for missing values.
4. During feature engineering, if a code has not been assigned a category in the specification, the value `"Other"` is assigned.
