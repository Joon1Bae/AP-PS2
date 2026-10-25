"""Q3(b): GMM estimate of gamma from E[R_w,t^(-gamma) xR_w,t] = 0.

Implements spec/q3b.md (point estimate; the standard error waits for the Newey-West rounding
rule to be added to spec/q34_common.md item 8):
- Data: EQ Dataset, R_w,t = exp(re_t), R_f,t = exp(rf_t), xR_w,t = R_w,t - R_f,t;
  sample Jun 1928 - Dec 2021 (spec/q34_common.md item 6).
- One moment, one parameter. gamma solves G * E[R_w^-gamma xR_w] = 0 with the analytical
  G = dE[R_w^-gamma xR_w]/dgamma = -E[ln(R_w) R_w^-gamma xR_w] (footnote 5), i.e. the
  minimizer of E[R_w^-gamma xR_w]^2.

Output (output/):
- q3b_gamma_estimate.csv   gamma, the moment and G at gamma, and the sample

Run from the repository root:  uv run python src/q3b.py
"""

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from q34_data import SAMPLE_END, SAMPLE_START, load_eq
from sdf import OUTPUT

SEARCH_GRID = np.linspace(-20.0, 60.0, 8001)  # numerical search range for the minimizer


def moment(gamma: float, r_w: np.ndarray, xr_w: np.ndarray) -> float:
    return float(np.mean(r_w ** (-gamma) * xr_w))


def g_hat(gamma: float, r_w: np.ndarray, xr_w: np.ndarray) -> float:
    """Analytical G = -E[ln(R_w) R_w^-gamma xR_w]."""
    return float(-np.mean(np.log(r_w) * r_w ** (-gamma) * xr_w))


def estimate_gamma(r_w: np.ndarray, xr_w: np.ndarray) -> float:
    """Root of G * E[moment] with the smallest squared moment (global minimizer on the grid)."""
    foc = np.array([g_hat(c, r_w, xr_w) * moment(c, r_w, xr_w) for c in SEARCH_GRID])
    brackets = np.where(np.sign(foc[:-1]) != np.sign(foc[1:]))[0]
    if len(brackets) == 0:
        raise ValueError("No solution of the first-order condition on the search grid.")
    roots = [
        brentq(lambda c: g_hat(c, r_w, xr_w) * moment(c, r_w, xr_w),
               SEARCH_GRID[i], SEARCH_GRID[i + 1], xtol=1e-14)
        for i in brackets
    ]
    return min(roots, key=lambda c: moment(c, r_w, xr_w) ** 2)


def main() -> None:
    eq = load_eq().loc[SAMPLE_START:SAMPLE_END]
    if not eq.index.equals(pd.period_range(SAMPLE_START, SAMPLE_END, freq="M")):
        raise ValueError("The EQ sample has gaps; the spec needs a rule for them.")
    r_w = eq["R_w"].to_numpy()
    xr_w = eq["xR_w"].to_numpy()

    gamma = estimate_gamma(r_w, xr_w)

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "gamma": gamma,
        "moment_at_gamma": moment(gamma, r_w, xr_w),
        "G_at_gamma": g_hat(gamma, r_w, xr_w),
        "sample_start": str(eq.index[0]), "sample_end": str(eq.index[-1]), "T": len(eq),
    }]).to_csv(OUTPUT / "q3b_gamma_estimate.csv", index=False, encoding="utf-8")

    print(f"Sample: {eq.index[0]} to {eq.index[-1]} (T = {len(eq)} months)")
    print(f"gamma = {gamma:.6f}; moment at gamma = {moment(gamma, r_w, xr_w):.3e}; "
          f"G = {g_hat(gamma, r_w, xr_w):.6f}")


if __name__ == "__main__":
    main()
