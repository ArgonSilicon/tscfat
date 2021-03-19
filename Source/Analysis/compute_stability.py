#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 09:57:53 2021

@author: arsi
"""
import numpy as np

def compute_stability(simmat, edge = 7):
    """
    

    Parameters
    ----------
    simmat : TYPE
        DESCRIPTION.
    edge : TYPE, optional
        DESCRIPTION. The default is 7.

    Returns
    -------
    stability : TYPE
        DESCRIPTION.

    """
    N = simmat.shape[0]
    M = 2*edge + 1
    
    stability = np.zeros(N)
    
    simmat_padded  = np.pad(simmat,edge,mode='constant')

    for i in range(N):
        A = simmat_padded[i:i+M, i:i+M]
        stability[i] = np.median(A[np.triu_indices_from(A, k=1)])
 
    return stability