# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is main file


"""
# standard library imports
import os
from pathlib import Path

# change correct working directory
WORK_DIR = Path(r'/home/arsi/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

# third party imports
import numpy as np

# Local application import
from csv_load import load_all_subjects
from rolling_stats import convert_to_datetime
from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler
from calculate_RQA import Calculate_RQA
from plot_recurrence2 import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries2 import show_timeseries

#%% Load the data into dictionary and extract keys 
DATA_FOLDER = Path(r'/home/arsi/Documents/SpecialAssignment/Data/CSV/')
csv = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv.keys())

###############################################################################
#%% choose App notifications
df0 = csv[dict_keys[1]]
# put these on import!!!
df0['time'] = convert_to_datetime(df0['time'],'s')
df0 = df0.set_index("time")

#%% filter dataframe, extract timeseries and encode labels 
df0_filt = df0.filter(["time","application_name",])
timeseries0 = ordinal_encoding(df0_filt['application_name'].values.reshape(-1,1))

#%% calculate receursion plot and metrics

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius

# Calculate recursion plot and metrix
res0, mat0 = Calculate_RQA(timeseries0,ED,TD,RA)
     
#%% show recursion plot and save figure

# set correct names and plot title
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "recplot_0"
TITLE = "AppNotifications Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat0,TITLE,FIGPATH,FIGNAME)

# set correct names and save metrics as json 
RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
RESNAME = "metrics_0.json"
dump_to_json(res0,RESPATH,RESNAME)          

#%% Plot timeseries and save figure
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_0"
show_timeseries(df0_filt.index,df0_filt.application_name,"Application usage","time","Applications",FIGPATH,FIGNAME)


##############################################################################
#%% Choose Battery level
df1 = csv[dict_keys[2]]
# put these on import!!!
df1['time'] = convert_to_datetime(df1['time'],'s')
df1 = df1.set_index("time")

#%% filter
df1_filt = df1.filter(["time","battery_level",])
resampled = df1_filt.resample("H").mean()
timeseries1 = resampled.values

#%% calculate receursion plot and metrics

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius

# Calculate recursion plot and metrix
res1, mat1 = Calculate_RQA(timeseries1,ED,TD,RA)

#%% show recursion plot and save figure

# set correct names and plot title
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "recplot_1"
TITLE = "Battery level Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat1,TITLE,FIGPATH,FIGNAME)

# set correct names and save metrics as json 
RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
RESNAME = "metrics_1.json"
dump_to_json(res1,RESPATH,RESNAME)          

#%% Plot timeseries and save figure
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_1"
show_timeseries(resampled.index,resampled.battery_level,"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)

##############################################################################
#%% ESM data
df2 = csv[dict_keys[4]]
# put these on import!!!
df2['time'] = convert_to_datetime(df2['time'],'s')
df2 = df2.set_index("time")
# decode answer values
mask1 = df2["type"] == 1
mask2 = df2["type"] == 2
mask3 = df2["type"] == 3
df2.loc[mask1,"answer"] = df2.loc[mask1,"answer"].map(decode_string)
df2.loc[mask2,"answer"] = df2.loc[mask2,"answer"].map(decode_string)
df2.loc[mask3,"answer"] = df2.loc[mask3,"answer"].map(decode_string_3)

#%%
df2_filt = df2.filter(["time","answer",])
df2_filt = df2_filt["answer"].astype(int)
resampled2 = df2_filt.resample("D").apply(custom_resampler)

#%%
timeseries2 = resampled2.values
timeseries2 = np.stack(timeseries2[:-1])

#%% calculate receursion plot and metrics

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius

# Calculate recursion plot and metrix
res2, mat2 = Calculate_RQA(timeseries2,ED,TD,RA)

#%% show recursion plot and save figure

# set correct names and plot title
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "recplot_2"
TITLE = "ESM Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat2,TITLE,FIGPATH,FIGNAME)

# set correct names and save metrics as json 
RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
RESNAME = "metrics_2.json"
dump_to_json(res2,RESPATH,RESNAME)          

#%% Plot timeseries and save figure -> How to plot these!!!
#FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
#FIGNAME = "timeseries_2"
#show_timeseries(resampled.index,resampled.battery_level,"ESM","time","Level",FIGPATH,FIGNAME)


##############################################################################
#%% Location / day ??
df3 = csv[dict_keys[0]]
# put these on import!!!
df3 = df3.set_index("day")
timeseries3 = df3["totdist"].values # what to choose?
#%% calculate receursion plot and metrics

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius

# Calculate recursion plot and metrix
res3, mat3 = Calculate_RQA(timeseries3,ED,TD,RA)

#%% show recursion plot and save figure

# set correct names and plot title
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "recplot_3"
TITLE = "Location / daily Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat3,TITLE,FIGPATH,FIGNAME)

# set correct names and save metrics as json 
RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
RESNAME = "metrics_3.json"
dump_to_json(res3,RESPATH,RESNAME)          

#%% Plot timeseries and save figure
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_3"
show_timeseries(df3.index,df3.totdist,"Total distance travelled / daily binned","time","Level",FIGPATH,FIGNAME)


##############################################################################
#%% Screen events
df4 = csv[dict_keys[3]]
# put these on import!!!
df4['time'] = convert_to_datetime(df4['time'],'s')
df4 = df4.set_index("time")
#%% filter
df4_filt = df4.filter(["time","screen_status",])
resampled4 = df4_filt.resample("H").count()
timeseries4 = resampled4.values

#%% calculate receursion plot and metrics

# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius

# Calculate recursion plot and metrix
res4, mat4 = Calculate_RQA(timeseries4,ED,TD,RA)

#%% show recursion plot and save figure

# set correct names and plot title
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "recplot_4"
TITLE = "Screen events / hourly Recurrence Plot \n dim = {}, td = {}, r = {}".format(ED,TD,RA)  
Show_recurrence_plot(mat4,TITLE,FIGPATH,FIGNAME)

# set correct names and save metrics as json 
RESPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Metrics/')
RESNAME = "metrics_4.json"
dump_to_json(res4,RESPATH,RESNAME)          

#%% Plot timeseries and save figure
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_4"
show_timeseries(df4_filt.index,df4_filt.screen_status,"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)





