# Data
1. Rf column from F-F_Research_Data_Factors.csv
2. From Lo 10 to Hi 10 column from Portfolios_Formed_on_BE-ME.csv
3. From Lo PRIOR to Hi PRIOR column from 10_Portfolios_Prior_12_2-ME.csv


Please only keep Rf column in F-F_Research_Data_Factors.csv
Sample Period: full sample from (1) Jul 1927 to Dec 1989, (2) Jan 1990 to the latest date


# Pre-Processsing
And please calculate each variables as follows:

xR = R_p - Rf where R_p is each portfolio return from
(1) Rp is Lo 10 to Hi 10 column in Portfolios_Formed_on_BE.csv
(2) Rp is Lo PRIOR to Hi PRIOR column in 10_Portfolios_Prior_12_2.csv
(3) and Rf is from F_Research_Data_Factors.csv 

The index for Rp is from 1 to 20. (1 is Lo10, 10 is Hi 10, and 11 is Lo PRIOR and so on.)

# Basics

1. According to the PS, we use the normalized M, which is E[M] = 1.
2. Then, E[M] = a - b'E[xR] = 1
3. And SDF should satisty E[M * xR_j] = 0 for j = 1, ..., 20.
4. By plugging in M = a - b'xR, we get a * E[xR] = E[xR_j * xR'] * b for j = 1, ..., 20.
5. By using matrix notation,  a * E[xR * xR']^-1 * E[xR] = b
6. Therefore, we have two equations for a, b.
7. Note: E[.] operator can be estimated using the time average. But, for this problem, use (1) JUL 1927 TO DEC 1989 sample period to estimate the a^hat and b^hat.

# Additional Decisions

1. Use the monthly value-weighted returns. The 10_Portfolios_Prior_12_2 file also has equal-weighted and annual versions of the same "Lo PRIOR" to "Hi PRIOR" columns, and the BE-ME file also has equal-weighted and annual versions of the same "Lo 10" to "Hi 10" columns.
2. Use Percent per month unit.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.

# Additional analysis on sharpe ratio

1. We now know the vectors b^hat, as well as the estimated parameters a^hat.
2. We also can recover M using the equation M_{t+1} = a^hat - b^hat'xR_{t+1}.
3. Then, we can calculate Cov[-M, xR_j] using the sample covariance formula: 1/T \Sigma^{T}_{t=1} [(-M_t + M^bar) * (xR_j,t - xR^bar_j)] where the bar denotes the time average for each j, and t = Jan 1990 to the latest date.
4. From the estimated covariance and E[xR_j], we can calculate the pricing errors as alpha_j = E[xR_j] - Cov(-M, xR_j)$ for all j = 1, ..., 20.
5. Write down a code to implement the procedure above.
6. The output should include a table reporting a pricing error for each porfolio in A NEATED MANNER!!!!!
7. Label the SDF explicitly in the table header and caption as the "BM + MOM SDF" (the Question 2(c)
   construction with all 20 portfolios), estimated on Jul 1927 to Dec 1989 and evaluated on
   Jan 1990 to the latest date.
8. Next to the out-of-sample pricing errors, add a column with the in-sample pricing errors of the
   BM + MOM SDF from Question 2(d) (full sample, all zero by construction), so the two can be
   compared in one table. Label the columns "In-sample (Q2(d))" and "Out-of-sample (Q2(e))",
   state each column's sample period, and report both columns in the same unit (percent per month).

# Interpretation (use this text as written)

In sample, the pricing errors of all 20 portfolios are zero because the SDF is fitted to the
realized data, as if it had seen the answer key. Out of sample, without the answer key, sizable
pricing errors appear. The zero in-sample pricing errors are therefore not evidence that the
model is correct.

The out-of-sample pricing errors are positive for all 20 portfolios, ranging from about 0.43% to
about 2.71% per month.

- Replace 0.43% and 2.71% with the minimum and maximum computed out-of-sample pricing errors,
  and check that all 20 are positive. If not, flag it instead of changing the text.

An in-sample fit also fits the noise in the sample, so out-of-sample performance tends to
deteriorate. In this case it deteriorates sharply: the monthly Sharpe ratio of xR* (with b fixed
at its in-sample estimate) falls from about 0.35 in sample to about 0.19 out of sample.

This result also clarifies the pattern in Question 2(a). There, adjacent deciles are highly
correlated, so b̂ = Σ̂⁻¹ Ê[xR] reacts strongly to small differences in average excess returns.
Out-of-sample results help tell whether those differences reflect estimation error or the true
structure of returns: if they were real, they would persist after 1989, and the in-sample weights
would keep pricing the portfolios well, with small pricing errors and a similar Sharpe ratio.
Instead, the pricing errors become large and the Sharpe ratio of xR* falls sharply, so the
evidence leans toward the former: the decline is consistent with large estimation error in b̂.

- Replace the numbers in the text (0.35, 0.19) with the values computed from this code, and add
  the in-sample and out-of-sample Sharpe ratios of xR* = b̂′xR (b̂ fixed) to the output.
  The in-sample value is for Jul 1927 to Dec 1989 (the estimation sample), not the full sample.