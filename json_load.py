# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .json files in a given folder. The files are stored in a list.
All the subfolders in the given folder are ignored. If there is file of 
a type other than .json in the folder, an exception is raised.

"""

from __future__ import print_function
import json
from pathlib import Path
import itertools
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .json file.

    Parameters
    ----------
    openname : WindowsPath 
        path to the .json file

    Returns
    -------
    json_file: dict
        a dictionary based on the read json file

    """
    
    try:
        with open(str(open_name), "r") as read_file:
            json_file = json.load(read_file)
            return json_file
    except IOError:
        print("Cannot open the file.")
    
def load_all_subjects(foldername):
    """
    Loads all .json files in a given folder.

    Parameters
    ----------
    foldername : WindowsPath 
        path to the folder containing .json files

    Returns
    -------
    json_list: list 
        a list containing readed .json files

    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        #file_list = listdir(foldername)
    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
    json_list = []
    
    for filename in file_list:
        assert filename[-5:] == ".json", "Trying to load incorrect file format."
        open_name = foldername / filename
        json_list.append(load_one_subject(open_name))
         
    if json_list:
        return json_list
    else:
        raise Exception("There is no files in the selected folder.")


if __name__ == "__main__":
    # give the correct folder here
    DATA_FOLDER = Path("G:/SpecialAssignment/Json_test/files/")
    json_list = load_all_subjects(DATA_FOLDER)
    json_list = list(itertools.chain.from_iterable(json_list))