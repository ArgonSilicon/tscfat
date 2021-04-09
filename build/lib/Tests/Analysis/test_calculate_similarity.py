#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:19:59 2021

@author: arsii

Test function for similarity calculation.

"""
import os
import pytest
import numpy as np

cwd = os.getcwd()
print(cwd)

from tscfat.Utils.argument_loader import setup_np, setup_pd
from tscfat.Analysis.calculate_similarity import calculate_similarity, calculate_distance

class TestCalculateSimilarity(object):
    
    def test_calculate_distance(self):
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
        
    def test_calculate_similarity_proper(self):
        """
        Test calculate distance with proper argument.

        Returns
        -------
        None.

        """
                
        test_argument = np.array([[1,0.5,0],[0.5,1,0.5],[0,0.5,1]])
        Y_sim = calculate_distance(test_argument)
        
        assert isinstance(Y_sim, np.ndarray)
    
    def test_calculate_similarity(self):
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
        
    def test_calculate_distance_proper(self):
        """
        Test calculate similarity with proper argument.

        Returns
        -------
        None.

        """
        
        test_argument = np.array([[1,0.5,0],[0.5,1,0.5],[0,0.5,1]])
        Y_dis = calculate_distance(test_argument)
        
        assert isinstance(Y_dis, np.ndarray)
