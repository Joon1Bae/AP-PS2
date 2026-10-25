From the maximization problem in Equation (3.2),

varpi*_t = argmax_{varpi_t} E_t[U(W_{t+1})] : W_{t+1} = W_t * (R_{f,t+1} + varpi_t' xR_{t+1})

where R_{w,t+1} = R_{f,t+1} + varpi*_t' xR_{t+1} is the return on the optimal portfolio,
so that W_{t+1} = W_t * R_{w,t+1}.

F.O.C. satisfies:

dE_t[U(W_{t+1})] / dvarpi_t = E_t[U'(W_{t+1}) * W_t * xR_{t+1}] = 0 <> E_t[U'(W_{t+1}) * xR_{t+1}] = 0

Since W_t is the investor's wealth at time t, it is positive (W_t > 0) and known at time t,
so it can be taken outside E_t[.] and divided out.

Because U'(W_{t+1}) = (W_{t+1})^{-gamma} = (W_t * R_{w,t+1})^{-gamma},

E_t[(W_t * R_{w,t+1})^{-gamma} * xR_{t+1}] = 0 <> W_t^{-gamma} * E_t[R_{w,t+1}^{-gamma} * xR_{t+1}] = 0 <> E_t[R_{w,t+1}^{-gamma} * xR_{t+1}] = 0

where the last step uses the same argument for W_t^{-gamma} > 0.

Therefore, M_{t+1} = R_{w,t+1}^{-gamma} prices the vector of excess returns.
Because an SDF that prices only excess returns still does so after multiplication by any
positive factor (here, W_t^{-gamma}), the scale of M is not identified; a normalization is
therefore needed and is innocuous.
