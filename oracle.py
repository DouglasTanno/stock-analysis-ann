import sys
import pandas as pd

stocks = 0
wallet = 100000
n = 0

df = pd.DataFrame()
text_file = open(str(sys.argv[1]), "r")
df = pd.read_csv(text_file, sep='\t', header=None)
df.columns = ["Date", "Close", "RSI_VIV", "ROC_VIV", "MACD_VIV"]
df = df.set_index(df['Date'])

last_value = 0
for i in range(len(df)):
    value = df.iloc[i,1]
    if (i > 0):
        if((wallet > 0) and (value > last_value)): #COMPRA
            stocks = wallet/float(last_value)
            wallet = 0
            n = n + 1
        if((stocks > 0) and (value < last_value)): #VENDA
            wallet = float(last_value)*stocks
            stocks = 0
            n = n + 1
    
    last_value = value


if(stocks > 0):
    wallet = float(value)*stocks
    stocks = 0
    #print(str(date) +': venda final\n')

print('retorno: '+str(wallet))
#print('acoes: '+str(stocks))
print(str(n)+' transacoes')
text_file.close()
sys.exit()