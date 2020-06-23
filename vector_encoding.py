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

def decode_string(cell_value):
    cell_value = str(cell_value)
    if (cell_value == 0 or cell_value.lower() == "nan" or cell_value.lower() == "no"):
        ret = int(0)
    else:
        ret = int(1)
    return ret

def decode_string_3(cell_value):
    splitted = cell_value.split()
    cleaned = [''.join(filter(str.isalnum, s)).lower() for s in splitted]
    ret = cleaned.count('yes')   
    return ret  

def custom_resampler(array_like):
    return array_like.values               