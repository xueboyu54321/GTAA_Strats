#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Cleaning
author: Boyu Xue

Warning:
Coding for data cleaning
No Use for now
Please ignore!!!
"""
import pandas as pd
import numpy as np

data_list = '''1M_Libor.csv	EWJ.csv		GLD.csv		MUB.csv		VNQ.csv
DBA.csv		EWL.csv		GOVT.csv	QQQ.csv		VNQI.csv
EWA.csv		EWQ.csv		GWX.csv		SPY.csv		VWO.csv
EWC.csv		EWT.csv		HYEM.csv	TIP.csv		VWOB.csv
EWG.csv		EWU.csv		HYG.csv		UNG.csv		WIP.csv
EWH.csv		EWY.csv		IWM.csv		USO.csv'''

data_list=data_list.split()

data = pd.read_csv('/Users/xueboyu/Desktop/GTAA/Data/'+ data_list[0])[['Date','Close']].rename(columns={'Close':'1m-Libor'})
data['Date']=pd.to_datetime(data['Date'],format='%m/%d/%Y')

for i in range(1,len(data_list)):
    name = data_list[i]
    temp = pd.read_csv('/Users/xueboyu/Desktop/GTAA/Data/'+ name)[['Date','Close']].rename(columns={'Close':name[:-4]})
    temp['Date']=pd.to_datetime(temp['Date'],format='%m/%d/%Y')
    data = data.merge(temp,on='Date' ,how='inner')

data.set_index('Date')

data.to_csv('/Users/xueboyu/Desktop/GTAA/Data.csv')
