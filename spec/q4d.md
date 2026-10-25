# Data
Same as q4b.md (EQ Dataset, Fama/French 3 Factors RF, BM and MOM decile portfolios).

# Pre-Processing
Same as q4b.md: xR_w,t, the 20 portfolio excess returns, and the asset index
(1-10: Lo 10 to Hi 10, 11-20: Lo PRIOR to Hi PRIOR, 21: xR_w).

# Sketch

1. Assumption: R_f,t is treated as constant (R_f,t = R_f). Then
   M_t = a − b · R_w,t = (a − b · R_f) − b · xR_w,t,
   so the same SDF has the excess-return factor F_t = xR_w,t (same b, different intercept),
   and the time-series approach of slide 3.9 applies (λ = E[F], α_j = pricing errors).

2. λ̂: time-series regression of the factor on a constant, with Newey-West (1987, 1994)
   standard errors. Under the constant-R_f assumption, regressing R_w,t or xR_w,t on a
   constant gives the same standard error; report λ̂ = mean(xR_w,t).

3. For each asset j = 1, ..., 21 (OLS):
   xR_j,t = α_j + β_j · F_t + ε_j,t
   t-stat of α̂_j from Newey-West (1987, 1994) on that regression.
   (For j = 21, the factor itself: α̂_21 = 0, β̂_21 = 1, ε_21,t = 0.)

4. GRS test (Gibbons, Ross, Shanken 1989):
   GRS = (T − J − K)/J · (1 + Ê[F]′ Σ̂_F⁻¹ Ê[F])⁻¹ · α̂′ Σ̂_ε⁻¹ α̂ ~ F(J, T − J − K),
   with K = 1, T = number of monthly observations, J = 20 (assets 1-20; the factor,
   asset 21, is excluded).
   p-value = P(F(J, T − J − K) > GRS).
   (Note: slide 3.9 omits the inverse on (1 + Ê[F]′ Σ̂_F⁻¹ Ê[F]); the original GRS (1989)
   statistic includes it.)

# Output
1. λ̂ and its Newey-West standard error.
2. α̂_j and its t-stat for each asset j = 1, ..., 21.
3. The GRS statistic and its p-value.

# Additional Decisions
1. Refer to q34_common.md for data alignment (items 1-5), sample period (item 6,
   1928-06 to 2021-12), and Newey-West details (item 8; lag selected separately
   for each regression).
2. Purpose: Q4(d) imposes the constant-R_f approximation so that the factor is an excess
   return; Q4(e) uses Fama-MacBeth regressions, which do not require the factor to be an
   excess return (slide 3.11), so the two sets of results can be compared.
3. J in the GRS test: exclude asset 21 (the factor itself), giving J = 20. Its residual is
   identically zero, so including it would make Σ̂_ε singular. The α table still reports
   j = 21 (α̂_21 = 0 by construction).
4. Divisors with degrees-of-freedom corrections:
   Σ̂_ε = (1/(T − K − 1)) Σ_t ε̂_t ε̂_t′ (= 1/(T − 2) with K = 1), and
   Σ̂_F = (1/(T − 1)) Σ_t (F_t − F̄)².
