HowTo
=====

This section describes how to run each analysis function independently.

Calculate similarity
--------------------

Calculate Novelty
-----------------

Calculate Stability
-------------------

Plot Similarity
---------------

Timeseries Decomposition
------------------------

The following is a code block::

	"""
	Created on Thu Apr  1 14:41:53 2021

	@author: arsii
	"""

	import pandas as pd

	from tscfat.Analysis.decompose_timeseries import STL_decomposition

	df = pd.read_csv('/home/arsii/tscfat/Data/Test_data.csv',index_col=0)
	df.index = pd.to_datetime(df.index)

	_ = STL_decomposition(df.level.values,
                      		title = 'example decomposition',
                      		test = False,
                      		savepath = False,
                      		savename = False,
                      		ylabel = "Value",
                      		xlabel  = "Date",
                      		dates = False,
                      		)  
      
      
Timeseries Clustering
---------------------

Degree of Distribution
----------------------

Fluctuation Intensity
---------------------

Plot Timeseries
---------------

Rolling Statistics
------------------

Summary Statistics
------------------





