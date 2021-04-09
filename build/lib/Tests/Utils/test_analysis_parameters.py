#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:04:32 2021

@author: ikaheia1

Test for analysis paramters class.

"""

from tscfat.Utils.analysis_parameters import AnalysisParameters

class TestAnalysisParameters(object):
    
    def test_add(self):
        """
        Test add method.

        Returns
        -------
        None.

        """
        
        ap = AnalysisParameters()
        ap.add("alias","value")
        
        assert ap.alias == 'value'
        
        
    def test_list_parameters(self):
        """
        Test list_parameters method.

        Returns
        -------
        None.

        """
        ap = AnalysisParameters()
        ap.add('alias_1', 'value_1')
        ap.add('alias_2', 'value_2')
        
        assert ap.list_parameters() == {'alias_1': 'value_1', 'alias_2': 'value_2'}