# Data
1. re and rf columns from EQ Dataset.csv
2. RF column from F-F_Research_Data_Factors.csv
3. From Lo 10 to Hi 10 columns from Portfolios_Formed_on_BE-ME.csv
4. From Lo PRIOR to Hi PRIOR columns from 10_Portfolios_Prior_12_2.csv

# Pre-Processing for EQ Dataset
Please calculate each variable as follows:

xR_w,t = R_w,t - R_f,t where
(1) R_w,t = R_e,t = e^re,t where re is from the EQ Dataset
(2) R_f,t = e^rf,t where rf is from the EQ Dataset

# Pre-Processing for the French portfolios
Compute the 12-month excess returns xR_j,t of the 20 decile portfolios exactly as in
q34_common.md items 2-5 (trailing 12-month gross returns, value-weighted block,
nominal, excess over the 12-month compounded RF).

The index for the assets follows q4b.md: 1 is Lo 10, ..., 10 is Hi 10, 11 is Lo PRIOR, ...,
20 is Hi PRIOR, and 21 is xR_w.

# Sketch

1. Moment conditions (21 moments, one parameter):
   E[R_w,t^(-γ) · xR_j,t] = 0 for j = 1, ..., 21
   (z is not used; see q34_common.md item 7).

2. The weighting matrix is the identity matrix (Ŵ = I), so Â = Ĝ′.
   Find γ̂ that solves Â · Ê[ε(γ̂)] = Ĝ′ · Ê[ε(γ̂)] = 0,
   where Ê[ε(γ)] is the 21 × 1 vector of sample moments and
   Ĝ = Ê[∂γ ε(γ)] (21 × 1) evaluated at γ̂
   (the first-order condition of γ̂ = argmin Ê[ε(γ)]′ Ê[ε(γ)]).

3. Estimate S (21 × 21) with Newey and West (1987, 1994) and use it in the asymptotic variance:
   aVar[γ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′ with A = G′.

4. Pricing errors and joint test (slides 2.8 and 2.10):
   - Pricing errors: Ê[ε(γ̂)]_j for j = 1, ..., 21.
   - aVar[Ê[ε(γ̂)]] = (1/T)[I − G(AG)⁻¹A] S [I − G(AG)⁻¹A]′ with A = G′,
     using the same S as in Sketch 3.
   - This 21 × 21 matrix has rank 20 (Q − K = 21 − 1), so it is singular.

# Output

Same table as q3c.md:
1. The estimated value of γ.
2. Its standard error, based on the Newey-West (1987, 1994) estimate of S.
3. The pricing errors Ê[ε]_j for the 21 moments.
   Each one's t-stat, Ê[ε]_j / √aVar_jj.
4. The χ² test on all 21 moments jointly, using the Moore–Penrose pseudo-inverse
   with 20 degrees of freedom (size(J) − K = 21 − 1), and its p-value.

# Additional Decisions

1. Refer to q34_common.md for the data alignment (items 1-5), the sample period (item 6),
   and the Newey-West details (item 8).
2. Ĝ: analytical derivative, consistent with q3b.md and q3c.md.
3. Sample: 1940-12 to 2021-12 (q34_common.md item 6). Q3(e) does not need z,
   but it uses the same sample as the rest of Question 3.
