Introduction
============

A python Toolbox for exploratory time series data analysis

What is it for?
---------------

The toolbox is designed for exploratory data analysis of Ecological Momentary Assesment (EMA), Experience Sampling Methods (ESM), and Digital phenotyping data. The toolbox enables the inspection of time series interaction and dynamics by providing methods for summary statistics, trend and periodicity evaluation, and linear and nonlinear dependency assesment. The emphasis of the analysis is on the visualizations. 

The toolbox has simple user interface, having a single configuration file for filenames, paths, and variables used in the analysis.

For the toolbox testing purposes, anomymized real life test data sets are availabe at the GitHub repository.

Main features
-------------

The toolbox features include:

* Summary statistics
* Rolling windows statistics
* Time series decomposition
* Similarity analysis

   * Similarity plot
   * Novelty score
   * Stability index

* Clustering

Installation
------------

Pip install::

	pip install tscfat
	
You may also [clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) the project.

The source code is currently hosted on GitHub at: <https://github.com/ArgonSilicon/tscfat/>

Dependencies
------------

The project dependencies:

* Pandas
* Numpy
* Matplotlib
* Statsmodels
* sklearn
* tslearn
* nolds
* pytest
* seaborn

Usage example
-------------

After cloning, make sure that pipenv is installed::
	
	pip install pipenv

CD into tscfat root folder and activate the virtual environment::

	pipenv install 

tscfat/Examples folder contain a file conf.py. Open it in a text editor and replace following paths.

Fill in the correct path for output directory::

	# The directory where output figures are stored
	OUTPUT_DIR = Path(' ... /tscfat/Results') # <- replace with correct path!
	
Fill in the correct path for data loading::

	# Path to the data file to be imported
	CSV_PATH = Path(' ... /tscfat/Data/one_subject_data.csv') # <- replace with the correct path!

Make sure that the tscfat/Results folder contains the following subfolders::

	tscfat
	└── Results
	    ├── Clustering
	    ├── Decomposition
	    ├── RollingStatistics
	    ├── Similarity  
	    ├── Summary
	    ├── Timeseries        
	    └── setup.py
    

While in tscfat root folder the example file::

	pipenv run python ./Examples/example_one_subject.py

Each analysis function can be used independently. Functions assume that the input data is expected to be in a CSV file, using the following format:

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

* The Time column contains timestamps in [unix][unix] format.
* Rest of the columns contain observations, which should be in numerical format. Each column represents one variable, rows correspond to the sampling timepoint. 

For more examples and usage, please refer to the [Docs][docs].

Release history
---------------

* 0.0.1

    * Initial version, WIP

Contributing
------------

1. Fork it (<https://github.com/ArgonSilicon/tscfat/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
