import sys

stocks = 0
wallet = 100000
n = 0
transaction = 0
a = 0
e = 0
buy = 0
sell = 0

text_file = open(str(sys.argv[1]), "r")
date, value, rsi_viv, roc_viv, macd_viv, sma5_viv, sma10_viv, sma20_viv, ema5_viv, ema10_viv, ema20_viv, rsi_sfty, roc_sfty, macd_sfty, sma5_sfty, sma10_sfty, sma20_sfty, ema5_sfty, ema10_sfty, ema20_sfty = text_file.readline().strip('\n').split('\t') #, sma5, sma10, sma20, ema5, ema10, ema20
top_rsi = int(sys.argv[2])
bottom_rsi = int(sys.argv[3])
top_roc = int(sys.argv[4])
bottom_roc = int(sys.argv[5])

while(text_file):

    if(transaction != 0):
        if(transaction == -1):
            if(last_value > float(value)):
                #print('acerto'+'\n')
                a = a + 1
            else:
                #print('erro'+'\n')
                e = e + 1
        if(transaction == 1):
            if(last_value < float(value)):
                #print('acerto'+'\n')
                a = a + 1
            else:
                #print('erro'+'\n')
                e = e + 1
        transaction = 0  
        n = n + 1
    
    if(wallet > 0): #compra
        buy = 0
        if(float(rsi_viv) <= bottom_rsi):
            buy = buy + 1
        if((float(roc_viv)*100) <= bottom_roc):
            buy = buy + 1
        if(float(macd_viv) <= 0):
            buy = buy + 1
        if(float(rsi_sfty) <= bottom_rsi):
            buy = buy + 1
        if((float(roc_sfty)*100) <= bottom_roc):
            buy = buy + 1
        if(float(macd_sfty) <= 0):
            buy = buy + 1
        if((float(sma5_viv) > float(sma10_viv)) and (float(sma5_viv) > float(sma20_viv))):
            buy = buy + 1
        if((float(ema5_viv) > float(ema10_viv)) and (float(ema5_viv) > float(ema20_viv))):
            buy = buy + 1
        if((float(sma5_sfty) > float(sma10_sfty)) and (float(sma5_sfty) > float(sma20_sfty))):
            buy = buy + 1
        if((float(ema5_sfty) > float(ema10_sfty)) and (float(ema5_sfty) > float(ema20_sfty))):
            buy = buy + 1            
        if(buy >= 4):
            stocks = wallet/float(value)
            wallet = 0
            last_value = float(value)
            transaction = 1
            #print(str(date) +': compra')
            #print('retorno: '+str(wallet))
            #print('acoes: '+str(stocks))
            buy = 0
        
    if(stocks > 0): #venda
        sell = 0
        if(float(rsi_viv) >= top_rsi):
            sell = sell + 1
        if((float(roc_viv)*100) >= top_roc):
            sell = sell + 1
        if(float(macd_viv) >= 0):
            sell = sell + 1
        if(float(rsi_sfty) >= top_rsi):
            sell = sell + 1
        if((float(roc_sfty)*100) >= top_roc):
            sell = sell + 1
        if(float(macd_sfty) >= 0):
            sell = sell + 1
        if((float(sma5_viv) < float(sma10_viv)) and (float(sma5_viv) < float(sma20_viv))):
            sell = sell + 1
        if((float(ema5_viv) < float(ema10_viv)) and (float(ema5_viv) < float(ema20_viv))):
            sell = sell + 1
        if((float(sma5_sfty) < float(sma10_sfty)) and (float(sma5_sfty) < float(sma20_sfty))):
            sell = sell + 1
        if((float(ema5_sfty) < float(ema10_sfty)) and (float(ema5_sfty) < float(ema20_sfty))):
            sell = sell + 1
        if(sell >= 4):
            wallet = float(value)*stocks
            stocks = 0
            last_value = float(value)
            transaction = -1
            #print(str(date) +': venda')
            #print('retorno: '+str(wallet))
            #print('acoes: '+str(stocks))
            sell = 0
  
    try:
        date, value, rsi_viv, roc_viv, macd_viv, sma5_viv, sma10_viv, sma20_viv, ema5_viv, ema10_viv, ema20_viv, rsi_sfty, roc_sfty, macd_sfty, sma5_sfty, sma10_sfty, sma20_sfty, ema5_sfty, ema10_sfty, ema20_sfty = text_file.readline().split('\t') #, sma5, sma10, sma20, ema5, ema10, ema20
    except:
        if(stocks > 0):
            wallet = float(value)*stocks
            stocks = 0
            #print(str(date) +': venda final\n')
        print('retorno: '+str(round(wallet,2))+' ('+str(n)+')')
        print('acoes: '+str(stocks))
        print('total de acertos: '+str(a)+' ('+str(round((a*100/n),2))+'%)')
        print('total de erros: '+str(e)+' ('+str(round((e*100/n),2))+'%)')
        text_file.close()
        sys.exit()