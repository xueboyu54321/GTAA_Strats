#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTAA Strategy Backtest file
Author: Boyu Xue
"""
import numpy as np
import pandas as pd

def get_asset_return(data):
    ret = data.div(data.shift(1)).fillna(1)
    return ret.cumprod()
