Tutorials
=========

The toobox comes with two test datasets. The first dataset ontains multimodal data from one subject. The data contains daily aggregated, actively and passively sampled data. The second dataset contains high frequency battery level data. This section contains tutorials, how to run analysis on the datasets. The most important toolbox features are covered in the tutorials

One subject data
----------------

First step in the tutorial is to clone the respository.

Open the terminal and change your current working directory to the location where you want to clone the repository directory. Type in the following clone command::

	git clone https://github.com/ArgonSilicon/tscfat
	
For more detailed instructions, refer the GitHub `documentation <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository/>`_. 

Make sure that the tscfat/Results folder contains the following subfolders::

	tscfat
	└── Results
	    ├── Clustering
	    ├── Decomposition
	    ├── RollingStatistics
	    ├── Similarity  
	    ├── Summary
	    └── Timeseries        
    
These are the folders, where the result figures are saved.

After repository cloning, make sure that pipenv is installed::
	
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

While in tscfat root folder, you may run the example file::

	pipenv run python ./Examples/example_one_subject.py

The script will run analyisis on each of the dataset columns, saving the resulting figures in dedicated folders.

Each analysis function can also be used independently. The input data is expected to be in a CSV file, using the following format:

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

* The Time column contains timestamps in [unix][unix] format. The timestamps should be uniformly distributed.
* Rest of the columns contain observations, which should be in numerical format. Each column represents one variable, rows correspond to the sampling timepoint. Make sure to impute any missing datapoints before running the analysis.

For more examples and usage, please refer to the HowTo section.


Clustering example
------------------
