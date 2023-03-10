import numpy as np
import pandas as pd

from avoidable_admissions.features import feature_maps


def _age(df: pd.DataFrame) -> pd.DataFrame:

    age_labels = feature_maps.age_labels
    age_bins = feature_maps.age_bins

    df["admiage_cat"] = pd.cut(df.admiage, bins=age_bins, labels=age_labels)

    return df


def _gender(df: pd.DataFrame) -> pd.DataFrame:

    df["gender_cat"] = df.gender.replace(feature_maps.gender)

    return df


def _ethnos(df: pd.DataFrame) -> pd.DataFrame:

    df["ethnos_cat"] = df.ethnos.replace(feature_maps.ethnos)
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

    # If the final values are not in allowed_categories, replace with "-".
    df.diag_seasonal_cat = df.diag_seasonal_cat.where(
        df.diag_seasonal_cat.isin(allowed_categories),
        "-",
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


def _acsc_code(df: pd.DataFrame) -> pd.DataFrame:

    # TODO: This section needs manual review of a good sample size to ensure it works

    acsc_mapping = feature_maps.load_apc_acsc_mapping()
    df["diag_01_acsc"] = df.diag_01.replace(acsc_mapping)
    df.diag_01_acsc = df.diag_01_acsc.where(
        df.diag_01_acsc.isin(set(acsc_mapping.values())), "-"
    )

    return df


def _procedures(df: pd.DataFrame) -> pd.DataFrame:
    """Using primary and all secondary procedure codes, categorise as follows to determine
    whether a patient had any procedures or not:

    No:
        - = No procedures performed
    Count:
        4an = Procedure code

    Missing:
        & = Not known
        X998 = Procedure carried out but no appropriate OPCS-4 code available (submitted value present between 1997-98 and 2005-07)
        X999 = No procedure carried out (submitted value present between 1997-98 and 2001-02)

    # TODO: Clarify how the X99* codes need to be dealt with. These codes do not appear in LTH data.

    # 1. Filter all operation columns (01-12).
    # 2. Use regex to replace X998, X999 and O, Y and Z codes (these indicate anatomy, site or method of operation  )
    # 3. Count number of non-null values across each row

    # opertn_count should be >=0
    """
    # TODO: Instead of replacing invalid codes with nan, should we count only valid OPCS codes

    df["opertn_count"] = (
        df.filter(regex="opertn_[0-1][0-9]$")
        .replace({"X99[8-9]|[OYZ][0-9]+|\-": np.nan}, regex=True)
        .count(axis=1)
    )

    rules = {
        'Yes': df['opertn_count'] > 0,
        'No': df['opertn_count'] <= 0,
        'Missing': df['opertn_count'].isna()
    }

    df['opertn_cat'] = np.select(
        list(rules.values()), list(rules.keys()), default='Missing'
    )    

    return df

def _comorbidities(df: pd.DataFrame) -> pd.DataFrame:        
    diag_cols = [f'diag_{i:02d}' for i in range(2, 21)]
    df['comorb_count'] = df[diag_cols].count(axis=1)
    df['comorb_cat'] = df['comorb_count'].apply(lambda x: 'Yes' if x > 0 else 'No')

    return df



def build_all(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.pipe(_age)
        .pipe(_gender)
        .pipe(_ethnos)
        .pipe(_admisorc)
        .pipe(_admidate)
        .pipe(_diag_seasonal)
        .pipe(_length_of_stay)
        .pipe(_disdest)
        .pipe(_dismeth)
        .pipe(_acsc_code)
        .pipe(_procedures)
        .pipe(_comorbidities)
    )

    return df
