#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:15 2021

@author: arsii
"""
import pytest
import numpy as np

from Source.Utils.argument_loader import setup_np, setup_pd
from Source.Analysis.plot_similarity import plot_similarity

class TestPlotSimilarity(object):
    
    def test_bad_arguments(self):
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            plot_similarity(setup_pd(),setup_np(),test=True)
        expected_error_msg = "Similarity matrix type is not np.ndarray."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            plot_similarity(setup_np(),setup_pd(),test=True)
        expected_error_msg = "Novelty score array type is not np.ndarray."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)

    def test_plot_similarity(self):
    
        simmat = np.eye(5)
        novelty = np.ones(5).reshape(1,-1)
        ker = np.array([[1,1,0,-1,-1],
                        [1,1,0,-1,-1],
                        [0,0,0,0,0],
                        [-1,-1,0,1,1],
                        [-1,-1,0,1,1]])
        ret = plot_similarity(simmat,novelty, savepath = False, savename = False, kernel = ker, axis = None, test = True)
        assert ret is not None