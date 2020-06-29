#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:58:21 2020

@author: arsi
"""

import numpy as np
import scipy.io as sio

def save2mat(ts,
             savepath,
             filename):
    
    
    assert isinstance(ts, np.ndarray), "Timeseries to be saved is not a numpy array."
    assert isinstance(filename,str), "Invalid savename type, should be str."
    
    if savepath.exists():
        
        save_name = savepath / filename
        sio.savemat(save_name, {'time_series':ts})
        
    else:
        raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    
if __name__ == "__main__":
    pass