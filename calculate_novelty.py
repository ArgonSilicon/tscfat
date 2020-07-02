#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:54:12 2020

Inspired by:
Jonathan Foote: Automatic audio segmentation using a measure of audio novelty.
roceedings of the IEEE International Conference on Multimedia and Expo (ICME), 
New York, NY, USA, 2000, pp. 452-455. 
"""

import numpy as np
import matplotlib.pyplot as plt

def checkerboard_kernel(L):
    """Compute box-like checkerboard kernel [FMP, Section 4.4.1]

    Notebook: C4/C4S4_NoveltySegmentation.ipynb

    Args:
        L: Parameter specifying the kernel size M=2*L+1

    Returns:
        kernel: Kernel matrix of size M x M
    """       
    
    axis = np.arange(-L,L+1)
    kernel = np.outer(np.sign(axis),np.sign(axis))
    return kernel

def Gaussian_checkerboard_kernel(L, var=1, normalize=True): 
    """Compute Guassian-like checkerboard kernel [FMP, Section 4.4.1]
    See also: https://scipython.com/blog/visualizing-the-bivariate-gaussian-distribution/

    Notebook: C4/C4S4_NoveltySegmentation.ipynb

    Args:
        L: Parameter specifying the kernel size M=2*L+1
        var: Variance parameter determing the tapering (epsilon)

    Returns:
        kernel: Kernel matrix of size M x M
    """  
    taper = np.sqrt(1/2)/(L*var)
    axis = np.arange(-L,L+1)
    gaussian1D = np.exp(-taper**2 * (axis**2))
    gaussian2D = np.outer(gaussian1D,gaussian1D)
    kernel_box = np.outer(np.sign(axis),np.sign(axis))
    kernel = kernel_box * gaussian2D
    
    if normalize:     
        kernel = kernel / np.sum(np.abs(kernel))
    
    return kernel

def compute_novelty_SSM(S, kernel=None, L=10, var=0.5, exclude=False):
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
    if kernel is None:
        kernel = Gaussian_checkerboard_kernel(L=L, var=var)
        
    N = S.shape[0]
    M = 2*L + 1
    nov = np.zeros(N)
    
    S_padded  = np.pad(S,L,mode='constant')
    
    for n in range(N):
        nov[n] = np.sum(S_padded[n:n+M, n:n+M]  * kernel)
    
    if exclude:
        right = np.min([L,N])
        left = np.max([0,N-L])
        nov[0:right] = 0
        nov[left:N] = 0
        
    return nov

if __name__ == "__main__":
    
    # test with an ordinary checkerboard kernel
    L = 10
    kernel = compute_kernel_checkerboard_box(L)
    plt.figure(figsize=(4,3))
    plt.imshow(kernel, aspect='auto', origin='lower', 
               extent=[-L-0.5,L+0.5,-L-0.5,L+0.5], cmap='seismic')
    plt.colorbar()
    plt.tight_layout()
    
    # check with gaussian checkerboard kernel
    L = 10
    var = 0.5
    kernel = compute_kernel_checkerboard_Gaussian(L, var)
    plt.figure(figsize=(4,3))
    plt.imshow(kernel, aspect='auto', origin='lower', 
               extent=[-L-0.5,L+0.5,-L-0.5,L+0.5], cmap='seismic')
    plt.colorbar()
    plt.tight_layout()