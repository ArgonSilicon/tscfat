# Time series co-fluctuation analysis toolbox.
A python Toolbox for time series exploratory data analysis.

[![PyPI version](https://badge.fury.io/py/tscfat.svg)](https://badge.fury.io/py/tscfat)
[![Documentation Status](https://readthedocs.org/projects/tscfat/badge/?version=latest)](https://tscfat.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/kevchn/travis-ci-pytest.svg?branch=master)](https://travis-ci.org/kevchn/travis-ci-pytest)
[![codecov](https://codecov.io/gh/ArgonSilicon/tscfat/branch/master/graph/badge.svg?token=6OG1W7LQPM)](https://codecov.io/gh/ArgonSilicon/tscfat)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


## What is it for?
The toolbox is designed for exploratory data analysis of Ecological Momentaty Assesment (EMA), Experience Sampling Methods (ESM), and Digital phenotyping data. The toolbox enables the inpection of time series interaction and dynamics by providing methods for summary statistics, trend and periodicity evaluation, and linear and nonlinear dependency assesment. The emphasis of the analysis is on the visualizations. 

The toolbox has simple user interface, having a single configuration file for filenames, paths, and variables used in the analysis.

For the toolbox testing purposes, anomymized real life test data set is also provided.

## Main Features
The toolbox features include:
* Summary statistics
* Rolling windows statistics
* Time series decomposition
* Similarity analysis
   * Similarity plot
   * Novelty score
   * Stability index
* Clustering

![](header.png)

## Installation

Pip install

```sh
pip install tscfat
```

You may also [clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) the project.

The source code is currently hosted on GitHub at: <https://github.com/ArgonSilicon/tscfat/>


<!--
OS X & Linux:

```sh
pip install tscfat


Windows:

```sh
pip install tscfat
```
-->

## Dependencies
The project dependencies:
* [Pandas][pandas] 
* [Numpy][numpy]
* [Matplotlib][matplotlib]
* [Statsmodels][statsmodels]
* [Sklearn][sklearn]
* [Tslearn][tslearn]
* [Nolds][nolds]
* [Pytest][pytest]
* [Seaborn[[seaborn]



## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

After cloning, make sure that pipenv is installed:
```sh
pip install pipenv
```
Activate the virtual environment:
```sh
pipenv install 
```
Run the example file:
```sh
pipenv run python ./Examples/example_one_subject.py
```
Each analysis function can be used independently. Functions assume that the input data is expected to be in a CSV file, using the following format:

| Time          | Y_1   | Y_2   | X_1   | X_2   | ...   | X_n   |
| :-----------: |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1472677200    |  3    | 5     | 56    |  0.1  | ...   | 0.56  |
| 1472763600    |  4    | 3     | 47    |  0.1  | ...   | 0.41  |
|   :           |  :    | :     |  :    |  :    | :     |   :   |
| 1478037600    |  4    | 2     | 99    |  0.2  | ...   | 0.71  |

* The Time column contains timestamps in [unix][unix] format.
* Rest of the columns contain observations, which should be in numerical format. Each column represents one variable, rows correspond to the sampling timepoint. 

For more examples and usage, please refer to the [Docs][docs].
<!--
## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```
-->

## Release History

* 0.0.1
    * Initial version, WIP

## Meta

Arsi Ikäheimonen – arsi.ikaheimonen@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/ArgonSilicon/tscfat](https://github.com/ArgonSilicon/)

## Contributing

1. Fork it (<https://github.com/ArgonSilicon/tscfat/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's 
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics -->
[docs]: https://tscfat.readthedocs.io/en/latest/index.html
[unix]: https://en.wikipedia.org/wiki/Unix_time
[pandas]: https://pandas.pydata.org/
[numpy]: https://numpy.org/
[matplotlib]: https://matplotlib.org/
[statsmodels]: https://www.statsmodels.org/stable/index.html
[sklearn]: https://scikit-learn.org/stable/
[tslearn]: https://tslearn.readthedocs.io/en/stable/
[nolds]: https://pypi.org/project/nolds/
[pytest]: https://docs.pytest.org/en/stable/
[seaborn]: https://seaborn.pydata.org/
