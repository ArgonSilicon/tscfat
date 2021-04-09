#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:09 2021

@author: arsii

Test for time series decomposition.

"""

import pytest

from tscfat.Utils.argument_loader import setup_np, setup_pd
from tscfat.Analysis.decompose_timeseries import STL_decomposition, _plot_decomposition

class TestDecomposeTimeseries(object):
                
    def test_STL_decomposition(self):
        """ Test STL_decomposition function. Test passes with proper arguments
        and raises an AssertionError if the input time series is not numpy 
        array.
    
        Returns
        -------
        None.
    
        """
        
        res = STL_decomposition(setup_np(),'Test title', test=True) 
        assert res is not None
        assert res.observed.all() is not None
        assert res.trend.all() is not None
        assert res.seasonal.all() is not None
        assert res.resid.all() is not None
        
        test_argument = setup_pd()
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            STL_decomposition(test_argument,'Test title', test=True)
        expected_error_msg = "Series is not a numpy array."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
    def test_STL_decomposition_proper(self):
        """ Test that the STL_decomposition returns something.
        

        Returns
        -------
        None.

        """
        
        test_argument = setup_np()
        res = STL_decomposition(test_argument,'Test title', test=True)
        
        assert res is not None

    def test_plot_decomposition(self):
        """ Test that the _plot_decomposition returns something.
        

        Returns
        -------
        None.

        """
        
        test_argument = setup_np()
        res = STL_decomposition(test_argument,'Test title', test=True)
        fig = _plot_decomposition(res,
                                  title="test",
                                  savepath = False,
                                  savename = False,
                                  dates = False,
                                  test = True,
                                  )
        assert fig is not None