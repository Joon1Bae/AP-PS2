"""Q4(e): Fama-MacBeth estimates of lambda and alpha_j for the linear beta pricing model.

Implements spec/q4e.md (data and sample as in Q4(b): Jun 1928 - Dec 2021):
- Factor F_t = R_w,t = exp(re_t) (gross return; no constant-R_f assumption).
- First pass: for each asset j = 1..21, full-sample OLS xR_j,t = beta_0,j + beta_j R_w,t + eps_j,t.
- Second pass: for each month t, OLS without intercept across the 21 assets,
      xR_j,t = lambda_t beta_j + alpha_j,t,
  giving lambda_t and the residuals alpha_j,t.
- lambda = mean(lambda_t), alpha_j = mean(alpha_j,t); standard errors from a regression of each
  series on a constant with Newey-West S (lag selected separately for each series; gmm.py).

Outputs (output/):
- q4e_estimates.csv   lambda, its s.e. and NW lag
- q4e_alphas.csv      beta_j, alpha_j, its s.e., t-stat and NW lag for each asset
- q4e_lambda_t.csv    the monthly lambda_t series
- q4e_table.tex       LaTeX tabular (input by tex/ps2_solution.tex)

Run from the repository root:  uv run python src/q4e.py
"""

import numpy as np
import pandas as pd

from q34_data import load_q34_sample
from q4d import nw_mean
from sdf import OUTPUT
from tables import long_table, sample_text


def latex_table(lam: dict, alphas: pd.DataFrame, months: pd.PeriodIndex) -> str:
    """Panels A (lambda), B (alphas, BM and MOM side by side), C (Newey-West lags, sample)."""
    return long_table(
        "src/q4e.py",
        {"title": "Panel A: Factor risk premium", "header": ("Estimate", "s.e."),
         "rows": [(r"$\hat{\lambda}$", f"{lam['lambda']:.4f}", f"{lam['se']:.4f}")]},
        {"title": "Panel B: Pricing errors", "stat": r"$\hat{\alpha}_j$",
         "blocks": [(None, alphas["alpha"].to_numpy(), alphas["t_alpha"].to_numpy())]},
        {"title": "Panel C: Newey--West lags",
         "header": (r"Lag, $\hat{\lambda}$", r"Lags, $\hat{\alpha}_j$", "", ""),
         "rows": [("", str(lam["lag"]), f"{int(alphas['nw_lag'].min())}--{int(alphas['nw_lag'].max())}", "", "")]},
        sample_text(months),
    )


def main() -> None:
    xr, r_w = load_q34_sample()
    y = xr.to_numpy()                      # T x 21
    f = r_w.to_numpy()

    # First pass: full-sample time-series betas (with intercept).
    x_ts = np.column_stack([np.ones_like(f), f])
    beta = np.linalg.lstsq(x_ts, y, rcond=None)[0][1]          # 21

    # Second pass: monthly cross-sectional regressions on beta, no intercept.
    lambda_t = y @ beta / (beta @ beta)                         # T
    alpha_t = y - lambda_t[:, None] * beta[None, :]             # T x 21

    lam_hat, lam_se, lam_lag = nw_mean(lambda_t)
    lam = {"lambda": lam_hat, "se": lam_se, "lag": lam_lag}
    rows = []
    for j, name in enumerate(xr.columns):
        a, se, lag = nw_mean(alpha_t[:, j])
        rows.append({"j": j + 1, "asset": name, "beta": beta[j], "alpha": a, "se_alpha": se,
                     "t_alpha": a / se, "nw_lag": lag})
    alphas = pd.DataFrame(rows)

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "lambda": lam_hat, "se_lambda": lam_se, "t_lambda": lam_hat / lam_se, "nw_lag_lambda": lam_lag,
        "sample_start": str(xr.index[0]), "sample_end": str(xr.index[-1]), "T": len(f),
    }]).to_csv(OUTPUT / "q4e_estimates.csv", index=False, encoding="utf-8")
    alphas.to_csv(OUTPUT / "q4e_alphas.csv", index=False, encoding="utf-8")
    pd.DataFrame({"date": xr.index.astype(str), "lambda_t": lambda_t}).to_csv(
        OUTPUT / "q4e_lambda_t.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4e_table.tex").write_text(latex_table(lam, alphas, xr.index), encoding="utf-8")

    print(f"Sample: {xr.index[0]} to {xr.index[-1]} (T = {len(f)} months)")
    print(f"lambda = {lam_hat:.6f} (se {lam_se:.6f}, t {lam_hat / lam_se:.2f}, NW lag {lam_lag})")
    print(alphas.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
