Introduction
============

:py:mod:`windspharm` is a Python package for performing computations on global wind fields in spherical geometry. It provides a high level interface for computations using spherical harmonics. :py:mod:`windspharm` is capable of computing the following quantities from an input vector wind:

* divergence

* vorticity (relative and absolute)

* streamfunction

* velocity potential

* irrotational and non-divergent components of the wind (Helmholtz decomposition)

* vector gradient of a scalar function

* magnitude (wind speed)


Download & Installation
-----------------------

The package can be downloaded from `github <http://github.com/ajdawson/windspharm>`_. To get the latest source and install the module on your system run:

.. code-block:: bash

   $ git clone git://github.com/ajdawson/windspharm.git
   $ cd windspharm
   $ sudo python setup.py install

If you want to install in your home directory replace the last line with:

.. code-block:: bash

   $ python setup.py install --user

If you don't have ``git`` installed then you can download a zip file from the `project's code page <http://github.com/ajdawson/windspharm>`_.


Getting Started
---------------

The :py:mod:`windspharm` package currently provides three interfaces for performing computations.
The `standard` interface is designed to work with :py:mod:`numpy` arrays; the `iris` interface is designed to work with :py:mod:`iris` cubes; and the `cdms` interface is designed to work with :py:mod:`cdms2` variables.
Each interface supports exactly the same sets of operations, the only differences are that the `iris` and `cdms` interfaces also use the meta-data stored in input variables to construct outputs with meta-data.

Regardless of which interface you use, the basic usage is the same. All computation is handled by the :py:class:`windspharm.standard.VectorWind`, :py:class:`windspharm.iris.VectorWind` or :py:class:`windspharm.cdms.VectorWind` classes. These classes are initialized with global vector wind components. Method calls are then used to return quantities of interest.

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

This package requires as a minimum that you have `numpy <http://http://numpy.scipy.org/>`_ and `pyspharm <http://code.google.com/p/pyspharm/>`_ available. The `iris` interface can only be used if the :py:mod:`iris` module is available (see the `iris documentation <http://scitools.org.uk/iris/>`_). The `cdms` interface can only be used if the :py:mod:`cdms` module is available. This module is distributed as part of the `UV-CDAT <http://uv-cdat.llnl.gov>`_ project. It is also distributed as part of the `cdat_lite <http://proj.badc.rl.ac.uk/cedaservices/wiki/CdatLite>`_ package.

.. warning:: It is recommended to use pyspharm 1.0.7 or later. There is a bug in previous versions that causes incorrect fields to be returned when there is more than one input field.


Developing and Contributing
---------------------------

All development is done through the `github <http://github.com/ajdawson/windspharm>`_ system. To check out the latest sources run:

.. code-block:: bash

   $ git clone git://github.com/ajdawson/windspharm.git

Please file bug reports and feature requests using the github `issues <http://github.com/ajdawson/windspharm/issues?state=open>`_.

