import warnings
from contextlib import nullcontext
from datetime import date, datetime
from typing import Tuple

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series

from avoidable_admissions.data import nhsdd
from avoidable_admissions.features import feature_maps


class AdmittedCareEpisodeSchema(pa.SchemaModel):
    """Rules for validating the Admitted Care Episodes Data _before_ feature engineering.
    The dataset should be validated successfully against this schema before feature engineering.
    """

    # visit_id is not part of the data spec but is used here as a unique row identifier
    # Use `df["visit_id"] = df.reset_index(drop=True).index`

    visit_id: Series[np.int64] = pa.Field(nullable=False, unique=True)

    # Ensure this has been pseudonymised appropriately.
    patient_id: Series[np.int64] = pa.Field(nullable=False)

    gender: Series[str] = pa.Field(
        description=nhsdd.gender["url"],
        isin=list(feature_maps.gender),
        nullable=False,
    )

    ethnos: Series[str] = pa.Field(
        description=nhsdd.ethnos["url"],
        isin=list(feature_maps.ethnos),
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
        ge=0,  # fill missing values with 0 to pass validation.
        le=10,
        nullable=False,
    )

    admimeth: Series[str] = pa.Field(
        description=nhsdd.admimeth["url"],
        isin=list(nhsdd.admimeth["mapping"].keys()),
        nullable=True,
    )

    admisorc: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/admission_source__hospital_provider_spell_.html",
        isin=list(feature_maps.admisorc),
        nullable=True,
    )

    admidate: Series[date] = pa.Field(
        ge=date(year=2021, month=10, day=1),
        le=date(year=2022, month=9, day=30),
        nullable=False,
    )

    admitime: Series[str] = pa.Field(
        nullable=True, str_matches="2[0-3]|[01]?[0-9]:[0-5][0-9]", coerce=True
    )

    disdest: Series[str] = pa.Field(
        description=nhsdd.disdest["url"],
        isin=list(feature_maps.disdest),
        nullable=True,
    )

    dismeth: Series[str] = pa.Field(
        description=nhsdd.dismeth["url"],
        isin=list(feature_maps.dismeth),
        nullable=True,
    )

    length_of_stay: Series[float] = pa.Field(nullable=True, ge=0)

    epiorder: Series[int] = pa.Field(nullable=True, ge=0)

    admiage: Series[int] = pa.Field(
        ge=18,
        le=130,
        nullable=False,
    )

    # Include regex columns here to ensure at least the first one exists

    diag_01: Series[str] = pa.Field(nullable=True)
    opertn_01: Series[str] = pa.Field(nullable=True)
    opdate_01: Series[datetime] = pa.Field(nullable=True)

    class Config:
        coerce = False


AdmittedCareEpisodeSchema: pa.DataFrameSchema = (
    AdmittedCareEpisodeSchema.to_schema().add_columns(
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
)

# This picks up extra columns that should not be in the dataframe
AdmittedCareEpisodeSchema.strict = True

# Schema for validating Admitted Care Data Set after feature engineering
AdmittedCareFeatureSchema: pa.DataFrameSchema = AdmittedCareEpisodeSchema.add_columns(
    {
        "admiage_cat": pa.Column(
            str, nullable=False, checks=[pa.Check.isin(feature_maps.age_labels)]
        ),
        "gender_cat": pa.Column(
            str,
            nullable=False,
            checks=[pa.Check.isin(set(feature_maps.gender.values()))],
        ),
        "ethnos_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.ethnos.values()))],
        ),
        "townsend_score_quintile": pa.Column(
            int, nullable=True, checks=[pa.Check.in_range(min_value=1, max_value=5)]
        ),
        "admisorc_cat": pa.Column(
            nullable=True, checks=[pa.Check.isin(set(feature_maps.admisorc.values()))]
        ),
        "admidayofweek": pa.Column(
            nullable=True,
            checks=[
                pa.Check.isin(
                    [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ]
                )
            ],
        ),
        "diag_seasonal_cat": pa.Column(
            nullable=True,
            checks=[
                pa.Check.isin(
                    ["Respiratory infection", "Chronic disease exacerbation", "-"]
                )
            ],
        ),
        "length_of_stay_cat": pa.Column(
            nullable=True, checks=[pa.Check.isin(["<2 days", ">=2 days"])]
        ),
        "disdest_cat": pa.Column(
            nullable=True, checks=[pa.Check.isin(set(feature_maps.disdest.values()))]
        ),
        "dismeth_cat": pa.Column(
            nullable=True, checks=[pa.Check.isin(set(feature_maps.dismeth.values()))]
        ),
        "diag_01_acsc": pa.Column(
            # nullable=True,
            checks=[
                pa.Check.isin(
                    set([*feature_maps.load_apc_acsc_mapping().values(), "-"]),
                    ignore_na=True,
                )
            ],
        ),
        "opertn_count": pa.Column(int, nullable=False, checks=[pa.Check.ge(0)]),
    }
)

AdmittedCareFeatureSchema.strict = True

AdmittedCareFeatureSchema.__dict__[
    "_description"
] = """Rules for validating the Admitted Care Features Data _after_ feature engineering.
This dataset should have all the information from the raw data set as well as additional generated features.
The dataset should be validated successfully against this schema before analysis and modelling.
    """


class EmergencyCareEpisodeSchema(pa.SchemaModel):

    visit_id: Series[np.int64] = pa.Field(nullable=False)

    patient_id: Series[np.int64] = pa.Field(nullable=False)

    gender: Series[str] = pa.Field(
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
        ge=0,  # fill missing values with 0 to pass validation.
        le=10,
        nullable=True,
    )

    accommodationstatus: Series[np.int64] = pa.Field(
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

    edarrivalmode: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_arrival_mode__snomed_ct_.html",
        nullable=False,
    )

    edattendcat: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_category.html",
        isin=list(nhsdd.edattendcat["mapping"].keys()),
        nullable=True,
    )
    edattendsource: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_attendance_source__snomed_ct_.html",
        nullable=True,
    )
    edarrivaldatetime: Series[datetime] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_arrival_date.html",
        ge=datetime(year=2021, month=10, day=1),
        le=datetime(year=2022, month=9, day=30),
        nullable=True,
        coerce=True,
    )
    activage: Series[int] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/age_at_cds_activity_date.html",
        ge=18,
        le=130,
        nullable=True,
    )
    edacuity: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_acuity__snomed_ct_.html",
        nullable=True,
    )
    edchiefcomplaint: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_chief_complaint__snomed_ct_.html",
        nullable=True,
    )

    timeined: Series[int] = pa.Field(
        description="Derived from Departure Date and Departure Time",
        nullable=True,
    )
    edattenddispatch: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_discharge_destination__snomed_ct_.html",
        nullable=True,
    )
    edrefservice: Series[np.int64] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/referred_to_service__snomed_ct_.html",
        nullable=True,
    )

    edcomorb_01: Series[np.int64] = pa.Field(nullable=True)
    eddiag_01: Series[np.int64] = pa.Field(nullable=True)
    edentryseq_01: Series[int] = pa.Field(nullable=True)
    eddiagqual_01: Series[np.int64] = pa.Field(nullable=True)
    edinvest_01: Series[np.int64] = pa.Field(nullable=True)
    edtreat_01: Series[np.int64] = pa.Field(nullable=True)

    class Config:
        coerce = False


EmergencyCareEpisodeSchema: pa.DataFrameSchema = EmergencyCareEpisodeSchema.to_schema().add_columns(
    {
        "edcomorb_[0-9]{2}$": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/comorbidity__snomed_ct_.html",
            dtype=np.int64,
            nullable=True,
            regex=True,
            coerce=True,
        ),
        "eddiag_[0-9]{2}$": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis__snomed_ct_.html",
            dtype=np.int64,
            nullable=True,
            regex=True,
            coerce=True,
        ),
        "edentryseq_[0-9]{2}$": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/coded_clinical_entry_sequence_number.html",
            dtype=int,
            nullable=True,
            regex=True,
            coerce=True,
        ),
        "eddiagqual_[0-9]{2}$": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_diagnosis_qualifier__snomed_ct_.html",
            dtype=np.int64,
            nullable=True,
            regex=True,
            coerce=True,
        ),
        "edinvest_[0-9]{2}$": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_clinical_investigation__snomed_ct_.html",
            dtype=np.int64,
            nullable=True,
            regex=True,
            coerce=True,
        ),
        "edtreat_[0-9]{2}": pa.Column(
            description="https://www.datadictionary.nhs.uk/data_elements/emergency_care_procedure__snomed_ct_.html",
            dtype=np.int64,
            nullable=True,
            regex=True,
            coerce=True,
        ),
    }
)

# Picks up columns not in schema
EmergencyCareEpisodeSchema.strict = True

# Schema for validating Emergency Care Data Set after feature engineering
EmergencyCareFeatureSchema: pa.DataFrameSchema = EmergencyCareEpisodeSchema.add_columns(
    {
        "activage_cat": pa.Column(
            str, nullable=False, checks=[pa.Check.isin(feature_maps.age_labels)]
        ),
        "gender_cat": pa.Column(
            str,
            nullable=False,
            checks=[pa.Check.isin(set(feature_maps.gender.values()))],
        ),
        "ethnos_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.ethnos.values()))],
        ),
        "townsend_score_quintile": pa.Column(
            int, nullable=True, checks=[pa.Check.in_range(min_value=1, max_value=5)]
        ),
        "accommodationstatus_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.accomodationstatus.values()))],
        ),
        "edarrivalmode_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edarrivalmode.values()))],
        ),
        "edattendsource_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edattendsource.values()))],
        ),
        "edacuity_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edacuity.values()))],
        ),
        # Ensures at least _01 is present
        "edinvest_01_cat": pa.Column(str, nullable=True),
        "edtreat_01_cat": pa.Column(str, nullable=True),
        "edinvest_[0-9]{2}_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edinvest.values()))],
            regex=True,
        ),
        "edtreat_[0-9]{2}_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edtreat.values()))],
            regex=True,
        ),
        "eddiag_seasonal_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.eddiag_seasonal.values()))],
        ),
        "eddiagqual_01_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.eddiagqual.values()))],
        ),
        "edattenddispatch_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edattenddispatch.values()))],
        ),
        "edrefservice_cat": pa.Column(
            str,
            nullable=True,
            checks=[pa.Check.isin(set(feature_maps.edrefservice.values()))],
        ),
    }
)

# Picks up columns not in schema
EmergencyCareFeatureSchema.strict = True


def validate_dataframe(
    df: pd.DataFrame, schema: pa.DataFrameSchema
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Validates data against a specified schema.

    The data should have been prepared as per the specification set by the lead site.
    Use the output of this function to iteratively identify and address data quality issues.

    The following schema are defined:

    Admitted Care Data:

    - `AdmittedCareEpisodeSchema`
    - `AdmittedCareFeatureSchema`

    Emergency Care Data:

    - `EmergencyCareEpisodeSchema`
    - `EmergencyCareFeatureSchema`

    See __[source code](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/blob/dev/avoidable_admissions/data/validate.py)__
    for validation rules.

    Returns a _good_ dataframe containing rows that passed validation and
    a _bad_ dataframe with rows that failed validation.
    The _bad_ dataframe has additional columns that provide information on failure cause(s).
    If there is a column error (misspelt, missing or additional), all rows will be returned in _bad_ dataframe.

    Args:
        df (pandas.DataFrame): Dataframe to be validated
        schema (pa.DataFrameSchema): Pandera schema to validate against

    Returns:
        _Good_ and _Bad_ dataframes. See example below.



    ## Validation Example:

    ``` python
    from avoidable_admissions.data.validate import (
        validate_dataframe,
        AdmittedCareEpisodeSchema
    )


    df = pd.read_csv('path/to/data.csv')
    good, bad = validate_dataframe(df, AdmittedCareEpisodeSchema)

    ```

    If `df` had rows that fail validation, the function will print an output similar to below.

        Schema AdmittedCareEpisodeSchema: A total of 1 schema errors were found.

        Error Counts
        ------------
        - schema_component_check: 1

        Schema Error Summary
        --------------------
                                                            failure_cases  n_failure_cases
        schema_context column  check
        Column         admiage greater_than_or_equal_to(18)        [17.0]                1

    This message indicates that there was a validation error in the `admiage` column which expects values >=18.

    Fix data quality iteratively to ensure there are no errors.

    If you find a bug in the validation code, and correct data fails validation, please raise a
    [GitHub issue](https://github.com/LTHTR-DST/hdruk_avoidable_admissions/issues).

    """

    df_errors = pd.DataFrame()

    # todo: document this behaviour to warn user that index will be dropped.
    # alternatively find a way to set a unique key for each row - important for merging errors
    df = df.copy().reset_index(drop=True)

    try:
        # Capture all errors
        # https://pandera.readthedocs.io/en/stable/lazy_validation.html
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as ex:

        print(ex.args[0])

        df_errors = ex.failure_cases.copy()

        # First get the rows that are causing errors
        df_errors["index"] = df_errors["index"].fillna(df.index.max() + 1)
        df_errors = df.merge(df_errors, how="right", left_index=True, right_on="index")
        df_errors["index"] = df_errors["index"].replace(df.index.max() + 1, None)

        # Column name mismatches will have an 'index' of NaN which causes merge to fail
        # If a column name is not present, then all rows should be returned as errors

        if df_errors["index"].hasnans:  # this
            # there is a column error. drop all rows from the 'good' dataframe
            df = df.iloc[0:0]

            print("No data will pass validation due to column error. See output above.")

        else:
            df = df[~df.index.isin(df_errors["index"])]
    except Exception as ex:
        # This is to catch all other errors.
        print(ex.args[0])
        print(
            "No data will pass validation due to undefined error."
            "See output above and please raise an issue on GitHub."
        )

        df = df.iloc[0:0]
        df_errors = df.copy()

    finally:
        return df, df_errors


def validate_admitted_care_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convenience wrapper for `validate_dataframe(df, AdmittedCareEpisodeSchema)`

    See [avoidable_admissions.data.validate.validate_dataframe][] for usage.
    """

    return validate_dataframe(df, AdmittedCareEpisodeSchema)


def validate_emergency_care_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convenience wrapper for `validate_dataframe(df, EmergencyCareEpisodeSchema)`

    See [avoidable_admissions.data.validate.validate_dataframe][] for usage.
    """
    return validate_dataframe(df, EmergencyCareEpisodeSchema)


def validate_admitted_care_features(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convenience wrapper for `validate_dataframe(df, AdmittedCareFeatureSchema)`

    See [avoidable_admissions.data.validate.validate_dataframe][] for usage.
    """
    return validate_dataframe(df, AdmittedCareFeatureSchema)


def validate_emergency_care_features(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convenience wrapper for `validate_dataframe(df, EmergencyCareFeatureSchema)`

    See [avoidable_admissions.data.validate.validate_dataframe][] for usage.
    """
    return validate_dataframe(df, EmergencyCareFeatureSchema)


def get_schema_properties(schema: pa.DataFrameSchema) -> pd.DataFrame:
    """Get detailed information about a validation schema including checks, dtypes, nullability and more.

    Args:
        schema (Pandera DataFrameSchema): One of `AdmittedCareEpisodeSchema`, `AdmittedCareFeatureSchema`,
        `EmergencyCareEpisodeSchema`, `EmergencyCareFeatureSchema`

    Returns:
        pd.DataFrame: Dataframe containing schema properties.
    """

    df = pd.DataFrame([x.properties for x in schema.columns.values()])

    columns = [
        "name",
        "dtype",
        "nullable",
        "unique",
        "coerce",
        "required",
        "checks",
        "regex",
        "title",
        "description",
    ]

    return df[columns]
