import numpy as np
import pandas as pd
import sys
import mo
import datetime as dt
import ef
import matplotlib.pyplot as plt
import stats
import scipy as sp
import plot
class MyStrategy():
    #-------- MyStrategy -------------------
    # Goal: Collect and analyze data, generate signal and weight, run simulation, do results analysis
    # Description: This is the core part of the strategy.
    # Workflow: 1. Initialization                    (func call: __init__)
    #           2. Collect data                      (func call: read_data)
    #           3. Generate signal                   (func call:get_siganl)
    #           4. Do backtest                       (func call: back_test)
    #              i.   Adjust postion every 22 days (func call: get_assets)
    #              ii.  Get weighting                (func call:get_weights)
    #              iii. Result analysis              (func call: get_stats,)
    # Input: MyStrategy Object
    # Return: None
    #--------------------------------------
    def __init__(self, args):
    #Initialization
        #Get inputs
        self.file_path = args.file_path
        self.quantile  = args.quantile
        self.weight    = args.weight
        self.cost      = args.cost
        self.diversify = args.diversify
        #Define assets classification
        self.category  = {
        "stock":["SPY","QQQ","EWJ","EWY","EWT","EWA","EWH","EWU",
                 "EWG","EWL","EWQ","EWC","IWM","GWX","VWO","VNQ","VNQI"],
        "bond":["TIP","MUB","HYG","GOVT","WIP","VWOB","HYEM"],
        "commo":["GLD","USO","UNG","DBA"]}
        self.read_data()
        self.signal    = mo.get_signal(self.data,22)                # Generate Siganl
        self.signal_date=self.signal.index.to_list()                # The list of dates correponding with signals
        self.benchmark = self.data['SPY'].loc[self.signal_date[0]:] #Get Benchmark
    def read_data(self):
    # Collect data
        self.data = pd.read_csv(self.file_path,index_col=0)
        self.data.index=pd.to_datetime(self.data.index,format='%m/%d/%Y')
        self.Libor = self.data['1m-Libor']
        self.data = self.data.drop('1m-Libor',1)
        self.date = self.data.index.to_list()

    def get_assets(self,date):
    #Get assets based signals
        sig = self.signal.loc[date]
        if self.diversify:      # nd Refinement
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

                l_weight = pd.concat([stock_l_weight,bond_l_weight,commo_l_weight])
                s_weight = pd.concat([stock_s_weight,bond_s_weight,commo_s_weight])
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
                start_date = self.date[self.date.index(end_date)-22]

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

                l_weight = np.abs(l_weight)/np.abs(l_weight.sum())
                s_weight = np.abs(s_weight)/np.abs(l_weight.sum())
                return l_weight,s_weight

            else:
                l,s = assets
                asset_list = pd.concat([l,s]).index.to_list()
                end_date = l.name
                start_date = self.date[self.date.index(end_date)-22]
                data = self.data.loc[start_date:end_date][asset_list]
                weight,P,ret,vol = ef.get_weights(data)
                l_weight = weight.loc[weight>0]
                s_weight = weight.loc[weight<0]
                l_weight = np.abs(l_weight)/np.abs(l_weight.sum())
                s_weight = np.abs(s_weight)/np.abs(l_weight.sum())
                return l_weight,s_weight

        else:
            sys.exit("Weighting method can only be 'signal' or 'ef', program terminated!\n ")

    def back_test(self):
        signal_date = self.signal_date
        cnt = 0
        net_value = [1,]
        for i in range(1,len(signal_date)):
            cost = 1
            today = signal_date[i]
            yesterday = signal_date[i-1]
            if cnt == 0:
                assets = self.get_assets(today)
                l_weight,s_weight = self.get_weights(assets)
                cost = (1-self.cost)
                print("[Check]: Position adjusted on:",yesterday)
            elif cnt ==22:
                cnt = -1
            ret = self.data.loc[today]/self.data.loc[yesterday]-1
            l_ret = (ret.loc[l_weight.index]+1)*l_weight
            s_ret = (-1*ret.loc[s_weight.index]+1)*s_weight

            if self.weight=='ef':
                net_weight = l_weight.sum()+s_weight.sum()
                tot_ret = l_ret.sum()*(l_weight.sum()/net_weight) + s_ret.sum()*(l_weight.sum()/net_weight)

            else:
                tot_ret = (l_ret.sum()+s_ret.sum())/2.0

            net_value.append(net_value[i-1]*tot_ret*cost)
            cnt+=1

        self.ret = net_value
            # 1.correlation; 2.beta;
        return net_value
    def get_stats(self):
        ret_rate = [self.ret[i]/self.ret[i-1]-1 for i in range(1,len(self.ret))]
        ave_ret,vol = sp.stats.norm.fit(ret_rate)
        Sharpe = (ave_ret-self.Libor.loc[self.date[-1]])/vol
        kurtosis = sp.stats.kurtosis(ret_rate)
        VaR = ave_ret - 2.576*vol
        self.ret_rate = ret_rate

        benchmark_ret = [self.benchmark[i]/self.benchmark[i-1]-1 for i in range(1,len(self.benchmark))]
        corr = np.corrcoef(ret_rate,benchmark_ret)[0,1]
        beta = (corr*vol)/np.std(benchmark_ret)
        print("Average Daily Return:"+str(round(ave_ret*100,2))+"%\n")
        print("Daily Volatility:"+str(round(vol*100,2))+"%\n")
        print("Daily 99% VaR:"+str(round(VaR*100,2))+"%\n")
        print("Sharpe Ratio:"+str(round(Sharpe,1))+"\n")
        print("kurtosis:"+str(round(kurtosis,1))+"\n")
        print("Correlation with Benchmark:"+str(round(corr,2))+"\n")
        print("Beta:"+str(round(beta,2))+"\n")
        return
