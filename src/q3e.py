"""Q3(e): GMM estimate of gamma from E[R_w,t^-gamma xR_j,t] = 0 for 21 assets, W = I.

Implements spec/q3e.md:
- Assets (spec/q34_common.md items 1-5): j = 1..20 trailing 12-month BE/ME and momentum decile
  excess returns (French data, value-weighted, decimals, nominal), j = 21 xR_w = exp(re) - exp(rf);
  R_w = exp(re). Two samples (item 6): (1) Common Dec 1940 - Dec 2021, (2) Max Jun 1928 -
  Dec 2021; z is not used (item 7).
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
from q34_data import VERSIONS, load_q34_version
from q3c import estimate_gamma, g_hat, moments
from sdf import OUTPUT
from tables import long_table, p_text, sample_text

CHI2_DF = 20  # spec: 21 moments - 1 parameter


def latex_table(res: dict) -> str:
    """Panels A (gamma), B (pricing errors, BM and MOM side by side), C (chi2 test, lag) for each version."""
    keys = list(VERSIONS)
    return long_table(
        "src/q3e.py",
        {"title": "Panel A: Parameter estimate", "header": (r"$\hat{\gamma}$", "s.e."),
         "rows": [(VERSIONS[k], f"{res[k]['gamma']:.4f}", f"{res[k]['se']:.4f}") for k in keys]},
        {"title": "Panel B: Pricing errors", "stat": r"$\widehat{\mathbb{E}}[\epsilon_j]$",
         "blocks": [(rf"\textit{{{VERSIONS[k]}}}", res[k]["eps"], res[k]["t_eps"]) for k in keys]},
        {"title": "Panel C: Joint test", "header": (rf"$\chi^2({CHI2_DF})$", "$p$-value", "Newey--West lag", "$T$"),
         "rows": [(VERSIONS[k], f"{res[k]['chi2']:.2f}", p_text(res[k]["p_chi2"]), str(res[k]["lag"]),
                   str(len(res[k]["months"]))) for k in keys]},
        [(f"Sample, {VERSIONS[k]}", sample_text(res[k]["months"])) for k in keys],
    )


def run(xr: pd.DataFrame, r_w: pd.Series) -> dict:
    r = r_w.to_numpy()
    x = xr.to_numpy()
    gamma = estimate_gamma(r, x)
    u = moments(gamma, r, x)
    g = g_hat(gamma, r, x)[:, None]
    lag = nw94_lag(u)
    avar_gamma, avar_eps = gmm_avar(g.T, g, newey_west_s(u, lag), len(xr))
    e = u.mean(axis=0)
    chi2 = float(e @ np.linalg.pinv(avar_eps, hermitian=True) @ e)
    return {"gamma": gamma, "se": float(np.sqrt(avar_gamma[0, 0])), "lag": lag, "eps": e,
            "t_eps": e / np.sqrt(np.diag(avar_eps)), "chi2": chi2, "p_chi2": float(stats.chi2.sf(chi2, CHI2_DF)),
            "months": xr.index, "assets": list(xr.columns)}


def main() -> None:
    res = {k: run(*load_q34_version(k)) for k in VERSIONS}

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "version": k, "gamma": r["gamma"], "se_gamma": r["se"], "nw_lag": r["lag"],
        "chi2": r["chi2"], "chi2_df": CHI2_DF, "p_value": r["p_chi2"],
        "sample_start": str(r["months"][0]), "sample_end": str(r["months"][-1]), "T": len(r["months"]),
    } for k, r in res.items()]).to_csv(OUTPUT / "q3e_gamma_estimate.csv", index=False, encoding="utf-8")
    pd.concat([pd.DataFrame({"version": k, "j": range(1, 22), "asset": r["assets"],
                             "pricing_error": r["eps"], "t_stat": r["t_eps"]}) for k, r in res.items()]
              ).to_csv(OUTPUT / "q3e_pricing_errors.csv", index=False, encoding="utf-8")
    (OUTPUT / "q3e_table.tex").write_text(latex_table(res), encoding="utf-8")

    for k, r in res.items():
        print(f"{VERSIONS[k]:11s} {r['months'][0]} to {r['months'][-1]} (T = {len(r['months'])}): "
              f"gamma = {r['gamma']:.6f} (se {r['se']:.6f}, NW lag {r['lag']}); "
              f"chi2({CHI2_DF}) = {r['chi2']:.3f}, p = {r['p_chi2']:.3g}")


if __name__ == "__main__":
    main()
