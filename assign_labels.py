#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:09:54 2020

@author: ikaheia1
"""
import pandas as pd

def assign_groups(df,path):
    
    labels = pd.read_csv(path)
    