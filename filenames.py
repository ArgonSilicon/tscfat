#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 12:08:28 2020

@author: ikaheia1
"""
from pathlib import Path
import pytest

class FileNames(object):
    """
    """
    def __init__(self, work_dir,data_folder,figpath):
        assert isinstance(work_dir, Path), "Given argument is not a Path object"
        assert isinstance(data_folder, Path), "Given argument is not a Path object"
        assert isinstance(figpath, Path), "Given argument is not a Path object"
        
        self.work_dir = work_dir
        self.data_folder = data_folder
        self.figpath = figpath
        
    def __repr__(self):
        return "FileNames:\n{}\n{}\n{}\n".format(self.work_dir,self.data_folder,self.figpath)
        
    def __str__(self):
        return "From str method of FileNames:\n{}\n{}\n{}\n".format(self.work_dir,self.data_folder,self.figpath)


def test_proper_paths():
    # define proper path objects
    test_arguments = (Path(r'C:/'),Path(r'C:/'),Path(r'C:/'))
    fn = FileNames(*test_arguments)
    assert isinstance(fn,FileNames), "fn is not a Filenames object" 
    assert fn.data_folder is not None
    assert fn.figpath is not None
    assert fn.work_dir is not None

      
def test_improper_paths():
    # define proper path objects
    test_arguments = (Path(r'C:/'),Path(r'C:/'),"c:/")
    # Store information about raised ValueError in exc_info
    with pytest.raises(AssertionError) as exc_info:
        FileNames(*test_arguments)
    expected_error_msg = "Given argument is not a Path object"
    # Check if the raised ValueError contains the correct message
    assert exc_info.match(expected_error_msg)