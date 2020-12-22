# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:45:10 2020

@author: arsii
"""

import matplotlib.pyplot as plt
from arma import autocorr
from degree_of_fluctuation import fluctuation_intensity
from scipy.stats import entropy
import nolds

def Rolling_statistics(ts,w,savename = False, savepath = False):
    
    variance = ts.rolling(window = w).var()
    autocorrelation = ts.rolling(window = w).apply(autocorr)
    mean = ts.rolling(window = w).mean() 
    skew = ts.rolling(window = w).skew()
    kurt = ts.rolling(window = w).kurt()
    flu_int = ts.rolling(window = w).apply(fluctuation_intensity,args=(100,w))
    #ent = ts.rolling(window = w).apply(entropy)
    ent = ts.rolling(window = w).apply(nolds.sampen)
    
    
    fig,ax = plt.subplots(4,2,figsize=(15,15))
    fig.suptitle("Rolling Statistics",fontsize=26,y=1.0)
    
    ax[0,0].plot(ts)
    ax[0,0].set_title('Original timeseries',fontsize=16)
    ax[0,0].set_xlabel('Date')
    ax[0,0].set_ylabel('Value')
    
    ax[0,1].plot(mean)
    ax[0,1].set_title('Mean',fontsize=16)
    ax[0,1].set_xlabel('Date')
    ax[0,1].set_ylabel('Value')
    
    ax[1,0].plot(variance)
    ax[1,0].set_title('Variance',fontsize=16)
    ax[1,0].set_xlabel('Date')
    ax[1,0].set_ylabel('Value')
    
    ax[1,1].plot(autocorrelation)
    ax[1,1].set_title('Autocorrelation',fontsize=16)
    ax[1,1].set_xlabel('Date')
    ax[1,1].set_ylabel('Value')
    
    ax[2,0].plot(skew)
    ax[2,0].set_title('Skewness',fontsize=16)
    ax[2,0].set_xlabel('Date')
    ax[2,0].set_ylabel('Value')
    
    ax[2,1].plot(kurt)
    ax[2,1].set_title('Kurtosis',fontsize=16)
    ax[2,1].set_xlabel('Date')
    ax[2,1].set_ylabel('Value')
    
    ax[3,0].plot(flu_int)
    ax[3,0].set_title('Fluctuation intensity',fontsize=16)
    ax[3,0].set_xlabel('Date')
    ax[3,0].set_ylabel('Value')
     
    ax[3,1].plot(ent)
    ax[3,1].set_title('Entropy',fontsize=16)
    ax[3,1].set_xlabel('Date')
    ax[3,1].set_ylabel('Value')
    
    
    if not savename and not savepath:
        plt.show()
        
    elif savename and savepath:
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
    
    