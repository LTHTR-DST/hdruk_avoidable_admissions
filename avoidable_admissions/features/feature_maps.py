from functools import lru_cache
from typing import Dict

import numpy as np
import pandas as pd

age_labels = [
    "18-19",
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

age_bins = age_bins = [17, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 130]


gender = {
    "1": "Male",
    "2": "Female",
    "9": "Indeterminate",
    "X": "Not Known",
    # if using the old gender code current NHS DD definition
    "0": "Not Known",
}

ethnos = {
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

accomodationstatus = {
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

edarrivalmode = {
    0: np.nan,
    1047991000000102: "Sheffield-ToDo",
    1048001000000106: "Sheffield-ToDo",
    1048021000000102: "Sheffield-ToDo",
    1048031000000100: "Sheffield-ToDo",
    1048041000000109: "Sheffield-ToDo",
    1048051000000107: "Sheffield-ToDo",
    1048061000000105: "Walk-In",
    1048071000000103: "Walk-In",
    1048081000000101: "Sheffield-ToDo",
}

edattendsource = {
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
    1082331000000106: "Primary Care",  # OOH
    166941000000106: "Primary Care",
    183877003: "Private Referral",  # from refset
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

edacuity = {
    0: np.nan,
    1064891000000107: "1 - Immediate care level emergency care",
    1064901000000108: "3 - Urgent level emergency care",
    1064911000000105: "2 - Very urgent level emergency care",
    1077241000000103: "4 - Standard level emergency care",
    1077251000000100: "5 - Low acuity level emergency care",
}

edinvest = {
    0: np.nan,
    1088291000000101: np.nan,
    167252002: "Non-urgent",
    27171005: "Non-urgent",
    53115007: "Non-urgent",
    67900009: "Non-urgent",
}

edtreat = {
    0: np.nan,
    183964008: np.nan,
    266712008: "Non-urgent",
    413334001: "Non-urgent",
    81733005: "Non-urgent",
}

eddiag_seasonal = {
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

eddiagqual = {
    415684004: "Suspected",
    410605003: "Confirmed",
}

edattenddispatch = {
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

edrefservice = {
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

disstatus = {
    0: np.nan,
    1066301000000103: "Non-urgent",
    1066311000000101: "Non-urgent",
    1066321000000107: "Non-urgent",
    1077021000000100: "Non-urgent",
    1077031000000103: "Urgent",
    1077041000000107: "Urgent",
    1077051000000105: "Urgent",
    1077061000000108: "Urgent",
    1077071000000101: "Urgent",
    1077081000000104: "Urgent",
    1077091000000102: "Urgent",
    1077101000000105: "Urgent",
    1077781000000101: "Urgent",
    1324201000000109: "Urgent",
    182992009: "Non-urgent",
    63238001: "Died",
    75004002: "Died",
}


admisorc = {
    "19": "Residence",
    "29": "Residence",
    "37": "Penal",  # CDS V6-3
    "39": "Penal",
    "40": "Penal",  # CDS V6-3
    "49": "Medical care",
    "51": "Medical care",
    "52": "Medical care",
    "53": "Medical care",
    "54": "Care Home",
    "55": "Care Home",  # CDS V6-3
    "56": "Care Home",  # CDS V6-3
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

admdiag_seasonal_3char = {
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

admdiag_seasonal_4char = {
    "U071": "Respiratory infection",
    "U072": "Respiratory infection",
}

disdest = {
    "19": "Residence",
    "29": "Residence",
    "30": "Medical care",
    "37": "Penal",
    "38": "Penal",
    "39": "Penal",
    "48": "Medical care",
    "49": "Medical care",
    "50": "Medical care",
    "51": "Medical care",
    "52": "Medical care",
    "53": "Medical care",
    "54": "Care Home",
    "65": "Care Home",
    "66": "Residence",
    "79": "Died",
    "84": "Medical care",
    "85": "Care Home",
    "87": "Medical care",
    "88": "Care Home",
    "98": "Unknown",
    "99": "Unknown",
}

dismeth = {
    "1": "Discharged",
    "2": "Discharged",
    "3": "Discharged",
    "4": "Died",
    "5": "Died",
    "8": "Not Applicable",
    "9": "Unknown",
}


@lru_cache(maxsize=1)
def load_apc_acsc_mapping() -> Dict[str, str]:
    """Download ICD10 to Ambulatory Care Sensitive Conditions mapping from Sheffield Google Docs
    and return a dictionary of icd10_code:acsc_name
    """

    # TODO: Store this file locally and hit Google Docs only if there is no local file.

    sheet_id = "1M3uS6qh3d9OY31gFxy8858ZxBiFjGE_Y"  # APC - ACSC V1 20230130
    sheet_name = "Sheet1"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    acsc = pd.read_csv(url, usecols=[0, 1])
    acsc.columns = acsc.columns.str.lower().str.replace("[^a-z0-9]+", "_", regex=True)
    acsc.icd10_code = acsc.icd10_code.str.replace(".", "", regex=False)
    acsc_mapping = acsc.set_index("icd10_code").aec_clinical_conditions.to_dict()

    return acsc_mapping


@lru_cache(maxsize=1)
def load_ed_acsc_mapping() -> Dict[str, str]:
    """Download SNOMED codes to Ambulatory Care Sensitive Conditions mapping from Sheffield Google Docs
    and return a dictionary of snomed_code:acsc_name
    """

    # TODO: Store this file locally and hit Google Docs only if there is no local file.

    sheet_id = "1Jsx4Am9a3Hvv7VJwIFb4z4_oV7zXL39e"  # ECDS - ACSC V5 20230130
    sheet_name = "ACSC ECDS and ICD-10"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = url.replace(" ", "%20")
    acsc = pd.read_csv(url, usecols=[0, 11])
    acsc.columns = acsc.columns.str.strip()
    acsc.columns = acsc.columns.str.lower().str.replace("[^a-z0-9]+", "_", regex=True)
    acsc_mapping = acsc.set_index("snomed_code").aec_clinical_conditions.to_dict()

    return acsc_mapping
