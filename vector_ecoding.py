# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:29:20 2020

@author: arsii
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

def one_hot_encoding(ts):
    return None

def ordinal_encoding(ts):
    enc = OrdinalEncoder()
    enc.fit(ts)
    print(enc.categories)
    enc.transform(ts)
    return ts
