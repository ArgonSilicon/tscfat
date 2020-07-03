#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:43:01 2020

@author: arsi
"""

# standard library imports
import json
from pathlib import Path

# Local application import
from csv_load import load_one_subject

#%% open csv
foldername = Path(r'/home/arsi/Documents/SpecialAssignment/Data/AppClasses/')
filename = 'apps_group.csv'
open_name = foldername / filename

_, df_labels = load_one_subject(open_name)

#%% Create labels dictionary

labels_dict = {}
for label, content in df_labels.items():
    temp_dict = {}    
    for c in content:
        if c == c:
            temp_dict[c] = label
    labels_dict = {**labels_dict, **temp_dict}

#%% save as json
json = json.dumps(labels_dict)
f = open("labels_dict.json","w")
f.write(json)
f.close()
