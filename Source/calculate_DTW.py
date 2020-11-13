#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:41:35 2020

@author: ikaheia1
"""
from dtw import *

def DTW_distance(x,y):
    alignment = dtw(x, y, distance_only = True)
    return alignment.distance


