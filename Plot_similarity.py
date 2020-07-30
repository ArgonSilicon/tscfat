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

plt.rcParams.update({'figure.max_open_warning': 0})


def Plot_similarity(sim,
                    nov,
                    title="Similarity and novelty",
                    savepath = False, 
                    savename = False,
                    ylim = (0,0.05),
                    threshold = 0,
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
    fig, ax = plt.subplots(4,3,figsize=(10,12),sharex=True) 
    gridsize = (4,3)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=3,rowspan=3)
    ax2 = plt.subplot2grid(gridsize, (3,0), colspan=3)
    
    ax1.imshow(sim,cmap="Blues", origin='lower')
    ax1.set_title("Similarity matrix", fontsize=14)
    ax1.set_xlabel('$m = {}$'.format(sim.shape[0]))
    ax1.set_ylabel('$n = {}$'.format(sim.shape[1]))
    
    #ax1 = plt.subplot(gs[1])
    ax2.plot(nov)
    ax2.set_title("Novelty score", fontsize=14)
    ax2.set_xlabel('Time (d)')
    ax2.set_ylabel('Novelty')
    ax2.set_ylim(ylim)
    
    plt.suptitle(title + " daily patterns",fontsize=20,y=1.01)
    plt.grid(True)
    plt.tight_layout(pad=1.0)
    
    
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