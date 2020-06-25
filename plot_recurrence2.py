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





def Show_recurrence_plot(recurrence_matrix,title="Recurrence Plot", 
                         savename = False, savepath = False):
    
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
    
    plt.figure(figsize=(5, 5))
    plt.imshow(recurrence_matrix, cmap='binary', origin='lower')
    plt.title(title, fontsize=16)
    plt.xlabel('$m = {}$'.format(recurrence_matrix.shape[0]))
    plt.ylabel('$n = {}$'.format(recurrence_matrix.shape[1]))
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
    
def Save_recurrence_plot(rp,savename,savepath):
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
    pass

