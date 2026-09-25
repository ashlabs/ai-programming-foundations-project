"""Prepare BTS monthly flight data for analysis.

The script reads downloaded BTS ZIP files, retains the fields needed
for this project, and writes one Parquet file per month.

Example:
    python scripts/prepare_bts_data.py \
        --start-year 2025 \
        --start-month 1 \
        --end-year 2026 \
        --end-month 7
"""

import argparse
from pathlib import Path
from zipfile import ZipFile

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SELECTED_COLUMNS = [
    "Year",
    "Month",
    "DayOfWeek",
    "FlightDate",
    "Reporting_Airline",
    "DOT_ID_Reporting_Airline",
    "Flight_Number_Reporting_Airline",
    "OriginAirportID",
    "Origin",
    "OriginCityName",
    "OriginState",
    "DestAirportID",
    "Dest",
    "DestCityName",
    "DestState",
    "CRSDepTime",
    "DepTime",
    "DepDelay",
    "DepDelayMinutes",
    "DepDel15",
    "DepTimeBlk",
    "TaxiOut",
    "CRSArrTime",
    "ArrTime",
    "ArrDelay",
    "ArrDelayMinutes",
    "ArrDel15",
    "ArrTimeBlk",
    "TaxiIn",
    "Cancelled",
    "CancellationCode",
    "Diverted",
    "CRSElapsedTime",
    "ActualElapsedTime",
    "AirTime",
    "Distance",
    "CarrierDelay",
    "WeatherDelay",
    "NASDelay",
    "SecurityDelay",
    "LateAircraftDelay",
]


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Prepare downloaded BTS flight data for analysis."
    )

    parser.add_argument(
        "--start-year",
        type=int,
        required=True
    )

    parser.add_argument(
        "--start-month",
        type=int,
        required=True,
        choices=range(1, 13),
        metavar="[1-12]",
    )

    parser.add_argument(
        "--end-year",
        type=int,
        required=True
    )

    parser.add_argument(
        "--end-month",
        type=int,
        required=True,
        choices=range(1, 13),
        metavar="[1-12]",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing processed Parquet files.",
    )

    return parser.parse_args()


def build_month_range(start_year, start_month, end_year, end_month):
    """Return inclusive year/month pairs for the requested range."""
    start = (start_year, start_month)
    end = (end_year, end_month)

    if start > end:
        raise ValueError(
            "Start year/month must not be later than end year/month."
        )

    months = []
    year = start_year
    month = start_month

    while (year, month) <= end:
        months.append((year, month))

        month += 1

        if month == 13:
            month = 1
            year += 1

    return months


def get_archive_name(year, month):
    """Return the BTS ZIP filename for a year and month.
    
    Parameters
    ----------
    year : int
        Four-digit year of the requested BTS dataset.
    month : int
        Month number from 1 through 12.

    Returns
    -------
    str
        BTS ZIP archive filename for the requested year and month.
    """
    return (
        "On_Time_Reporting_Carrier_On_Time_Performance_"
        f"1987_present_{year}_{month}.zip"
    )


def get_csv_file_in_archive(archive):
    """Return the single CSV filename contained in a BTS ZIP archive.

    Parameters
    ----------
    archive : zipfile.ZipFile
        Open BTS ZIP archive to inspect.

    Returns
    -------
    str
        Name of the CSV file contained in the archive.

    Raises
    ------
    RuntimeError
        If the archive does not contain exactly one CSV file.
    """
    csv_files = [
        name
        for name in archive.namelist()
        if name.lower().endswith(".csv")
    ]

    if len(csv_files) != 1:
        raise RuntimeError(
            "Expected exactly one CSV file in BTS archive, "
            f"found {len(csv_files)}."
        )

    return csv_files[0]


def process_month_to_parquet(year, month, overwrite=False):
    """Convert one BTS monthly ZIP archive to a focused Parquet file.

    Parameters
    ----------
    year : int
        Four-digit year of the BTS monthly dataset to process.
    month : int
        Month number from 1 through 12.
    overwrite : bool, optional
        Whether to overwrite an existing processed Parquet file.
        Defaults to False.

    Returns
    -------
    int or None
        Number of rows written to the Parquet file, or None if the
        output file already exists and overwrite is False.

    Raises
    ------
    FileNotFoundError
        If the expected raw BTS ZIP archive does not exist.
    RuntimeError
        If the ZIP archive does not contain exactly one CSV file.
    """
    raw_path = RAW_DIR / get_archive_name(year, month)

    output_path = (
        PROCESSED_DIR
        / f"bts_flights_{year}_{month:02d}.parquet"
    )

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw BTS file not found: {raw_path}"
        )

    if output_path.exists() and not overwrite:
        print(f"Skipping existing file: {output_path.name}")
        return None

    print(f"Processing {year}-{month:02d}...")

    with ZipFile(raw_path) as archive:
        csv_name = get_csv_file_in_archive(archive)

        with archive.open(csv_name) as csv_file:
            df = pd.read_csv(
                csv_file,
                usecols=SELECTED_COLUMNS,
                parse_dates=["FlightDate"],
                low_memory=False,
            )

    df.to_parquet(
        output_path,
        index=False,
        engine="pyarrow",
    )

    print(
        f"  Rows: {len(df):,} | "
        f"Columns: {len(df.columns)} | "
        f"Saved: {output_path.name}"
    )

    return len(df)


def main():
    """Prepare all requested monthly BTS files."""
    args = parse_arguments()

    months = build_month_range(
        args.start_year,
        args.start_month,
        args.end_year,
        args.end_month,
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    total_rows = 0

    for year, month in months:
        row_count = process_month_to_parquet(
            year,
            month,
            overwrite=args.overwrite,
        )

        if row_count is not None:
            total_rows += row_count

    print()
    print("Preparation complete.")

    if total_rows:
        print(f"Rows processed this run: {total_rows:,}")


if __name__ == "__main__":
    main()