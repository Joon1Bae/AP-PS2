"""Q2(b): SDF M* = a - b'xR that prices the excess returns of the 10 momentum deciles.

Implements spec/q2b.md:
- Data: RF from F-F_Research_Data_Factors.csv; "Lo PRIOR" ... "Hi PRIOR" from the
  monthly value-weighted block of 10_Portfolios_Prior_12_2.csv.
- Sample: July 1927 to the latest month in the data.
- xR = (R_p - RF) / 100, i.e. excess returns in decimal units.
- (a, b) solve the two sample-moment equations of the spec (E[.] = time average):
      a - b' E[xR] = 1              (normalization E[M*] = 1)
      a E[xR] - E[xR xR'] b = 0     (E[M* xR] = 0 for each decile)

Outputs (output/):
- q2b_b_scatter.pdf         scatterplot of b by momentum decile
- q2b_sdf_coefficients.csv  estimated a and b

Run from the repository root:  uv run python src/q2b.py
"""

import pandas as pd

from sdf import OUTPUT, load_excess_returns, plot_b, print_summary, save_coefficients, solve_sdf

DECILES = [
    "Lo PRIOR", "PRIOR 2", "PRIOR 3", "PRIOR 4", "PRIOR 5",
    "PRIOR 6", "PRIOR 7", "PRIOR 8", "PRIOR 9", "Hi PRIOR",
]
SAMPLE_START = pd.Period("1927-07", freq="M")


def load_mom_excess_returns() -> pd.DataFrame:
    """Monthly decimal excess returns of the 10 value-weighted momentum deciles."""
    return load_excess_returns(
        "10_Portfolios_Prior_12_2.csv", "Value Weight Returns -- Monthly", DECILES, SAMPLE_START
    )


def main() -> None:
    xr = load_mom_excess_returns()
    a, b = solve_sdf(xr)

    OUTPUT.mkdir(exist_ok=True)
    save_coefficients(a, b, OUTPUT / "q2b_sdf_coefficients.csv")
    plot_b(b, OUTPUT / "q2b_b_scatter.pdf", xlabel="Momentum decile (1 = Lo PRIOR, 10 = Hi PRIOR)")
    print_summary(xr, a, b)


if __name__ == "__main__":
    main()
