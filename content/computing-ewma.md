Title: Computing EWMA
Date: 2013-08-18
Author: Wilson Freitas
Lang: en
Category: finance
Tags: risk management, volatility, R

As a loop oriented developer—and long time user of old static typed languages—my first attempt to compute EWMA in R was

	ewma.loop <- function(rets, lambda) {
		n <- length(rets)+1
		sig.s <- rep(0, n)
		for (i in 2:n) {
			sig.s[i] <- sig.s[i-1]*lambda + (rets[i-1]^2)*(1 - lambda)
		}
		return(sqrt(tail(sig.s, n-1)))
	}

At a first sigh this implementation seemed to be good but from the perspective of an R developer it isn't.
Avoiding loops would be a better.
After a little research I found 

	ewma.func <- function(rets, lambda) {
		sig.p <- 0
		sig.s <- vapply(rets, function(r) sig.p <<- sig.p*lambda + (r^2)*(1 - lambda), 0)
		return(sqrt(sig.s))
	}

This implementation looked clean and sexy to me and it also reveals the power of `*apply` functions.
I decided to evaluate the performance of both implementations in order to find out which one is really the best.

	lambda <- 0.94
	rets <- 0.02*rnorm(100)
	system.time( replicate(10000, ewma.loop(rets, lambda)) )
	# user  system elapsed 
	# 4.075   0.018   4.093 
	system.time( replicate(10000, ewma.func(rets, lambda)) )
	# user  system elapsed 
	# 2.271   0.001   2.272 

The results are amazing.
Using functional approach is, without doubt, much better.
It is almost 2 times better and this is significant.

<script src="https://gist.github.com/wilsonfreitas/6279978.js"></script>
