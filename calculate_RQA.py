#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:45:46 2020

@author: arsi
"""

from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
from pyrqa.computation import RPComputation


def Calculate_RQA(ts,ED,TD,RA):
    """
    Create a recurrence plot object containing RQA results and a recurrence
    matrix
    
    Parameters
    ----------
    ts : numpy array
        timesieries must be a numpy array of a shape (time,features)
    
    additional parameters?

    Returns
    -------
    result : pyrqa.result.RQAResult
        An object containing the recurrence matrix and precalculated metrics. 
    rec_mat : numpy.ndarray
        A recurcion matrix array
    """
    
    time_series = TimeSeries(ts,
                             embedding_dimension=ED,
                             time_delay=TD)
    
    settings = Settings(time_series,
                        analysis_type=Classic,
                        neighbourhood=FixedRadius(0.85),
                        similarity_measure=EuclideanMetric,
                        theiler_corrector=1)
    
    computation_1 = RQAComputation.create(settings,
                                        verbose=False)
    result = computation_1.run()
    result.min_diagonal_line_length = 2
    result.min_vertical_line_length = 2
    result.min_white_vertical_line_length = 2
    
    computation_2 = RPComputation.create(settings)
    result_2 = computation_2.run()
    rec_mat = result_2.recurrence_matrix
    
    return result, rec_mat

if __name__ == "__main__":
    pass

