# Welcome to Avoidable Admissions

This Python package is being developed as part of a federated multi-site collaboration led by the [School of Health and Related Research](https://www.sheffield.ac.uk/scharr) at [Sheffield University](https://www.sheffield.ac.uk/) and coordinated by [HDRUK](https://www.hdruk.ac.uk/).

The study documentation is maintained at <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs>.

The `avoidable_admissions` Python package is documented here along with examples.

## Installation

Please see the [README.md](https://github.com/LTHTR-DST/hdruk_avoidable_admissions#readme) file for more information on environment setup for contributing to development.

The following describes installation of the package within an existing environment.
A separate virtual environment is recommended.

The package maybe installed directly from GitHub using one of the following commands:

To install only the package:

```shell
pip install "avoidable_admissions @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"
```

To install with optional dependencies for _exploratory data analysis_:

```shell
pip install "avoidable_admissions[eda] @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"
```

To install with optional dependecies for _contributing to development and documentation_:

```shell
pip install "avoidable_admissions[dev] @ git+https://github.com/LTHTR-DST/hdruk_avoidable_admissions.git@<release-name>"
```

Replace `<release-name>` with the latest release version e.g. `v0.3.1`. List of releases can be found here - <https://github.com/LTHTR-DST/hdruk_avoidable_admissions/releases>.

Omit `@<release-name>` to install the latest code in the repo.

See <https://lthtr-dst.github.io/hdruk_avoidable_admissions/admitted_care_pipeline_example> for a complete example.
