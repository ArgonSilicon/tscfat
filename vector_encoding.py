# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:29:20 2020

@author: arsii
"""

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

def one_hot_encoding(timeseries):
    enc = OneHotEncoder(handle_unknown="ignore")
    enc.fit(timeseries)
    transformed = enc.transform(timeseries).toarray()
    return transformed

def ordinal_encoding(timeseries):
    enc = OrdinalEncoder()
    enc.fit(timeseries)
    transformed = enc.transform(timeseries)
    return transformed
