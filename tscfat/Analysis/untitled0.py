#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:28:31 2021

@author: arsii
"""

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

fig, ax = plt.subplots(2,1)

ax[0].plot([datetime(2019,2,14), datetime(2019,4,26)], [1,2])

ax[0].axvspan(date2num(datetime(2019,3,1)), date2num(datetime(2019,3,31)), 
           label="March", color="crimson", alpha=0.3)

ax[0].legend()

ax[1].plot([datetime(2019,2,14), datetime(2019,4,26)], [1,2])

ax[1].axvspan(date2num(datetime(2019,3,1)), date2num(datetime(2019,3,31)), 
           label="March", color="crimson", alpha=0.3)

ax[1].legend()

fig.autofmt_xdate()
plt.show()

fig, ax = plt.subplots(4,1,figsize=(10,10))
    
ax[0].plot(Result.observed)
if doi is not None:
    #ax[0].axvspan(doi[0], doi[1], ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    ax[0].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")
    
ax[1].plot(Result.trend)

if doi is not None:
    ax[1].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")

ax[2].plot(Result.seasonal)

if doi is not None:
    ax[2].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")

ax[3].plot(Result.resid)

if doi is not None:
    ax[3].axvspan(date2num(datetime(*doi[0])), date2num(datetime(*doi[1])),facecolor="yellow",alpha=0.13,label="Days of interest")

plt.show()

#%%
import scipy.spatial as sp

matrix1 = calculate_similarity(df.positive.values.reshape(-1,1))
matrix2 = calculate_similarity(df.negative.values.reshape(-1,1))
dist1 =  1 - sp.distance.cdist(matrix1, matrix2, 'cosine')

sns.heatmap(dist1.T, cmap="YlGnBu")