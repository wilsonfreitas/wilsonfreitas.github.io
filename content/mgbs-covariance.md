Title: Covariance between stochastic processes
Date: 2014-07-04
Author: Wilson Freitas
Lang: en
Category: finance
Tags: math


Let $dX_1$ and $dX_2$, describe the asset returns in different time intervals, $s$ and $u$.

$$
\begin{aligned}
dX_1(s) & = \sigma_1 dW_1 \\\\
dX_2(u) & = \sigma_2 dW_2
\end{aligned}
$$

> Note that these processes are arithmetic and Gaussian.

We consider the returns being independent and since we are working with only one asset we have:

$$
\begin{aligned}
\sigma_1 & \equiv \sigma\sqrt{t_1} \\\\
\sigma_2 & \equiv \sigma\sqrt{t_2}
\end{aligned}
$$

where $\sigma$ is the daily volatility.

## Covariance between $dX_1$ and $dX_2$

The covariance between $dX_1$ and $dX_2$ is given by:

$$
\begin{aligned}
COV(dX_1, dX_2) & = E[dX_1(t_1) dX_2(t_2)] \\\\
                & = E[\sigma_1 dW_1 \sigma_2 dW_2]
\end{aligned}
$$

If $t_1 < t_2$ we can write:

$$
\begin{aligned}
COV(dX_1, dX_2) & = E[\sigma_1 dW_1 (\sigma_1 dW_1 + \sigma_2 dW_2 - \sigma_1 dW_1)] \\\\
                & = E[\sigma_1^2 dW_1^2 + \sigma_1 dW_1(\sigma_2 dW_2 - \sigma_1 dW_1)] \\\\
                & = \sigma_1^2 E[dW_1^2] +  E[\sigma_1 dW_1(\sigma_2 dW_2 - \sigma_1 dW_1)] \\\\
                & = \sigma_1^2 t1 +  E[\sigma_1 dW_1(\sigma_2 dW_2 - \sigma_1 dW_1)]
\end{aligned}
$$
