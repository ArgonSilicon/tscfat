#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:28:09 2020

@author: arsi

Functions for distance matrix and similarity matrix calculation.

"""
from scipy.spatial.distance import pdist, squareform
import numpy as np
from Source.Utils.argument_loader import setup_pd, setup_np
import pytest



def calculate_similarity(X,metric='Euclidean'):        
    """
    Calculate similarity matrix. Utilize numpy pdist function. 
    Full reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html

    Parameters
    ----------
    X : Numpy ndarray
        An m by n array of m original observations in an n-dimensional space.

        
    metric : str or function, optional
            The default is "Euclidean"-

    Returns
    -------
    Y_sim : Numpy ndarray
            Returns a similarity matrix Y. 
            

    """
    
    assert isinstance(X, np.ndarray), "Data format is not a numpy array."
    assert np.ndim(X) == 2, "Matrix is not 2 dimensional."
    
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    Y_sim = 1 / (1+Y_square)
    return Y_sim

def calculate_distance(X,metric="Euclidean"):
    
    """
    Calculate similarity matrix. Utilize numpy pdist function. 
    Full reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html

    Parameters
    ----------
    X : Numpy ndarray
        An m by n array of m original observations in an n-dimensional space.

        
    metric : str or function, optional
            The default is "Euclidean"-

    Returns
    -------
    Y_square : Numpy ndarray
            Returns a condensed distance matrix Y.

    """
    
    assert isinstance(X, np.ndarray), "Data format is not a numpy array."
    assert np.ndim(X) == 2, "Matrix is not 2 dimensional."
    
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    return Y_square

def test_distance():
    """
    Test calculate_distance function. The test fails when:
        - Given array is not a numpy array
        - Given array is not 2 dimensional 

    Returns
    -------
    None.

    """
    test_argument = setup_pd()
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        calculate_distance(test_argument)
    expected_error_msg = "Data format is not a numpy array."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    test_argument2 = setup_np()
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        calculate_distance(test_argument2)
    expected_error_msg = "Matrix is not 2 dimensional."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
def test_similarity():
    """
    Test calculate_similarity function. The test fails when:
        - Given array is not a numpy array
        - Given array is not 2 dimensional 

    Returns
    -------
    None.

    """
    test_argument = setup_pd()
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        calculate_similarity(test_argument)
    expected_error_msg = "Data format is not a numpy array."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    test_argument2 = setup_np()
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        calculate_similarity(test_argument2)
    expected_error_msg = "Matrix is not 2 dimensional."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)