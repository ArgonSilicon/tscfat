#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:47:09 2020

@author: arsi
"""


from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Joint
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation

data_points_x = [0.9, 0.1, 0.2, 0.3, 0.5, 1.7, 0.4, 0.8, 1.5]
time_series_x = TimeSeries(values1,
                           embedding_dimension=2,
                           time_delay=1)
data_points_y = [0.3, 1.3, 0.6, 0.2, 1.1, 1.9, 1.3, 0.4, 0.7, 0.9, 1.6]

time_series_y = TimeSeries(values3,
                           embedding_dimension=2,
                           time_delay=2)

time_series = (time_series_x,
               time_series_x)

settings = Settings(time_series,
                    analysis_type=Cross,
                    neighbourhood=FixedRadius(0.9),
                    similarity_measure=EuclideanMetric,
                    theiler_corrector=0)

computation = RQAComputation.create(settings,
                                    verbose=True)
result = computation.run()
result.min_diagonal_line_length = 2
result.min_vertical_line_length = 2
result.min_white_vertical_line_length = 2
print(result)