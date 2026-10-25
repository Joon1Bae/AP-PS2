"""Data alignment shared by Questions 3 and 4 (spec/q34_common.md).

- EQ Dataset: R_e,t = exp(re_t), R_f,t = exp(rf_t), gross returns over months t-11 to t;
  xR_w,t = exp(re_t) - exp(rf_t). Real returns.
- French portfolios: monthly value-weighted "Lo 10" ... "Hi 10" (BE/ME) and "Lo PRIOR" ...
  "Hi PRIOR" (momentum), in decimals, compounded to trailing 12-month gross returns
  R12_j,t = (1 + R_j,t) ... (1 + R_j,t-11); likewise R12_f,t from the monthly "RF".
  xR_j,t = R12_j,t - R12_f,t. Nominal returns (no deflation).
- Common sample: 1928-06 to 2021-12.
"""

import numpy as np
import pandas as pd

from french_data import MISSING_CODES, read_french_block
from q2a import DECILES as BM_DECILES
from q2b import DECILES as MOM_DECILES
from sdf import DATA

FRENCH_START = pd.Period("1927-07", freq="M")
SAMPLE_START = pd.Period("1928-06", freq="M")
SAMPLE_END = pd.Period("2021-12", freq="M")


def load_eq() -> pd.DataFrame:
    """R_w,t = exp(re_t) and xR_w,t = exp(re_t) - exp(rf_t) from the EQ Dataset, by month."""
    eq = pd.read_csv(DATA / "EQ Dataset.csv")
    eq.index = pd.PeriodIndex.from_fields(year=eq["YEAR"], month=eq["MONTH"], freq="M").rename("date")
    if eq[["re", "rf"]].isna().any().any():
        raise ValueError("Missing values in EQ Dataset.csv; the spec needs a rule for them.")
    r_w = np.exp(eq["re"])
    return pd.DataFrame({"R_w": r_w, "xR_w": r_w - np.exp(eq["rf"])})


def trailing_12m(monthly: pd.DataFrame) -> pd.DataFrame:
    """Trailing 12-month gross return (1 + R_t)...(1 + R_t-11); NaN until 12 months exist."""
    return (1.0 + monthly).rolling(12).apply(np.prod, raw=True)


def load_french_12m_excess() -> pd.DataFrame:
    """xR_j,t = R12_j,t - R12_f,t for j = 1..20 (BE/ME deciles, then momentum deciles)."""
    rf = read_french_block(DATA / "F-F_Research_Data_Factors.csv")[["RF"]]
    bm = read_french_block(DATA / "Portfolios_Formed_on_BE-ME.csv", title="Value Weight Returns -- Monthly")
    mom = read_french_block(DATA / "10_Portfolios_Prior_12_2.csv", title="Value Weight Returns -- Monthly")
    monthly = pd.concat([bm[BM_DECILES], mom[MOM_DECILES], rf], axis=1, join="inner").loc[FRENCH_START:]

    # The spec has no missing-data rule, so stop instead of silently handling gaps.
    if monthly.isin(MISSING_CODES).any().any() or monthly.isna().any().any():
        raise ValueError("Missing values in the French data; the spec needs a rule for them.")
    if not monthly.index.equals(pd.period_range(monthly.index[0], monthly.index[-1], freq="M")):
        raise ValueError("The French data have missing months; the spec needs a rule for them.")

    r12 = trailing_12m(monthly / 100.0).dropna()
    return r12[BM_DECILES + MOM_DECILES].sub(r12["RF"], axis=0)


def load_q34_sample() -> tuple[pd.DataFrame, pd.Series]:
    """21 excess returns (20 French deciles, then xR_w) and R_w on the common sample."""
    eq = load_eq()
    xr = pd.concat([load_french_12m_excess(), eq["xR_w"]], axis=1, join="inner")
    months = xr.index
    if months[0] != SAMPLE_START or months[-1] != SAMPLE_END:
        raise ValueError(f"Common sample is {months[0]} to {months[-1]}, not {SAMPLE_START} to {SAMPLE_END}.")
    if not months.equals(pd.period_range(SAMPLE_START, SAMPLE_END, freq="M")):
        raise ValueError("The common sample has gaps; the spec needs a rule for them.")
    return xr, eq.loc[months, "R_w"]
