#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:11:12 2021

@author: arsi
"""
import numpy as np

def PAM_encoder(value):
    
    value = int(np.rint(value))
    value = str(value)
    
    # Arousal / Valence
    PAM_dict = {'1': (0,0),
                '2': (1,0),
                '3': (0,1),
                '4': (1,1),
                '5': (2,0),
                '6': (3,0),
                '7': (2,1),
                '8': (3,1),
                '9': (0,2),
                '10': (1,2),
                '11': (0,3),
                '12': (1,3),
                '13': (2,2),
                '14': (3,2),
                '15': (3,2),
                '16': (3,3)
                }
    
    aro, val = PAM_dict[value]
    
    return val, aro