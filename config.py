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
doi = (2020,10,1),(2020,12,24)


#%% Filenames -> CHANGE THESE!!!

# DATA LOADING:
# Path to the data file to be imported
CSV_PATH = Path('/u/26/ikaheia1/data/Documents/Data/Combined_data.csv')

# SUMMARY STATISTICS:
# Output folder for summary statistics
SUMMARY_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/Summary')
# BAse name for summary statistics image
SUMMARY_BASE = 'aware_similarity_'

# ROLLING STATISTICS:
# Output folder for Rolling statistics
ROLLING_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/RollingStatistics')
# BAse name for summary statistics image
ROLLING_BASE = 'aware_similarity_'

# TIMESERIES DECOMPOSITION:
# Output folder for Decomposition
DECOMPOSITION_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/Decomposition')
# BAse name for summary statistics image
DECOMPOSITION_BASE = 'aware_similarity_'

# SIMILARITY, NOVELTY, AND STABILITY
# Output folder for similarity plot
SIMILARITY_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/Similarity')
# BAse name for summary statistics image
SIMILARITY_BASE = 'aware_similarity_'

# TIMESERIES CLUSTERING
# Output folder for similarity plot
CLUSTERING_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/Clustering')
# BAse name for summary statistics image
CLUSTERING_BASE = 'aware_similarity_'

# PLOT SELECTED TIMESERIES
# Output folder for similarity plot
PLOT_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/Plotting')
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

#%% Create a filename object -> DO NOT CHANGE!!!
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


#%% Create an Analysis Parameters object -> DO NOT CHANGE!!!
ap = AnalysisParameters()

ap.add('summary_window', SUMMARY_WINDOW)

ap.add('rolling_window', ROLLING_WINDOW)