#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:52:40 2021

@author: ikaheia1

Tests for argument loader.
    1) setup_pd should return a pandas dataframe
    2) setup_ps should return a pandas series
    3) setup_np shoulf return a numpy array

"""

import numpy as np
import pandas as pd

from tscfat.Utils.argument_loader import setup_pd, setup_np, setup_ps

class TestProcessDecorator(object):
    
    def test_setup_pd(self):
        """
        Test that setup_pd function returns a pandas dataframe

        Returns
        -------
        None.

        """
        
        test_argument = setup_pd()
        
        assert isinstance(test_argument, pd.DataFrame)
    
    def test_setup_ps(self):
        """
        Test that setup_pd function returns a pandas series

        Returns
        -------
        None.

        """
        
        test_argument = setup_ps()
        
        assert isinstance(test_argument, pd.Series)

    def test_setup_np(self):
        """
        Test that setup_pd function returns a numpy array.

        Returns
        -------
        None.

        """
        
        test_argument = setup_np()
        
        assert isinstance(test_argument, np.ndarray)
        