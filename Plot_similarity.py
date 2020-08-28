#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:07:02 2020

@author: arsi
"""


from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from datetime import datetime

plt.rcParams.update({'figure.max_open_warning': 0})


def Plot_similarity(sim,
                    nov,
                    title="Similarity and novelty",
                    savepath = False, 
                    savename = False,
                    ylim = (0,0.05),
                    threshold = 0,
                    axis = False,
                    kernel = False,
                    ):
    
    """
    TODO: fix these!
    
    Plots given recurrence plot. Optionally, the plot can be saved 
    on a disk.

    Parameters
    ----------
    recurrence_matrix : numpy array
        Recurrence plot array of a shape (m,n), where m does not have to be 
        equal to n
    title : str (default = "Similarity and novelty")
        Plot title
    savename : str (default = False)
        Name used as plot save name. Has to be a type of str
    savepath : Path -object (default = False)
        path where plot is to be saved. Path has to exist before calling this 
        function.

    Returns
    -------

    """
    
    assert isinstance(sim,np.ndarray), "Recurrence matrix type is not np.ndarray."
    assert isinstance(nov,np.ndarray), "Recurrence matrix type is not np.ndarray."

    sim[sim < threshold] = 0
    # plot it
    fig, ax = plt.subplots(4,4,figsize=(8.3,9.5),sharex=True)  
    gridsize = (4,4)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=3,rowspan=3)
    ax2 = plt.subplot2grid(gridsize, (1,3), colspan=1,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (3,0), colspan=4,rowspan=1)
    
    ax1.imshow(sim,cmap="Blues", origin='lower')
    ax1.set_title("Similarity matrix (cosine distance)", fontsize=22)
    ax1.set_xlabel('$m = {}$'.format(sim.shape[0]),fontsize=16)
    ax1.set_ylabel('$n = {}$'.format(sim.shape[1]),fontsize=16)
    #ax1.text(-0.1, 1.05, "A", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    
    
    if type(kernel) != bool:
        ax2.imshow(kernel,cmap='Blues')
        ax2.set_title('Kernel',fontsize=22)
        #ax[1,3].text(-0.1, 1.05, "B", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    
    #ax1 = plt.subplot(gs[1])
    ax3.plot(axis,nov,label="Novelty")
    ax3.set_title("Novelty score", fontsize=22)
    ax3.set_xlabel('Time (date)',fontsize=16)
    ax3.set_ylabel('Novelty',fontsize=16)
    ax3.set_xticks(np.arange(len(axis))[::7])
    ax3.set_xticklabels(axis[::7])
    #ax2.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
    ax3.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
    ax3.legend(fontsize=16)
    ax3.set_ylim(ylim)
    #ax[3,0].set_text(-0.1, 1.05, "C", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    
    ax[0,3].set_axis_off()
    ax[2,3].set_axis_off()
    
    plt.suptitle(title + " Daily Patterns",fontsize=26,y=1.03)
    plt.grid(True)
    plt.tight_layout(pad=0)
    
    
    """
    # plot letters
    for i, label in enumerate(('A', 'B', 'C', 'D')):
        ax = fig.add_subplot(2,2,i+1)
        ax.text(-0.1, 1.15, label, transform=ax.transAxes,
                fontsize=16, fontweight='bold', va='top', ha='right')
    """
    
    if not savename and not savepath:
        plt.show()
        
    elif savename and savepath:
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png",bbox_inches = 'tight')
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")