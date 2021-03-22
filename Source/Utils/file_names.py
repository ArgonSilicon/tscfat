#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:26:36 2021

@author: ikaheia1
"""

class FileNames(object):
    
    def list_filenames(self):
        names = {}
        for key, value in self.__dict__.items():
            names[key] = value
        return names
        
        
    def add(self,alias,filename):
        self.__dict__[alias] = filename