#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 12:01:57 2020

@author: ikaheia1

Pipeline configuration parameters

"""
from pathlib import Path
from filenames import FileNames

# Subject information
SUBJECTS = []

# Paths
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Source')
DATA_FOLDER = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/Data')
FIGPATH = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/Results')

# create an filenames object
fnames = FileNames(WORK_DIR,DATA_FOLDER,FIGPATH)


