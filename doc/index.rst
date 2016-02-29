.. default-role:: py:obj

.. toctree::
   :maxdepth: 2
   :hidden:

   userguide/index
   examples/index
   api/index
   downloads


Introduction
============

`windspharm` is a Python package for performing computations on global wind fields in spherical geometry. It provides a high level interface for computations using spherical harmonics. `windspharm` is capable of computing the following quantities from an input vector wind:

* divergence

* vorticity (relative and absolute)

* streamfunction

* velocity potential

* irrotational and non-divergent components of the wind (Helmholtz decomposition)

* vector gradient of a scalar function

* magnitude (wind speed)


Download & Installation
-----------------------

Released versions of `windspharm` can be downloaded from the :doc:`downloads` page.
You must have setuptools_ installed in order to install `windspharm`.
After downloading the source code archive, unzip it and change into the unzipped archive's directory, then to install it:

.. code-block:: bash

   $ python setup.py install

`windspharm` can also be installed from PyPI using pip:

.. code-block:: bash

   $ pip install windspharm

Releases are also available via conda_ and binstar_, packages are built for both Python 2 and 3 on Linux and OSX:

.. code-block:: bash

   $ conda install -c ajdawson windspharm

You can also check out the source code for the development version from the `github repository <https://github.com/ajdawson/windspharm>`_ to access features which are not yet in the released version.

.. note::

   When installing via pip it may appear that the installation has hung.
   However, it is likely that pip is just trying to install the dependency pyspharm, whose setup process requires the user to accept a license.
   If you think your install has hung, try typing *yes* and pressing enter, the install should continue after a short pause (but know that in doing so you are accepting the terms of the Spherepack license: http://www2.cisl.ucar.edu/resources/legacy/spherepack/license).


Getting Started
---------------

The `windspharm` package provides several interfaces for performing computations.
The `windspharm.standard` interface is designed to work with `numpy` arrays; the `windspharm.iris` interface is designed to work with `iris` cubes; the `windspharm.cdms` interface is designed to work with `cdms2` variables; and the `windspharm.xarray` interface works with the `xarray` package.
Each interface supports exactly the same sets of operations, the only differences are that the `windspharm.iris`, `windspharm.cdms`, and `windspharm.xarray` interfaces also use the meta-data stored in input variables to construct outputs with meta-data.

Regardless of which interface you use, the basic usage is the same. All computation is handled by the `windspharm.standard.VectorWind`, `windspharm.iris.VectorWind`, `windspharm.cdms.VectorWind` or `windspharm.xarray.VectorWind` classes. These classes are initialized with global vector wind components. Method calls are then used to return quantities of interest.

The following is a very simple illustrative example which computes the streamfunction and vorticity associated with a global vector wind field using the `iris` interface:

.. code-block:: python

   import iris
   from windspharm.iris import VectorWind


   # Read u and v wind components from file.
   u = iris.load_cube('uwind_file.nc')
   v = iris.load_cube('vwind_file.nc')

   # Create an instance of the VectorWind class to do the computations.
   w = VectorWind(u, v)

   # Call methods to compute streamfunction and relative vorticity.
   psi = w.streamfunction()
   xi = w.vorticity()


Requirements
------------

This package requires as a minimum that you have numpy_ and pyspharm_ available, and requires setuptools_ for installation.
It is recommended that you use pyspharm version 1.0.8 or later, versions of pyspharm prior to 1.0.7 should not be used at all due to a serious bug.
The `windspharm.iris` interface can only be used if the `iris` package is available (see the iris_ documentation).
The `windspharm.cdms` interface can only be used if the `cdms2` module is available. This module is distributed as part of the UVCDAT_ project.
The `windspharm.xarray` interface can only be used if the `xarray` package is available (see the xarray_ documentation).


.. warning::

   It is strongly recommended to use pyspharm 1.0.8 or later.
   There is a bug in versions prior to 1.0.7 that causes incorrect fields to be returned when there is more than one input field, and a small bug in version 1.0.7 that causes problems with fields with a singleton time dimension.


Developing and Contributing
---------------------------

All development is done through `Github <http://github.com/ajdawson/windspharm>`_. To check out the latest sources run:

.. code-block:: bash

   $ git clone git://github.com/ajdawson/windspharm.git

It is always a good idea to run the tests during development, to do so:

.. code-block:: bash

   $ cd windspharm
   $ nosetests

Running the tests requires nose_.

Bug reports and feature requests should be filed using the Github issues_ system.
If you have code you would like to contribute, fork the `repository <http://github.com/ajdawson/windspharm>`_ on Github, do the work on a feature branch of your fork, push your feature branch to *your* Github fork, and send a pull request.


.. _UVCDAT: http://uvcdat.llnl.gov/

.. _iris: http://scitools.org.uk/iris

.. _xarray: http://xarray.pydata.org

.. _numpy: http://numpy.scipy.org

.. _pyspharm: https://code.google.com/p/pyspharm

.. _cdat-lite: http://proj.badc.rl.ac.uk/cedaservices/wiki/CdatLite

.. _nose: https://nose.readthedocs.org/en/latest/

.. _setuptools: https://pypi.python.org/pypi/setuptools

.. _issues: http://github.com/ajdawson/windspharm/issues?state=open

.. _windspharm: http://ajdawson.github.com/windspharm

.. _conda: http://conda.pydata.org/docs/

.. _binstar: https://binstar.org
