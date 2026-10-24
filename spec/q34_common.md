# Data alignment spec (Questions 3 and 4)

1. EQ Dataset
    - Convert log returns to gross returns: R_e,t = exp(re_t), R_f,t = exp(rf_t)
    - Each value is the gross return over the 12 months ending in month t (months t-11 to t).
    - Market excess return: xR_w,t = exp(re_t) - exp(rf_t).

2. French portfolios (BM: "Lo 10"-"Hi 10", MOM: "Lo PRIOR"-"Hi PRIOR")
    - Convert monthly returns from percent to decimal.
    - For each month t, compute the trailing 12-month gross return:
     R12_j,t = (1 + R_j,t) * (1 + R_j,t-1) * ... * (1 + R_j,t-11)
    - This puts the French portfolios in the same form as exp(re_t) (monthly observations of 12-month gross returns ending in month t).

3. Use the value-weighted monthly block ("Value Weight Returns -- Monthly") for BM and MOM data.

4. Keep French returns nominal (no deflation). EQ returns are real.
    - Treat the mismatch as an approximation error

5. Portfolio excess returns: xR_j,t = R12_j,t - R12_f,t, where R12_f,t is the trailing 12-month compounded "RF" from the Fama/French 3 Factors file (same compounding as item 2).

6. Common sample period: 1928-06 to 2021-12 (1,123 monthly observations).
    - Start: first R12 computed from French data beginning July 1927.
    - End: last EQ observation.
    - Note: Question 3e also uses the instrument z_{t-1} from Problem Set 1 (2e), so its sample may start later, depending on when the OOS forecasts begin.