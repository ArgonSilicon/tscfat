#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:13 2021

@author: arsii

Test for degree distribution calculation.

"""

import numpy as np
import pytest

from tscfat.Analysis.degree_of_distribution import distribution_degree

#TODO! write docstings
class TestDegreeOfDistribution(object):
    
    def test_distribution_degree(self):
        y_1 = np.array([3,5,6,3,3,3,7,5,4])
        y_2 = np.array([3,3,3,3,3,3,3])
        y_3 = np.array([2,5,2,5,2,5,2])
        y_4 = np.array([1,1,1,1,7,7,7])
        y_5 = np.array([1,7,1,7,1,7,1])
        y_6 = np.array([1,2,3,4,5,6,7])
        y_7 = np.array([4,5,3,6,2,7,1])
     
        assert distribution_degree(y_1,6,7) == pytest.approx(0.41666666666666663)
        assert distribution_degree(y_2,6,7) == pytest.approx(0.0)
        assert distribution_degree(y_3,6,7) == pytest.approx(0.5515873015873016)
        assert distribution_degree(y_4,6,7) == pytest.approx(0.6349206349206349)
        assert distribution_degree(y_5,6,7) == pytest.approx(0.6349206349206349)
        assert distribution_degree(y_6,6,7) == pytest.approx(1.0)
        assert distribution_degree(y_7,6,7) == pytest.approx(1.0)
       
    def test_bad_series(self):
        y_1 = [1,2,3,4,5,6]
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            distribution_degree(y_1,6,6)
        expected_error_msg = "Given time series is not a numpy array."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_bad_scale(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            distribution_degree(y_1,float(6),6)
        expected_error_msg = "Given scale is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_bad_window(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            distribution_degree(y_1,6,"6")
        expected_error_msg = "Given window length is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_neg_scale(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            distribution_degree(y_1,-6,6)
        expected_error_msg = "Given scale is negative."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_large_window(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            distribution_degree(y_1,6,10)
        expected_error_msg = "Improper window length."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
      