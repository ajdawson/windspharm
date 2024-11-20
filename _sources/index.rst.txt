.. default-role:: py:obj

.. toctree::
   :maxdepth: 2
   :hidden:

   userguide/index
   examples/index
   api/index
   changelog
   devguide/index


Introduction
============

`windspharm` is a Python package for performing computations on global wind fields in spherical geometry. It provides a high level interface for computations using spherical harmonics. `windspharm` is capable of computing the following quantities from an input vector wind:

* divergence

* vorticity (relative and absolute)

* streamfunction

* velocity potential

* irrotational and non-divergent components of the wind (Helmholtz decomposition)

* vector gradient of a scalar function

* triangular truncation of a scalar field

* magnitude (wind speed)


Download & Installation
-----------------------

The easiest way to install is via conda_:

.. code-block:: bash

   $ conda install -c conda-forge windspharm

Released versions of `windspharm` can be downloaded from `Github <https://github.com/ajdawson/windspharm/releases>`_.
After downloading the source code archive, unzip it and change into the unzipped archive's directory, then to install it:

.. code-block:: bash

   $ python setup.py install

You can also check out the source code for the development version from the `github repository <https://github.com/ajdawson/windspharm>`_ to access features which are not yet in the released version.


Requirements
------------

This package requires as a minimum that you have numpy_ and pyspharm_ available.
The `windspharm.iris` interface can only be used if the `iris` package is available (see the iris_ documentation).
The `windspharm.xarray` interface can only be used if the `xarray` package is available (see the xarray_ documentation).


Getting Started
---------------

The `windspharm` package provides several interfaces for performing computations.
The :ref:`standard <standard-interface>` interface is designed to work with `numpy` arrays.
On top of this are layers desinged to work with more advanced data structures that also contain metadata.
Currently there is support for :ref:`iris cubes <iris-interface>` and :ref:`xarray DataArrays <xarray-interface>`.

Regardless of which interface you use, the basic usage is the same. All computation is handled by a `VectorWind` instance initialized with global vector wind components. Method calls are then used to return quantities of interest.

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


Citation
--------

If you use windspharm in published research, please cite it by referencing the `peer-reviewed paper <http://doi.org/10.5334/jors.129>`_.
You can additionally cite the `Zenodo DOI <https://zenodo.org/records/1401190>`_ if you need to cite a particular version (but please also cite the paper, it helps me justify my time working on this and similar projects).


Developing and Contributing
---------------------------


Contributions big or small are welcomed from anyone with an interest in the project.
Bug reports and feature requests can be filed using the Github issues_ system.
If you would like to contribute code or documentation please see the :doc:`devguide/index`.


.. _iris: https://scitools-iris.readthedocs.io/en/stable

.. _xarray: https://xarray.dev

.. _numpy: https://numpy.org

.. _pyspharm: https://github.com/jswhit/pyspharm

.. _issues: https://github.com/ajdawson/windspharm/issues

.. _windspharm: https://ajdawson.github.io/windspharm

.. _conda: https://github.com/conda-forge/miniforge
