import pandas as pd

from avoidable_admissions.features import (admitted_care_features,
                                           emergency_care_features)


def build_admitted_care_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate features described in the Admitted Care Data Specification

    See [Analysis Pipeline][data-analysis-pipeline] for more information

    Args:
        df (Pandas DataFrame): Dataframe that has passed the first validation step

    Returns:
        pd.DataFrame: Dataframe with additional feature columns


    ## Feature Engineering Example:

    ``` python
    import pandas as pd
    from avoidable_admissions.data.validate import (
        validate_dataframe,
        AdmittedCareEpisodeSchema
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

    # Second validation step and continue...
    ```

    See [Analysis Pipeline][data-analysis-pipeline] for more information.
    """

    df = admitted_care_features.build_all(df)

    return df


def build_emergency_care_features(df: pd.DataFrame) -> pd.DataFrame:

    df = emergency_care_features.build_all(df)

    return df
