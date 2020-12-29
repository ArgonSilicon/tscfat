#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:42:46 2020

@author: ikaheia1

Check if the system is ready to run the analysis pipeline

"""

import os
import pkg_resources

# Check the python dependecies
dep = []

with open('./requirements.txt') as f:
    for line in f:
        if line == "\n" or line.startswith(('_','#')):
            continue
        dep.append(line.strip())

# Raise an error if the requirements are not met
pkg_resources.working_set.require(dep)

'''
# Check that the data is present on the system
from config import fname
if not os.path.exists(fname.raw_data_dir):
    raise ValueError('The `raw_data_dir` points to a directory that does not exist: ' + fname.raw_data_dir)

# Make sure the output directories exist
os.makedirs(fname.processed_data_dir, exist_ok=True)
os.makedirs(fname.figures_dir, exist_ok=True)
os.makedirs(fname.reports_dir, exist_ok=True)

# Prints some information about the system
import mne
mne.sys_info()

with open(fname.system_check, 'w') as f:
    f.write('System check OK.')

print("\nAll seems to be in order.\nYou can now run the entire pipeline with: python -m doit")
'''