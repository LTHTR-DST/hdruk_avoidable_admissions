# Data Analysis Pipeline

Data harmonisation is a vital step in constructing a reproducible, reusable data analytics pipeline.

Please refer to the detailed data specification and analysis plan developed by the lead team at Sheffield University.

These documentation as well as detailed, step-by-step information on setting up a Python environment and getting started on this project are available at <https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/>.

The Avoidable Admissions project requires the preparation and analysis of 2 distinct datasets - for admitted care and emergency care.
The steps are identical for both and are shown in the flow chart below.

Click on the flowchart elements for more information as it applies to the Admitted Care Dataset.
Similar functions are available for the Emergency Care Dataset.

``` mermaid
flowchart TB
    subgraph Admitted_Care_Pipeline
        direction TB
        subgraph Preprocessing
            A(Extract) --> B(Validate)
            B --> C{Errors?}
            C -->|Yes| D(Fix Errors)
            D --> B
        end
        subgraph Feature_Engineering
            C -->|No| E(Generate Features)
            E --> F(Validate)
            F --> G{Errors?}
            G -->|Yes| H(Fix Errors)
            H --> F
        end
        subgraph Analysis
            G -->|No| I(Analysis)
        end
    end
    style A fill:#eee,stroke:#526cfe,stroke-width:4px
    style E fill:#eee,stroke:#526cfe,stroke-width:4px
    style I fill:#eee,stroke:#526cfe,stroke-width:4px

    style B stroke: #26b079, stroke-width:4px
    style F stroke: #26b079, stroke-width:4px

    style D stroke: #ff7872
    style H stroke: #ff7872


    style Admitted_Care_Pipeline fill:#fff
    style Preprocessing fill: #fff
    style Feature_Engineering fill: #fff
    style Analysis fill: #fff

    click B "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_admitted_care_data"
    click F "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_admitted_care_features"

    click C "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_dataframe--validation-example"
    click G "/hdruk_avoidable_admissions/validation/#avoidable_admissions.data.validate.validate_dataframe--validation-example"


    click E "/hdruk_avoidable_admissions/features/#avoidable_admissions.features.build_features.build_admitted_care_features"

    click D "/hdruk_avoidable_admissions/validation/#fixing-errors"

```
