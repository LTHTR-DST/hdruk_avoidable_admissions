"""
We need to use the ECDS module to map the terms.

See below pseudocode example:

Examples:
    >>> from avoidable_admissions import Mapper
    >>> avoidable_admissions.Mapper(icd10, snomed)
        ("C124024" , 1349813271)

"""

import pandas as pd
df = pd.read_csv('mapper_file.csv')
mapper = df['ICD10', 'SNOMED'].to_dict()

def Mapper(icd10, snomed) -> str:
    """
    Takes the ICD10 codes and converts them to SNOMED-CT

    """
    snomed_mapping = icd10.map(mapper)
    return snomed_mapping
