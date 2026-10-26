# Data
1. Rf column from F-F_Research_Data_Factors.csv
2. From Lo 10 to Hi 10 column from Portfolios_Formed_on_BE-ME.csv


Please only keep Rf column in F-F_Research_Data_Factors.csv
Sample Period: full sample from  Jul 1927 to the latest date

# Pre-Processsing
And please calculate each variables as follows:

xR = R_p - Rf where R_p is each portfolio return from Lo 10 to Hi 10 column in Portfolios_Formed_on_BE.csv and Rf is from F_Research_Data_Factors.csv 

# Basics

1. According to the PS, we use the normalized M, which is E[M] = 1.
2. Then, E[M] = a - b'E[xR] = 1
3. And SDF should satisty E[M * xR_j] = 0 for j = Lo 10, ..., Hi 10.
4. By plugging in M = a - b'xR, we get a * E[xR] = E[xR_j * xR'] * b for j = Lo 10, ..., Hi 10.
5. By using matrix notation,  a * E[xR * xR']^-1 * E[xR] = b
6. Therefore, we have two equations for a, b.



Output should be a scatterplot with the porfolio deciles (Lo 10 to Hi 10) in the x-axis and the respective b coefficients in the y-axis.

Leave it as placeholder(blank) regarding the explanation why this pattern emereges.

# Interpretation (3): pattern (use this text as written)

The estimated coefficients b̂ show no systematic pattern across the book-to-market deciles.
First, b̂ is not monotonic in the decile: it neither increases nor decreases as the
book-to-market ratio rises. Second, adjacent deciles sometimes have coefficients of opposite
signs (e.g., b̂_6 ≈ 3.0 and b̂_7 ≈ −5.3).

This pattern emerges from the closed form of b implied by the Method: b̂ = Σ̂⁻¹ Ê[xR],
where Σ̂ is the covariance matrix of the 10 excess returns. Adjacent deciles are highly
correlated (pairwise correlations of about 0.92 to 0.95). Inverting this nearly collinear Σ̂ and
multiplying by Ê[xR] can make the weights of adjacent deciles vary greatly, even with opposite
signs.

- Compute the correlations between adjacent deciles and report their range; replace
  "0.92 to 0.95" in the text with the computed range.
- Show in the Method that the two moment conditions give b̂ = Σ̂⁻¹ Ê[xR] (with Σ̂ using 1/T).

# Additional Decisions

1. Use the monthly value-weighted returns. The BE-ME file also has equal-weighted and annual versions of the same "Lo 10" to "Hi 10" columns.
2. Use decimal units, dividing the percent returns by 100. This changes the size of b by a factor of 100.
3. Also create a LaTeX skeleton, which doesn't need to go in the spec.