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
