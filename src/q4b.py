"""Q4(b): first-stage GMM (W = I) estimate of b in M_t = 1 - b (R_w,t - E[R_w]).

Implements spec/q4b.md (point estimate of b only; standard errors, pricing errors and the
chi-squared test are not specified yet):
- j = 1..20: monthly value-weighted "Lo 10" ... "Hi 10" and "Lo PRIOR" ... "Hi PRIOR" excess
  returns over RF from F-F_Research_Data_Factors.csv, in decimal units (as in Q2).
- j = 21: xR_w,t = R_w,t - R_f,t with R_w,t = exp(re_t), R_f,t = exp(rf_t) from the EQ Dataset
  (annual returns observed monthly), paired with the monthly portfolio returns of the same
  month t (Additional Decision 1).
- Sample: months in which all 21 excess returns and R_w are available, Dec 1927 - Dec 2021.
- Estimator (no intercept), with F = R_w and Cov dividing by T:
      d = Cov(F, xR),   b = (d'd)^-1 d' E[xR].

Output (output/):
- q4b_b_estimate.csv   b and the sample it was estimated on

Run from the repository root:  uv run python src/q4b.py
"""

import numpy as np
import pandas as pd

from q2a import load_bm_excess_returns
from q2b import load_mom_excess_returns
from sdf import DATA, OUTPUT


def load_eq() -> pd.DataFrame:
    """R_w,t = exp(re_t) and xR_w,t = exp(re_t) - exp(rf_t) from the EQ Dataset, by month."""
    eq = pd.read_csv(DATA / "EQ Dataset.csv")
    eq.index = pd.PeriodIndex.from_fields(year=eq["YEAR"], month=eq["MONTH"], freq="M").rename("date")
    if eq[["re", "rf"]].isna().any().any():
        raise ValueError("Missing values in EQ Dataset.csv; the spec needs a rule for them.")
    r_w = np.exp(eq["re"])
    return pd.DataFrame({"R_w": r_w, "xR_w": r_w - np.exp(eq["rf"])})


def estimate_b(xr: pd.DataFrame, f: pd.Series) -> float:
    """b = (d'd)^-1 d' E[xR] with d_j = 1/T sum_t (F_t - Fbar)(xR_j,t - xRbar_j)."""
    x = xr.to_numpy()
    f = f.to_numpy()
    d = ((f - f.mean())[:, None] * (x - x.mean(axis=0))).mean(axis=0)
    return float(d @ x.mean(axis=0) / (d @ d))


def main() -> None:
    xr_bm = load_bm_excess_returns()
    xr_mom = load_mom_excess_returns()
    eq = load_eq()

    # Common months of all 21 excess returns and R_w (Additional Decision 2).
    months = xr_bm.index.intersection(xr_mom.index).intersection(eq.index)
    xr = pd.concat([xr_bm.loc[months], xr_mom.loc[months], eq.loc[months, ["xR_w"]]], axis=1)
    r_w = eq.loc[months, "R_w"]
    if not months.equals(pd.period_range(months[0], months[-1], freq="M")):
        raise ValueError("The common sample has gaps; the spec needs a rule for them.")

    b = estimate_b(xr, r_w)

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame({
        "parameter": ["b"],
        "estimate": [b],
        "sample_start": [str(months[0])],
        "sample_end": [str(months[-1])],
        "T": [len(months)],
    }).to_csv(OUTPUT / "q4b_b_estimate.csv", index=False, encoding="utf-8")

    print(f"Sample: {months[0]} to {months[-1]} (T = {len(months)} months, N = {xr.shape[1]} assets)")
    print(f"b = {b:.6f}")


if __name__ == "__main__":
    main()
