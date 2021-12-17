"""
GTAA Strategy Momentum Signal Generation file
Author: Boyu Xue
"""
import numpy as np
import pandas as pd

def get_signal(data,N):
    #-------- get_signal ----------
    # Goal: Signal Generation
    # Description: This function generate signals based on momentum
    #              Signal = (Pt-Pt-1)/Pt-1
    #------------------------------
    signal = data.div(data.shift(N))
    return signal.dropna()-1


def get_stocks(sig, quantile):
    #--------get_stocks------------
    # Goal: get the top and bottom quantile of assets based on signal
    # Input: quantile: quantile number e.g. 0.25 -->top 25% and bottom 25%
    # Return: l: Assets taking long positions
    #         s: Assets taking short positions
    #------------------------------
    l = sig.quantile(1-quantile)
    s = sig.quantile(quantile)

    l = sig.loc[sig>l]
    s = sig.loc[sig<s]

    return l,s #two series
