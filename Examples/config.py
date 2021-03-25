#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:23:21 2021

@author: ikaheia1

Configuration file for datframe containing data from single subject.

    1) General variables
    2) Filenames and paths
    3) Analysis parameters

"""

# imports
from pathlib import Path
from Source.Utils.file_names import FileNames
from Source.Utils.analysis_parameters import AnalysisParameters

#%% General variables -> CHANGE THESE!!!

# The days of interest ((start date), (end date))
# Use the format: (YEAR,DAY,MONTH,HOUR,MINUTE)
#doi = (2020,10,1),(2020,12,24)
doi = (2011,3,1),(2011,6,1)
# The directory where output figures are stored
OUTPUT_DIR = Path('/home/arsi/Documents/tscfat/Results')


#%% Filenames -> CHANGE THESE!!!

# DATA LOADING:
# Path to the data file to be imported
#CSV_PATH = Path('/home/arsi/Documents/Data/Combined_data.csv')
CSV_PATH = Path('/home/arsi/Documents/Data/example_data.csv')

# SUMMARY STATISTICS:
# Output folder for summary statistics
SUMMARY_OUT = OUTPUT_DIR / 'Summary'
# BAse name for summary statistics image
SUMMARY_BASE = 'aware_summary_'

# ROLLING STATISTICS:
# Output folder for Rolling statistics
ROLLING_OUT = OUTPUT_DIR / 'RollingStatistics'
# BAse name for Rolling statistics image
ROLLING_BASE = 'aware_rolling_'

# TIMESERIES DECOMPOSITION:
# Output folder for Decomposition
DECOMPOSITION_OUT = OUTPUT_DIR / 'Decomposition'
# BAse name for timeseriesn decomposition image
DECOMPOSITION_BASE = 'aware_decomposition_'

# SIMILARITY, NOVELTY, AND STABILITY
# Output folder for similarity plot
SIMILARITY_OUT = OUTPUT_DIR / 'Similarity'
# BAse name for similarity image
SIMILARITY_BASE = 'aware_similarity_'

# TIMESERIES CLUSTERING
# Output folder for similarity plot
CLUSTERING_OUT = OUTPUT_DIR / 'Clustering'
# BAse name for clustering image
CLUSTERING_BASE = 'aware_clustering_'

# PLOT SELECTED TIMESERIES
# Output folder for similarity plot
PLOT_OUT = OUTPUT_DIR / 'Timeseries'
# BAse name for summary statistics image
PLOT_BASE = 'aware_timeseries_'

#%% Analysis parameters -> CHANGE THESE!!!

# SUMMARY STATISTICS:
# Rolling window length
SUMMARY_WINDOW = 14

# ROLLING STATISTICS:
# Rolling window length
ROLLING_WINDOW = 28

# TIMESERIES DECOMPOSITION:
# Rolling window length
ROLLING_WINDOW = 28

# SIMILARITY, NOVELTY, STABILITY
# some parameters here

# TIMESERIES CLUSTERING

# TIMESERIES PLOTTING
# Dataframe columns to be plotted as list of lists
COLUMN_LIST = [['positive', 'negative', 'Average HRV'],
               ['positive', 'negative', 'app_sum'],
               ['positive', 'negative', 'screen_activations'],
              ]
#%% Create a filename object -> DO NOT CHANGE THESE!!!
fn = FileNames()

fn.add('csv_path',CSV_PATH)

fn.add('summary_out', SUMMARY_OUT)
fn.add('summary_base', SUMMARY_BASE)

fn.add('rolling_out', ROLLING_OUT)
fn.add('rolling_base', ROLLING_BASE)

fn.add('decomposition_out', DECOMPOSITION_OUT)
fn.add('decomposition_base', DECOMPOSITION_BASE)

fn.add('similarity_out', SIMILARITY_OUT)
fn.add('similarity_base', SIMILARITY_BASE)

fn.add('plotting_out', PLOT_OUT)
fn.add('plotting_base', PLOT_BASE)


#%% Create an Analysis Parameters object -> DO NOT CHANGE!!!
ap = AnalysisParameters()

ap.add('summary_window', SUMMARY_WINDOW)

ap.add('rolling_window', ROLLING_WINDOW)

ap.add('plot_cols', COLUMN_LIST)