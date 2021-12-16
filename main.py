"""
GTAA Strategy main file
Author: Boyu Xue
"""
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import sys
import momemtum as mo
import backtest as bt
import datetime as dt
import efficient_frontier as ef
class MyStrategy():
    def __init__(self, args):
        self.file_path = args.file_path
        self.quantile  = args.quantile
        self.weight    = args.weight
        self.cost      = args.cost
        self.diversify = args.diversify
        self.category  = {
        "stock":["SPY","QQQ","EWJ","EWY","EWT","EWA","EWH","EWU",
                 "EWG","EWL","EWQ","EWC","IWM","GWX","VWO","VNQ","VNQI"],
        "bond":["TIP","MUB","HYG","GOVT","WIP","VWOB","HYEM"],
        "commo":["GLD","USO","UNG","DBA"]}
        self.read_data()
        self.signal    = mo.get_signal(self.data,22)

    def read_data(self):
        self.data = pd.read_csv(self.file_path,index_col=0)
        self.data.index=pd.to_datetime(self.data.index,format='%m/%d/%Y')
        self.Libor = self.data['1m-Libor']
        self.data = self.data.drop('1m-Libor',1)
        self.date = self.data.index.to_list()

    def get_assets(self,date):
        sig = self.signal.loc[date]
        if self.diversify:
            stock = sig.loc[self.category['stock']]
            bond  = sig.loc[self.category['bond']]
            commo = sig.loc[self.category['commo']]
            return [mo.get_stocks(stock,0.25),mo.get_stocks(bond,0.25),mo.get_stocks(commo,0.25)]
        else:
            return mo.get_stocks(sig,0.25)

    def get_weights(self,assets):
        if self.weight == "signal":
            if self.diversify:
                stock_l,stock_s = assets[0]
                bond_l , bond_s = assets[1]
                commo_l,commo_s = assets[2]

                stock_median = pd.concat([stock_l,stock_s]).median()
                stock_l-=stock_median
                stock_s-=stock_median
                stock_l_weight = 0.50*stock_l/stock_l.sum()
                stock_s_weight = 0.50*stock_s/stock_s.sum()

                bond_median = pd.concat([bond_l,bond_s]).median()
                bond_l-=bond_median
                bond_s-=bond_median
                bond_l_weight = 0.35*bond_l/bond_l.sum()
                bond_s_weight = 0.35*bond_s/bond_s.sum()

                commo_median = pd.concat([commo_l,commo_s]).median()
                commo_l-=commo_median
                commo_s-=commo_median
                commo_l_weight = 0.15*commo_l/commo_l.sum()
                commo_s_weight = 0.15*commo_s/commo_s.sum()

                l_weight = pd.concat([stock_l,bond_l,commo_l])
                s_weight = pd.concat([stock_s,bond_s,commo_s])
                return np.abs(l_weight),np.abs(s_weight)

            else:
                l,s = assets
                median = pd.concat([l,s]).median()
                l-=median
                s-=median
                l_weight = l/l.sum()
                s_weight = s/s.sum()
                return np.abs(l_weight),np.abs(s_weight)


        elif self.weight == "ef":
            if self.diversify:
                stock_l,stock_s = assets[0]
                bond_l , bond_s = assets[1]
                commo_l,commo_s = assets[2]
                stock_list = pd.concat([stock_l,stock_s]).index.to_list()
                bond_list = pd.concat([bond_l,bond_s]).index.to_list()
                commo_list = pd.concat([commo_l,commo_s]).index.to_list()

                end_date = stock_l.name
                start_date = self.date[self.date.index(end_date)-30]

                stock_data = self.data.loc[start_date:end_date][stock_list]
                stock_weight,stock_P,stock_ret,stock_vol = ef.get_weights(stock_data)
                stock_l_weight = stock_weight.loc[stock_weight>0]
                stock_s_weight = stock_weight.loc[stock_weight<0]

                bond_data = self.data.loc[start_date:end_date][bond_list]
                bond_weight,bond_P,bond_ret,bond_vol = ef.get_weights(bond_data)
                bond_l_weight = bond_weight.loc[bond_weight>0]
                bond_s_weight = bond_weight.loc[bond_weight<0]

                commo_data = self.data.loc[start_date:end_date][commo_list]
                commo_weight,commo_P,stock_ret,commo_vol = ef.get_weights(commo_data)
                commo_l_weight = commo_weight.loc[commo_weight>0]
                commo_s_weight = commo_weight.loc[commo_weight<0]

                l_weight = pd.concat([stock_l_weight,bond_l_weight,commo_l_weight])
                s_weight = pd.concat([stock_s_weight,bond_s_weight,commo_s_weight])

                fig, axs = plt.subplots(2, 2)
                axs[0,0].scatter(stock_P[1],stock_P[0],c='r',marker='^',label='Maximum Sharpe Ratio')
                axs[0,0].scatter(stock_vol, stock_ret, s = 4, c = 'g', marker = '.', label = 'Stock Efficient Frontier')
                axs[0,0].set_title('EfficientFrontier')
                axs[0,0].set_xlabel('Annualized Volatility')
                axs[0,0].set_ylabel('Annualized Return')
                axs[0,0].legend()

                axs[0,1].scatter(bond_P[1],bond_P[0],c='r',marker='^',label='Maximum Sharpe Ratio')
                axs[0,1].scatter(bond_vol, bond_ret, s = 4, c = 'g', marker = '.', label = 'Bond Efficient Frontier')
                axs[0,1].set_title('EfficientFrontier')
                axs[0,1].set_xlabel('Annualized Volatility')
                axs[0,1].set_ylabel('Annualized Return')
                axs[0,1].legend()

                axs[1,0].scatter(commo_P[1],commo_P[0],c='r',marker='^',label='Maximum Sharpe Ratio')
                axs[1,0].scatter(commo_vol, commo_ret, s = 4, c = 'g', marker = '.', label = 'Stock Efficient Frontier')
                axs[1,0].set_title('EfficientFrontier')
                axs[1,0].set_xlabel('Annualized Volatility')
                axs[1,0].set_ylabel('Annualized Return')
                axs[1,0].legend()

                fig.savefig("./dump/EfficientFrontier.jpg")

                return np.abs(l_weight),np.abs(s_weight)

            else:
                l,s = assets
                asset_list = pd.concat([l,s]).index.to_list()
                end_date = l.name
                start_date = self.date[self.date.index(end_date)-30]
                data = self.data.loc[start_date:end_date][asset_list]
                weight,P,ret,vol = ef.get_weights(data)
                l_weight = weight.loc[weight>0]
                s_weight = weight.loc[weight<0]

                plt.scatter(P[1],P[0],c='r',marker='^',label='Maximum Sharpe Ratio')
                plt.scatter(vol, ret, s = 4, c = 'g', marker = '.', label = 'Efficient Frontier')
                plt.title('EfficientFrontier')
                plt.xlabel('Annualized Volatility')
                plt.ylabel('Annualized Return')
                plt.legend()
                plt.savefig("./dump/EfficientFrontier.jpg")

                return np.abs(l_weight),np.abs(s_weight)

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
