#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:47:09 2020

@author: arsi
"""

from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic, Cross
from pyrqa.neighbourhood import FixedRadius, RadiusCorridor
from pyrqa.computation import JRQAComputation
from pyrqa.metric import MaximumMetric, TaxicabMetric, EuclideanMetric
from pyrqa.settings import JointSettings
from pyrqa.computation import RPComputation, JRPComputation

def Calculate_JRQA(ts_x,ts_y):
    """
    Create a joint recurrence plot object containing RQA results and a recurrence
    matrix
    
    Parameters
    ----------
    ts_x : numpy array
        timeseries must be a numpy array of a shape (time,features)
    ts_y : numpy array
        timeseries must be a numpy array of a shape (time,features)
    
    additional parameters?

    Returns
    -------
    result : pyrqa.result.RQAResult
        An object containing the recurrence matrix and precalculated metrics. 
    rec_mat : numpy.ndarray
        A recurcion matrix array
    """

    time_series_1 = TimeSeries(ts_x,
                           embedding_dimension=1,
                           time_delay=1)
    
    settings_1 = Settings(time_series_1,
                      analysis_type=Classic,
                      neighbourhood=FixedRadius(2),
                      similarity_measure=MaximumMetric,
                      theiler_corrector=0)

    
    time_series_2 = TimeSeries(ts_y,
                             embedding_dimension=1,
                             time_delay=1)


    settings_2 = Settings(time_series_2,
                      analysis_type=Classic,
                      neighbourhood=FixedRadius(2),
                      similarity_measure=MaximumMetric,
                      theiler_corrector=0)

    joint_settings = JointSettings(settings_1,
                    settings_2)

    computation = JRQAComputation.create(joint_settings,
                                     verbose=False)

    result = computation.run()
    result.min_diagonal_line_length = 2
    result.min_vertical_line_length = 1
    result.min_white_vertical_line_length = 2
    
    computation_2 = JRPComputation.create(joint_settings)
    result_2 = computation_2.run()
    cross_rec_mat = result_2.recurrence_matrix
    
    return result, cross_rec_mat

if __name__ == "__main__":
    pass




    



