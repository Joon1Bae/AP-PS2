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


