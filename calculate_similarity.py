#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:28:09 2020

@author: arsi
"""
from scipy.spatial.distance import pdist, squareform
import numpy as np

def calculate_similarity(X,metric):
    
    """
    

    Parameters
    ----------
    X : TYPE
        DESCRIPTION.
    metric : TYPE
        DESCRIPTION.

    Returns
    -------
    Y_sim : TYPE
        DESCRIPTION.

    """
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    Y_sim = 1 / (1+Y_square)
    return Y_sim

def calculate_distance(X,metric):
    
    """
    
    Parameters
    ----------
    X : TYPE
        DESCRIPTION.
    metric : TYPE
        DESCRIPTION.

    Returns
    -------
    Y_square : TYPE
        DESCRIPTION.

    """
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    return Y_square

