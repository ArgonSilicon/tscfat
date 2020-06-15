# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:18:31 2020

@author: arsii

This script creates a recurrence plot from time series data. One 1D-timeseries
is plotted at time. Input imeseries are expected to be numpy arrays of a 
shape (1,n). Recurrence plot matrix are returned as (n,n) numpy arrays. 
Recurrence plots can be optionally plotted with matplotlib and saved as 
numpy arrays.  

"""

import matplotlib.pyplot as plt
from pyts.image import RecurrencePlot
from pathlib import Path
import pandas as pd
import numpy as np

def Recurrence_plot_trans(timeseries,dimension=1, time_delay=1, 
                          threshold='point', percentage=15, flatten=False): 
    """
    Function creates a (n,n) recurrence plot object, where n denotes the 
    length of the 1D-timeseries. Function requires A Python Package for Time
    Series Classification. Full documentation of pyts can be found at:
    https://pyts.readthedocs.io/en/stable/user_guide.html
    
    Parameters
    ----------
    timeseries : numpy array
        timesieries must be a numpy array of a shape (1,n)
    dimension : int or float (default = 1)
        Trajectory dimensions.
    time_delay : int or float (default=1)
        Time delay between trajectory points.
    threshold = float,'point','distance', or None (default='point')
        Minimun distance threshold.
    percentage : int or float (default=15)
        Threshold as percentage
    flatten : boolean (default = False)
        When set to true, recursion plot is flattened into one dimension.

    Returns
    -------
    rp : numpy array
        (n,n) numpy array containing the calculated recurrence plot values. 
       
    """
    rp = RecurrencePlot(dimension, time_delay, threshold, percentage, flatten)    
    rp_fit = rp.fit_transform(timeseries)
    return np.squeeze(rp_fit)

def Plot_recurrence(rp,savename = False, savepath = False):
    """
    Function plots given recurrence plot. Optionally, the plot can be saved 
    on a disk.

    Parameters
    ----------
    rp : numpy array
        Recurrence plot array of a shape (n,n)
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.

    Returns
    -------

    """
    plt.figure(figsize=(5, 5))
    plt.imshow(rp, cmap='binary', origin='lower')
    plt.title('Recurrence Plot', fontsize=16)
    plt.tight_layout()
    
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
        
def Save_recurrence(rp,savename,savepath):
    """
    SAves given recurrence plot matrix as a numpy array.

    Parameters
    ----------
     rp : numpy array
        Recurrence plot array of a shape (n,n)
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where recurrence plot matrix is to be saved. 
        Path has to exist before calling this function.

    Returns
    -------
    
    """
    assert isinstance(rp,np.ndarray), "Filetype should be numpy.ndarray."
    assert isinstance(savename,str), "Invalid savename type."
    
    if savepath.exists():
        with open(savepath / (savename + ".npy"), mode="wb") as outfile:
            np.save(outfile, rp)
    else:
        raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    
       
if __name__ == "__main__":
    # Insert correct path here
    SAVE_PATH = Path(r'C:/Users/arsii/Documents/Work/Recurrence_plots/Matrices')
    SAVE_NAME = "test"
    SAVE_PATH_2 = Path(r'C:/Users/arsii/Documents/Work/Recurrence_plots/Images/')
    SAVE_NAME_2 = "test_2"
    
    df = pd.read_excel("Move_2020_06_05_18_28_21_Juoksu.xlsx")
    timeseries = df.iloc[1:,115].dropna().values.reshape(1,-1)
    
    rp = Recurrence_plot_trans(timeseries)
      
    Save_recurrence(rp,SAVE_NAME,SAVE_PATH)
    Plot_recurrence(rp,SAVE_NAME_2,SAVE_PATH_2)