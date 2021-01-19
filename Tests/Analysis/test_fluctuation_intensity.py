# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:14 2021

@author: arsii
"""
import numpy as np
import pytest

from Source.Analysis.fluctuation_intensity import fluctuation_intensity

class TestFluctuationIntensity(object):
    
    def test_fluctuation_intensity(self):
        y_2 = np.array([3,3,3,3,3,3,3])
        y_3 = np.array([2,5,2,5,2,5,2])
        y_4 = np.array([1,1,1,1,7,7,7])
        y_5 = np.array([1,7,1,7,1,7,1])
        y_6 = np.array([1,2,3,4,5,6,7])
        y_7 = np.array([4,5,3,6,2,7,1])   
        assert fluctuation_intensity(y_2,6,7) == pytest.approx(0.0)
        assert fluctuation_intensity(y_3,6,7) == pytest.approx(0.5)
        assert fluctuation_intensity(y_4,6,7) == pytest.approx(0.16666666666666666)
        assert fluctuation_intensity(y_5,6,7) == pytest.approx(1.0)
        assert fluctuation_intensity(y_6,6,7) == pytest.approx(0.027777777777777776)
        assert fluctuation_intensity(y_7,6,7) == pytest.approx(0.5833333333333334)
        
    def test_bad_series(self):
        y_1 = [1,2,3,4,5,6]
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            fluctuation_intensity(y_1,6,6)
        expected_error_msg = "Given time series is not a numpy array."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_bad_scale(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            fluctuation_intensity(y_1,float(6),6)
        expected_error_msg = "Given scale is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_bad_window(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            fluctuation_intensity(y_1,6,"6")
        expected_error_msg = "Given window length is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_neg_scale(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            fluctuation_intensity(y_1,-6,6)
        expected_error_msg = "Given scale is negative."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_large_window(self):
        y_1 = np.array([1,2,3,4,5,6])
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            fluctuation_intensity(y_1,6,10)
        expected_error_msg = "Improper window length."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)