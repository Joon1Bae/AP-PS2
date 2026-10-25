# Data
Same as q4b.md (EQ Dataset, Fama/French 3 Factors RF, BM and MOM decile portfolios).

# Pre-Processing
Same as q4b.md: xR_w,t, the 20 portfolio excess returns, and the asset index
(1-10: Lo 10 to Hi 10, 11-20: Lo PRIOR to Hi PRIOR, 21: xR_w).

# Sketch

1. SDF, moment conditions, and the treatment of μ: same as q4b.md (Sketch 1-3).
   - μ̂ = mean(R_w) (moment 22 set exactly to zero, q34_common.md item 9).
   - The efficient weighting applies only to the 21 pricing moments: Ŵ = Ŝ⁻¹, where Ŝ is the
     21 × 21 pricing-moment block of the Newey-West estimate.
   - For any given Ŵ, b̂ has the closed form (GLS when Ŵ = Ŝ⁻¹):
     b̂(Ŵ) = (d′Ŵd)⁻¹ d′Ŵ Ê[xR], with d = Ĉov[R_w, xR] (1/T, as in q4b.md).

2. Two-step efficient GMM (slide 2.6, method 1):
   - Step 1: b̂_1 = b̂(I), i.e., the Q4(b) estimate.
   - Estimate Ŝ at b̂_1 (Newey-West, q34_common.md item 8).
   - Step 2: b̂_2S = b̂(Ŝ⁻¹), using the closed form above. Do not iterate further.

3. Iterated efficient GMM (slide 2.6, method 2):
   - Start from b̂_1 = b̂(I).
   - Repeat: estimate Ŝ at the current b̂, then update b̂ = b̂(Ŝ⁻¹),
     until |b̂_{h+1} − b̂_h| < tolerance.
   - Report the number of iterations and whether it converged.

4. Standard errors and pricing errors for 2 and 3: general sandwich formulas from q4b.md
   (Sketch 4-5), with the block matrix
   A = [ Ĝ_b′ Ŵ  0 ]
       [ 0′      1 ]
   where Ŵ is the weighting matrix used to obtain that estimate.
   - aVar[θ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′, with θ = (b, μ).
   - Pricing errors: Ê[ε(θ̂)]_j for j = 1, ..., 21, evaluated at that estimate's b̂.
   - aVar[Ê[ε]] = (1/T)[I − G(AG)⁻¹A] S [I − G(AG)⁻¹A]′, using the same S as for aVar[θ̂];
     use its 21 × 21 pricing-moment block (rank 20) for the t-stats and the χ² test.

# Output

One table with a column for each estimate: Q4(b) (Ŵ = I, for reference), two-step,
and iterated. For each column:
1. The estimated value of b.
2. Its standard error, based on the Newey-West (1987, 1994) estimate of S.
3. The pricing errors Ê[ε]_j for the 21 pricing moments and each one's t-stat, Ê[ε]_j / √aVar_jj.
4. The χ² test on all 21 pricing moments jointly, using the Moore–Penrose pseudo-inverse
   with 20 degrees of freedom, and its p-value.
5. The selected Newey-West lag(s) and, for the iterated estimate, the number of iterations.

# Additional Decisions

1. Refer to q34_common.md for the data alignment (items 1-5), the sample period (item 6),
   the Newey-West details (item 8), and the treatment of μ (item 9).
2. Ĝ_b: analytical derivative, consistent with q4b.md.
3. "Analytical expression" in the problem: read as the closed form b̂(Ŵ) in Sketch 1 with
   Ŵ = Ŝ⁻¹ (GLS), so no numerical optimization is needed. The slide 3.6 special case
   (b = Σ_F⁻¹E[F]) is not used: its conditions do not hold here (the factor R_w is not
   itself an excess return in xR, and Ŝ differs from Ĉov[xR]).
4. Lag rule for the iterated estimate: re-select the lag with the NW (1994) automatic rule
   every time Ŝ is re-estimated (q34_common.md item 8). Report the lag at convergence and
   check that b̂ converges (no oscillation from lag switching).
5. S in the middle of the sandwich for 2 and 3: re-estimated at the final b̂ (as in q3d.md),
   with its lag re-selected by the NW (1994) automatic rule, while A uses the Ŝ that served
   as the weighting matrix.
   - Two-step: the sandwich lag can differ from the weighting-matrix lag (e.g., 20 vs 22).
   - Iterated: at convergence the sandwich S equals the last weighting Ŝ.
