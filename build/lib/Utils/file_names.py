#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:26:36 2021

@author: ikaheia1

A helper class for storing the filenames / paths used in the analysis.
The filenames are stored in the __dict__ dictionary by using an alias name as 
the key.

"""

class FileNames(object):
    
    def list_filenames(self):
        """
        Return a dictionaty containing the key : value pairs used as filenames
        or paths for data loading and saving the plotted figures.

        Returns
        -------
        names : dict
            key : value pairs used as filenames.
            
        """
        names = {}
        for key, value in self.__dict__.items():
            names[key] = value
        return names
        
        
    def add(self,alias,filename):
        """
        Adds a new key : value pair in __dict__ dictionary. 

        Parameters
        ----------
        alias : str
            Alias name / key for the filename
        parameter : str / Path
            A parameter used as a filename / Path for saving the figures.

        Returns
        -------
        None.

        """
        self.__dict__[alias] = filename