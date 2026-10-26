# Data alignment spec (Questions 3 and 4)

Precedence: if an individual spec (q3b.md-q4e.md) conflicts with this file, this file takes
precedence. In particular, item 6 below overrides any sample period stated in an individual spec.

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

6. Sample periods: two versions.
    - Version (1) "Common": every subquestion of Questions 3 and 4 uses the same sample,
      1940-12 to 2021-12 (the latest start, set by z in Q3(c)-(d)), so results are comparable
      across subquestions and across the two Questions.
    - Version (2) "Max": each subquestion uses the longest sample available for it.
    - End (all): 2021-12, the last EQ observation.

    | Item        | Constraint                                   | (1) Common                | (2) Max                    |
    |-------------|----------------------------------------------|---------------------------|----------------------------|
    | Q3(b)       | EQ only (first EQ observation 1927-12)       | 1940-12 to 2021-12 (973)  | 1927-12 to 2021-12 (1,129) |
    | Q3(c), (d)  | z_{t-1} (item 7; first OOS origin 1939-12)   | 1940-12 to 2021-12 (973)  | 1940-12 to 2021-12 (973)   |
    | Q3(e)       | French R12 (first R12 1928-06), no z         | 1940-12 to 2021-12 (973)  | 1928-06 to 2021-12 (1,123) |
    | Q4(b)-(e)   | French R12 (first R12 1928-06), no z         | 1940-12 to 2021-12 (973)  | 1928-06 to 2021-12 (1,123) |

    - Report both versions for Q3(b), Q3(e), and Q4(b)-(e). Q3(c) and Q3(d) are identical in
      both versions, so report one set and say so.
    - Reporting: always state the sample period and T explicitly in the .tex file
      (in the text and in every table or figure note), and label each column or panel
      with its version, "(1) Common" or "(2) Max".
    - State the reason for the two versions explicitly in the text (at the start of
      Question 3 and again at the start of Question 4):
      Version (1) puts Questions 3 and 4 on the same sample, so that differences between the
      non-linear SDF (Question 3, M_t = R_w,t^(-γ)) and its linearized version (Question 4,
      M_t = a − b · R_w,t) are not driven by differences in the sample period; for example,
      Q3(e) and Q4(b) use the same 21 moments. Version (2) uses all data available for each
      subquestion, so each estimate is as precise as the data allow.

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

10. Efficient GMM (Question 4c): report two-step and iterated estimates, both computed with the
    closed-form GLS expression (details in q4c.md).
    The iterated procedure is:
    - Start from the Question 4b estimate (W = I).
    - Re-estimate S at the current b, set W = S_hat^{-1} (21 x 21 pricing-error block), and re-estimate b.
    - Repeat until b converges, re-selecting the Newey-West lag automatically each time S is
      re-estimated (q4c.md decision 4).