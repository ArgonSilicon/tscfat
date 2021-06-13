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

from pathlib import Path

from tscfat.Utils.file_names import FileNames
from tscfat.Utils.analysis_parameters import AnalysisParameters

#%% General variables -> CHANGE THESE!!!

# The days of interest ((start date), (end date))
# Use the format: (YEAR,DAY,MONTH,HOUR,MINUTE)
doi = (2011,3,1),(2011,6,1)

# The directory where output figures are stored
OUTPUT_DIR = Path('/home/arsii/tscfat/Results')

# Path or Url to the data file to be imported
#CSV_PATH = Path('/home/arsii/tscfat/Data/one_subject_data.csv')
CSV_PATH = "https://raw.githubusercontent.com/ArgonSilicon/tscfat/master/Data/one_subject_data.csv"

#%% Filenames -> CHANGE THESE!!!
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
PLOT_OUT = OUTPUT_DIR / 'Timeseries_raw'
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
COLUMN_LIST = [['positive', 'negative', 'Sleep Score'],
               ['positive', 'negative', 'Average Resting Heart Rate'],
               ['positive', 'negative', 'Awake Time'],
               ['positive', 'negative', 'Respiratory Rate'],
               ['positive', 'negative', 'Sleep Efficiency'],
               ['positive', 'negative', 'Sleep Latency'],
               ['positive', 'negative', 'Total Bedtime'],
               ['positive', 'negative', 'Total Sleep Time'],
               ['positive', 'negative', 'Average HRV'],
               ['positive', 'negative', 'Lowest Resting Heart Rate'],
               ['positive', 'negative', 'Temperature Deviation (°C)'],
               ['positive', 'negative', 'Activity Score'],
               ['positive', 'negative', 'Activity Burn'],
               ['positive', 'negative', 'Inactive Time'],
               ['positive', 'negative', 'Rest Time'],
               ['positive', 'negative', 'Total Burn'],
               ['positive', 'negative', 'Non-wear Time'],
               ['positive', 'negative', 'Steps'],
               ['positive', 'negative', 'Readiness Score'],
               ['positive', 'negative', 'light'],
               ['positive', 'negative', 'Communication'],
               ['positive', 'negative', 'Entertainment'],
               ['positive', 'negative', 'Shop'],
               ['positive', 'negative', 'Social_media'],
               ['positive', 'negative', 'Sports'],
               ['positive', 'negative', 'Transportation'],
               ['positive', 'negative', 'Travel'],
               ['positive', 'negative', 'Health'],
               ['positive', 'negative', 'Notifications_total'],
               ['positive', 'negative', 'battery_level'],
               ['positive', 'negative', 'screen_status'],
               ['positive', 'negative', 'sms_out'],
               ['positive', 'negative', 'sms_total'],
               ['positive', 'negative', 'sms_in'],
               ['positive', 'negative', 'call_out_duration'],
               ['positive', 'negative', 'call_in_duration'],
               ['positive', 'negative', 'call_total_duration'],
               ['positive', 'negative', 'call_out_count'],
               ['positive', 'negative', 'call_in_count'], 
               ['positive', 'negative', 'call_total_count'],
               ['positive', 'negative', 'Battery_average'],
               ['positive', 'negative', 'Battery_stability'],
               ['positive', 'negative', 'screen_activations'],
               ['positive', 'negative', 'screen_stability'],
               ['positive', 'negative', 'app_sum'],
               ['positive', 'negative', 'app_stability']
              ]

COLUMN_LIST = [['positive', 'negative', 'Average Resting Heart Rate'],
               ['positive', 'negative', 'screen_activations'],
              ]

######################################################              
# Create a filename object -> DO NOT CHANGE THESE!!!
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

############################################################
#%% Create an Analysis Parameters object -> DO NOT CHANGE!!!
ap = AnalysisParameters()

ap.add('summary_window', SUMMARY_WINDOW)

ap.add('rolling_window', ROLLING_WINDOW)

ap.add('plot_cols', COLUMN_LIST)
