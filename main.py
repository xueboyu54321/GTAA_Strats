"""
GTAA Strategy main file
Author: Boyu Xue
"""
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd

# Define Argumentfunction so that we can add arguments
def get_args():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('file', type=str,
                        help="Name or directory of the input data file\n")

    parser.add_argument('--quantile',type=float, default=0.25,
                        help="Select stocks from top/bottom x quantile based on simple momentum\n"
                        "Default to 0.25 (1/4 quantile)",required=False)

    parser.add_argument("--weight",type = str, default="signal",required=False,
                        help="Weighting Methods:\n"
                              "signal: Simple signal weighting based on momemtum; \n"
                              "ef: efficient frontier weighting by maximize sharpe ratio;\n")

    parser.add_argument("--diversify",action = "store_true", default = False, required = False,
                        help="Make sure at least one asset is selected from each asset class\n")

    return parser.parse_args()
#------------------------------------End-----------------------------------


if __name__ == '__main__':
   # If this file is called from cmd line
   args = get_args()


   #prices = pd.read_csv("portfolio.csv",index_col=0)
   #Step 1: Run momentum.py to get signals and stocks (may have to classify assets)
   #Step 2: Get weighting (Signal or ef)
   #Step 3: Backtesting(while loop/plotting)
