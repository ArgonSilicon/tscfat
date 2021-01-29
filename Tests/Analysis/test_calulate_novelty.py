#!/usr/bin/env python3#
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:19:57 2021

@author: arsii
"""

import pytest
import numpy as np

from Source.Analysis.calculate_novelty import compute_novelty, _create_kernel

class TestCalculateNovelty(object):
    
    def test_compute_novelty(self):
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
      

    def test_create_kernel(self):
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
