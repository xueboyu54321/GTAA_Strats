"""
GTAA Strategy plotting tool
Author: Boyu Xue
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

def plot(strat):
    #-------- plot func -------------------
    # Goal: Plot the return against benchmark
    # Description: This function will plot the return and dump the graph in dump folder
    # Input: MyStrategy Object
    # Return: None
    #--------------------------------------
    fig,ax = plt.subplots(figsize = (8,4))
    ax.plot(strat.signal_date,strat.ret)
    ax.plot(strat.signal_date,strat.benchmark/strat.benchmark[0])
    ax.set_xlabel('Date')
    ax.set_ylabel('Net Value')
    ax.set_title('Backtest')
    ax.legend(['Strategy Return','SPY Return'])
    fig.savefig("./dump/Net_Value.jpg")
    plt.show()

    return

def normal_fit(strat):
    #-------- normal_fit func -------------------
    # Goal: Fit the data into normal and plot the hist graph
    # Description: This function will plot the noraml fit and dump the graph in dump folder
    # Input: MyStrategy Object
    # Return: None
    #--------------------------------------
    ret_rate = strat.ret_rate
    ave_ret,vol = sp.stats.norm.fit(ret_rate)
    fig=plt.figure()
    plt.hist(ret_rate, bins=25, density=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = sp.stats.norm.pdf(x, ave_ret, vol)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = {0} %,  std = {1} %".format(round(ave_ret*100,2), round(vol*100,2))
    plt.title(title)
    plt.show()
    fig.savefig("./dump/NormalFit.jpg")

def max_drawdown(strat):
    #-------- max_drawdown func -------------------
    # Goal: Compute and plot the maximum drawdown
    # Description: This function will plot compute and plot the max_drawdown and dump the graph in dump folder
    #              Maximum Daily Drawdown: The maximum drawdown by Daily
    #              Maximum Yearly Drawdown: The maximum drawdown with a yearly rolling
    # Input: MyStrategy Objec
    # Return: Maximum Daily drawdown
    #--------------------------------------
    net_value = pd.Series(strat.ret,index = strat.signal_date)
    Roll_Max = net_value.rolling(252,min_periods=1).max()
    Daily_Drawdown = net_value/Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(252, min_periods=1).min()

    fig=plt.figure(figsize=(8,4))
    Daily_Drawdown.plot()
    Max_Daily_Drawdown.plot()
    plt.title('Maximum Drawdown')
    plt.legend(['Maximum Daily Drawdown','Maximum Yearly Drawdown'])
    plt.show()
    fig.savefig("./dump/MaxDrawdown.jpg")
    return round(min(Max_Daily_Drawdown),2)
