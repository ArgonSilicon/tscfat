#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:54:12 2020

Function for time series novelty score calculation. Function requires a 
similairty matrix and calculates the novelty score with sliding windows 
gaussian kernel. For further reference, check:
https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S4_NoveltySegmentation.html   

"""

import numpy as np

def _create_kernel(edge, sigma=1.0, mu=0.0):
    """
    Create a (2*edge+1) x (2*edge+1) gaussian kernel.
    

    Parameters
    ----------
    edge : int, optional
        Gaussian kernel window length / 2. 
    sigma : float, optional
        Variance for the gaussian kernel construction. The default is 1.0.
    mu : float, optional
        Mean for the gaussian kernel construction. The default is 0.0.

    Returns
    -------
    kernel : numpy ndarray
        2D gaussian convolution kernel.

    """   
    assert isinstance(edge,int), "Edge is not an integer."
    assert edge > 0, "Edge should be positive, non zero integer."
    
    grid = np.linspace(-1, 1, 2*edge + 1)    
    x,y = np.meshgrid(grid,grid)
    d = np.sqrt(x**2 + y**2)
    gaussian_mat = np.exp(-((d - mu)**2 / (2.0 * sigma**2)))
    
    kernel_grid = np.sign(np.linspace(-edge, edge, 2*edge +1))
    signs = np.outer(kernel_grid, kernel_grid)
    signed_gaussian = signs * gaussian_mat
    kernel = signed_gaussian / np.sum(np.abs(signed_gaussian))
    
    return kernel

def compute_novelty(simmat, edge = 7, sigma=1.0, mu = 0.0):
    """
    Compute novelty score using the self similarity matrix and gaussian 
    checkerboard convolution kernel, calculating the convolution along the 
    self similarity matrix diagonal.

    Parameters
    ----------
    simmat : numpy ndarray 
        N x N self similarity matrix. 
    edge : float, optional
        Gaussian kernel window length / 2. The default is 7.
    sigma : float, optional
        Variance for the gaussian kernel construction. The default is 1.0.
    mu : float, optional
        Mean for the gaussian kernel construction. The default is 0.0.

    Returns
    -------
    nov : numpy ndarray
        1D novelty score vector.
    kernel : numpy ndarray
        2D gaussian convolution kernel.

    """
    
    assert isinstance(simmat,np.ndarray), "Self similarity matrix is not a numpy array."
    assert np.ndim(simmat) == 2, "Self similarity matrix is not 2-dimensional."
    assert simmat.shape[0] == simmat.shape[1], "Self similarity matrix is not square."
    assert 2*edge + 1 <= simmat.shape[0], "Kernel size is larger than the self similarity matrix."
    
    kernel = _create_kernel(edge, sigma, mu)
    
    N = simmat.shape[0]
    M = 2*edge + 1
    
    novelty = np.zeros(N)
    
    simmat_padded  = np.pad(simmat,edge,mode='constant')

    for i in range(N):
        novelty[i] = np.sum(simmat_padded[i:i+M, i:i+M] * kernel)
 
    return novelty, kernel


