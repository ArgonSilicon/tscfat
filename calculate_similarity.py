#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:28:09 2020

@author: arsi
"""
from scipy.spatial.distance import pdist, squareform
import numpy as np

def calculate_similarity(X,metric):
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    Y_sim = 1 / (1+Y_square)
    return Y_sim
    
def EDM(A,B):
    p1 = np.sum(A**2, axis=1)[:,np.newaxis]
    p2 = np.sum(B**2,axis=1)
    p3 = -2 * np.dot(A,B.T)
    return np.round(np.sqrt(p1+p2+p3),2)