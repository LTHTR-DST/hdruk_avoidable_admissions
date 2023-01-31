import pandas as pd

from avoidable_admissions.features import build_emergency_care_features as ecf


def build_emergency_care_features(df: pd.DataFrame) -> pd.DataFrame:

    df = (
        df.pipe(ecf._age)
        .pipe(ecf._accomondationstatus)
        .pipe(ecf._edacuity)
        .pipe(ecf._edarivalemode)
        .pipe(ecf._edattenddispatch)
        .pipe(ecf._edattendsource)
        .pipe(ecf._eddiag)
        .pipe(ecf._edinvest)
        .pipe(ecf._edrefservice)
        .pipe(ecf._edtreat)
        .pipe(ecf._ethnos)
        .pipe(ecf._gender)
        .pipe(ecf._townsend)
    )

    return df
