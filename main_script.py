# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:28:18 2020

@author: arsii

This is main file


"""
import numpy as np
from pathlib import Path
from csv_load import load_all_subjects, load_one_subject
from recurrence_plot import *
from rolling_stats import *
import matplotlib.pyplot as plt
import seaborn as sns
from recurrence_plot_pu import *
from vector_encoding import ordinal_encoding, one_hot_encoding


#%%
DATA_FOLDER = Path(r'C:/Users/arsii/Documents/Work/Data/CSV/')
csv = load_all_subjects(DATA_FOLDER)

#%%
dict_keys = list(csv.keys())
df = csv[dict_keys[2]]
df['time'] = convert_to_datetime(df['time'],'s')
df = df.set_index("time")

#%%

def custom_resampler(array_like):
    print(array_like.values)
    return array_like.values


mask = df["type"] == 6
ft = df[mask]
ans = ft["answer"].astype(int)
resampled = ans.resample("D").apply(custom_resampler)

#%%
tsa = resampled.values
tsa = tsa[:-1]
tsa = np.stack(tsa)

#%%
rp = Create_recurrence_plot(tsa2,recurrence_rate=0.15)
rm = rp.recurrence_matrix()
Show_recurrence_plot(rm)

#%%
df_resampled = resample_dataframe(df, 'D', 'time')
#%%
timeseries = df_resampled.iloc[:,3].dropna().values.reshape(-1,1)
timeseries = df.iloc[:,3].dropna().values.reshape(-1,1)
#%% ESM asnwers encoder
ft = df.filter(["time","id","answer","type"])

# mask
mask = df["type"] == 6
# encode
encoded = one_hot_encoding(ft[mask]["answer"].values.reshape(-1,1))
encoded = ordinal_encoding(ft[mask]["answer"].values.reshape(-1,1))
# replace values
ft["encoded"] = np.empty((len(ft), 0)).tolist()
ft.loc[mask,"encoded"] = encoded

#%%
#rp = Recurrence_plot_trans(timeseries)

#%%
#Plot_recurrence(rp)
#%%

sns.lineplot(x="time",y="battery_level",data=df_resampled)
plt.title('Battery level plot')
plt.xticks(rotation=45)
plt.show()

#%%
sns.lineplot(x="time",y="screen_status",data=df)
plt.title('Screen status')
plt.xticks(rotation=45)
plt.show()

#%% Test Pyunicorn
# Parameters for recursion
DIM = 1  # Embedding dimension
TAU = 0  # Embedding delay

#  Settings for the recurrence plot
EPS = 0.05  # Fixed threshold
RR = 0.05   # Fixed recurrence rate
# Distance metric in phase space ->
# Possible choices ("manhattan","euclidean","supremum")
METRIC = "supremum"

#%%
rp = Create_recurrence_plot(timeseries,recurrence_rate=0.3)
rm = rp.recurrence_matrix()
Show_recurrence_plot(rm)