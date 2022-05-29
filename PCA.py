import numpy as np
import pandas
import data_main

def PCA(x, num_axis):

    X = x - np.mean(x, axis=0)

    cov_mat = np.cov(X, rowvar=False)
    """
    rowvar parametar funkcije koji ako je False oznacava da su kolone podaci, a redovi samplovi, ako je True suprotno
    ako matrica ima imaginarne brojeve ako clanove, dodati parametar kod eigh funkcije eogvals_only = True
    """

    e_values, e_vectors = np.linalg.eigh(cov_mat)

    indexs = np.argsort(e_values)[::-1]

    sorted_evalue = e_values[indexs]
    toatal = sum(e_values)
    variance = [(i / toatal) * 100 for i in e_values[indexs]]
    sorted_evectors = e_vectors[:,indexs]


    evector_subset = sorted_evectors[:, 0:num_axis]

    X_reduced = np.dot(evector_subset.transpose(), X.transpose()).transpose()

    return X_reduced, variance

"""
atp_2010 = data_main.loading_data('tennis_atp/atp_matches_2010.csv')
atp_2010 = atp_2010.astype('float')
coli = atp_2010.columns

atp_2010 = atp_2010.to_numpy()
labels = atp_2010[:,-1]
X = atp_2010[:,:-1]


components= pca(X,2)
print(components)
"""