# Time series co-fluctuation analysis toolbox.
A python Toolbox for time series exploratory data analysis.

[![Documentation Status](https://readthedocs.org/projects/tscfat/badge/?version=latest)](https://tscfat.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/kevchn/travis-ci-pytest.svg?branch=master)](https://travis-ci.org/kevchn/travis-ci-pytest)
[![codecov](https://codecov.io/gh/ArgonSilicon/tscfat/branch/master/graph/badge.svg?token=6OG1W7LQPM)](https://codecov.io/gh/ArgonSilicon/tscfat)

## What is it for?
## Main Features
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

Pip install is not implemented yet. 

The source code is currently hosted on GitHub at: <https://github.com/ArgonSilicon/tscfat/>
Meanwhile you can [clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) the project.

<!--
OS X & Linux:

```sh
pip install tscfat
```

Windows:

```sh
pip install tscfat
```
-->

## Dependencies

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Docs][docs]._

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
The data is expected to be in CSV file, using the following format:

| Time          | Y_1   | Y_2   | X_1   | X_2   | ...   | X_n   |
| :-----------: |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1472677200    |  3    | 5     | 56    |  0.1  | ...   | 0.56  |
| 1472763600    |  4    | 3     | 47    |  0.1  | ...   | 0.41  |
|   :           |  :    | :     |  :    |  :    | :     |   :   |
| 1478037600    |  4    | 2     | 99    |  0.2  | ...   | 0.71  |

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

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

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
