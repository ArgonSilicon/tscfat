#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:05:03 2020

@author: arsi
"""

import pandas as pd
import numpy as np

def interpolate_missing(ts, interpolation):
    
    """

    Parameters
    ----------
    ts : TYPE
        DESCRIPTION.
    interpolation : TYPE
        DESCRIPTION.

    Returns
    -------
    interpolated_ts : TYPE
        DESCRIPTION.
    missing_values : TYPE
        DESCRIPTION.

    """
    
    missing_values = ts.isna()
    
    interpolated_ts = ts.interpolate(interpolation)    
    
    return interpolated_ts, missing_values

if __name__ == "__main__":
    pass