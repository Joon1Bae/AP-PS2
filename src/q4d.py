"""Q4(d): time-series estimates of lambda and alpha_j for the linear beta pricing model.

Implements spec/q4d.md (data as in Q4(b)), for both sample versions of spec/q34_common.md item 6:
(1) Common Dec 1940 - Dec 2021, (2) Max Jun 1928 - Dec 2021:
- Factor F_t = xR_w,t (constant-R_f approximation, so the factor is an excess return).
- lambda = mean(F); its standard error from the regression of F on a constant with Newey-West S.
- For each asset j = 1..21, OLS xR_j,t = alpha_j + beta_j F_t + eps_j,t; the t-stat of alpha_j
  uses Newey-West on that regression: aVar = (1/T) (X'X/T)^-1 S (X'X/T)^-1, S from the moment
  series x_t eps_t (lag selected separately for each regression; see gmm.py).
  For j = 21 (the factor itself) alpha = 0, beta = 1, eps = 0, so its t-stat is undefined.
- GRS (1989) on J = 20 assets (1-20), K = 1:
      GRS = (T - J - K)/J (1 + Fbar' Sigma_F^-1 Fbar)^-1 alpha' Sigma_eps^-1 alpha ~ F(J, T - J - K),
  Sigma_eps = eps'eps / (T - K - 1), Sigma_F = sum (F - Fbar)^2 / (T - 1).

Outputs (output/):
- q4d_estimates.csv   lambda, its s.e. and NW lag, GRS statistic and p-value
- q4d_alphas.csv      alpha_j, beta_j, t-stat of alpha_j and NW lag for each asset
- q4d_table.tex       LaTeX tabular (input by tex/ps2_solution.tex)

Run from the repository root:  uv run python src/q4d.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from gmm import newey_west_s, nw94_lag
from q34_data import VERSIONS, load_q34_version
from sdf import OUTPUT
from tables import long_table, p_text, sample_text

K = 1
J_GRS = 20  # assets 1-20; the factor (asset 21) is excluded


def nw_mean(f: np.ndarray) -> tuple[float, float, int]:
    """Mean of f and its Newey-West standard error (regression on a constant)."""
    u = (f - f.mean())[:, None]
    lag = nw94_lag(u)
    return float(f.mean()), float(np.sqrt(newey_west_s(u, lag)[0, 0] / len(f))), lag


def ts_regression(y: np.ndarray, f: np.ndarray) -> dict:
    """OLS of y on (1, f) with the Newey-West t-stat of the intercept."""
    x = np.column_stack([np.ones_like(f), f])
    coef, *_ = np.linalg.lstsq(x, y, rcond=None)
    eps = y - x @ coef
    h = x * eps[:, None]
    lag = nw94_lag(h)
    q_inv = np.linalg.inv(x.T @ x / len(y))
    avar = q_inv @ newey_west_s(h, lag) @ q_inv / len(y)
    return {"alpha": coef[0], "beta": coef[1], "t_alpha": coef[0] / np.sqrt(avar[0, 0]), "lag": lag, "eps": eps}


def latex_table(res: dict) -> str:
    """Panels A (lambda), B (alphas, BM and MOM side by side), C (GRS test, lags) for each version."""
    keys = list(VERSIONS)
    def lag_range(alphas):
        lags = alphas["nw_lag"].dropna()
        return f"{int(lags.min())}--{int(lags.max())}"
    return long_table(
        "src/q4d.py",
        {"title": "Panel A: Factor risk premium", "header": (r"$\hat{\lambda}$", "s.e."),
         "rows": [(VERSIONS[k], f"{res[k]['lam']['lambda']:.4f}", f"{res[k]['lam']['se']:.4f}") for k in keys]},
        {"title": "Panel B: Pricing errors", "stat": r"$\hat{\alpha}_j$",
         "blocks": [(rf"\textit{{{VERSIONS[k]}}}", res[k]["alphas"]["alpha"].to_numpy(),
                     res[k]["alphas"]["t_alpha"].to_numpy()) for k in keys]},
        {"title": "Panel C: GRS test and Newey--West lags",
         "header": ("GRS", "$p$-value", r"Lag, $\hat{\lambda}$", r"Lags, $\hat{\alpha}_j$"),
         "rows": [(rf"{VERSIONS[k]}, $F({J_GRS}, {res[k]['grs']['df2']})$", f"{res[k]['grs']['stat']:.2f}",
                   p_text(res[k]["grs"]["p"]), str(res[k]["lam"]["lag"]), lag_range(res[k]["alphas"])) for k in keys]},
        [(f"Sample, {VERSIONS[k]}", sample_text(res[k]["months"])) for k in keys],
    )


def run(xr: pd.DataFrame) -> dict:
    f = xr["xR_w"].to_numpy()
    t = len(f)
    lam_hat, lam_se, lam_lag = nw_mean(f)
    rows, resid = [], []
    for j, name in enumerate(xr.columns, start=1):
        if name == "xR_w":
            # The factor regressed on itself: alpha = 0, beta = 1, eps = 0; t-stat undefined.
            rows.append({"j": j, "asset": name, "alpha": 0.0, "beta": 1.0, "t_alpha": np.nan, "nw_lag": np.nan})
            continue
        r = ts_regression(xr[name].to_numpy(), f)
        rows.append({"j": j, "asset": name, "alpha": r["alpha"], "beta": r["beta"],
                     "t_alpha": r["t_alpha"], "nw_lag": r["lag"]})
        resid.append(r["eps"])
    alphas = pd.DataFrame(rows)

    eps = np.column_stack(resid)                       # T x 20
    alpha = alphas["alpha"].to_numpy()[:J_GRS]
    sigma_eps = eps.T @ eps / (t - K - 1)
    sigma_f = np.sum((f - f.mean()) ** 2) / (t - 1)
    df2 = t - J_GRS - K
    stat = df2 / J_GRS / (1 + f.mean() ** 2 / sigma_f) * (alpha @ np.linalg.solve(sigma_eps, alpha))
    return {"lam": {"lambda": lam_hat, "se": lam_se, "lag": lam_lag}, "alphas": alphas,
            "grs": {"stat": float(stat), "df2": df2, "p": float(stats.f.sf(stat, J_GRS, df2))}, "months": xr.index}


def main() -> None:
    res = {k: run(load_q34_version(k)[0]) for k in VERSIONS}

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "version": k, "lambda": r["lam"]["lambda"], "se_lambda": r["lam"]["se"], "nw_lag_lambda": r["lam"]["lag"],
        "grs": r["grs"]["stat"], "grs_df1": J_GRS, "grs_df2": r["grs"]["df2"], "grs_p_value": r["grs"]["p"],
        "sample_start": str(r["months"][0]), "sample_end": str(r["months"][-1]), "T": len(r["months"]),
    } for k, r in res.items()]).to_csv(OUTPUT / "q4d_estimates.csv", index=False, encoding="utf-8")
    pd.concat([r["alphas"].assign(version=k) for k, r in res.items()]).to_csv(
        OUTPUT / "q4d_alphas.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4d_table.tex").write_text(latex_table(res), encoding="utf-8")

    for k, r in res.items():
        print(f"{VERSIONS[k]:11s} {r['months'][0]} to {r['months'][-1]} (T = {len(r['months'])}): "
              f"lambda = {r['lam']['lambda']:.6f} (se {r['lam']['se']:.6f}, lag {r['lam']['lag']}); "
              f"GRS = {r['grs']['stat']:.3f} ~ F({J_GRS}, {r['grs']['df2']}), p = {r['grs']['p']:.3g}")


if __name__ == "__main__":
    main()
