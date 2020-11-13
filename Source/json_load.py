# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

Load all .json files in a given folder. The files are stored in a dictinary, 
where file names are used as keys. All the subfolders in the given folder 
are ignored. If there is file of a type other than .json in the folder, 
an exception is raised.


"""

from __future__ import print_function
import json
from pathlib import Path
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .json file.

    Parameters
    ----------
    openname : Path -object
        path to the .json file

    Returns
    -------
    file_name : str
        Name of the given file without suffix


    json_file: dict
        a dictionary based on the read json file

    """

    with open_name.open('r') as read_file:
        json_file = json.load(read_file)
        file_name = open_name.stem
        return file_name, json_file

    
def load_all_subjects(foldername):
    """
    Loads all .json files in a given folder.

    Parameters
    ----------

    foldername : Path -object
        path to the folder containing .json files

    Returns
    -------

    json_dict: dict
        a dictionary containing readed .json files, 
        filenames used as dict keys.

    json_list: list 
        a list containing readed .json files


    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]

    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 
    
    json_dict = {}
    
    for filename in file_list:
        open_name = foldername / filename
        assert open_name.suffix == ".json", "Trying to load incorrect file format."
        file_name, json_file = load_one_subject(open_name)
        json_dict[file_name] = json_file
         
    if json_dict:
        return json_dict

    else:
        raise Exception("Requested folder: " + str(foldername) + " does not exist.") 

if __name__ == "__main__":
    # give the correct folder here
    DATA_FOLDER = Path(r'C:/Users/arsii/Documents/Work/Data/Json/')
    json_dict = load_all_subjects(DATA_FOLDER)

