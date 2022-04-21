#importing variables
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import seaborn as sns
import matplotlib.pyplot as plt

#extracting data from Yahoo Finance API
tickers = ['SFTBY','VIVT3.SA']
all_data = pd.DataFrame()
test_data = pd.DataFrame()
no_data = []

for i in tickers:
    try:
        test_data = pdr.get_data_yahoo(i, start = dt.datetime(2017,1,1), end = dt.datetime(2021,12,31))
        test_data['symbol'] = i
        all_data = all_data.append(test_data)
    except:
        no_data.append(i)

#Creating Return column
all_data['return'] = all_data.groupby('symbol')['Close'].pct_change() 

#SMA
all_data['SMA(5)'] = all_data.groupby('symbol')['Close'].transform(lambda x: x.rolling(window = 5).mean())
all_data['SMA(10)'] = all_data.groupby('symbol')['Close'].transform(lambda x: x.rolling(window = 10).mean())
all_data['SMA(20)'] = all_data.groupby('symbol')['Close'].transform(lambda x: x.rolling(window = 20).mean())
##all_data['SMA_ratio'] = all_data['SMA_15'] / all_data['SMA_5']

#EMA
all_data['EMA(5)'] = all_data['Close'].ewm(span=5, adjust=False).mean()
all_data['EMA(10)'] = all_data['Close'].ewm(span=10, adjust=False).mean()
all_data['EMA(20)'] = all_data['Close'].ewm(span=20, adjust=False).mean()
EMA_12 = all_data['Close'].ewm(span=12, adjust=False).mean()
all_data['EMA(12)'] = EMA_12
EMA_26 = all_data['Close'].ewm(span=26, adjust=False).mean()
all_data['EMA(26)'] = EMA_26

#RSI
all_data['Diff'] = all_data.groupby('symbol')['Close'].transform(lambda x: x.diff())
all_data['Up'] = all_data['Diff']
all_data.loc[(all_data['Up']<0), 'Up'] = 0

all_data['Down'] = all_data['Diff']
all_data.loc[(all_data['Down']>0), 'Down'] = 0 
all_data['Down'] = abs(all_data['Down'])

avg_14up = all_data.groupby('symbol')['Up'].transform(lambda x: x.rolling(window=14).mean())
avg_14down = all_data.groupby('symbol')['Down'].transform(lambda x: x.rolling(window=14).mean())

RS_14 = avg_14up / avg_14down

all_data['RSI(14)'] = 100 - (100/(1+RS_14))

##all_data['RSI_ratio'] = all_data['RSI_5']/all_data['RSI_15']

#MACD
all_data['MACD'] = EMA_12 - EMA_26

#ROC
all_data['ROC'] = all_data.groupby('symbol')['Close'].transform(lambda x: x.pct_change(periods = 15)) 


all_data.to_csv('data.csv', encoding='utf-8')