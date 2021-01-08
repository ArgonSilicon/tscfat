#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:49:55 2021

@author: ikaheia1
"""
import matplotlib.pyplot as plt

def print_decorator(func):
    def wrapper(*args,**kwargs):
        func(*args,*kwargs)
        sn = kwargs['savename']
        sp = kwargs['savepath']
        
        if not all((sn,sp)):
            plt.show()
      
        elif all((sn,sp)):
        
            assert isinstance(sn,str), "Invalid savename type."
        
            if sp.exists():
                with open(sp / (sn + ".png"), mode="wb") as outfile:
                    plt.savefig(outfile, format="png")
            else:
                raise Exception("Requested folder: " + str(sp) + " does not exist.")
        else:
            raise Exception("Arguments were not given correctly.")
    return wrapper

