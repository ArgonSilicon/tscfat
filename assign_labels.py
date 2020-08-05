#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:09:54 2020

@author: ikaheia1
"""
import pandas as pd

def assign_groups(df,path):
    
    labels = pd.read_csv(path)
    
    #%% create dictionary
    keys = labels.label.astype(str).values
    values = zip(labels.group.values,labels.negate_value.values)
    labels_dict = dict(zip(keys, values))
    
    #%% assing values to df
    df['group'] = [labels_dict[i][0] for i in df.id.values]
    df['negate_value'] = [labels_dict[i][1] for i in df.id.values]
    
    return df

    
    
    
    
    