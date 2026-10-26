"""Q4(b): first-stage GMM estimate of b in M_t = 1 - b (R_w,t - E[R_w]).

Implements spec/q4b.md:
- Data: the 21 excess returns of spec/q34_common.md, two samples (item 6): (1) Common Dec 1940 -
  Dec 2021, (2) Max Jun 1928 - Dec 2021: j = 1..20 trailing
  12-month BE/ME and momentum decile excess returns (French data, decimals), j = 21
  xR_w = exp(re) - exp(rf); F = R_w = exp(re) (EQ Dataset).
- Parameters theta = (b, mu), mu = E[R_w]. Moments (22):
      u_j,t   = (1 - b (R_w,t - mu)) xR_j,t   j = 1..21 (pricing moments)
      u_22,t  = R_w,t - mu
  mu moment satisfied exactly (mu = mean R_w); b with identity weights on the pricing moments:
      d = Cov(F, xR) (dividing by T),   b = (d'd)^-1 d' E[xR].
  This is A E[u] = 0 with A = [[G_b', 0], [0', 1]] (2 x 22), G_b = dE[u_1..21]/db = -d at mu = mean R_w.
- G = dE[u]/dtheta': dg_j/db = -E[(R_w - mu) xR_j], dg_j/dmu = b E[xR_j], dg_22/dmu = -1.
- S: Newey-West, Bartlett kernel, NW (1994) automatic lag (see gmm.py).
- aVar[theta] and aVar[E[eps]] from the A-form formulas; t_j = E[eps]_j / sqrt(aVar_jj);
  chi-squared test on all 21 pricing moments: E[eps]' aVar^+ E[eps] (Moore-Penrose
  pseudo-inverse), 20 degrees of freedom.

Outputs (output/):
- q4b_b_estimate.csv     b, its standard error, mu, the NW lag, chi2 statistic and p-value
- q4b_pricing_errors.csv pricing error and t-statistic of each of the 21 pricing moments
- q4b_table.tex          the same as a LaTeX tabular (input by tex/ps2_solution.tex)

Run from the repository root:  uv run python src/q4b.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from gmm import gmm_avar, newey_west_s, nw94_lag
from q34_data import VERSIONS, load_q34_version
from sdf import OUTPUT
from tables import long_table, p_text, sample_text

CHI2_DF = 20  # spec: 21 pricing moments - 1


def estimate(xr: pd.DataFrame, r_w: pd.Series) -> dict:
    x = xr.to_numpy()
    f = r_w.to_numpy()
    t, n = x.shape

    mu = f.mean()
    mean_x = x.mean(axis=0)
    d = ((f - mu)[:, None] * (x - mean_x)).mean(axis=0)
    b = d @ mean_x / (d @ d)

    u = np.column_stack([(1 - b * (f - mu))[:, None] * x, f - mu])
    g = np.zeros((n + 1, 2))
    g[:n, 0] = -((f - mu)[:, None] * x).mean(axis=0)
    g[:n, 1] = b * mean_x
    g[n, 1] = -1.0
    a = np.zeros((2, n + 1))
    a[0, :n] = g[:n, 0]  # G_b' (spec Sketch 3)
    a[1, n] = 1.0

    lag = nw94_lag(u)
    s = newey_west_s(u, lag)
    avar_theta, avar_eps = gmm_avar(a, g, s, t)

    eps = u.mean(axis=0)[:n]
    avar_p = avar_eps[:n, :n]
    chi2 = eps @ np.linalg.pinv(avar_p, hermitian=True) @ eps
    return {
        "b": b, "se_b": np.sqrt(avar_theta[0, 0]), "mu": mu, "lag": lag, "T": t,
        "eps": eps, "t_eps": eps / np.sqrt(np.diag(avar_p)),
        "chi2": chi2, "p_chi2": stats.chi2.sf(chi2, CHI2_DF),
        "eig_avar_p": np.linalg.eigvalsh(avar_p),
    }


def fmt(value: float, digits: int) -> str:
    """Fixed decimals with a typeset minus sign; a value that rounds to zero has no sign."""
    text = f"{value:.{digits}f}"
    if float(text) == 0:
        return text.lstrip("-")
    return text.replace("-", "$-$")


def latex_table(res: dict) -> str:
    """Panels A (b), B (pricing errors, BM and MOM side by side), C (chi2 test, lag) for each version."""
    keys = list(VERSIONS)
    return long_table(
        "src/q4b.py",
        {"title": "Panel A: Parameter estimate", "header": (r"$\hat{b}$", "s.e."),
         "rows": [(VERSIONS[k], f"{res[k]['b']:.4f}", f"{res[k]['se_b']:.4f}") for k in keys]},
        {"title": "Panel B: Pricing errors", "stat": r"$\widehat{\mathbb{E}}[\epsilon_j]$",
         "blocks": [(rf"\textit{{{VERSIONS[k]}}}", res[k]["eps"], res[k]["t_eps"]) for k in keys]},
        {"title": "Panel C: Joint test", "header": (rf"$\chi^2({CHI2_DF})$", "$p$-value", "Newey--West lag", "$T$"),
         "rows": [(VERSIONS[k], f"{res[k]['chi2']:.2f}", p_text(res[k]["p_chi2"]), str(res[k]["lag"]),
                   str(res[k]["T"])) for k in keys]},
        [(f"Sample, {VERSIONS[k]}", sample_text(res[k]["months"])) for k in keys],
    )


def main() -> None:
    res = {}
    for k in VERSIONS:
        xr, r_w = load_q34_version(k)
        res[k] = {**estimate(xr, r_w), "months": xr.index, "assets": list(xr.columns)}

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "version": k, "b": r["b"], "se_b": r["se_b"], "mu": r["mu"], "nw_lag": r["lag"],
        "chi2": r["chi2"], "chi2_df": CHI2_DF, "p_value": r["p_chi2"],
        "sample_start": str(r["months"][0]), "sample_end": str(r["months"][-1]), "T": r["T"],
    } for k, r in res.items()]).to_csv(OUTPUT / "q4b_b_estimate.csv", index=False, encoding="utf-8")
    pd.concat([pd.DataFrame({"version": k, "j": range(1, 22), "asset": r["assets"],
                             "pricing_error": r["eps"], "t_stat": r["t_eps"]}) for k, r in res.items()]
              ).to_csv(OUTPUT / "q4b_pricing_errors.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4b_table.tex").write_text(latex_table(res), encoding="utf-8")

    for k, r in res.items():
        print(f"{VERSIONS[k]:11s} {r['months'][0]} to {r['months'][-1]} (T = {r['T']}): b = {r['b']:.6f} "
              f"(se {r['se_b']:.6f}, mu {r['mu']:.6f}, NW lag {r['lag']}); chi2({CHI2_DF}) = {r['chi2']:.3f}, "
              f"p = {r['p_chi2']:.3g}; smallest eig {r['eig_avar_p'][:2]}")


if __name__ == "__main__":
    main()
