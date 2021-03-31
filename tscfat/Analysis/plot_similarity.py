#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:07:02 2020

@author: arsi

Plot and save self similarity matrix, convolution kernel and novelty score.
 
"""

import numpy as np
import matplotlib.pyplot as plt
from tscfat.Utils.plot_decorator import plot_decorator

plt.rcParams.update({'figure.max_open_warning': 0})

#TODO! fix xlabel
#TODO! remove ylim
#TODO! fix documentation!
#TODO! clean the code

@plot_decorator
def plot_similarity(sim,
                    nov,
                    stab,
                    title="Similarity and novelty",
                    doi = None,
                    savepath = False, 
                    savename = False,
                    ylim = (0,0.05),
                    threshold = 0,
                    axis = None,
                    kernel = False,
                    test = False
                    ):
    """
    Plot the similarity matrix. Optionally save the figure, plot the kernel, 
    and plot the similarity score.
    
    Parameters
    ----------
    sim : Numpy ndarray
        m x m array containing similarity values
    nov : Numpy ndarray
        m x 1 array containing  novelty scores
    stab : Numpy ndarray
        m x 1 array containing  stability scores
    doi : tuple
        (float, float) values used to highlight certain region of interest. 
    title : str, optional
        Similarity plot title. The default is "Similarity and novelty".
    savepath : Path object, optional
        Path for figure saving. The default is False.
    savename : str object, optional
        Savename for the figure. The default is False.
    ylim : tuple, optional
        (float,float) ylimits for the plot. The default is (0,0.05).
    threshold : float, optional
        Similarity score threshold for showing in the plot. The default is 0.
    axis : pandas.core.indexes.base.Index, optional
        Date range used in the novelty score plot. The default is False.
    kernel : Numpy ndarray, optional
        m x m convolution kernel used for novelty score calculation. T
        he default is False.
    test : boolean
        Indicates whether the function is tested by pytest.
        he default is False.
        
    Raises
    ------
    Exception
        - Requested save folder does not exist
        - Savename and/or savename are not given
        - Novelty score is not a numpy array
        - Stability score is not a numpy array

    Returns
    -------
    None.

    """
     
    assert isinstance(sim,np.ndarray), "Similarity matrix type is not np.ndarray."
    assert isinstance(nov,np.ndarray), "Novelty score array type is not np.ndarray."
    assert isinstance(stab,np.ndarray), "Stability score array type is not np.ndarray."
    
    
    sim[sim < threshold] = 0

    fig, ax = plt.subplots(5,4,figsize=(10,12),sharex=True)  
    gridsize = (5,4)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=3,rowspan=3)
    ax2 = plt.subplot2grid(gridsize, (1,3), colspan=1,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (3,0), colspan=4,rowspan=1)
    ax4 = plt.subplot2grid(gridsize, (4,0), colspan=4,rowspan=1)
    
    ax1.imshow(sim,cmap="Blues", origin='lower')
    ax1.set_title("Similarity matrix", fontsize=18)
    ax1.set_xlabel('$m = {}$'.format(sim.shape[0]),fontsize=16)
    ax1.set_ylabel('$n = {}$'.format(sim.shape[1]),fontsize=16)
    if doi is not None:
        ax1.axvspan(doi[0], doi[1], ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    
    if type(kernel) != bool:
        ax2.imshow(kernel,cmap='Blues')
        ax2.set_title('Kernel',fontsize=18)
        #ax[1,3].text(-0.1, 1.05, "B", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    
    ax3.plot(nov,label="Novelty")
    ax3.set_title("Novelty score", fontsize=18)
    ax3.set_xlabel('Time (day)',fontsize=16)
    ax3.set_ylabel('Novelty',fontsize=16)
    #ax3.set_xticks(np.arange(len(axis))[::7])
    #ax3.set_xticklabels(axis[::7])
    #ax2.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
    #ax3.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
    if doi is not None:
        ax3.axvspan(doi[0], doi[1] ,ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    #ax3.axvspan(98,182,ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    ax3.legend(fontsize=16)
    ax3.set_ylim((0.95*np.min(nov[7:-7]),1.05*(np.max(nov[7:-7]))))
    
    ax4.plot(stab,label="Stability")
    ax4.set_title("Stability score", fontsize=18)
    ax4.set_xlabel('Time (day)',fontsize=16)
    ax4.set_ylabel('Stability',fontsize=16)        
    #ax4.axvspan(98,182,ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    if doi is not None:
        ax4.axvspan(doi[0], doi[1], ymin=0, ymax=1,facecolor="yellow",alpha=0.13,label="Days of interest")
    ax4.legend(fontsize=16)
    ax4.set_ylim((0.95*np.min(stab[7:-7]),1.05*(np.max(stab[7:-7]))))
        
    
    #ax[3,0].set_text(-0.1, 1.05, "C", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    ax[0,3].set_axis_off()
    ax[2,3].set_axis_off()
    
    plt.suptitle(title + " Daily Patterns",fontsize=20,y=1)
    plt.suptitle(title,fontsize=20,y=1)
    plt.grid(True)
    plt.tight_layout(pad=1)
    
    return fig

