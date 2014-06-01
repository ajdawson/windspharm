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


You can also check out the source code for the development version from the `github repository <https://github.com/ajdawson/windspharm>`_ to access features which are not yet in the released version.


Getting Started
---------------

The `windspharm` package currently provides three interfaces for performing computations.
The `windspharm.standard` interface is designed to work with `numpy` arrays; the `windspharm.iris` interface is designed to work with `iris` cubes; and the `windspharm.cdms` interface is designed to work with `cdms2` variables.
Each interface supports exactly the same sets of operations, the only differences are that the `windspharm.iris` and `windspharm.cdms` interfaces also use the meta-data stored in input variables to construct outputs with meta-data.

Regardless of which interface you use, the basic usage is the same. All computation is handled by the `windspharm.standard.VectorWind`, `windspharm.iris.VectorWind` or `windspharm.cdms.VectorWind` classes. These classes are initialized with global vector wind components. Method calls are then used to return quantities of interest.

The following is a very simple illustrative example which computes the streamfunction and vorticity associated with a global vector wind field using the `cdms` interface:

.. code-block:: python

   import cdms2
   from windspharm.cdms import VectorWind


   # Read u and v wind components from file.
   ncin = cdms2.open('uv_components.nc')
   u = ncin('u')
   v = ncin('v')
   ncin.close()

   # Create an instance of the VectorWind class to do the computations.
   w = VectorWind(u, v)

   # Call methods to compute streamfunction and relative vorticity.
   psi = w.streamfunction()
   xi = w.vorticity()


Requirements
------------

This package requires as a minimum that you have numpy_ and pyspharm_ available, and requires setuptools_ for installation.
It is recommended that you use pyspharm version 1.0.8 or later, versions of pyspharm prior to 1.0.7 should not be used at all due to a serious bug.
The `windspharm.iris` interface can only be used if the `iris` module is available (see the iris_ documentation).
The `windspharm.cdms` interface can only be used if the `cdms2` module is available.
This module is distributed as part of the CDAT_ project.
It is also distributed as part of the cdat-lite_ package.

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


.. _CDAT: http://uv-cdat.llnl.gov

.. _iris: http://scitools.org.uk/iris

.. _numpy: http://numpy.scipy.org

.. _pyspharm: https://code.google.com/p/pyspharm

.. _cdat-lite: http://proj.badc.rl.ac.uk/cedaservices/wiki/CdatLite

.. _nose: https://nose.readthedocs.org/en/latest/

.. _setuptools: https://pypi.python.org/pypi/setuptools

.. _issues: http://github.com/ajdawson/windspharm/issues?state=open

.. _windspharm: http://ajdawson.github.com/windspharm
