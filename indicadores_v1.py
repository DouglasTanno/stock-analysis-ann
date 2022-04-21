#importing variables
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import seaborn as sns
import matplotlib.pyplot as plt
import sys

text_file = open(str(sys.argv[1]), "r")


#extracting data from Yahoo Finance API
all_data = pd.read_csv(text_file, sep = "\t", names = ['Date','Close'])

#Creating Return column
all_data['return'] = all_data['Close'].pct_change() 

#SMA
all_data['SMA(5)'] = all_data['Close'].transform(lambda x: x.rolling(window = 5).mean())
all_data['SMA(10)'] = all_data['Close'].transform(lambda x: x.rolling(window = 10).mean())
all_data['SMA(20)'] = all_data['Close'].transform(lambda x: x.rolling(window = 20).mean())
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
all_data['Diff'] = all_data['Close'].transform(lambda x: x.diff())
all_data['Up'] = all_data['Diff']
all_data.loc[(all_data['Up']<0), 'Up'] = 0

all_data['Down'] = all_data['Diff']
all_data.loc[(all_data['Down']>0), 'Down'] = 0 
all_data['Down'] = abs(all_data['Down'])

avg_14up = all_data['Up'].transform(lambda x: x.rolling(window=14).mean())
avg_14down = all_data['Down'].transform(lambda x: x.rolling(window=14).mean())

RS_14 = avg_14up / avg_14down

all_data['RSI(14)'] = 100 - (100/(1+RS_14))

##all_data['RSI_ratio'] = all_data['RSI_5']/all_data['RSI_15']

#MACD
all_data['MACD'] = EMA_12 - EMA_26

#ROC
all_data['ROC'] = all_data['Close'].transform(lambda x: x.pct_change(periods = 15)) 


all_data.to_csv('data.csv', encoding='utf-8')