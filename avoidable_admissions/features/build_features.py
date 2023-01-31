import pandas as pd

from avoidable_admissions.features import (admitted_care_features,
                                           emergency_care_features)


def build_admitted_care_features(df: pd.DataFrame) -> pd.DataFrame:

    df = admitted_care_features.build_all(df)

    return df


def build_emergency_care_features(df: pd.DataFrame) -> pd.DataFrame:

    df = emergency_care_features.build_all(df)

    return df
