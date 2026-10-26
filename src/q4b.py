"""Q4(b): first-stage GMM estimate of b in M_t = 1 - b (R_w,t - E[R_w]).

Implements spec/q4b.md:
- Data: the 21 excess returns of spec/q34_common.md, Jun 1928 - Dec 2021: j = 1..20 trailing
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
from q34_data import load_q34_sample
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


def latex_table(res: dict, labels: list[str], months: pd.PeriodIndex) -> str:
    """Panels A (b), B (pricing errors, BM and MOM side by side), C (chi2 test, lag, sample)."""
    return long_table(
        "src/q4b.py",
        {"title": "Panel A: Parameter estimate", "header": ("Estimate", "s.e."),
         "rows": [(r"$\hat{b}$", f"{res['b']:.4f}", f"{res['se_b']:.4f}")]},
        {"title": "Panel B: Pricing errors", "stat": r"$\widehat{\mathbb{E}}[\epsilon_j]$",
         "blocks": [(None, res["eps"], res["t_eps"])]},
        {"title": "Panel C: Joint test", "header": (rf"$\chi^2({CHI2_DF})$", "$p$-value", "Newey--West lag", ""),
         "rows": [("", f"{res['chi2']:.2f}", p_text(res["p_chi2"]), str(res["lag"]), "")]},
        sample_text(months),
    )


def main() -> None:
    xr, r_w = load_q34_sample()
    res = estimate(xr, r_w)

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "b": res["b"], "se_b": res["se_b"], "mu": res["mu"], "nw_lag": res["lag"],
        "chi2": res["chi2"], "chi2_df": CHI2_DF, "p_value": res["p_chi2"],
        "sample_start": str(xr.index[0]), "sample_end": str(xr.index[-1]), "T": res["T"],
    }]).to_csv(OUTPUT / "q4b_b_estimate.csv", index=False, encoding="utf-8")
    pd.DataFrame({
        "j": range(1, 22), "asset": list(xr.columns),
        "pricing_error": res["eps"], "t_stat": res["t_eps"],
    }).to_csv(OUTPUT / "q4b_pricing_errors.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4b_table.tex").write_text(latex_table(res, list(xr.columns), xr.index), encoding="utf-8")

    print(f"Sample: {xr.index[0]} to {xr.index[-1]} (T = {res['T']} months, N = {xr.shape[1]} assets)")
    print(f"b = {res['b']:.6f}  se = {res['se_b']:.6f}  mu = {res['mu']:.6f}  NW lag = {res['lag']}")
    print(f"chi2({CHI2_DF}) = {res['chi2']:.4f}  p = {res['p_chi2']:.4g}")
    print("Eigenvalues of aVar[E[eps]] (pricing block), smallest 3:", res["eig_avar_p"][:3])
    for name, e, tt in zip(xr.columns, res["eps"], res["t_eps"]):
        print(f"  {name:10s} {e: .5f}  t = {tt: .2f}")


if __name__ == "__main__":
    main()
