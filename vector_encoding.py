# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:29:20 2020

@author: arsii
"""

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

#TODO: fill docstrings

def one_hot_encoding(timeseries):
    """
    

    Parameters
    ----------
    timeseries : TYPE
        DESCRIPTION.

    Returns
    -------
    transformed : TYPE
        DESCRIPTION.

    """
    enc = OneHotEncoder(handle_unknown="ignore")
    enc.fit(timeseries)
    transformed = enc.transform(timeseries).toarray()
    return transformed

def ordinal_encoding(timeseries):
    """
    

    Parameters
    ----------
    timeseries : TYPE
        DESCRIPTION.

    Returns
    -------
    transformed : TYPE
        DESCRIPTION.

    """
    enc = OrdinalEncoder()
    enc.fit(timeseries)
    transformed = enc.transform(timeseries)
    return transformed

def decode_string(cell_value):
    """
    

    Parameters
    ----------
    cell_value : TYPE
        DESCRIPTION.

    Returns
    -------
    ret : TYPE
        DESCRIPTION.

    """
    cell_value = str(cell_value)
    if (cell_value == 0 or cell_value.lower() == "nan" or cell_value.lower() == "no"):
        ret = int(0)
    else:
        ret = int(1)
    return ret

def decode_string_3(cell_value):
    """
    

    Parameters
    ----------
    cell_value : TYPE
        DESCRIPTION.

    Returns
    -------
    ret : TYPE
        DESCRIPTION.

    """
    splitted = cell_value.split()
    cleaned = [''.join(filter(str.isalnum, s)).lower() for s in splitted]
    ret = cleaned.count('yes')   
    return ret  

def custom_resampler(array_like):
    """
    

    Parameters
    ----------
    array_like : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return array_like.values               

def normalize_values(array,maximum=1,minimum=0):
    """
    

    Parameters
    ----------
    array : TYPE
        DESCRIPTION.
    maximum : TYPE, optional
        DESCRIPTION. The default is 1.
    minimum : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    X_scaled : TYPE
        DESCRIPTION.

    """
    X = array.reshape(-1,1)

    X_std = (X -X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

    X_scaled = X_std * (maximum - minimum) + minimum
    
    return X_scaled