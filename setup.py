#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:06:42 2021

@author: arsii
"""

from distutils.core import setup

setup(
  name = 'tscfat',         
  packages = ['tscfat'],   
  version = '0.0.1',      
  license='MIT',        
  description = 'A time series co-fluctuation analysis toolbox',   
  author = 'Arsi Ikaheimonen',                   
  author_email = 'arsi.ikaheimonen@gmail.com',      
  url = 'https://github.com/ArgonSilicon/tscfat',   
  download_url = 'https://github.com/ArgonSilicon/tscfat/archive/refs/tags/V0.0.1.tar.gz',
  keywords = ['Timeseries', 'Exploratory', 'Analysis'],  
  install_requires=['nolds',
                    'sklearn',
                    'pytest',
                    'numpy',
                    'matplotlib',
                    'pandas',
                    'statsmodels',
                    'tslearn'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Researchers',      
    'Topic :: Mood research :: Time series analysis', #?
    'License :: OSI Approved :: MIT License',   #P
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
