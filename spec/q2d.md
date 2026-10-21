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

# Additional Decisions

1. Use the monthly value-weighted returns. The 10_Portfolios_Prior_12_2 file also has equal-weighted and annual versions of the same "Lo PRIOR" to "Hi PRIOR" columns, and the BE-ME file also has equal-weighted and annual versions of the same "Lo 10" to "Hi 10" columns.
2. Use decimal units, dividing the percent returns by 100. This changes the size of b by a factor of 100.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.

# Outputs

The output should be a scatterplot with portfolio deciles (1 to 10) on the x-axis and the respective b coefficients in the y-axis.

For this problem, one in blue (representing j = 1 to 10) and one in red (representing j = 11 to 20).

Leave it as placeholder(blank) regarding the explanation why this pattern emereges.

# Additional analysis on sharpe ratio

1. We now know the vectors b1, b2 and b3 (calculated from BE/ME, Mom, and BE/ME + Mom, repectively), as well as the estimated parameters a1, a2, and a3.
2. We also can recover M using the equation M = a - b'xR.
3. Then, we can calculate Cov[-M, xR_j] using the sample covariance formula: 1/T \Sigma^{T}_{t=1} [(-M_t + M^bar) * (xR_j,t - xR^bar_j)] where the bar denotes the time average for each j.
4. From the estimated Cov and E^[xR_j], we can calculate the pricing errors as alpha_j = E^[xR_j] - Cov^(-M, xR_j) for j = 1, ..., 20 (if BE/ME + Mom is the case. If not, index ends at 10)
5. Write down a code to implement the procedure above.
6. The output should include a table reporting a pricing error for BE/ME only, Mom only, and BE/ME + Mom cases for each porfolio in A NEATED MANNER!!!!!