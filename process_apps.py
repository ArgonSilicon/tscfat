#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:08:26 2020

@author: arsi
"""


def process_apps(df):
        
    # Load dictionary for app labels
    DICT_PATH = Path(r'/home/arsi/Documents/SpecialAssignment/CS-special-assignment/')
    DICT_NAME = 'labels_dict.json'
    loadname = DICT_PATH / DICT_NAME
    _,labels = load_one_subject(loadname)
    
    #
    df0 = csv_dict[dict_keys[1]]
    df0['Encoded'] = ordinal_encoding(df0['application_name'].values.reshape(-1,1))
    df0['group'] = [labels[value] for value in df0['application_name'].values]
    df0['Encoded_group'] = ordinal_encoding(df0['group'].values.reshape(-1,1))
    #enc_df = pd.DataFrame(one_hot_encoding(df0['Encoded_group'].values.reshape(-1,4)))
    Colnames = ['Communication','Entertainment','Other','Sports','Work/Study']
    enc_df = pd.DataFrame(one_hot_encoding(df0['Encoded_group'].values.reshape(-1,1)),columns=Colnames,index=df0.index)
    df0 = pd.concat([df0,enc_df], axis=1, join='outer') 
    df0_filt = df0.filter(["time",*Colnames])
    resampled = df0_filt.resample("H").sum()
    
    timeseries1 = resampled.to_numpy()
    #%%
    res0, mat0 = Calculate_RQA(timeseries1,ED,TD,RA)
    sim0 = calculate_similarity(timeseries1,'euclidean')
    sim1 = calculate_similarity(timeseries1,'euclidean')
    nov1 = compute_novelty_SSM(sim1)
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
    show_timeseries(df0.index,df0.Encoded_group,"Application usage","time","Applications",FIGPATH,FIGNAME)
    
    #%% Extract features from timeseries, plot, and save
    FIGNAME = "features_0"
    show_features(df0['Encoded'],"title","xlab","ylab")

if __name__ == "__main__":
    pass