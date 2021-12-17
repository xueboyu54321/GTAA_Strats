"""
GTAA Strategy main file
Author: Boyu Xue
"""
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import datetime as dt
from Strategy import MyStrategy
import matplotlib.pyplot as plt
import plot
# Define Argumentfunction so that we can add arguments
def get_args():
    #-------- get_args -------
    # Goal: Collect inputs
    # Run command:
    #         Basic strategy: python3 data.csv
    #         1st Refinement: python3 data.csv --ef (Run with efficient frontier)
    #         2nd Refinement: python3 data.csv --diversify (Make sure all types of assets to have a weight)
    # Warning: In principle, --ef and --diversify could be compiled and run together but
    #          this is not recommended since it is very likely to generate bug!
    #-------------------------
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('file_path', type=str,
                        help="Name or directory of the input data file\n")

    parser.add_argument('--quantile',type=float, default=0.25,
                        help="Select stocks from top/bottom x quantile based on simple momentum\n"
                        "Default to 0.25 (1/4 quantile)",required=False)

    parser.add_argument("--weight",type = str, default="signal",required=False,
                        help="Weighting Methods:\n"
                              "signal: Simple signal weighting based on momemtum; \n"
                              "ef: efficient frontier weighting by maximize sharpe ratio;\n")

    parser.add_argument("--cost", type = float, default = 0.0004, required=False,
                        help="Transaction cost:\n"
                         "Transaction cost will be directly applied to the buy/sell price")

    parser.add_argument("--diversify",action = "store_true", default = False, required = False,
                            help="Make sure at least one asset is selected from each asset class\n")
    return parser.parse_args()
#------------------------------------End-----------------------------------

if __name__ == '__main__':                       # If this file is called from cmd line
    args = get_args()                            # Get Argument
    strat = MyStrategy(args)                     # Define MyStrategy Object
    strat.back_test()                            # Do backtest
    plot.plot(strat)                             # Plot the return
    msg = strat.get_stats()                      # Get Statistics
    plot.normal_fit(strat)                       # Check Normality
    drawdown = plot.max_drawdown(strat)          # Plot the Drawdown
    print("Maximum Drawdown"+str(drawdown)+"\n")
    msg += "Maximum Drawdown"+str(drawdown)+"\n"
    result_analysis = open("./dump/result_analysis.txt", "w")
    n = result_analysis.write(msg)
    result_analysis.close()
