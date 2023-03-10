import numpy as np
import pandas as pd

from avoidable_admissions.features import feature_maps


def replace_values(
    data: pd.Series, replacements: dict, other: str = "ERROR:Unmapped - Not In Refset"
) -> pd.Series:
    # if value is in replacements, keep the value, else use `other` for all others
    # then use replacements to assign the other categories

    data_cat = (
        data.where(data.isin(replacements), other).replace(replacements).astype(str)
    )

    return data_cat


def _age(df: pd.DataFrame) -> pd.DataFrame:

    age_labels = feature_maps.age_labels
    age_bins = feature_maps.age_bins
    df["activage_cat"] = pd.cut(df.activage, bins=age_bins, labels=age_labels)
    df["activage_cat"] = df["activage_cat"].astype(str)

    return df


def _gender(df: pd.DataFrame) -> pd.DataFrame:

    df["gender_cat"] = replace_values(df.gender.astype(str), feature_maps.gender)

    return df


def _ethnos(df: pd.DataFrame) -> pd.DataFrame:

    df["ethnos_cat"] = replace_values(df.ethnos, feature_maps.ethnos)

    return df


def _accommodationstatus(df: pd.DataFrame) -> pd.DataFrame:

    df["accommodationstatus_cat"] = replace_values(
        df.accommodationstatus, feature_maps.accommodationstatus
    )

    return df


def _edarrivaldatetime(df: pd.DataFrame) -> pd.DataFrame:

    df.edarrivaldatetime = pd.to_datetime(df.edarrivaldatetime)
    df["edarrival_dayofweek"] = df.edarrivaldatetime.dt.strftime("%A")
    df["edarrival_hourofday"] = df.edarrivaldatetime.dt.hour

    return df


def _edarivalemode(df: pd.DataFrame) -> pd.DataFrame:

    df["edarrivalmode_cat"] = replace_values(
        df.edarrivalmode, feature_maps.edarrivalmode
    )

    return df


def _edattendsource(df: pd.DataFrame) -> pd.DataFrame:

    df["edattendsource_cat"] = replace_values(
        df.edattendsource, feature_maps.edattendsource
    )

    return df


def _edacuity(df: pd.DataFrame) -> pd.DataFrame:

    df["edacuity_cat"] = replace_values(df.edacuity, feature_maps.edacuity)

    return df


def _edinvest(df: pd.DataFrame) -> pd.DataFrame:

    cols = df.filter(regex="edinvest_[0-9]{2}$").columns
    replacements = feature_maps.edinvest

    for col in cols:

        df[col + "_cat"] = replace_values(df[col], replacements, "Urgent")

    return df


def _edtreat(df: pd.DataFrame) -> pd.DataFrame:

    cols = df.filter(regex="edtreat_[0-9]{2}$").columns
    replacements = feature_maps.edtreat
    for col in cols:

        df[col + "_cat"] = replace_values(df[col], replacements, "Urgent")

    return df


def _eddiag_seasonal(df: pd.DataFrame) -> pd.DataFrame:
    # Only use first diagnosis recorded (eddiag_01) to record seasonal diagnosis

    df["eddiag_seasonal_cat"] = replace_values(
        df.eddiag_01, feature_maps.eddiag_seasonal
    )

    return df


def _edattenddispatch(df: pd.DataFrame) -> pd.DataFrame:
    # Discharge Destination

    df["edattenddispatch_cat"] = replace_values(
        df.edattenddispatch, feature_maps.edattenddispatch
    )

    return df


def _edrefservice(df: pd.DataFrame) -> pd.DataFrame:

    df["edrefservice_cat"] = replace_values(
        df.edrefservice, feature_maps.edrefservice, "Other"
    )

    return df


def _eddiagqual(df: pd.DataFrame) -> pd.DataFrame:
    # Only applicable to eddiag_01

    df["eddiagqual_01_cat"] = replace_values(df.eddiagqual_01, feature_maps.eddiagqual)

    return df


def _acsc_code(df: pd.DataFrame) -> pd.DataFrame:

    # TODO: This section needs manual review of a good sample size to ensure it works

    acsc_mapping = feature_maps.load_ed_acsc_mapping()
    df["eddiag_01_acsc"] = replace_values(df.eddiag_01, acsc_mapping)

    return df


def _disstatus(df: pd.DataFrame) -> pd.DataFrame:

    df["disstatus_cat"] = replace_values(df.disstatus, feature_maps.disstatus)

    return df

def _cc_code(df: pd.DataFrame) -> pd.DataFrame:

    # TODO: This section needs manual review of a good sample size to ensure it works

    cc_mapping = feature_maps.load_ed_cc_mapping()
    df["edchiefcomplaint_cat"] = replace_values(df.edchiefcomplaint, cc_mapping)

    return df



def build_all(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.pipe(_age)
        .pipe(_accommodationstatus)
        .pipe(_acsc_code)
        .pipe(_cc_code)
        .pipe(_disstatus)
        .pipe(_edacuity)
        .pipe(_edarivalemode)
        .pipe(_edarrivaldatetime)
        .pipe(_edattenddispatch)
        .pipe(_edattendsource)
        .pipe(_eddiag_seasonal)
        .pipe(_eddiagqual)
        .pipe(_edinvest)
        .pipe(_edrefservice)
        .pipe(_edtreat)
        .pipe(_ethnos)
        .pipe(_gender)
    )

    return df
