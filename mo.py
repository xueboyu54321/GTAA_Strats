"""
GTAA Strategy Momentum Signal Generation file
Author: Boyu Xue
"""
import numpy as np
import pandas as pd

def get_signal(data,N):  #Must all be floats    date as index

    signal = data.div(data.shift(N))
    
    return signal.dropna()-1


def get_stocks(sig, quantile):

    l = sig.quantile(1-quantile)
    s = sig.quantile(quantile)

    l = sig.loc[sig>l]
    s = sig.loc[sig<s]
    
    return l,s #two series


