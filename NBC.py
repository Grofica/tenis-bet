#Gaussian Naive Bayes Classificator

import math
import random
import pandas as pd
import numpy as np
from pandas.core.reshape.concat import concat
from scipy.stats.stats import _shape_with_dropped_axis
import PCA
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from scipy.stats import norm
import data_main

#ucitavanje

def q_setup(data):
    data = data_main.loading_data(data)
    data = data.astype('float')
    coli = data.columns
    data = data.to_numpy()
    labels = data[:,-1]
    X = data[:,:-1]

    u,v = PCA.PCA(X, 3)

    df = pd.DataFrame(u, columns=['PC1', 'PC2', 'PC3'])
    
    df['winner'] = labels
    print('q_setup done') #test

    return df


#funkcija normalne raspodele
def normal_dist(x , mean , sd):
    y = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return y


def GNBC(df):
    
    #podela na train i test podatke, 4:1
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=25)
    
    #posto su indeksi sada izmesani, moraju da se resetuju
    df_train = df_train.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    # deljenje training_data na dataframe-ove gde su winner1 i winner2:
    #pravljenje dva prazna dataframe-a
    df_train_1 = pd.DataFrame(columns = ['PC1', 'PC2', 'PC3', 'winner'])
    df_train_2 = pd.DataFrame(columns = ['PC1', 'PC2', 'PC3', 'winner'])

    print(df_train)

    #df_train_1 se puni parametrima za koje je winner 1 i obrnuto
    for i in range(len(df_train)):
        if df_train['winner'][i] == 1:
            df_train_1 = df_train_1.append({'PC1':df_train['PC1'][i], 'PC2':df_train['PC2'][i], 'PC3':df_train['PC3'][i], 'winner':df_train['winner'][i]}, ignore_index=True)
        else:
            df_train_2 = df_train_2.append({'PC1':df_train['PC1'][i], 'PC2':df_train['PC2'][i], 'PC3':df_train['PC3'][i], 'winner':df_train['winner'][i]}, ignore_index=True)
    
    #racunanje standardne devijacije i srednje vrednosti za svaku kolonu oba train dataframe-a
    df1_s1 = df_train_1['PC1'].std()
    df1_s2 = df_train_1['PC2'].std()
    df1_s3 = df_train_1['PC3'].std()
    df1_m1 = df_train_1['PC1'].mean()
    df1_m2 = df_train_1['PC2'].mean()
    df1_m3 = df_train_1['PC3'].mean()

    df2_s1 = df_train_2['PC1'].std()
    df2_s2 = df_train_2['PC2'].std()
    df2_s3 = df_train_2['PC3'].std()
    df2_m1 = df_train_2['PC1'].mean()
    df2_m2 = df_train_2['PC2'].mean()
    df2_m3 = df_train_2['PC3'].mean()

    #deljenje df_test od kolone winner
    labels = df_test['winner'].to_numpy()
    del df_test['winner']

    #inicijalizacija 
    good_predictions = 0
    bad_predictions = 0

    #vrsi se predvidjanje za svaki red u df_test 
    for i in range(len(df_test)):
        
        #ucitavanje parametara reda i
        PC1_in = df_test['PC1'][i]
        PC2_in = df_test['PC2'][i]
        PC3_in = df_test['PC3'][i]
        
        #poredjenje ucitanih parametara sa poznatim normalnim raspodelama parametara iz df_train,
        #da bi se izbegao underflow uzima se prirodni logaritam proizvoda verovatnoca
        likelihood1 = math.log(normal_dist(PC1_in, df1_m1, df1_s1) * normal_dist(PC2_in, df1_m2, df1_s2) * normal_dist(PC3_in, df1_m3, df1_s3))
        likelihood2 = math.log(normal_dist(PC1_in, df2_m1, df2_s1) * normal_dist(PC2_in, df2_m2, df2_s2) * normal_dist(PC3_in, df2_m3, df2_s3))
        
        if likelihood1>=likelihood2:
            prediction = 1
        else:
            prediction = 2
        
        if labels[i] == prediction: 
            good_predictions += 1
        else:
            bad_predictions += 1
        
        accuracy = good_predictions/(good_predictions + bad_predictions)
    print('accuracy: ', accuracy*100, "%")
        

df = q_setup('C:/Users/HP/Downloads/tennis_atp-master/atp_matches_futures_2005.csv')

GNBC(df)