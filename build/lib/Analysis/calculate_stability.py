#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 09:57:53 2021

@author: arsi

Calculate a rolling window stability index value for given timeseries.
Function requires a similairty matrix for the calculation.
Reference for the stability index:
https://www.nature.com/articles/s41537-020-00123-2

"""

import numpy as np

def compute_stability(simmat, edge = 7):
    """ Calculate stability index for given similarity matrix,
    that represents a timeseries.

    Parameters
    ----------
    simmat : np.array
        Similarity / self-similarity matrix
    edge : int, optional
        Window size used for stability calculation. The default is 7.

    Returns
    -------
    stability : np.array
        An array containing the rolling stability index values..

    """
    assert isinstance(edge, int), "Edge is not an integer."
    assert edge > 0, "Edge should be positive, non zero integer."
    assert isinstance(simmat, np.ndarray), "Self similarity matrix is not a numpy array."
    assert np.ndim(simmat) == 2, "Self similarity matrix is not 2-dimensional."
    assert simmat.shape[0] == simmat.shape[1], "Self similarity matrix is not square."
    assert 2*edge + 1 <= simmat.shape[0], "Kernel size is larger than the self similarity matrix."

    N = simmat.shape[0]
    M = 2*edge + 1

    stability = np.zeros(N)

    simmat_padded = np.pad(simmat, edge, mode='constant')

    for i in range(N):
        A = simmat_padded[i:i+M, i:i+M]
        stability[i] = np.median(A[np.triu_indices_from(A, k=1)])

    return stability
