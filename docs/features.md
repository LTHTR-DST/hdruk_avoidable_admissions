# Feature Engineering

Feature engineering is the process of generating new variables from one or more existing variables.

The Data Processing document defined by the lead team provides excellent and explicit documentation on what new features are expected. Refer to these documents for more details.

- [HDRUK Data Processing V1 Google Docs](https://docs.google.com/document/d/1vysTKmvELK-5Rr7Dib3zDp8mCe_lUVr2e5EES23ShbQ/edit)

The functions described below generate these features automatically in preparation for the second validation step and further analysis.

Ensure that data has undergone preprocessing and has passed the first validation step as described in the [analysis pipeline][data-analysis-pipeline] before using these functions.

## Error codes

A pragmatic approach has been used in dealing with missing data, unmapped codes and codes not in refsets.
Please read section on [missing values][missing-values] in the [Data Validation][data-validation] chapter as well.

During feature engineering, especially in the Emergency Care dataset that has several columns with SNOMED codes, the following rules are applied to assign the appropriate categories.

| Source Data   | Mapping   | Refset    | Category                              | Who fixes             |
|:-------------:|:---------:|:---------:|---------------------------------------|-----------------------|
| Yes           | Yes       | Yes       | Assign to `Category`                  |                       |
| Yes           | No        | Yes       | `ERROR:Unmapped - In Refset`          | Lead site to advise   |
| Yes           | Yes       | No        | `ERROR:Not In Refset|{Category}`   | Lead site to fix      |
| No            | x         | x         | `ERROR:Missing Data`                  | Local site if feasible|
| Yes           | No        | No        | `ERROR:Unmapped - Not In Refset`      | Local site to fix     |

Please see the source code for [`feature_maps.py`](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/features/feature_maps.py) and raise a [GitHub issue](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/issues) for any questions or bugs.

::: avoidable_admissions.features.build_features
    handler: python
    options:
        members:
            - build_admitted_care_features
            - build_emergency_care_features
        show_root_heading: false

Read the source code for generating [admitted care features](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/features/admitted_care_features.py) and [emergency care features](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/features/emergency_care_features.py) on GitHub.
