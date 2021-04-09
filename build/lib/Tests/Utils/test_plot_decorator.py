#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 11:36:22 2021

@author: arsii
"""

import pytest

from tscfat.Utils.plot_decorator import plot_decorator
from tscfat.Analysis.plot_timeseries import plot_timeseries
from tscfat.Utils.argument_loader import setup_pd

class TestPlotDecorator(object):
    
    
    def test_plot_decorator(self):
        
        df = setup_pd()
        name = ['level']
        _ = plot_timeseries(df,
                        name,
                        title = "test title",
                        roll = False, 
                        xlab = "Time", 
                        ylab = "Value", 
                        ylim = False, 
                        savename = False, 
                        savepath = False,
                        highlight = False, 
                        test=True
                        )
    
  