#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:07:02 2020

@author: arsi
"""


from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def Plot_similarity(sim,
                    nov,
                    title="Similarity and novelty",
                    savepath = False, 
                    savename = False):
    
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
    
    plt.subplot(211)
    #plt.figure(figsize=(5, 5))
    plt.imshow(sim, cmap='binary', origin='lower')
    plt.title(title, fontsize=16)
    plt.xlabel('$m = {}$'.format(sim.shape[0]))
    plt.ylabel('$n = {}$'.format(sim.shape[1]))
    plt.tight_layout()
    plt.subplot(212)
    plt.plot(nov)
    
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