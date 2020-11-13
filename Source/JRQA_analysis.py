#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:32:21 2020

@author: ikaheia1
"""

import os
from pathlib import Path

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
LOAD_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/')
os.chdir(WORK_DIR)

import numpy as np
import pandas as pd
from calculate_JRQA import Calculate_JRQA
from plot_recurrence import Show_recurrence_plot
#%% Test JRQA
# '/u/26/ikaheia1/data/Documents/SpecialAssignment/Results/SL/Timeseries'
LOADPATH = LOAD_DIR / "Results/"
FILENAME_1 = "SL/Timeseries/u02.npy"
FILENAME_2 = "SL_2/Timeseries/u02.npy"
FILENAME_3 = "SL_3/Timeseries/u02.npy"

#%%
mat_1 = np.load(LOADPATH / FILENAME_1)
mat_2 = np.load(LOADPATH / FILENAME_2)
mat_3 = np.load(LOADPATH / FILENAME_3)

#%%
res_2 = mat_2.reshape(-1,1)
res_3 = mat_3.reshape(-1,1)
#%%
res_1, rec_1 = Calculate_JRQA(res_3,res_3)

#%%
Show_recurrence_plot(rec_1)