#!/usr/bin/env python

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score

np.random.seed(0)

precio_leche_pp_pib = pd.read_csv('./data/precio_leche_pp_pib.csv')
precio_leche_pp_pib.drop(['mes_ano'], axis = 1, inplace = True)

X = precio_leche_pp_pib.drop(['Precio_leche'], axis = 1)
y = precio_leche_pp_pib['Precio_leche']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

pipe = Pipeline([('scale', StandardScaler()),
                 ('selector', SelectKBest(mutual_info_regression)),
                 ('poly', PolynomialFeatures()),
                 ('model', Ridge())])

k = [3, 4, 5, 6, 7, 10]
alpha = [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
poly = [1, 2, 3, 5, 7]
param = dict(selector__k = k, poly__degree = poly, model__alpha = alpha)

grid = GridSearchCV(estimator = pipe, param_grid = param, cv = 3, scoring = 'r2')
grid.fit(X_train, y_train)
y_predicted = grid.predict(X_test)

grid.best_params_
X_train.columns[grid.best_estimator_.named_steps['selector'].get_support()]

pickle.dump(grid, open('model.pkl', 'wb'))
