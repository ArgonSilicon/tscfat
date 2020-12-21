# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:45:10 2020

@author: arsii
"""

import matplotlib.pyplot as plt
from arma import arma, autocorr

def Rolling_statistics(ts,w,savename = False, savepath = False):
    
    variance = ts.rolling(window = w).var()
    autocorrelation = ts.rolling(window = w).apply(autocorr)
    mean = ts.rolling(window = w).mean() 
    skew = ts.rolling(window = w).skew()
    kurt = ts.rolling(window = w).kurt()
    
    fig,ax = plt.subplots(3,2,figsize=(15,15))
    fig.suptitle("Rolling Statistics",fontsize=26,y=1.0)
    
    ax[0,0].plot(variance)
    ax[0,0].set_title('Variance',fontsize=16)
    ax[0,0].set_xlabel('Date')
    ax[0,0].set_ylabel('Value')
    
    ax[0,1].plot(autocorrelation)
    ax[0,1].set_title('Autocorrelation',fontsize=16)
    ax[0,1].set_xlabel('Date')
    ax[0,1].set_ylabel('Value')
    
    ax[1,0].plot(mean)
    ax[1,0].set_title('Mean',fontsize=16)
    ax[1,0].set_xlabel('Date')
    ax[1,0].set_ylabel('Value')
    
    ax[1,1].plot(skew)
    ax[1,1].set_title('Skew',fontsize=16)
    ax[1,1].set_xlabel('Date')
    ax[1,1].set_ylabel('Value')
    
    ax[2,0].plot(kurt)
    ax[2,0].set_title('Kurt',fontsize=16)
    ax[2,0].set_xlabel('Date')
    ax[2,0].set_ylabel('Value')
    
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
    
    