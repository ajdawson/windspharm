Standard Interface Reference
============================

The `standard` interface is contained in the module :py:mod:`windspharm.standard`. It is designed for use with :py:mod:`numpy` arrays. Computation is done by creating an instance of the class :py:class:`windspharm.standard.VectorWind`. The :py:class:`~windspharm.standard.VectorWind` class is initialized with the eastward and northward components of the global wind field. In the `standard` interface :py:class:`~windspharm.standard.VectorWind` also takes a keyword parameter indicating the type of grid the input wind components are on.

.. autoclass:: windspharm.standard.VectorWind
   :members:

