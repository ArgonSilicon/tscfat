# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:51:52 2020

@author: arsii
"""

from rolling_stats import convert_to_datetime, resample_dataframe
import matplotlib.pyplot as plt
import seaborn as sns
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

