"""Shared pieces for Question 2: excess returns, the SDF M* = a - b'xR, and the b scatterplot."""

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
logging.getLogger("fontTools").setLevel(logging.ERROR)  # harmless font-timestamp warnings on PDF export
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from french_data import MISSING_CODES, read_french_block

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

# Chart colors: one series on a light print surface.
SERIES = "#2a78d6"
SURFACE = "#ffffff"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
ZERO_LINE = "#9a9893"


def load_excess_returns(
    file_name: str, title: str, columns: list[str], sample_start: pd.Period
) -> pd.DataFrame:
    """Monthly excess returns xR = (R_p - RF) / 100 (decimal units) from sample_start on.

    R_p are the given columns of the titled table in data/<file_name>; RF is from the
    monthly table of F-F_Research_Data_Factors.csv.
    """
    rf = read_french_block(DATA / "F-F_Research_Data_Factors.csv")["RF"]
    returns = read_french_block(DATA / file_name, title=title)[columns]
    returns = returns.loc[sample_start:]

    # The specs have no missing-data rule, so stop instead of silently handling gaps.
    if returns.isin(MISSING_CODES).any().any() or returns.isna().any().any():
        raise ValueError(f"Missing values in {file_name}; the spec needs a rule for them.")
    months_without_rf = returns.index.difference(rf.index)
    if len(months_without_rf):
        raise ValueError(f"RF is missing for {len(months_without_rf)} sample months.")

    return returns.sub(rf.loc[returns.index], axis=0) / 100.0


def solve_sdf(xr: pd.DataFrame) -> tuple[float, pd.Series]:
    """Solve the specs' two moment equations jointly for a and b (sample moments).

        a - b' E[xR] = 1              (normalization E[M*] = 1)
        a E[xR] - E[xR xR'] b = 0     (E[M* xR] = 0 for each portfolio)
    """
    x = xr.to_numpy()
    t, n = x.shape
    mean_xr = x.mean(axis=0)
    second_moment = x.T @ x / t

    # Unknowns (a, b_1, ..., b_n). Row 0: a - b'E[xR] = 1. Rows 1..n: a E[xR] - E[xR xR'] b = 0.
    lhs = np.zeros((n + 1, n + 1))
    lhs[0, 0] = 1.0
    lhs[0, 1:] = -mean_xr
    lhs[1:, 0] = mean_xr
    lhs[1:, 1:] = -second_moment
    rhs = np.zeros(n + 1)
    rhs[0] = 1.0

    solution = np.linalg.solve(lhs, rhs)
    return solution[0], pd.Series(solution[1:], index=xr.columns, name="b")


def sdf_series(xr: pd.DataFrame, a: float, b: pd.Series) -> pd.Series:
    """Time series M*_t = a - b'xR_t."""
    return pd.Series(a - xr.to_numpy() @ b.to_numpy(), index=xr.index, name="M*")


def pricing_errors(xr: pd.DataFrame, m: pd.Series) -> pd.Series:
    """alpha_j = E[xR_j] - Cov(-M, xR_j) for each column j, with time averages (Cov divides by T)."""
    x = xr.to_numpy()
    neg_m = -m.to_numpy()
    cov = ((neg_m - neg_m.mean())[:, None] * (x - x.mean(axis=0))).mean(axis=0)
    return pd.Series(x.mean(axis=0) - cov, index=xr.columns, name="alpha")


def sharpe_ratio(xr: pd.DataFrame, b: pd.Series) -> float:
    """Sharpe ratio E[xR*] / sigma(xR*) of xR* = b'xR, with time averages (sigma divides by T)."""
    x_star = xr.to_numpy() @ b.to_numpy()
    return x_star.mean() / x_star.std(ddof=0)


def save_coefficients(a: float, b: pd.Series, path: Path) -> None:
    coefficients = pd.DataFrame({
        "parameter": ["a"] + ["b"] * len(b),
        "decile": [pd.NA] + list(range(1, len(b) + 1)),
        "portfolio": [pd.NA] + list(b.index),
        "value": [a] + list(b.to_numpy()),
    })
    coefficients.to_csv(path, index=False, encoding="utf-8")


def plot_b(b: pd.Series, path: Path, xlabel: str) -> None:
    """Scatterplot of b (y-axis) against portfolio decile 1..10 (x-axis)."""
    plot_b_groups([(b, SERIES, "o", None)], path, xlabel)


def plot_b_groups(
    groups: list[tuple[pd.Series, str, str, str | None]], path: Path, xlabel: str
) -> None:
    """Scatterplot of b against decile 1..10 for one or more sorts.

    Each group is (b, color, marker, legend label); a legend is drawn when labels are given.
    """
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["cmr10"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "pdf.fonttype": 42,
    })
    n = len(groups[0][0])
    deciles = np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.axhline(0.0, color=ZERO_LINE, linewidth=0.8, zorder=1)
    for b, color, marker, label in groups:
        ax.scatter(
            deciles, b.to_numpy(), s=48, color=color, marker=marker,
            edgecolors=SURFACE, linewidths=1.5, zorder=3, label=label,
        )
    if any(label for *_, label in groups):
        ax.legend(frameon=False, labelcolor=TEXT_PRIMARY, loc="best")

    ax.set_xticks(deciles)
    ax.set_xlim(0.5, n + 0.5)
    ax.set_xlabel(xlabel, color=TEXT_PRIMARY)
    ax.set_ylabel("$b$ coefficient", color=TEXT_PRIMARY)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TEXT_SECONDARY, length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.set_facecolor(SURFACE)

    fig.tight_layout()
    fig.savefig(path, metadata={"CreationDate": None})  # no timestamp: reruns give identical files
    plt.close(fig)


def print_summary(xr: pd.DataFrame, a: float, b: pd.Series) -> None:
    """Print the estimates and check that the sample moment conditions hold (ASCII only)."""
    sdf = sdf_series(xr, a, b).to_numpy()
    pricing_errors = (sdf[:, None] * xr.to_numpy()).mean(axis=0)
    print(f"Sample: {xr.index[0]} to {xr.index[-1]} (T = {len(xr)} months)")
    print(f"a = {a:.6f}")
    for name, value in b.items():
        print(f"b[{name}] = {value:.6f}")
    print(f"Check: sample mean of M* = {sdf.mean():.12f}")
    print(f"Check: max |sample E[M* xR]| = {np.abs(pricing_errors).max():.3e}")
