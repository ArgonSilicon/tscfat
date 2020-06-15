# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .csv files in a given folder. The files are loaded as pandas 
dataframes which are stored in a ictionary. All the subfolders in the given 
folder are ignored. If there is file of a type other than csv in the folder, 
an exception is raised.

"""

from __future__ import print_function
import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .csv file.

    Parameters
    ----------
    openname : Path -object
        path to the .csv file

    Returns
    -------
    file_name : str
        Name of the given file without suffix
    df: dataframe
        a pandas dataframe created from the read csv file

    """
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file)
        file_name = open_name.stem
        return file_name, df
    
    
def load_all_subjects(foldername):
    """
    Loads all .csv files in a given folder.

    Parameters
    ----------
    foldername : Path -object
        path to the folder containing .csv files

    Returns
    -------
    csv_dict : dictionary 
        a dictionary containing readed .csv files, 
        filenames used as dict keys.

    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        
    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
    csv_dict = {}
    
    for filename in file_list:
        open_name = foldername / filename
        assert open_name.suffix == ".csv", "Trying to load incorrect file format."
        file_name, csv_file = load_one_subject(open_name)
        csv_dict[file_name] = csv_file
    
    
    if csv_dict:
        return csv_dict
    else:
        raise Exception("There is no files in the selected folder.")
       
        
if __name__ == "__main__":
    # give the correct folder here
    DATA_FOLDER = Path(r'C:/Users/arsii/Documents/Work/StudentLife/dataset/call_log/')
    csv = load_all_subjects(DATA_FOLDER)
    