#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:23:21 2021

@author: ikaheia1
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
SUMMARY_BASE = 'aware_'

# ROLLING STATISTICS:
# Output folder for Rolling statistics
ROLLING_OUT = Path('/u/26/ikaheia1/unix/Documents/tscfat/Results/RollingStatistics')
# BAse name for summary statistics image
ROLLING_BASE = 'aware_'

#%% Analysis parameters -> CHANGE THESE!!!

# SUMMARY STATISTICS:
# Rolling window length
SUMMARY_WINDOW = 14

# ROLLING STATISTICS:
# Rolling window length
ROLLING_WINDOW = 28

#%% Create a filename object -> DO NOT CHANGE!!!
fn = FileNames()

fn.add('csv_path',CSV_PATH)

fn.add('summary_out', SUMMARY_OUT)
fn.add('summary_base', SUMMARY_BASE)

fn.add('rolling_out', ROLLING_OUT)
fn.add('rolling_base', ROLLING_BASE)


#%% Create an Analysis Parameters object -> DO NOT CHANGE!!!
ap = AnalysisParameters()

ap.add('summary_window', SUMMARY_WINDOW)

ap.add('rolling_window', ROLLING_WINDOW)