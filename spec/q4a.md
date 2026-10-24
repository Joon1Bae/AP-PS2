# 1. Show that we also have (as an approximation) a conditionally CAPM, M_{t+1} ~= a_{t} - b_{t} * R_{w, t+1}, and provide expressions for a_{t} and b_{t}.

M_{t+1} = M(F_{t+1}; \theta)

It can be approximated by the Taylar expression as follows:

M(F_{t+1}; \theta) = \Sigma^{\inf}_{n=0} M^(n)(E_t[F_{t+1}]; theta) / n! (F_{t+1} - E_t[F_{t+1}])^n

And above second-order term can be neglected.

Then, 

M(F_{t+1}; \theta) ~= M(E_t[F_{t+1}]; \theta) + M'(E_t[F_{t+1}]; \theta) * (F_{t+1} - E_t[F_{t+1}]).


If we plugged in M(F_t+1; theta) = F_{t+1}^{-gamma} where F_{t+1} = R_{w, t+1}, then

M_{t+1} = -\gamma * E_t[R_{w, t}]^{-\gamma -1} * R_{w, t} + (\gamma + 1) * E_t[R_{w, t}]^{-\gamma}

Therefore, a_t = (\gamma + 1) * E_t[R_{w, t}]^{-\gamma} and b_t = -\gamma * E_t[R_{w, t}]^{-\gamma -1}

# 2. Highlight a disadvantage of the M_{t+1} ~= a_{t} - b_{t} * R_{w, t+1} relative to the original M_{t+1} = R^{-gamma}_{w, t+1}


1. The original model, M_{t+1} = R_{w,t+1}^(−γ), contains only the factor and the parameter, so there is no concern about additional assumptions or time-varying coefficients.

2. After linearization, a_t and b_t become time-varying, so E[xR_j] can no longer be written in the form E[b_t]′Cov(F_t, xR_{j,t}).

3. The time variation in a_t and b_t comes from E_t[R_{w,t+1}] as shown in the above. This conditional expectation must be estimated, and the choice of how to estimate it (e.g., with a linear model or some other method) introduces estimation error. The model could be wrong or there could be estimation error if model is correct.

4. By imposing additional assumptions or a model on a_t and b_t, they can be made time-invariant. However, if that model is wrong or the assumptions are inconsistent with reality, the estimates move further away from reality.


5. E_t[xR_{t+1}] = b_t′Cov_t(F_{t+1}, xR_{t+1}) holds, but from the perspective of the unconditional implications used in GMM, it can be written as E[xR_j] = E[b_t' * Cov_t(F_t+1, xR_{j, t+1})].

6. But again, b_t is determined by the E_t[R_{w,t}]. As in the PS1, we already checked that estimating the equity premium "VERY WELL" based on either IS or OS is really difficult.

Please write my argument in the .tex file in a VERY NEATED FORM!!!!!