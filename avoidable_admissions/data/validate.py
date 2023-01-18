from datetime import date, datetime, time

import pandas as pd
import pandera as pa
from pandera.typing import Series

from avoidable_admissions.data import nhsdd


class AdmittedCareEpisodeSchema(pa.SchemaModel):
    visit_id: Series[int] = pa.Field(nullable=True)
    patient_id: Series[int] = pa.Field(nullable=True)

    gender: Series[int] = pa.Field(
        description=nhsdd.gender["url"],
        isin=nhsdd.gender["mapping"].keys(),
        nullable=False,
        coerce=True,
    )

    ethnos: Series[str] = pa.Field(
        description=nhsdd.ethnos["url"],
        isin=nhsdd.ethnos["mapping"].keys(),
        nullable=False,
        coerce=True,
    )

    procodet: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/organisation_code__code_of_provider_.html",
        nullable=False,
        coerce=True,
    )

    sitetret: Series[str] = pa.Field(
        description="https://www.datadictionary.nhs.uk/data_elements/site_code__of_treatment_.html",
        nullable=False,
        coerce=True,
    )

    townsend_score_decile: Series[int] = pa.Field(
        description="https://statistics.ukdataservice.ac.uk/dataset/2011-uk-townsend-deprivation-scores",
        ge=1,
        le=10,
        nullable=True,
    )

    admimeth: Series[str] = pa.Field(
        description=nhsdd.admimeth["url"],
        isin=nhsdd.admimeth["mapping"].keys(),
        coerce=True,
        nullable=True,
    )

    admisorc: Series[str] = pa.Field(
        description=nhsdd.admisorc["url"],
        isin=nhsdd.admisorc["mapping"].keys(),
        coerce=True,
        nullable=True,
    )
    admidate: Series[date] = pa.Field(
        ge=date(year=2021, month=10, day=1),
        le=date(year=2022, month=9, day=30),
        coerce=True,
        nullable=False,
    )
    admitime: Series[time] = pa.Field(nullable=True, coerce=True)

    disdest: Series[str] = pa.Field(
        description=nhsdd.disdest["url"],
        isin=nhsdd.disdest["mapping"].keys(),
        coerce=True,
        nullable=True,
    )

    dismeth: Series[str] = pa.Field(
        description=nhsdd.dismeth["url"],
        isin=nhsdd.dismeth["mapping"].keys(),
        coerce=True,
        nullable=True,
    )
    length_of_stay: Series[float] = pa.Field(nullable=True)

    epiorder: Series[int] = pa.Field(nullable=True)

    admiage: Series[float] = pa.Field(
        ge=0,
        le=130,
        nullable=True,
    )


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
