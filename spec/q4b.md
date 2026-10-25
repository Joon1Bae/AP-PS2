# Data
1. Rf column from F-F_Research_Data_Factors.csv
2. From Lo 10 to Hi 10 column from Portfolios_Formed_on_BE-ME.csv
3. From Lo PRIOR to Hi PRIOR column from 10_Portfolios_Prior_12_2-ME.csv
4. R_{w, t} from EQ Dataset.csv

# Pre-Processsing for Portfolios_Formed_on_BE and 10_Portfolios_Prior_12_2
Please calculate each variables as follows:

xR = R_p - Rf where R_p is each portfolio return from
(1) Rp is Lo 10 to Hi 10 column in Portfolios_Formed_on_BE.csv
(2) Rp is Lo PRIOR to Hi PRIOR column in 10_Portfolios_Prior_12_2.csv
(3) and Rf is from F_Research_Data_Factors.csv 

The index for Rp is from 1 to 20. (1 is Lo10, 10 is Hi 10, and 11 is Lo PRIOR and so on.)

# Pre-Processsing for EQ Dataset
Please calculate each variables as follows:

xR = Rw,t - Rf,t where
(1) Rw,t = Re,t = e^re,t where re from the EQ dataset
(2) Rf,t = e^rf,t where rf from the EQ Dataset

The index for Rw,t is 21


# Sketch

1. If weighting matrix is identity matrix, the estimated beta will be the OLS coefficient of regression of E^hat[xR_j] onto Cov^hat[xR_j, R_w] for j = 1, ..., 20 and 21.

2. Standard errors should be reported based on Newey and West 1987 and 1994.

3. Pricing error for each moment condition and p-value for a chi-squared test with pricing errors are jointly zero.

# Output

1. The table should contain the estimated value of b as well as its standard error (standard errors should be based on Newey-West 1987 and 1994)

2. The pricing errors Ê[ε]_j for the 21 pricing moments
Each one's t-stat, Ê[ε]_j / √aVar_jj.
The χ² test on all 21 pricing moments, using the Moore–Penrose pseudo-inverse with 20 degrees of freedom.


# Additional Decisions

1. Refer to the Q34_common.md for the excess return on the 20 decile portfolios.

2. Sample: use the months where all 21 excess returns and R_w are available, which is Dec 1927 – Dec 2021.

3. Units: use decimals, dividing the Ken French percent returns by 100.

4. Estimator: b = (Ĉov[F, xR]′Ĉov[F, xR])⁻¹ Ĉov[F, xR]′Ê[xR] with F = R_w,t, no intercept. Ĉov = 1/T \Sigma^T_{t=1} (F_t-F^hat)(xR_t - xR^hat).

5. Use automatic NW 1994 lag selection

    - Bartlett, equal, demeaned
    - (1) Bartlett kernel, (2) lag chosen from the equally weighted sum of all moment series, (3) moment series u_t demeaned before building S, (4) selected lag rounded down.

5. Treat μ = E[R_w] as a parameter, with E[R_w − μ] = 0 satisfied exactly.

6. aVar[θ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′, with θ = (b, μ).
aVar[Ê[ε]] = (1/T)[I − G(AG)⁻¹A] S [I − G(AG)⁻¹A]′.
G now includes ∂g_j/∂μ = b·Ê[xR_j] and ∂(R_w − μ)/∂μ = −1.