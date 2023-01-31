import numpy as np
import pandas as pd


def _age(df: pd.DataFrame) -> pd.DataFrame:

    age_labels = [
        "<20",
        "20 - 24",
        "25 - 29",
        "30 - 34",
        "35 - 39",
        "40 - 44",
        "45 - 49",
        "50 - 54",
        "55 - 59",
        "60 - 64",
        "65 - 69",
        "70 - 74",
        "75 - 79",
        "80 - 84",
        ">85",
    ]
    age_bins = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 999]

    df["admiage"] = pd.cut(df.activage, bins=age_bins, labels=age_labels)

    return df


def _gender(df: pd.DataFrame) -> pd.DataFrame:

    df["gender_cat"] = df.gender.astype(str).replace(
        {
            "1": "Male",
            "2": "Female",
            "9": "Indeterminate",
            "X": "Not Known",
            # if using the old gender code current NHS DD definition
            "0": "Not Known",
        }
    )

    return df


def _ethnos(df: pd.DataFrame) -> pd.DataFrame:

    df["ethnos_cat"] = df.ethnos.rename(
        {
            "A": "White",
            "B": "White",
            "C": "White",
            "D": "Mixed",
            "E": "Mixed",
            "F": "Mixed",
            "G": "Mixed",
            "H": "Asian or Asian British",
            "J": "Asian or Asian British",
            "K": "Asian or Asian British",
            "L": "Asian or Asian British",
            "M": "Black or Black British",
            "N": "Black or Black British",
            "P": "Black or Black British",
            "R": "Other Ethnic Groups",
            "S": "Other Ethnic Groups",
            "Z": "Not stated",
            "99": "Not known",
        }
    )
    return df


def _townsend(df: pd.DataFrame) -> pd.DataFrame:
    # Data spec variable: townsend_score_decile (2011 UK Townsend Deprivation Scores - Dataset - UK Data Service CKAN)

    df["townsend_score_quintile"] = (df.townsend_score_decile + 1) // 2
    df.townsend_score_quintile = df.townsend_score_quintile.replace({0: np.nan})

    return df


def _admisorc(df: pd.DataFrame) -> pd.DataFrame:

    df["admisorc_cat"] = df.admisorc.replace(
        {
            "19": "Residence",
            "29": "Residence",
            "39": "Penal",
            "49": "Medical care",
            "51": "Medical care",
            "52": "Medical care",
            "53": "Medical care",
            "54": "Care Home",
            "65": "Care Home",
            "66": "Residence",
            "79": "Residence",
            "85": "Care Home",
            "86": "Care Home",
            "87": "Medical care",
            "88": "Care Home",
            "98": "Unknown",
            "99": "Unknown",
        }
    )
    return df


def _admidate(df: pd.DataFrame) -> pd.DataFrame:

    df.admidate = pd.to_datetime(df.admidate)

    df["admidayofweek"] = df.admidate.dt.strftime("%A")

    return df


def _diag_seasonal(df: pd.DataFrame) -> pd.DataFrame:
    replacement_3char = {
        "J09": "Respiratory infection",
        "J10": "Respiratory infection",
        "J11": "Respiratory infection",
        "J12": "Respiratory infection",
        "J13": "Respiratory infection",
        "J14": "Respiratory infection",
        "J15": "Respiratory infection",
        "J16": "Respiratory infection",
        "J17": "Respiratory infection",
        "J18": "Respiratory infection",
        "J20": "Respiratory infection",
        "J21": "Respiratory infection",
        "J22": "Respiratory infection",
        "J00": "Respiratory infection",
        "J01": "Respiratory infection",
        "J02": "Respiratory infection",
        "J03": "Respiratory infection",
        "J04": "Respiratory infection",
        "J05": "Respiratory infection",
        "J06": "Respiratory infection",
        "J40": "Chronic disease exacerbation",
        "J41": "Chronic disease exacerbation",
        "J42": "Chronic disease exacerbation",
        "J43": "Chronic disease exacerbation",
        "J44": "Chronic disease exacerbation",
        "J45": "Chronic disease exacerbation",
        "J46": "Chronic disease exacerbation",
        "J47": "Chronic disease exacerbation",
        "U10": "Respiratory infection",
    }

    replacement_4char = {
        "U071": "Respiratory infection",
        "U072": "Respiratory infection",
    }

    df["diag_seasonal_cat"] = (
        df.diag_01.replace(replacement_4char).str.slice(0, 3).replace(replacement_3char)
    )

    df.diag_seasonal_cat = df.diag_seasonal_cat.where(
        df.diag_seasonal_cat.isin(
            ["Respiratory infection", "Chronic disease exacerbation"]
        ),
        np.nan,
    )

    return df


def _length_of_stay(df: pd.DataFrame) -> pd.DataFrame:
    # validate length of stay so that there are no negative values. Negative values will get binned as <2 days

    f["length_of_stay_cat"] = pd.cut(
        df.length_of_stay, bins=[-np.inf, 2, np.inf], labels=["<2 days", ">=2 days"]
    )
    df["length_of_stay_cat"].value_counts(dropna=False)

    return df


def _disdest(df: pd.DataFrame) -> pd.DataFrame:

    df["disdest_cat"] = df.disdest.replace(
        {
            19: "Residence",
            29: "Residence",
            30: "Medical care",
            37: "Penal",
            38: "Penal",
            39: "Penal",
            48: "Medical care",
            49: "Medical care",
            50: "Medical care",
            51: "Medical care",
            52: "Medical care",
            53: "Medical care",
            54: "Care Home",
            65: "Care Home",
            66: "Residence",
            79: "Died",
            84: "Medical care",
            85: "Care Home",
            87: "Medical care",
            88: "Care Home",
            98: "Unknown",
            99: "Unknown",
        }
    )

    return df


def _dismeth(df: pd.DataFrame) -> pd.DataFrame:

    df["dismeth_cat"] = df.dismeth.replace(
        {
            1: "Discharged",
            2: "Discharged",
            3: "Discharged",
            4: "Died",
            5: "Died",
            8: "Not Applicable",
            9: "Unknown",
        }
    )

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
