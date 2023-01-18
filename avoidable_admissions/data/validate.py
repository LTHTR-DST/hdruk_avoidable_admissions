from datetime import date, datetime, time
from typing import Tuple

import pandas as pd
import pandera as pa
from pandera.typing import Series

from avoidable_admissions.data import nhsdd


class AdmittedCareEpisodeSchema(pa.SchemaModel):
    visit_id: Series[int] = pa.Field(nullable=False)
    patient_id: Series[int] = pa.Field(nullable=False)

    gender: Series[int] = pa.Field(
        description=nhsdd.gender["url"],
        isin=list(nhsdd.gender["mapping"].keys()),
        nullable=False,
    )

    ethnos: Series[str] = pa.Field(
        description=nhsdd.ethnos["url"],
        isin=list(nhsdd.ethnos["mapping"].keys()),
        nullable=False,
    )

    procodet: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/organisation_code__code_of_provider_.html",
        nullable=False,
    )

    sitetret: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/site_code__of_treatment_.html",
        nullable=False,
    )

    townsend_score_decile: Series[int] = pa.Field(
        description="https://statistics.ukdataservice.ac.uk/dataset/2011-uk-townsend-deprivation-scores",
        ge=1,
        le=10,
        nullable=True,
    )

    admimeth: Series[str] = pa.Field(
        description=nhsdd.admimeth["url"],
        isin=list(nhsdd.admimeth["mapping"].keys()),
        nullable=True,
    )

    admisorc: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/admission_source__hospital_provider_spell_.html",
        isin=list(nhsdd.admisorc["mapping"].keys()),
        nullable=True,
    )

    admidate: Series[date] = pa.Field(
        ge=date(year=2021, month=10, day=1),
        le=date(year=2022, month=9, day=30),
        nullable=False,
    )

    admitime: Series[str] = pa.Field(
        str_matches="2[0-3]|[01]?[0-9]:[0-5][0-9]", nullable=True, coerce=True
    )

    disdest: Series[str] = pa.Field(
        description=nhsdd.disdest["url"],
        isin=list(nhsdd.disdest["mapping"].keys()),
        nullable=True,
    )

    dismeth: Series[str] = pa.Field(
        description=nhsdd.dismeth["url"],
        isin=list(nhsdd.dismeth["mapping"].keys()),
        nullable=True,
    )

    length_of_stay: Series[float] = pa.Field(nullable=True)

    epiorder: Series[int] = pa.Field(nullable=True)

    admiage: Series[float] = pa.Field(
        ge=0,
        le=130,
        nullable=True,
    )

    class Config:
        coerce = True


AdmittedCareEpisodeSchema = AdmittedCareEpisodeSchema.to_schema().add_columns(
    {
        "diag_[0-9]{2}": pa.Column(
            str,
            nullable=True,
            regex=True,
        ),
        "opertn_[0-9]{2}": pa.Column(
            str,
            nullable=True,
            regex=True,
        ),
        "opdate_[0-9]{2}": pa.Column(
            datetime,
            nullable=True,
            regex=True,
        ),
    }
)


class EmergencyCareEpisodeSchema(pa.SchemaModel):

    visit_id: Series[int] = pa.Field(nullable=False)

    patient_id: Series[int] = pa.Field(nullable=False)

    gender: Series[int] = pa.Field(
        description=nhsdd.gender["url"],
        isin=list(nhsdd.gender["mapping"].keys()),
        nullable=False,
    )

    ethnos: Series[str] = pa.Field(
        description=nhsdd.ethnos["url"],
        isin=list(nhsdd.ethnos["mapping"].keys()),
        nullable=False,
    )

    townsend_score_decile: Series[int] = pa.Field(
        description="https://statistics.ukdataservice.ac.uk/dataset/2011-uk-townsend-deprivation-scores",
        ge=1,
        le=10,
        nullable=True,
    )

    accommodationstatus_snomedct: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/accommodation_status__snomed_ct_.html",
        nullable=True,
    )

    procodet: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/organisation_code__code_of_provider_.html",
        nullable=False,
    )

    edsitecode: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/organisation_site_identifier__of_treatment_.html",
        nullable=False,
    )

    eddepttype: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_department_type.html",
        isin=list(nhsdd.eddepttype["mapping"].keys()),
        nullable=False,
    )

    edarrivalmode: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_arrival_mode__snomed_ct_.html",
        nullable=False,
    )

    edattendcat: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_category.html",
        isin=list(nhsdd.edattendcat["mapping"].keys()),
        nullable=True,
    )
    edattendsource: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_source__snomed_ct_.html",
        nullable=True,
    )
    edarrivaldatetime: Series[datetime] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_arrival_date.html",
        nullable=True,
    )
    activage: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/age_at_cds_activity_date.html",
        nullable=True,
    )
    edacuity: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_acuity__snomed_ct_.html",
        nullable=True,
    )
    edcheifcomplaint: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_chief_complaint__snomed_ct_.html",
        nullable=True,
    )

    timeined: Series[str] = pa.Field(
        description="Derived from Departure Date and Departure Time",
        nullable=True,
    )
    edattenddispatch: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_discharge_destination__snomed_ct_.html",
        nullable=True,
    )
    edrefservice: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/referred_to_service__snomed_ct_.html",
        nullable=True,
    )

    class Config:
        coerce = True


EmergencyCareEpisodeSchema = EmergencyCareEpisodeSchema.to_schema().add_columns(
    {
        "edcomorb_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/comorbidity__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "eddiag_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "edentryseq_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/coded_clinical_entry_sequence_number.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "eddiag_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis_qualifier__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "edinvest_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_clinical_investigation__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "edtreat_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_procedure__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
        "eddiag_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis_qualifier__snomed_ct_.html",
            dtype=int,
            nullable=True,
            regex=True,
        ),
    }
)


def _validate_dataframe(
    df: pd.DataFrame, schema: pa.SchemaModel
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_errors = pd.DataFrame()
    try:
        # Capture all errors
        # https://pandera.readthedocs.io/en/stable/lazy_validation.html
        schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as ex:
        df_errors = df.merge(
            ex.failure_cases, how="right", left_index=True, right_on="index"
        )
        df = df[~df.index.isin(ex.failure_cases["index"])]
        print(ex.args[0])
    finally:
        return df, df_errors


def validate_admitted_care_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return _validate_dataframe(df, AdmittedCareEpisodeSchema)


def validate_emergency_care_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return _validate_dataframe(df, EmergencyCareEpisodeSchema)
