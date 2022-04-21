import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.utils import check_random_state
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler

seed = 20
seedSplit = 1
y_true = 0
seedMax = 0
acuraciaMax = 0
f1Max = 0
ganhoMax = 0

df = pd.DataFrame()
text_file = open(str(sys.argv[1]), "r")
df = pd.read_csv(text_file, sep='\t', header=None)
df.columns = ["Date", "Close", "RSI", "ROC", "MACD"]
df = df.set_index(df['Date'])

top_rsi = 80
bottom_rsi = 20
top_roc = 0.1
bottom_roc = -0.1


df['Decision_RSI'] = 0
df.loc[df['RSI'] <= bottom_rsi, 'Decision_RSI'] = 1 #compra
df.loc[df['RSI'] >= top_rsi, 'Decision_RSI'] = -1 #venda

df['Decision_ROC'] = 0
df.loc[df['ROC'] <= bottom_roc, 'Decision_ROC'] = 1 #compra
df.loc[df['ROC'] >= top_roc, 'Decision_ROC'] = -1 #venda

df['Decision_MACD'] = 0
df.loc[df['MACD'] <= 0, 'Decision_MACD'] = 1 #compra
df.loc[df['MACD'] >= 0, 'Decision_MACD'] = -1 #venda

df['Decision'] = 0
df.loc[df['Decision_RSI']+df['Decision_ROC'] >= 2, 'Decision'] = 1 #compra
df.loc[df['Decision_RSI']+df['Decision_MACD'] >= 2, 'Decision'] = 1 #compra
df.loc[df['Decision_ROC']+df['Decision_MACD'] >= 2, 'Decision'] = 1 #compra

df.loc[df['Decision_RSI']+df['Decision_ROC'] <= -2, 'Decision'] = -1 #venda
df.loc[df['Decision_RSI']+df['Decision_MACD'] <= -2, 'Decision'] = -1 #venda
df.loc[df['Decision_ROC']+df['Decision_MACD'] <= -2, 'Decision'] = -1 #venda

#print('\nResult dataframe :\n', df[df['Decision'] == 1])
#print('\nResult dataframe :\n', df[df['Decision'] == -1])
#print('\nResult dataframe :\n', df[df['Decision'] == 0])

df_train = df['2017-01-26':'2020-12-30']
df_test  = df['2021-01-04':]

features = ['Close','RSI','ROC','MACD']
nFeatures = len(features)
train = df_train[features]
y = df_train['Decision']

X_train, X_test, y_train, y_test = train_test_split(train, y, test_size = 0.10, random_state = seedSplit)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

yFutInv = df_test['Decision']
dias_investimento = len(yFutInv)
featInvTmp = df_test[features]

# converte dataframe para array
featInv = featInvTmp.values
# normalização
featInv = sc.transform(featInv)

avg = 0

def investimento(caixa=100000):


    erro = 0
    acerto = 0
    acoes = 0
    for i in range(0,dias_investimento):
        #print(featInv[i])
        opPredita = mlp.predict([featInv[i]])[0] # corrigi aqui
        opCorreta = yFutInv[i]
        #print('Operação predita: ' + str(opPredita))
        #print('Operação correta: ' + str(opCorreta))
        if (opPredita==opCorreta):
              acerto += 1
        else:
              erro += 1

        close = df_test['Close'][i]

        if (caixa > 0 and opPredita>0): #compra
            acoes = caixa / close
            caixa = 0
        elif (caixa == 0 and opPredita<0): #venda
            caixa = acoes * close
            acoes = 0
        if (i+1==dias_investimento): 
            if (caixa==0): # venda final
                caixa = acoes * close
                acoes = 0
                

        #print(str(close)+'\t '+str(opPredita)+ '\t ' +str(caixa) + '\t '+str(acoes))


    print('Total de acertos: '+str(acerto)+ '. Total de erros: '+str(erro))

    ganho = ((caixa-100000)/100000*100)
    print('Caixa: '+str(round(caixa,2)))
    return caixa, ganho

for seedTMP in range(1,seed + 1): #[3,40]:
    print('A seed do modelo MLP é: '+str(seedTMP))

    mlp = MLPClassifier(hidden_layer_sizes=(nFeatures,nFeatures*2+1,1),max_iter=100000, random_state=seedTMP) # random_state=seedMLP  
    mlp.fit(X_train,y_train)#treinamento em si

    #predictions and evaluations
    predictions = mlp.predict(X_test)


    f1Score = f1_score(y_test, predictions, average=None)
    f1 = f1Score[0]+ f1Score[2]# saída -1 venda
    f1Compra = f1Score[2] # saída 1 compra
    #f1 = f1_score(y_test, predictions, average='macro')
    acuracia = mlp.score(X_test, y_test)
    #print('TESTE '+str(f1[2]))

    print("F1 measure de (-1) (0) e (+1): "+str(round(f1Score[0],4))+'\t'+str(round(f1Score[1],4))+'\t'+str(round(f1Score[2],4)))
    #print(confusion_matrix(y_test,predictions))
    
    caixa, ganho = investimento(100000)
    avg = avg + caixa
    #if (f1>f1Max and f1Compra>0): 
    if (ganho>ganhoMax):
        f1Max = f1
        seedMax = seedTMP
        ganhoMax = ganho
        
    print('O ganho foi de: '+ str(round(ganho,2))+'%')
    print('\n')

print(str(avg/seed))
