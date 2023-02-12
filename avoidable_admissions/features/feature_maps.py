from functools import lru_cache
from typing import Dict

import numpy as np
import pandas as pd

from avoidable_admissions.data import nhsdd_snomed

# to prevent accidentally removing nhsdd_snomed import which is used in eval
_ = nhsdd_snomed.__doc__

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


def generate_map(name: str, feature_r: dict) -> dict:

    # First generate a reverse map as snomed_code:category

    feature = {
        snomed_code: category
        for category, snomed_list in feature_r.items()
        for snomed_code in snomed_list
    }

    # Get the members of the refset from nhsdd_snomed
    # This file has been automatically generated from the Ontology Server
    refset_members = eval(f"nhsdd_snomed.{name}['members']")

    # Create a set of all snomed codes in feature
    feature_members = feature.keys()

    # Unmapped codes are the codes in the refset that are not in feature
    # For each code in refset that is not in feature, set to 'unmapped'

    for i in refset_members:
        if i not in feature_members:
            feature[i] = "ERROR:Unmapped - In Refset"

    # For codes that appear in the mapping but not in the refset
    # append '|Not-In-Refset' tp existing value

    for k, v in feature.items():
        if k not in refset_members:
            feature[k] = "ERROR:Not In Refset|" + v

    feature[0] = "ERROR:Missing Data"

    # Add in a placeholder for codes that are neither in the featuremap nor in refset
    # These are for unforeseen values that may appear in the source data

    feature[1] = "ERROR:Unmapped - Not In Refset"

    return feature


##############################################################################
# accommodationstatus
##############################################################################
accommodationstatus_r = {
    "Unknown": [1064831000000106, 1064841000000102, 1066881000000100],
    "Yes": [160734000],
    "No": [224221006, 224225002, 224231004, 32911000, 394923006, 414418009],
}

accommodationstatus = generate_map("accommodationstatus", accommodationstatus_r)

##############################################################################
# edarrivalmode
##############################################################################
edarrivalmode_r = {
    "Walk-In": [1048061000000105, 1048071000000103],
}

edarrivalmode = generate_map("edarrivalmode", edarrivalmode_r)

##############################################################################
# edattendsource
##############################################################################
edattendsource_r = {
    "Community": [
        1052681000000105,
        1065401000000101,
        1065991000000100,
        1066001000000101,
        1066011000000104,
        1077191000000103,
        1077201000000101,
        1077211000000104,
        1077761000000105,
        185363009,
        185366001,
        185368000,
        185369008,
        877171000000103,
    ],
    "Personal": [1065391000000104, 315261000000101, 507291000000100],
    "Emergency Services": [
        1066021000000105,
        1066031000000107,
        1066041000000103,
        1066051000000100,
        1066061000000102,
        198261000000104,
        889801000000100,
    ],
    "Hospital": [
        1066431000000102,
        1066441000000106,
        1079521000000104,
        835091000000109,
        835101000000101,
    ],
    "Primary Care": [1082331000000106, 166941000000106, 276491000, 879591000000102],
    "Private Referral": [183877003],
}

edattendsource = generate_map("edattendsource", edattendsource_r)

##############################################################################
# edacuity
##############################################################################
edacuity = {
    0: "ERROR:Missing Data",
    1064891000000107: "1 - Immediate care level emergency care",
    1064901000000108: "3 - Urgent level emergency care",
    1064911000000105: "2 - Very urgent level emergency care",
    1077241000000103: "4 - Standard level emergency care",
    1077251000000100: "5 - Low acuity level emergency care",
}

##############################################################################
# edinvest
##############################################################################

edinvest_r = {
    "Non-urgent": [167252002, 27171005, 53115007, 67900009],
    "Urgent": [
        104686004,
        105000003,
        113091000,
        16254007,
        16310003,
        164729009,
        165320004,
        167036008,
        16830007,
        168338000,
        168537006,
        179929004,
        252167001,
        252316009,
        252375001,
        26604007,
        26958001,
        269874008,
        270982000,
        271232007,
        282096008,
        29303009,
        29893006,
        30088009,
        3116009,
        35650009,
        363255004,
        392010000,
        397798009,
        401294003,
        40701008,
        416838001,
        43396009,
        55235003,
        56027003,
        60170009,
        61911006,
        62847008,
        68793005,
        70648006,
        74500006,
        77477000,
        86944008,
        89659001,
    ],
    "No-investigation": [1088291000000101],
}

edinvest = generate_map("edinvest", edinvest_r)

##############################################################################
# edtreat
##############################################################################
edtreat_r = {
    "Non-urgent": [
        183964008,
        266712008,
        413334001,
        81733005,
    ]
}

edtreat = generate_map("edtreat", edtreat_r)

##############################################################################
# eddiag_seasonal
##############################################################################
eddiag_seasonal_r = {
    "Chronic disease exacerbation": [12295008, 13645005, 195951007, 195967001],
    "Respiratory infection": [
        1325161000000102,
        1325171000000109,
        1325181000000106,
        205237003,
        233604007,
        278516003,
        36971009,
        50417007,
        54150009,
        6142004,
        62994001,
        80384002,
        90176007,
    ],
}

eddiag_seasonal = generate_map("eddiag", eddiag_seasonal_r)

##############################################################################
# eddiagqual
##############################################################################
eddiagqual = {
    415684004: "Suspected",
    410605003: "Confirmed",
}

##############################################################################
# edattenddispatch
##############################################################################
edattenddispatch_r = {
    "Ambulatory / Short Stay": [1066331000000109, 1066341000000100, 1066351000000102],
    "Admitted": [
        1066361000000104,
        1066371000000106,
        1066381000000108,
        1066391000000105,
        1066401000000108,
        306706006,
    ],
    "Transfer": [183919006, 19712007],
    "Died": [305398007],
    "Discharged": [306689006, 306691003, 306694006, 306705005, 50861005],
}

edattenddispatch = generate_map("edattenddispatch", edattenddispatch_r)

##############################################################################
# edrefservice
##############################################################################
edrefservice_r = {
    "Medical": [
        1064851000000104,
        183516009,
        183518005,
        183519002,
        183521007,
        183522000,
        183523005,
        306111000,
        306114008,
        306118006,
        306123006,
        306124000,
        306125004,
        306127007,
        306140002,
        306148009,
        306237005,
        306285006,
        306802002,
        307374004,
        898791000000105,
    ],
    "Psychiatric": [
        183524004,
        202291000000107,
        306136006,
        306138007,
        380241000000107,
        413127007,
    ],
    "Surgical": [
        183542009,
        183543004,
        183544005,
        183545006,
        183546007,
        306182003,
        306184002,
        306198005,
        306200004,
        306201000,
        306934005,
        327121000000104,
        384711009,
        384712002,
    ],
    "ObGyn": [183548008, 183549000],
    "Local Medical": [183561008, 276490004, 306152009, 770411000000102],
    "Community / OPD": [
        247541000000106,
        306129005,
        307375003,
        307376002,
        307380007,
        353961000000104,
        38670004,
        415263003,
        4266003,
        516511000000107,
        61801003,
        78429003,
        785621000000108,
        785681000000109,
        785701000000106,
        785721000000102,
        785761000000105,
        785781000000101,
        811391000000104,
        818861000000107,
        823961000000102,
        894171000000100,
    ],
    "Critical Care": [306107006, 382271000000102, 770677000, 975951000000109],
}

edrefservice = generate_map("edrefservice", edrefservice_r)

##############################################################################
# disstatus
##############################################################################
disstatus_r = {
    "Non-urgent": [
        1066301000000103,
        1066311000000101,
        1066321000000107,
        1077021000000100,
        182992009,
    ],
    "Urgent": [
        1077031000000103,
        1077041000000107,
        1077051000000105,
        1077061000000108,
        1077071000000101,
        1077081000000104,
        1077091000000102,
        1077101000000105,
        1077781000000101,
        1324201000000109,
    ],
    "Died": [63238001, 75004002],
}

disstatus = generate_map("disstatus", disstatus_r)


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

    # Set ERROR codes to allow validation to pass after feature engineering
    # TODO: Tidy this up

    # Get the members of the refset from nhsdd_snomed
    # This file has been automatically generated from the Ontology Server
    refset_members = nhsdd_snomed.eddiag["members"]

    # Create a set of all snomed codes in feature
    feature_members = acsc_mapping.keys()

    # Unmapped codes are the codes in the refset that are not in feature
    # For each code in refset that is not in feature, set to 'unmapped'

    for i in refset_members:
        if i not in feature_members:
            acsc_mapping[i] = "ERROR:Unmapped - In Refset"

    # For codes that appear in the mapping but not in the refset
    # append '|Not-In-Refset' tp existing value

    for k, v in acsc_mapping.items():
        if k not in refset_members:
            acsc_mapping[k] = "ERROR:Mapped - Not In Refset|" + v

    acsc_mapping[0] = "ERROR:Missing Data"

    # Add in a placeholder for codes that are neither in the featuremap nor in refset
    # These are for unforeseen values that may appear in the source data

    acsc_mapping[1] = "ERROR:Unmapped - Not In Refset"

    return acsc_mapping
