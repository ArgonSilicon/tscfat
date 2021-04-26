#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:17:54 2021

@author: arsii
"""

import pandas as pd
from scipy import stats

from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import mutual_info_score

#%%
a = df[(df['id'] == 8) & (df['type'] == 'valence')].value.values
b = df[(df['id'] == 8) & (df['type'] == 'arousal')].value.values
print(mutual_info_score(b,b))
#%%
print(stats.entropy([0.5,0.5])) # entropy of 0.69, expressed in nats
print(mutual_info_classif(a.reshape(-1,1), b)) # mutual information of 0.69, expressed in nats
print(mutual_info_score(a,b))

#%%
def calc_MI(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi

print(calc_MI(a,b,10))
print(calc_MI(a,a,10))
print(calc_MI(b,b,10))