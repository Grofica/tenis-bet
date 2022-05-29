from PCA import PCA as pca
from sklearn.model_selection import train_test_split
import data_main
import logistic_valjda_konacno
import numpy as np
import pandas as pd

def tacnost(y,predicted):
    return np.sum(y == predicted) / len(y)

atp_2010 = data_main.loading_data('tennis_atp/atp_matches_2010.csv')
atp_2010 = data_main.years_data('tennis_atp/atp_matches_2010.csv',3)
atp_2010 = atp_2010.astype('float')

coli = atp_2010.columns
coli = np.array(coli)

atp_2010 = atp_2010.to_numpy()
labels = atp_2010[:,-1]
labels = np.where(labels == 1, 0, labels)
labels = np.where(labels == 2, 1, labels)

x = atp_2010[:,:-1]
x, variance= pca(x, 3)

x = logistic_valjda_konacno.normalizacija(x) #ide za logisticku regresiju

x_trening, x_test, y_trening, y_test = train_test_split(x, labels, test_size=0.1)

w,b,e = logistic_valjda_konacno.logistic_regresion(x_trening,y_trening,100, 1000, 0.001)
predicted = logistic_valjda_konacno.fit(x_test,w, b)
print('Tacnost logisticke reegresije: ', tacnost(y_test, predicted)*100)
