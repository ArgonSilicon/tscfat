Tutorials
=========

The toobox comes with two example datasets. The datasets can be accessed via cloning the GitHub repository or by copying directly from the GitHub repository `Data <https://github.com/ArgonSilicon/tscfat/tree/master/Data>`_ folder. The first dataset (`one_subject_data.csv <https://github.com/ArgonSilicon/tscfat/blob/master/Data/one_subject_data.csv>`_) contains multimodal data from one subject. The data contains daily aggregated, actively and passively sampled data. The second dataset (`Battery_test_data.csv <https://github.com/ArgonSilicon/tscfat/blob/master/Data/Battery_test_data.csv>`_)contains high frequency battery level data. This section contains tutorials, how to run analysis on these datasets. The most important toolbox features are covered in the tutorials.

One subject data
----------------

This tutorial assumes, that the user has already pip installed the tscfat toolbox. If the repository is cloned, it should contain the following subfolders::

	tscfat
	└── Results
	    ├── Clustering
	    ├── Decomposition
	    ├── RollingStatistics
	    ├── Similarity  
	    ├── Summary
	    └── Timeseries        
    
These are the folders, where the result figures are saved. If you do not wish to clone the repository, make sure that you create the folders for output figures.

The examples python scripts are located at the GitHub repository `Examples <https://github.com/ArgonSilicon/tscfat/tree/master/Examples>`_ folder. These are also included in the cloned respository under tscfat/Examples::
	
	Examples
	├── config.py
	├── config_clustering.py
	├── example_clustering.py
	└── example_one_subject.py

To run the example with one subject data, config.py and example_one_subject.py files should be kept in the same folder.
 
Examples folder contains a file config.py. Open it in a text editor and replace following paths.

Fill in the correct path for output directory::

	# The directory where output figures are stored
	OUTPUT_DIR = Path(' ... /tscfat/Results') # <- replace with correct path!
	
Fill in the correct path for data loading::

	# Path or Url to the data file to be imported
	CSV_PATH = Path(' ... /tscfat/Data/one_subject_data.csv') 
	
By the default, the example data will be loaded from the GitHub repository::

	# Path or Url to the data file to be imported
	CSV_PATH = "https://raw.githubusercontent.com/ArgonSilicon/tscfat/master/Data/Battery_test_data.csv"

If you have cloned the repository, you may run the example file from the tscfat root folder::

	python ./Examples/example_one_subject.py

The script will run analysis on each of the dataset columns, saving the resulting figures in dedicated folders.

You can use your own data, by changing the input data path (CVS_PATH). The input data is expected to be in a CSV file, using the following format:

+---------------+-------+-------+-------+-------+-------+-------+
| Time          | Y_1   | Y_2   | X_1   | X_2   | ...   | X_n   |
+===============+=======+=======+=======+=======+=======+=======+
| 1472677200    |  3    | 5     | 56    |  0.1  | ...   | 0.56  |
+---------------+-------+-------+-------+-------+-------+-------+
| 1472763600    |  4    | 3     | 47    |  0.1  | ...   | 0.41  |
+---------------+-------+-------+-------+-------+-------+-------+
|   :           |  :    | :     |  :    |  :    | :     |   :   |
+---------------+-------+-------+-------+-------+-------+-------+
| 1478037600    |  4    | 2     | 99    |  0.2  | ...   | 0.71  |
+---------------+-------+-------+-------+-------+-------+-------+

* The Time column contains timestamps in `Unix <https://en.wikipedia.org/wiki/Unix_time>`_ time format. The timestamps should be uniformly distributed.
* Rest of the columns contain observations, which should be in numerical format. Each column represents one variable, rows correspond to the sampling timepoint. Make sure to impute any missing datapoints before running the analysis.

Each analysis function can also be used independently. For more examples and usage, please refer to the HowTo section.


Clustering example
------------------

tscfat/Examples folder contain a file config_clustering.py. To run the clustering example, config_clustering.py and example_clustering.py should be kept in the same folder. 

Open the config_clustering.py in a text editor and replace the following paths.

If you have the data stored locally, fill in the correct path for data loading::
	
	# DATA LOADING:
	# Path to the data file to be imported
	CSV_PATH = Path(' ... /tscfat/Data/Battery_test_data.csv')

By the default, the example data will be loaded from the GitHub repository::

	# DATA LOADING:
	# Path to the data file to be imported
	CSV_PATH = "https://raw.githubusercontent.com/ArgonSilicon/tscfat/master/Data/Battery_test_data.csv"


Fill in the correct path for the output directory::

	# TIMESERIES CLUSTERING
	# Output folder for similarity plot
	CLUSTERING_OUT = Path(' ... /tscfat/Results/Clustering') 
	
If you have cloned the repository, you may run the example file from the tscfat root folder::

	python ./Examples/example_clustering.py

The script will run clustering analysis on dataset, saving the resulting figures in dedicated folders.


