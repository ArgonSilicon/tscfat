#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:56:03 2020

@author: arsi
"""
import matplotlib.pyplot as plt
import seaborn as sns

def show_timeseries(x_name,
                    y_name,
                    title,
                    xlab,
                    ylab,
                    savepath = False, 
                    savename = False):
    """ Write docstrings
    """
    
    # Insert assertions
    
    plt.figure(figsize=(15,15))
    plt.scatter(x_name, y_name)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    
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