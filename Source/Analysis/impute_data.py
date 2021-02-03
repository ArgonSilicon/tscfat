#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:07:04 2021

@author: arsi
"""
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

X = np.array([[1, 2], [3, 6], [4, 8], [np.nan, 3], [7, np.nan]])


imp = IterativeImputer(max_iter=10, random_state=0)

imp.fit(X)

IterativeImputer(random_state=0)

X_test = [[np.nan, 2], [6, np.nan], [np.nan, 6]]

# the model learns that the second feature is double the first
print(np.round(imp.transform(X_test)))
