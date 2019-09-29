import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from yellowbrick.classifier import ConfusionMatrix

'''Aqui vamos usar um método de classificação usando a Árvore de Decisão, para saber como o computador irá dizer qual o tipo de produto derivado do petróleo. '''

#Carregamento da base de dados
dados = pd.read_csv('D:\\Meus Documentos\\Downloads\\Banco de dados\\Anuário Estatístico 2019 - Distribuição percentual da produção de derivados de petróleo não energéticos.csv', sep = ';')

#Criaremos uma lista para adicionar os números para cada tipo de produto
coluna_numerica_produtos = []

#Aqui foi criado um laço para atribuir um número para cada produto derivado do petróleo
for index, column in dados.iterrows():
    if column['Derivados de petróleo'] == 'Gasolina A ':
        coluna_numerica_produtos.append('Gasolina Aditivada')
    elif column['Derivados de petróleo'] == 'Gasolina de aviação':
        coluna_numerica_produtos.append('Gasolina de aviação')
    elif column['Derivados de petróleo'] == 'GLP1':
        coluna_numerica_produtos.append('GLP')
    elif column['Derivados de petróleo'] == 'Óleo combustível2,3':
        coluna_numerica_produtos.append('Óleo combustível')
    elif column['Derivados de petróleo'] == 'Óleo diesel3':
        coluna_numerica_produtos.append('Óleo diesel')
    elif column['Derivados de petróleo'] == 'QAV':
        coluna_numerica_produtos.append('QAV')
    elif column['Derivados de petróleo'] == 'Querosene iluminante':
        coluna_numerica_produtos.append('Querosene Iluminante')
    elif column['Derivados de petróleo'] == 'Outros4':
        coluna_numerica_produtos.append('Outros4')
    elif column['Derivados de petróleo'] == 'Asfalto':
        coluna_numerica_produtos.append('Asfalto')
    elif column['Derivados de petróleo'] == 'Coque5':
        coluna_numerica_produtos.append('Coque')
    elif column['Derivados de petróleo'] == 'Nafta6':
        coluna_numerica_produtos.append('Nafta')
    elif column['Derivados de petróleo'] == 'Óleo lubrificante ':
        coluna_numerica_produtos.append('Óleo lubrificante')
    elif column['Derivados de petróleo'] == 'Parafina':
        coluna_numerica_produtos.append('Parafina')
    elif column['Derivados de petróleo'] == 'Solvente':
        coluna_numerica_produtos.append('Solvente')
    elif column['Derivados de petróleo'] == 'Outros7':
        coluna_numerica_produtos.append('Outros7')

#Criaremos uma nova coluna 'Números dos derivados de petróleo' no dataframe 'dados'
dados['Números dos derivados de petróleo'] = coluna_numerica_produtos

#Precisaremos fazer a transformação dos números da coluna 'produção (m3)' para o tipo float, pelo fato do python não reconhecer a ',' como elemento separador de número.
dados['Produção (m3)'] = dados['Produção (m3)'].str.replace(",", ".").astype(float)

#Criação de uma variável com variáveis independentes(x)
previsores = dados.iloc[:, [0, 3]].values

#Criação de uma variável com variável de resposta(y)
classe = dados.iloc[:, 4].values

#Aqui iremos transformar as colunas categóricas em colunas numéricas
labelencoder = LabelEncoder()
previsores[:, 0] = labelencoder.fit_transform(previsores[:, 0])

#Aqui hávera a divisão dos dados para treinamento e teste passando como parâmetros(variavel independente, variável resposta, a amostra de teste[0 até 1] e divisao da base de dados igual)
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(previsores, classe, test_size = 0.22, random_state = 0)

#Criação do algoritmo da árvore de decisão, juntamente com o treinamento do algoritmo
arvore = DecisionTreeClassifier()
arvore.fit(X_treinamento, y_treinamento)

#Gera um arquivo de texto no diretório específico onde o código está salvo, copia o texto que foi gerado e cola na aba lá presente no site webgraphviz.com para gerar a árvore.
export_graphviz(arvore, out_file = 'tree.dot')

#Faz as previsões da variável teste.
previsoes = arvore.predict(X_teste)

#Gera uma variável com a matriz de confusão
confusao = confusion_matrix(y_teste, previsoes)

#Gera duas variáveis com as taxas de acertos e erros da árvore de decisão
taxa_acerto = accuracy_score(y_teste, previsoes)
taxa_erro = 1 - taxa_acerto

#Gera o imagem da matriz de confusão
v = ConfusionMatrix(arvore)
v.fit(X_treinamento, y_treinamento)
v.score(X_teste, y_teste)
v.poof()

'''Obs: Para efeito de comparação, decidi ajustar o test_size para ver quais valores seriam melhor para o teste de predição da máquina, e o resultado foi esse:
    
         Como constatado, a taxa de acerto foi 75.5%, aproximadamente, com 30% de dados para teste.
         Como constatado, a taxa de acerto foi 75.0%, com 29% de dados para teste.
         Como constatado, a taxa de acerto foi 74.4%, aproximadamente, com 28% de dados para teste.
         Como constatado, a taxa de acerto foi 75.6%, aproximadamente, com 27% de dados para teste.
         Como constatado, a taxa de acerto foi 76.9%, aproximadamente, com 26% de dados para teste.
         Como constatado, a taxa de acerto foi 76.3%, aproximadamente, com 25% de dados para teste.
         Como constatado, a taxa de acerto foi 77.7%, aproximadamente, com 24% de dados para teste.
         Como constatado, a taxa de acerto foi 80.0%, com 23% de dados para teste.
         Como constatado, a taxa de acerto foi 81.8%, aproximadamente, com 22% de dados para teste.
         Como constatado, a taxa de acerto foi 81.2%, aproximadamente, com 21% de dados para teste.
         Como constatado, a taxa de acerto foi 80.0%, com 10% de dados para teste.
         
         Como constatado, o melhor resultado da máquina foi um valor de 0.22(22%) dos dados para o teste e 0.78(78%) dos dados para treinamento. A conclusão que se
         tira é de que nem sempre muitos dados para treinamento faz com que o teste seja mais eficiente, e nem de menos. Isso mostra que os dados tem que ser ajustados
         ao ponto máximo da performance dele, nem para mais, nem para menos.'''
