#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:06:42 2021

@author: arsii
"""

from distutils.core import setup

setup(
  name = 'tscfat',  
  package_dir = {'':'tscfat'},       
  packages = ['Analysis','Utils'],
  version = '0.0.5',      
  license='MIT',        
  description = 'A time series co-fluctuation analysis toolbox', 
  author = 'Arsi Ikaheimonen',                   
  author_email = 'arsi.ikaheimonen@gmail.com',      
  url = 'https://github.com/ArgonSilicon/tscfat',   
  download_url = 'https://github.com/ArgonSilicon/tscfat/archive/refs/tags/0.0.5.tar.gz',
  keywords = ['Timeseries', 'Exploratory', 'Analysis'],
  include_package_data=True,  
  install_requires=['nolds',
                    'sklearn',
                    'pytest',
                    'numpy',
                    'matplotlib',
                    'pandas',
                    'statsmodels',
                    'tslearn',
                    'seaborn'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Scientific/Engineering :: Medical Science Apps.', 
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
