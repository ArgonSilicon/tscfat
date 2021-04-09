#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:26:36 2021

@author: ikaheia1

A helper class for storing the parameters used in the analysis.
The parameters are stored in the __dict__ dictionary by using an alias name as 
the key.
 
"""

class AnalysisParameters(object):
    
    def list_parameters(self):
        """
        Return a dictionaty containing the key : value pairs used as function
        parameters.

        Returns
        -------
        names : dict
            key : value pairs used as function arguments.
            
        """
        names = {}
        for key, value in self.__dict__.items():
            names[key] = value
        return names
        
        
    def add(self,alias,parameter):
        """
        Adds a new key : value pair in __dict__ dictionary. 

        Parameters
        ----------
        alias : str
            Alias name / key for the parameter 
        parameter : str / int / list
            A parameter used as an argument for analysis functions.

        Returns
        -------
        None.

        """
        self.__dict__[alias] = parameter