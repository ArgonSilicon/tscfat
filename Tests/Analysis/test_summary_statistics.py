#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:16 2021

@author: arsii
"""
import pytest

from Source.Analysis.summary_statistics import summary_statistics, _plot_summary 
from Source.Utils.argument_loader import setup_pd, setup_ps


class TestSummaryStatistics(object):
    
    def test_summary_statistics(self):
        """
        Test Summary_statistics function. Test that Pandas data frame as an
        Sargument raises an error.
    
        Returns
        -------
        None.
    
        """
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            summary_statistics(setup_pd(),'Test title', savepath = False, savename = False, test = True)
        expected_error_msg = "Series is not a pandas Series."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
class TestSummaryPlot(object):
    
    def test_summary_plot(self):
        
        test_argument = setup_ps()
        res = _plot_summary(test_argument, title="test", test=True)
        assert res is not None, "Returned figure is None type."