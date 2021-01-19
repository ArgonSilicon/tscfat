#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:19:59 2021

@author: arsii
"""

import pytest

from Source.Utils.argument_loader import setup_np, setup_pd
from Source.Analysis.calculate_similarity import calculate_similarity, calculate_distance

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