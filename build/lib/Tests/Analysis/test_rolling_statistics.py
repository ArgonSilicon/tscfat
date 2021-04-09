# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:15:03 2021

@author: arsii

Test for rolling statistics.

"""
import pytest
import numpy as np

from tscfat.Utils.argument_loader import setup_np, setup_pd, setup_ps
from tscfat.Analysis.rolling_statistics import rolling_statistics, _autocorr

#TODO! write docstrings
#TODO! check test with proper arguments

class TestRollingStatistics(object):
    
    
    def test_rolling_statistics(self):
        """
        Test with proper arguments.
    
        Returns
        -------
        None.
    
        """
        test_argument = setup_pd()
        test_argument = test_argument['level'].to_frame()
        res = rolling_statistics(test_argument, w = 7, savename = False, savepath = False, test = True)
        print(type(res))
        assert res is not None, 'Function returned a None object.' 
    
        
    def test_rolling_statistics_ts(self):
        """
        Given a numpy array, Rolling_statistics raises an error.
    
        Returns
        -------
        None.
    
        """
        test_argument = setup_np()
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            rolling_statistics(test_argument,w=7)
        expected_error_msg = "Timeseries is not a pandas dataframe."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    
    def test_rolling_statistics_w(self):
        """
        Given window size as a string, Rolling_statistics raises an error.
    
        Returns
        -------
        None.
    
        """
        test_argument = setup_pd()
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            rolling_statistics(test_argument,w=str(7))
        expected_error_msg = "Window size is not an integer."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)  
        
    def test_rolling_statistics_long_window(self):
        """
        Given too large window size, Rolling_statistics raises an error.
    
        Returns
        -------
        None.
    
        """
        test_argument = setup_pd()
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            rolling_statistics(test_argument,w=10000000)
        expected_error_msg = "Window length is larger than the time series length."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_autocorr(self):
        test_argument = setup_ps()
        ac = _autocorr(test_argument)
        assert isinstance(ac, np.float64)
    