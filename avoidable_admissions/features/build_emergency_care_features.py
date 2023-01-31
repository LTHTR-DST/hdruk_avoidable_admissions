import numpy as np
import pandas as pd


def _age(ecds: pd.DataFrame) -> pd.DataFrame:

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

    ecds["activage_cat"] = pd.cut(ecds.activage, bins=age_bins, labels=age_labels)

    return ecds


def _gender(ecds: pd.DataFrame) -> pd.DataFrame:

    ecds["gender_cat"] = ecds.gender.astype(str).replace(
        {
            "1": "Male",
            "2": "Female",
            "9": "Indeterminate",
            "X": "Not Known",
            # if using the old gender code current NHS DD definition
            "0": "Not Known",
        }
    )

    return ecds


def _ethnos(ecds: pd.DataFrame) -> pd.DataFrame:

    ecds["ethnos_cat"] = ecds.ethnos.rename(
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
    return ecds


def _townsend(ecds: pd.DataFrame) -> pd.DataFrame:
    # Data spec variable: townsend_score_decile (2011 UK Townsend Deprivation Scores - Dataset - UK Data Service CKAN)

    ecds["townsend_score_quintile"] = (ecds.townsend_score_decile + 1) // 2
    ecds.townsend_score_quintile = ecds.townsend_score_quintile.replace({0: np.nan})

    return ecds


def _accomondationstatus(ecds: pd.DataFrame) -> pd.DataFrame:
    ecds["accommodationstatus_cat"] = ecds.accommodationstatus.replace(
        {
            0: np.nan,
            1064831000000106: "Unknown",
            1064841000000102: "Unknown",
            1066881000000100: "Unknown",
            160734000: "Yes",
            224221006: "No",
            224225002: "No",
            224231004: "No",
            32911000: "No",
            394923006: "No",
            414418009: "No",
        }
    )
    return ecds


def _edarivalemode(ecds: pd.DataFrame) -> pd.DataFrame:
    ecds["edarrivalmode_cat"] = ecds.edarrivalmode.replace(
        {
            0: np.nan,
            1048061000000105: "Walk-In",
            1048071000000103: "Walk-In",
            2018310000: "Ambulance",
            2018350000: "Ambulance",
            2018370000: "Ambulance",
            2018510000: "Ambulance",
            2018550000: "Other",
            2018810000: "Other",
            2018910000: "Other",
        }
    )

    return ecds


def _edattendsource(ecds: pd.DataFrame) -> pd.DataFrame:
    ecds["edattendsource_cat"] = ecds.edattendsource.replace(
        {
            0: np.nan,
            1052681000000105: "Community",
            1065391000000104: "Personal",
            1065401000000101: "Community",
            1065991000000100: "Community",
            1066001000000101: "Community",
            1066011000000104: "Community",
            1066021000000105: "Emergency Services",
            1066031000000107: "Emergency Services",
            1066041000000103: "Emergency Services",
            1066051000000100: "Emergency Services",
            1066061000000102: "Emergency Services",
            1066431000000102: "Hospital",
            1066441000000106: "Hospital",
            1077191000000103: "Community",
            1077201000000101: "Community",
            1077211000000104: "Community",
            1077761000000105: "Community",
            1079521000000104: "Hospital",
            166941000000106: "Primary Care",
            185363009: "Community",
            185366001: "Community",
            185368000: "Community",
            185369008: "Community",
            198261000000104: "Emergency Services",
            276491000: "Primary Care",
            315261000000101: "Personal",
            507291000000100: "Personal",
            835091000000109: "Hospital",
            835101000000101: "Hospital",
            877171000000103: "Community",
            879591000000102: "Primary Care",
            889801000000100: "Emergency Services",
        }
    )

    return ecds


def _edacuity(ecds: pd.DataFrame) -> pd.DataFrame:
    ecds["edacuity_cat"] = ecds.edacuity.replace(
        {
            0: np.nan,
            1064891000000107: "1 - Immediate care level emergency care",
            1064901000000108: "3 - Urgent level emergency care",
            1064911000000105: "2 - Very urgent level emergency care",
            1077241000000103: "4 - Standard level emergency care",
            1077251000000100: "5 - Low acuity level emergency care",
        }
    )
    return ecds


# edinvest


def _edinvest(ecds: pd.DataFrame) -> pd.DataFrame:
    cols = ecds.filter(regex="edinvest_[0-9]{2}$").columns
    replacements = {
        0: np.nan,
        1088291000000101: np.nan,
        167252002: "Non-urgent",
        27171005: "Non-urgent",
        53115007: "Non-urgent",
        67900009: "Non-urgent",
    }
    for col in cols:

        # if value is in replacements, keep the value, else use 'Urgent' for all others
        # then use replacements to assign the other categories
        ecds[col + "_cat"] = (
            ecds[col]
            .where(ecds[col].isin(replacements), "Urgent")
            .replace(replacements)
        )

    return ecds


def _edtreat(ecds: pd.DataFrame) -> pd.DataFrame:
    # edtreat
    cols = ecds.filter(regex="edtreat_[0-9]{2}$").columns
    replacements = {
        0: np.nan,
        183964008: np.nan,
        266712008: "Non-urgent",
        413334001: "Non-urgent",
        81733005: "Non-urgent",
    }
    for col in cols:

        # if value is in replacements, keep the value, else use 'Urgent' for all others
        # then use replacements to assign the other categories
        ecds[col + "_cat"] = (
            ecds[col]
            .where(ecds[col].isin(replacements), "Urgent")
            .replace(replacements)
        )

    return ecds


def _eddiag(ecds: pd.DataFrame) -> pd.DataFrame:
    # Only use first diagnosis recorded (eddiag_01) to record seasonal diagnosis
    replacements = {
        0: np.nan,
        12295008: "Chronic disease exacerbation",
        1325161000000102: "Respiratory infection",
        1325171000000109: "Respiratory infection",
        1325181000000106: "Respiratory infection",
        13645005: "Chronic disease exacerbation",
        195951007: "Chronic disease exacerbation",
        195967001: "Chronic disease exacerbation",
        205237003: "Respiratory infection",
        233604007: "Respiratory infection",
        278516003: "Respiratory infection",
        36971009: "Respiratory infection",
        50417007: "Respiratory infection",
        54150009: "Respiratory infection",
        6142004: "Respiratory infection",
        62994001: "Respiratory infection",
        80384002: "Respiratory infection",
        90176007: "Respiratory infection",
    }

    # if value is in replacements, keep the value, else use 'Urgent' for all others
    # then use replacements to assign the other categories
    ecds["eddiag_seasonal_cat"] = ecds.eddiag_01.where(
        ecds.eddiag_01.isin(replacements), np.nan
    ).replace(replacements)

    return ecds


def _edattenddispatch(ecds: pd.DataFrame) -> pd.DataFrame:
    # Discharge Destination

    ecds["edattenddispatch_cat"] = ecds.edattenddispatch.replace(
        {
            0: np.nan,
            1066331000000109: "Ambulatory / Short Stay",
            1066341000000100: "Ambulatory / Short Stay",
            1066351000000102: "Ambulatory / Short Stay",
            1066361000000104: "Admitted",
            1066371000000106: "Admitted",
            1066381000000108: "Admitted",
            1066391000000105: "Admitted",
            1066401000000108: "Admitted",
            183919006: "Transfer",
            19712007: "Transfer",
            305398007: "Died",
            306689006: "Discharged",
            306691003: "Discharged",
            306694006: "Discharged",
            306705005: "Discharged",
            306706006: "Admitted",
            50861005: "Discharged",
        }
    )
    return ecds


def _edrefservice(ecds: pd.DataFrame) -> pd.DataFrame:

    replacements = {
        0: np.nan,
        1064851000000104: "Medical",
        183516009: "Medical",
        183518005: "Medical",
        183519002: "Medical",
        183521007: "Medical",
        183522000: "Medical",
        183523005: "Medical",
        183524004: "Psychiatric",
        183542009: "Surgical",
        183543004: "Surgical",
        183544005: "Surgical",
        183545006: "Surgical",
        183546007: "Surgical",
        183548008: "ObGyn",
        183549000: "ObGyn",
        183561008: "Local Medical",
        202291000000107: "Psychiatric",
        247541000000106: "Community / OPD",
        276490004: "Local Medical",
        306107006: "Critical Care",
        306111000: "Medical",
        306114008: "Medical",
        306118006: "Medical",
        306123006: "Medical",
        306124000: "Medical",
        306125004: "Medical",
        306127007: "Medical",
        306129005: "Community / OPD",
        306136006: "Psychiatric",
        306138007: "Psychiatric",
        306140002: "Medical",
        306148009: "Medical",
        306152009: "Local Medical",
        306182003: "Surgical",
        306184002: "Surgical",
        306198005: "Surgical",
        306200004: "Surgical",
        306201000: "Surgical",
        306237005: "Medical",
        306285006: "Medical",
        306802002: "Medical",
        306934005: "Surgical",
        307374004: "Medical",
        307375003: "Community / OPD",
        307376002: "Community / OPD",
        307380007: "Community / OPD",
        327121000000104: "Surgical",
        353961000000104: "Community / OPD",
        380241000000107: "Psychiatric",
        382271000000102: "Critical Care",
        384711009: "Surgical",
        384712002: "Surgical",
        38670004: "Community / OPD",
        413127007: "Psychiatric",
        415263003: "Community / OPD",
        4266003: "Community / OPD",
        516511000000107: "Community / OPD",
        61801003: "Community / OPD",
        770411000000102: "Local Medical",
        770677000: "Critical Care",
        78429003: "Community / OPD",
        785621000000108: "Community / OPD",
        785681000000109: "Community / OPD",
        785701000000106: "Community / OPD",
        785721000000102: "Community / OPD",
        785761000000105: "Community / OPD",
        785781000000101: "Community / OPD",
        811391000000104: "Community / OPD",
        818861000000107: "Community / OPD",
        823961000000102: "Community / OPD",
        894171000000100: "Community / OPD",
        898791000000105: "Medical",
        975951000000109: "Critical Care",
    }
    ecds["edrefservice_cat"] = ecds.edrefservice.where(
        ecds.edrefservice.isin(replacements), "Other"
    ).replace(replacements)

    return ecds
