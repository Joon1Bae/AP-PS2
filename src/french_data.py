"""Readers for the Ken French data library CSV files in data/."""

import io
from pathlib import Path

import pandas as pd

# Missing-value codes used in the Ken French files.
MISSING_CODES = (-99.99, -999.0)


def read_french_block(path: Path, title: str | None = None) -> pd.DataFrame:
    """Return one monthly table of a Ken French CSV file, indexed by month.

    The files stack several tables (e.g. value- and equal-weighted returns). Each
    table is a header row starting with ',' followed by YYYYMM rows and ends at a
    blank line. With ``title`` the table right after that title line is returned;
    without it, the first table in the file. Values are kept in the file's units.
    """
    lines = Path(path).read_text().splitlines()
    if title is None:
        start = next(i for i, line in enumerate(lines) if line.startswith(","))
    else:
        start = next(i for i, line in enumerate(lines) if line.strip() == title) + 1
    end = start + 1
    while end < len(lines) and lines[end].strip():
        end += 1

    df = pd.read_csv(io.StringIO("\n".join(lines[start:end])), skipinitialspace=True)
    dates = df.pop(df.columns[0]).astype(str).str.strip()
    if not dates.str.fullmatch(r"\d{6}").all():
        raise ValueError(f"{path}: block {title!r} does not have monthly YYYYMM dates")
    df.index = pd.PeriodIndex(pd.to_datetime(dates, format="%Y%m").dt.to_period("M"), name="date")
    df.columns = df.columns.str.strip()
    return df.astype(float)
