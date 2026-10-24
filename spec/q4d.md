# Sketch

1. Lambda = E[F_t+1] where F_t+1 = R_{w,t}
2. Using NW 1987 and 1994 method, the standard error for lambda can be calculated.
3. or, run the following time-series regression in the below:

R_{w, t} = \lambda + \epsilon


β_j can be calculated from the time-series regression as follows:

xR_{j,t} = α_{j} + β_{j} * R_{w, t} + ε_{j,t} for each j.

Then, we can estimate lambda, alpha_j, and beta_j for all j.

GRS = (T−J−K) / J * (1+ E^hat[F]' * Σ^hat_{F}−1 * E^hat[F]) * α′Σε^−1α ∼ FJ,T−J−K

Then, we can calculate the p-value as follows:

