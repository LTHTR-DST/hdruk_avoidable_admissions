"""Utility function to download Code:Description mapping from NHS Data Dictionary Website

Caution: This will rewrite data/nhsdd.py if called from this directory.

```
cd avoidable_admissions/utils
python nhsdd_generator.py
```

Check git diff to ensure everything looks good. The script will also print to stdout.
"""
import json
import os
import re
import sys

import black
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv

from avoidable_admissions.data.validate import EmergencyCareEpisodeSchema
from avoidable_admissions.utils.FHIRTerminologyUtilites import FHIRTermClient


def generate_nhsdd():

    urls = {
        "gender": "https://www.datadictionary.nhs.uk/data_elements/person_gender_code_current.html",
        "ethnos": "https://www.datadictionary.nhs.uk/data_elements/ethnic_category.html",
        "admisorc": "https://www.datadictionary.nhs.uk/data_elements/admission_source__hospital_provider_spell_.html",
        "admimeth": "https://www.datadictionary.nhs.uk/data_elements/admission_method_code__hospital_provider_spell_.html",
        "disdest": "https://www.datadictionary.nhs.uk/data_elements/discharge_destination_code__hospital_provider_spell_.html",
        "dismeth": "https://www.datadictionary.nhs.uk/data_elements/discharge_method_code__hospital_provider_spell_.html",
        "edattendcat": "https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_category.html",
        "eddepttype": "https://www.datadictionary.nhs.uk/data_elements/emergency_care_department_type.html",
    }

    out = {}
    for k, v in urls.items():
        x = pd.read_html(v, match="Code")
        x = pd.concat(x)
        x.Code = x.Code.astype(str)
        x.Description = x.Description.apply(
            lambda x: x.encode(encoding="ascii", errors="replace").decode()
        )
        x = x.set_index("Code").Description.to_dict()
        out[k] = {"url": v, "mapping": x}

    # todo: generate this in the loop above
    nhsdd_py = ""
    for k, v in out.items():
        line = f"{k} = {v}\n\n"
        # replace non-ascii characters
        line = line.encode(encoding="ascii", errors="replace").decode().replace("?", "")
        nhsdd_py += line

    # format using black
    nhsdd_py = black.format_file_contents(nhsdd_py, fast=True, mode=black.FileMode())
    with open("../data/nhsdd.py", "wt") as f:
        f.write(nhsdd_py)

    print("Successfully created black formatted nhsdd.py")

    print(nhsdd_py)


def generate_nhsdd_snomed():
    """
    Refset members based on 2019 edition of SNOMED-GB

    The Refset IDs (SNOMED code) were extracted from the following urls for each variable.
    These codes were used to query the [IHTSDO Snowstorm API](https://github.com/IHTSDO/snowstorm) at
    <https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN%2FSNOMEDCT-GB%2F2019-10-01/members>.
    The latest edition of SNOMED-GB is from 2019-10-01.


    - accommodationstatus: [ACCOMMODATION_STATUS](https://www.datadictionary.nhs.uk/data_elements/accommodation_status__snomed_ct_.html)
    - edarrivalmode: [EMERGENCY_CARE_ARRIVAL_MODE](https://www.datadictionary.nhs.uk/data_elements/emergency_care_arrival_mode__snomed_ct_.html)
    - edattendsource: [EMERGENCY_CARE_ATTENDANCE_SOURCE](https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_source__snomed_ct_.html)
    - edacuity: [EMERGENCY_CARE_ACUITY](https://www.datadictionary.nhs.uk/data_elements/emergency_care_acuity__snomed_ct_.html)
    - edchiefcomplaint: [EMERGENCY_CARE_CHIEF_COMPLAINT](https://www.datadictionary.nhs.uk/data_elements/emergency_care_chief_complaint__snomed_ct_.html)
    - edattenddispatch: [EMERGENCY_CARE_DISCHARGE_DESTINATION](https://www.datadictionary.nhs.uk/data_elements/emergency_care_discharge_destination__snomed_ct_.html)
    - edrefservice: [REFERRED_TO_SERVICE](https://www.datadictionary.nhs.uk/data_elements/referred_to_service__snomed_ct_.html)
    - edcomorb: [COMORBIDITY](https://www.datadictionary.nhs.uk/data_elements/comorbidity__snomed_ct_.html)
    - eddiagqual: [EMERGENCY_CARE_DIAGNOSIS_QUALIFIER](https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis_qualifier__snomed_ct_.html)
    - eddiag: [EMERGENCY_CARE_DIAGNOSIS](https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis__snomed_ct_.html)
    - edinvest: [EMERGENCY_CARE_CLINICAL_INVESTIGATION](https://www.datadictionary.nhs.uk/data_elements/emergency_care_clinical_investigation__snomed_ct_.html)
    - edtreat: [EMERGENCY_CARE_PROCEDURE](https://www.datadictionary.nhs.uk/data_elements/emergency_care_procedure__snomed_ct_.html)

    **Replace this method with one that uses the most recent edition of SNOMED-UK**

    """

    try:
        load_dotenv(find_dotenv())
    except:
        load_dotenv("../../.env")

    try:
        client_id = os.environ["ONTOLOGY_SERVER_CLIENT_ID"]
        client_secret = os.environ["ONTOLOGY_SERVER_CLIENT_SECRET"]
        token_url = os.environ["ONTOLOGY_SERVER_TOKEN_URL"]
    except Exception as exc:
        raise KeyError(
            "Environment variables not set for Ontology Server credentials.", *exc.args
        )

    try:
        fhir_url = "https://ontology.nhs.uk/staging/fhir"
        fhirclient = FHIRTermClient(
            fhir_url=fhir_url,
            client_id=client_id,
            client_secret=client_secret,
            cache_backend="memory",
            token_url=token_url,
        )
    except Exception as exc:
        raise ConnectionError("Error creating FHIR Terminology Client", *exc.args)

    # Get URLs to NHS Data Dictionary definitions from the Schema
    ecds = EmergencyCareEpisodeSchema
    urls = {}
    for k, v in ecds.columns.items():
        if v.description:
            if "snomed" in v.description and "https:" in v.description:
                urls[k.split("_")[0]] = v.description

    # Get SNOMED Codes and member codes
    refset_members = {}
    for k, v in urls.items():

        print("Getting SNOMED Refset ID for ", k)
        r = requests.get(v)
        soup = BeautifulSoup(r.text, features="lxml")
        a = soup.find(name="a", href=re.compile("https://termbrowser\.nhs\.uk/"))

        try:
            refset_id = int(a.attrs["href"].split("=")[-1])
        except:
            print("ID Extraction error", k, v)
            continue

        print(k, "has SNOMED Code", refset_id, ". Getting Member Ids")

        # Use @dfleming9 client to get refset members
        members = fhirclient.expand_valueset_to_list(
            f"http://snomed.info/sct?fhir_vs=refset/{refset_id}",
        )
        members = sorted(int(i) for i in members)

        print("Got", len(members), "members")
        refset_members[k] = {"refset_id": refset_id, "members": members}

    # Convert dict object into a python module
    text = ""
    for k, v in refset_members.items():
        line = f"{k.split('_')[0]} = {json.dumps(v)}\n\n"
        text += line

    text = black.format_file_contents(text, fast=True, mode=black.FileMode())

    with open("../data/nhsdd_snomed.py", "wt") as f:
        f.write(text)

    print("Successfully created black formatted nhsdd_snomed.py")


if __name__ == "__main__":

    if sys.argv[1] == "dd":
        print("Generating avoidable_admissions/data/nhsdd.py")
        generate_nhsdd()
    elif sys.argv[1] == "snomed":
        print("Generating avoidable_admissions/data/nhsdd_snomed.py")
        generate_nhsdd_snomed()
    else:
        print(
            "Generating avoidable_admissions/data/nhsdd.py and avoidable_admissions/data/nhsdd_snomed.py"
        )
        generate_nhsdd()
        generate_nhsdd_snomed()
