Toolbox installation, dependencies, and virtual environment
===========================================================

Installation
------------

There are two ways to install the toolbox:

1. Pip install via The Python Package Index `PyPi <https://pypi.org/>`_
2. `Cloning <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository/>`_ the project from `GitHub <https://github.com/>`_ repository

1. Pip install
^^^^^^^^^^^^^^


Pip install::

	pip install tscfat
	

2. Cloning the repository
^^^^^^^^^^^^^^^^^^^^^^^^^

The source code is currently hosted on GitHub at: <https://github.com/ArgonSilicon/tscfat/>. To clone the repository, open the terminal and change your current working directory to the location where you want to clone the repository directory. Then type in the following clone command::

	git clone https://github.com/ArgonSilicon/tscfat
	
The cloned respository should have the following folder structure::

	tscfat
	├── Data
	├── Docs
	├── Examples
	├── Results
	├── Tests
	├── __pycache__
	├── _build
	├── dist
	├── tscfat
	└── tscfat.egg-info
	
Here the most important subfolders are:
	 
	* Data folder contains example data sets
	* Docs folder contains the toolbox documentation
	* Examples folder contain example scripts for toolbox tutorials
	* Results is the default analysis output folder 
	* Tests contains pytest tests
	* tscfat contains the Python modules and utility functions needed for the analysis
	
	
Dependencies
------------

The toolbox requires Python version 3.7. or higher to work. In addition, it is depenedent on the following packages:

* `Pandas <https://pandas.pydata.org/>`_
* `Numpy <https://numpy.org/>`_
* `Matplotlib <https://matplotlib.org/>`_
* `Statsmodels <https://www.statsmodels.org/stable/index.html>`_
* `Sklearn <https://scikit-learn.org/stable/>`_
* `Tslearn <https://tslearn.readthedocs.io/en/stable/>`_
* `Nolds <https://pypi.org/project/nolds/>`_
* `Pytest <https://docs.pytest.org/en/stable/>`_
* `Seaborn <https://seaborn.pydata.org/>`_

Virtual environment
-------------------

Requirements can be fullfilled by using the `Pipenv <https://pipenv.pypa.io/en/latest/>`_ virtual environment bundled with the toolbox.

Pipenv can be installed by using pip install::
	
	pip install pipenv
	
Virtual environment activation (in the tscfat root folder)::

	pipenv install
	
Running the python scripts inside the environment::

	pipenv run python <... /python_script.py>
	
Running unit tests
------------------

Inside the tscfat root folder, you may run pytest unittests using the activated virtual environment::

	pipenv run pytest

