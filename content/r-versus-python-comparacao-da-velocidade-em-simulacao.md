Title: R versus Python Comparação da Velocidade em Simulação
Category: data science
Author: Wilson Freitas
Tags: python, R, performance
Date: 2015-05-22
slug: r-versus-python-comparacao-da-velocidade-em-simulacao
Status: draft


```{r}
set.seed(101)
 
# generate data
x <- 0:100
y <- 2*x + rnorm(101, 0, 10)
 
# plot data
plot(x, y)
 
# run the regression
mod1 <- lm(y ~ x)
yHat <- fitted(mod1)
 
# get the residuals
errors <- resid(mod1)
 
# make a bootstrapping function
boot <- function(n = 10000) {
 b1 <- numeric(n)
 b1[1] <- coef(mod1)[2]
 
 for(i in 2:n){
 residBoot <- sample(errors, replace=F)
 yBoot <- yHat + residBoot
 modBoot <- lm(yBoot ~ x)
 b1[i] <- coef(modBoot)[2]
 }
 
 return(b1)
}
 
# Run the bootstrapping function
system.time( bootB1 <- boot() )
mean(bootB1)
```


```{python}
import numpy as np
import pylab as py
import statsmodels.api as sm
import time
 
# Create the data
x = np.arange(0, 101)
y = 2*x + np.random.normal(0, 10, 101)
 
# Add the column of ones for the intercept
X = sm.add_constant(x, prepend=False)
 
# Plot the data
py.clf()
py.plot(x, y, 'bo', markersize=10)
 
# Define the OLS models
mod1 = sm.OLS(y, X)
 
# Fit the OLS model
results = mod1.fit()
 
# Get the fitted values
yHat = results.fittedvalues
 
# Get the residuals
resid = results.resid
 
# Set bootstrap size
n = 10000
 
t0 = time.time()
# Save the slope
b1 = np.zeros( (n) )
b1[0] = results.params[0]
 
for i in np.arange(1, 10000):
    residBoot = np.random.permutation(resid)
    yBoot = yHat + residBoot
    modBoot = sm.OLS(yBoot, X)
    resultsBoot = modBoot.fit()
    b1[i] = resultsBoot.params[0]
 
t1 = time.time()
 
elapsedTime = t1 - t0
print elapsedTime
 
np.mean(b1)
```