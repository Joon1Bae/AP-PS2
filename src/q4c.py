"""Q4(c): efficient GMM estimates of b in M_t = 1 - b (R_w,t - mu): two-step and iterated.

Implements spec/q4c.md (data, moments and the treatment of mu as in Q4(b)):
- mu_hat = mean(R_w) (moment 22 holds exactly). For a weighting matrix W on the 21 pricing
  moments, b has the closed form (GLS when W = S^-1):
      b(W) = (d'W d)^-1 d'W E[xR],   d = Cov(R_w, xR) (1/T).
- S: Newey-West estimate of the 22-moment S at a given b (Bartlett kernel, NW (1994) automatic
  lag on the sum of all moment series, demeaned, lag rounded down, 1/T; see gmm.py), with its
  lag re-selected every time S is re-estimated. The weighting matrix is the inverse of the
  21 x 21 pricing-moment block.
- Two-step: b_1 = b(I) (Q4(b)); S at b_1; b_2S = b(S_1^-1). No further iteration.
- Iterated: from b_1, repeat S at the current b, b = b(S^-1), until |change in b| < TOL.
- Inference for each estimate: A = [[G_b' W, 0], [0', 1]] with the W that produced it, G at
  that b, and S re-estimated at that b (lag re-selected) in the middle:
      aVar[theta] = (1/T)(AG)^-1 A S A' (AG)^-1',  aVar[E[eps]] = (1/T)[I - G(AG)^-1 A] S [...]'
  t_j = E[eps]_j / sqrt(aVar_jj) from the 21 x 21 pricing block; chi2 with the Moore-Penrose
  pseudo-inverse, 20 d.f.

Outputs (output/):
- q4c_estimates.csv        b, s.e., chi2, p-value, lags and iterations for each estimate
- q4c_pricing_errors.csv   pricing error and t-statistic of each of the 21 moments, per estimate
- q4c_iterations.csv       the path of b and the lag over the iterations
- q4c_table.tex            LaTeX tabular (input by tex/ps2_solution.tex)

Run from the repository root:  uv run python src/q4c.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from gmm import gmm_avar, newey_west_s, nw94_lag
from q34_data import load_q34_sample
from sdf import OUTPUT
from tables import long_table, p_text, sample_text

CHI2_DF = 20   # spec: 21 pricing moments - 1
TOL = 1e-10    # convergence tolerance on |b_{h+1} - b_h| (numerical choice)
MAX_ITER = 1000
ESTIMATES = {"q4b": "4(b), $\\hat{\\mathbf{W}} = \\mathbf{I}$", "two_step": "Two-step", "iterated": "Iterated"}


class Q4Model:
    """Moments, G, and the closed-form b(W) for M_t = 1 - b (R_w,t - mu), mu = mean(R_w)."""

    def __init__(self, xr: pd.DataFrame, r_w: pd.Series):
        self.x = xr.to_numpy()
        self.f = r_w.to_numpy()
        self.t, self.n = self.x.shape
        self.mu = self.f.mean()
        self.mean_x = self.x.mean(axis=0)
        self.d = ((self.f - self.mu)[:, None] * (self.x - self.mean_x)).mean(axis=0)

    def b_of(self, w: np.ndarray) -> float:
        return float(self.d @ w @ self.mean_x / (self.d @ w @ self.d))

    def moments(self, b: float) -> np.ndarray:
        return np.column_stack([(1 - b * (self.f - self.mu))[:, None] * self.x, self.f - self.mu])

    def g(self, b: float) -> np.ndarray:
        g = np.zeros((self.n + 1, 2))
        g[: self.n, 0] = -((self.f - self.mu)[:, None] * self.x).mean(axis=0)
        g[: self.n, 1] = b * self.mean_x
        g[self.n, 1] = -1.0
        return g

    def s_at(self, b: float) -> tuple[np.ndarray, int]:
        """Newey-West S (22 x 22) at b with the automatically selected lag."""
        u = self.moments(b)
        lag = nw94_lag(u)
        return newey_west_s(u, lag), lag

    def weight_at(self, b: float) -> tuple[np.ndarray, int]:
        """W = inverse of the 21 x 21 pricing block of S at b."""
        s, lag = self.s_at(b)
        return np.linalg.inv(s[: self.n, : self.n]), lag

    def inference(self, b: float, w: np.ndarray) -> dict:
        g = self.g(b)
        a = np.zeros((2, self.n + 1))
        a[0, : self.n] = g[: self.n, 0] @ w
        a[1, self.n] = 1.0
        s_mid, lag_mid = self.s_at(b)
        avar_theta, avar_eps = gmm_avar(a, g, s_mid, self.t)
        eps = self.moments(b).mean(axis=0)[: self.n]
        avar_p = avar_eps[: self.n, : self.n]
        chi2 = float(eps @ np.linalg.pinv(avar_p, hermitian=True) @ eps)
        return {"b": b, "se_b": float(np.sqrt(avar_theta[0, 0])), "eps": eps,
                "t_eps": eps / np.sqrt(np.diag(avar_p)), "chi2": chi2,
                "p_chi2": float(stats.chi2.sf(chi2, CHI2_DF)), "lag_sandwich": lag_mid}


def latex_table(res: dict, months: pd.PeriodIndex) -> str:
    """Panels A (b per estimate), B (pricing errors per estimate, BM and MOM side by side), C (tests, lags)."""
    keys = list(ESTIMATES)
    return long_table(
        "src/q4c.py",
        {"title": "Panel A: Parameter estimates", "header": (r"$\hat{b}$", "s.e."),
         "rows": [(ESTIMATES[k], f"{res[k]['b']:.4f}", f"{res[k]['se_b']:.4f}") for k in keys]},
        {"title": "Panel B: Pricing errors", "stat": r"$\widehat{\mathbb{E}}[\epsilon_j]$",
         "blocks": [(rf"\textit{{{ESTIMATES[k]}}}", res[k]["eps"], res[k]["t_eps"]) for k in keys]},
        {"title": "Panel C: Joint test and Newey--West lags",
         "header": (rf"$\chi^2({CHI2_DF})$", "$p$-value", r"Lag, $\hat{\mathbf{W}}$ / sandwich", "Iterations"),
         "rows": [(ESTIMATES[k], f"{res[k]['chi2']:.2f}", p_text(res[k]["p_chi2"]),
                   f"{res[k]['lag_weight']} / {res[k]['lag_sandwich']}",
                   str(res[k]["iterations"]) if "iterations" in res[k] else "--") for k in keys]},
        sample_text(months),
    )


def main() -> None:
    xr, r_w = load_q34_sample()
    model = Q4Model(xr, r_w)
    identity = np.eye(model.n)

    # Q4(b) reference and two-step.
    b_1 = model.b_of(identity)
    w_1, lag_1 = model.weight_at(b_1)
    b_2s = model.b_of(w_1)

    # Iterated, re-selecting the lag each time S is re-estimated.
    b, path, converged = b_1, [], False
    for h in range(1, MAX_ITER + 1):
        w, lag = model.weight_at(b)
        b_new = model.b_of(w)
        path.append({"iteration": h, "b_in": b, "lag": lag, "b_out": b_new})
        if abs(b_new - b) < TOL:
            b, converged = b_new, True
            break
        b = b_new
    if not converged:
        raise RuntimeError(f"Iterated GMM did not converge in {MAX_ITER} iterations.")
    w_iter, lag_iter = w, lag

    res = {
        "q4b": {**model.inference(b_1, identity), "lag_weight": "--"},
        "two_step": {**model.inference(b_2s, w_1), "lag_weight": str(lag_1)},
        "iterated": {**model.inference(b, w_iter), "lag_weight": str(lag_iter), "iterations": len(path)},
    }

    OUTPUT.mkdir(exist_ok=True)
    pd.DataFrame([{
        "estimate": k, "b": r["b"], "se_b": r["se_b"], "chi2": r["chi2"], "chi2_df": CHI2_DF,
        "p_value": r["p_chi2"], "nw_lag_weight": r["lag_weight"], "nw_lag_sandwich": r["lag_sandwich"],
        "iterations": r.get("iterations", ""), "converged": converged if k == "iterated" else "",
        "mu": model.mu, "T": model.t,
    } for k, r in res.items()]).to_csv(OUTPUT / "q4c_estimates.csv", index=False, encoding="utf-8")
    pd.DataFrame({
        "j": range(1, 22), "asset": list(xr.columns),
        **{f"{col}_{k}": res[k][key] for k in res for col, key in (("pricing_error", "eps"), ("t_stat", "t_eps"))},
    }).to_csv(OUTPUT / "q4c_pricing_errors.csv", index=False, encoding="utf-8")
    pd.DataFrame(path).to_csv(OUTPUT / "q4c_iterations.csv", index=False, encoding="utf-8")
    (OUTPUT / "q4c_table.tex").write_text(latex_table(res, xr.index), encoding="utf-8")

    print(f"Sample: {xr.index[0]} to {xr.index[-1]} (T = {model.t} months, N = {model.n} assets)")
    for k, r in res.items():
        print(f"{k:9s} b = {r['b']:.6f}  se = {r['se_b']:.6f}  chi2 = {r['chi2']:.3f}  p = {r['p_chi2']:.3g}  "
              f"lag W/sandwich = {r['lag_weight']}/{r['lag_sandwich']}")
    print(f"iterated: converged = {converged} after {len(path)} iterations; last lags: "
          f"{[p['lag'] for p in path[-5:]]}")


if __name__ == "__main__":
    main()
