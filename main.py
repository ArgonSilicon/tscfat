#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is main file


"""
# standard library imports
import os
from pathlib import Path
import re
from collections import Counter

# change correct working directory
WORK_DIR = Path(r'/u/26/ikaheia1/data/Documents/SpecialAssignment/CS-special-assignment/')
os.chdir(WORK_DIR)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import pearsonr, spearmanr
from sklearn.manifold import TSNE

# Local application imports
from csv_load import load_all_subjects
import process_apps, process_ESM, process_battery, process_screen_events, process_location
from cluster_timeseries import cluster_timeseries, gaussian_MM
from interpolate_missing import interpolate_missing

###############################################################################
#%% Load the data
DATA_FOLDER = Path('/u/26/ikaheia1/data/Documents''/SpecialAssignment/Data/CSV/')
csv_dict = load_all_subjects(DATA_FOLDER)
dict_keys = list(csv_dict.keys()) # the order of keys is probably different

#%% loop thru keys and assing dataframes
for k in dict_keys:
    if re.search("Battery",k):
        df1 = csv_dict[k]
        
    elif re.search("ESM",k):
        df2 = csv_dict[k]
        
    elif re.search("Location",k):
        df3 = csv_dict[k]
        
    elif re.search("Screen",k):
        df4 = csv_dict[k]
        
    elif re.search("Application",k):
        df5 = csv_dict[k]
        
    else:
        pass
        #raise Exception("Dictionary key unknown.") 
###############################################################################
#%% Process Battery level
df1_r = process_battery.process_battery(df1)
#%%
df1_bl = df1['battery_level']
df1_re = df1_bl.resample('H').mean()
df1_re, _ = interpolate_missing(df1_re,'linear')

df_grouped = df1_re.groupby(df1_re.index.floor('d')).apply(list)
data = np.stack(df_grouped.values[1:-1])

bic = []
aic = []
for i in range(2,20):
    model, Y = gaussian_MM(data,i,1000)
    aic.append(model.aic(data))
    bic.append(model.bic(data))

xmin = np.min(bic)
ix_min = np.argmin(bic)
ymin = bic[ix_min]

fig, ax = plt.subplots(1,2,figsize=(15,7))

ax[0].plot(np.arange(2,20),bic,'o:')
ax[0].plot(ix_min+2,ymin,'X',c="red",markersize=14)
ax[0].set_title('BIC score / number of clusters')
ax[0].set_xlabel('Number of clusters')
ax[0].set_ylabel('BIC score')
ax[0].set_xticks(np.arange(2,20))

xmin = np.min(aic)
ix_min = np.argmin(aic)
ymin = aic[ix_min]

ax[1].plot(np.arange(2,20),aic,'o:')
ax[1].plot(ix_min+2,ymin,'X',c="red",markersize=14)
ax[1].set_title('AIC score / number of clusters')
ax[1].set_xlabel('Number of clusters')
ax[1].set_ylabel('AIC score')
ax[1].set_xticks(np.arange(2,20))

plt.show()

model, Y = cluster_timeseries(df1_bl)


#%% show some sample days
g = df1.groupby(df1.index.floor('d'))
my_day = pd.Timestamp('2020-06-25')
my_day_2 = pd.Timestamp('2020-06-30')
df_slice = g.get_group(my_day)
df_slice_2 = g.get_group(my_day_2)
#%%
df_slice.battery_level.plot()
plt.xlabel("Time / hours")
plt.ylabel("Battery_level")
plt.title("Battery level {}".format(my_day.date()))
plt.ylim(0,105)
plt.show()

#%%
df_slice_2.battery_level.plot()
plt.xlabel("Time / hours")
plt.ylabel("Battery_level")
plt.title("Battery level {}".format(my_day_2.date()))
plt.ylim(0,105)
plt.show()
#%%
df_slice_r = df_slice.resample("H").mean()
df_slice_r.index = np.arange(24)
df_slice_r.battery_level.plot.bar(rot=0)
plt.xlabel("Time / hours")
plt.ylabel("Battery_level")
plt.title("Battery level / averages {}".format(my_day.date()))
plt.ylim(0,105)
plt.show()

#%%
df_slice_r2 = df_slice_2.resample("H").mean()
df_slice_r2.index = np.arange(24)
df_slice_r2.battery_level.plot.bar(rot=0)
plt.xlabel("Time / hours")
plt.ylabel("Battery_level")
plt.title("Battery level / averages {}".format(my_day_2.date()))
plt.ylim(0,105)
plt.show()

###############################################################################
#%% Process ESM data
df2_r, ts_2 = process_ESM.process_ESM(df2)

##############################################################################
#%% Location / daily
df3_r = process_location.process_location(df3)

# mood and location correlation?
df_stack = pd.concat([df2_r,df3_r[:-1]],axis=1)
sns.pairplot(df_stack,kind="reg")
corr_s = df_stack.corr(method="spearman")
##############################################################################
#%% Screen events
df4_r, df4_unlocked = process_screen_events.process_screen_events(df4)

#%%
df_grouped = df4_unlocked.groupby(df4_unlocked.index.floor('d'))['screen_status'].apply(list)
data = np.stack(df_grouped.values[1:-1])

bic = []
aic = []
for i in range(2,20):
    model, Y = gaussian_MM(data,i,100)
    aic.append(model.aic(data))
    bic.append(model.bic(data))

xmin = np.min(bic)
ix_min = np.argmin(bic)
ymin = bic[ix_min]

fig = plt.figure(figsize=(15,10))
plt.plot(np.arange(2,20),bic,'o:')
plt.plot(ix_min+2,ymin,'X',c="red",markersize=14)
plt.title('BIC score / number of clusters')
plt.xlabel('Number of clusters')
plt.ylabel('BIC score')
plt.xticks(np.arange(2,20))
plt.show()

xmin = np.min(aic)
ix_min = np.argmin(aic)
ymin = aic[ix_min]

fig = plt.figure(figsize=(15,10))
plt.plot(np.arange(2,20),aic,'o:')
plt.plot(ix_min+2,ymin,'X',c="red",markersize=14)
plt.title('AIC score / number of clusters')
plt.xlabel('Number of clusters')
plt.ylabel('AIC score')
plt.xticks(np.arange(2,20))
plt.show()

#%%    
model, Y = gaussian_MM(data,7,1000)  
  
df_grouped = df_grouped.drop(df_grouped.index[0])
df_grouped = df_grouped.drop(df_grouped.index[-1])
clustered_data = df_grouped.to_frame()
clustered_data.columns = ['Screen_events']
clustered_data['cluster'] = Y + 1
print("Daily screen events patterns clustered: ")
print(clustered_data.cluster.value_counts())

#%% some plotting, remove this!!
val0 = np.stack(clustered_data[clustered_data['cluster'] == 1]['Screen_events'].values)
val1 = np.stack(clustered_data[clustered_data['cluster'] == 2]['Screen_events'].values)
val2 = np.stack(clustered_data[clustered_data['cluster'] == 3]['Screen_events'].values)
val3 = np.stack(clustered_data[clustered_data['cluster'] == 4]['Screen_events'].values)
val4 = np.stack(clustered_data[clustered_data['cluster'] == 5]['Screen_events'].values)
val5 = np.stack(clustered_data[clustered_data['cluster'] == 6]['Screen_events'].values)
val6 = np.stack(clustered_data[clustered_data['cluster'] == 7]['Screen_events'].values)


for i in range(len(val0)):
    plt.plot(val0[i],':')
    plt.title('Clusters: 1')
    plt.ylim(0,30)
plt.plot(val0.mean(axis=0),c='black')
plt.show()

for i in range(len(val1)):
    plt.plot(val1[i],':')
    plt.title('Cluster: 2')
    plt.ylim(0,30)
plt.plot(val1.mean(axis=0),c='black')
plt.show()

for i in range(len(val2)):
    plt.plot(val2[i],':')
    plt.title('Cluster: 3')
    plt.ylim(0,30)
plt.plot(val2.mean(axis=0),c='black')
plt.show()

for i in range(len(val3)):
    plt.plot(val3[i],':')
    plt.title('Cluster: 4')
    plt.ylim(0,30)
plt.plot(val3.mean(axis=0),c='black')
plt.show()

for i in range(len(val4)):
    plt.plot(val4[i],':')
    plt.title('Cluster: 5')
    plt.ylim(0,30)
plt.plot(val4.mean(axis=0),c='black')
plt.show()


for i in range(len(val5)):
    plt.plot(val5[i],':')
    plt.title('Cluster: 6')
    plt.ylim(0,30)
plt.plot(val5.mean(axis=0),c='black')
plt.show()


for i in range(len(val6)):
    plt.plot(val6[i],':')
    plt.title('Cluster: 7')
    plt.ylim(0,30)
plt.plot(val6.mean(axis=0),c='black')
plt.show()

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
clustered_data['cluster'].plot(style='o:')
ax.set_title('Screen events daily patterns clustered')
ax.set_yticks(np.arange(7))
ax.set_ylabel('Cluster no.')
ax.set_xlabel('Time (day)')
ax.set_ylim(0.8,7.2)
ax.set_xlim('2020-06-01','2020-07-17')
plt.show()

#%% check corrrelations
df4_res = df4_unlocked.resample('D').sum()
df_stack = pd.concat([df_stack,df4_res[1:-1]],axis=1)
corr_s = df_stack.corr(method="spearman")

###############################################################################
#%% Process App notfications
df5_r, ts_5 = process_apps.process_apps(df5,df1,df4)

#%%'
df5_a = df5_r[df5_r['is_active'] == True]

df5_f = df5_a.filter(['Communication', 'Entertainment', 'Other', 'Shop', 'Social_media',
       'Sports', 'Travel', 'Work/Study'])

df5_d = df5_f.resample('D').sum()

df_stack = pd.concat([df_stack,df5_d],axis=1)
corr_s = df_stack.corr(method="spearman")

#%% combine dataframes

comb = pd.concat([df2_r,df5_d], axis=1)

#%%
def corrfunc(x,y, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = spearmanr(x, y)
    ax = ax or plt.gca()
    # Unicode for lowercase rho (ρ)
    rho = '\u03C1'
    ax.annotate(f'{rho} = {r:.2f}', xy=(.1, .9), xycoords=ax.transAxes)
    
g = sns.pairplot(comb,kind="reg")
g.map_lower(corrfunc)
g.fig.suptitle("ESM data pairplots and Spearman correlation", y=1.02,fontsize=20)

#%%
corr_p = comb.corr(method ='pearson') 
corr_s = comb.corr(method ='spearman')
corr_k = comb.corr(method ='kendall')

#%%
from sklearn.preprocessing import MinMaxScaler
from calculate_similarity import calculate_similarity
from calculate_novelty import compute_novelty_SSM
from Plot_similarity import Plot_similarity
from calculate_RQA import Calculate_RQA
from plot_recurrence import Show_recurrence_plot
#%% preoare data
ts = df_stack.values
ts[:,18] = 0
ts = np.delete(ts, [8,9],axis=1)
#%% similairty and novelty
scaler = MinMaxScaler()
scaler.fit(ts)
scaled_data = scaler.transform(ts)
#%%'
TITLE = "full dataframe RP"
FIGPATH = False
FIGNAME = False
#%%
res, mat = Calculate_RQA(ts,2,2,0.05)
Show_recurrence_plot(mat,TITLE,FIGPATH,FIGNAME)

#sim = calculate_similarity(ts,'cityblock')
nov = compute_novelty_SSM(mat,L=7,exclude=False)
Plot_similarity(mat,nov)
nov = np.hstack([0, nov, 0])
df_stack['novelty'] = nov
corr_s = df_stack.corr(method="spearman")

#%% Differences betwen consequent days
data = pd.DataFrame(scaled_data, index=df_stack.index)
diff = data.diff()

diff["sum"] = diff.sum(axis=1)
diff['mean'] = diff.mean(axis=1)
diff['var'] = diff.var(axis=1)

#%% trying to visualize days
data.drop(data.columns[18], axis=1, inplace=True)
X_embedded = TSNE(n_components=2).fit_transform(data)
data['tsne1'] = X_embedded[:,0]
data['tsne2'] = X_embedded[:,1]
weeks = data.index.week
colors = ['red','green','blue','yellow','black']
cmap = ListedColormap(colors)

fig = plt.figure(figsize=(13,13))

plt.scatter(data['tsne1'],data['tsne2'])
plt.plot(data['tsne1'],data['tsne2'],':')

# zip joins x and y coordinates in pairs
for x,y,i in zip(data['tsne1'],data['tsne2'],data.index):

    label = str(i.month) + " - " + str(i.day)

    # this method is called for each point
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10),# distance from text to points (x,y)
                 size=10, 
                 ha='center') # horizontal alignment can be left, right or center
    
plt.title('Days visualized in TSNE space')
plt.xlabel("Feature_1")
plt.ylabel("Feature_2")

#%%



