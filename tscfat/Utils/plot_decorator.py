#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:49:55 2021

@author: ikaheia1

Function wrapper for handling the plotting of figure or saving it to the 
destined folder.

"""
import matplotlib.pyplot as plt
import functools

def plot_decorator(func):
    """ Save the plot figure if savename and path are in function 
    keyword arguments.
    
    
    Parameters
    ----------
    func : function
        Plotting function to be decorated.

    Raises
    ------
    Exception
        Requested folder does not exist og the agruments are not given in 
        correct way.

    Returns
    -------
    wrapper : function wrapper
        Wrapped plotting function.

    """
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        """ Function wrapper for handling the plots.
        

        Parameters
        ----------
        *args : arguments
            Arguments of the wrapped function
        **kwargs : keyword arguments
            Keyword arguments of the wrapped function

        Raises
        ------
        Exception
            Requested folder does not exist og the agruments are not given in 
            correct way.

        Returns
        -------
        fig : matplotlib plt object
            Plotted figure

        """
        fig = func(*args,**kwargs)
        
        sn = ()
        sp = ()
        
        if 'savename' in kwargs:
            sn = kwargs.get('savename')
        if 'savepath' in kwargs:
            sp = kwargs.get('savepath')
        
        if not all((sn,sp)):
            plt.show()
      
        elif all((sn,sp)):
            assert isinstance(sn,str), "Invalid savename type."
        
            if sp.exists():
                with open(sp / (sn + ".png"), mode="wb") as outfile:
                    #plt.close()
                    plt.savefig(outfile, format="png")
            else:
                raise Exception("Requested folder: " + str(sp) + " does not exist.")
        else:
            raise Exception("Arguments were not given correctly.")
        
        if 'test' in kwargs:
            if kwargs.get('test') == True:
                return fig
        
    return wrapper

