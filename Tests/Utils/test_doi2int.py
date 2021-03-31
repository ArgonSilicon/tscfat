#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:08:46 2021

@author: arsi

Test for doi2int function.

"""

import pytest

from tscfat.Utils.doi2int import doi2index
from tscfat.Utils.argument_loader import setup_pd, setup_np

class TestDoi2Int(object):
        
    def test_doi2int(self):
        """
        Test with proper arguments.

        Returns
        -------
        None.

        """
        df = setup_pd()
        test_argument = (2011,3,1),(2011,6,1)
        a,b = doi2index(test_argument, df)
        
        assert a == pytest.approx(4478.12331851853)
        assert b == pytest.approx(4570.12331851853)
        
        
    def test_doi2int_bad_arguments(self):
        
        test_argument = (2011,3,1),(2011,6,1)
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            a,b = doi2index(test_argument, setup_np())
        expected_error_msg = "df is not a pandas dataframe."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            a,b = doi2index(123, setup_np())
        expected_error_msg = "Doi is not a tuple."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
       
        
