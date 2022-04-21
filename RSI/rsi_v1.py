import sys

stocks = 0
wallet = 100000
n = 0
transaction = 0
a = 0
e = 0

text_file = open(str(sys.argv[1]), "r")
date, value, rsi_viv, rsi_sfty = text_file.readline().strip('\n').split('\t')
top = int(sys.argv[2])
bottom = int(sys.argv[3])

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

    if(((float(rsi_viv) <= bottom) and (wallet > 0)) or ((float(rsi_sfty) <= bottom) and (wallet > 0))): #COMPRA
        stocks = wallet/float(value)
        wallet = 0
        last_value = float(value)
        transaction = 1
        #print(str(date) +': compra')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        n = n + 1
        
    elif(((float(rsi_viv) >= top) and (stocks > 0)) or ((float(rsi_sfty) >= top) and (stocks > 0))): #VENDA
        wallet = float(value)*stocks
        stocks = 0
        last_value = float(value)
        transaction = -1
        #print(str(date) +': venda')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        n = n + 1
    
    try:
        date, value, rsi_viv, rsi_sfty = text_file.readline().split('\t')
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