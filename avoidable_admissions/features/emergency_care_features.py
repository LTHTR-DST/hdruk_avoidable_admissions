import numpy as np
import pandas as pd

from avoidable_admissions.features import feature_maps


def _age(df: pd.DataFrame) -> pd.DataFrame:

    age_labels = feature_maps.age_labels
    age_bins = feature_maps.age_bins
    df["activage_cat"] = pd.cut(df.activage, bins=age_bins, labels=age_labels)

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

    return df


def _accomondationstatus(df: pd.DataFrame) -> pd.DataFrame:

    df["accommodationstatus_cat"] = df.accommodationstatus.replace(
        feature_maps.accomodationstatus
    )
    return df


def _edarivalemode(df: pd.DataFrame) -> pd.DataFrame:

    df["edarrivalmode_cat"] = df.edarrivalmode.replace(feature_maps.edarrivalmode)

    return df


def _edattendsource(df: pd.DataFrame) -> pd.DataFrame:

    df["edattendsource_cat"] = df.edattendsource.replace(feature_maps.edattendsource)

    return df


def _edacuity(df: pd.DataFrame) -> pd.DataFrame:

    df["edacuity_cat"] = df.edacuity.replace(feature_maps.edacuity)

    return df


def _edinvest(df: pd.DataFrame) -> pd.DataFrame:

    cols = df.filter(regex="edinvest_[0-9]{2}$").columns
    replacements = feature_maps.edinvest

    for col in cols:

        # if value is in replacements, keep the value, else use 'Urgent' for all others
        # then use replacements to assign the other categories
        df[col + "_cat"] = (
            df[col].where(df[col].isin(replacements), "Urgent").replace(replacements)
        )

    return df


def _edtreat(df: pd.DataFrame) -> pd.DataFrame:

    cols = df.filter(regex="edtreat_[0-9]{2}$").columns
    replacements = feature_maps.edtreat
    for col in cols:

        # if value is in replacements, keep the value, else use 'Urgent' for all others
        # then use replacements to assign the other categories
        df[col + "_cat"] = (
            df[col].where(df[col].isin(replacements), "Urgent").replace(replacements)
        )

    return df


def _eddiag_seasonal(df: pd.DataFrame) -> pd.DataFrame:
    # Only use first diagnosis recorded (eddiag_01) to record seasonal diagnosis
    replacements = feature_maps.eddiag_seasonal

    # if value is in replacements, keep the value, else use 'Urgent' for all others
    # then use replacements to assign the other categories
    df["eddiag_seasonal_cat"] = df.eddiag_01.where(
        df.eddiag_01.isin(replacements), np.nan
    ).replace(replacements)

    return df


def _edattenddispatch(df: pd.DataFrame) -> pd.DataFrame:
    # Discharge Destination

    df["edattenddispatch_cat"] = df.edattenddispatch.replace(
        feature_maps.edattenddispatch
    )
    return df


def _edrefservice(df: pd.DataFrame) -> pd.DataFrame:

    replacements = feature_maps.edrefservice

    df["edrefservice_cat"] = df.edrefservice.where(
        df.edrefservice.isin(replacements), "Other"
    ).replace(replacements)

    return df


def _eddiagqual(df: pd.DataFrame) -> pd.DataFrame:
    # Only applicable to eddiag_01
    # This deviates from the spec by assigning nan to values not in the spec

    replacements = feature_maps.eddiagqual
    df["eddiagqual_01_cat"] = df.eddiagqual_01.where(
        df.eddiagqual_01.isin(replacements), np.nan
    ).replace(replacements)

    return df


def build_all(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.pipe(_age)
        .pipe(_accomondationstatus)
        .pipe(_edacuity)
        .pipe(_edarivalemode)
        .pipe(_edattenddispatch)
        .pipe(_edattendsource)
        .pipe(_eddiag_seasonal)
        .pipe(_eddiagqual)
        .pipe(_edinvest)
        .pipe(_edrefservice)
        .pipe(_edtreat)
        .pipe(_ethnos)
        .pipe(_gender)
        .pipe(_townsend)
    )

    return df
