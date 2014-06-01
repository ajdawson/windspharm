Changelog
=========


v1.3.x
------

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
