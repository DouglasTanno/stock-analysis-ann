import sys

stocks = 0
wallet = 100000
n = 0
transaction = 0
a = 0
e = 0

text_file = open(str(sys.argv[1]), "r")

date, value, rsi, roc, macd = text_file.readline().strip('\n').split('\t') #, sma5, sma10, sma20, ema5, ema10, ema20
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

    if((float(rsi) <= bottom_rsi) and ((float(roc)*100) <= bottom_roc) and (float(macd) <= 0) and (wallet > 0)): #COMPRA
        
        stocks = wallet/float(value)
        wallet = 0
        last_value = float(value)
        transaction = 1
        #print(str(date) +': compra')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        n = n + 1
        
    if((float(rsi) >= top_rsi) and ((float(roc)*100) >= top_roc) and (float(macd) >= 0) and (stocks > 0)): #VENDA
        
        wallet = float(value)*stocks
        stocks = 0
        last_value = float(value)
        transaction = -1
        #print(str(date) +': venda')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        n = n + 1
    
    try:
        date, value, rsi, roc, macd = text_file.readline().split('\t')
    except:
        if(stocks > 0):
            wallet = float(value)*stocks
            stocks = 0
            #print(str(date) +': venda final\n')
        print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        print(str(n)+' transacoes')
        print('total de acertos: '+str(a)+' ('+str(round((a*100/n),2))+'%)')
        print('total de erros: '+str(e)+' ('+str(round((e*100/n),2))+'%)')
        text_file.close()
        sys.exit()