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
from tscfat.Utils.file_names import FileNames
from tscfat.Utils.analysis_parameters import AnalysisParameters

#%% General variables -> CHANGE THESE!!!

# The days of interest ((start date), (end date))
# Use the format: (YEAR,DAY,MONTH,HOUR,MINUTE)
doi = (2020,10,1),(2020,12,24)


#%% Filenames -> CHANGE THESE!!!

# DATA LOADING:
# Path to the data file to be imported
CSV_PATH = Path('/home/arsii/tscfat/Data/Battery_test_data.csv')

# TIMESERIES CLUSTERING
# Output folder for similarity plot
CLUSTERING_OUT = Path('/home/arsii//tscfat/Results/Clustering')
# BAse name for summary statistics image
CLUSTERING_BASE = 'aware_clusters_'

#%% Analysis parameters -> CHANGE THESE!!!
# number fo clusters
N_CLUST = 5
# maximun iterations
MAX_ITER = 5
# maximun iteration barycenters
MAX_ITER_BARYCENTER = 5
# random state
RANDOM_STATE= 0
# distance metric
METRIC = "dtw"
# ylimit range for the plots
YLIM = (0,100)

#%% Create a filename object -> DO NOT CHANGE!!!
fn = FileNames()

fn.add('csv_path',CSV_PATH)

fn.add('clustering_out', CLUSTERING_OUT)
fn.add('clustering_base', CLUSTERING_BASE)

#%% Create an Analysis Parameters object -> DO NOT CHANGE!!!
ap = AnalysisParameters()

ap.add('n',N_CLUST)
ap.add('mi',MAX_ITER)
ap.add('mib',MAX_ITER_BARYCENTER)
ap.add('rs',RANDOM_STATE)
ap.add('metric',METRIC)
ap.add('ylim',YLIM)

