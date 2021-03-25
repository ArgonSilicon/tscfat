#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 16:08:46 2021

@author: arsi
"""

import pytest
import numpy as np

from Source.Utils.process_decorator import process_decorator
from Source.Utils.argument_loader import setup_pd

class TestProcessDecorator(object):
    
    """
    def test_bad_arguments(self):
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            process_decorator(print("str",[]))
        expected_error_msg = "Given argument df is not a pandas dataframe."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            process_decorator(print(setup_pd(),{}))
        expected_error_msg = "Given argument cols is not a list."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        
    """
