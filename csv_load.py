# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .csv files in a given folder. The files are loaded as pandas 
<<<<<<< HEAD
dataframes which are stored in a ictionary. All the subfolders in the given 
folder are ignored. If there is file of a type other than csv in the folder, 
an exception is raised.
=======
dataframes which are stored in a list. All the subfolders in the given 
folder are ignored. In (the future version) addition, .xls and .xlsx files are supported.
If there is file of a type other than those in the folder, an exception 
is raised.
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627

"""

from __future__ import print_function
import pandas as pd
from pathlib import Path
<<<<<<< HEAD
=======
import itertools
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .csv file.

    Parameters
    ----------
<<<<<<< HEAD
    openname : Path -object
=======
    openname : WindowsPath 
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
        path to the .csv file

    Returns
    -------
<<<<<<< HEAD
    file_name : str
        Name of the given file without suffix
=======
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    df: dataframe
        a pandas dataframe created from the read csv file

    """
<<<<<<< HEAD
    with open_name.open('r') as read_file:
        df = pd.read_csv(read_file)
        file_name = open_name.stem
        return file_name, df
    
=======
    
    try:
        with open(open_name, "r") as read_file:
            df = pd.read_csv(read_file)
            return df
    except IOError:
        print("Cannot open the file.")
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    
def load_all_subjects(foldername):
    """
    Loads all .csv files in a given folder.

    Parameters
    ----------
<<<<<<< HEAD
    foldername : Path -object
=======
    foldername : WindowsPath 
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
        path to the folder containing .csv files

    Returns
    -------
<<<<<<< HEAD
    csv_dict : dictionary 
        a dictionary containing readed .csv files, 
        filenames used as dict keys.
=======
    json_list: list 
        a list containing readed .csv files
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627

    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        
    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
<<<<<<< HEAD
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
=======
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
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    csv = load_all_subjects(DATA_FOLDER)
    