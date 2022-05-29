import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def loss(y,y_predicted):
    loss = -np.mean(y*(np.log(y_predicted)) - (1-y)*np.log(1-y_predicted))
    return loss

def izvodi(x,y,y_predicted):

    derivative_weights = (1 / len(y)) * np.dot(x.T, (y_predicted - y))  # ispred X.T i sume moze da stoji neki koeficijent =1,2..
    derivative_bias = (1 / len(y)) * np.sum(y_predicted - y)  # proveri da li treba X.T
    return derivative_weights, derivative_bias

def logistic_regresion(x, y, bs, n_steps, lr):
    m, n = x.shape
    w = np.zeros((n, 1))
    b = 0
    y = y.reshape(m, 1)

    #x = normalize(X)

    losses = []

    for step in range(n_steps):
            y_out = sigmoid(np.dot(x, w) + b)
            derivative_w, derivative_b = izvodi(x, y, y_out)

            w -= lr * derivative_w
            b -= lr * derivative_b

            l = loss(y, sigmoid(np.dot(x, w) + b))
            losses.append(l)
    return w, b, losses


def normalizacija(X):
    for i in range(len(X)):
        X = (X - X.mean(axis=0))/X.std(axis=0)

    return X

def fit(X, w,b):
    #x = normalize(X)
    predictions = sigmoid(np.dot(X, w) + b)
    classes = [1 if i > 0.5 else 0 for i in predictions]
    return classes



