#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:43:00 2021

@author: arsii

Test function for stability calculation.

"""

import pytest
import numpy as np

from tscfat.Analysis.calculate_stability import compute_stability

class TestCalculateStability(object):
    
    def test_compute_stability(self):
        """
        Test compute stability function:
            - Proper arguments return non-empty stability score.
            - Self similarity matrix given as array raises an error
            - 1D self similarity matrix raises an error
            - Non-square self similarity matrix raises an error
            - Kernel size larger than the self similarity matrix raises an error
            - Edge given as float raises an error
            - Edge given as negative integer raises an error
    
        Returns
        -------
        None.
    
        """
        
        test_argument = np.random.rand(5,5)
        np.fill_diagonal(test_argument,1)
        stab = compute_stability(test_argument,edge=1)
        assert stab is not None
                
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            compute_stability([[1,0,0],[0,1,0],[0,0,1]])
        expected_error_msg = "Self similarity matrix is not a numpy array."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        with pytest.raises(AssertionError) as exc_info:
            compute_stability(np.array([1,0,0]))
        expected_error_msg = "Self similarity matrix is not 2-dimensional."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        with pytest.raises(AssertionError) as exc_info:
            compute_stability(np.random.rand(3,2))
        expected_error_msg = "Self similarity matrix is not square."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        with pytest.raises(AssertionError) as exc_info:
            compute_stability(np.random.rand(3,3),edge=10)
        expected_error_msg = "Kernel size is larger than the self similarity matrix."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
    
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            compute_stability(test_argument,float(1))
        expected_error_msg = "Edge is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        with pytest.raises(AssertionError) as exc_info:
            compute_stability(test_argument,-1)
        expected_error_msg = "Edge should be positive, non zero integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        