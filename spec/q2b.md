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

# Additional Decisions

1. Use the monthly value-weighted returns. The 10_Portfolios_Prior_12_2 file also has equal-weighted and annual versions of the same "Lo PRIOR" to "Hi PRIOR" columns.
2. Use decimal units, dividing the percent returns by 100. This changes the size of b by a factor of 100.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.