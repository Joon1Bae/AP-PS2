"""GMM inference shared by Questions 3 and 4: Newey-West S and the A-matrix formulas.

- S: Bartlett kernel (Newey-West 1987) with the lag chosen by the Newey-West (1994)
  automatic procedure on the equally weighted sum of all moment series; moment series are
  demeaned before building S; the selected lag is rounded down (spec/q4b.md, decision 5).
- aVar[theta] = (1/T) (AG)^-1 A S A' (AG)^-1'
  aVar[E[eps]] = (1/T) [I - G (AG)^-1 A] S [I - G (AG)^-1 A]'
"""

import numpy as np


def nw94_lag(u: np.ndarray) -> int:
    """Newey-West (1994) automatic lag for the Bartlett kernel, rounded down.

    u is the T x N matrix of moment series. The procedure uses f_t = 1'(u_t - ubar) and
    the pre-set initial lag n = floor(4 (T/100)^(2/9)):
        sigma_j = (1/T) sum_t f_t f_t-j,   s0 = sigma_0 + 2 sum_j sigma_j,
        s1 = 2 sum_j j sigma_j,            m = 1.1447 ((s1/s0)^2)^(1/3) T^(1/3).
    """
    t = u.shape[0]
    f = (u - u.mean(axis=0)).sum(axis=1)
    n = int(np.floor(4 * (t / 100) ** (2 / 9)))
    sigma = np.array([f[j:] @ f[: t - j] / t for j in range(n + 1)])
    j = np.arange(1, n + 1)
    s0 = sigma[0] + 2 * sigma[1:].sum()
    s1 = 2 * (j * sigma[1:]).sum()
    m = 1.1447 * ((s1 / s0) ** 2) ** (1 / 3) * t ** (1 / 3)
    return int(np.floor(m))


def newey_west_s(u: np.ndarray, lag: int) -> np.ndarray:
    """S = Gamma_0 + sum_{j=1}^{lag} (1 - j/(lag+1)) (Gamma_j + Gamma_j'), from demeaned u."""
    t = u.shape[0]
    e = u - u.mean(axis=0)
    s = e.T @ e / t
    for j in range(1, lag + 1):
        gamma = e[j:].T @ e[: t - j] / t
        s += (1 - j / (lag + 1)) * (gamma + gamma.T)
    return s


def gmm_avar(a: np.ndarray, g: np.ndarray, s: np.ndarray, t: int) -> tuple[np.ndarray, np.ndarray]:
    """(aVar[theta], aVar[E[eps]]) for the GMM estimate defined by A E[u(theta)] = 0."""
    ag_inv = np.linalg.inv(a @ g)
    avar_theta = ag_inv @ a @ s @ a.T @ ag_inv.T / t
    proj = np.eye(g.shape[0]) - g @ ag_inv @ a
    avar_eps = proj @ s @ proj.T / t
    return avar_theta, avar_eps
