import numpy as np
import pandas as pd

from avoidable_admissions.features import feature_maps


def _age(df: pd.DataFrame) -> pd.DataFrame:

    age_labels = feature_maps.age_labels
    age_bins = feature_maps.age_bins

    df["admiage_cat"] = pd.cut(df.admiage, bins=age_bins, labels=age_labels)

    return df


def _gender(df: pd.DataFrame) -> pd.DataFrame:

    df["gender_cat"] = df.gender.astype(str).replace(feature_maps.gender)

    return df


def _ethnos(df: pd.DataFrame) -> pd.DataFrame:

    df["ethnos_cat"] = df.ethnos.replace(feature_maps.ethnos)
    return df


def _townsend(df: pd.DataFrame) -> pd.DataFrame:
    # Data spec variable: townsend_score_decile (2011 UK Townsend Deprivation Scores - Dataset - UK Data Service CKAN)

    df["townsend_score_quintile"] = (df.townsend_score_decile + 1) // 2
    df.townsend_score_quintile = df.townsend_score_quintile.replace({0: np.nan})

    return df


def _admisorc(df: pd.DataFrame) -> pd.DataFrame:

    df["admisorc_cat"] = df.admisorc.replace(feature_maps.admisorc)
    return df


def _admidate(df: pd.DataFrame) -> pd.DataFrame:

    df.admidate = pd.to_datetime(df.admidate)
    # %A returns the full name of the day of week
    # An alternative approach to be do `df.admidate.dt.dayofweek` and map to day names

    df["admidayofweek"] = df.admidate.dt.strftime("%A")

    return df


def _diag_seasonal(df: pd.DataFrame) -> pd.DataFrame:

    replacement_3char = feature_maps.admdiag_seasonal_3char
    replacement_4char = feature_maps.admdiag_seasonal_4char

    # The allowed categories are unique values in both replacement dicts
    x = set(feature_maps.admdiag_seasonal_3char.values())
    y = set(feature_maps.admdiag_seasonal_4char.values())
    allowed_categories = x.union(y)

    # First replace all 4 char ICD10 codes as they should be exact matches
    # Then slice the remaining codes to get first 3 characters and replace using the 3char mapping
    # Finally, if the end values are not in the 2 allowed categories, replace with nan.

    df["diag_seasonal_cat"] = (
        df.diag_01.replace(replacement_4char).str.slice(0, 3).replace(replacement_3char)
    )

    # If the final values are not in allowed_categories, replace with nan.
    df.diag_seasonal_cat = df.diag_seasonal_cat.where(
        df.diag_seasonal_cat.isin(allowed_categories),
        np.nan,
    )

    return df


def _length_of_stay(df: pd.DataFrame) -> pd.DataFrame:

    # Validate length of stay so that there are no negative values.
    # Negative values will get binned as <2 days

    df["length_of_stay_cat"] = pd.cut(
        df.length_of_stay, bins=[-np.inf, 2, np.inf], labels=["<2 days", ">=2 days"]
    )

    return df


def _disdest(df: pd.DataFrame) -> pd.DataFrame:

    df["disdest_cat"] = df.disdest.replace(feature_maps.disdest)

    return df


def _dismeth(df: pd.DataFrame) -> pd.DataFrame:

    df["dismeth_cat"] = df.dismeth.replace(feature_maps.dismeth)

    return df


def build_all(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.pipe(_age)
        .pipe(_gender)
        .pipe(_ethnos)
        .pipe(_townsend)
        .pipe(_admisorc)
        .pipe(_admidate)
        .pipe(_diag_seasonal)
        .pipe(_length_of_stay)
        .pipe(_disdest)
        .pipe(_dismeth)
    )

    return df
