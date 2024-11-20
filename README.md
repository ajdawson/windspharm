windspharm - spherical harmonic vector wind analysis in Python
==============================================================

[![DOI (paper)](https://img.shields.io/badge/DOI%20%28paper%29-10.5334%2Fjors.129-blue.svg)](http://doi.org/10.5334/jors.129) [![DOI (latest release)](https://zenodo.org/badge/4715033.svg)](https://zenodo.org/records/1401190)

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

`windspharm` only requires [`numpy`](http://numpy.org) and [`pyspharm`](https://github.com/jswhit/pyspharm) (version 1.0.9 or higher), but for full functionality (meta-data interfaces) one or both of [`iris`](http://scitools.org.uk/iris/) and/or [`xarray`](http://xarray.pydata.org) are required.


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

* **Do I need iris/xarray to use windspharm?**
  No. All the computation code uses numpy only. The iris and/or xarray modules are only required for the meta-data preserving interfaces.
* **Is windspharm a drop in replacement for windfield?**
  No. Because windspharm was written from scratch the naming conventions for methods
  are different. Some new methods have been added compared to windfield, and some
  methods from windfield do not exist in windspharm.


Installation
------------

The easiest way to install is via [conda](http://conda.pydata.org):

    conda install -c conda-forge windspharm

You can also install with pip::

    python -m pip install windspharm

> [!CAUTION]
> Make sure you already have pyspharm dependency installed, as it may fail to install if pip tries to do it.
