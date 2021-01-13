#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:54:12 2020

Calculate similarity novelty score using checkerboard Gaussian kernel 
convolution. plot the results in one figure.
Inspired by:
Jonathan Foote: Automatic audio segmentation using a measure of audio novelty.
roceedings of the IEEE International Conference on Multimedia and Expo (ICME), 
New York, NY, USA, 2000, pp. 452-455. 
"""

import numpy as np

def compute_novelty_SSM(simmat, L=10, var=1.0, exclude=False):
    """Compute novelty function from SSM [FMP, Section 4.4.1]

    Notebook: C4/C4S4_NoveltySegmentation.ipynb

    Args:
        S: SSM
        kernel: Checkerboard kernel (if kernel==None, it will be computed)
        L: Parameter specifying the kernel size M=2*L+1
        var: Variance parameter determing the tapering (epsilon)
        exclude: Sets the first L and last L values of novelty function to zero

    Returns:
        nov: Novelty function
    """    
    grid = np.linspace(-1,1,2*L+1)    
    v = np.meshgrid(grid,grid)
    d = np.sqrt(v*v + v*v)
    sigma = 1.0
    mu = 0.0
    gaussian_2D = np.exp(-((d - mu)**2 / (2.0 * sigma**2)))
    
    kernel_grid = np.sign(np.linspace(-L,L,2*L+1))
    signs = np.outer(kernel_grid,kernel_grid)
    kernel = signs * gaussian_2D
    kernel = kernel / np.sum(np.abs(kernel))
        
    
    N = simmat.shape[0]
    M = 2*L + 1
    nov = np.zeros(N)
    
    S_padded  = np.pad(simmat,L,mode='constant')
    
    for n in range(N):
        nov[n] = np.sum(S_padded[n:n+M, n:n+M]  * kernel)
    
    if exclude:
        right = np.min([L,N])
        left = np.max([0,N-L])
        nov[0:right] = 0
        nov[left:N] = 0
        
    return nov, kernel

if __name__ == "__main__":
    pass    
