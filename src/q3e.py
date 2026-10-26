"""Q3(e): GMM estimate of gamma from E[R_w,t^-gamma xR_j,t] = 0 for 21 assets, W = I.

Implements spec/q3e.md:
- Assets (spec/q34_common.md items 1-5): j = 1..20 trailing 12-month BE/ME and momentum decile
  excess returns (French data, value-weighted, decimals, nominal), j = 21 xR_w = exp(re) - exp(rf);
  R_w = exp(re). Sample Dec 1940 - Dec 2021 (item 6); z is not used (item 7).
- Moments u_j,t = R_w,t^-gamma xR_j,t (21), parameter gamma (1). gamma solves G' E[u] = 0
  (W = I, A = G') with the analytical G_j = -E[ln(R_w) u_j]; same estimator as Q3(c).
- S: Newey-West (see gmm.py). aVar[gamma] = (1/T)(AG)^-1 A S A' (AG)^-1';
  aVar[E[eps]] = (1/T)[I - G(AG)^-1 A] S [I - G(AG)^-1 A]' (rank 20);
  t_j = E[eps]_j / sqrt(aVar_jj); chi2 = E[eps]' aVar^+ E[eps] (Moore-Penrose), 20 d.f.

Outputs (output/):
- q3e_gamma_estimate.csv   gamma, its standard error, the NW lag, chi2 and p-value
- q3e_pricing_errors.csv   pricing error and t-statistic of each of the 21 moments
- q3e_table.tex            LaTeX tabular (input by tex/ps2_solution.tex)

Run from the repository root:  uv run python src/q3e.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from gmm import gmm_avar, newey_west_s, nw94_lag
from q34_data import Q3_SAMPLE_START, SAMPLE_END, load_q34_sample
from q3c import estimate_gamma, g_hat, moments
from sdf import OUTPUT
from tables import long_table, p_text, sample_text

CHI2_DF = 20  # spec: 21 moments - 1 parameter


def latex_table(res: dict, months: pd.PeriodIndex) -> str:
    """Panels A (gamma), B (pricing errors, BM and MOM side by side), C (chi2 test, lag, sample)."""
    return long_table(
        "src/q3e.py",
        {"title": "Panel A: Parameter estimate", "header": ("Estimate", "s.e."),
         "rows": [(r"$\hat{\gamma}$", f"{res['gamma']:.4f}", f"{res['se']:.4f}")]},
        {"title": "Panel B: Pricing errors", "stat": r"$\widehat{\mathbb{E}}[\epsilon_j]$",
         "blocks": [(None, res["eps"], res["t_eps"])]},
        {"title": "Panel C: Joint test", "header": (rf"$\chi^2({CHI2_DF})$", "$p$-value", "Newey--West lag", ""),
         "rows": [("", f"{res['chi2']:.2f}", p_text(res["p_chi2"]), str(res["lag"]), "")]},
        sample_text(months),
    )


def main() -> None:
    xr_all, r_w_all = load_q34_sample()
    xr = xr_all.loc[Q3_SAMPLE_START:SAMPLE_END]
    if not xr.index.equals(pd.period_range(Q3_SAMPLE_START, SAMPLE_END, freq="M")):
        raise ValueError("The Question 3 sample is incomplete.")
    r_w = r_w_all.loc[xr.index].to_numpy()
    x = xr.to_numpy()
    t = len(xr)

    gamma = estimate_gamma(r_w, x)
    u = moments(gamma, r_w, x)
    g = g_hat(gamma, r_w, x)[:, None]
    lag = nw94_lag(u)
    avar_gamma, avar_eps = gmm_avar(g.T, g, newey_west_s(u, lag), t)

    e = u.mean(axis=0)
    t_eps = e / np.sqrt(np.diag(avar_eps))
    chi2 = float(e @ np.linalg.pinv(avar_eps, hermitian=True) @ e)
    res = {"gamma": gamma, "se": float(np.sqrt(avar_gamma[0, 0])), "lag": lag, "eps": e, "t_eps": t_eps,
           "chi2": chi2, "p_chi2": float(stats.chi2.sf(chi2, CHI2_DF))}

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "gamma": gamma, "se_gamma": res["se"], "nw_lag": lag,
        "chi2": chi2, "chi2_df": CHI2_DF, "p_value": res["p_chi2"],
        "sample_start": str(xr.index[0]), "sample_end": str(xr.index[-1]), "T": t,
    }]).to_csv(OUTPUT / "q3e_gamma_estimate.csv", index=False, encoding="utf-8")
    pd.DataFrame({
        "j": range(1, 22), "asset": list(xr.columns), "pricing_error": e, "t_stat": t_eps,
    }).to_csv(OUTPUT / "q3e_pricing_errors.csv", index=False, encoding="utf-8")
    (OUTPUT / "q3e_table.tex").write_text(latex_table(res, xr.index), encoding="utf-8")

    print(f"Sample: {xr.index[0]} to {xr.index[-1]} (T = {t} months, N = {x.shape[1]} assets)")
    print(f"gamma = {gamma:.6f} (se {res['se']:.6f}, NW lag {lag})")
    print(f"chi2({CHI2_DF}) = {chi2:.4f}, p = {res['p_chi2']:.4g}; "
          f"smallest eigenvalues of aVar[E[eps]]: {np.linalg.eigvalsh(avar_eps)[:2]}")
    for name, ee, tt in zip(xr.columns, e, t_eps):
        print(f"  {name:10s} {ee: .5f}  t = {tt: .2f}")


if __name__ == "__main__":
    main()
