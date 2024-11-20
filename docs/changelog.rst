Changelog
=========

Source code downloads for released versions can be downloaded from `Github <https://github.com/ajdawson/windspharm/releases>`_.

v2.0
----

:Release: v2.0.0

The v2.0.0 release removes the cdms interface. The cdms2 package is no longer maintained and therefore support has been dropped.


v1.7
----

:Release: v1.7.0
:Date: 21 August 2018

The v1.7.0 release makes further progress on the road to more modern tooling and processes. The significant changes for users/contributors are:

* Support for using Legendre functions computed on-the-fly or stored, implemented by `@rcomer <https://github.com/rcomer>`_ [:issue:`97`, :pr:`98`].
* The source code directories have been reorganised, the ``lib/windspharm`` directory has been moved to ``windspharm/`` (``lib/`` is removed) and the ``doc/`` directory has been renamed ``docs/`` [:pr:`105`].
* The package version is now controlled by `versioneer <https://github.com/warner/python-versioneer>`_.

In addition, this is the first release where documentation and PyPI packages will be built automatically as part of the continuous integration system.


v1.6
----

:Release: v1.6.0
:Date: 9 May 2018

This release has no major user-facing changes, its main purpose is to modernise the test suite and fix problems with NumPy compatibility, although the modifications to the test suite may have knock-on effects for package maintainers.

* Fixes for NumPy compatibility [:issue:`89`, :pr:`90`].
* Switch from `nose` to `pytest <http://pytest.org>`_ for the test suite [:pr:`91`, :pr:`94`].


v1.5
----

:Release: v1.5.1
:Date: 9 January 2017

* Improved recognition of Gaussian grids [:issue:`78`, :pr:`76`, :pr:`79`].

:Release: v1.5.0
:Date: 27 April 2016

* Added a keyword argument to control the radius of the sphere used in the spherical harmonic computations. The `rsphere` keyword is available for all interfaces.


v1.4
----

:Release: v1.4.0
:Date: 1 March 2016

* Added an `xarray <http://xarray.pydata.org>`_ interface allowing use of `windspharm` with `xarray.DataArray` objects.
* Fixed a bug in the identification of Gaussian grids in the iris interface.
* Fixed a bug where the `truncate` method would not work on inverted latitude grids in the iris interface.


v1.3
----

:Release: v1.3.2
:Date: 18 May 2015

* Fixed a bug in the iris and cdms interfaces that caused incorrect results to be returned from the `gradient` method if the input had a latitude dimension ordered south-north (thanks to Adrian Matthews for the report).
* Fixed the metadata of the return values from the gradient and truncate methods in the cdms interface, previously a temporary variable name would be included in the id and long_name attributes when it should have been the name of the input field.

:Release: v1.3.1
:Date: 1 June 2014

* Improved support for setuptools, users already using v1.3.0 need not upgrade to v1.3.1.

:Release: v1.3.0
:Date: 2 May 2014

* Added a method to apply spectral truncation to a scalar field.
* Basic Python3 compatibility using 2to3 (pyspharm does not yet have Python3 support but some Linux distros provide a patched package).


v1.2
----

:Release: v1.2.1
:Date: 8 August 2013

* Fixed error in the iris interface where cubes with a south-north latitude dimension
  could not be used [:pr:`22`].

:Release: v1.2.0
:Date: 20 May 2013

* Prevented possible double copying of data in `order_latdim` [:pr:`16`].
* Refactored test suite and added more test coverage [:pr:`14`].
* Fixed bug in calculation of the magnitude of a vector wind [:pr:`13`, :issue:`11`].


v1.1
----

:Release: v1.1.0
:Date: 10 January 2013

* First release.
