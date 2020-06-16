# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:36:18 2020

@author: arsii
"""
import numpy as np
import pandas as pd

from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import periodogram
import matplotlib.pyplot as plt

#%%
df = pd.read_excel("C:/Users/arsii/Documents/Work/Suunto/Move_2020_06_05_18_28_21_Running.xlsx")
#df = pd.read_excel("Move_2020_06_05_18_28_21_Juoksu.xlsx")
#%%
hr = df.iloc[1:,115].dropna()

#%%
plt.plot(hr)
plt.show()



#%%
plot_pacf(hr.values,lags=20,alpha=0.05)
#%%
mod = ARMA(hr.values,order=(1,1))
res = mod.fit()
print(res.params)

#%%
pg = periodogram(hr.values)
plt.plot(pg)
plt.xlim([0,100])