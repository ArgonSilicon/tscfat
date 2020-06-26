#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:41:31 2020

@author: arsi
"""
from pathlib import Path
import json

def dump_to_json(result,savepath,filename):
    
    """ Convert result object to json and save it into given folder.
    """
    
    #assert isinstance(result, pyrqa.result.RQAResult), "Filetype should be numpy.ndarray."
    assert isinstance(filename,str), "Invalid savename type, should be str."
    
    if savepath.exists():
        
        save_name = savepath / filename
        
        with open(save_name, "w") as write_file:
            json.dump({"Minimum diagonal line length (L_min)": result.min_diagonal_line_length,
                           "Minimum vertical line length (V_min)": result.min_vertical_line_length,
                           "Minimum white vertical line length (W_min)": result.min_white_vertical_line_length,
                           "Recurrence rate (RR)": result.recurrence_rate,
                           "Determinism (DET)": result.determinism,
                           "Average diagonal line length (L)": result.average_diagonal_line,
                           "Longest diagonal line length (L_max)": int(result.longest_diagonal_line),
                           "Divergence (DIV)": result.divergence,
                           "Entropy diagonal lines (L_entr)": result.entropy_diagonal_lines,
                           "Laminarity (LAM)": result.laminarity,
                           "Trapping time (TT)": result.trapping_time,
                           "Longest vertical line length (V_max)": int(result.longest_vertical_line),
                           "Entropy vertical lines (V_entr)": result.entropy_vertical_lines,
                           "Average white vertical line length (W)": result.average_white_vertical_line,
                           "Longest white vertical line length (W_max)": int(result.longest_white_vertical_line),
                           "Longest white vertical line length inverse (W_div)": result.longest_white_vertical_line_inverse,
                           "Entropy white vertical lines (W_entr)": result.entropy_white_vertical_lines,
                           "Ratio determinism / recurrence rate (DET/RR)": result.ratio_determinism_recurrence_rate,
                           "Ratio laminarity / determinism (LAM/DET)": result.ratio_laminarity_determinism
                          },
                          write_file,
                          sort_keys=False,
                          indent=4,
                          separators=(',', ': ')
                          )
    else:
        raise Exception("Requested folder: " + str(savepath) + " does not exist.")