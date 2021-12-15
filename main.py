"""
GTAA Strategy main file
Author: Boyu Xue
"""
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import sys

class MyStrategy():
    def __init__(self, args):
        self.file_path = args.file_path
        self.quantile  = args.quantile
        self.weight    = args.weight
        self.cost      = args.cost
        self.diversify = args.diversify

    def read_data(self):
        self.data = pd.read_csv(self.file_path,index_col=0)

    def get_assets(self):
        # get assets based on signal
        pass

    def get_weights(self):
        if self.weight == "signal":

            pass

        elif self.weight == "ef":

            pass
        else:
            sys.exit("Weighting method can only be 'signal' or 'ef', program terminated!\n ")

    def back_test(self):
        #metrics:
            # 1.return; 2.vol; 3.IR/Sharpe; (Annualized)
            # 1.correlation; 2.beta; 3.kurtosis; 3.drawdown; 4.VaR (1d/99%); 5.
        #plots
        return



# Define Argumentfunction so that we can add arguments
def get_args():

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

    parser.add_argument("--cost", type = float, default = 0.02, required=False,
                        help="Transaction cost:\n"
                         "Transaction cost will be directly applied to the buy/sell price")

    parser.add_argument("--diversify",action = "store_true", default = False, required = False,
                            help="Make sure at least one asset is selected from each asset class\n")
    return parser.parse_args()
#------------------------------------End-----------------------------------

if __name__ == '__main__':
   # If this file is called from cmd line
   args = get_args()
   strat = MyStrategy(args)
   strat.get_weights()
