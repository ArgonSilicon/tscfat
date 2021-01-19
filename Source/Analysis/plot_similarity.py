#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:07:02 2020

@author: arsi

Plot and save self similarity matrix, convolution kernel and novelty score.
 
"""


from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from datetime import datetime
from Source.Utils.plot_decorator import plot_decorator
import pytest


plt.rcParams.update({'figure.max_open_warning': 0})

@plot_decorator
def plot_similarity(sim,
                    nov,
                    title="Similarity and novelty",
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
            m x m convolution kernel used for novelty score calculation. The default is False.

    Raises
    ------
    Exception
        - Requested save folder does not exist
        - Savename and/or savename are not given

    Returns
    -------
    None.

    """
     
    assert isinstance(sim,np.ndarray), "Similarity matrix type is not np.ndarray."
    assert isinstance(nov,np.ndarray), "Novelty score array type is not np.ndarray."

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
 
    if axis is not None:
        ax3.plot(axis,nov,label="Novelty")
        ax3.set_title("Novelty score", fontsize=22)
        ax3.set_xlabel('Time (date)',fontsize=16)
        ax3.set_ylabel('Novelty',fontsize=16)
        ax3.set_xticks(np.arange(len(axis))[::7])
        ax3.set_xticklabels(axis[::7])
        #ax2.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
        #ax3.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
        ax3.legend(fontsize=16)
        ax3.set_ylim(ylim)
        #ax[3,0].set_text(-0.1, 1.05, "C", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')

    else:
        ax3.plot(nov,label="Novelty")
        ax3.set_title("Novelty score", fontsize=22)
        ax3.set_xlabel('Time (date)',fontsize=16)
        ax3.set_ylabel('Novelty2',fontsize=16)
        #ax3.set_xticks(np.arange(len(axis))[::7])
        #ax3.set_xticklabels(axis[::7])
        #ax2.axvspan(datetime(2020,7,1),datetime(2020,7,15),facecolor="red",alpha=0.15,label="Days of interest")
        #ax3.axvspan(29,43,facecolor="red",alpha=0.15,label="Days of interest")
        ax3.legend(fontsize=16)
        ax3.set_ylim(ylim)
        
    
    #ax[3,0].set_text(-0.1, 1.05, "C", fontsize=26, fontweight='bold', transform=ax1.transAxes,va='top', ha='right')
    ax[0,3].set_axis_off()
    ax[2,3].set_axis_off()
    
    plt.suptitle(title + " Daily Patterns",fontsize=26,y=1.03)
    plt.grid(True)
    plt.tight_layout(pad=0)
    
    return fig

'''
    assert fig is not None, "ohno!"
    if test == True:
        return fig
'''     
def test_Plot_similarity():
    from setup import setup_pd, setup_np
    '''
    import numpy as np
    simmat = np.eye(5)
    novelty = np.ones(5).reshape(1,-1)
    ker = np.array([[1,1,0,-1,-1],
                    [1,1,0,-1,-1],
                    [0,0,0,0,0],
                    [-1,-1,0,1,1],
                    [-1,-1,0,1,1]])
    ret = Plot_similarity(simmat,novelty, savepath = False, savename = False, kernel = ker, axis = None, test = True)
    assert ret is not None
    '''
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        plot_similarity(setup_pd(),setup_np())
    expected_error_msg = "Similarity matrix type is not np.ndarray."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
    
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        plot_similarity(setup_np(),setup_pd())
    expected_error_msg = "Novelty score array type is not np.ndarray."
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)
