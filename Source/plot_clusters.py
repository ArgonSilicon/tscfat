# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 12:57:38 2020

@author: arsii
"""
import matplotlib.pyplot as plt

def Plot_clustered_timeseries():
    
    return None
    
    
def Plot_clusters(clusters,title,xlab="Timepoint",ylab="Cluster",savename = False, savepath = False):
    """
    

    Parameters
    ----------
    clusters : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    xlab : TYPE, optional
        DESCRIPTION. The default is "Timepoint".
    ylab : TYPE, optional
        DESCRIPTION. The default is "Cluster".
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
    assert isinstance(series, np.ndarray), "Series is not a numpy array."
    
    plt.plot(clusters,'o')
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
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