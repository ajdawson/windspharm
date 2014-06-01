windspharm - spherical harmonic vector wind analysis in Python
==============================================================


Overview
--------

``windspharm`` is a Python package for computing quantities derived from global wind
fields using spherical harmonics, licensed under the MIT license.

``windspharm`` provides a user-friendly interface for vector wind computations on the
sphere (e.g., divergence, streamfunction etc.). ``windspharm`` is based on the
[``pyspharm``](http://code.google.com/p/pyspharm/) module.

``windspharm`` provides a replacement for the ``windfield`` package from CDAT (``windfield``
was based on the ``sphere`` module, which is now deprecated).


Requirements
------------

``windspharm`` only requires ``numpy`` and ``pyspharm`` (version 1.0.8 or higher), but for full functionality (meta-data interfaces) either or both of the [``iris``](http://scitools.org.uk/iris/) module or the ``cdms2`` module is required.
The setuptools package is required for installation.
``cdms2`` is part of the Climate Data Analysis Tools ([CDAT](http://www2-pcmdi.llnl.gov/cdat)) or can be obtained separately in the [cdat_lite](http://proj.badc.rl.ac.uk/ndg/wiki/CdatLite) package.


Documentation
-------------

Documentation is available [online](http://ajdawson.github.io/windspharm). The package
docstrings are also very complete and can be used as a source of reference when working
interactively.


Frequently asked questions
--------------------------

* **Do I need CDAT/``cdms2`` or ``iris`` to use ``windspharm``?**
  No. All the computation code uses ``numpy`` only. The ``iris`` or ``cdms2`` modules
  are only required for the meta-data preserving interfaces.
* **Is ``windspharm`` a drop in replacement for ``windfield``?**
  No. Because ``windspharm`` was written from scratch the naming conventions for methods
  are different. Some new methods have been added compared to ``windfield``, and some
  methods from ``windfield`` do not exist in ``windspharm``.


Installation
------------

    python setup.py --user

to install in your home directory, or to install system wide if you have permissions:

    sudo python setup.py install
