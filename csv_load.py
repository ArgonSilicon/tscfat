# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .csv files in a given folder. The files are loaded as pandas 
dataframes which are stored in a list. All the subfolders in the given 
folder are ignored. In (the future version) addition, .xls and .xlsx files are supported.
If there is file of a type other than those in the folder, an exception 
is raised.

"""

from __future__ import print_function
import pandas as pd
from pathlib import Path
import itertools
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .csv file.

    Parameters
    ----------
    openname : WindowsPath 
        path to the .csv file

    Returns
    -------
    df: dataframe
        a pandas dataframe created from the read csv file

    """
    
    try:
        with open(open_name, "r") as read_file:
            df = pd.read_csv(read_file)
            return df
    except IOError:
        print("Cannot open the file.")
    
def load_all_subjects(foldername):
    """
    Loads all .csv files in a given folder.

    Parameters
    ----------
    foldername : WindowsPath 
        path to the folder containing .csv files

    Returns
    -------
    json_list: list 
        a list containing readed .csv files

    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        
    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
    csv_list = []
    
    for filename in file_list:
        assert filename[-4:] == ".csv", "Trying to load incorrect file format."
        open_name = foldername / filename
        csv_list.append(load_one_subject(open_name))
         
    if csv_list:
        return csv_list
    else:
        raise Exception("There is no files in the selected folder.")


if __name__ == "__main__":
    # give the correct folder here
    DATA_FOLDER = Path("G:/SpecialAssignment/StudentLife/dataset/call_log/")
    csv = load_all_subjects(DATA_FOLDER)
    