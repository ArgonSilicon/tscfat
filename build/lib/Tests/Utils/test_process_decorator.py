#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:08:46 2021

@author: arsi
"""

import pytest

from tscfat.Utils.process_decorator import process_decorator
from tscfat.Analysis import summary_statistics
from tscfat.Utils.argument_loader import setup_pd

class TestProcessDecorator(object):
    
    
    def test_process_decorator(self):
        
        @process_decorator
        def summary(df,name):
            ser = df[name] 
            _ = summary_statistics.summary_statistics(ser,
                                                      "{} summary".format(name),
                                                      window = 14,
                                                      savepath = False,
                                                      savename = False,
                                                      test = False)
        
        df = setup_pd()
        cols = ['level']
        summary(df,cols)
        
        
    
        
