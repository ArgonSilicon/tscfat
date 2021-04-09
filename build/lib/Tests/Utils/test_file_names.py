#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:04:32 2021

@author: ikaheia1

Test for file_names class.

"""

from tscfat.Utils.file_names import FileNames

class TestFileNames(object):
    
    def test_add(self):
        """
        Test add method.

        Returns
        -------
        None.

        """
        
        fn = FileNames()
        fn.add("alias","value")
        
        assert fn.alias == 'value'
        
        
    def test_list_filenames(self):
        """
        Test list_parameters method.

        Returns
        -------
        None.

        """
        fn = FileNames()
        fn.add('alias_1', 'value_1')
        fn.add('alias_2', 'value_2')
        
        assert fn.list_filenames() == {'alias_1': 'value_1', 'alias_2': 'value_2'}