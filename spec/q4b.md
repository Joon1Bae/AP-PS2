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
nominal, excess over the 12-month compounded RF). Units: decimals (Ken French percent returns / 100).

The index for the assets: 1 is Lo 10, ..., 10 is Hi 10, 11 is Lo PRIOR, ..., 20 is Hi PRIOR,
and 21 is xR_w.

# Sketch

1. SDF: M_t = 1 − b · (R_w,t − μ), with μ = E[R_w] (normalization E[M] = 1).

2. Moment conditions (22 moments, two parameters θ = (b, μ)):
   E[M_t · xR_j,t] = E[xR_j,t − b · (R_w,t − μ) · xR_j,t] = 0 for j = 1, ..., 21 (pricing moments)
   E[R_w,t − μ] = 0 (moment 22)

3. Estimation (q34_common.md item 9):
   - μ: moment 22 is set exactly to zero, so μ̂ = mean(R_w).
   - b: with the identity weighting matrix on the 21 pricing moments (Ŵ = I), holding μ = μ̂,
     b̂ = (Ĉov[F, xR]′Ĉov[F, xR])⁻¹ Ĉov[F, xR]′Ê[xR] with F = R_w,t, no intercept,
     Ĉov = (1/T) Σ_{t=1}^{T} (F_t − F̄)(xR_t − x̄R).
     This is the OLS coefficient of a regression of Ê[xR_j] onto Ĉov[xR_j, R_w] for j = 1, ..., 21.
   - Together, this is a GMM with the block matrix A (2 × 22):
     A = [ Ĝ_b′  0 ]   (row for b: Ĝ_b′ is the 1 × 21 derivative of the pricing moments w.r.t. b)
         [ 0′    1 ]   (row for μ: picks moment 22)

4. Estimate S (22 × 22) with Newey and West (1987, 1994) and use it in the asymptotic variance:
   aVar[θ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′, with θ = (b, μ).
   G (22 × 2) includes ∂g_j/∂μ = b · Ê[xR_j] and ∂(R_w − μ)/∂μ = −1.

5. Pricing errors and joint test (slides 2.8 and 2.10):
   - Pricing errors: Ê[ε(θ̂)]_j for j = 1, ..., 21.
   - aVar[Ê[ε]] = (1/T)[I − G(AG)⁻¹A] S [I − G(AG)⁻¹A]′, using the same S as in Sketch 4;
     use its 21 × 21 pricing-moment block (rank 20).

# Output

1. The estimated value of b.
2. Its standard error, based on the Newey-West (1987, 1994) estimate of S.
3. The pricing errors Ê[ε]_j for the 21 pricing moments.
   Each one's t-stat, Ê[ε]_j / √aVar_jj.
4. The χ² test on all 21 pricing moments jointly, using the Moore–Penrose pseudo-inverse
   with 20 degrees of freedom, and its p-value.

# Additional Decisions

1. Refer to q34_common.md for the data alignment (items 1-5), the sample period (item 6),
   the Newey-West details (item 8), and the treatment of μ (item 9).
2. Sample: use the months where all 21 excess returns and R_w are available
   (1928-06 to 2021-12, q34_common.md item 6).
3. Newey-West: automatic NW 1994 lag selection; (1) Bartlett kernel, (2) lag chosen from the
   equally weighted sum of all moment series, (3) moment series demeaned before building S,
   (4) selected lag rounded down, (5) 1/T divisor in Ω̂_ℓ (q34_common.md item 8).
4. Ĝ_b: analytical derivative, consistent with q3b.md, q3c.md, and q3e.md.
