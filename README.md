# U.S. Airline Operational Performance Analysis

A reproducible Python data analysis workflow examining recent U.S. airline operational performance using the U.S. Bureau of Transportation Statistics Reporting Carrier On-Time Performance dataset.

This project is part of the AI Programming Foundations capstone and serves as a portfolio-quality foundation  for future machine learning and AI applications.

## Dataset

This project uses the U.S. Bureau of Transportation Statistics [Reporting Carrier On-Time Performance](https://transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=b0-gvzr&V0s1_b0yB=D&gnoyr_VQ=FGJ) dataset.

The analysis covers January 2025 through July 2026 and includes 11,121,962 domestic flight records across 19 monthly partitions. The preparation workflow retains 41 operational fields covering flight schedules, carriers, origin and destination airports, delays, cancellations, diversions, flight duration, distance, and BTS-attributed delay causes.

Raw BTS archives and processed Parquet files are excluded from the repository because of their size. Reproducible download and preparation scripts are included instead.

## What This Project Builds

The project implements an end-to-end, reproducible data-analysis workflow that:

- Downloads monthly BTS source archives;
- Converts the raw data into analysis-focused Parquet partitions;
- Validates and cleans operational data using reusable functions;
- Processes more than 11 million records without loading the full dataset into memory at once;
- Analyzes reliability across time, reporting airlines, and major origin airports;
- Examines the composition of BTS-attributed delay minutes; and
- Produces publication-ready visualizations and a documented analytical summary.

## Key Results

Across 11,121,962 flights from January 2025 through July 2026:

- Monthly arrival-delay rates varied from 16.6% in September 2025 to 28.9% in July 2025.
- Carrier arrival-delay rates ranged from 17.3% for Hawaiian Airlines (HA) to 27.8% for Frontier Airlines (F9).
- Among the 20 busiest origin airports, departure-delay rates ranged from 15.7% for flights departing Salt Lake City (SLC) to 29.2% for flights departing Dallas/Fort Worth (DFW).
- Late-arriving aircraft accounted for 39.4% of BTS-attributed delay minutes, carrier delays for 32.9%, and National Airspace System delays for 21.2%. Together, these three categories represented approximately 93.4% of attributed delay minutes.

These results are descriptive rather than causal. Differences across carriers and airports may reflect route mix, scheduling, weather exposure, airspace constraints, network structure, and other operational factors.

## Repository Structure

```text
ai-programming-foundations-project/
├── data/
│   ├── raw/                    # Downloaded BTS ZIP archives (not committed)
│   └── processed/              # Prepared monthly Parquet files (not committed)
├── figures/                    # Generated analysis visualizations
├── scripts/
│   ├── download_bts_data.py    # Downloads monthly BTS source archives
│   └── prepare_bts_data.py     # Converts raw archives to focused Parquet files
├── data_workflow.ipynb         # Main reproducible analysis notebook
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and run instructions
```

The raw and processed datasets are intentionally excluded from Git because of their size. They can be recreated using the scripts in `scripts/`.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/ashlabs/ai-programming-foundations-project.git
cd ai-programming-foundations-project
```

### 2. Create and activate a virtual environment

This project was developed and tested with Python 3.14.0.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

The submitted `requirements.txt` is generated from the project environment using:
```bash
pip freeze > requirements.txt
```

### 4. Download the BTS source data

The project analyzes monthly data from January 2025 through July 2026.

```bash
python scripts/download_bts_data.py \
    --start-year 2025 \
    --start-month 1 \
    --end-year 2026 \
    --end-month 7
```

Downloaded archives are stored under `data/raw/`.

### 5. Prepare the analysis dataset

Convert the raw BTS archives into focused monthly Parquet files:

```bash
python scripts/prepare_bts_data.py \
    --start-year 2025 \
    --start-month 1 \
    --end-year 2026 \
    --end-month 7
```

Prepared files are stored under `data/processed/`.

The preparation script also supports the optional `--overwrite` flag when existing Parquet files need to be regenerated.

### 6. Run the notebook

Start Jupyter:

```bash
jupyter lab
```

Open `data_workflow.ipynb` and run all cells from top to bottom.

The notebook processes the monthly Parquet partitions sequentially, so the complete 11.1-million-record dataset does not need to be loaded into memory at once.

## Data Quality and Bias Awareness

Poor data cleaning could bias this analysis if structurally missing values were treated as ordinary missing data or if disrupted flights were removed without considering why their fields were absent. Cancelled and diverted flights, for example, may legitimately lack normal arrival or elapsed-time measurements.

To reduce this risk, the workflow preserves structurally meaningful missing values and removes only clearly invalid measurements. A full-dataset quality audit identified 14 records with nonpositive scheduled elapsed times; those values were replaced with missing values while the remainder of each flight record was retained.

The analysis is descriptive. Differences among airlines and airports may also reflect route mix, schedules, weather exposure, airport capacity, airspace constraints, and other operational factors that are not controlled for here.

## Future AI Extensions

This workflow provides a foundation for more advanced machine learning, deep-learning, and agentic AI applications.

- **Machine learning:** A predictive extension could use schedule, carrier, airport, route, distance, and external weather features to estimate the probability of delays or cancellations. The workflow would need additional feature engineering, train/validation/test splits, leakage checks, model evaluation, and monitoring beyond the descriptive analysis performed here.

- **Neural networks:** Preparing this dataset for neural-network models would require numerical encoding of categorical features, normalization or standardization where appropriate, careful handling of missing values, and construction of model-ready tensors or batches. The large partitioned dataset could also support mini-batch training rather than loading all records into memory at once.

- **Agentic automation:** An AI agent could automate recurring ingestion, validation, analysis, and reporting as new monthly BTS data becomes available. A future operational-intelligence agent could monitor reliability trends, identify emerging anomalies, retrieve supporting data, generate visual summaries, and explain which observed factors are associated with changing performance while preserving appropriate human review.
