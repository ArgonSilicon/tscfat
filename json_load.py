# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:06:32 2020

@author: arsii

<<<<<<< HEAD
Load all .json files in a given folder. The files are stored in a dictinary, 
where file names are used as keys. All the subfolders in the given folder 
are ignored. If there is file of a type other than .json in the folder, 
an exception is raised.
=======
Load all .json files in a given folder. The files are stored in a list.
All the subfolders in the given folder are ignored. If there is file of 
a type other than .json in the folder, an exception is raised.
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627

"""

from __future__ import print_function
import json
from pathlib import Path
<<<<<<< HEAD
=======
import itertools
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
from os import listdir
from os.path import isfile, join, exists
    
def load_one_subject(open_name):
    """
    Loads an arbitrary .json file.

    Parameters
    ----------
<<<<<<< HEAD
    openname : Path -object
=======
    openname : WindowsPath 
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
        path to the .json file

    Returns
    -------
<<<<<<< HEAD
    file_name : str
        Name of the given file without suffix
=======
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    json_file: dict
        a dictionary based on the read json file

    """
    
<<<<<<< HEAD
    with open_name.open('r') as read_file:
        json_file = json.load(read_file)
        file_name = open_name.stem
        return file_name, json_file
=======
    try:
        with open(str(open_name), "r") as read_file:
            json_file = json.load(read_file)
            return json_file
    except IOError:
        print("Cannot open the file.")
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    
def load_all_subjects(foldername):
    """
    Loads all .json files in a given folder.

    Parameters
    ----------
<<<<<<< HEAD
    foldername : Path -object
=======
    foldername : WindowsPath 
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
        path to the folder containing .json files

    Returns
    -------
<<<<<<< HEAD
    json_dict: dict
        a dictionary containing readed .json files, 
        filenames used as dict keys.
=======
    json_list: list 
        a list containing readed .json files
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627

    """
    
    if exists(foldername):
        file_list = [f for f in listdir(foldername) if isfile(join(foldername, f))]
<<<<<<< HEAD
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
=======
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
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
    else:
        raise Exception("There is no files in the selected folder.")


if __name__ == "__main__":
    # give the correct folder here
<<<<<<< HEAD
    DATA_FOLDER = Path(r'C:/Users/arsii/Documents/Work/Json_test/files/')
    json_dict = load_all_subjects(DATA_FOLDER)
    
    
=======
    DATA_FOLDER = Path("G:/SpecialAssignment/Json_test/files/")
    json_list = load_all_subjects(DATA_FOLDER)
    json_list = list(itertools.chain.from_iterable(json_list))
>>>>>>> 80cfa83ecf66c9904bf8fcf4ca44d6290ef33627
