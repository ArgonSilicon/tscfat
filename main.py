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
import matplotlib.pyplot as plt

# Local application import
from csv_load import load_all_subjects

from vector_encoding import ordinal_encoding, one_hot_encoding, decode_string, decode_string_3, custom_resampler, normalize_values
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
from save_results import dump_to_json
from plot_timeseries import show_timeseries, show_features
from save2mat import save2mat
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM



###############################################################################
#%% Recursion plot default parameters
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.05 # neigborhood radius
FTC = [np.min,np.max,np.mean,np.std] # features to be calculated (functions)

#############################################################df2.loc[mask3,"answer"] = df2.loc[mask3,"answer"].map(decode_string_3)##################
#%% Load the data into dictionary and extract keys 
DATA_FOLDER = Path(r'/home/arsi/Documents/SpecialAssignment/Data/CSV/')
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys())

###############################################################################
#%% choose App notifications, extract timeseries, calculate recursion plot and metrics
df0 = csv_dict[dict_keys[1]]
df0['Encoded'] = ordinal_encoding(df0['application_name'].values.reshape(-1,1))
res0, mat0 = Calculate_RQA(df0['Encoded'].values,ED,TD,RA)
     
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

# save the timeseries
TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
TSNAME = "timeseries_0.mat"
save2mat(df0['Encoded'].values,TSPATH,TSNAME)        

#% Plot timeseries and save figureShow_recurrence_plot(sim2)
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_0"
show_timeseries(df0.index,df0.application_name,"Application usage","time","Applications",FIGPATH,FIGNAME)

#%% Extract features from timeseries, plot, and save
FIGNAME = "features_0"
show_features(df0['Encoded'],"title","xlab","ylab")


###############################################################################
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

# save the timeseries
TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
TSNAME = "timeseries_1.mat"
save2mat(timeseries1,TSPATH,TSNAME)       

#%% Plot timeseries and save figure
FIGNAME = "timeseries_1"
show_timeseries(resampled.index,resampled.battery_level,"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)

#%% Extract features from timeseries, plot, and save



###############################################Show_recurrence_plot(sim2)###############################
#%% ESM data
df2 = csv_dict[dict_keys[4]]
# put these on import!!!
#df2['time'] = convert_to_datetime(df2['time'],'s')
#df2 = df2.set_index("time")
# decode answer values
mask1 = df2["type"] == 1
mask2 = df2["type"] == 2
mask3 = df2["type"] == 3
mask6 = df2["type"] == 6
df2['Scaled_answer'] = 0

df2.loc[mask1,"answer"] = df2.loc[mask1,"answer"].map(decode_string)
df2.loc[mask2,"answer"] = df2.loc[mask2,"answer"].map(decode_string)
df2.loc[mask3,"answer"] = df2.loc[mask3,"answer"].map(decode_string_3)

df2.loc[mask1,"Scaled_answer"] = df2.loc[mask1,"answer"] 
df2.loc[mask2,"Scaled_answer"] = df2.loc[mask2,"answer"] 
df2.loc[mask3,"Scaled_answer"] = normalize_values(df2.loc[mask3,"answer"].values.astype(float))
df2.loc[mask6,"Scaled_answer"] = normalize_values(df2.loc[mask6,"answer"].values.astype(float))

#%%
#df2_filt = df2.filter(["time","Scaled_answer",])
df2_filt = df2.filter(["time","answer",])
#df2_filt = df2_filt["Scaled_answer"].astype(int)
df2_filt = df2_filt["answer"].astype(int)
resampled2 = df2_filt.resample("D").apply(custom_resampler)

#%%
timeseries2 = resampled2.values
timeseries2 = np.stack(timeseries2[:-1])

#%% calculate receursion plot and metrics
# similarity
sim2 = calculate_similarity(timeseries2,'euclidean')
nov2 = compute_novelty_SSM(sim2,L=4)
sim2[sim2 >= 0.11] = 1
Show_recurrence_plot(sim2)
#%%
# Recursion plot settings
ED = 1 # embedding dimensions
TD = 1 # time delay
RA = 0.01 # neigborhood radius

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

# save the timeseries
TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
TSNAME = "timeseries_2.mat"
save2mat(timeseries2,TSPATH,TSNAME)        

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

# save the timeseries
TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
TSNAME = "timeseries_3.mat"
save2mat(timeseries3,TSPATH,TSNAME)       

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

# save the timeseries
TSPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Timeseries/')
TSNAME = "timeseries_4.mat"
save2mat(timeseries4,TSPATH,TSNAME)
#%% Plot timeseries and save figure
FIGPATH = Path(r'/home/arsi/Documents/SpecialAssignment/Results/Plots/')
FIGNAME = "timeseries_4"
show_timeseries(df4_filt.index,df4_filt.screen_status,"Battery level / hourly binned","time","Level",FIGPATH,FIGNAME)



