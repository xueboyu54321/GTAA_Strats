# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.cla import CLA
from pypfopt.efficient_frontier import EfficientFrontier
from scipy.stats import norm
import sys
#from pypfopt.objective_functions import negative_cvar

# Define Private MPT_User Function
def MPT_sharpe(ef):
    wSharpe=ef.max_sharpe()
    clean_weights=ef.clean_weights()
    P=ef.portfolio_performance(verbose=True)
    return pd.Series(clean_weights),P

def MPT_return(ef,target):
    wReturn=ef.efficient_return(target_return=target)
    clean_weights=ef.clean_weights()
    P=ef.portfolio_performance(verbose=True)
    return pd.Series(clean_weights),P

def MPT_vol(ef):
    wVol=ef.min_volatility()
    clean_weights=ef.clean_weights()
    P=ef.portfolio_performance(verbose=True)
    return pd.Series(clean_weights),P

#------------------------------------End-----------------------------------

# Define Monte Carlo Simulation
def MontC(mu,e_cov,prices):               #mu and sigma are arrays!
    total_steps = 365                # One Year
    N           = 10000
    ndata       = np.shape(prices)[1]
    yearly_return  = np.zeros((ndata,N))
    mPad          = np.zeros((ndata,total_steps))
    #Build Up mPad Array
    for i in range (total_steps):
        mPad[:,i]     = mu[:]

# Create the Monte Carlo simulated runs
    for n in range(N):
        # Compute simulated path of length total_steps for correlated returns
        # Gaussian is assumed
        correlated_randomness = e_cov @ norm.rvs(size = (ndata,total_steps))
        # Adjust simulated path by number of total_steps and mean of returns
        daily_return = mPad * (1/total_steps) + correlated_randomness * np.sqrt(1/total_steps)
        yearly_return[:, n] =  daily_return.sum(axis=1)

    Mu  = np.average(yearly_return,axis=1)
    Cov = np.cov(yearly_return)
    return Mu,Cov


#------------------------------------End-----------------------------------
def get_weights(prices):
    N = np.shape(prices)[0]   #number of trading days
# Compute the annualized average (mean) historical return and the Covariance
    mean_returns = mean_historical_return(prices, frequency = N)
    efficient_cov = CovarianceShrinkage(prices).ledoit_wolf()
# Calculate the weights
    ef1=EfficientFrontier(mean_returns,efficient_cov,weight_bounds=(-1,1))

    print('==============MPT Results==============\n')
# Maximizing the Sharpe's Ratio

    weight,P=MPT_sharpe(ef1)

    print('===================================\n')

# Construct the Efficient Frontier Curve
    cla = CLA(mean_returns, efficient_cov)
    (ret, vol, weights) = cla.efficient_frontier()

    return weight,P,ret,vol
