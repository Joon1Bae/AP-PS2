# Data
1. Rf column from F-F_Research_Data_Factors.csv
2. From Lo PRIOR to Hi PRIOR column from 10_Portfolios_Prior_12_2-ME.csv


Please only keep Rf column in F-F_Research_Data_Factors.csv
Sample Period: full sample from  Jul 1927 to the latest date

# Pre-Processsing
And please calculate each variables as follows:

xR = R_p - Rf where R_p is each portfolio return from Lo PRIOR to Hi PRIOR column in 10_Portfolios_Prior_12_2.csv and Rf is from F_Research_Data_Factors.csv 

# Basics

1. According to the PS, we use the normalized M, which is E[M] = 1.
2. Then, E[M] = a - b'E[xR] = 1
3. And SDF should satisty E[M * xR_j] = 0 for j = Lo PRIOR, ..., Hi PRIOR.
4. By plugging in M = a - b'xR, we get a * E[xR] = E[xR_j * xR'] * b for j = Lo PRIOR, ..., Hi PRIOR.
5. By using matrix notation,  a * E[xR * xR']^-1 * E[xR] = b
6. Therefore, we have two equations for a, b.
7. Note: E[.] operator can be estimated using the time average.



Output should be a scatterplot with the porfolio deciles (Lo PRIOR to Hi PRIOR) in the x-axis and the respective b coefficients in the y-axis.

Leave it as placeholder(blank) regarding the explanation why this pattern emereges.

# Interpretation (3): pattern (use this text as written)

The estimated coefficients b̂ for the momentum deciles show no monotonic pattern.
In the middle deciles (2 to 9), as in Question 2(a), there is no clear pattern: the
coefficients change sign without a systematic order (e.g., b̂_5 ≈ 2.5 and b̂_6 ≈ −0.8).
The two extreme deciles, however, resemble the familiar momentum pattern: the SDF takes
a large short position in the loser decile (b̂_1 ≈ −4.0) and a large long position in the
winner decile (b̂_10 ≈ 3.4), i.e., long past winners and short past losers.

In the middle deciles, the pattern emerges for the same reason as in Question 2(a): adjacent
deciles are highly correlated (pairwise correlations of about 0.87 to 0.94) and have similar
average excess returns, so inverting Σ̂ in b̂ = Σ̂⁻¹ Ê[xR] can make the weights of adjacent
deciles vary greatly. At the extremes, however, the weights likely reflect the actual momentum
premium. The difference in average excess returns between decile 10 and decile 1 is large
(about 1.12% per month), which is hard to attribute to noise and is better viewed as a real
signal, and deciles 1 and 10 are relatively less correlated (about 0.59). As a result, the weight
on decile 10 is positive and the weight on decile 1 is negative.

- Compute these numbers (range of adjacent-decile correlations, the mean excess return of
  decile 10 minus decile 1, and the correlation between deciles 1 and 10) and replace the
  values in the text with the computed ones.

# Additional Decisions

1. Use the monthly value-weighted returns. The 10_Portfolios_Prior_12_2 file also has equal-weighted and annual versions of the same "Lo PRIOR" to "Hi PRIOR" columns.
2. Use decimal units, dividing the percent returns by 100. This changes the size of b by a factor of 100.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.


# Additional analysis on correlation

1. We now know that b1, b2 vector (calculated from BE/ME, Mom, repectively).
2. We also know a1, a2.
3. Then, we can recover M in such a way that M = a - b'xR.
4. Write down a code for calculating correlation between M1 and M2. 

# Interpretation (correlation) (use this text as written)

The correlation between the SDF from Question 2(a) and the SDF from Question 2(b) is positive
(about 0.355). Since a high SDF realization marks a high-marginal-utility ("bad") state, a
positive correlation means that the two SDFs partly agree on which states are bad. However,
the correlation is far from 1, which suggests that the two SDFs also capture different
dimensions of risk.

- Replace 0.355 with the computed correlation.