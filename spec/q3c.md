# Data
1. re, rf, dp, and dg columns from EQ Dataset.csv

# Pre-Processing for EQ Dataset
Please calculate each variable as follows:

xR_w,t = R_w,t - R_f,t where
(1) R_w,t = R_e,t = e^re,t where re is from the EQ Dataset
(2) R_f,t = e^rf,t where rf is from the EQ Dataset

# Pre-Processing for the instrument z
Please calculate each variable as follows:

z_t = Ê^OS_t[xR_e] / σ²_e where
(1) Ê^OS_t[xR_e] is the out-of-sample forecast from Problem Set 1 (2e), computed exactly as in q2e_PS1.md: Ê^OS_t[xR_e] = (G_t − 1) + G_t · D_t/P_t
(2) σ²_e is the unconditional variance of R_e,t over the sample
    - Variance of R_e: σ²_e is computed with the 1/(T−1) divisor.

# Sketch

1. Moment conditions (two moments, one parameter):
   E[R_w,t^(-γ) · xR_w,t] = 0
   E[R_w,t^(-γ) · (z_{t-1} · xR_w,t)] = 0

2. The weighting matrix is the identity matrix (Ŵ = I), so Â = Ĝ′.
   Find γ̂ that solves Â · Ê[ε(γ̂)] = Ĝ′ · Ê[ε(γ̂)] = 0,
   where Ê[ε(γ)] is the 2 × 1 vector of sample moments and
   Ĝ = Ê[∂γ ε(γ)] (2 × 1) evaluated at γ̂
   (the first-order condition of γ̂ = argmin Ê[ε(γ)]′ Ê[ε(γ)]).

3. Estimate S (2 × 2) with Newey and West (1987, 1994) and use it in the asymptotic variance: aVar[γ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′ with A = G′.
    - Newey–West: Bartlett kernel, moment series demeaned before building S, and the selected lag rounded down (same as Q3(b) and Q4(b)).

# Output

1. The estimated value of γ.
2. Its standard error, based on the Newey-West (1987, 1994) estimate of S.
(Pricing errors and the χ² test are skipped for now.)

# Additional Decisions

1. Refer to q34_common.md for the timing of z_{t-1} (item 7) and the Newey-West lag selection (item 8).
2. Ĝ: analytical derivative, consistent with q3b.md.
3. Sample: 1940-12 to 2021-12 (q34_common.md item 6), the first t at which z_{t-1} (month t-12 value, item 7) exists.
4. "Over the sample" when calculating σ²_e: the Q3(c) estimation sample.
