# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:18:31 2020

@author: arsii

Functions for creating a recurrence plot object from the time series data, 
and to show the recurrence plot. Inputs for recurrence plot 
creation are expected to be 2D - numpy arrays of a shape (time,features).
Function returns the recurrence plot objects containing recurrence matrices 
and precalculated metrics. Recurrence matrix are plotted with matplotlib and
saved as numpy arrays if so desired. 
Pynicorn library is needed for recurrence plots. Full documentation can be 
found at:
http://www.pik-potsdam.de/~donges/pyunicorn/api_doc.html#timeseries
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.ticker as ticker
from datetime import datetime






def Show_recurrence_plot(recurrence_matrix,
                         title="Recurrence Plot",
                         savepath = False, 
                         savename = False,
                         axis = False,
                         x1 = False,
                         X2 = False):
    
    """
    Plots given recurrence plot. Optionally, the plot can be saved 
    on a disk.

    Parameters
    ----------
    recurrence_matrix : numpy array
        Recurrence plot array of a shape (m,n), where m does not have to be 
        equal to n
    title : str (default = "Recurrence Plot")
        Plot title
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.

    Returns
    -------

    """
    assert isinstance(recurrence_matrix,np.ndarray), "Recurrence matrix type is not np.ndarray."
    
    #tick_spacing = 
    fig, ax = plt.subplots(1,1,figsize=(10,10)) 

   
    ax.imshow(recurrence_matrix, cmap="Blues",origin='lower')
    
    plt.suptitle(title, fontsize=16,y=1.02)
    
    if type(axis) != bool:
        # We want to show all ticks...
        ax.set_xticks(np.arange(len(axis))[::7])
        ax.set_yticks(np.arange(len(axis))[::7])
        # ... and label them with the respective list entries
        ax.set_xticklabels(axis[::7])
        ax.set_yticklabels(axis[::7])
        
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        
        #plt.xticks(np.arange(len(axis)),axis)
        #plt.yticks(np.arange(len(axis)),axis)
        plt.xlabel('date (m-d)')
        plt.ylabel('date (m-d)')
        
    else:
        plt.xlabel('$m = {}$'.format(recurrence_matrix.shape[0]))
        plt.ylabel('$n = {}$'.format(recurrence_matrix.shape[1]))
        

    #ax.grid(color='black', linewidth=1,linestyle=':')
   
    
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
        
def Show_joint_recurrence_plot(recurrence_matrix,
                         title="Recurrence Plot",
                         savepath = False, 
                         savename = False,
                         axis = False,
                         X1 = False,
                         X2 = False,
                         fig1title = False,
                         fig2title = False,
                         ylab1 = False,
                         ylab2 = False):
    
    """
    Plots given recurrence plot. Optionally, the plot can be saved 
    on a disk.

    Parameters
    ----------
    recurrence_matrix : numpy array
        Recurrence plot array of a shape (m,n), where m does not have to be 
        equal to n
    title : str (default = "Recurrence Plot")
        Plot title
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.

    Returns
    -------

    """
    assert isinstance(recurrence_matrix,np.ndarray), "Recurrence matrix type is not np.ndarray."
    
    #tick_spacing = 
    fig, ax = plt.subplots(6,4,figsize=(10,12),sharex=True) 
    gridsize = (6,4)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=4,rowspan=1)
    ax2 = plt.subplot2grid(gridsize, (1,0), colspan=4,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (2,0), colspan=4,rowspan=4)
    
    ax1.plot(axis,X1)
    ax1.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
    ax1.set_xticks(np.arange(len(axis))[::7])
    ax1.set_xticklabels(axis[::7])
    ax1.set_ylabel(ylab1)
    ax1.set_title(fig1title)
    
    
    ax2.plot(axis,X2)
    ax2.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
    ax2.set_xticks(np.arange(len(axis))[::7])
    ax2.set_xticklabels(axis[::7])
    ax2.set_ylabel(ylab2)
    ax2.set_title(fig2title)
    
    
    ax3.imshow(recurrence_matrix, cmap="Blues",origin='lower')
    ax3.set_title('Joint Recursion Plot')
    
    plt.suptitle(title, fontsize=16,y=1.02)
    
    if type(axis) != bool:
        # We want to show all ticks...
        ax3.set_xticks(np.arange(len(axis))[::7])
        ax3.set_yticks(np.arange(len(axis))[::7])
        # ... and label them with the respective list entries
        ax3.set_xticklabels(axis[::7])
        ax3.set_yticklabels(axis[::7])
        
        # Rotate the tick labels and set their alignment.
        plt.setp(ax3.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        
        #plt.xticks(np.arange(len(axis)),axis)
        #plt.yticks(np.arange(len(axis)),axis)
        ax3.set_xlabel('date (m-d)')
        ax3.set_ylabel('date (m-d)')
        
    else:
        ax3.set_xlabel('$m = {}$'.format(recurrence_matrix.shape[0]))
        ax3.set_ylabel('$n = {}$'.format(recurrence_matrix.shape[1]))
        

    #ax.grid(color='black', linewidth=1,linestyle=':')
   
    
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
    

if __name__ == "__main__":
    pass

