
def normal_dist(x , mean , sd):
    y = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return y

def GNBC(df_train, df_test):
    # deljenje training_data na dataframe-ove gde su winner1 i winner2:
    #pravljenje dva prazna dataframe-a
    df_train_1 = pd.DataFrame(columns = ['PC1', 'PC2', 'PC3', 'winner'])
    df_train_2 = pd.DataFrame(columns = ['PC1', 'PC2', 'PC3', 'winner'])

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