# Data
Same as q4b.md (EQ Dataset, Fama/French 3 Factors RF, BM and MOM decile portfolios).

# Pre-Processing
Same as q4b.md: R_w,t, xR_w,t, the 20 portfolio excess returns, and the asset index
(1-10: Lo 10 to Hi 10, 11-20: Lo PRIOR to Hi PRIOR, 21: xR_w).

# Sketch

0. Model: write the SDF in the lecture-note form M_t = E[M] · (a − b · R_w,t) and use the
   normalization E[M] = 1 (as in Q4(b)), so M_t = a − b · R_w,t with a = 1 + b · E[R_w].
   This constant-coefficient SDF is the special case of the conditional model on slide 3.11
   with a_t = a and b_t = b. Then λ_t = λ and β_j,t = β_j are constant, and the implied beta
   pricing model is E[xR_j] = λ · β_j.
   Derivation (F_t = R_w,t):
   (i)   E[M · xR_j] = 0 ⇔ E[M] · E[xR_j] + Cov(M, xR_j) = 0
         ⇔ E[xR_j] = −Cov(M/E[M], xR_j), using E[M] > 0 (no arbitrage).
   (ii)  Substituting M = E[M] · (a − b′F): −M/E[M] = −a + b′F. Since a is a constant,
         it drops out of the covariance: E[xR_j] = Cov(−a + b′F, xR_j) = b′ Cov(F, xR_j).
         (E[M] cancels exactly here, so this step does not need the normalization E[M] = 1;
         the normalization only pins down the values of a and b.)
   (iii) Insert the identity I = Σ_F Σ_F⁻¹ (Σ_F = Var(F) is invertible; here Σ_F = Var(R_w) > 0):
         E[xR_j] = b′ Σ_F Σ_F⁻¹ Cov(F, xR_j) = λ′ β_j,
         with λ′ = b′ Σ_F (λ = Σ_F b, since Σ_F is symmetric) and β_j = Σ_F⁻¹ Cov(F, xR_j).
   β_j = Σ_F⁻¹ Cov(F, xR_j) is the OLS slope of xR_j on F, so the first-pass time-series
   regressions in Sketch 2 estimate exactly this β_j.
   The Fama-MacBeth procedure of slide 3.11 applies unchanged; each monthly λ̂_t is a noisy estimate of the constant λ.

1. Factor: F_t = R_w,t (the gross return, not an excess return). No constant-R_f assumption:
   Fama-MacBeth estimates λ from cross-sectional regressions, so λ = E[F] is not required
   (slide 3.11: "F_t may or may not be excess returns").

2. Betas: for each asset j = 1, ..., 21, time-series regression (OLS) over the full sample
   xR_j,t = β_0,j + β_j · R_w,t + ε_j,t
   giving one constant β̂_j per asset.

3. Cross-sectional regressions: for each month t, regress the 21 excess returns on the betas,
   with no intercept (slides 3.10-3.11: the model predicts λ_0,t = 0)
   xR_j,t = λ_t · β̂_j + α_j,t   (j = 1, ..., 21)
   This gives the time series λ̂_t and α̂_j,t (the residuals of each cross-sectional regression).

4. Estimates and standard errors:
   λ̂ = mean of λ̂_t, and α̂_j = mean of α̂_j,t.
   The standard error of λ̂ (α̂_j) comes from a time-series regression of λ̂_t (α̂_j,t)
   on a constant with Newey-West (1987, 1994) standard errors.

# Output
1. λ̂ and its standard error.
2. α̂_j and its t-stat for each asset j = 1, ..., 21.

# Additional Decisions
1. Refer to q34_common.md for data alignment (items 1-5), sample period (item 6,
   1928-06 to 2021-12), and Newey-West details (item 8; lag selected separately
   for each regression on a constant).
2. Purpose: compare with Q4(d), which imposes the constant-R_f approximation so that the
   factor is an excess return; here the factor R_w,t is used as is.
3. Estimation window for β̂_j: the full sample. The SDF has constant coefficients, so β_j is
   constant (Sketch 0); a moving window (slide 3.11) is meant for time-varying β_j,t.
4. Intercept: none in the cross-sectional regressions, following slides 3.10-3.11
   (the model predicts λ_0,t = 0).
