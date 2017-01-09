Changelog
=========


v1.5.x
------

:Release: v1.5.1
:Date: 9 January 2017

* Improved recognition of Gaussian grids [`#78 <https://github.com/ajdawson/windspharm/issues/78>`_, `#76 <https://github.com/ajdawson/windspharm/pull/76>`_, `#79 <https://github.com/ajdawson/windspharm/pull/79>`_].

:Release: v1.5.0
:Date: 27 April 2016

* Added a keyword argument to control the radius of the sphere used in the spherical harmonic computations. The `rsphere` keyword is available for all interfaces.


v1.4.x
------

:Release: v1.4.0
:Date: 1 March 2016

* Added an `xarray <http://xarray.pydata.org>`_ interface allowing use of `windspharm` with `xarray.DataArray` objects.
* Fixed a bug in the identification of Gaussian grids in the iris interface.
* Fixed a bug where the `truncate` method would not work on inverted latitude grids in the iris interface.


v1.3.x
------

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


v1.2.x
------

:Release: v1.2.1
:Date: 8 August 2013

* Fixed error in the iris interface where cubes with a south-north latitude dimension
  could not be used [`#22 <https://github.com/ajdawson/windspharm/pull/22>`_].

:Release: v1.2.0
:Date: 20 May 2013

* Prevented possible double copying of data in `order_latdim` [`#16 <https://github.com/ajdawson/windspharm/pull/16>`_].
* Refactored test suite and added more test coverage [`#14 <https://github.com/ajdawson/windspharm/pull/14>`_].
* Fixed bug in calculation of the magnitude of a vector wind [`#13 <https://github.com/ajdawson/windspharm/pull/13>`_, `#11 <https://github.com/ajdawson/windspharm/issues/11>`_].


v1.1.x
------

:Release: v1.1.0
:Date: 10 January 2013

* First release.
