"""Utility function to download Code:Description mapping from NHS Data Dictionary Website

Caution: This will rewrite data/nhsdd.py if called from this directory.

```{code-block} python
cd avoidable_admissions/utils
python nhsdd_generator.py
```
Check git diff to ensure everything looks good. The script will also print to stdout.
"""
import black
import pandas as pd

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


def main():
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
    print(nhsdd_py)


if __name__ == "__main__":
    main()
