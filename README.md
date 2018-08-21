windspharm - spherical harmonic vector wind analysis in Python
==============================================================

[![Build Status](https://api.travis-ci.org/repositories/ajdawson/windspharm.svg?branch=master)](https://travis-ci.org/ajdawson/windspharm) [![DOI (paper)](https://img.shields.io/badge/DOI%20%28paper%29-10.5334%2Fjors.129-blue.svg)](http://doi.org/10.5334/jors.129) [![DOI (latest release)](https://zenodo.org/badge/20448/ajdawson/windspharm.svg)](https://zenodo.org/badge/latestdoi/20448/ajdawson/windspharm)

Overview
--------

`windspharm` is a Python package for computing quantities derived from global wind
fields using spherical harmonics, licensed under the MIT license.
windspharm provides a user-friendly interface for vector wind computations on the
sphere (e.g., divergence, streamfunction etc.). It is based on the
[pyspharm](https://github.com/jswhit/pyspharm) module.
windspharm provides a replacement for the windfield package from CDAT.


Requirements
------------

`windspharm` only requires [`numpy`](http://numpy.org) and [`pyspharm`](https://github.com/jswhit/pyspharm) (version 1.0.8 or higher), but for full functionality (meta-data interfaces) one or more of [`iris`](http://scitools.org.uk/iris/), [`xarray`](http://xarray.pydata.org) or the `cdms2` module (from [UV-CDAT](http://uvcdat.llnl.gov) is required.
The setuptools package is required for installation.
windspharm runs on Python 2 and 3.


Documentation
-------------

Documentation is available [online](http://ajdawson.github.io/windspharm).
The package docstrings are also very complete and can be used as a source of reference when working interactively.


Citation
--------

If you use windspharm in published research, please cite it by referencing the [peer-reviewed paper](http://doi.org/10.5334/jors.129).
You can additionally cite the [Zenodo DOI](https://zenodo.org/badge/latestdoi/20448/ajdawson/windspharm) if you need to cite a particular version (but please also cite the paper, it helps me justify my time working on this and similar projects).


Frequently asked questions
--------------------------

* **Do I need UV-CDAT/iris/xarray to use windspharm?**
  No. All the computation code uses numpy only. The iris, xarray and  cdms2 modules are only required for the meta-data preserving interfaces.
* **Is windspharm a drop in replacement for windfield?**
  No. Because windspharm was written from scratch the naming conventions for methods
  are different. Some new methods have been added compared to windfield, and some
  methods from windfield do not exist in windspharm.


Installation
------------

The easiest way to install is via [conda](http://conda.pydata.org):

    conda install -c conda-forge windspharm

You can also install from the source distribution.
Download the archive, unpack it, then enter the source directory and use:

    python setup.py install
