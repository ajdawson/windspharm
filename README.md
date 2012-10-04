windspharm - spherical harmonic vector wind analysis in Python
==============================================================


Overview
--------

``windspharm`` is a Python package for computing quantities derived from global wind
fields using spherical harmonics, licensed under the MIT license.

``windspharm`` provides a user-friendly interface for vector wind computations on the
sphere (e.g., divergence, streamfunction etc.). The package is a replacement for
 the ``windfield`` package from CDAT (``windfield`` was based on the ``sphere`` module,
which is now deprecated). ``windspharm`` is a completely new package based on the more
 up-to-date [``pyspharm``](http://code.google.com/p/pyspharm/) module.


Requirements
------------

``windspharm`` only requires ``numpy`` and ``pyspharm``, but for full functionality (meta-data interface)
the ``cdms2`` module is required. ``cdms2`` is part of the Climate Data Analysis Tools
([CDAT](http://www2-pcmdi.llnl.gov/cdat)) or can be obtained separately in the
[cdat_lite](http://proj.badc.rl.ac.uk/ndg/wiki/CdatLite) package.


Documentation
-------------

Documentation is available [online](http://ajdawson.github.com/windspharm). The package
docstrings are also very complete and can be used as a source of reference when working
interactively.


Frequently asked questions
--------------------------

* **Is ``windspharm`` a drop in replacement for ``windfield``?**
  No. Because ``windspharm`` was written from scratch the naming conventions for methods
  are different. Some new methods have been added compared to ``windfield``, and some
  methods from ``windfield`` do not exist in ``windspharm``.
* **Do I need CDAT/``cdms2`` to use ``windspharm``?**
  No. All the computation code uses ``numpy`` only. The ``cdms2`` module is only required
  for the meta-data preserving interfaces.


Installation
------------

    sudo python setup.py install

to install system-wide, or to install in a specified location:

    python setup.py install --install-lib=/PATH/TO/INSTALL/DIR

