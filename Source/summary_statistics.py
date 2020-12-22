#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:56:55 2020

@author: ikaheia1
"""
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt


def __Plot_summary(df):
    print(df['battery_level'].describe())
    
    fig = plt.figure()
    df['battery_level'].plot.hist(bins=20,grid=True,title="Battery level histogram")
    
    fig = plt.figure()
    df['battery_level'].plot.box(grid=True,title="Battery level bar plot")
    
    fig = plt.figure()
    pd.plotting.lag_plot(df.battery_level,lag=1)
    
    fig = plt.figure()
    pd.plotting.autocorrelation_plot(df.battery_level).set_xlim([0,240])
    
    fig = plt.figure()
    sm.graphics.tsa.plot_pacf(df.battery_level,lags=48)
    
    
    fig = plt.figure()
    sm.graphics.tsa.plot_acf(df.battery_level,lags=24)
    
    
    return None


def Summary_statistics(df):
    
    __Plot_summary(df)
    
    return None