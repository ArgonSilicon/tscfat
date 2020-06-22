# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:41:05 2020

@author: arsii
"""


import matplotlib.pyplot as plt
from pyunicorn.timeseries import RecurrencePlot

def Create_recurrence_plot(time_series, dim = 60, tau = 0, metric="supremum",
                    normalize=False, recurrence_rate=0.15):
    """ Docstrigns here
    """    
    print(dim)
    #print(time_series)
    rp = RecurrencePlot(time_series, dim=dim, tau=tau, metric=metric, 
                         normalize=False,recurrence_rate=recurrence_rate)
                  
    
    return rp


def Show_recurrence_plot(recurrence_matrix):
    """ Insert docstrigns
    """
    
    plt.figure(figsize=(5, 5))
    plt.imshow(recurrence_matrix, cmap='binary', origin='lower')
    plt.title('Recurrence Plot', fontsize=16)
    plt.xlabel('$n$')
    plt.ylabel('$n$')
    plt.tight_layout()


if __name__ == "__main__":
    # Parameters for recursion
    DIM = 15  # Embedding dimension
    TAU = 0  # Embedding delay

    #  Settings for the recurrence plot
    EPS = 0.05  # Fixed threshold
    RR = 0.50   # Fixed recurrence rate
    # Distance metric in phase space ->
    # Possible choices ("manhattan","euclidean","supremum")
    METRIC = "supremum"
    
    rp = RecurrencePlot(sta, dim=DIM, tau=TAU, metric=METRIC, 
                         normalize=False,recurrence_rate=RR)