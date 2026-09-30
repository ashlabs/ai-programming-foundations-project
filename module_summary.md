---
title: U.S. Airline Operational Performance Analysis — Module Summary
author: Ashwin Parthasarathy
date: 2026-09-30
tags:
  - ai-masters
  - capstone
  - data-science
  - reproducibility
---

# U.S. Airline Operational Performance Analysis

**AI Programming Foundations Capstone**
**Author:** Ashwin Parthasarathy
**Date:** September 30, 2026

## Overview

This project developed a reproducible Python data-analysis workflow for examining recent U.S. airline operational performance using the U.S. Bureau of Transportation Statistics (BTS) [Reporting Carrier On-Time Performance](https://www.transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ) dataset. The analysis evaluates flight reliability across time, reporting airlines, and major U.S. origin airports, and examines the distribution of BTS-attributed arrival-delay causes. The workflow combines reproducible data acquisition and preparation with data-quality validation, exploratory analysis, and visualization of more than 11 million domestic flight records.

## Dataset Description

The project uses the BTS Reporting Carrier On-Time Performance dataset, which contains flight-level operational information for non-stop U.S. domestic flights reported by qualifying air carriers (Bureau of Transportation Statistics [BTS], n.d.). The analysis covers January 2025 through July 2026 and includes **11,121,962 flight records across 19 monthly partitions**. The processed analytical dataset retains **41 fields**, including flight dates, airlines and airport identifiers, scheduled and actual departure and arrival information, delay measures, cancellation and diversion indicators, elapsed time, distance, and BTS-attributed delay causes. Monthly source archives were converted to Parquet format and processed partition by partition so that the full dataset did not need to be loaded into memory at once. Raw and processed data files are excluded from Git because of their size, while reproducible scripts are provided to recreate them from the BTS source.

## Workflow Description

The workflow was designed as a reproducible sequence of ingestion, cleaning, exploratory analysis, visualization, and interpretation. Monthly BTS ZIP archives were downloaded with a configurable script and converted into focused Parquet partitions containing only the 41 fields needed for the analysis. The notebook then loaded those monthly partitions rather than combining the full dataset into a single in-memory dataset.

Data cleaning began with checks for missing values, duplicates, invalid identifiers, inconsistent dates, nonpositive distances or elapsed times, and invalid operational flags. Because some missing values are expected for cancelled or diverted flights, the workflow preserved structurally meaningful missingness rather than treating all missing values as errors. Reusable cleaning functions removed exact duplicates if present, standardized binary operational fields, and replaced nonpositive scheduled elapsed times with missing values while retaining the rest of each affected flight record.

Exploratory analysis was performed across all 19 monthly partitions. Each partition was loaded, cleaned with the same functions, summarized, and released from memory. Reusable analysis functions produced monthly, carrier, origin-airport, and delay-cause summaries, allowing the complete dataset to be analyzed consistently while keeping memory usage manageable.

The visualization stage produced five analyses aligned with the analysis questions: monthly departure and arrival delay trends, airline arrival-delay rates, departure-delay rates for the busiest origin airports, overall BTS-attributed delay causes, and delay-cause composition across the busiest origin airports. The final stage interprets the observed patterns, documents assumptions and limitations, and identifies possible extensions into predictive modeling and automated operational analysis.

## Key Decisions and Assumptions

Several design choices were made to keep the workflow reproducible, memory-conscious, and conservative in how it altered source data. The project uses scripts to recreate the raw and processed datasets, a `requirements.txt` file to capture the software environment, and a Jupyter notebook that combines code, outputs, visualizations, and narrative explanation. These choices align with Danchev's (2022) focus on transparent, executable, and reproducible computational workflows.

The dataset was processed in monthly Parquet partitions rather than being loaded into memory as one table. This decision was driven by the size of the dataset—more than 11 million flight records—and allowed the same cleaning and aggregation logic to be applied consistently to every partition while limiting memory usage. The processed data were also restricted to the 41 fields needed for the project rather than retaining every column in the BTS source.

Cleaning was intentionally conservative. Missing values were evaluated in the context of flight operations because cancelled or diverted flights can legitimately lack normal arrival or elapsed-time measurements. Rather than deleting records solely because they contained missing or unusual values, the workflow first screened for potential abnormalities and then applied targeted corrections. This approach is consistent with Van den Broeck et al. (2005), who describe data cleaning as a process of screening, diagnosing, and editing suspected abnormalities and emphasize that missing or extreme values should be interpreted before modification. The full-dataset audit found only 14 nonpositive scheduled elapsed-time values; those individual measurements were replaced with missing values while the rest of each flight record was retained, and no records were removed.

The exploratory analysis focused on operational reliability at several levels rather than attempting to explain delays causally. Departure and arrival delay rates use the BTS 15-minute delay indicators rather than a project-defined threshold. Airport comparisons were limited to the 20 busiest origin airports to make the visualization interpretable while still examining high-volume operations. Delay-cause analysis used attributed delay **minutes**, because the BTS cause fields represent the amount of delay attributed to each category; these percentages therefore describe the composition of attributed delay time rather than the frequency or cause of all flight disruptions (BTS, n.d.).

The visualizations were selected to match the structure of each analytical question: a line chart for changes over time, ranked bar charts for airline and airport comparisons, a bar chart for the overall distribution of attributed delay causes, and a heatmap for comparing delay-cause composition across major origin airports. All comparisons are treated as descriptive. The analysis does not account for route mix, scheduling, weather, network structure, airport capacity, or other confounding factors, and the 19-month window contains only one complete calendar year. Accordingly, observed differences should not be interpreted as causal effects or as established long-term seasonality.

## Results and Interpretation

The analysis identified substantial variation in U.S. airline operational reliability across time, reporting airlines, and major origin airports.

**Figure 1**
*Monthly flight delay rates.*

![[figures/monthly_delay_rates.png]]

Figure 1 shows that departure and arrival delay rates generally moved together across the 19-month analysis period. The arrival-delay rate reached a high of **28.9% in July 2025** and a low of **16.6% in September 2025**, a difference of 12.3 percentage points. Elevated delay rates were visible during June and July in both years, but the observation window contains only one complete calendar year and is therefore insufficient to establish a long-term seasonal pattern.

**Figure 2**
*Arrival delay rates by reporting airline.*

![[figures/carrier_arrival_delay_rates.png]]

Figure 2 compares arrival-delay rates across reporting airlines. Rates ranged from **17.3% for Hawaiian Airlines (HA)** to **27.8% for Frontier Airlines (F9)**. This spread indicates meaningful differences in observed arrival reliability, but it should not be interpreted as measuring carrier performance in isolation because airlines operate different route networks and face different airport, schedule, weather, and operational conditions.

**Figure 3**
*Departure delay rates for flights from the 20 busiest U.S. origin airports.*

![[figures/airport_departure_delay_rates.png]]

Figure 3 examines departure reliability among the 20 busiest U.S. origin airports. Flights departing **Dallas/Fort Worth (DFW)** had the highest departure-delay rate at **29.2%**, while flights departing **Salt Lake City (SLC)** had the lowest at **15.7%**, producing a difference of approximately **13.5 percentage points**. The magnitude of this variation is notable because the comparison is restricted to the 20 busiest origin airports in the dataset. These airports each handled approximately 179,000 to 540,000 departures during the 19-month analysis period and together accounted for about 51.8% of all flights analyzed. Despite operating at these high volumes, their departure-delay rates differed by approximately 13.5 percentage points, suggesting that flight volume alone does not characterize the observed differences in reliability.

**Figure 4**
*Share of BTS-attributed arrival-delay minutes by cause.*

![[figures/delay_cause_composition.png]]

Figure 4 shows the distribution of BTS-attributed arrival-delay minutes. **Late-arriving aircraft accounted for 39.4%**, **carrier delays for 32.9%**, and **National Airspace System (NAS) delays for 21.2%**. Together, these three categories represented approximately **93.4% of all attributed delay minutes** in the analysis. Weather accounted for 6.4%, while security-related delay represented less than 0.2%. These percentages describe attributed delay time for qualifying delayed flights and should not be interpreted as the causes of all flight disruptions.

**Figure 5**
*Composition of attributed delay minutes for flights departing from the 20 busiest U.S. origin airports.*

![[figures/airport_delay_cause_composition.png]]

Figure 5 demonstrates that the composition of attributed delay minutes also varies across major origin airports. Late-arriving aircraft represented nearly half of attributed delay minutes for flights departing DCA, while carrier-attributed delays represented approximately half for flights departing DTW and MSP. NAS-related delay had comparatively larger shares for flights departing LGA, BOS, and EWR. These differences reinforce that airport reliability is multidimensional: the same overall delay rate can arise from different operational mixes, and the delay category assigned to a flight should not be interpreted as proof that the origin airport itself caused the delay.

Taken together, the findings show that reliability differs across time, airlines, airports, and attributed delay categories. The results support examining these dimensions jointly in future predictive work rather than treating any single observed characteristic as a complete explanation of operational reliability.

## Responsible Practice — Bias and Data Quality

Data cleaning can introduce bias when valid observations are removed or when missing values are interpreted without considering why they are missing. In this dataset, cancelled and diverted flights may legitimately lack normal arrival-time or elapsed-time measurements, and BTS delay-cause fields are populated only for qualifying delayed flights (BTS, n.d.). Treating these values as ordinary data errors could systematically exclude disrupted flights and produce an overly favorable/unfavorable picture of operational reliability. The workflow therefore preserved structurally meaningful missing values and based cleaning decisions on the operational meaning of each field.

The cleaning process was deliberately conservative. A full-dataset quality audit covering all **11,121,962 records** found no duplicate records, missing flight dates, invalid calendar values, nonpositive distances, negative taxi times, invalid cancellation or diversion indicators, or inconsistencies between flight dates and their year/month fields. It identified only **14 records with nonpositive scheduled elapsed times**. Rather than removing those flights, the invalid `CRSElapsedTime` values were replaced with missing values while the remaining information in each record was retained. Post-cleaning validation confirmed that all 14 invalid measurements were corrected and that no flight records were removed. This targeted approach is consistent with the recommendation by Van den Broeck et al. (2005) to distinguish the detection and diagnosis of data abnormalities from the decision about whether and how those values should be edited.

Bias can also arise during interpretation. Differences in delay rates among airlines or airports may reflect route mix, scheduling, weather exposure, airspace constraints, airport capacity, network structure, and other operational factors that were not controlled for in this descriptive analysis. For that reason, observed differences are reported as associations rather than causal effects or rankings of airline or airport quality.

Finally, the dataset covers January 2025 through July 2026, providing substantial recent data but only one complete calendar year. Repeated patterns, such as higher summer delay rates, should therefore not be presented as established long-term seasonality. Likewise, BTS delay-cause percentages represent the composition of **attributed delay minutes for qualifying delayed flights**, not the causes of all flights or all disruptions. Future analysis could reduce these limitations by incorporating longer historical periods and external variables such as weather, airport capacity, and route characteristics.

## Reproducibility

Reproducibility was treated as a design requirement rather than as a final packaging step. The repository contains the complete analysis notebook, data-acquisition and preparation scripts, generated figures, dependency specification, and Git history needed to reconstruct the workflow. The raw BTS archives and processed Parquet files are intentionally excluded because of their size; instead, `download_bts_data.py` and `prepare_bts_data.py` reproduce the January 2025 through July 2026 dataset from the original BTS source.

The Python software environment is captured in `requirements.txt`, generated using `pip freeze > requirements.txt`. The project was developed and tested with **Python 3.14.0**, and the frozen environment includes the primary dependencies used by the notebook, including NumPy, Pandas, Matplotlib, Seaborn, PyArrow, and JupyterLab. Someone reproducing the analysis can create a virtual environment, install the frozen dependencies, regenerate the BTS data using the provided scripts, and then execute `data_workflow.ipynb` from top to bottom.

The Git repository also records the project's development history through multiple incremental commits and separate `main` and `develop` branches. This provides traceability for the evolution of ingestion, cleaning, exploratory analysis, visualization, and final notebook changes rather than presenting the project as a single final code snapshot.

These practices are consistent with Danchev's (2022) emphasis on reproducible computational workflows in which code, data-processing steps, and explanatory documentation are sufficiently explicit for another researcher or practitioner to rerun the work. In this project, reproducibility therefore includes not only rerunning the notebook but also recreating the local analytical dataset and software environment from documented sources and commands.

## Sources and Citations

### References

Bureau of Transportation Statistics. (n.d.). *Reporting carrier on-time performance (1987–present)* [Data set]. U.S. Department of Transportation. Retrieved September 29, 2026, from https://www.transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ

Danchev, V. (2022). Reproducible data science with Python: An open learning resource. *Journal of Open Source Education, 5*(56), 156. https://doi.org/10.21105/jose.00156

Van den Broeck, J., Argeseanu Cunningham, S., Eeckels, R., & Herbst, K. (2005). Data cleaning: Detecting, diagnosing, and editing data abnormalities. *PLOS Medicine, 2*(10), e267. https://doi.org/10.1371/journal.pmed.0020267
