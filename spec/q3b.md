# Data
1. re and rf columns from EQ Dataset.csv

# Pre-Processing for EQ Dataset
Please calculate each variable as follows:

xR_w,t = R_w,t - R_f,t where
(1) R_w,t = R_e,t = e^re,t where re is from the EQ Dataset
(2) R_f,t = e^rf,t where rf is from the EQ Dataset

# Sketch

1. Moment condition: E[R_w,t^(-γ) · xR_w,t] = 0 (one moment, one parameter).

2. As given in footnote 5, find γ̂ that solves Ĝ · Ê[R_w,t^(-γ̂) · xR_w,t] = 0,
   where Ĝ = Ê[∂γ(R_w,t^(-γ) · xR_w,t)] evaluated at γ̂
   (the first-order condition of γ̂ = argmin Ê[R_w,t^(-γ) · xR_w,t]²).

3. Estimate S with Newey and West (1987, 1994) and use it in the asymptotic variance:
   aVar[γ̂] = (1/T)(AG)⁻¹ A S A′ (AG)⁻¹′.

# Output

1. The estimated value of γ.
2. Its standard error, based on the Newey-West (1987, 1994) estimate of S.

# Additional Decisions

1. Refer to q34_common.md for the sample period (item 6) and the Newey-West lag selection (item 8).
2. Ĝ: analytical derivative.
