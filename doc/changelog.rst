Changelog
=========


v1.3.x
------

v1.3.0
~~~~~~

* Added a method to apply spectral truncation to a scalar field.
* Basic Python3 compatibility using 2to3 (pyspharm does not yet have Python3 support but some Linux distros provide a patched package).


v1.2.x
------

v1.2.1
~~~~~~

* Fixed error in the iris interface where cubes with a south-north latitude dimension
  could not be used [`#22 <https://github.com/ajdawson/windspharm/pull/22>`_].

v1.2.0
~~~~~~

* Prevented possible double copying of data in `order_latdim` [`#16 <https://github.com/ajdawson/windspharm/pull/16>`_].
* Refactored test suite and added more test coverage [`#14 <https://github.com/ajdawson/windspharm/pull/14>`_].
* Fixed bug in calculation of the magnitude of a vector wind [`#13 <https://github.com/ajdawson/windspharm/pull/13>`_, `#11 <https://github.com/ajdawson/windspharm/issues/11>`_].


v1.1.x
------

v1.1.0
~~~~~~

* First release.
