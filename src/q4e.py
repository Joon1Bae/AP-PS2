"""Q4(e): Fama-MacBeth estimates of lambda and alpha_j for the linear beta pricing model.

Implements spec/q4e.md (data as in Q4(b)), for both sample versions of spec/q34_common.md item 6:
(1) Common Dec 1940 - Dec 2021, (2) Max Jun 1928 - Dec 2021:
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

from q34_data import VERSIONS, load_q34_version
from q4d import nw_mean
from sdf import OUTPUT
from tables import long_table, sample_text


def latex_table(res: dict) -> str:
    """Panels A (lambda), B (alphas, BM and MOM side by side), C (Newey-West lags) for each version."""
    keys = list(VERSIONS)
    return long_table(
        "src/q4e.py",
        {"title": "Panel A: Factor risk premium", "header": (r"$\hat{\lambda}$", "s.e."),
         "rows": [(VERSIONS[k], f"{res[k]['lam']['lambda']:.4f}", f"{res[k]['lam']['se']:.4f}") for k in keys]},
        {"title": "Panel B: Pricing errors", "stat": r"$\hat{\alpha}_j$",
         "blocks": [(rf"\textit{{{VERSIONS[k]}}}", res[k]["alphas"]["alpha"].to_numpy(),
                     res[k]["alphas"]["t_alpha"].to_numpy()) for k in keys]},
        {"title": "Panel C: Newey--West lags",
         "header": (r"Lag, $\hat{\lambda}$", r"Lags, $\hat{\alpha}_j$", "$T$", ""),
         "rows": [(VERSIONS[k], str(res[k]["lam"]["lag"]),
                   f"{int(res[k]['alphas']['nw_lag'].min())}--{int(res[k]['alphas']['nw_lag'].max())}",
                   str(len(res[k]["months"])), "") for k in keys]},
        [(f"Sample, {VERSIONS[k]}", sample_text(res[k]["months"])) for k in keys],
    )


def run(xr: pd.DataFrame, r_w: pd.Series) -> dict:
    y = xr.to_numpy()                      # T x 21
    f = r_w.to_numpy()

    # First pass: full-sample time-series betas (with intercept).
    x_ts = np.column_stack([np.ones_like(f), f])
    beta = np.linalg.lstsq(x_ts, y, rcond=None)[0][1]          # 21

    # Second pass: monthly cross-sectional regressions on beta, no intercept.
    lambda_t = y @ beta / (beta @ beta)                         # T
    alpha_t = y - lambda_t[:, None] * beta[None, :]             # T x 21

    lam_hat, lam_se, lam_lag = nw_mean(lambda_t)
    rows = []
    for j, name in enumerate(xr.columns):
        a, se, lag = nw_mean(alpha_t[:, j])
        rows.append({"j": j + 1, "asset": name, "beta": beta[j], "alpha": a, "se_alpha": se,
                     "t_alpha": a / se, "nw_lag": lag})
    return {"lam": {"lambda": lam_hat, "se": lam_se, "lag": lam_lag}, "alphas": pd.DataFrame(rows),
            "lambda_t": lambda_t, "months": xr.index}


def main() -> None:
    res = {k: run(*load_q34_version(k)) for k in VERSIONS}

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "version": k, "lambda": r["lam"]["lambda"], "se_lambda": r["lam"]["se"],
        "t_lambda": r["lam"]["lambda"] / r["lam"]["se"], "nw_lag_lambda": r["lam"]["lag"],
        "sample_start": str(r["months"][0]), "sample_end": str(r["months"][-1]), "T": len(r["months"]),
    } for k, r in res.items()]).to_csv(OUTPUT / "q4e_estimates.csv", index=False, encoding="utf-8")
    pd.concat([r["alphas"].assign(version=k) for k, r in res.items()]).to_csv(
        OUTPUT / "q4e_alphas.csv", index=False, encoding="utf-8")
    pd.concat([pd.DataFrame({"version": k, "date": r["months"].astype(str), "lambda_t": r["lambda_t"]})
               for k, r in res.items()]).to_csv(OUTPUT / "q4e_lambda_t.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4e_table.tex").write_text(latex_table(res), encoding="utf-8")

    for k, r in res.items():
        print(f"{VERSIONS[k]:11s} {r['months'][0]} to {r['months'][-1]} (T = {len(r['months'])}): "
              f"lambda = {r['lam']['lambda']:.6f} (se {r['lam']['se']:.6f}, lag {r['lam']['lag']})")


if __name__ == "__main__":
    main()
