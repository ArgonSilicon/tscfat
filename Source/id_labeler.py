#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:12:17 2020

@author: arsi
"""


def quick_and_dirty_labeling(series):
    array = []
    
    for value in series.values:
        
        if value[:2] == 'am':
            label = 'AM'
            
        elif value[:2] == 'dq':
            label = 'DQ'
            
        elif value[:2] == 'pm':
            label = 'PM'
            
        else:
            raise ValueError('Column contain unknown id.')
            
        array.append(label)
        
    return array