"""Download BTS Reporting Carrier On-Time Performance data.

Example:
    python scripts/download_bts_data.py \
        --start-year 2025 \
        --start-month 1 \
        --end-year 2026 \
        --end-month 7

Downloaded ZIP files are stored in data/raw/ and are intentionally
excluded from Git because of their size.
"""

import argparse
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://transtats.bts.gov/PREZIP"

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

CHUNK_SIZE = 1024 * 1024  # 1 MB


def parse_arguments():
    """Parse command-line arguments for the requested date range."""
    parser = argparse.ArgumentParser(
        description=(
            "Download monthly BTS Reporting Carrier "
            "On-Time Performance files."
        )
    )

    parser.add_argument(
        "--start-year",
        type=int,
        required=True,
        help="First year to download.",
    )

    parser.add_argument(
        "--start-month",
        type=int,
        required=True,
        choices=range(1, 13),
        metavar="[1-12]",
        help="First month to download.",
    )

    parser.add_argument(
        "--end-year",
        type=int,
        required=True,
        help="Last year to download.",
    )

    parser.add_argument(
        "--end-month",
        type=int,
        required=True,
        choices=range(1, 13),
        metavar="[1-12]",
        help="Last month to download.",
    )

    return parser.parse_args()


def build_download_list(
    start_year,
    start_month,
    end_year,
    end_month,
):
    """Return inclusive year/month combinations for the requested range."""
    start = (start_year, start_month)
    end = (end_year, end_month)

    if start > end:
        raise ValueError(
            "Start year/month must be earlier than or equal to "
            "end year/month."
        )

    downloads = []

    year = start_year
    month = start_month

    while (year, month) <= end:
        downloads.append((year, month))

        month += 1

        if month == 13:
            month = 1
            year += 1

    return downloads


def build_filename(year, month):
    """Return the BTS ZIP filename for a given year and month."""
    return (
        "On_Time_Reporting_Carrier_On_Time_Performance_"
        f"1987_present_{year}_{month}.zip"
    )


def download_file(url, destination):
    """Download one BTS file unless it already exists locally."""
    if destination.exists():
        print(f"Skipping existing file: {destination.name}")
        return

    temporary_file = destination.with_suffix(".zip.part")

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 BTS-Airline-Performance-Analysis"
            )
        },
    )

    try:
        with urlopen(request) as response:
            total_bytes = int(
                response.headers.get("Content-Length", 0)
            )
            downloaded_bytes = 0

            with temporary_file.open("wb") as output_file:
                while True:
                    chunk = response.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    output_file.write(chunk)
                    downloaded_bytes += len(chunk)

                    if total_bytes:
                        percent = (
                            downloaded_bytes / total_bytes * 100
                        )

                        print(
                            f"\rDownloading {destination.name}: "
                            f"{percent:5.1f}%",
                            end="",
                        )

        temporary_file.rename(destination)
        print(f"\nSaved: {destination}")

    except (HTTPError, URLError) as error:
        if temporary_file.exists():
            temporary_file.unlink()

        print(f"\nFailed to download {url}")
        print(f"Reason: {error}")

        raise


def main():
    """Download BTS files for the requested inclusive date range."""
    args = parse_arguments()

    downloads = build_download_list(
        args.start_year,
        args.start_month,
        args.end_year,
        args.end_month,
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(
        "Requested range: "
        f"{args.start_year}-{args.start_month:02d} "
        "through "
        f"{args.end_year}-{args.end_month:02d}"
    )

    print(f"Monthly files: {len(downloads)}")
    print(f"Destination: {DATA_DIR}\n")

    for year, month in downloads:
        filename = build_filename(year, month)
        url = f"{BASE_URL}/{filename}"
        destination = DATA_DIR / filename

        download_file(url, destination)

    print("\nAll requested BTS files are available.")


if __name__ == "__main__":
    main()