# Data
1. Rf column from F-F_Research_Data_Factors.csv
2. From Lo 10 to Hi 10 column from Portfolios_Formed_on_BE-ME.csv
3. From Lo PRIOR to Hi PRIOR column from 10_Portfolios_Prior_12_2-ME.csv


Please only keep Rf column in F-F_Research_Data_Factors.csv
Sample Period: full sample from  Jul 1927 to the latest date

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
7. Note: E[.] operator can be estimated using the time average.


The output should be a scatterplot with portfolio deciles (1 to 10) on the x-axis and the respective b coefficients in the y-axis.

For this problem, one in blue (representing j = 1 to 10) and one in red (representing j = 11 to 20).

Leave it as placeholder(blank) regarding the explanation why this pattern emereges.

# Interpretation (pattern) (use this text as written)

As in Questions 2(a) and 2(b), the coefficients b̂ show no clear systematic pattern across
the deciles. One notable feature is that the joint estimates look like the two separate
estimates overlaid: the book-to-market coefficients are close to those in Question 2(a),
and the momentum coefficients are close to those in Question 2(b) (the correlation between
the separate and the joint estimates is 0.98 for both sets). In particular, the momentum
extremes keep the long-winner / short-loser pattern (b̂ ≈ −4.4 for Lo PRIOR and ≈ 3.5
for Hi PRIOR).

- Compute and report the two correlations quoted above (2(a) b̂ vs. the first 10 elements of
  the 2(c) b̂; 2(b) b̂ vs. the last 10 elements) so that the numbers in the text come from this
  code. If they differ from 0.98, −4.4, or 3.5, update the text with the computed values.

Within each set, the erratic coefficients arise for the same reason as in Questions 2(a) and
2(b): adjacent deciles are highly correlated, so inverting Σ̂ in b̂ = Σ̂⁻¹ Ê[xR] can make the
weights of adjacent deciles vary greatly. The joint estimates look like the two separate
estimates overlaid because, as seen in Question 2(b), the book-to-market SDF and the momentum
SDF (equivalently, the two maximum Sharpe ratio portfolios xR*) have a low correlation
(about 0.355). The two sets carry different pricing information, so combining them changes
the weights within each set little.

- Note: the individual book-to-market and momentum portfolios are themselves highly correlated
  with each other; the low correlation refers to the two SDFs (xR* portfolios), not to the
  individual portfolios. Do not state that the individual portfolios have low correlation.
- Replace 0.355 with the computed correlation from Question 2(b).

# Additional Decisions

1. Use the monthly value-weighted returns. The 10_Portfolios_Prior_12_2 file also has equal-weighted and annual versions of the same "Lo PRIOR" to "Hi PRIOR" columns, and the BE-ME file also has equal-weighted and annual versions of the same "Lo 10" to "Hi 10" columns.
2. Use decimal units, dividing the percent returns by 100. This changes the size of b by a factor of 100.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.


# Additional analysis on sharpe ratio

1. We now know that b1, b2 and b3 vector (calculated from BE/ME, Mom, and BE/ME + Mom, repectively).
2. Then, we can calculate the Sharpe Ratio of xR^* portfolios in such a way that (1) xR^* = b'xR, (2) SR(xR^\*) = E[xR^\*] / sigma(xR^\*)
3. Write down a code for calculating the Sharpe Ratio of each xR^\* portfolio and write it down in the LaTeX file.

# Interpretation (Sharpe ratios) (use this text as written)

The Sharpe ratio of xR* in Question 2(c) is higher than those in Questions 2(a) and 2(b),
as expected when the set of assets expands from 10 to 20 portfolios: any portfolio that can be
formed with 10 of the assets can also be formed with all 20 assets, by setting the weights on
the other 10 assets to zero, so the maximum Sharpe ratio with 20 assets cannot be lower. This is in line with the
Hansen-Jagannathan bound, Vol(M) ≥ SR · E[M]: since the maximum Sharpe ratio is larger with
20 assets, the lower bound on the volatility of an SDF that prices all 20 assets is larger than
the bound for an SDF that prices only 10 of them.