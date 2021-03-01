#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:54:12 2020

 
"""

import numpy as np
import pytest

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

def test_compute_novelty():
    """
    Test compute novelty function:
        - Proper arguments return non-empty novelty score array and kernel.
        - Self similarity matrix given as array raises an error
        - 1D self similarity matrix raises an error
        - Non-square self similarity matrix raises an error
        - Kernel size larger than the self similarity matrix raises an error

    Returns
    -------
    None.

    """
    import numpy as np
    test_argument = np.random.rand(5,5)
    np.fill_diagonal(test_argument,1)
    nov,ker = compute_novelty(test_argument,edge=1)
    assert nov is not None
    assert ker is not None
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        compute_novelty([[1,0,0],[0,1,0],[0,0,1]])
    expected_error_msg = "Self similarity matrix is not a numpy array."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    with pytest.raises(AssertionError) as exc_info:
        compute_novelty(np.array([1,0,0]))
    expected_error_msg = "Self similarity matrix is not 2-dimensional."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    with pytest.raises(AssertionError) as exc_info:
        compute_novelty(np.random.rand(3,2))
    expected_error_msg = "Self similarity matrix is not square."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    with pytest.raises(AssertionError) as exc_info:
        compute_novelty(np.random.rand(3,3),edge=10)
    expected_error_msg = "Kernel size is larger than the self similarity matrix."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
      

def test_create_kernel():
    """
    Test create kernel function:
        - Proper arguments yield an N x N numpy array
        - Edge given as float raises an error
        - Negative edge lenght raises an error

    Returns
    -------
    None.

    """
    res = _create_kernel(7)
    assert isinstance(res,np.ndarray), "Kernel is not a numpy array."
    assert (np.ndim(res) == 2), "Kernel is not a 2D array."
    assert res.shape[0]  == res.shape[1], "Kernel is not a square matrix." 
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        _create_kernel(float(1))
    expected_error_msg = "Edge is not an integer."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    with pytest.raises(AssertionError) as exc_info:
        _create_kernel(-1)
    expected_error_msg = "Edge should be positive, non zero integer."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    
