import sys

stocks = 0
wallet = 100000
n = 0
transaction = 0
a = 0
e = 0

text_file = open(str(sys.argv[1]), "r")
date, value, sma5_viv, sma10_viv, sma20_viv, sma5_sfty, sma10_sfty, sma20_sfty = text_file.readline().strip('\n').split('\t')

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
        
    if(((float(sma5_viv) > float(sma10_viv)) and (float(sma5_viv) > float(sma20_viv)) and (wallet > 0)) 
        or 
    ((float(sma5_sfty) > float(sma10_sfty)) and (float(sma5_sfty) > float(sma20_sfty)) and (wallet > 0))): #COMPRA
        stocks = wallet/float(value)
        wallet = 0
        last_value = float(value)
        transaction = 1
        #print(str(date) +': compra')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks)+'\n')
        n = n + 1

    elif(((float(sma5_viv) < float(sma10_viv)) and (float(sma5_viv) < float(sma20_viv)) and (stocks > 0)) 
        or 
    ((float(sma5_sfty) < float(sma10_sfty)) and (float(sma5_sfty) < float(sma20_sfty)) and (stocks > 0))): #VENDA
        wallet = float(value)*stocks
        stocks = 0
        last_value = float(value)
        transaction = -1
        #print(str(date) +': venda')
        #print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks)+'\n')
        n = n + 1
    try:
        date, value, sma5_viv, sma10_viv, sma20_viv, sma5_sfty, sma10_sfty, sma20_sfty = text_file.readline().split('\t')
    except:
        if(stocks > 0):
            wallet = float(value)*stocks
            stocks = 0
            #print(str(date) +': venda final\n')
        #print('Fim')
        print('retorno: '+str(wallet))
        #print('acoes: '+str(stocks))
        print(str(n)+' transacoes')
        print('total de acertos: '+str(a)+' ('+str(round((a*100/n),2))+'%)')
        print('total de erros: '+str(e)+' ('+str(round((e*100/n),2))+'%)')
        text_file.close()
        sys.exit()