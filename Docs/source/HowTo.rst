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

STL_decomposition function decomposes the given timeseries into **trend**, **seasonal**, and **residual** components.

The example code::

	"""
	Created on Thu Apr  1 14:41:53 2021
	
	@author: arsii
	"""

	import pandas as pd

	from tscfat.Analysis.decompose_timeseries import STL_decomposition
		
	# load a dataframe and convert the index to datetime
	df = pd.read_csv('/home/arsii/tscfat/Data/Test_data.csv',index_col=0)
	df.index = pd.to_datetime(df.index)
		
	# timeseries has to be a numpy array
	series = df.level.values
		
	_ = STL_decomposition(series,
	              		title = 'example decomposition',
	              		test = False,
	              		savepath = False,
	              		savename = False,
	              		ylabel = "Value",
	              		xlabel  = "Date",
	              		dates = False,
	              		)  
 
The output image:  

.. image:: ../images/decomposition.png
  :width: 800
  :alt: Alternative text
  
     
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

The example code::

	import pandas as pd

	from tscfat.Analysis.rolling_statistics import rolling_statistics
	
	# load a dataframe and convert the index to datetime
	df = pd.read_csv('/home/arsii/tscfat/Data/one_subject_data.csv',index_col=0)
	df.index = pd.to_datetime(df.index)
	
	# dataframe can contain only one column
	df = df.filter(['positive'])
	
	# rolling window length
	window = 14

	_ = rolling_statistics(df,
		               window,
		               doi = None,
		               savename = False,
		               savepath = False,
		               test = False,
		               )

The output image:

.. image:: ../images/rolling.png
  :width: 800
  :alt: Alternative text
  
Summary Statistics
------------------





