HowTo
=====

This section describes how to run each analysis function independently.

Calculate similarity
--------------------

The example code::
	
	"""
	Created on Sat Apr  3 23:48:38 2021

	@author: arsi
	"""

	import pandas as pd

	from tscfat.Analysis.calculate_similarity import calculate_similarity
		
	# load a dataframe and convert the index to datetime
	df = pd.read_csv('/home/arsi/Documents/tscfat/Data/one_subject_data.csv',index_col=0)
	df.index = pd.to_datetime(df.index)

	# convert one column to a numpy array
	name = 'positive'
	ser = df[name].values.reshape(-1,1)

	sim = calculate_similarity(ser)

The similarity matrix::

	print(sim)
	[[1.         0.8962963  0.8962963  ... 0.78317152 0.75467775 0.81208054]
	 [0.8962963  1.         0.81208054 ... 0.86120996 0.82687927 0.8962963 ]
	 [0.8962963  0.81208054 1.         ... 0.71810089 0.69407266 0.74233129]
	 ...
	 [0.78317152 0.86120996 0.71810089 ... 1.         0.95400788 0.95652174]
	 [0.75467775 0.82687927 0.69407266 ... 0.95400788 1.         0.91435768]
	 [0.81208054 0.8962963  0.74233129 ... 0.95652174 0.91435768 1.        ]]

Calculate Novelty
-----------------

The example code::

	import pandas as pd

Calculate Stability
-------------------

The example code::

	import pandas as pd

Plot Similarity
---------------

The example code::

	import pandas as pd

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

The example code::

	import pandas as pd
	
Degree of Distribution
----------------------
	
	import pandas as pd
	
The example code::

Fluctuation Intensity
---------------------

	
	
The example code::

	import pandas as pd


Plot Timeseries
---------------

The example code::

	"""
	Created on Fri Apr  2 12:14:27 2021

	@author: arsi
	"""

	import pandas as pd

	from tscfat.Analysis.plot_timeseries import plot_timeseries
		
	# load a dataframe and convert the index to datetime
	df = pd.read_csv('/home/arsi/Documents/tscfat/Data/one_subject_data.csv',index_col=0)
	df.index = pd.to_datetime(df.index)
		
	# A list containing column names
	cols = ['positive','negative']

	# Rolling window size
	window = 14


	_ = plot_timeseries(df,
		            cols,
		            title = 'Positive and negative affects',
		            roll = window, 
		            xlab = "Time", 
		            ylab = "Value", 
		            ylim = False, 
		            savename = False,
		            savepath = False, 
		            highlight = False, 
		            test = False
		            )

The output image:

.. image:: ../images/timeseries.png
  :width: 800
  :alt: Alternative text


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

The example code::

	import pandas as pd
	
	from tscfat.Analysis.summary_statistic import summary_statistics
	
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

.. image:: ../images/summary.png
  :width: 800
  :alt: Alternative text



