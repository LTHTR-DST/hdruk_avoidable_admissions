## Using a notebook / jupyter lab

Once you have the notebook or lab working your view should look something like this (lab displayed below). You need nothing else to run the pipeline.

![Jupyter Lab](https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs/blob/southampton/docs/images/notebook.JPG?raw=true)

If you don't have a strong preference I recommend using the lab as it has more features and provides a very satisfactory browser based programming environment completely for free on almost any machine.

## Why a notebook?

Data based projects tend to be very iterative. Notebooks although terrible for production allow a lot of experimentation and testing which is what is needed while learning. They allow us here to strike an optimal balance between all the sites as they minimise the need for software engineering skill while maximising results and visibility for the analyst.

## Opening a notebook

First navigate to the data extraction folder. Then open the data extraction notebook - `data_extraction.ipynb`

It should look something like this:

![Extraction](https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs/blob/southampton/docs/images/extraction.JPG?raw=true)

## Importing packages

In order to use the notebook you need to first import the packages. This is done in the first line of the notebook with the lines:

```python
import numpy as np
import pandas as pd

import avoidable_admissions as aa
```

if this doesn't work it is because python can't find the avoidable admissions package inside the repository. A quick way to fix this is to copy this into the data_extraction folder but if you ran through the previous steps in order it should work as the setup.py file looks for this at install and logs its location so python can find it.

The other way to solve the problem is too complicated for the scope of this guide so I recommend copying needed modules into the same root folder as the notebook for now. The priority here is to get going not have a perfect folder structure.

NB. The data used in this repository is entirely artificatial and was generated using [NHSx Synthic VAE Data](https://github.com/nhsx/SynthVAE) - it is intentially of low quality to illustrate the validator failing.

## Loading in dataset

In this tutorial we are going to use a synthetic dataset we generated specifically for this project. Thanks to Vishnu for creating this.

We load in the dataset as follows:

```python
df = pd.read_csv("synthetic_data/sdv_hdruk_admitted_care_synthetic_data.csv", dtype=str)
```

Pandas is a python package for handling data. You will need to load your data in via whatever means relevant. You can use pd.read_csv(), pd.read_excel(), pd.read_sql() or any other pandas method to load the data in.

The aim is not to be too prescriptive here but if you would like more info on how to load data into a notebook using pure SQL please check out [NHS SQL Querying in a Notebook Examples](https://github.com/MattStammers/Life_Death_Python) which explains all the steps needed to do this with a couple of examples. We now use neither of these methods but they are good stepping stones to learning how to do this.

## Manipulating the Data

You can use the python notebook to manipulate the data as demonstrated here. The first step is to re-format the data correctly. A simple re-mapping technique is demonstrated here.

This process is best done with SQL if possible upon extract but not everyone has that luxury

## First Validation

Oh dear that didn't go very well and we get a horrible stack trace as below:

![Validation Failure Case](https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs/blob/southampton/docs/images/failure_cases.JPG?raw=true)

This means we need to do more work on our dataset before it will pass validation. Presently we have

```python
Total number of rows in input data   : 20000
Number of rows that passed validation: 0
Number of rows that failed validation: 40014
```

but at least we have some data which is a good start.
