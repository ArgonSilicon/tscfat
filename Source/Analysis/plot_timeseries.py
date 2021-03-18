#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:44:59 2021

@author: arsi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from Source.Utils.plot_decorator import plot_decorator

@plot_decorator
def plot_timeseries(data, columns, title, xlab="Timepoint",ylab="Cluster",savename = False, savepath = False, highlight = False, test=False):
    
    fig = None
    
    return fig