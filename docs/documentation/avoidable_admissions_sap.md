## Avoidable Admissions Statistical Analysis Approach

Please consult the core protocol from Sheffield for a detailed explanation of the purpose of the project and use that as the primary point of reference not this website which only mirrors their protocol.

## Aims

1.	To understand variation across the country in all acute hospital admissions 
2.	To explore methods for identifying an avoidable acute admission focussing on ambulatory care sensitive conditions

Ambulatory care sensitive conditions (ACSCs) are conditions where effective community care and case management can help prevent the need for hospital admission.

## Objectives

1.	Take a multi-regional approach to analysing routine data to describe patterns of acute admission and regional variation in admissions over a defined period of time
2.	Analyse variation in acute admission by factors including deprivation, patient demographics, time of day, day of week, waiting times
3.	Use hospital admission data to describe outcomes following acute admission including length of stay, death in hospital.
4.	 Identifying groups of patients at high risk of an avoidable admission using ACSC codes from the Emergency Department and also acute admissions data

For ambulatory care conditions (ACSC), we are wanting to explore variations in ED attendances and admitted patients. We are interested in exploring this by patient characteristics such as deprivation and age, as well as looking to see how the attendances differ, i.e. time of day. In addition, we want to explore variations in the outcomes, for example, length of stay and death.

## 1. ECDS (ED) dataset:

### 1.1 Analysis Populations
This section describes the analysis populations for the analysis of the ECDS data. These populations will be referred to in the analysis descriptions that follow.

#### 1.1.1 All Attendances
This analysis population includes all adult unplanned first emergency care attendances for a new clinical condition (or deterioration of a chronic condition) at Type 1 Emergency Departments (Emergency Departments that are a consultant led 24 hour service with full resuscitation facilities and designated accommodation for the reception of emergency care patients)

- Filter: (edattendcat = 1) & (eddepttype = 01)

These filters should have been applied to the original data extract.

#### 1.1.2 Attendances for ACSCs
This analysis population includes all unplanned first emergency care attendances for a new clinical condition (or deterioration of a chronic condition) at a Type 1 Emergency Department where the primary diagnosis is an ACSC.

- Filter: (edattendcat = 1) & (eddepttype = 01) & (eddiag_01 = ACSC_Code_ED)

Please see HDRUK Data Processing V1 for ACSC_Code_ED definition. (These definitions are replicated in the codebase inside this repository)

#### 1.1.3 Attendances for Non-ACSCs
This analysis population includes all unplanned first emergency care attendances for a new clinical condition (or deterioration of a chronic condition) at a Type 1 Emergency Department where the primary diagnosis is not an ACSC.

- Filter: (edattendcat = 1) & (eddepttype = 01) & (eddiag_01 != ACSC_Code_ED)

Please see HDRUK Data Processing V1 for ACSC_Code_ED definition.

### 1.2 Demographics
Summary statistics of the patient demographics, attendance characteristics and attendance outcomes will be calculated. For numerical variables, the minimum (min), maximum (max), mean, standard deviation (SD), median, lower quartile (Q1) and upper quartile (Q3) will be presented with the number of observations used in the calculations. For categorical variables, the number and percentage of patients in each of the categories and the total number of observations will be calculated.

Summary statistics for the demographic variables will be presented at the hospital site level (identified using edsitecode). This analysis will allow the comparison of demographics between different Emergency Departments and investigate any variation in discharge destination (e.g. variation in admissions).

The following summaries will be presented for analysis populations: All Attendances, Attendances for ACSCs and Attendances for Non-ACSCs.

#### 1.2.1 Patient Demographics

-   Age (categorical (to be decided)) - Frequency and proportions
-   Age (continuous) - (N, min, max, mean, SD, median, Q1, Q3)
-   Gender - Frequency and proportions
-   Ethnicity (Categories to be decided) - Frequency and proportions
-   Townsend score decile - Frequencies and proportions
-   Care home flag - Frequencies and proportions
-   Comorbidities - Frequencies and proportions    

#### 1.2.2 Attendance Characteristics

-   Ambulatory Care Sensitive Condition - Frequencies and proportions 
(Attendances for ACSCs analysis population only)
-   Arrival mode - Frequencies and proportions
-   Source of attendance (Categories to be decided) - Frequencies and proportions
-   Day of week - Frequencies and proportions
-   Time of day (Categories to be decided) - Frequencies and proportions
-   Acuity - Frequencies and proportions
-   Presenting complaint - Frequencies and proportions
-   Investigations - Frequencies and proportions
-   Treatments - Frequencies and proportions
-   Certainty  - Frequencies and proportions
-   Time in department - (N, min, max, mean, SD, median, Q1, Q3)

#### 1.2.3 Attendance Outcomes

-   Discharge destination - Frequencies and proportions
-   Service referred to - Frequencies and proportions
-   Discharge method - Frequencies and proportions

### 1.3 ACSC Analysis
This analysis will investigate how all ACSC conditions are handled coming through ED in terms of the discharge destination (e.g. admitted, not admitted, died). It will also potentially identify patient and attendance characteristics that are predictors of avoidable admission.

Summary statistics of the patient demographics, attendance characteristics and attendance outcomes will be calculated. For numerical variables, the minimum (min), maximum (max), mean, standard deviation (SD), median, lower quartile (Q1) and upper quartile (Q3) will be presented with the number of observations used in the calculations. For categorical variables, the number and percentage of patients in each of the categories and the total number of observations will be calculated.

Summary statistics for the demographic variables will be calculated by discharge destination (edattenddispatch - categorisation to be decided) and presented at the hospital site level (identified using edsitecode). 

The following summaries will be presented for analysis populations: Attendances for ACSCs.

#### 1.3.1 Patient Demographics

-   Age (categorical (to be decided)) - Frequencies and proportions
-   Age continuous (N, min, max, mean, SD, median, Q1, Q3)
-   Gender - Frequencies and proportions
-   Ethnicity (Categories to be decided) - Frequencies and proportions
-   Townsend - Frequencies and proportions
-   Carehome flag - Frequencies and proportions
-   Comorbidities - Frequencies and proportions

#### 1.3.2 Attendance Characteristics

-   Ambulatory Care Sensitive Condition - Frequencies and proportions
-   Arrival mode - Frequencies and proportions
-   Source - Frequencies and proportions
-   Day of week - Frequencies and proportions
-   Time of day - Frequencies and proportions
-   Acuity - Frequencies and proportions
-   Presenting complaint - Frequencies and proportions
-   Investigations - Frequencies and proportions
-   Treatments - Frequencies and proportions
-   Certainty  - Frequencies and proportions
-   Time in department - (N, min, max, mean, SD, median, Q1, Q3)


## 2. Admitted Patient Care (APC) Dataset

### 2.1 Analysis Populations
This section describes the analysis populations or the analysis of the APC data. These populations will be referred to in the analysis descriptions that follow.

#### 2.1.1 All Acute Admissions
This analysis population includes all acute admissions.

- Filter: (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1)

These filters should have been applied to the original data extract.

#### 2.1.2 All Acute Admissions for ACSCs
This analysis population includes all acute admissions where the primary diagnosis from the first episode is an ACSC.

- Filter: (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1) & (diag_01 = ACSC_Code_APC)

Please see HDRUK Data Processing V1 for ASCS_Code_APC definition.

#### 2.1.3 All Acute Admissions for Non-ACSCs
This analysis population includes all acute admissions where the primary diagnosis from the first episode is not an ACSC.

- Filter: (admimeth in 21, 22, 23, 24, 25, 2A, 2B, 2C, 2D, 28) & (epiorder = 1) & (diag_01 != ACSC_Code_APC)

Please see HDRUK Data Processing V1 for ASCS_Code_APC definition.

### 2.2 Demographics
Summary statistics of the patient demographics, admission characteristics and admission outcomes will be calculated. For numerical variables, the minimum (min), maximum (max), mean, standard deviation (SD), median, lower quartile (Q1) and upper quartile (Q3) will be presented with the number of observations used in the calculations. For categorical variables, the number and percentage of patients in each of the categories and the total number of observations will be calculated.

Summary statistics for the demographic variables will be presented at the hospital site level (identified using sitret). This analysis will allow the comparison of demographics between different Hospitals.

The following summaries will be presented for analysis populations: All Acute Admissions, All Acute Admissions for ACSCs and All Acute Admissions for Non-ACSCs.

#### 2.2.1 Patient Demographics

-   Age (categorical (to be decided)) - Frequency and proportions
-   Age (continuous) - (N, min, max, mean, SD, median, Q1, Q3)
-   Gender - Frequency and proportions
-   Ethnicity (Categories to be decided) - Frequency and proportions
-   Townsend score decile - Frequencies and proportions
-   Comorbidities - Frequencies and proportions

#### 2.2.2 Admission Characteristics

-   Ambulatory Care Sensitive Condition - Frequencies and proportions (All Acute Admissions for ACSC analysis population only)
-   Source of admission - Frequencies and proportions
-   Day of the week - Frequencies and proportions

#### 2.2.3 Admission Outcomes

-   Length of stay  - (N, min, max, mean, SD, median, Q1, Q3)
-   Length of stay dichotomised (<2 days)
-   Discharge destination - Frequencies and proportions
-   Procedures - Frequencies and proportions