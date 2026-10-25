# Data alignment spec (Questions 3 and 4)

1. EQ Dataset
    - Convert log returns to gross returns: R_e,t = exp(re_t), R_f,t = exp(rf_t).
    - Each value is the gross return over the 12 months ending in month t (months t-11 to t).
    - Market excess return: xR_w,t = exp(re_t) - exp(rf_t).

2. French portfolios (BM: "Lo 10"-"Hi 10", MOM: "Lo PRIOR"-"Hi PRIOR")
    - Convert monthly returns from percent to decimal.
    - For each month t, compute the trailing 12-month gross return:
      R12_j,t = (1 + R_j,t) * (1 + R_j,t-1) * ... * (1 + R_j,t-11)
    - This puts the French portfolios in the same form as exp(re_t)
      (monthly observations of 12-month gross returns ending in month t).

3. Use the value-weighted monthly block ("Value Weight Returns -- Monthly") for BM and MOM data.

4. Keep French returns nominal (no deflation). EQ returns are real.
    - Treat the mismatch as an approximation error.

5. Portfolio excess returns: xR_j,t = R12_j,t - R12_f,t, where R12_f,t is the trailing
   12-month compounded "RF" from the Fama/French 3 Factors file (same compounding as item 2).

6. Sample periods.
    - Question 3, all subquestions (b)-(e): 1940-12 to 2021-12 (973 monthly observations).
        - Start: first t at which z_{t-1} exists (item 7: value from month t-12; the first
          OOS forecast origin in q2e_PS1.md is 1939-12).
        - Q3(b) does not use z, but it uses the same sample so that results are
          comparable across subquestions.
    - Question 4: 1928-06 to 2021-12 (1,123 monthly observations).
        - Start: first R12 computed from French data beginning July 1927.
    - End (both): last EQ observation.
    - Reporting: always state the sample period explicitly in the .tex file
      (in the text and in every table or figure note).

7. Instrument z (Problem Set 1, 2e)
    - Used in Q3(c) and Q3(d).
    - z is not used in Q3(e): Q3(e) replaces the moment vector of Q3(c) with
      xR_w and the 20 decile portfolios (same 21 assets as Q4(b)).
    - Timing: z_{t-1} in the moment z_{t-1} · xR_w,t is the value from month t-12.
      xR_w,t is the 12-month return over months t-11 to t, so z must be known before
      that window starts. This is the OOS forecast made at origin t-12 (q2e_PS1.md),
      i.e., the forecast whose target is xR_e,t.
    - Time index: in Questions 3 and 4, t indexes months. t+1 is the next month, and each
      variable dated t+1 is the 12-month cumulative return ending in that month.
      This intentionally differs from Problem Set 1, where t+1 is one year ahead of t.

8. HAC standard errors: use Newey-West (1994) automatic lag selection for every
   Newey-West estimate in Questions 3 and 4.
    - With multiple moments, select a single lag from w'h_t with w = vector of ones (NW 1994 default).
    - Details (same as q4b.md decision 5): Bartlett kernel; moment series demeaned before
      building S; the selected lag is rounded down (e.g., m = 23.6 -> lag 23).
    - Divisor: Ω̂_ℓ = (1/T) Σ_{t=ℓ+1}^{T} (ε_t − ε̄)(ε_{t−ℓ} − ε̄)′, i.e., 1/T as in the original
      Newey-West (1987) definition (not 1/(T − ℓ) from Problem Set 1, footnote 3).

9. E[R_w] in Question 4 (M_t = 1 - b(R_w,t - mu)):
    - Add the moment E[R_w,t - mu] = 0 and set it exactly to zero, so mu_hat = mean(R_w).
    - Estimate b from the 21 pricing-error moments, holding mu = mu_hat.
    - Standard errors and pricing-error tests use the full 22-moment GMM sandwich,
      so they account for estimating mu.

10. Efficient GMM (Question 4c): iterated GMM.
    - Start from the Question 4b estimate (W = I).
    - Re-estimate S at the current b, set W = S_hat^{-1} (21 x 21 pricing-error block), and re-estimate b.
    - Repeat until b converges.
    - Also report the closed-form estimate and compare it with the iterated efficient GMM estimate.